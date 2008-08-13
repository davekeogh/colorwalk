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
			
			self.win.statusbar.set_text(
				self.app.files[self.app.current])
			
			self.win.set_pages(len(self.app.images))
			self.win.set_page(self.app.current + 1)
			
			self.win.statusbar.set_size(self.app.size)
			self.win.statusbar.set_res(self.app.current_pb.get_width(),
				self.app.current_pb.get_height())
			
			self.win.ui.get_widget('combobox1').set_sensitive(True)
			
			self.app.next_pb = \
			new_pixbuf(os.path.join(self.app.archive.temp_dir, 
					   self.app.files[self.app.current + 1]),
					   width=self.app.win.get_view_width())
		
		else:
			self.win.set_title('Color Walk')
			self.win.statusbar.set_text('No images found in <b>%s</b>'
										% self.app.archive.name)
			self.app.archive.remove_temp_dir()
			self.app.archive = None
		
		
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
