#!/usr/bin/python2.2

import sys
import os
import string
import signal
import time
import firstbootBackend

sys.path.append("/usr/share/firstboot")

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")

wm_pid = None
xserver_pid = None
doDebug = None
doReconfig = None
lowRes = None
FILENAME = "/etc/sysconfig/firstboot"

for arg in sys.argv:
    if arg == '--reconfig':
        print "starting reconfig mode"
        doReconfig = 1
    if arg == '--debug':
        print "starting with debugging options"
        doDebug = 1
    if arg == '--lowres':
        print "starting in lowres mode"
        lowRes = 1

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


def startWindowManager():    
    wm_pid = os.fork()

    if (not wm_pid):
        path = '/usr/bin/metacity'
        args = ['--display=:1']
        os.execvp(path, args)

    status = 0
    try:
        pid, status = os.waitpid (wm_pid, os.WNOHANG)
        
    except OSError, (errno, msg):
        print "in except"
        print __name__, "waitpid:", msg

    if status:
        raise RuntimeError, "Window manager failed to start"

    return wm_pid

def mergeXresources():
    path = "/etc/X11/Xresources"
    if os.access(path, os.R_OK):
	os.system("xrdb -merge %s" % path)


#Let's check to see if firstboot should be run or not
#If we're in debug mode, run anyway.  Even if the file exists
if (not doDebug):
    #Well first, is this even being run as root?
    if os.getuid() > 0 or os.geteuid() > 0:
       print "You must be root to run firstboot."
       sys.exit(0)

    #We're not in debug mode, so do some checking
    #First, look and see if /etc/sysconfig/firstboot exists
    if os.access(FILENAME, os.R_OK):
        fd = open(FILENAME, 'r')
        lines = fd.readlines()
        fd.close()

        #If /etc/sysconfig/firstboot exists, parse the file
        #If we find 'RUN_FIRSTBOOT=NO' in the file, then don't run firstboot
        for line in lines:            
            line = string.strip(line)
            if (string.find(line, "RUN_FIRSTBOOT") > -1) and line[0] != "#":
                if string.find(line, "="):
                    key, value = string.split(line, "=")
		    value = string.strip(value)
                    if value == "NO":
                        #Firstboot should not be run
			print (_("Firstboot has already been run once on this system.\n"))
			print (_("In order to run firstboot from the command line, "
                                 "run the following commands:"))
			print ("1) rm /etc/sysconfig/firstboot")
			print ("2) /usr/sbin/firstboot\n")

			print (_("In order to run firstboot during system bootup, run the "
                                 "following commands:"))
			print ("1) rm /etc/sysconfig/firstboot")
			print ("2) chkconfig --level 5 firstboot on")
			print ("3) reboot")
                        os._exit(0)
                    
    else:
        #Firstboot has never been run before, so start it up
        pass

#Let's check to see if we're in runlevel 5.  If we're in runlevel 3, let's ask the user
#if they want to run firstboot or not.

line = os.popen('/sbin/runlevel', 'r').readline()
line = string.strip(line)
tokens = string.split(line)
runlevel = int(tokens[-1])

if runlevel == 3:
    #They booted the machine in runlevel 3.  Assume that they don't want to see firstboot
    print (_("Firstboot does not run in runlevel 3."))
    firstbootBackend.writeSysconfigFile(doDebug)
    os._exit(0)
    
##-------Comment out the newt window for now.  Ran out of time for GinGin
##     import textWindow
##     from snack import *
    
##     screen = SnackScreen()

##     result = textWindow.TextWindow()(screen)

##     if result == -1:
##         #If they don't want to run firstboot, exit for good
##         screen.finish()
##         firstbootBackend.writeSysconfigFile(doDebug)
##         os._exit(0)
##     else:
##         #They want to run firstboot, so let's pass on through
##         screen.finish()

#If rhgb (graphical boot) is running, let's use it's X server
if os.access("/usr/bin/rhgb-client", os.R_OK| os.X_OK) and (os.system ("/usr/bin/rhgb-client --ping") == 0):
    os.environ["DISPLAY"] = "127.0.0.1:0"
    #However, we still need to start up metacity and merge the X resources
    wm_pid = None
    wm_pid = startWindowManager()
    mergeXresources()

#If there's no X Server running, let's start one
if not os.environ.has_key('DISPLAY'):
    
     if os.access("/etc/X11/XF86Config", os.R_OK) or os.access("/etc/X11/XF86Config-4", os.R_OK):
          #set the display environment variable
          os.environ['DISPLAY'] = ':1'

	  xserver_pid = os.fork()

          if not xserver_pid:
              path = "/etc/X11/X"
              args = [path, ':1', 'vt7', '-s', '1440', '-terminate', '-dpms', '-v', '-quiet']

              os.execvp(path, args)
	      os._exit(1)

          count = 0
          while count < 60:
            sys.stdout.write(".")
            sys.stdout.flush()
            pid = 0
            try:
                pid, status = os.waitpid (xserver_pid, os.WNOHANG)
            except OSError, (errno, msg):
                print __name__, "waitpid:", msg
            if pid:
                sys.stderr.write("X SERVER FAILED")
                raise RuntimeError, "X server failed to start"
            try:
                os.stat("/tmp/.X11-unix/X1")
                break
            except OSError:
                pass
            time.sleep(1)
            count = count + 1

     wm_pid = None
     wm_pid = startWindowManager()
     mergeXresources()

import firstbootWindow
firstbootWindow.firstbootWindow(xserver_pid, wm_pid, doReconfig, doDebug, lowRes)
