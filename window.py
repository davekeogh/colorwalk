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
		
		self.image = self.ui.get_widget('image3')
		self.menubar = self.ui.get_widget('toolbar1')
		
		self.statusbar = StatusBar(self, self.ui)
		
		self.callbacks = Callbacks(self)
		self.connect('delete-event', self.callbacks.quit)
		
		self.set_icon_name('image')
		self.set_title('Color Walk')
		self.resize(600, 600)
		self.show()
	
	
	def get_view_width(self):
		return self.window.get_size()[0] - 19
	
	
	def get_view_height(self):
		return self.window.get_size()[1] - 40
