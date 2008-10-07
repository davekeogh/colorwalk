import os, os.path

from preferences import PREFS_DIR
from error import BookmarkError


class Bookmarks(dict):
	
	file = os.path.join(PREFS_DIR, 'bookmarks')
	
	def __init__(self):
		if os.path.isfile(self.file):
			fb = open(PREFS_PATH)
			lines = ()
			lines = fb.read().chop('\n').split('\n')
			fb.close()
			
			for line in lines:
				(key, value) = line.split('\t')
				self[key] = value
	
	
	def add(self, file, page):
		if self.has_key(file):
			raise BookmarkError(os.path.split(file)[1], self[file]
								page)
		else:
			self[file] = page
	
	
	def remove(self, file):
		self.__delitem__(self)
	
	
	def save(self):
		fb = open(PREFS_PATH, 'w')
		
		for key in self:
			fb.writeline('%s\t%s' % (key, self[key]))
		
		fb.close()
	
	
	def __del__(self):
		self.save()
