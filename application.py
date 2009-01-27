
class Application(object):
    
    win = None
    worker = None
    archive = None
    prefs = None
    recent = None
    bookmarks = None
    
    open_dir = None
    log = ['\n']
    scale = 0
    
    current_pb = None
    next_pb = None
    previous_pb = None
    
    
    def reset(self):
        self.current_pb = None
        self.next_pb = None
        self.previous_pb = None

