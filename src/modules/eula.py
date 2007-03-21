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

from gtk import *
import string
import gtk
import gobject
import sys
import functions
import os

##
## I18N
## 
from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("firstboot")

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 15
    moduleName = (_("License Information"))

    def launch(self, doDebug = None):
        self.doDebug = doDebug
        if self.doDebug:
            print "initializing eula module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        msg = (_("License Information"))

        title_pix = functions.imageFromFile("workstation.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)
        internalVBox.set_spacing(5)

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
visit http://fedoraproject.org/wiki/Legal/Licenses/EULA."""))

        label = gtk.Label(_("Understood, please proceed."))
        label.set_alignment(0.0, 0.1)

        textView.set_buffer(textBuffer)
        textView.set_wrap_mode(gtk.WRAP_WORD)

        internalVBox.pack_start(textSW)
        internalVBox.pack_start(label)

        self.vbox.pack_start(internalVBox, True, 5)
        return self.vbox, title_pix, msg

    def apply(self, notebook):
        return 0
