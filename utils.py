import subprocess


def open_url(url):
    try:
        subprocess.call(['xdg-open', url])
    except OSError:
        return
