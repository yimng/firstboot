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
import gtk

from module import *
from rhpl.translate import _, N_

class moduleClass(Module):
    def __init__(self):
        Module.__init__(self)
        self.priority = 2
        self.sidebarTitle = "Second"
        self.title = "Second Module"

    def apply(self, interface, testing=False):
        pass

    def createScreen(self):
        self.vbox = gtk.VBox()
        label = gtk.Label(_("This is some meaningless text from the second module."))
        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)

        self.vbox.pack_start(label, False, True)

    def initializeUI(self):
        pass
