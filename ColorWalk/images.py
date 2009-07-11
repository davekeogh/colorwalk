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

import gc, os, os.path, threading

import gtk

from globals import DEFAULT_SIZE, FIT_BY_WIDTH


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
    
    # Pixbufs don't get collected properly with older versions of pygtk:
    gc.collect()


def preload_images(window, next=True, prev=True):
    '''Loads the pages into memory. This spawns a new thread to avoid blocking 
    the UI'''
    
    def worker():
        '''Runs in the background to avoid blocking the UI. Opens the required
        images.'''
        
        window.lock.acquire()
        
        if next:
            try:
                window.next_pixbuf = new_pixbuf(os.path.join(window.temp_dir, window.images[window.index + 1]), window.scale, *window.get_available_space())
            except IndexError:
                window.next_pixbuf = None
        
        if prev:
            try:
                window.prev_pixbuf = new_pixbuf(os.path.join(window.temp_dir, window.images[window.index - 1]), window.scale, *window.get_available_space())
            except IndexError:
                window.prev_pixbuf = False
            
        window.lock.release()
    
    threading.Thread(target=worker).start()


def reload_all(window):
    '''Loads all the images into memory then re-displays the current one. This 
    spawns a new thread to avoid blocking the UI'''
    
    def worker():
        '''Runs in the background to avoid blocking the UI. Opens the required
        images.'''
        
        window.lock.acquire()
        
        window.current_pixbuf = new_pixbuf(os.path.join(window.temp_dir, window.images[window.index]), window.scale, *window.get_available_space())
        window.widgets.get_object('image').set_from_pixbuf(window.current_pixbuf)
        
        try:
            window.next_pixbuf = new_pixbuf(os.path.join(window.temp_dir, window.images[window.index + 1]), window.scale, *window.get_available_space())
        except IndexError:
            window.next_pixbuf = None
        
        try:
            window.prev_pixbuf = new_pixbuf(os.path.join(window.temp_dir, window.images[window.index - 1]), window.scale, *window.get_available_space())
        except IndexError:
            window.prev_pixbuf = None
        
        window.lock.release()
    
    threading.Thread(target=worker).start()
