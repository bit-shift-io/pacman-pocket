
import requests
from bs4 import BeautifulSoup
import re

url = 'http://office.lan:9129/repo/archlinux/'

response = requests.get(url)
# parse html
soup = BeautifulSoup(response.content, 'html.parser')

list = []
# Find all  tags with href attribute
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.sig'):
    	continue
    # trim and tidy
    href = href.strip('.').strip('/')
    href = href.replace('%3A', ':').replace('%253A', ':')
    # get arch and ext
    archext = re.sub('.*-', '', href)
    # get package name
    pkg = re.sub('-\d.*', '', href)
    # get version
    version = href.replace(archext, '').replace(pkg,'')
    version = version[:-1][1:]
    clean = pkg + ' ' + version
    list.append(clean)
    print(clean)

with open("packages.txt", "w") as f:
	 for line in list:
	 	f.write('%s\n' % line)