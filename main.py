#!/usr/bin/env python

import sys
import gtk

from window import Window
from worker import Worker
from archive import Archive
from error import ArchiveError

GLADE = 'colorwalk.glade'


class Application(object):
	
	# TODO: This class is only going to become larger, better to move it
	#		to its own module.
	
	# TODO: Many of these properties would probably make more sense to
	#		reside in the Archive object
	
	win = None
	worker = None
	archive = None
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


def main(args):
	gtk.gdk.threads_init()
	
	app = Application()
	
	app.win = Window(app, GLADE)
	app.worker = Worker(app)
	
	try:
		app.archive = Archive(args[1])
	except IndexError:
		app.archive = None
	except ArchiveError, error:
		# TODO: Throw an error dialog or display the error text in the
		#		statusbar.
		print error.message
		app.archive = None
	
	if app.archive:
		app.worker.connect('extracting-finished',
						   app.win.callbacks.extracting_finished)
		app.worker.set_function(app.archive.extract)
		app.worker.start()
	
	gtk.main()
	

if __name__ == '__main__':
	main(sys.argv)
