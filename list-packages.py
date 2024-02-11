
import requests
from bs4 import BeautifulSoup
import util

url = 'http://office.lan:9129/repo/archlinux/'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

list = []
# Find all  tags with href attribute
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.sig'):
    	continue
    	
    pkg = util.get_package_info(href)
    
    # db file
    if pkg == None:
    	continue
    
    list.append(pkg['name'] + ' ' + pkg['version'])

with open("packages.txt", "w") as f:
	 for line in list:
	 	print(line)
	 	f.write('%s\n' % line)