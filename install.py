#!/usr/bin/env python

import sys, os, subprocess, optparse

APPLICATION = 'Color Walk'
VERSION = '0.1.0'
PREFIX = '/usr'

DIRECTORIES = ['share/colorwalk']
FILES = {
    'colorwalk.ui'      : 'share/colorwalk',
    'colorwalk.desktop' : 'share/applications',
    'colorwalk'         : 'bin'
}

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--prefix', dest='prefix', help='define an alternate location to install to')

    if parser.parse_args()[0].prefix:
        PREFIX = options.prefix

    print 'Installing %s %s :\n' % (APPLICATION, VERSION)

    for dir in DIRECTORIES:
        print 'Creating directory %s/%s ...' % (PREFIX, dir) ,
        if subprocess.call(['mkdir', '-p', os.path.join(PREFIX, dir)]):
            print 'Failed'
            print '\nColor Walk failed to install.'
            sys.exit(1)
        else:
            print 'Done'
    
    for file in FILES:
        print 'Copying %s to %s/%s ...' % (file, PREFIX, FILES[file]) ,
        if subprocess.call(['install', '%s' % file, os.path.join(PREFIX, os.path.join(FILES[file], file))]):
            print 'Failed'
            print '\nColor Walk failed to install.'
            sys.exit(1)
        else:
            print 'Done'

    print '\n%s %s is now installed.' % (APPLICATION, VERSION)
