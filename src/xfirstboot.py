#!/usr/bin/python2
#
# xfirstboot.py - X-related firstboot functions
#
# Copyright (C) 2002, 2003, 2005 Red Hat, Inc.
# Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>
# Copyright (C) 2005, 2006 Chris Lumens <clumens@redhat.com>
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
import sys
import rhpl.keyboard as keyboard
import rhpl
import firstbootBackend

sys.path.append("/usr/share/firstboot")
from firstboot import Firstboot

DISPLAY_FILE = "/etc/rhgb/temp/display"

class XFirstboot (Firstboot):
    def mergeXresources(self):
        path = "/etc/X11/Xresources"
        if os.access(path, os.R_OK):
           os.system("xrdb -merge %s" % path)

    # Initializes the UI for firstboot by starting up an X server and
    # window manager, but returns control to the caller to proceed.
    def startGraphicalUI(self):
        import rhpxl.xserver
        import rhpxl.xhwstate as xhwstate
        import rhpxl.monitor

        xserver = rhpxl.xserver.XServer()
        xserver.probeHW(skipMouseProbe=0)
        xserver.setHWState()
        xserver.keyboard = keyboard.Keyboard()

        if self.lowRes:
            xserver.resolution = "640x480"
        else:
            xserver.resolution = "800x600"

        xhwstate.get_valid_resolution(xserver)

        try:
            xserver.generateConfig()
            xserver.addExtraScreen("Firstboot")
            xserver.serverflags.extend(["-screen", "Firstboot"])
            self.xserver_pid = xserver.startX()
        except RuntimeError:
            sys.stderr.write("X SERVER FAILED TO START")
            raise RuntimeError, "X server failed to start"

        # Init GTK to connect to the X server, then write a token on a pipe to
        # tell our parent process that we're ready to start metacity.
        (rd, wr) = os.pipe()
        pid = os.fork()
        if not pid:
            import gtk
            os.write(wr, "#")
            return

        # Block on read of token
        os.read(rd, 1)
        os.close(rd)
        os.close(wr)

        self.wm_pid = self.startWindowManager()
        self.mergeXresources()

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

    # Attempt to start up the window manager.  Check the value of self.wm_pid
    # afterwards to see if this succeeded.
    def startWindowManager(self):    
        self.wm_pid = os.fork()

        if not self.wm_pid:
            path = '/usr/bin/metacity'
            args = [path, '--display=%s' % os.environ["DISPLAY"]]
            os.execvp(path, args)

        status = 0
        try:
            pid, status = os.waitpid (self.wm_pid, os.WNOHANG)
        except OSError, (errno, msg):
            print "in except"
            print __name__, "waitpid:", msg

        if status:
            raise RuntimeError, "Window manager failed to start"
