
import requests
from bs4 import BeautifulSoup
import json

url = 'http://office.lan:9129/repo/archlinux/'

response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

list = []
# Find all  tags with href attribute
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.sig'):
    	continue
    #trim . and /
    href = href.strip('.')
    href = href.strip('/')
    list.append(href)
    
print(list)

with open("filelist.json", "w") as fp:
	 json.dump(list, fp)