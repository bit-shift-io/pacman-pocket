import re
import sys
import os
import json
from ftplib import FTP

host = 'office.lan'
port = 22
user = 'user'
password = 'password'
remote = '/ftp/user/pkgs/archlinux/'
path = os.getcwd() + '/packages/'

# load filelist
filelist = []
with open('filelist.json') as f:
    filelist = json.load(f)
	
# get updated files
newlist = sorted(next(os.walk(path), (None, None, []))[2])

# get list files to delete
deletecount = 0
deletelist = []
for file in newlist:
	reg = re.sub('-\d.*', '', file)
	
	for old in filelist:
		oldreg = re.sub('-\d.*', '', old)
		
		if reg == oldreg:
			deletelist.append(old)
			deletelist.append(old + '.sig')
			deletecount += 1
			break
			
#print(deletelist)
print(str(deletecount) + ' files to remove\n')

ftp = FTP(host, user, password)
ftp.cwd(remote)

# del old files
delcount = 0
for file in deletelist:
	try:
		ftp.delete(file)
		print(file + ' -> deleted')
		delcount += 1
	except Exception as e:
		print(file + ' -> doesnt exist or is root')


# push new files
pushcount = 0
for file in newlist:
	filepath = path + file
	
	try:
		with open(filepath, 'rb') as openfile:
			ftp.storbinary(f'STOR {file}', openfile)
		print(file + ' -> added')
		pushcount += 1
	except Exception as e:
		print(file + ' -> exists as root')

ftp.quit()

print(str(delcount) + ' files removed')
print(str(pushcount) + ' files added')