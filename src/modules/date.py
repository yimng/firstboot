#
# date_gui.py - GUI front end code for mouse configuration
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

sys.path.append('/usr/share/dateconfig/')
import date_gui
import dateBackend

from rhpl.firstboot_gui_window import FirstbootGuiWindow

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class TimeWindow(FirstbootGuiWindow):
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 90
    moduleName = _("Date & Time")
    windowTitle = _("Date & Time Configuration")
    htmlTag = "time"
    shortMessage = _("Please set the date and time for the system.")

    def getNext(self):
        pass
    
    def destroy(self, args):
        gtk.mainquit()
    
    def setupScreen(self):
        self.datePage = date_gui.datePage()
        self.datePageVBox = self.datePage.getVBox()
        #Initialize date backend
        self.dateBackend = dateBackend.dateBackend()        

        #Add icon to the top frame
        self.icon = functions.imageFromFile("dateconfig-icon.png")

        self.myVbox = self.datePageVBox


    def launch(self, doDebug=None):
        self.doDebug = doDebug
        if doDebug:
            print "in mouse launch"
        self.setupScreen()
        return FirstbootGuiWindow.launch(self)

    def apply(self, *args):
        if self.doDebug:
            print "applying date changes not available in debug mode"
        else:
            sysDate = self.datePage.getDate()
            sysTime = self.datePage.getTime()
            ntpEnabled = self.datePage.getNtpEnabled()

            if ntpEnabled == gtk.FALSE:
                #We're not using ntp, so stop the service
                self.dateBackend.stopNtpService()
                #set the time on the system according to what the user set it to
                self.dateBackend.writeDateConfig(sysDate, sysTime)
                self.dateBackend.syncHardwareClock()

            elif ntpEnabled == gtk.TRUE:
                sysTimeServer = self.datePage.getTimeServer()
                self.dateBackend.writeNtpConfig(sysTimeServer)
                self.dateBackend.startNtpService()
                self.dateBackend.syncHardwareClock()

        return 1


    def stand_alone(self, doDebug = None):
        self.doDebug = doDebug
        self.setupScreen()
        return FirstbootGuiWindow.stand_alone(self, TimeWindow.windowTitle)

childWindow = TimeWindow
