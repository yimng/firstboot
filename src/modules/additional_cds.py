from gtk import *
import string
import gtk
import gobject
import os
import functions

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 1000
    moduleName = (_("Additional CDs"))

    def __init__(self):
        self.additionalDiscs = {(_("Red Hat Documentation CD")) : "docs.png",
                                (_("Linux Application CD")) : "lacd.png"}
                
    def launch(self, doDebug=None):
        if doDebug:
            print "initializing additional_cd module"

        os.stat('/etc/sysconfig/rhn/rhn_register')
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        label = gtk.Label("Install additional software")

        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("boxset_standard.png")
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

        label = gtk.Label(_("If you have additional CDs from the Red Hat Linux box "
                          "set, such as the Red Hat Linux Documentation CD or the "
                          "Linux Applications CD, please insert the disc now and "
                          "click the button below."))
        
        label.set_line_wrap(TRUE)
        label.set_size_request(400, -1)
        label.set_alignment(0.0, 0.5)
        internalVBox.pack_start(label, FALSE, TRUE)

        buttons = self.additionalDiscs.keys()
        buttons.sort()
        for button in buttons:
            newButton = self.create_button(self.additionalDiscs[button], button)
            newButton.connect("clicked", self.autorun)
            internalVBox.pack_start(newButton, gtk.FALSE, padding=10)

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
        mount = os.fork()
        if (not mount):
            os.execv("/bin/mount", ["mount", "/dev/cdrom"])

        pid, status = os.waitpid(mount, 0)

        if os.WIFEXITED(status) and (os.WEXITSTATUS(status) == 0):
            try:
                os.stat('/mnt/cdrom/autorun')

                win = os.fork()
                if not win:
                    os.execv("/mnt/cdrom/autorun", ["autorun"])
            except:
                pass
                
    def apply(self, notebook):
        return 1
