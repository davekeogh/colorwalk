import os, os.path, subprocess, mimetypes

try:
    import magic
    MAGIC = True
    MS = magic.open(magic.MAGIC_NONE)
    MS.load()
except ImportError:
    MAGIC = False


def is_text_file(path):
    if os.path.splitext(path.lower())[1] == '.txt':
        return True


def open_url(url):
    try:
        subprocess.call(['xdg-open', url])
    except OSError:
        return


def check_type(path, string, mimes):
    if not MAGIC:
        p = subprocess.Popen('file \"%s\"' % path, shell=True, 
                             stdout=subprocess.PIPE)
        p.wait()
        stdout = p.stdout.read()
        
        if stdout.split(': ')[1].startswith(string):
            return True
        else:
            return is_mime_correct(path, mimes)
    
    else:
        type =  MS.file(path)
        
        if type.startswith(string):
            return True
        else:
            return is_mime_correct(path, mimes)


def is_mime_correct(name, mimes):
    import mimetypes
    
    if mimetypes.guess_type(name, strict=False)[0] in mimes:
        return True
    else:
        return False
