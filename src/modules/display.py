#
# display.py - GUI front end code for firstboot screen resolution
#
# Copyright 2003 Red Hat, Inc.
# Copyright 2003 Brent Fox <bfox@redhat.com>
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
import xf86config
from rhpxl.xhwstate import *
import rhpxl.videocard
from firstboot_module_window import FirstbootModuleWindow

##
## I18N
## 
from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("system-config-display")

class DisplayWindow(FirstbootModuleWindow):
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 105
    moduleName = _("Display")
    windowTitle = moduleName
    htmlTag = "display"
    shortMessage = _("Please select the resolution and color depth that you wish to use")

    def getNext(self):
        pass
    
    def setupScreen(self):
        (xconfig, xconfigpath) = xf86config.readConfigFile()
        
        hardware_state = XF86HardwareState(xconfig)
        vc = rhpxl.videocard.VideoCardInfo()

        sys.path.append("/usr/share/system-config-display")
        import xConfigDialog
        self.displayClass = xConfigDialog.XConfigDialog(hardware_state, xconfig, vc)        

        vbox = self.displayClass.get_display_page()
        
        #Add icon to the top frame
        self.icon = functions.imageFromPath("/usr/share/system-config-display/pixmaps/system-config-display.png")
        self.mainVBox = gtk.VBox()

        internalVBox = gtk.VBox(False, 10)
        internalVBox.set_border_width(10)

        messageLabel = gtk.Label(_(self.shortMessage))
        messageLabel.set_line_wrap(True)
        messageLabel.set_size_request(500, -1)
        messageLabel.set_alignment(0.0, 0.5)

        internalVBox.pack_start(vbox, True)
        self.mainVBox.pack_start(internalVBox, True)

    def launch(self, doDebug=None):
        self.doDebug = doDebug
        self.setupScreen()
        return self.mainVBox, self.icon, self.windowTitle

    def apply(self, *args):
        if self.doDebug:
            print "applying monitor changes not available in debug mode"
        else:
            self.displayClass.firstboot_apply()

        return 0

    def grabFocus(self):
        pass

childWindow = DisplayWindow
