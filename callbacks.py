import gtk

class Callbacks(object):
	
	def __init__(self, win):
		self.win = win
		self.app = win.app
	
	
	def extracting_finished(self, worker):
		self.win.statusbar.progressbar.hide()
		self.win.statusbar.clear_text()
	
	
	def quit(self, widget, event=None):
		if self.app.archive:
			self.app.archive.remove_temp_dir()
		gtk.main_quit()
