import os, os.path, tempfile, shutil, subprocess

from error import ArchiveError

ZIP = 0
RAR = 1

ZIP_MIMES = ('application/x-zip', 'application/x-cbz')
RAR_MIMES = ('application/x-rar', 'application/x-cbr')

try:
    import magic
    MAGIC = True
    MS = magic.open(magic.MAGIC_NONE)
    MS.load()
except ImportError:
    MAGIC = False
    print MAGIC_WARNING



def is_zip_file(path):
    if not MAGIC:
        p = subprocess.Popen('file \"%s\"' % path, shell=True, 
                             stdout=subprocess.PIPE)
        p.wait()
        stdout = p.stdout.read()
        
        if stdout.split(': ')[1].startswith('Zip archive data'):
            return True
        else:
            return is_mime_correct(path, ZIP_MIMES)
    
    else:
        type =  MS.file(path)
        
        if type.startswith('Zip archive data'):
            return True
        else:
            return is_mime_correct(path, ZIP_MIMES)


def is_rar_file(path):
    if not MAGIC:
        p = subprocess.Popen('file \"%s\"' % path, shell=True, 
                             stdout=subprocess.PIPE)
        p.wait()
        stdout = p.stdout.read()
        
        if stdout.split(': ')[1].startswith('RAR archive data'):
            return True
        else:
            return is_mime_correct(path, RAR_MIMES)
    
    else:
        type =  MS.file(path)
        
        if type.startswith('RAR archive data'):
            return True
        else:
            return is_mime_correct(path, RAR_MIMES)


def is_mime_correct(name, mimes):
    import mimetypes
    
    if mimetypes.guess_type(name, strict=False)[0] in mimes:
        return True
    else:
        return False


def is_text_file(path):
    if os.path.splitext(path.lower())[1] == '.txt':
        return True


class Archive(object):
    
    path = None
    name = None
    type = None
    temp_dir = None
    
    files = []
    images = []
    text = []
    current = 0
    size = 0
    
    def __init__(self, path):
        self.path = path
        
        if not os.path.isfile(path):
            raise ArchiveError('<i>%s</i> does not exist.' % path)
        
        if is_zip_file(path):
            self.type = ZIP
        elif is_rar_file(path):
            self.type = RAR
        else:
            raise ArchiveError('<i>%s</i> is not a valid file type.' 
                               % path)
        
        self.name = os.path.split(path)[1]
        
        
    def make_temp_dir(self):
        self.temp_dir = tempfile.mkdtemp(prefix='colorwalk-%s-' % 
                                         os.environ['USER'])
    
    
    def remove_temp_dir(self):
        if self.temp_dir:
            shutil.rmtree(self.temp_dir)
    
    
    def extract(self):
        self.make_temp_dir()
        
        if self.type == ZIP:
            command = 'unzip -j \"%s\" -d \"%s\"' % (self.path,
                                                     self.temp_dir)
        if self.type == RAR:
            command = 'unrar e \"%s\" \"%s\"' % (self.path,
                                                 self.temp_dir)
        
        return subprocess.Popen(command, shell=True, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
