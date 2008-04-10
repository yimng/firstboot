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

from firstboot.config import *
from firstboot.constants import *
from firstboot.functions import *
from firstboot.module import *

from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")

class moduleClass(Module):
    def __init__(self):
        Module.__init__(self)
        self.priority = 2
        self.sidebarTitle = N_("License Information")
        self.title = N_("License Information")
        self.icon = "workstation.png"

    def apply(self, interface, testing=False):
        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=5)

        textBuffer = gtk.TextBuffer()
        textView = gtk.TextView()
        textView.set_editable(False)
        textSW = gtk.ScrolledWindow()
        textSW.set_shadow_type(gtk.SHADOW_IN)
        textSW.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textSW.add(textView)

        textBuffer.set_text(_("""Thank you for installing Fedora.  Fedora is a \
compilation of software packages, each under its own license.  The \
compilation is made available under the GNU General Public License version \
2.  There are no restrictions on using, copying, or modifying this code.  \
However, there are restrictions and obligations that apply to the \
redistribution of the code, either in its original or a modified form.  \
Among other things, those restrictions/obligations pertain to the \
licensing of the redistribution, trademark rights, and export control.\n\n\
If you would like to understand what those restrictions are, please \
visit http://fedoraproject.org/wiki/Legal/Licenses/LicenseAgreement."""))

        label = gtk.Label(_("Understood, please proceed."))
        label.set_alignment(0.0, 0.1)

        textView.set_buffer(textBuffer)
        textView.set_wrap_mode(gtk.WRAP_WORD)

        self.vbox.pack_start(textSW)
        self.vbox.pack_start(label)

    def initializeUI(self):
        pass
