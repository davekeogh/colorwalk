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


try:
    import numpy
except ImportError:
    numpy = None


import utilities


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


class AboutDialog(gtk.AboutDialog):
    
    def __init__(self):
        '''A GTK+ about dialog that displays the license a link to the website
        etc.'''
        
        # This is as good a spot as any to set these hooks.
        gtk.about_dialog_set_email_hook(utilities.open_email, None)
        gtk.about_dialog_set_url_hook(utilities.open_url, None)
        
        # We don't use gtk.LinkButton, but gtk.AboutDialog does. In gtk 2.16+
        # without this, the about uri opens twice:
        gtk.link_button_set_uri_hook(lambda *args:None)

        gtk.AboutDialog.__init__(self)
        
        self.set_logo_icon_name('image')
        self.set_name('Color Walk')
        self.set_version('0.1.1')
        self.set_comments('A really simple comic book reading application')
        self.set_copyright('Copyright (c) 2009 David Keogh')
        self.set_authors(['David Keogh <davekeogh@shaw.ca>'])
        self.set_license(LICENSE)
        self.set_wrap_license(True)
        self.set_website('http://members.shaw.ca/davekeogh/')


class FloatingToolbar(gtk.Dialog):
    
    parent = None
    widgets = None
    
    def __init__(self, parent):
        '''A copy of Color Walk's toolbar in a undecorated gtk.Window. This
        allows us to position it overtop of the displayed image and show and
        hide it easily.'''
        
        self.parent = parent
        self.widgets = parent.widgets
        
        gtk.Window.__init__(self)
        self.get_content_area().add(parent.widgets.get_object('fullscreen_toolbar'))
        
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_transient_for(parent)
        self.set_property('skip-taskbar-hint', True)
        self.set_property('skip-pager-hint', True)
        self.set_has_separator(False)
        
        self.resize(self.get_screen().get_width(), 32)
        self.move(0, self.get_screen().get_height() + 32)
    
    def destroy(self):
        '''A custom destroy method that removes the widgets first so that they
        can be added to another dialog later if necessary.'''
        
        self.get_content_area().remove(self.widgets.get_object('fullscreen_toolbar'))
        gtk.Dialog.destroy(self)


class HelpDialog(gtk.Dialog):
    
    parent = None
    widgets = None
    
    def __init__(self, parent):
        '''A dialog that displays a list of keyboard shortcuts.'''
        
        self.parent = parent
        self.widgets = parent.widgets
        
        gtk.Dialog.__init__(self, 'Color Walk Help', parent,
                            gtk.DIALOG_MODAL | gtk.DIALOG_NO_SEPARATOR, ())
        
        self.get_content_area().add((parent.widgets.get_object('dialog-vbox')))
        
        button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        button.grab_default()
        button.grab_focus()
        
        self.set_icon_name('help')
        self.resize(350, 200)
    
    def destroy(self):
        '''A custom destroy method that removes the widgets first so that they
        can be added to another dialog later if necessary.'''
        
        self.get_content_area().remove(self.widgets.get_object('dialog-vbox'))
        gtk.Dialog.destroy(self)


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
        
        gtk.Dialog.__init__(self, 'Color Walk Preferences', parent,
                            gtk.DIALOG_MODAL | gtk.DIALOG_NO_SEPARATOR, ())
        
        self.get_content_area().add((self.widgets.get_object('prefs-vbox')))
        
        button = self.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        button.grab_default()
        button.grab_focus()
        
        self.set_icon_name('preferences-desktop')
        
        self.widgets.get_object('editor_entry').connect('changed', self.editor_text_changed)
        
        if not numpy:
            self.widgets.get_object('match_radiobutton').set_sensitive(False)
            self.widgets.get_object('match_radiobutton').set_tooltip_markup('This feature requires the <b>numpy</b> module. Check your package manager to see if it can be installed.')
        
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
            if utilities.find_executable(self.widgets.get_object('editor_entry').get_text()):
                self.widgets.get_object('editor_image').set_from_stock(gtk.STOCK_YES, gtk.ICON_SIZE_BUTTON)
            else:
                self.widgets.get_object('editor_image').set_from_stock(gtk.STOCK_NO, gtk.ICON_SIZE_BUTTON)
    
    def load(self):
        '''Gets the values from the Preferences object and inputs them into the
        appropriate widgets. '''
        
        if self.preferences.get('Preferences', 'editor'):
            self.widgets.get_object('editor_entry').set_text(self.preferences.get('Preferences', 'editor'))
        
        self.widgets.get_object('toolbar_checkbutton').set_active(self.preferences.getboolean('Window', 'show_toolbar'))
        
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
        
        if self.widgets.get_object('match_radiobutton').get_active():
            self.preferences.set('Preferences', 'background', 'match')
        
        elif self.widgets.get_object('theme_radiobutton').get_active():
            self.preferences.set('Preferences', 'background', 'theme')
        
        else:
            self.preferences.set('Preferences', 'background', self.widgets.get_object('colorbutton').get_color().to_string())
