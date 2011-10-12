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

import os, os.path, configparser

from .globals import FIT_BY_WIDTH


class Preferences(configparser.SafeConfigParser):
    
    config_file = os.path.expanduser('~/.config/colorwalk/config')
    
    def __init__(self):
        '''Represents a configuration file at ~/.config/colorwalk/config. 
        Creates one with the default values if it does not exist.'''
        
        # TODO: Some sort of fallback if the file or directory can't be created
        
        configparser.SafeConfigParser.__init__(self)
        
        if not os.path.exists(os.path.split(self.config_file)[0]):
            os.mkdir(os.path.split(self.config_file)[0])
        
        if os.path.exists(self.config_file):
            self.read(self.config_file)
        
        else:
            # Set some reasonable default values
            self.add_section('Window')
            self.set('Window', 'width', str(800))
            self.set('Window', 'height', str(800))
            self.set('Window', 'maximized', str(False))
            self.set('Window', 'show_toolbar', str(True))
            
            self.add_section('Image')
            self.set('Image', 'scale', str(FIT_BY_WIDTH))
            
            self.add_section('Preferences')
            self.set('Preferences', 'editor', '')
            self.set('Preferences', 'background', 'theme')
    
    def save(self):
        with open(self.config_file, 'w') as f:
            self.write(f)
