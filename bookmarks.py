import os, os.path

from preferences import PREFS_DIR
from error import BookmarkError


class Bookmarks(dict):
    
    file = os.path.join(PREFS_DIR, 'bookmarks')
    
    def __init__(self):
        if os.path.isfile(self.file):
            fb = open(self.file)
            lines = ()
            lines = fb.read().strip('\n').split('\n')
            fb.close()
            
            for line in lines:
                (key, value) = line.split('\t')
                self[key] = value
    
    
    def add(self, file, page):
        if self.has_key(file):
            raise BookmarkError(os.path.split(file)[1], self[file], page)
        else:
            self[file] = page
    
    
    def prune(self):
        for key in self:
            if not os.path.isfile(key):
                self.remove(key)
    
    
    def remove(self, file):
        self.__delitem__(file)
    
    
    def save(self):
        if len(self):
            fb = open(self.file, 'w')
            
            for key in self:
                fb.write('%s\t%s\n' % (key, self[key]))
            
            fb.close()
    
    
    def __del__(self):
        self.save()

