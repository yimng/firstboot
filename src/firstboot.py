#!/usr/bin/python

import sys, os
import signal

xcfg = None

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


if not os.environ.has_key('DISPLAY'):
    import xserver
    try:
        if os.access("/etc/X11/XF86Config", os.R_OK) or os.access("/etc/X11/XF86Config-4", os.R_OK):
         xcfg = xserver.start_existing_X ()
    except:
         pass

    wm = os.fork()

    if (not wm):
        path = '/usr/bin/sawfish'
        args = ['--display=:1']
        os.execv(path, args)

#from splashscreen import splashScreenShow
#splashScreenShow()

#from window import showWindow
#showWindow()

import firstbootWindow
firstbootWindow.firstbootWindow()
