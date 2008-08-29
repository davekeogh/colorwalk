import gtk, gtk.glade

from callbacks import Callbacks
from statusbar import StatusBar

SCROLL_LTR = 0
SCROLL_RTL = 1


class Window(gtk.Window):
	
	width = 800
	height = 800
	
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
		self.connect('configure-event', self.callbacks.window_resized)
		
		dic = {
			'on_back_clicked'	: self.callbacks.go_back,
			'on_forward_clicked': self.callbacks.go_forward
		}
		self.ui.signal_autoconnect(dic)
		
		self.ui.get_widget('combobox1').set_active(self.app.scale)
		
		self.ui.get_widget('toolbutton2').set_flags(gtk.CAN_FOCUS)
		
		self.set_icon_name('image')
		self.set_title('Color Walk')
		self.resize(self.width, self.height)
		self.show()
	
	
	def refresh(self):
		self.statusbar.set_text('Current image: <i>%s</i>' % 
								self.app.files[self.app.current])
			
		self.set_pages(len(self.app.images))
		self.set_page(self.app.current + 1)
			
		self.statusbar.set_size(self.app.size)
		self.statusbar.set_res(self.app.current_pb.get_width(),
							   self.app.current_pb.get_height())
			
		self.ui.get_widget('combobox1').set_sensitive(True)
		
		if self.app.current < (len(self.app.images) -1):
			self.ui.get_widget('toolbutton2').set_sensitive(True)
		else:
			self.ui.get_widget('toolbutton2').set_sensitive(False)
		if self.app.current > 0:
			self.ui.get_widget('toolbutton1').set_sensitive(True)
		else:
			self.ui.get_widget('toolbutton1').set_sensitive(False)
		
		self.reset_scrollbars()
		
		# Focus the forward button so that spacebar presses don't
		# activate other tool buttons.
		self.ui.get_widget('toolbutton2').grab_focus()
		
	
	def reset_scrollbars(self, mode=SCROLL_LTR):
		viewport = self.ui.get_widget('scrolledwindow1')
		hadj = viewport.get_hadjustment()
		vadj = viewport.get_vadjustment()
		vadj.set_value(vadj.lower)
		
		
		if mode == SCROLL_RTL:
			hadj.set_value(hadj.upper)
		else: # RTL
			hadj.set_value(hadj.lower)
		
		viewport.set_hadjustment(hadj)
		viewport.set_vadjustment(vadj)
	
	
	def blank(self):
		self.set_title('Color Walk')
		self.statusbar.set_text('No images found in <i>%s</i>'
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
		# FIXME: Get the actual width of the scrollbar + any padding.
		return self.width - 19
	
	
	def get_view_height(self):
		# FIXME: Get the actual height of the menubar + statusbar
		#		 + any padding.
		return self.height - 40
