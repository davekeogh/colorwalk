import gtk

from image import get_thumbnail
from utils import open_url

# TODO: Find a better place for this?
GPL_V2 = """This program is free software; you can redistribute it\
 and/or modify it under the terms of the GNU General Public License as\
 published by the Free Software Foundation; either version 2 of the\
 License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but\
 WITHOUT ANY WARRANTY; without even the implied warranty of\
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\
 General Public License for more details.

You should have received a copy of the GNU General Public License along\
 with this program; if not, write to the Free Software Foundation, Inc.,\
 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
"""

def choose_file(path=None):
    dialog = FileChooserDialog()
    
    if path:
        dialog.set_current_folder(path)
    
    response = dialog.run()
    file = dialog.get_filename()
    dialog.destroy()
    
    if response == gtk.RESPONSE_ACCEPT:
        return file
    else:
        return None


class FileChooserDialog(gtk.FileChooserDialog):
    
    def __init__(self):
        
        gtk.FileChooserDialog.__init__(self, title='Open File',
                                       buttons=(gtk.STOCK_CANCEL, 
                                                gtk.RESPONSE_REJECT,
                                                gtk.STOCK_OK,
                                                gtk.RESPONSE_ACCEPT))
        
        self.connect('selection-changed', self.set_preview)
        
        self.set_preview_widget(gtk.Image())
        
        self.set_icon_name('fileopen')
        
        main_filter = gtk.FileFilter()
        main_filter.set_name('All Supported Files')
        main_filter.add_pattern('*.cbz')
        main_filter.add_pattern('*.cbr')
        main_filter.add_pattern('*.zip')
        main_filter.add_pattern('*.rar')
        
        comic_filter = gtk.FileFilter()
        comic_filter.set_name('Comic Book Archives')
        comic_filter.add_pattern('*.cbz')
        comic_filter.add_pattern('*.cbr')
        
        arc_filter = gtk.FileFilter()
        arc_filter.set_name('Archives')
        arc_filter.add_pattern('*.zip')
        arc_filter.add_pattern('*.rar')
        
        all_filter = gtk.FileFilter()
        all_filter.set_name('All Files')
        all_filter.add_pattern('*')
        
        self.add_filter(main_filter)
        self.add_filter(comic_filter)
        self.add_filter(arc_filter)
        self.add_filter(all_filter)
    
    
    def set_preview(self, chooser):
        if self.get_uri():
            pb = get_thumbnail(self.get_uri())
        
            if pb:
                self.get_preview_widget().set_from_pixbuf(pb)
                
            else:
                self.get_preview_widget().clear()
        

class AboutDialog(gtk.AboutDialog):
    
    website = 'http://members.shaw.ca/davekeogh/colorwalk/'
    copyright = 'Copyright (c) 2008 David Keogh'
    authors = ['David Keogh <davekeogh@shaw.ca>']
    
    def __init__(self):
        # TODO: Set the version here from the build script.
        
        def url_hook(dialog, link, data):
            open_url(link)
        
        def email_hook(dialog, link, data):
            open_url('mailto:%s' % link)
        
        gtk.about_dialog_set_url_hook(url_hook, data=None)
        gtk.about_dialog_set_email_hook(email_hook, data=None)
        
        gtk.AboutDialog.__init__(self)
        self.set_icon_name('help-about')
        self.set_name('Color Walk')
        self.set_copyright(self.copyright)
        self.set_authors(self.authors)
        self.set_website(self.website)
        self.set_license(GPL_V2)
        self.set_wrap_license(True)
    
