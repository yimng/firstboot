#
# xserver.py - initial xserver startup for GUI mode.
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

serverPath = ""

#
# to start X server using existing XF86Config file (reconfig mode use only)
#
def start_existing_X():

    os.environ['DISPLAY'] = ':1'

    server = os.fork()
    serverPath = "/etc/X11/X"

    # override fontpath because xfs is not running yet!
    if (not server):
        print "Starting X using existing XF86Config"
	args = [serverPath, ':1', 'vt7', '-s', '1440', '-terminate', '-dpms',
                '-v']
	args.append("-fp")
                    
	os.execv(serverPath, args)

    # give time for the server to fail (if it is going to fail...)
    # FIXME: Should find out if X server is already running
    # otherwise with NFS installs the X server may be still being
    # fetched from the network while we already continue to run
    time.sleep (4)
    status = 0
    try:
        pid, status = os.waitpid (server, os.WNOHANG)
    except OSError, (errno, msg):
        print __name__, "waitpid:", msg

    if status:
        raise RuntimeError, "X server failed to start"

    # startX() function above does a double-fork here, do we need to in
    # reconfig mode?
    
    return (None, None)
