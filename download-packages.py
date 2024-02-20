import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import os
import util
import sys

# mirrors
mirror = ['http://ftp.iinet.net.au/pub/archlinux/core/os/x86_64/', 'http://ftp.iinet.net.au/pub/archlinux/multilib/os/x86_64/', 'http://ftp.iinet.net.au/pub/archlinux/extra/os/x86_64/']

path = util.get_download_path()

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
        pbar = tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024)
        
        for data in response.iter_content(1024):
        	pbar.update(len(data))
        	f.write(data)
        	
            
# load txt files
pkgs = {}
files = util.get_files_in_dir(os.getcwd(), '.txt')
for txtfile in files:
	with open(txtfile, 'r') as f:
	    for line in f.read().splitlines():
	    	item = line.split(' ')
	    	# todo, lowest or highest vetsion?
	    	pkgs[item[0]] = { 'name' : item[0], 'version' : item[1]}

print(str(len(pkgs)) +  ' local packages\n')


# search mirror
mirrorpkgs = {}
mirrordb = []
print('scrape mirrors...')

for url in mirror:
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find all  tags with href attribute
	for link in soup.find_all('a', href=True):
	    href = link['href']
	    if href.endswith('.sig'):
	    	continue
		
	    # get db
	    if href.endswith('.db'):
	    	mirrordb.append(url + href)
	    	continue
		
	    p = util.get_package_info(href)
	    if p is None:
	    	continue
	    	
	    p['url'] = url + href
	    pkg = p['name']
	    mirrorpkgs[pkg] = p
	    

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