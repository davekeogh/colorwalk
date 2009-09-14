#!/usr/bin/python

from distutils.core import setup

def make_readme():
    '''Makes a plaintext README file from the markdown version.'''
    pass


setup(
    version = '0.1.0',
    name = 'colorwalk',
    
    description = 'A GTK+ comicbook reader written in Python',
    license = 'GNU GPL version 3',
    url = 'http://github.com/davekeogh/colorwalk/tree/master',
    author = 'David Keogh',
    author_email = 'davekeogh@shaw.ca',
    long_description = 'Color Walk is a really simple comic book reading application. The main design goals were to make it fast and easy to use. It\'s written in Python and uses the GTK+ bindings to draw the user interface.',
    
    classifiers = [
        'Intended Audience :: End Users/Desktop',
    ],
    
    packages = [
        'ColorWalk',
    ],
    
    scripts = [
        'colorwalk',
    ],
    
    data_files = [
        ('share/applications', ['colorwalk.desktop']),
        ('share/colorwalk', ['colorwalk.ui']),
    ],
)
