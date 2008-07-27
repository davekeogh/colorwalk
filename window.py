import gtk, gtk.glade

from callbacks import Callbacks
from statusbar import StatusBar


class Window(gtk.Window):
	
	def __init__(self, app, ui):
		self.app = app
		app.win = self
		
		gtk.Window.__init__(self)
		
		self.ui = gtk.glade.XML(ui, 'vbox1')
		self.add(self.ui.get_widget('vbox1'))
		
		self.statusbar = StatusBar(self, self.ui)
		
		self.callbacks = Callbacks(self)
		self.connect('delete-event', self.callbacks.quit)
		
		self.set_icon_name('image')
		self.set_title('Color Walk')
		self.resize(400, 400)
		self.show()
