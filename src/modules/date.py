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
import signal
import time
import functions

sys.path.append('/usr/share/redhat-config-date/')
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
    moduleName = _("Date and Time")
    windowTitle = _("Date and Time Configuration")
    htmlTag = "time"
    shortMessage = _("Please set the date and time for the system.")

    def getNext(self):
        pass
    
    def setupScreen(self):
        #Initialize date backend
        self.dateBackend = dateBackend.dateBackend()

        #Initialize datePage and pass dateBackend into it
        self.datePage = date_gui.datePage(self.dateBackend)
        self.datePageVBox = self.datePage.getVBox()

        #Add icon to the top frame
        self.icon = functions.imageFromPath("/usr/share/redhat-config-date/pixmaps/redhat-config-date.png")

        self.myVbox = self.datePageVBox


    def launch(self, doDebug=None):
        self.doDebug = doDebug
        self.setupScreen()
        return FirstbootGuiWindow.launch(self)

    def response_cb (self, dialog, response_id, pid):
        if response_id == gtk.RESPONSE_CANCEL:
            os.kill (pid, signal.SIGINT)
        dialog.hide ()

    def apply(self, *args):
        self.failedFlag = None
        
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
                self.dateBackend.chkconfigOff()

            elif ntpEnabled == gtk.TRUE:
                sysTimeServer = self.datePage.getTimeServer()

                if sysTimeServer == "":
                    #They want ntp but have not set a server
                    text = (_("Please enter a time server."))
                    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                    dlg.set_title(_("Error"))
                    dlg.set_default_size(100, 100)
                    dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
                    dlg.set_border_width(2)
                    dlg.set_modal(gtk.TRUE)
                    rc = dlg.run()
                    dlg.destroy()
                    self.datePage.ntpCombo.entry.grab_focus()
                    return

                ntpServerList = self.datePage.getNtpServerList()
                self.dateBackend.writeNtpConfig(sysTimeServer, ntpServerList)

                def child_handler (signum, stack_frame):
                    if not pid:
                        return
                    
                    realpid, waitstat = os.waitpid(pid, os.WNOHANG)
                        
                    if realpid != pid:
                        return
                    gtk.mainquit()
                    result = os.read (read,100)
                    os.close (read)
                    signal.signal (signal.SIGCHLD, signal.SIG_DFL)
                    
                    if int(result) > 0:
                        text = (_("A connection with %s could not be established.  "
                                               "Either %s is not available or the firewall settings "
                                               "on your computer are blocking NTP connections." %
                                               (sysTimeServer, sysTimeServer)))

                        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)

                        dlg.set_title(_("Error"))
                        dlg.set_default_size(100, 100)
                        dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
                        dlg.set_border_width(2)
                        dlg.set_modal(gtk.TRUE)
                        rc = dlg.run()
                        dlg.destroy()
                        self.failedFlag = 1
                        return

                    self.dateBackend.syncHardwareClock()

                signal.signal (signal.SIGCHLD, child_handler)
                (read, write) = os.pipe ()
                pid = os.fork ()

                if pid == 0:
                    signal.signal (signal.SIGCHLD, signal.SIG_DFL)
                    # do something slow
                    os.close (read)
                    time.sleep (2)
                    retval = self.dateBackend.startNtpService(None)
                    retval = str(retval)
                    os.write (write, retval)
                    os._exit (0)

                os.close (write)

                dlg = gtk.Dialog('', None, 0, (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
                dlg.set_border_width(10)
                label = gtk.Label(_("Contacting NTP server.  Please wait..."))
                dlg.vbox.set_spacing(5)
                dlg.vbox.add(label)
                dlg.set_position (gtk.WIN_POS_CENTER)
                dlg.set_modal(gtk.TRUE)
                dlg.connect ('response', self.response_cb, pid)
                dlg.show_all()

                #work around http://bugzilla.gnome.org/show_bug.cgi?id=72333 )-;
                id = gtk.timeout_add(20, lambda:1)
                gtk.mainloop()
                dlg.destroy()
                gtk.idle_remove (id)          

                self.dateBackend.chkconfigOn()

        if self.failedFlag:
            return None
        else:
            return 0

    def grabFocus(self):
        print "entering date screen"
        self.datePage.updateSpinButtons()

    def stand_alone(self, doDebug = None):
        self.doDebug = doDebug
        self.setupScreen()
        return FirstbootGuiWindow.stand_alone(self, TimeWindow.windowTitle)

childWindow = TimeWindow
