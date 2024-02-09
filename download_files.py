
import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import os

mirror = ['http://ftp.iinet.net.au/pub/archlinux/core/os/x86_64/', 'http://ftp.iinet.net.au/pub/archlinux/extra/os/x86_64/']

path = os.getcwd() + '/packages/'

if not os.path.exists(path):
	os.makedirs(path)


# fn for resume downloads
def fetch(url, filename):
    with open(filename, 'ab') as f:
        headers = {}
        pos = f.tell()
        if pos:
            headers['Range'] = f'bytes={pos}-'
        response = requests.get(url, headers=headers, stream=True)
        #if pos:
        #    validate_as_you_want_(pos, response)
        total_size = int(response.headers.get('content-length'))  
        for data in tqdm(iterable = response.iter_content(chunk_size = 1024), total = total_size//1024, unit = 'KB'):
            f.write(data)
            
            
# load filelist
filelist = []
with open('filelist.json') as f:
    filelist = json.load(f)

# clean filelist
# keep original for version
pkglist = []
for file in filelist:
	reg = re.sub('-\d.*', '', file)
	pkglist.append([reg, file])

count = 0
print(str(len(pkglist)) +  ' packages found\n')

# search mirror
for url in mirror:
	response = requests.get(url)

	# Parse the HTML content using BeautifulSoup
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find all  tags with href attribute
	for link in soup.find_all('a', href=True):
	    href = link['href']
	    if href.endswith('.sig'):
	    	continue
	    
	    #trim . and /
	    href = href.strip('.')
	    href = href.strip('/')
	    
	    # do we want the file
	    # same name, diffetent version, or db
	    reg = re.sub('-\d.*', '', href)
	    
	    for pkg in pkglist:
	    	if href.endswith('.db') or ( pkg[0] == reg and pkg[1] != href ) :
	    		
	    		dl = url + href
	    		sig = dl + '.sig'
	    		local = path + href
	    		localsig = path + href + '.sig'
	    		
	    		# skip existing
	    		if os.path.isfile(localsig):
	    			continue
	    			
	    		print(pkg[0])
	    		
	    		# download
	    		local = path + href
	    		fetch(dl, local)
	    		fetch(sig, localsig)
	    		print()
	    		
	    		count+=1
	    		break

print()
print('complete')
print(str(count) + ' updates')
print(str(len(pkglist)) + ' packages')