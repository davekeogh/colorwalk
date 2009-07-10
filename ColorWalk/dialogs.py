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

import gtk


LICENSE = '''This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>.'''


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
