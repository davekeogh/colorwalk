import gtk

class Image(object):
	
	path = None
	name = None
	pixbuf = None
	
	def __init__(self, path):
		self.path = path

