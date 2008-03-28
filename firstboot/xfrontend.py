#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import logging
import os
import rhpl.keyboard as keyboard

class XFrontEnd:
    def __init__(self):
        self._wm_pid = None
        self._xserver_pid = None

    def _mergeXresources(self):
        path = "/etc/X11/Xresources"
        if os.access(path, os.R_OK):
            os.system("xrdb -merge %s" % path)

    # Attempt to start up the window manager.  Check the value of self.wm_pid
    # afterwards to see if this succeeded.
    def _startWindowManager(self):
        self._wm_pid = os.fork()

        if not self._wm_pid:
            path = "/usr/bin/metacity"
            args = [path, "--display", os.environ["DISPLAY"]]
            os.execvp(path, args)

        status = 0
        try:
            (pid, status) = os.waitpid (self._wm_pid, os.WNOHANG)
        except OSError, (errno, msg):
            logging.error ("starting window manager failed: %s" % msg)

        if status:
            raise RuntimeError, "Window manager failed to start."

    # Initializes the UI for firstboot by starting up an X server and
    # window manager, but returns control to the caller to proceed.
    def start(self):
        import rhpxl.xserver
        import rhpxl.xhwstate as xhwstate
        import rhpxl.monitor

        xserver = rhpxl.xserver.XServer()
        xserver.probeHW(skipMouseProbe=0)
        xserver.setHWState()
        xserver.keyboard = keyboard.Keyboard()
        xserver.resolution = "800x600"

        xhwstate.get_valid_resolution(xserver)

        try:
            xserver.generateConfig()
            xserver.addExtraScreen("Firstboot")
            xserver.serverflags.extend(["-screen", "Firstboot"])
            self._xserver_pid = xserver.startX()
        except RuntimeError:
            logging.error("X server failed to start")
            raise RuntimeError, "X server failed to start"

        # Init GTK to connect to the X server, then write a token on a pipe to
        # tell our parent process that we're ready to start metacity.
        (rd, wr) = os.pipe()
        pid = os.fork()
        if not pid:
            import gtk
            os.write(wr, "#")

            # Block until the X server is killed.
            gtk.main()
            os._exit(0)

        # Block on read of token
        os.read(rd, 1)
        os.close(rd)
        os.close(wr)

        self._wm_pid = self._startWindowManager()
        self._mergeXresources()

    def stop(self):
        if self._wm_pid:
            os.kill(self._wm_pid, 15)

        if self._xserver_pid:
            os.kill(self._xserver_pid, 15)
