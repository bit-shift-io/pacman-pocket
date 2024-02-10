
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os

# mirrors
mirror = ['http://ftp.iinet.net.au/pub/archlinux/core/os/x86_64/', 'http://ftp.iinet.net.au/pub/archlinux/multilib/os/x86_64/', 'http://ftp.iinet.net.au/pub/archlinux/extra/os/x86_64/']

# download location
path = os.getcwd() + '/packages/'
if not os.path.exists(path):
	os.makedirs(path)

# if sig exists
def exists(url):
	filename = path + re.sub('.*/', '', url) + '.sig'
	return os.path.isfile(filename)
	
# downloads
def fetch(url):
    filename = path + re.sub('.*/', '', url)
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
            
            
# load pkg list
pkgs = {}
with open('packages.txt', 'r') as f:
    for line in f.read().splitlines():
    	item = line.split(' ')
    	pkgs[item[0]] = { 'name' : item[0], 'version' : item[1]}

print(str(len(pkgs)) +  ' local packages\n')

# search mirror
mirrorpkgs = {}
mirrordb = []
print('scrape mirrors...')
for url in mirror:
	response = requests.get(url)
	# parse html
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find all  tags with href attribute
	for link in soup.find_all('a', href=True):
	    href = link['href']
	    if href.endswith('.sig'):
	    	continue
	    
	    href = href.strip('.').strip('/')
	    href = href.replace('%3A', ':').replace('%253A', ':')
	    # get arch and ext
	    archext = re.sub('.*-', '', href)
	    # get package name
	    pkg = re.sub('-\d.*', '', href)
	    # get version
	    version = href.replace(archext, '').replace(pkg,'')
	    version = version[:-1][1:]
	    mirrorpkgs[pkg] = {'name' : pkg, 'version' : version, 'url' : url +href}
	    
	    # get db and sig
	    if href.endswith('.db'):
	    	mirrordb.append(url + href)

print(str(len(mirrorpkgs)) + ' mirror packages\n')

print('download databases...')
dbcount = 0	    			
for db in mirrordb:
	name = re.sub('.*/', '', db).replace('.db', '')
	if exists(db):
		continue
	print(name)
	fetch(db)
	fetch(db + '.sig')
	dbcount += 1
	
	
print('\ndownload packages...')
count = 0
for pk in pkgs:
	# maybe extra packages not on mirror
	if pk not in mirrorpkgs:
		continue
	
	local = pkgs[pk]
	remote = mirrorpkgs[pk]
	
	if exists(remote['url']):
		continue
	
	if local['version'] != remote['version']:
		print(pk)
		fetch(remote['url'])
		fetch(remote['url'] + '.sig')
		count += 1

print()
print(str(dbcount) + ' database updates')
print(str(count) + ' package updates')
print(str(len(pkgs)) + ' packages')
print('complete')