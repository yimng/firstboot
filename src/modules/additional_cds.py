from gtk import *
import string
import gtk
import gobject
import os
import time
import functions
import rhpl.diskutil as diskutil

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 140
    moduleName = (_("Additional CDs"))

    def launch(self, doDebug=None):
        if doDebug:
            print "initializing additional_cd module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        msg = (_("Install Additional Software"))
        label = gtk.Label("")
        label.set_alignment(0.4, 0.5)
        label.set_markup("<span size='x-large'>%s</span>" % msg)
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("lacd.png")
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
        self.vbox.pack_start(eventBox, FALSE)

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        table = gtk.Table(3, 2)
        table.set_col_spacings(10)
        table.set_row_spacings(10)

        label = gtk.Label(_("If you have any of the CDs listed below, you can install "
                            "packages from them by inserting the CD and clicking the "
                            "appropriate button."))

        label.set_line_wrap(TRUE)
        label.set_size_request(500, -1)
        label.set_alignment(0.0, 0.5)
        internalVBox.pack_start(label, FALSE, TRUE)

        pix = functions.imageFromFile("docs.png")
        table.attach(pix, 0, 1, 0, 1, gtk.SHRINK)

        label = gtk.Label(_("Red Hat Linux Documentation CD"))                            
        label.set_alignment(0.0, 0.5)
        table.attach(label, 1, 2, 0, 1, gtk.FILL, gtk.SHRINK)

        button = gtk.Button(_("Install..."))
        button.connect("clicked", self.autorun)
        table.attach(button, 2, 3, 0, 1, gtk.SHRINK, gtk.SHRINK)
 
        pix = functions.imageFromFile("cd.png")
        table.attach(pix, 0, 1, 1, 2, gtk.SHRINK)

        label = gtk.Label(_("Red Hat Linux Installation CD"))                            
        label.set_alignment(0.0, 0.5)
        table.attach(label, 1, 2, 1, 2, gtk.FILL, gtk.SHRINK)

        button = gtk.Button(_("Install..."))
        button.connect("clicked", self.autorun)
        table.attach(button, 2, 3, 1, 2, gtk.SHRINK, gtk.SHRINK)

        pix = functions.imageFromFile("lacd.png")
        table.attach(pix, 0, 1, 2, 3, gtk.SHRINK)

        label = gtk.Label(_("Additional CDs"))                            
        label.set_alignment(0.0, 0.5)
        table.attach(label, 1, 2, 2, 3, gtk.FILL, gtk.SHRINK)

        button = gtk.Button(_("Install..."))
        button.connect("clicked", self.autorun)
        table.attach(button, 2, 3, 2, 3, gtk.SHRINK, gtk.SHRINK)

        internalVBox.pack_start(table, gtk.FALSE, padding=20)
        self.vbox.pack_start(internalVBox, gtk.TRUE)

        return self.vbox, eventBox

    def autorun(self, *args):
        #Create a gtkInvisible dialog to block until the autorun is complete
        i = gtk.Invisible ()
        i.grab_add ()

        mountFlag = None

        while not mountFlag:
            try:
                diskutil.mount('/dev/cdrom', '/mnt/cdrom', fstype="iso9660", readOnly = 1)
                mountFlag = 1
            except:
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_NONE,
                                        (_("A CD-ROM has not been detected.  Please insert "
                                           "a CD-ROM in the drive and click \"OK\" to continue.")))
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_modal(gtk.TRUE)
                cancelButton = dlg.add_button('gtk-cancel', 0)
                okButton = dlg.add_button('gtk-ok', 1)
                rc = dlg.run()
                dlg.destroy()
                
                if rc == 0:
                    return
                
        pid = functions.start_process("/mnt/cdrom/autorun")

        flag = None
        while not flag:
            while gtk.events_pending():
                gtk.main_iteration_do()

            child_pid, status = os.waitpid(pid, os.WNOHANG)
            
            if child_pid == pid:
                flag = 1
            else:
                time.sleep(0.1)

        diskutil.umount('/mnt/cdrom')

        i.grab_remove ()

    def apply(self, notebook):
        return 1
