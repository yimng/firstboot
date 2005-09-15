#!/usr/bin/python2
#
# firstboot.py - configuration and convenience functions in a single class
#
# Copyright (C) 2002, 2003, 2005 Red Hat, Inc.
# Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>
# Copyright (C) 2005 Chris Lumens <clumens@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os
import string
import sys
import rhpl.keyboard as keyboard
import rhpl
import snack
import firstbootBackend

FILENAME = "/etc/sysconfig/firstboot"
DISPLAY_FILE = "/etc/rhgb/temp/display"

class Firstboot:
    def __init__(self):
        self.wm_pid = None
        self.xserver_pid = None
        self.doDebug = False
        self.doReconfig = False
        self.lowRes = False
        self.rhgb = False
        self.autoscreenshot = False
        self.forcegui = False

    #Let's check to see if firstboot should be run or not
    #If we're in debug mode, run anyway.  Even if the file exists
    def mayRun(self):
        if not self.doDebug:
            #Well first, is this even being run as root?
            if os.getuid() > 0 or os.geteuid() > 0:
               print "You must be root to run firstboot."
               return False

            #We're not in debug mode, so do some checking
            #First, look and see if /etc/sysconfig/firstboot exists
            if os.access(FILENAME, os.R_OK):
                fd = open(FILENAME, 'r')
                lines = fd.readlines()
                fd.close()

                #If /etc/sysconfig/firstboot exists, parse the file
                #If we find 'RUN_FIRSTBOOT=NO' in the file, then don't run
                for line in lines:            
                    line = string.strip(line)
                    if string.find(line, "RUN_FIRSTBOOT") > -1 and line[0] != "#":
                        if string.find(line, "="):
                            key, value = string.split(line, "=")
                            value = string.strip(value)
                            if value == "NO":
                                #Firstboot should not be run
                                firstbootBackend.chkconfigOff()
                                return False
                            
            else:
                #Firstboot has never been run before, so start it up
                return True

    def mergeXresources(self):
        path = "/etc/X11/Xresources"
        if os.access(path, os.R_OK):
           os.system("xrdb -merge %s" % path)

    # Initializes the UI for firstboot by starting up an X server and
    # window manager, but returns control to the caller to proceed.
    def startGraphicalUI(self):
        import rhpl.xserver as xserver
        import rhpl.xhwstate as xhwstate

        kbd = keyboard.Keyboard()
        (videohw, monitorhw, mousehw) = xserver.probeHW(skipDDCProbe=0,
                                                        skipMouseProbe=0)

        if self.lowRes:
            runres = "640x480"
        else:
            runres = "800x600"

        if rhpl.getPPCMachine() == "PMac":
            runres = xhwstate.get_valid_resolution(videohw, monitorhw, runres,
                                                   onPMac=True)
        else:
            runres = xhwstate.get_valid_resolution(videohw, monitorhw, runres)

        xsetup_failed = False
        try:
            xcfg = xserver.startX(runres, videohw, monitorhw, mousehw, kbd)
        except RuntimeError:
            xsetup_failed = True

        if xsetup_failed:
            sys.stderr.write("X SERVER FAILED TO START")
            raise RuntimeError, "X server failed to start"

        # Init GTK to connect to the X server, then write a token on a pipe to
        # tell our parent process that we're ready to start metacity.
        (rd, wr) = os.pipe()
        self.xserver_pid = os.fork()
        if not self.xserver_pid:
            import gtk
            os.write(wr, "#")

        # Block on read of token
        os.read(rd, 1)
        os.close(rd)
        os.close(wr)

        self.wm_pid = self.startWindowManager()
        self.mergeXresources()
        self.setKeyboard()

    # Initializes the UI for firstboot via rhgb, but returns control to
    # the caller to proceed.
    def startRhgbUI(self):
        try:
            os.environ["DISPLAY"] = open(DISPLAY_FILE, "r").read()
        except:
            os.environ["DISPLAY"] = "127.0.0.1:0"

        #However, we still need to start up metacity and merge the X resources
        self.wm_pid = self.startWindowManager()
        self.mergeXresources()
        self.rhgb = True
        self.setKeyboard()

    # Sets up the text UI and assumes control.  The caller will never be
    # returned to and firstboot will exit from within here.
    def runTextUI(self):
        import textWindow
        
        screen = snack.SnackScreen()
        result = 0

        while result != -1:
           #Keep running the program until either the timer has expired or the user pressed Exit
            screen = snack.SnackScreen()
            result = textWindow.TextWindow()(screen)

        if result == -1:
            #They're done with firstboot.  Exit for good.
            screen.finish()
            firstbootBackend.writeSysconfigFile(self.doDebug)
            os._exit(0)

    def setKeyboard(self):
        kb = keyboard.Keyboard()
        kb.read()
        kb.activate()

    # Attempt to start up the window manager.  Check the value of self.wm_pid
    # afterwards to see if this succeeded.
    def startWindowManager(self):    
        self.wm_pid = os.fork()

        if not self.wm_pid:
            path = '/usr/bin/metacity'
            args = ['--display=:1']
            os.execvp(path, args)

        status = 0
        try:
            pid, status = os.waitpid (self.wm_pid, os.WNOHANG)

        except OSError, (errno, msg):
            print "in except"
            print __name__, "waitpid:", msg

        if status:
            raise RuntimeError, "Window manager failed to start"
