import os, os.path

import gtk

from image import Image, new_pixbuf

class Callbacks(object):
	
	def __init__(self, win):
		self.win = win
		self.app = win.app
	
	
	def extracting_finished(self, worker):
		self.win.statusbar.clear_text()
		self.win.statusbar.progressbar.hide()
		
		self.win.set_title(self.app.archive.name)
		
		self.app.files = os.listdir(self.app.archive.temp_dir)
		self.app.files.sort()
		self.app.current = 0
		
		self.app.size = \
		os.stat(self.app.archive.path).st_size / 1048576
		
		self.app.current_pb = \
		new_pixbuf(os.path.join(self.app.archive.temp_dir, 
				   self.app.files[self.app.current]),
				   width=self.app.win.get_view_width())
				   
		self.win.image.set_from_pixbuf(self.app.current_pb)
		
		self.win.statusbar.set_text(self.app.files[self.app.current])
		self.win.statusbar.set_pages(self.app.current + 1,
									 len(self.app.files))
		self.win.statusbar.set_size(self.app.size)
		self.win.statusbar.set_res(self.app.current_pb.get_width(),
								   self.app.current_pb.get_height())
		
		self.app.next_pb = \
		new_pixbuf(os.path.join(self.app.archive.temp_dir, 
				   self.app.files[self.app.current + 1]),
				   width=self.app.win.get_view_width())
		
		
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
