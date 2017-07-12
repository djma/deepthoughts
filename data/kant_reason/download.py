import requests
import re

PURE_DIR = 'http://www.philosophy-index.com/kant/critique_pure_reason/'
PRAC_DIR = 'http://www.philosophy-index.com/kant/critique-practical-reason/'

pure = requests.get(PURE_DIR)
prac = requests.get(PRAC_DIR)

pages = re.findall(r'<a href="([^>/]*)">', pure.text)
pages = list(filter(lambda title: title.find("preface") == -1, pages))
for page in pages:
  with open("pure/" + page, 'w+') as f:
    print("downloading " + PURE_DIR + page)
    text = requests.get(PURE_DIR + page).text
    f.write(text)

pages = re.findall(r'<a href="/kant/critique-practical-reason/([^>/]+)">', prac.text)
pages = list(filter(lambda title: title.find("preface") == -1, pages))
for page in pages:
  with open("prac/" + page, 'w+') as f:
    print("downloading " + PRAC + page)
    text = requests.get(PRAC_DIR + page).text
    f.write(text)
