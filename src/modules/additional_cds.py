#
# additional_cds.py - firstboot module for add-on CDs
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

from gtk import *
import string
import gtk
import gobject
import kudzu
import os
import time
import functions
import rhpl.diskutil as diskutil


##
## I18N
## 
from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("firstboot")

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 140
    moduleName = (_("Additional CDs"))

    # Turned off for now.
    skipme = True

    def launch(self, doDebug=None):
        if doDebug:
            print "initializing additional_cd module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        title_pix = functions.imageFromFile("lacd.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        table = gtk.Table(3, 3)
        table.set_col_spacings(10)
        table.set_row_spacings(10)

        cd_label_rhel = _("""Please insert the disc labeled "Red Hat Enterprise Linux """
                          """Extras" to allow for installation of third-party plug-ins and """
                          """applications.  You may also insert the Documentation disc, or """
                          """other Red Hat-provided discs to install additional software at """
                          """this time.""")

        cd_label = _("""Please insert any additional software install cds """
                     """at this time.""")


        if os.uname()[4] == "ia64":
#        if 1:
            cd_label = cd_label + _("""\n\nTo enable runtime support of 32-bit applications on the Intel """
                                    """Itanium2 architecture you must install the Intel Execution """
                                    """Layer package from the Extras disc now.""")


            
        label = gtk.Label(cd_label)
        label.set_line_wrap(True)
        label.set_size_request(500, -1)
        label.set_alignment(0.0, 0.5)
        internalVBox.pack_start(label, False, True)

#        pix = functions.imageFromFile("docs.png")
#        table.attach(pix, 0, 1, 0, 1, gtk.SHRINK)

#        label = gtk.Label(_("Red Hat Linux Documentation CD"))                            
#        label.set_alignment(0.0, 0.5)
#        table.attach(label, 1, 2, 0, 1, gtk.FILL, gtk.SHRINK)

#        button = gtk.Button(_("Install..."))
#        button.connect("clicked", self.autorun)
#        table.attach(button, 2, 3, 0, 1, gtk.SHRINK, gtk.SHRINK)
 
##         pix = functions.imageFromFile("cd.png")
##         table.attach(pix, 0, 1, 1, 2, gtk.SHRINK)

##         label = gtk.Label(_("Red Hat Linux Installation CD"))                            
##         label.set_alignment(0.0, 0.5)
##         table.attach(label, 1, 2, 1, 2, gtk.FILL, gtk.SHRINK)

##         button = gtk.Button(_("Install..."))
##         button.connect("clicked", self.autorun)
##         table.attach(button, 2, 3, 1, 2, gtk.SHRINK, gtk.SHRINK)

        pix = functions.imageFromFile("lacd.png")
        table.attach(pix, 0, 1, 2, 3, gtk.SHRINK)

        label = gtk.Label(_("Additional CDs"))                            
        label.set_alignment(0.0, 0.5)
        table.attach(label, 1, 2, 2, 3, gtk.FILL, gtk.SHRINK)

        button = gtk.Button(_("Install..."))
        button.connect("clicked", self.autorun)
        table.attach(button, 2, 3, 2, 3, gtk.SHRINK, gtk.SHRINK)


#        pix = functions.imageFromFile("lacd.png")
#        table.attach(pix, 0, 1, 3, 4, gtk.SHRINK)
                                                                                                             
#        label = gtk.Label(_("Intel Execution Layer from the Extras CD."))
#        label.set_alignment(0.0, 0.5)
#        table.attach(label, 1, 2, 3, 4, gtk.FILL, gtk.SHRINK)
                                                                                                             
#        button = gtk.Button(_("Install..."))
#        button.connect("clicked", self.autorun)
#        table.attach(button, 2, 3, 3, 4, gtk.SHRINK, gtk.SHRINK)


        internalVBox.pack_start(table, False, padding=20)
        self.vbox.pack_start(internalVBox, True)

        return self.vbox, title_pix, self.moduleName

    def autorun(self, *args):
        def getCDDev():
            drives = kudzu.probe(kudzu.CLASS_CDROM,
                                 kudzu.BUS_UNSPEC, kudzu.PROBE_ALL)
            for d in drives:
                return d.device
            return None
            
            
        #Create a gtkInvisible widget to block until the autorun is complete
        i = gtk.Invisible ()
        i.grab_add ()

        mountFlag = None

        while not mountFlag:
            try:
                dev = getCDDev()
                if dev is None:
                    raise Exception, "no cd drive found"
                diskutil.mount("/dev/%s" % (dev,) , '/mnt', fstype="iso9660", readOnly = 1)
                mountFlag = 1
            except:
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE,
                                        (_("A CD-ROM has not been detected.  Please insert "
                                           "a CD-ROM in the drive and click \"OK\" to continue.")))
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_modal(True)
                cancelButton = dlg.add_button('gtk-cancel', 0)
                okButton = dlg.add_button('gtk-ok', 1)
                rc = dlg.run()
                dlg.destroy()
                
                if rc == 0:
                    #Be sure to remove the focus grab if we have to return here.
                    #Otherwise, the user is stuck
                    i.grab_remove ()
                    return

        if os.access("/mnt/autorun", os.R_OK):
            #If there's an autorun file on the cd, run it
            pid = functions.start_process("/mnt/autorun")

            flag = None
            while not flag:
                while gtk.events_pending():
                    gtk.main_iteration_do()

                child_pid, status = os.waitpid(pid, os.WNOHANG)

                if child_pid == pid:
                    flag = 1
                else:
                    time.sleep(0.1)

        else:
            #There's no autorun on the disc, so complain
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE,
                                    (_("The autorun program cannot be found on the CD. "
                                       "Click \"OK\" to continue.")))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)
            okButton = dlg.add_button('gtk-ok', 0)
            rc = dlg.run()
            dlg.destroy()

            if rc == 0:
                #Be sure to remove the focus grab if we have to return here.
                #Otherwise, the user is stuck
                i.grab_remove ()

        #I think system-config-packages will do a umount, but just in case it doesn't...
        try:
            diskutil.umount('/mnt')
        except:
            #Yep, system-config-packages has already umounted the disc, so fall through and go on
            pass

        #Remove the focus grab of the gtkInvisible widget
        i.grab_remove ()

    def apply(self, notebook):
        return 1
