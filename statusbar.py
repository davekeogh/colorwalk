
class StatusBar(object):
	
	context = 'message area'
	id = 0
	
	def __init__(self, win, ui):
		self.win = win
		self.ui = ui
		
		self.message_area = ui.get_widget('statusbar1')
		self.resize_grip = ui.get_widget('statusbar2')
		
		self.progressbar = self.ui.get_widget('progressbar')
		
		self.id = self.message_area.get_context_id(self.context)
		
	
	def set_text(self, msg):
		self.message_area.push(self.id, msg)
	
	
	def clear_text(self):
		self.message_area.pop(self.id)
