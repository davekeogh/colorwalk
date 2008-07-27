import gtk

class Callbacks(object):
	
	def __init__(self, win):
		self.win = win
		self.app = win.app
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
