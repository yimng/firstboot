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
    runPriority = -140
    moduleName = (_("Additional CDs"))

#    def __init__(self):
#        self.additionalDiscs = {(_("Red Hat Documentation CD")) : "docs.png",
#                                (_("Linux Application CD")) : "lacd.png"}
                
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

        pix = functions.imageFromFile("docs.png")
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
        self.vbox.pack_start(eventBox, FALSE)

        a = gtk.Alignment()
        a.add(gtk.HSeparator())
        a.set(0.5, 0.5, 1.0, 1.0)

        self.vbox.pack_start(a, FALSE)

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        label = gtk.Label(_("If you have additional CD-ROMs that you would like to install, "
                            "such as the Red Hat Linux Docmentation CD, you may do that "
                            "now.  Place the CD-ROM in the drive and click the "
                            "\"Install software\" button below."))


#        label = gtk.Label(_("If you have additional CDs from the Red Hat Linux box "
#                          "set, such as the Red Hat Linux Documentation CD or the "
#                          "Linux Applications CD, please insert the disc now and "
#                          "click the corresponding button below."))
        
        label.set_line_wrap(TRUE)
        label.set_size_request(400, -1)
        label.set_alignment(0.0, 0.5)
        internalVBox.pack_start(label, FALSE, TRUE)

 #       buttons = self.additionalDiscs.keys()
 #       buttons.sort()
##        for button in buttons:
##             newButton = self.create_button(self.additionalDiscs[button], button)
##             newButton.connect("clicked", self.autorun)
##             internalVBox.pack_start(newButton, gtk.FALSE, padding=10)

        self.installButton = self.create_button("lacd.png", "Install software")
        self.installButton.connect("clicked", self.autorun)
        internalVBox.pack_start(self.installButton, gtk.FALSE, padding=10)


        self.vbox.pack_start(internalVBox, TRUE)

        return self.vbox, eventBox

    def create_button(self, image, name):
        pix = functions.imageFromFile(image)
        box = gtk.HBox()
        if pix:
            box.pack_start(pix, gtk.FALSE)

        label = gtk.Label(name)
        box.pack_start(label, gtk.FALSE)
        button = gtk.Button()
        button.add(box)
        return button


    def autorun(self, *args):
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

    def apply(self, notebook):
        return 1
