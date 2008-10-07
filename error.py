
class BookmarkError(Exception):
	
	def __init__(self, file, old_page, new_page):
		self.file = file
		self.old_page = old_page
		self.new_page = new_page


class ArchiveError(Exception):
	
	def __init__(self, message):
		self.message = message
