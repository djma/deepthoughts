import os
import re
import pickle

def getListOfParagraphs(html):
  # Uses the *? modifier for non-greedy matching
  # Ignores foot notes
  html = html.replace('\n', ' ')
  paragraphs = re.findall(r'<p>.*?</p>', html)
  return paragraphs

def filterNonCoreParagraphs(paragraphs):
  # Crude, but good enough for this dataset
  # Paragraphs shorter than 100 chars are not core
  # Paragraphs with pipes are titles
  # Paragraphs with the word Footnote are in-line footnotes
  def myfilter(p):
    return len(p) > 100 and \
           p.find("|") == -1 and \
           p.find("Footnote") == -1
  ans = filter(myfilter, paragraphs)
  return ans

def removeTagsAndSuperscripts(html):
  # Uses the *? modifier for non-greedy matching
  ans = re.sub(r'<sup>\d*</sup>', '', html)
  return re.sub(r'<.*?>', '', ans)

def my_tokenize(p):
  # html encoding
  p = re.sub(r'&#8212;', " - ", p)
  p = re.sub(r'&quot;', '"', p)
  p = re.sub(r'&ldquo;', '"', p)
  p = re.sub(r'&rdquo;', '"', p)

  # useful tokens
  p = re.sub(r'\'s', ' \'s', p)
  p = re.sub(r'i\.e\.', 'ie', p)
  p = re.sub(r'e\.g\.', 'eg', p)

  # Don't wanna start listing stuff I'm not that ambitious.
  p = re.sub(r'^[0-9]\.', '', p)
  p = re.sub(r'^ *\(.\)', '', p)
  p = re.sub(r'^ *[IVX]*\.', '', p)
  p = re.sub(r'\*', '', p)

  # Punctuation tokens
  p = re.sub(r'\[', '', p)
  p = re.sub(r'\]', '', p)
  p = re.sub(r'\.', ' . ', p)
  p = re.sub(r',', ' , ', p)
  p = re.sub(r';', ' ; ', p)
  p = re.sub(r':', ' : ', p)
  p = re.sub(r'\?', ' ? ', p)
  p = re.sub(r'"', ' " ', p)
  p = re.sub(r'\(', ' ( ', p)
  p = re.sub(r'\)', ' ) ', p)
  p = re.sub(r'--', ' - ', p)
  p = re.sub(r'\+', ' + ', p)
  p = re.sub(r'=', ' = ', p)

  return p.lower().strip().split() + ["endofparagraph"]

output_file = open("./kant_paragraphs.txt", "w+")

for foo in ["prac/" , "pure/"]:
  for _, _, files in os.walk(foo):
    for fil in files:
      with open("./" + foo + fil, 'r') as f:
        paragraphs = getListOfParagraphs(f.read())
        paragraphs = map(removeTagsAndSuperscripts, paragraphs)
        paragraphs = filterNonCoreParagraphs(paragraphs)
        paragraphs = map(my_tokenize, paragraphs)
        for p in paragraphs:
          for token in p:
            output_file.write(token + "\n")
