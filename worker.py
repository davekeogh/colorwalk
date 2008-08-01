import threading, subprocess, time
import gtk, gobject

class Worker(threading.Thread, gobject.GObject):
	
	__gsignals__ = {
	
		'finished' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
					  ()),
	
		'cancel' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
					())
	}
	
	function = None
	process = None

	
	def __init__(self, app):
		self.app = app
		app.worker = self
		
		threading.Thread.__init__(self)
		gobject.GObject.__init__(self)
	
	
	def set_function(self, f, sub=True):
		self.function = f
		self.sub = sub
	
	
	def clear(self):
		self.function = None
		self.process = None
		self.sub = True
	
	
	def run(self):
		if self.sub:
			self.process = self.function()
			
			self.app.win.statusbar.progressbar.show()
			self.app.win.statusbar.set_markup('Opening <b>%s</b>...' %
											  self.app.archive.name)
			
			while self.process.poll() == None:
				gtk.gdk.threads_enter()
				self.app.win.statusbar.progressbar.pulse()
				gtk.gdk.threads_leave()
				
				time.sleep(0.1)
		
		else:
			self.function()
			
		self.emit('finished')
