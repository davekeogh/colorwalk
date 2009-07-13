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

import sys, os, subprocess, optparse, distutils


APPLICATION = 'Color Walk'
VERSION = '0.1.0'
PREFIX = '/usr'
REMOVE = False

DIRECTORIES = ('share/colorwalk', 'lib/python%s.%s/dist-packages/ColorWalk' % (sys.version_info[0], sys.version_info[1]))

FILES = {
    'colorwalk.ui'              : DIRECTORIES[0],
    'colorwalk.desktop'         : 'share/applications',
    'colorwalk'                 : 'bin',
    'ColorWalk/__init__.py'     : os.path.split(DIRECTORIES[1])[0],
    'ColorWalk/dialogs.py'      : os.path.split(DIRECTORIES[1])[0],
    'ColorWalk/preferences.py'  : os.path.split(DIRECTORIES[1])[0],
    'ColorWalk/images.py'       : os.path.split(DIRECTORIES[1])[0],
    'ColorWalk/utilities.py'    : os.path.split(DIRECTORIES[1])[0],
    'ColorWalk/globals.py'    : os.path.split(DIRECTORIES[1])[0],
}


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--prefix', dest='prefix', help='define an alternate location to install to')
    parser.add_option('--remove', '-r', action='store_true', dest='remove', help='remove any installed files')
    
    options = parser.parse_args()[0]
    
    if options.remove:
        REMOVE = options.remove
    
    if options.prefix:
        PREFIX = options.prefix

    if not REMOVE:
        print 'Installing %s %s :\n' % (APPLICATION, VERSION)

        for dir in DIRECTORIES:
            print 'Creating directory %s ...' % os.path.join(PREFIX, dir) ,
            if subprocess.call(['mkdir', '-p', os.path.join(PREFIX, dir)]):
                print 'Failed'
                print '\n%s failed to install.' % APPLICATION
                sys.exit(1)
            else:
                print 'Done'
        
        for file in FILES:
            print 'Copying %s to %s ...' % (file, os.path.join(PREFIX, FILES[file])) ,
            if subprocess.call(['install', file, os.path.join(PREFIX, os.path.join(FILES[file], file))]):
                print 'Failed'
                print '\n%s failed to install.' % APPLICATION
                sys.exit(1)
            else:
                print 'Done'

        print '\n%s %s is now installed.' % (APPLICATION, VERSION)
    
    else:
        print 'Uninstalling %s %s :\n' % (APPLICATION, VERSION)
        
        for file in FILES:
            print 'Removing %s ...' % os.path.join(PREFIX, os.path.join(FILES[file], file)) ,
            if subprocess.call(['rm', os.path.join(PREFIX, os.path.join(FILES[file], file))]):
                print 'Failed'
                print '\nFailed to uninstall %s.' % APPLICATION
                sys.exit(1)
            else:
                print 'Done'
        
        for dir in DIRECTORIES:
            print 'Removing directory %s ...' % os.path.join(PREFIX, dir) ,
            if subprocess.call(['rm', '-rf', os.path.join(PREFIX, dir)]):
                print 'Failed'
                print '\n%s failed to install.' % APPLICATION
                sys.exit(1)
            else:
                print 'Done'
        
        print '\n%s %s has been uninstalled.' % (APPLICATION, VERSION)
