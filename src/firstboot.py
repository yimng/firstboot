#!/usr/bin/python2.2

import sys
import os
import string
import signal
import time

sys.path.append("/usr/share/firstboot")

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

wm_pid = None
doDebug = None
doReconfig = None
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

        #If /etc/sysconfig/firstboot exists, don't run again
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

    #Let's see if /etc/reconfigSys exists.  If it does, we need to enter reconfig mode
    try:	
        os.stat("/etc/reconfigSys")
        #It exists, so set reconfig mode flag to 1
        doReconfig = 1
    except:
        #It doesn't exist, so set reconfig mode flag to 0
        doReconfig = 0

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

          status = 0
          try:
               pid, status = os.waitpid (xserver_pid, os.WNOHANG)
          except OSError, (errno, msg):
               print __name__, "waitpid:", msg

          if status:
               raise RuntimeError, "X server failed to start"
	    

     wm_pid = None
     wm_pid = startWindowManager()
     mergeXresources()

import firstbootWindow
firstbootWindow.firstbootWindow(wm_pid, doReconfig, doDebug)
