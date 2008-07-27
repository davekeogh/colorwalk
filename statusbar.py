
class StatusBar(object):
	
	def __init__(self, win, ui):
		self.win = win
		self.ui = ui
		
		self.message_area = ui.get_widget('label4')
		self.resize_grip = ui.get_widget('statusbar2')
		
		self.progressbar = self.ui.get_widget('progressbar')
		
	
	def set_markup(self, msg):
		self.message_area.set_markup(msg)
	
	
	def set_text(self, msg):
		self.message_area.set_text(msg)
	
	
	def clear_text(self):
		self.message_area.set_text('')
