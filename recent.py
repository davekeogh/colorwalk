import os, os.path

from preferences import PREFS_DIR


class RecentFiles(object):
    
    file = os.path.join(PREFS_DIR, 'recent')
    files = []
    
    def __init__(self):
        if os.path.isfile(self.file):
            fb = open(self.file)
            self.files = fb.read().strip('\n').split('\n')
            fb.close()
    
    
    def add(self, file):
        if len(self.files) <= 9:
            self.files.append(file)
        else:
            self.files = self.files[1:]
            self.files.append(file)
    
    
    def read(self):
        return self.files
    
    
    def save(self):
        if len(self.files):
            fb = open(self.file, 'w')
            
            for file in self.files:
                fb.write('%s\n' % file)
            
            fb.close()
    
    
    def prune(self):
        for file in self.files:
            if not os.path.isfile(file):
                self.files.remove(file)
    
    
    def __del__(self):
        self.save()

