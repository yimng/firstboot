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

import rhpl.Conf
import os
import snack
import firstbootBackend

FILENAME = "/etc/sysconfig/firstboot"

def start_process(path, args = None):
    if args == None:
        args = [path]
    else:
        args = [path, args]

    child = os.fork()

    if not child:
        os.execvp(path, args)
        os._exit(1)
            
    return child

class Firstboot:
    def __init__(self):
        self.doDebug = False
        self.doReconfig = False
        self.wm_pid = None
        self.xserver_pid = None
        self.lowRes = False
        self.rhgb = False
        self.autoscreenshot = False
        self.forcegui = False

    #Let's check to see if firstboot should be run or not
    #If we're in debug mode, run anyway even if the file exists.
    def mayRun(self):
        if not self.doDebug and not self.doReconfig:
            #Well first, is this even being run as root?
            if os.getuid() > 0 or os.geteuid() > 0:
               print "You must be root to run firstboot."
               return False

            #We're not in debug mode, so do some checking
            #First, look and see if /etc/sysconfig/firstboot exists
            if os.access(FILENAME, os.R_OK):
                conf = rhpl.Conf.ConfShellVar(FILENAME)

                if conf.has_key("RUN_FIRSTBOOT"):
                    if conf["RUN_FIRSTBOOT"].upper() == "NO":
                        # Firstboot should not be run
                        return False

        # If we're in debug mode, or the file doesn't exist, or RUN_FIRSTBOOT
        # isn't in it, or RUN_FIRSTBOOT isn't NO, run.
        return True

    # Sets up the text UI and assumes control.  The caller will never be
    # returned to and firstboot will exit from within here.
    def runTextUI(self):
        import textWindow
        
        screen = snack.SnackScreen()
        result = 0

        while result != -1:
            # Keep running the program until either the timer has expired or
            # the user pressed Exit
            screen = snack.SnackScreen()
            result = textWindow.TextWindow()(screen)

        if result == -1:
            # They're done with firstboot.  Exit for good.
            screen.finish()
            firstbootBackend.writeSysconfigFile(self.doDebug)
            os._exit(0)
