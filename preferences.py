import os, os.path
from ConfigParser import SafeConfigParser

PREFS_FILE = 'colorwalkrc'
PREFS_DIR = os.path.expanduser('~/.config/colorwalk')
PREFS_PATH = os.path.join(PREFS_DIR, PREFS_FILE)

DEFAULTS = """[Window]
position=remember
show_toolbar=true
show_statusbar=true
show_scrollbars=true

[Background]
default=true
color=#000000

[Image]
size=width
quality=bilinear

[Behavior]
direction=ltr
turn_page_by_scroll=false
smart_scrolling=true

[Bookmarks]
open_last_on_start=false
bookmark_page_on_exit=false
max=0

"""

class Preferences(SafeConfigParser):
    
    def __init__(self):
        
        SafeConfigParser.__init__(self)
        
        if not os.path.isdir(PREFS_DIR):
            os.mkdir(PREFS_DIR)
        
        try:
            fb = open(PREFS_PATH)
        except IOError:
            fb = open(PREFS_PATH, 'w')
            fb.write(DEFAULTS)
            fb.close()
            fb = open(PREFS_PATH)
        
        self.readfp(fb, PREFS_FILE)
        fb.close()
        
    
    def save(self):
        fb = open(PREFS_PATH, 'w')
        self.write(fb)
        fb.close()
    
    
    def __del__(self):
        self.save()
        
