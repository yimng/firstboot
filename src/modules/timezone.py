#
# timezone.py - GUI front end code for timezone configuration
#
# Copyright 2002, 2003 Red Hat, Inc.
# Copyright 2002, 2003 Brent Fox <bfox@redhat.com>
# Copyright 2004 Nils Philippsen <nphilipp@redhat.com>
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
import sys
import os
import signal
import time
import functions

sys.path.append('/usr/share/system-config-date/')
import mainWindow

from rhpl.firstboot_gui_window import FirstbootGuiWindow

##
## I18N
## 
from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("firstboot")

class TimeWindow(FirstbootGuiWindow):
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 89
    moduleName = _("Timezone")
    windowTitle = moduleName
    moduleClass = "reconfig"
    htmlTag = "timezone"
    shortMessage = _("Please set the timezone for the system.")

    def getNext(self):
        pass

    def setupScreen(self):
        self.timezoneWindow = mainWindow.mainWindow (firstboot = True, showPages = ["timezone"])

        self.timezoneWidget = self.timezoneWindow.firstboot_widget ()

        #Add icon to the top frame
        self.icon = functions.imageFromPath("/usr/share/system-config-date/pixmaps/system-config-date.png")
        self.mainVBox = gtk.VBox()

        internalVBox = gtk.VBox(gtk.FALSE, 10)
        internalVBox.set_border_width(10)

        messageLabel = gtk.Label(_(self.shortMessage))
        messageLabel.set_line_wrap(gtk.TRUE)
        messageLabel.set_size_request(500, -1)
        messageLabel.set_alignment(0.0, 0.5)

        internalVBox.pack_start(messageLabel, gtk.FALSE)
        internalVBox.pack_start(self.timezoneWidget, gtk.TRUE)
        self.mainVBox.pack_start(internalVBox, gtk.TRUE)

    def launch(self, doDebug=None):
        self.doDebug = doDebug
        self.setupScreen()
        return self.mainVBox, self.icon, self.windowTitle

    def response_cb (self, dialog, response_id, pid):
        if response_id == gtk.RESPONSE_CANCEL:
            os.kill (pid, signal.SIGINT)
        dialog.hide ()

    def apply(self, *args):
        if self.doDebug:
            print "applying timezone changes not available in debug mode"
        else:
            return self.timezoneWindow.firstboot_apply ()

        return 0

    def grabFocus(self):
        pass

childWindow = TimeWindow
