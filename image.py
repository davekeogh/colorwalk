import os, os.path, subprocess
import gtk

from archive import MAGIC

IMAGES = ['JPEG image data', 'PNG image data', 'GIF image data']
EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']


def new_pixbuf(path, width=-1, height=-1):
	return gtk.gdk.pixbuf_new_from_file_at_size(path, width, height)


def is_image_ext(path):
	if os.path.splitext(path)[1] in EXTENSIONS:
		return True
	else:
		return False


def is_image_file(path):
	if not MAGIC:
		p = subprocess.Popen('file %s' % path, shell=True, 
							 stdout=subprocess.PIPE)
		p.wait()
		stdout = p.stdout.read()
		part = stdout.split(': ')[1]
		print part
		
		found = False
		for type in IMAGES:
			if part.startswith(type):
				found = True
				break
		
		if found:
			return True
		else:
			return False

