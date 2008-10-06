import os, os.path

import gtk, gobject

from image import new_pixbuf, is_image_ext
from worker import Worker
from dialogs import AboutDialog, choose_file
from error import ArchiveError
from archive import Archive
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
		self.app.files.sort(key=str.lower)
		
		for file in self.app.files:
			if is_image_ext(file):
				self.app.images.append(file)
		
		self.app.current = 0
		
		if len(self.app.images):
			self.app.size = \
			os.stat(self.app.archive.path).st_size / 1048576
			
			self.app.current_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.images[self.app.current]),
					   width=self.app.win.get_view_width())
					   
			self.win.refresh()
			self.win.image.set_from_pixbuf(self.app.current_pb)
			
			self.app.next_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.images[self.app.current + 1]),
					   width=self.app.win.get_view_width())
		
		else:
			self.win.blank()
			self.win.statusbar.set_text('No images found in <i>%s</i>'
										% self.app.archive.name)
			self.app.reset()
			self.app.archive.remove_temp_dir()
			self.app.archive = None
	
	
	def open(self, widget):
		file = choose_file(self.app.open_dir)
		
		if file:
			self.app.open_dir = os.path.split(file)[0]
			
			if self.app.archive:
				self.app.reset()
				self.win.blank()
				self.app.archive.remove_temp_dir()
				self.app.archive = None
			
			try:
				self.app.archive = Archive(file)
			except ArchiveError, error:
				# TODO: Throw an error dialog or display the error text 
				#		in the statusbar.
				print error.message
				self.app.archive = None
			
			if self.app.archive:
				self.app.win.statusbar.hide_all()
				self.app.worker = Worker(self.app)
				self.app.worker.connect('extracting-finished',
						   	 self.app.win.callbacks.extracting_finished)
				self.app.worker.set_function(self.app.archive.extract)
				self.app.worker.start()
	
	
	def close(self, widget):
		if self.app.archive:
			self.app.reset()
			self.win.blank()
			self.app.archive.remove_temp_dir()
			self.app.archive = None
	
	
	def about(self, widget):
		dialog = AboutDialog()
		if dialog.run():
			dialog.destroy()
	
	
	def go_back(self, widget):
		if self.app.current > 0:
			self.app.next_pb = self.app.current_pb
			self.app.current_pb = self.app.previous_pb
			
			self.app.current -= 1
			
			self.win.refresh()
			self.win.image.set_from_pixbuf(self.app.current_pb)
			
			gobject.idle_add(self.preload_previous)
	
	
	def go_forward(self, widget):
		# TODO: Implement smart paging here. Check the preferences
		#		value first to see if it's enabled.
		
		if self.app.current < len(self.app.images) - 1:
			self.app.previous_pb = self.app.current_pb
			self.app.current_pb = self.app.next_pb
			
			self.app.current += 1
			
			self.win.refresh()
			self.win.image.set_from_pixbuf(self.app.current_pb)
			
			gobject.idle_add(self.preload_next)
	
	
	def jump(self, widget):
		text = widget.get_text()
		
		def fail():
			self.app.win.set_page(self.app.current + 1)
			self.win.steal_focus()
		
		try:
			num = int(text)
			
			if num <= len(self.app.images) and num > 0:
				self.app.current = num - 1
				
				self.app.current_pb = \
				new_pixbuf(os.path.join(self.app.archive.temp_dir, 
				self.app.files[self.app.current]),
				width=self.app.win.get_view_width())
				
				self.win.refresh()
				self.win.steal_focus()
				self.win.image.set_from_pixbuf(self.app.current_pb)
				
				try:
					self.app.next_pb = \
					new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					self.app.images[self.app.current + 1]),
					width=self.app.win.get_view_width())
				except IndexError:
					self.app.next_pb = None
				
				try:
					self.app.previous_pb = \
					new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					self.app.images[self.app.current - 1]),
					width=self.app.win.get_view_width())
				except IndexError:
					self.app.previous_pb = None
				
			else:
				fail()
		except ValueError:
			fail()
	
	
	def preload_next(self):
		if (self.app.current + 1) <= (len(self.app.images) -1):
			self.app.next_pb = \
				new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   	   self.app.images[self.app.current + 1]),
					   	   width=self.app.win.get_view_width())
		
		return False
	
	
	def preload_previous(self):
		if (self.app.current - 1) >= 0:
			self.app.previous_pb = \
				new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   	   self.app.images[self.app.current - 1]),
					   	   width=self.app.win.get_view_width())
		
		return False
	
	
	def window_resized(self, widget, allocation):
		if self.app.archive:
			if (self.win.width != allocation.width or
				self.win.height != allocation.height):
				
				self.app.current_pb = \
				new_pixbuf(os.path.join(self.app.archive.temp_dir, 
						   self.app.images[self.app.current]),
						   width=self.app.win.get_view_width())
				self.win.image.set_from_pixbuf(self.app.current_pb)
				
				gobject.idle_add(self.preload_next)
				gobject.idle_add(self.preload_previous)
		
		self.win.width = allocation.width
		self.win.height = allocation.height
				
	
	def key_pressed(self, widget, event):
		if self.app.archive:
			if event.keyval == 32: # Spacebar
				self.go_forward(widget)
			
			if event.keyval == 65288: # Backspace
				self.go_back(widget)
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
