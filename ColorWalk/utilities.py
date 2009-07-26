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

import os, os.path, subprocess


def find_executable(name):
    '''Tries to find an executable that's being used by as a helper application.
    If the program is found anywhere in PATH it returns true; otherwise it
    returns false.'''
    
    for path in os.environ['PATH'].split(':'):
        if os.path.exists(os.path.join(path, name)):
            return True
    
    return False


def open_email(dialog, link, user_data):
    '''Attempts to open the default email program to send an email.'''
    
    subprocess.call(['xdg-open', 'mailto:%s' % link])


def open_url(dialog, link, user_data):
    '''Opens a url in the default web browser.'''
    
    subprocess.call(['xdg-open', link])
