#!/usr/bin/python2.2

import sys
import os
import string
import signal
import time

x_class = None
wm_pid = None
doDebug = None
FILENAME = "/etc/sysconfig/firstboot"

for arg in sys.argv:
    if arg == '--reconfig':
        print "starting reconfig mode"
        doReconfig = 1
    if arg == '--debug':
        print "starting with debugging options"
        doDebug = 1

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


def startWindowManager():    
    wm_pid = os.fork()

    if (not wm_pid):
        path = '/usr/bin/metacity'
        args = ['--display=:1']
        os.execv(path, args)


    # give time for the window manager to start up
    time.sleep (3)
    status = 0
    try:
        pid, status = os.waitpid (wm_pid, os.WNOHANG)
        
    except OSError, (errno, msg):
        print "in except"
        print __name__, "waitpid:", msg


    if status:
        raise RuntimeError, "Window manager failed to start"

    return wm_pid

def setRootBackground():
    root_pid = os.fork()

    if (not root_pid):
        path = '/usr/bin/X11/xsetroot'
        args = [path, '-solid', 'midnightblue']
        os.execv(path, args)


#Let's check to see if firstboot should be run or not
#If we're in debug mode, run anyway.  Even if the file exists
if (not doDebug):
    #We're not in debug mode, so do some checking
    #First, look and see if /etc/sysconfig/firstboot exists
    try:
        os.stat (FILENAME)

        fd = open(FILENAME, 'r')
        lines = fd.readlines()
        fd.close()

        for line in lines:            
            print "line is", line
            line = string.strip(line)
            if (string.find(line, "VERSION") > -1) and line[0] != "#":
                if string.find(line, "="):
                    key, value = string.split(line, "=")
                    print key, value

        print "file exists"
        os._exit(0)
    except:
        #Firstboot has never been run before, so start it up
        print "file doesn't exist"


if not os.environ.has_key('DISPLAY'):
    import xserver
    
    try:        
        if os.access("/etc/X11/XF86Config", os.R_OK) or os.access("/etc/X11/XF86Config-4", os.R_OK):
            x_class = xserver.XServer()
    except:
        pass
    
    wm_pid = startWindowManager()
    setRootBackground()


import firstbootWindow
firstbootWindow.firstbootWindow(wm_pid)



