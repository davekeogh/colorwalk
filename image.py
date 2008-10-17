import os, os.path, subprocess, gc
import gtk

from archive import MAGIC

try:
    import hashlib
    NEW_MD5 = hashlib.md5
except ImportError:
    import md5
    NEW_MD5 = md5.new


try:
    import gconf
    CLIENT = gconf.client_get_default()
    CBR_THUMBNAILER = CLIENT.get_string \
    ('/desktop/gnome/thumbnailers/application@x-cbr/command')
    CBZ_THUMBNAILER = CLIENT.get_string \
    ('/desktop/gnome/thumbnailers/application@x-cbz/command')
except ImportError:
    CBR_THUMBNAILER = None
    CBZ_THUMBNAILER = None


IMAGES = ['JPEG image data', 'PNG image data', 'GIF image data']
EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']


FIT_BY_WIDTH = 0
FIT_WINDOW = 1
DEFAULT_SIZE = 2


def create_thumbnail(uri):
    return


def get_thumbnail(uri):
    m = NEW_MD5()
    m.update(uri)
    
    thumb_dir = os.path.join(os.environ['HOME'], '.thumbnails/normal')
    thumb_file = '%s.png' % m.hexdigest()
    thumb_path = os.path.join(thumb_dir, thumb_file)
    
    if os.path.isfile(thumb_path):
        return new_pixbuf(thumb_path, DEFAULT_SIZE)
    else:
        return None    


def new_pixbuf(path, mode, width=-1, height=-1):
    if mode == DEFAULT_SIZE:
        return gtk.gdk.pixbuf_new_from_file_at_size(path, -1, -1)
    elif mode == FIT_BY_WIDTH:
        return gtk.gdk.pixbuf_new_from_file_at_size(path, width, -1)
    elif mode == FIT_WINDOW:
        if width > height:
            return gtk.gdk.pixbuf_new_from_file_at_size(path, -1, height)
        elif height > width:
            return gtk.gdk.pixbuf_new_from_file_at_size(path, width, 
                                                        -1)
        else:
            return gtk.gdk.pixbuf_new_from_file_at_size(path, width,
                                                        height)
    
    # gtk.gdk.Pixbuf()s don't seem to be collected properly. I'm not
    # sure if this is the best spot to call the garbage collecter
    # though.
    gc.collect()


def is_image_ext(path):
    if os.path.splitext(path)[1].lower() in EXTENSIONS:
        return True
    else:
        return False


def is_image_file(path):
    if not MAGIC:
        p = subprocess.Popen('file %s' % path, shell=True, 
                             stdout=subprocess.PIPE)
        p.wait()
        stdout = p.stdout.read()
        part = stdout.split(': ')[1]
        print part
        
        found = False
        for type in IMAGES:
            if part.startswith(type):
                found = True
                break
        
        if found:
            return True
        else:
            return False

