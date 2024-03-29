import re
from ftplib import FTP
import util
import sys

host = 'office.lan'
user = 'user'
password = 'password'
remote = '/manjaro/'

path = util.get_download_path()
files = util.get_files_in_dir(path)

# updated packages
pkgs = {}
for f in files:
	if f.endswith('.sig'):
	    	continue
	pk = util.get_package_info(f)
	if pk is None:
		continue
	pkgs[pk['name']] = pk
	
print(str(len(pkgs)) +  ' packages\n')

# connect ftp
ftp = None
ftpfiles=[]
try:
	ftp = FTP(host, user, password)
	ftp.set_pasv(False)
	ftp.cwd(remote)
	ftpfiles = ftp.nlst()
except Exception as e:
	print(e)
	sys.exit()

# del old
print('\ndeleting old packages...')
delcount = 0
for f in ftpfiles:
	pk = util.get_package_info(f)
	if pk is None:
		continue
		
	pkg = pk['name']
	ver = pk['version']
	
	# are we related to new files?
	if pkg not in pkgs:
		continue

	# delete older versions
	if ver != pkgs[pkg]['version']:
		try:
			ftp.delete(f)
			ftp.delete(f + '.sig')
			print(pkg + ' ' + ver)
			delcount += 1
		except Exception as e:
			print(f + ' -> doesnt exist or is root')

# push new files
print('\nadding new packages...')
pushcount = 0
for f in files:
	filepath = path + f
	pk = util.get_package_info(f)
	try:
		with open(filepath, 'rb') as openfile:
			ftp.storbinary(f'STOR {f}', openfile)
		if pk is None:
			print(f)
		else:
			print(pk['name'] + ' ' + pk['version'])
		pushcount += 1
	except Exception as e:
		print(e)

ftp.quit()

print()
print(str(delcount) + ' deletions')
print(str(pushcount) + ' additions')