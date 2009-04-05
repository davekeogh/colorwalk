#!/usr/bin/env python

import sys, os, subprocess, optparse

VERSION = '0.1.0'
PREFIX = '/usr'

def install(file, location):
    print 'Copying %s to %s/%s ...' % (file, PREFIX, location) ,
    if subprocess.call(['install', '%s' % file, os.path.join(PREFIX, os.path.join(location, file))]):
        print 'Failed'
        print '\nColor Walk failed to install.'
        sys.exit(1)
    else:
        print 'Done'

parser = optparse.OptionParser()
parser.add_option('--prefix', dest='prefix', help='define an alternate location to install to')
(options, args) = parser.parse_args()

if options.prefix:
    PREFIX = options.prefix

print 'Installing Color Walk %s :\n' % VERSION

subprocess.call(['mkdir', '-p', os.path.join(PREFIX, 'share/colorwalk')])

install('colorwalk.ui', 'share/colorwalk')
install('colorwalk.desktop', 'share/applications')
install('colorwalk', 'bin')

print '\nColor Walk %s is now installed.' % VERSION
