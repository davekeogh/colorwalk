import os, os.path, subprocess

import gtk, gobject

from image import new_pixbuf, is_image_ext
from worker import Worker
from dialogs import AboutDialog, choose_file
from error import ArchiveError
from archive import Archive
from utils import open_url, is_text_file

class Callbacks(object):
    
    def __init__(self, win):
        self.win = win
        self.app = win.app
    
    
    def extracting_finished(self, worker):
        self.win.statusbar.clear_text()
        self.win.statusbar.progressbar.hide()
        
        self.win.set_title(self.app.archive.name)
        
        self.app.archive.files = os.listdir(self.app.archive.temp_dir)
        self.app.archive.files.sort(key=str.lower)
        
        self.app.archive.images = []
        self.app.archive.current = 0
        
        for file in self.app.archive.files:
            if is_image_ext(file):
                self.app.archive.images.append(file)
            if is_text_file(file):
                self.app.archive.text.append(file)
        
        if len(self.app.archive.images):
            self.app.recent.add(self.app.archive.path)
            self.app.win.set_recent_files()
            
            self.app.archive.size = \
            os.stat(self.app.archive.path).st_size / 1048576
            
            self.app.current_pb = \
            new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                       self.app.archive.images
                       [self.app.archive.current]),
                       self.app.scale,
                       width=self.app.win.get_view_width(),
                       height=self.app.win.get_view_height())
                       
            self.win.refresh()
            self.win.image.set_from_pixbuf(self.app.current_pb)
            
            gobject.idle_add(self.preload_next)
        
        else:
            message = 'No images found in <i>%s</i>' \
            % self.app.archive.name
            
            self.win.blank()
            self.win.statusbar.set_text(message)
            self.win.statusbar.set_error_icon()
            self.app.log.errors.append(message)
            self.app.reset()
            self.app.archive.remove_temp_dir()
            self.app.archive = None
    
    
    def open(self, widget, choose=True, path=None):
        if choose:
            file = choose_file(self.app.open_dir)
        else:
            file = path
        
        if file:
            self.app.open_dir = os.path.split(file)[0]
            
            self.close(widget)
            
            try:
                self.app.archive = Archive(file)
            except ArchiveError, error:
                self.win.statusbar.set_text(error.message)
                self.win.statusbar.set_error_icon()
                self.app.log.errors.append(error.message)
                self.app.archive = None
            
            if self.app.archive:
                self.app.win.statusbar.hide_all()
                self.app.worker = Worker(self.app)
                self.app.worker.connect('extracting-finished',
                             self.app.win.callbacks.extracting_finished)
                self.app.worker.set_function(self.app.archive.extract)
                self.app.worker.start()
    
    
    def open_recent(self, widget, path):
        self.open(widget, choose=False, path=path)
    
    
    def close(self, widget):
        if self.app.archive:
            self.app.reset()
            self.win.blank()
            self.app.archive.remove_temp_dir()
            self.app.archive = None
    
    
    def add_bookmark(self, widget):
        return
    
    
    def go_to_bookmark(self, widget):
        return
    
    
    def preferences(self, widget):
        return
    
    
    def about(self, widget):
        dialog = AboutDialog()
        if dialog.run():
            dialog.destroy()
    
    
    def go_back(self, widget):
        if self.app.archive.current > 0:
            self.app.next_pb = self.app.current_pb
            self.app.current_pb = self.app.previous_pb
            
            self.app.archive.current -= 1
            
            self.win.refresh()
            self.win.image.set_from_pixbuf(self.app.current_pb)
            
            gobject.idle_add(self.preload_previous)
    
    
    def go_forward(self, widget):
        # TODO: Implement smart paging here. Check the preferences
        #       value first to see if it's enabled.
        
        if self.app.archive.current < len(self.app.archive.images) - 1:
            self.app.previous_pb = self.app.current_pb
            self.app.current_pb = self.app.next_pb
            
            self.app.archive.current += 1
            
            self.win.refresh()
            self.win.image.set_from_pixbuf(self.app.current_pb)
            
            gobject.idle_add(self.preload_next)
    
    
    def jump(self, widget, page=None):
        if page:
            text = page
        else:
            text = widget.get_text()
        
        def fail():
            self.app.win.set_page(self.app.archive.current + 1)
            self.win.steal_focus()
        
        try:
            num = int(text)
            
            if num <= len(self.app.archive.images) and num > 0:
                self.app.archive.current = num - 1
                
                self.app.current_pb = \
                new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                self.app.archive.images[self.app.archive.current]),
                self.app.scale,
                width=self.app.win.get_view_width(),
                height=self.app.win.get_view_height())
                
                self.win.refresh()
                self.win.steal_focus()
                self.win.image.set_from_pixbuf(self.app.current_pb)
                
                try:
                    self.app.next_pb = \
                    new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                    self.app.archive.images[self.app.archive.current \
                    + 1]),
                    self.app.scale,
                    width=self.app.win.get_view_width(),
                    height=self.app.win.get_view_height())
                except IndexError:
                    self.app.next_pb = None
                
                try:
                    self.app.previous_pb = \
                    new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                    self.app.archive.images[self.app.archive.current \
                    - 1]),
                    self.app.scale,
                    width=self.app.win.get_view_width(),
                    height=self.app.win.get_view_height())
                except IndexError:
                    self.app.previous_pb = None
                
            else:
                fail()
        except ValueError:
            fail()
    
    
    def preload_next(self):
        if (self.app.archive.current + 1) <= \
        (len(self.app.archive.images) -1):
            self.app.next_pb = \
                new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                           self.app.archive.images
                           [self.app.archive.current + 1]),
                           self.app.scale,
                           width=self.app.win.get_view_width(),
                           height=self.app.win.get_view_height())
        
        return False
    
    
    def preload_previous(self):
        if (self.app.archive.current - 1) >= 0:
            self.app.previous_pb = \
                new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                           self.app.archive.images
                           [self.app.archive.current - 1]),
                           self.app.scale,
                           width=self.app.win.get_view_width(),
                           height=self.app.win.get_view_height())
        
        return False
    
    
    def window_resized(self, widget, allocation):
        if self.app.archive:
            if (self.win.width != allocation.width or
                self.win.height != allocation.height):
                
                self.win.width = allocation.width
                self.win.height = allocation.height
                
                if self.app.archive.images:
                    self.app.current_pb = \
                    new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                               self.app.archive.images
                               [self.app.archive.current]),
                               self.app.scale,
                               width=self.app.win.get_view_width(),
                               height=self.app.win.get_view_height())
                    self.win.image.set_from_pixbuf(self.app.current_pb)
                    
                    gobject.idle_add(self.preload_next)
                    gobject.idle_add(self.preload_previous)
        
        else:
            self.win.width = allocation.width
            self.win.height = allocation.height
    
    
    def rescale(self, widget):
        if self.app.archive:
            self.app.scale = widget.get_active()
            
            self.app.current_pb = \
            new_pixbuf(os.path.join(self.app.archive.temp_dir, 
                       self.app.archive.images
                       [self.app.archive.current]),
                       self.app.scale,
                       width=self.app.win.get_view_width(),
                       height=self.app.win.get_view_height())
            self.win.image.set_from_pixbuf(self.app.current_pb)
            
            gobject.idle_add(self.preload_next)
            gobject.idle_add(self.preload_previous)
    
    
    def key_pressed(self, widget, event):
        if self.app.archive:
            if event.keyval == 32: # Spacebar
                self.go_forward(widget)
            
            elif event.keyval == 65366: # Page Down
                self.go_forward(widget)
            
            elif event.keyval == 65288: # Backspace
                self.go_back(widget)
            
            if event.keyval == 65365: # Page Up
                self.go_back(widget)
            
            elif event.keyval == 65480: # F11
                self.toggle_fullscreen(widget)
            
            elif event.keyval == 65360: # Home
                self.jump(widget, 1)
            
            elif event.keyval == 65367: # End
                self.jump(widget, len(self.app.archive.images))
    
    
    def toggle_fullscreen(self, widget):
        if self.win.is_fullscreen:
            self.win.is_fullscreen = False
            self.win.ui.get_widget('toolbar1').show()
            self.win.ui.get_widget('hbox1').show()
            self.win.unfullscreen()
        
        elif not self.win.is_fullscreen:
            self.win.is_fullscreen = True
            self.win.ui.get_widget('toolbar1').hide()
            self.win.ui.get_widget('hbox1').hide()
            self.win.fullscreen()
    
    
    def help(self, widget):
        # TODO: Full path to manual.html
        open_url('manual.html')
    
    
    def quit(self, widget, event=None):
        if self.app.archive:
            self.app.archive.remove_temp_dir()
        gtk.main_quit()
