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

import sys, os, os.path, gc, subprocess

import gtk


IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.gif', '.png', '.bmp')
DEFAULT_SIZE = 123
FIT_BY_WIDTH = 456

LICENSE = '''This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.'''


def choose_file(path=None):
    '''Creates a gtk.FileChooser and returns the value when the dialog is 
    destroyed.'''
    
    dialog = gtk.FileChooserDialog(title='Open File', buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    
    if path:
        dialog.set_current_folder(path)
    
    filter = gtk.FileFilter()
    filter.set_name('All supported files')
    filter.add_pattern('*.cbz')
    filter.add_pattern('*.cbr')
    filter.add_pattern('*.zip')
    filter.add_pattern('*.rar')
    dialog.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name('All files')
    filter.add_pattern('*')
    dialog.add_filter(filter)
    
    if dialog.run() == gtk.RESPONSE_ACCEPT:
        file = dialog.get_filename()
    
    else:
        file = None
    
    dialog.destroy()
    
    return file


def find_average_border_color(pixels, width, height):
    ''' Finds a roughly average color to use as the background of the window
    based on the corner colors of the image.'''
    
    # TODO: Sample more areas along the border of the image to get a better
    #       average.
    
    c1 = pixels[0][0] # top left
    c2 = pixels[height - 1][0] # bottom left
    c3 = pixels[0][width - 1] # top right
    c4 = pixels[height - 1][width - 1] # bottom right
    
    def average(values):
        '''Computes the arithmetic mean of a list of numbers.'''
        
        return sum(values) / len(values)
    
    r = int(average([c1[0], c2[0], c3[0], c4[0]]))
    g = int(average([c1[1], c2[1], c3[1], c4[1]]))
    b = int(average([c1[2], c2[2], c3[2], c4[2]]))
    
    return '#%02x%02x%02x' % (r, g, b)


def find_executable(name):
    '''Tries to find an executable that's being used by as a helper application.
    If the program is found anywhere in PATH it returns true; otherwise it
    returns false.'''
    
    paths = os.environ['PATH'].split(':')
    found = False
    
    for path in paths:
        full_path = os.path.join(path, name)
        
        if os.path.exists(full_path):
            found = True
    
    return found


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


def new_pixbuf(path, mode, width=-1, height=-1):
    '''Returns a gtk.gdk.Pixbuf object at the appropriate size.'''
    
    if mode == DEFAULT_SIZE:
        return gtk.gdk.pixbuf_new_from_file(path)
    elif mode == FIT_BY_WIDTH:
        temp = gtk.gdk.pixbuf_new_from_file(path)
        
        if temp.get_width() > width:
            del temp
            return gtk.gdk.pixbuf_new_from_file_at_size(path, width, -1)
        else:
            return temp
    
    # gtk.gdk.Pixbufs don't seem to be collected properly. I'm not sure if this
    # is the best spot to call the garbage collecter though.
    gc.collect()


def open_email(dialog, link, user_data):
    '''Attempts to open the default email program to send an email.'''
    
    subprocess.call(['xdg-open', 'mailto:%s' % link])


def open_url(dialog, link, user_data):
    '''Opens a url in the default web browser.'''
    
    subprocess.call(['xdg-open', link])
