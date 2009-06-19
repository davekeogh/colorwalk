#!/usr/bin/env python

#    This file is part of Color Walk.
#
#    Color Walk is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    Color Walk is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Color Walk.  If not, see <http://www.gnu.org/licenses/>.

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
    
    options = parser.parse_args()[0]
    
    if options.prefix:
        PREFIX = options.prefix

    print 'Installing %s %s :\n' % (APPLICATION, VERSION)

    for dir in DIRECTORIES:
        print 'Creating directory %s/%s ...' % (PREFIX, dir) ,
        if subprocess.call(['mkdir', '-p', os.path.join(PREFIX, dir)]):
            print 'Failed'
            print '\n%s failed to install.' % APPLICATION
            sys.exit(1)
        else:
            print 'Done'
    
    for file in FILES:
        print 'Copying %s to %s/%s ...' % (file, PREFIX, FILES[file]) ,
        if subprocess.call(['install', '%s' % file, os.path.join(PREFIX, os.path.join(FILES[file], file))]):
            print 'Failed'
            print '\n%s failed to install.' % APPLICATION
            sys.exit(1)
        else:
            print 'Done'

    print '\n%s %s is now installed.' % (APPLICATION, VERSION)
