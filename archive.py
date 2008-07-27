import os, os.path, tempfile, shutil, subprocess

from error import ArchiveError

MAGIC_WARNING = """\nInstall the python module 'magic' for improved \
performance when opening archive files. It's probably called \
python-magic by your package manager.\n"""

ZIP = 0
RAR = 1
 
try:
	import magic
	MAGIC = True
except ImportError:
	MAGIC = False
	print MAGIC_WARNING



def is_zip_file(path):
	if not MAGIC:
		p = subprocess.Popen('file %s' % path, shell=True, 
							 stdout=subprocess.PIPE)
		p.wait()
		stdout = p.stdout.read()
		
		if stdout.split(': ')[1].startswith('Zip archive data'):
			return True
		else:
			return False


def is_rar_file(path):
	if not MAGIC:
		p = subprocess.Popen('file %s' % path, shell=True, 
							 stdout=subprocess.PIPE)
		p.wait()
		stdout = p.stdout.read()
		
		if stdout.split(': ')[1].startswith('RAR archive data'):
			return True
		else:
			return False


class Archive(object):
	
	path = None
	name = None
	type = None
	temp_dir = None
	
	def __init__(self, path):
		self.path = path
		
		if not os.path.isfile(path):
			raise ArchiveError('%s does not exist.' % path)
		
		if is_zip_file(path):
			self.type = ZIP
		elif is_rar_file(path):
			self.type = RAR
		else:
			raise ArchiveError('%s is not a valid file type.' % path)
		
		self.name = os.path.split(path)[1]
		
		
	def make_temp_dir(self):
		self.temp_dir = tempfile.mkdtemp(prefix='colorwalk-%s-' % 
										 os.environ['USER'])
	
	
	def remove_temp_dir(self):
		shutil.rmtree(self.temp_dir)
	
	
	def extract(self):
		self.make_temp_dir()
		
		if self.type == ZIP:
			command = 'unzip -j %s -d %s' % (self.path, self.temp_dir)
		if self.type == RAR:
			command = 'unrar e %s %s' % (self.path, self.temp_dir)
		
		return subprocess.Popen(command, shell=True, 
								stdout=subprocess.PIPE,
								stderr=subprocess.STDOUT)
