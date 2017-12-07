import requests
from lxml import html
import urllib.request
from bs4 import BeautifulSoup


source = urllib.request.urlopen('https://football.fantasysports.yahoo.com/f1/764476/8').read()
soup = BeautifulSoup(source,'lxml')

# title of the page
print(soup.title)

# get attributes:
print(soup.title.name)

# get values:
print(soup.title.string)

# beginning navigation:
print(soup.title.parent.name)

# getting specific values:
print(soup.p)