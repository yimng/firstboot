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
    
    startWindowManager()
    setRootBackground()


import firstbootWindow
firstbootWindow.firstbootWindow(wm_pid)


def startWindowManager(self):    
    wm_pid = os.fork()

    if (not wm_pid):
        path = '/usr/bin/metacity'
        args = ['--display=:1']
        os.execv(path, args)


    # give time for the window manager to start up
    time.sleep (3)
    status = 0
    try:
        pid, status = os.waitpid (self.wm_pid, os.WNOHANG)
        
    except OSError, (errno, msg):
        print "in except"
        print __name__, "waitpid:", msg


    if status:
        raise RuntimeError, "Window manager failed to start"

def setRootBackground(self):
    root_pid = os.fork()

    if (not root_pid):
        path = '/usr/bin/X11/xsetroot'
        args = [path, '-solid', 'gray45']
        os.execv(path, args)

