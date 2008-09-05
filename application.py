
class Application(object):
	
	# TODO: This class is only going to become larger, better to move it
	#		to its own module.
	
	# TODO: Many of these properties would probably make more sense to
	#		reside in the Archive object
	
	win = None
	worker = None
	archive = None
	prefs = None
	log = ['\n']
	files = []
	images = []
	current = 0
	size = 0
	
	scale = 0
	
	current_pb = None
	next_pb = None
	previous_pb = None
	
	def reset(self):
		self.files = []
		self.images = []
		self.current = 0
		self.size = 0
	
		self.current_pb = None
		self.next_pb = None
		self.previous_pb = None
