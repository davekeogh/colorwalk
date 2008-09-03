import gtk

def choose_file():
	dialog = FileChooserDialog()
	response = dialog.run()
	file = dialog.get_filename()
	dialog.destroy()
	
	if response == gtk.RESPONSE_ACCEPT:
		return file
	else:
		return None


class FileChooserDialog(gtk.FileChooserDialog):
	
	def __init__(self):
		
		gtk.FileChooserDialog.__init__(self, title='Open File',
									   buttons=(gtk.STOCK_CANCEL, 
									   			gtk.RESPONSE_REJECT,
									   			gtk.STOCK_OK,
									   			gtk.RESPONSE_ACCEPT))
		
		self.set_icon_name('fileopen')
		
		comic_filter = gtk.FileFilter()
		comic_filter.set_name('Comic Book Archives')
		comic_filter.add_pattern('*.cbz')
		comic_filter.add_pattern('*.cbr')
		
		arc_filter = gtk.FileFilter()
		arc_filter.set_name('Archives')
		arc_filter.add_pattern('*.zip')
		arc_filter.add_pattern('*.rar')
		
		all_filter = gtk.FileFilter()
		all_filter.set_name('All Files')
		all_filter.add_pattern('*')
		
		self.add_filter(comic_filter)
		self.add_filter(arc_filter)
		self.add_filter(all_filter)
		
