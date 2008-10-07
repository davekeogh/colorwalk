
class BookmarkError(Exception):
	
	def __init__(self, message):
		self.message = message


class ArchiveError(Exception):
	
	def __init__(self, message):
		self.message = message
