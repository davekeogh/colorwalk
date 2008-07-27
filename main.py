#!/usr/bin/env python

import sys
import gtk

from window import Window
from worker import Worker
from archive import Archive
from error import ArchiveError

GLADE = 'colorwalk.glade'


class Application(object):
	
	win = None
	worker = None
	archive = None
	log = ['\n']


def main(args):
	gtk.gdk.threads_init()
	
	app = Application()
	
	try:
		app.archive = Archive(args[1])
	except IndexError:
		app.archive = None
	except ArchiveError, error:
		print error.message
		app.archive = None
	
	app.win = Window(app, GLADE)
	app.worker = Worker(app)
	
	if app.archive:
		app.worker.set_function(app.archive.extract)
		app.worker.start()
	
	gtk.main()
	

if __name__ == '__main__':
	main(sys.argv)
