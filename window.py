import os, os.path

import gtk, gtk.glade, pango

from callbacks import Callbacks
from statusbar import StatusBar
from image import get_thumbnail, new_pixbuf, FIT_BY_WIDTH, FIT_WINDOW, DEFAULT_SIZE
from utils import get_uri_for_path

SCROLL_LTR = 0
SCROLL_RTL = 1


class Window(gtk.Window):
    
    is_fullscreen = False
    width = 800
    height = 800
    
    def __init__(self, app, ui):
        self.app = app
        app.win = self
        
        gtk.Window.__init__(self)
        
        self.ui = gtk.glade.XML(ui, 'vbox1')
        self.add(self.ui.get_widget('vbox1'))
        
        self.image = self.ui.get_widget('image3')
        self.toolbar = self.ui.get_widget('toolbar1')
        self.statusbar = StatusBar(self, self.ui)
        
        self.callbacks = Callbacks(self)
        
        self.get_preferences()
        self.set_recent_files()
        
        self.connect('delete-event', self.callbacks.quit)
        self.connect('configure-event', self.callbacks.window_resized)
        self.connect('key-press-event', self.callbacks.key_pressed)
        
        dic = {
            'on_back_clicked'       : self.callbacks.go_back,
            'on_forward_clicked'    : self.callbacks.go_forward,
            'on_open_clicked'       : self.callbacks.open,
            'on_close_clicked'      : self.callbacks.close,
            'on_about_clicked'      : self.callbacks.about,
            'on_entry_activate'     : self.callbacks.jump,
            'on_combobox_changed'   : self.callbacks.rescale,
            'on_help_clicked'       : self.callbacks.help,
            'on_fullscreen_clicked' : self.callbacks.toggle_fullscreen,
            'on_preferences_clicked': self.callbacks.preferences,
            'on_bookmark_clicked'   : self.callbacks.add_bookmark,
            'on_go_clicked'         : self.callbacks.go_to_bookmark
        }
        self.ui.signal_autoconnect(dic)
        
        self.ui.get_widget('combobox1').set_active(self.app.scale)
        
        self.ui.get_widget('toolbutton2').set_flags(gtk.CAN_FOCUS)
        
        self.set_icon_name('image')
        self.set_title('Color Walk')
        self.resize(self.width, self.height)
        self.show()
    
    
    def refresh(self):
        self.statusbar.set_text('Current image: <i>%s</i>' % 
                              self.app.archive.images[self.app.archive.current])
            
        self.set_pages(len(self.app.archive.images))
        self.set_page(self.app.archive.current + 1)
            
        self.statusbar.set_size(self.app.archive.size)
        self.statusbar.set_res(self.app.current_pb.get_width(),
                               self.app.current_pb.get_height())
            
        self.ui.get_widget('toolbutton7').show()
        
        self.ui.get_widget('combobox1').set_sensitive(True)
        self.ui.get_widget('toolbutton13').set_sensitive(True)
        self.ui.get_widget('toolbutton15').set_sensitive(True)
        
        if self.app.bookmarks.has_key(self.app.archive.path):
            self.ui.get_widget('toolbutton21').set_sensitive(True)
        else:
            self.ui.get_widget('toolbutton21').set_sensitive(False)
        
        if self.app.archive.current < (len(self.app.archive.images) -1):
            self.ui.get_widget('toolbutton2').set_sensitive(True)
        else:
            self.ui.get_widget('toolbutton2').set_sensitive(False)
        if self.app.archive.current > 0:
            self.ui.get_widget('toolbutton1').set_sensitive(True)
        else:
            self.ui.get_widget('toolbutton1').set_sensitive(False)
        
        self.reset_scrollbars()
        self.steal_focus()
        
    
    def steal_focus(self):
        # Focus the forward button so that spacebar presses don't activate 
        # other tool buttons.
        self.ui.get_widget('toolbutton2').grab_focus()
    
    
    def reset_scrollbars(self, mode=SCROLL_LTR):
        viewport = self.ui.get_widget('scrolledwindow1')
        hadj = viewport.get_hadjustment()
        vadj = viewport.get_vadjustment()
        vadj.set_value(vadj.lower)
        
        
        if mode == SCROLL_RTL:
            # TODO: Hook this up to the preferences.
            hadj.set_value(hadj.upper)
        else: # RTL
            hadj.set_value(hadj.lower)
        
        viewport.set_hadjustment(hadj)
        viewport.set_vadjustment(vadj)
    
    
    def blank(self):
        self.set_title('Color Walk')
        self.statusbar.set_text('')
                                
        self.image.clear()
        
        self.statusbar.hide_all()
        
        self.ui.get_widget('combobox1').set_sensitive(False)
        self.ui.get_widget('toolbutton1').set_sensitive(False)
        self.ui.get_widget('toolbutton2').set_sensitive(False)
        self.ui.get_widget('toolbutton13').set_sensitive(False)
        self.ui.get_widget('toolbutton15').set_sensitive(False)
        
        self.ui.get_widget('label6').hide()
        self.ui.get_widget('entry1').hide()
        self.ui.get_widget('toolbutton7').hide()
    
    
    def set_pages(self, pages):
        self.ui.get_widget('label6').show()
        self.ui.get_widget('label6').set_text(' of %d' % pages)
    
    
    def set_page(self, page):
        self.ui.get_widget('entry1').show()
        self.ui.get_widget('entry1').set_text('%d' % page)
    
    
    def get_view_width(self):
        # FIXME: Get the actual width of the scrollbar + any padding.
        return self.width - 21
    
    
    def get_view_height(self):
        # FIXME: Get the actual height of the menubar + statusbar
        #        + any padding.
        return self.height - 64
    
    
    def load_current(self):
        self.app.current_pb = new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                                         self.app.archive.images
                                         [self.app.archive.current]),
                                         self.app.scale,
                                         width=self.get_view_width(),
                                         height=self.get_view_height())
        self.image.set_from_pixbuf(self.app.current_pb)
        self.refresh()
    
    
    def load_previous(self):
        self.app.previous_pb = new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                                         self.app.archive.images
                                         [self.app.archive.current - 1]),
                                         self.app.scale,
                                         width=self.get_view_width(),
                                         height=self.get_view_height())
        self.refresh()
    
    
    def load_next(self):
        self.app.next_pb = new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                                         self.app.archive.images
                                         [self.app.archive.current + 1]),
                                         self.app.scale,
                                         width=self.get_view_width(),
                                         height=self.get_view_height())
        self.refresh()
    
    
    def get_preferences(self):
        if self.app.prefs.get('Image', 'size') == 'width':
            self.app.scale = FIT_BY_WIDTH
        elif self.app.prefs.get('Image', 'size') == 'fit':
            self.app.scale = FIT_WINDOW
        elif self.app.prefs.get('Image', 'size') == 'default':
            self.app.scale = DEFAULT_SIZE
    
    
    def set_recent_files(self):
        menu = gtk.Menu()
        self.ui.get_widget('toolbutton10').set_menu(menu)
        
        self.app.recent.prune()
        
        for file in self.app.recent.read():
            # TODO: Use the thumbnail instead of a generic icon
            img = gtk.image_new_from_icon_name('package', 1)
            
            label = gtk.Label(os.path.split(file)[1])
            label.set_alignment(0, 0)
            label.set_width_chars(50)
            label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
            
            item = gtk.ImageMenuItem(stock_id=None, accel_group=None)
            item.set_image(img)
            item.add(label)
            item.set_has_tooltip(True)
            item.connect('activate', self.callbacks.open_recent, file)
            
            def show_tip(widget, x, y, keyboard_mode, tooltip, file):
                thumb = get_thumbnail(get_uri_for_path(file))
                
                if thumb:
                    tooltip.set_icon(thumb)
                    return True
                else:
                    return False
                
            
            item.connect('query-tooltip', show_tip, file)
            
            menu.append(item)
        
        menu.show_all()
        
