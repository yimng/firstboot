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
from rhpl.xhwstate import *


from rhpl.firstboot_gui_window import FirstbootGuiWindow

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class DisplayWindow(FirstbootGuiWindow):
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
#        xconfig = generate_xconfig(hardware_state)
        vc = rhpl.videocard.VideoCardInfo()

        sys.path.append("/usr/share/system-config-display")
        import xConfigDialog
        dialog = xConfigDialog.XConfigDialog(hardware_state, xconfig, vc)        

        vbox = dialog.get_display_page()
        

##         self.xconfig = xf86config.readConfigFile()

##         align = gtk.Alignment()
##         frame = gtk.Frame("")
##         frame.set_shadow_type(gtk.SHADOW_NONE)
##         align.add(frame)
        

##         self.table = gtk.Table(3,3)

##         monitorBaseImage = gtk.Image()
##         monitorTopImage = gtk.Image()
##         monitorLeftImage = gtk.Image()
##         monitorRightImage = gtk.Image()
##         screenshotArea = gtk.DrawingArea()

##         monitorBaseImage.set_from_file("/usr/share/system-config-display/pixmaps/monitor-base.png")
##         monitorTopImage.set_from_file("/usr/share/system-config-display/pixmaps/monitor-top.png")
##         monitorLeftImage.set_from_file("/usr/share/system-config-display/pixmaps/monitor-left.png")
##         monitorRightImage.set_from_file("/usr/share/system-config-display/pixmaps/monitor-right.png")

##         self.table.attach(monitorTopImage, 0, 3, 0, 1)
##         self.table.attach(monitorLeftImage, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
##         self.table.attach(screenshotArea, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL|gtk.EXPAND)
##         self.table.attach(monitorRightImage, 2, 3, 1, 2, gtk.FILL, gtk.FILL)
##         self.table.attach(monitorBaseImage, 0, 3, 2, 3)

##         frame.add(self.table)

        #Add icon to the top frame
        self.icon = functions.imageFromPath("/usr/share/system-config-date/pixmaps/system-config-date.png")
        self.mainVBox = gtk.VBox()

        internalVBox = gtk.VBox(gtk.FALSE, 10)
        internalVBox.set_border_width(10)

        messageLabel = gtk.Label(_(self.shortMessage))
        messageLabel.set_line_wrap(gtk.TRUE)
        messageLabel.set_size_request(500, -1)
        messageLabel.set_alignment(0.0, 0.5)

#        internalVBox.pack_start(messageLabel, gtk.FALSE)
#        internalVBox.pack_start(align, gtk.TRUE)
        internalVBox.pack_start(vbox, gtk.TRUE)
        self.mainVBox.pack_start(internalVBox, gtk.TRUE)

    def launch(self, doDebug=None):
        self.doDebug = doDebug
        self.setupScreen()
        return self.mainVBox, self.icon, self.windowTitle

    def apply(self, *args):
        
        if self.doDebug:
            print "applying date changes not available in debug mode"
        else:
            pass

        return 0

    def grabFocus(self):
        pass

childWindow = DisplayWindow
