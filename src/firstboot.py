#!/usr/bin/python2.2

import sys, os
import signal

x_class = None

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


if not os.environ.has_key('DISPLAY'):
    import xserver
    try:
        if os.access("/etc/X11/XF86Config", os.R_OK) or os.access("/etc/X11/XF86Config-4", os.R_OK):
            x_class = xserver.XServer()
    except:
         pass

    wm = os.fork()

    if (not wm):
        path = '/usr/bin/metacity'
        args = ['--display=:1']
        os.execv(path, args)

import firstbootWindow
firstbootWindow.firstbootWindow()
