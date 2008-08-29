import os, os.path

import gtk, gobject

from image import new_pixbuf, is_image_ext
from worker import Worker

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
					   
			self.win.refresh()
			self.win.image.set_from_pixbuf(self.app.current_pb)
			
			self.app.next_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.files[self.app.current + 1]),
					   width=self.app.win.get_view_width())
			
			self.win.connect('key-press-event', self.key_pressed)
		
		else:
			self.win.blank()
			
			self.app.archive.remove_temp_dir()
			self.app.archive = None
	
	
	def go_back(self, widget):
		self.app.next_pb = self.app.current_pb
		self.app.current_pb = self.app.previous_pb
		
		self.app.current -= 1
		
		self.win.refresh()
		self.win.image.set_from_pixbuf(self.app.current_pb)
		
		gobject.idle_add(self.preload_previous)
	
	
	def go_forward(self, widget):
		# TODO: Implement smart paging here. Check the preferences
		#		value first to see if it's enabled.
		self.app.previous_pb = self.app.current_pb
		self.app.current_pb = self.app.next_pb
		
		self.app.current += 1
		
		self.win.refresh()
		self.win.image.set_from_pixbuf(self.app.current_pb)
		
		gobject.idle_add(self.preload_next)
	
	
	def preload_next(self):
		if (self.app.current + 1) <= (len(self.app.images) -1):
			self.app.next_pb = \
				new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   	   self.app.files[self.app.current + 1]),
					   	   width=self.app.win.get_view_width())
		
		return False
	
	
	def preload_previous(self):
		if (self.app.current - 1) >= 0:
			self.app.previous_pb = \
				new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   	   self.app.files[self.app.current - 1]),
					   	   width=self.app.win.get_view_width())
		
		return False
	
	
	def window_resized(self, widget, allocation):
		if (self.win.width != allocation.width or
			self.win.height != allocation.height):
				
			self.win.width = allocation.width
			self.win.height = allocation.height
			
			self.app.current_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.files[self.app.current]),
					   width=self.app.win.get_view_width())
			self.win.image.set_from_pixbuf(self.app.current_pb)
			
			gobject.idle_add(self.preload_next)
			gobject.idle_add(self.preload_previous)
				
	
	def key_pressed(self, widget, event):
		if event.keyval == 32: # Spacebar
			self.go_forward(widget)
		
		if event.keyval == 65288: # Backspace
			self.go_back(widget)
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
