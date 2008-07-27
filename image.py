import subprocess
import gtk

from archive import MAGIC

IMAGES = ['JPEG image data', 'PNG image data', 'GIF image data']


def is_image_file(path):
	if not MAGIC:
		p = subprocess.Popen('file %s' % path, shell=True, 
							 stdout=subprocess.PIPE)
		p.wait()
		stdout = p.stdout.read()
		part = stdout.split(': ')[1]
		
		found = False
		for type in IMAGES:
			if part.startswith(type):
				found = True
				break
		
		if found:
			return True
		else:
			return False


class Image(object):
	
	path = None
	name = None
	pixbuf = None
	width = 0
	height = 0
	
	def __init__(self, path):
		self.path = path

