#
# xserver.py - initial xserver startup for firstboot
#
# Matt Wilson <msw@redhat.com>
# Brent Fox <bfox@redhat.com>
#
# Copyright 2001 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import os
import string
import time

class XServer:
    def __init__(self):
        self.xserver_pid = None
        self.start_existing_X()

    def start_existing_X(self):
        print 'in start_existing_X'
        os.environ['DISPLAY'] = ':1'

        self.xserver_pid = os.fork()
        
        serverPath = "/etc/X11/X"

        # override fontpath because xfs is not running yet!
        if (not self.xserver_pid):
            print "Starting X using existing XF86Config"
            args = [serverPath, ':1', 'vt7', '-s', '1440', '-terminate', '-dpms', '-v', '-quiet']
                    
            os.execv(serverPath, args)

        # give time for the server to fail (if it is going to fail...)
        time.sleep (5)
        status = 0
        print "about to try"
        try:
            pid, status = os.waitpid (self.xserver_pid, os.WNOHANG)

        except OSError, (errno, msg):
            print "in except"
            print __name__, "waitpid:", msg

        if status:
            raise RuntimeError, "X server failed to start"

