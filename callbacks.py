import os, os.path

import gtk

from image import new_pixbuf, is_image_ext

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
		
		for file in self.app.files:
			if is_image_ext(file):
				self.app.images.append(file)
		
		self.app.current = 0
		
		if len(self.app.images):
			self.app.size = \
			os.stat(self.app.archive.path).st_size / 1048576
			
			self.app.current_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.files[self.app.current]),
					   width=self.app.win.get_view_width())
					   
			self.win.image.set_from_pixbuf(self.app.current_pb)
			
			self.win.refresh()
			
			self.app.next_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.files[self.app.current + 1]),
					   width=self.app.win.get_view_width())
		
		else:
			self.win.blank()
			
			self.app.archive.remove_temp_dir()
			self.app.archive = None
		
	
	def preloading_finished(self, worker):
		self.win.refresh()
	
	
	def go_back(self, widget):
		self.app.next_pb = self.app.current_pb
		self.app.current_pb = self.app.previous_pb_pb
		self.app.previous_pb = None
		
		self.app.current -= 1
		
		self.win.image.set_from_pixbuf(self.app.current_pb)
		
		self.app.worker.set_preload(
			os.path.join(self.app.archive.temp_dir, 
			self.app.files[self.app.current - 1]),
			self.app.previous_pb, width=self.win.get_view_width(),
			height=-1)
		
		self.app.worker.start()
	
	
	def go_forward(self, widget):
		self.app.previous_pb = self.app.current_pb
		self.app.current_pb = self.app.next_pb
		self.app.next_pb = None
		
		self.app.current += 1
		
		self.win.image.set_from_pixbuf(self.app.current_pb)
		
		self.app.worker.set_preload(
			os.path.join(self.app.archive.temp_dir, 
			self.app.files[self.app.current + 1]), self.app.next_pb,
			width=self.win.get_view_width(), height=-1)
		
		self.app.worker.start()
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
