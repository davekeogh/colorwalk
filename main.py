#!/usr/bin/env python

import sys
import gtk

from window import Window
from worker import Worker
from archive import Archive
from error import ArchiveError
from application import Application
from preferences import Preferences

GLADE = 'colorwalk.glade'


def main(args):
	gtk.gdk.threads_init()
	
	app = Application()
	
	app.prefs = Preferences()
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
