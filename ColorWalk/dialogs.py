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

import gtk


LICENSE = '''This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.'''


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


def open_email(dialog, link, user_data):
    '''Attempts to open the default email program to send an email.'''
    
    subprocess.call(['xdg-open', 'mailto:%s' % link])


def open_url(dialog, link, user_data):
    '''Opens a url in the default web browser.'''
    
    subprocess.call(['xdg-open', link])


class AboutDialog(gtk.AboutDialog):
    
    def __init__(self):
        '''A GTK+ about dialog that displays the license a link to the website
        etc.'''
        
        # This is as good a spot as any to set these hooks.
        gtk.about_dialog_set_email_hook(open_email, None)
        gtk.about_dialog_set_url_hook(open_url, None)
        
        # We don't use gtk.LinkButton, but gtk.AboutDialog does. In gtk 2.16+
        # without this, the about uri opens twice:
        gtk.link_button_set_uri_hook(lambda *args:None)

        gtk.AboutDialog.__init__(self)
        
        self.set_logo_icon_name('image')
        self.set_name('Color Walk')
        self.set_version('0.1.0')
        self.set_comments('A really simple comic book reading application')
        self.set_copyright('Copyright (c) 2009 David Keogh')
        self.set_authors(['David Keogh <davekeogh@shaw.ca>'])
        self.set_license(LICENSE)
        self.set_wrap_license(True)
        self.set_website('http://members.shaw.ca/davekeogh/')


class FloatingToolbar(gtk.Window):
    
    parent = None
    toolbar = None
    
    def __init__(self, parent, toolbar):
        '''A copy of Color Walk's toolbar in a undecorated gtk.Window. This
        allows us to position it overtop of the displayed image and show and
        hide it easily.'''
        
        self.parent = parent
        self.toolbar = toolbar
        
        gtk.Window.__init__(self)
        self.add(toolbar)
        
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_property('skip-taskbar-hint', True)
        self.set_property('skip-pager-hint', True)
        
        self.resize(self.get_screen().get_width(), 32)
        self.move(0, self.get_screen().get_height() + 32)


class PreferencesDialog(gtk.Dialog):
    
    parent = None
    preferences = None
    widgets = None
    
    def __init__(self, parent):
        '''A dialog that allows the user to modify the application's appearance
        and behavior.'''
        
        self.parent = parent
        self.preferences = parent.preferences
        self.widgets = parent.widgets
        
        gtk.Dialog.__init__(self, 'Color Walk Preferences', self,
                            gtk.DIALOG_MODAL | gtk.DIALOG_NO_SEPARATOR, ())
        
        self.get_content_area().add((self.widgets.get_object('prefs-vbox')))
        button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        button.grab_default()
        button.grab_focus()
        self.set_icon_name('preferences-desktop')
        
        self.widgets.get_object('editor_entry').connect('changed', self.editor_text_changed)
        
        self.load()
    
    def destroy(self):
        '''A custom destroy method that removes the widgets first so that they
        can be added to another dialog later if necessary.'''
        
        self.get_content_area().remove(self.widgets.get_object('prefs-vbox'))
        gtk.Dialog.destroy(self)
    
    def editor_text_changed(self, entry):
        '''A callback connected to the entry's text-changed signal. It verifies
        that the entered executable does in fact exists and displays an icon.'''
        
        if not self.widgets.get_object('editor_entry').get_text():
                self.widgets.get_object('editor_image').set_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)
        else:
            if find_executable(self.widgets.get_object('editor_entry').get_text()):
                self.widgets.get_object('editor_image').set_from_stock(gtk.STOCK_YES, gtk.ICON_SIZE_BUTTON)
            else:
                self.widgets.get_object('editor_image').set_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)
    
    def load(self):
        '''Gets the values from the Preferences object and inputs them into the
        appropriate widgets. '''
        
        if self.preferences.get('Preferences', 'editor'):
            self.widgets.get_object('editor_entry').set_text(self.preferences.get('Preferences', 'editor'))
        
        self.widgets.get_object('toolbar_checkbutton').set_active(self.preferences.getboolean('Window', 'show_toolbar'))
        self.widgets.get_object('fullscreen_checkbutton').set_active(self.preferences.getboolean('Window', 'fullscreen'))
        
        bg = self.preferences.get('Preferences', 'background')
        
        if bg == 'match':
            self.widgets.get_object('match_radiobutton').set_active(True)
        
        elif bg == 'theme':
            self.widgets.get_object('theme_radiobutton').set_active(True)
        
        else:
            self.widgets.get_object('custom_radiobutton').set_active(True)
            self.widgets.get_object('colorbutton').set_color(gtk.gdk.color_parse(bg))
    
    def save(self):
        '''Copy values marked in the dialog into the Preferences object.'''
        
        self.preferences.set('Preferences', 'editor', self.widgets.get_object('editor_entry').get_text())
        self.preferences.set('Window', 'show_toolbar', str(self.widgets.get_object('toolbar_checkbutton').get_active()))
        self.preferences.set('Window', 'fullscreen', str(self.widgets.get_object('fullscreen_checkbutton').get_active()))
        
        if self.widgets.get_object('match_radiobutton').get_active():
            self.preferences.set('Preferences', 'background', 'match')
        
        elif self.widgets.get_object('theme_radiobutton').get_active():
            self.preferences.set('Preferences', 'background', 'theme')
        
        else:
            self.preferences.set('Preferences', 'background', self.widgets.get_object('colorbutton').get_color().to_string())
