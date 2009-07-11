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

import os, os.path

import gtk


from dialogs import AboutDialog, PreferencesDialog, HelpDialog, choose_file

from images import *

from globals import DEFAULT_SIZE, FIT_BY_WIDTH, IMAGE_EXTENSIONS

from preferences import Preferences

from utilities import *


def find_ui_definition():
    '''Tries to find the XML GtkBuilder file in all the usual places. The first
    place to be checked is the current working directory. If it's found we
    assume that we're debugging. If the file can't be found this function
    returns None.'''
    
    paths = os.environ['XDG_DATA_DIRS'].split(':')
    return_value = None
    
    # This is mostly so that debugging isn't a pain in the ass.
    local = os.path.join(os.getcwd(), 'colorwalk.ui')
    
    if os.path.exists(local):
        return_value = local
    
    if not return_value:
        for path in paths:
            full_path = os.path.join(path, 'colorwalk/colorwalk.ui')
            
            if os.path.exists(full_path):
                return_value = full_path
                break
    
    return return_value
