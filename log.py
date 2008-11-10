import gtk


class Log(object):
    
    stdout = []
    stderr = []
    
    messages = []
    errors = []
    
    def clear(self:
        self.stdout = []
        self.stderr = []
        
        self.messages = []
        self.errors = []


class LogViewer(gtk.Window):
    
    width = 400
    height = 400
    
    def __init__(self, app):
        
        self.app = app
        self.win = app.win
        
        self.ui = app.win.ui
        self.app(self.ui.get_widget('vbox10'))
        
        self.info_view = self.ui.get_widget('treeview1')
        self.errors_view = self.ui.get_widget('treeview2')
        self.terminal_view = self.ui.get_widget('textview1')
        
        gtk.Window.__init__(self)
        
        self.set_icon_name('text')
        self.set_title('Message Log')
        self.resize(self.width, self.height)
        self.show()
    
