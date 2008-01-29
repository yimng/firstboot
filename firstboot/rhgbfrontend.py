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
from firstboot.xfrontend import XFrontEnd

class RHGBFrontEnd(XFrontEnd):
    def __init__(self):
        XFrontEnd.__init__(self)

    def start(self):
        # Initializes the UI for firstboot via rhgb, but returns control
        # to the called to proceed.
        try:
            os.environ["DISPLAY"] = open("/etc/rhgb/temp/display", "r").read()
        except:
            logging.info("Couldn't open /etc/rhgb/temp/display, using default")
            os.environ["DISPLAY"] = "127.0.0.1:0"

        # We still need to start up metacity.
        self._wm_pid = self._startWindowManager()
        self._mergeXresources()

    def stop(self):
        if self._wm_pid:
            os.kill(self._wm_pid, 15)
