#
# soundcard_gui.py - GUI front end code for soundcard configuration
#
# Brent Fox <bfox@redhat.com>
#
# Copyright 2002 Red Hat, Inc.
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

#!/usr/bin/python2.2

import string
import gtk
import gobject
import sys
import os
import functions

sys.path.append('/usr/share/redhat-config-soundcard/')
import soundcard
import soundcardBackend

from rhpl.firstboot_gui_window import FirstbootGuiWindow

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class SoundWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 110
    moduleName = _("Sound Card")
    windowTitle = _("Sound Card Configuration")
    shortMessage = _("A sound card has been detected on your computer.")
    
    def __init__(self):
        #Initialize soundcard page
        self.soundcardPage = soundcard.childWindow()
        self.notebook = self.soundcardPage.getNotebook()
        self.notebook.set_border_width(5)

        self.soundcardBackend = soundcardBackend.soundcardBackend()
        
    def launch(self, doDebug = None):
        cards = self.soundcardBackend.probeCards()

        if not cards:
            return None, None
        else:
            self.mainVBox = gtk.VBox()

            title = gtk.Label("")
            title.set_alignment(0.4, 0.5)
            title.set_markup("<span size='x-large'>%s</span>" % self.windowTitle)            
            title.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

            titleBox = gtk.HBox()

            #Add icon to the top frame
            self.icon = functions.imageFromFile("multimedia.png")

            if self.icon:
                titleBox.pack_start(self.icon, gtk.FALSE, gtk.TRUE, 5)

            titleBox.pack_start(title)

            eventBox = gtk.EventBox()
            eventBox.add(titleBox)
            eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
            self.mainVBox.pack_start(eventBox, gtk.FALSE)

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

            messageLabel = gtk.Label(self.shortMessage)
            messageLabel.set_line_wrap(gtk.TRUE)
            messageLabel.set_size_request(500, -1)
            messageLabel.set_alignment(0.0, 0.5)

            self.mainVBox.pack_start(internalVBox, gtk.FALSE)
            internalVBox.pack_start(messageLabel, gtk.FALSE)
            internalVBox.pack_start(label, gtk.FALSE)
            self.notebook.set_show_border(gtk.FALSE)

            hbox = gtk.HBox()
            hbox.pack_start(self.notebook, gtk.FALSE)
            
            internalVBox.pack_start(hbox, gtk.FALSE)

            return self.mainVBox, eventBox

    def apply(self, *args):
        return 1

childWindow = SoundWindow
