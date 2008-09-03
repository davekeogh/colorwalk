
class StatusBar(object):
	
	def __init__(self, win, ui):
		self.win = win
		self.ui = ui
		
		self.message_area = ui.get_widget('label4')
		self.resize_grip = ui.get_widget('statusbar2')
		
		self.progressbar = self.ui.get_widget('progressbar')
	
	
	def set_text(self, msg):
		self.message_area.set_markup(msg)
	
	
	def clear_text(self):
		self.message_area.set_text('')
	
	
	def set_size(self, mb):
		self.ui.get_widget('label3').set_text('%i MB' % mb)
		self.ui.get_widget('frame3').show()
	
	
	def set_res(self, width, height):
		self.ui.get_widget('label2').set_text('%i x %i'
											  % (width, height))
		self.ui.get_widget('frame2').show()
	
	
	def hide_all(self):
		self.ui.get_widget('frame2').show()
		self.ui.get_widget('frame3').show()
		self.progressbar.hide()
