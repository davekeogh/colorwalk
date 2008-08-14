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
		self.toolbar = self.ui.get_widget('toolbar1')
		self.statusbar = StatusBar(self, self.ui)
		
		self.callbacks = Callbacks(self)
		
		self.connect('delete-event', self.callbacks.quit)
		
		dic = {
			'on_back_clicked'	: self.callbacks.go_back,
			'on_forward_clicked': self.callbacks.go_forward
		}
		self.ui.signal_autoconnect(dic)
		
		self.ui.get_widget('combobox1').set_active(self.app.scale)
		
		self.set_icon_name('image')
		self.set_title('Color Walk')
		self.resize(600, 600)
		self.show()
	
	
	def refresh(self):
		self.statusbar.set_text(self.app.files[self.app.current])
			
		self.set_pages(len(self.app.images))
		self.set_page(self.app.current + 1)
			
		self.statusbar.set_size(self.app.size)
		self.statusbar.set_res(self.app.current_pb.get_width(),
							   self.app.current_pb.get_height())
			
		self.ui.get_widget('combobox1').set_sensitive(True)
		self.ui.get_widget('toolbutton1').set_sensitive(True)
		self.ui.get_widget('toolbutton2').set_sensitive(True)
	
	
	def blank(self):
		self.set_title('Color Walk')
		self.statusbar.set_text('No images found in <b>%s</b>'
								% self.app.archive.name)
								
		self.statusbar.hide_all()
		
		self.ui.get_widget('combobox1').set_sensitive(False)
		self.ui.get_widget('toolbutton1').set_sensitive(False)
		self.ui.get_widget('toolbutton2').set_sensitive(False)
		
		self.ui.get_widget('label6').hide()
		self.ui.get_widget('entry1').hide()
	
	
	def set_pages(self, pages):
		self.ui.get_widget('label6').show()
		self.ui.get_widget('label6').set_text(' of %d' % pages)
	
	
	def set_page(self, page):
		self.ui.get_widget('entry1').show()
		self.ui.get_widget('entry1').set_text('%d' % page)
	
	
	def get_view_width(self):
		return self.window.get_size()[0] - 19
	
	
	def get_view_height(self):
		return self.window.get_size()[1] - 40
