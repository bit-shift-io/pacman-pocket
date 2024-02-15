import re
import os


# packages
def get_download_path():
	path = os.getcwd() + '/packages/'
	if not os.path.exists(path):
		os.makedirs(path)
	return path


# get files in dir
def get_files_in_dir(path, ext = None):
	#files = sorted(next(os.walk(path), (None, None, []))[2])
	print(path)
	files = []
	for name in os.listdir(path):
		if not os.path.isdir(os.path.join(path, name)):
			if ext is None:
				files.append(name)
			elif name.endswith(ext):
				files.append(name)
            
	return sorted(files)
	

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