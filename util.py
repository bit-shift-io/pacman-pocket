import re

# return dict, name, version, arch, ext
def get_package_info(file):
	# trim and tidy
	clean = file.strip('.').strip('/').replace('%3A', ':').replace('%253A', ':')
    
	# split name + version and arch + ext
	result = re.search('(.*)-(.*-.*)-(x86_64|any).(.*)', clean)
	if result == None:
		return None
		
	r = {
		'file' : file,
		'name' : result.group(1),
		'version' : result.group(2),
		'arch' : result.group(3),
		'extension' : result.group(4)
	}
	return r