#
# soundcard_gui.py - GUI front end code for soundcard configuration
#
# Copyright 2002, 2003 Red Hat, Inc.
# Copyright 2002, 2003 Brent Fox <bfox@redhat.com>
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
#

import string
import gtk
import gobject
import sys
import os
import functions

sys.path.append('/usr/share/system-config-soundcard/')
import soundcard
import soundcardBackend

from rhpl.firstboot_gui_window import FirstbootGuiWindow

##
## I18N
## 
from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("firstboot")

class SoundWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 120
    moduleName = _("Sound Card")
    windowTitle = _("Sound Card")
    shortMessage = _("A sound card has been detected on your computer.")
    
    def __init__(self):
        #Initialize soundcard page
        self.soundcardPage = soundcard.childWindow()
        self.soundcardBox = self.soundcardPage.getSoundcardBox()
        self.soundcardBackend = soundcardBackend.soundcardBackend()
        
    def launch(self, doDebug = None):
        cards = self.soundcardBackend.probeCards()

        if cards == []:
            return None, None, None
        else:
            self.mainVBox = gtk.VBox()

            #Add icon to the top frame
            self.icon = functions.imageFromFile("multimedia.png")

            internalVBox = gtk.VBox(gtk.FALSE, 10)
            internalVBox.set_border_width(10)


            label = gtk.Label(_("Click the "
                                "\"Play test sound\" button to hear a sample sound.  You should "
                                "hear a series of three sounds.  The first sound will be in the "
                                "right channel, the second sound will be in the left channel, "
                                "and the third sound will be in the center."))
            label.set_line_wrap(gtk.TRUE)
            label.set_size_request(500, -1)
            label.set_alignment(0.0, 0.5)

            messageLabel = gtk.Label(_(self.shortMessage))
            messageLabel.set_line_wrap(gtk.TRUE)
            messageLabel.set_size_request(500, -1)
            messageLabel.set_alignment(0.0, 0.5)

            self.mainVBox.pack_start(internalVBox, gtk.FALSE)
            internalVBox.pack_start(messageLabel, gtk.FALSE)
            internalVBox.pack_start(label, gtk.FALSE)

            hbox = gtk.HBox()
            hbox.pack_start(self.soundcardBox, gtk.FALSE)
            
            internalVBox.pack_start(hbox, gtk.FALSE)

            return self.mainVBox, self.icon, self.windowTitle

    def apply(self, *args):
        return 0

childWindow = SoundWindow
