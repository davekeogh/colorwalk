#!/usr/bin/env python

import os
import hotshot, hotshot.stats
from main import main

profile = hotshot.Profile('profile')
profile.runcall(main, ['python' ,'/home/david/Projects/colorwalk/test.cbz'])
profile.close()

stats = hotshot.stats.load('profile')
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

os.remove('profile')
