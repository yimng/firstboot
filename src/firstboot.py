#!/usr/bin/python2
##
## firstboot.py - kickoff script for firstboot
##
## Copyright (C) 2002, 2003 Red Hat, Inc.
## Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

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
rhgb = None
autoscreenshot = None
forcegui = None
FILENAME = "/etc/sysconfig/firstboot"
DISPLAY_FILE = "/etc/rhgb/temp/display"

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
    if arg == '--autoscreenshot':
        autoscreenshot = 1
    if arg == '--forcegui':
        forcegui = 1

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
                        firstbootBackend.chkconfigOff()
                        os._exit(0)
                    
    else:
        #Firstboot has never been run before, so start it up
        pass

#Let's check to see if we're in runlevel 5.  If we're in runlevel 3, let's call
#textWindow for the TUI

line = os.popen('/sbin/runlevel', 'r').readline()
line = string.strip(line)
tokens = string.split(line)
runlevel = int(tokens[-1])

if runlevel == 3 and forcegui == None:
    import textWindow
    from snack import *
    
    screen = SnackScreen()
    result = 0

    while result != -1:
        #Keep running the program until either the timer has expired or the user pressed Exit
        screen = SnackScreen()
        result = textWindow.TextWindow()(screen)

    if result == -1:
        #They're done with firstboot.  Exit for good
        screen.finish()
        firstbootBackend.writeSysconfigFile(doDebug)
        os._exit(0)

#If rhgb (graphical boot) is running, let's use it's X server
if os.access("/usr/bin/rhgb-client", os.R_OK| os.X_OK) and (os.system ("/usr/bin/rhgb-client --ping") == 0):
    try:
        os.environ["DISPLAY"] = open("DISPLAY_FILE", "r").read()
    except:
        os.environ["DISPLAY"] = "127.0.0.1:0"
    #However, we still need to start up metacity and merge the X resources
    wm_pid = None
    wm_pid = startWindowManager()
    mergeXresources()
    rhgb = 1

#If there's no X Server running, let's start one
if not os.environ.has_key('DISPLAY'):
    
     if os.access("/etc/X11/xorg.conf", os.R_OK) or os.access("/etc/X11/XF86Config", os.R_OK):
          #set the display environment variable
          os.environ['DISPLAY'] = ':1'

	  xserver_pid = os.fork()

          if not xserver_pid:
              path = "/etc/X11/X"
              args = [path, ':1', '-s', '1440', '-terminate', '-dpms', '-v', '-quiet']

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
firstbootWindow.firstbootWindow(xserver_pid, wm_pid, doReconfig, doDebug, lowRes, rhgb, autoscreenshot)
