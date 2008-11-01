import os, os.path, subprocess


def is_text_file(path):
    if os.path.splitext(path.lower())[1] == '.txt':
        return True


def open_url(url):
    try:
        subprocess.call(['xdg-open', url])
    except OSError:
        return
