from gtk import *
import string
import gtk
import gobject
import sys
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
    runPriority = 0
    moduleName = (_("Welcome"))

    def launch(self, doDebug = None):
        if doDebug:
            print "initializing welcome module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        msg = (_("Welcome"))

        title_pix = functions.imageFromFile("workstation.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        label = gtk.Label(_("There are a few more steps to "
                          "take before your system is ready to use.  The Red Hat Setup Agent "
                          "will now guide you through some basic configuration.  Please click the "
                            "\"Forward\" button in the lower right corner to continue."))

        label.set_line_wrap(gtk.TRUE)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        internalVBox.pack_start(label, FALSE, TRUE)

        self.vbox.pack_start(internalVBox, gtk.FALSE, 5)
        pix = functions.ditheredImageFromFile("splash-small.png")
        self.vbox.pack_start(pix, gtk.TRUE, gtk.TRUE, 5)
            
        return self.vbox, title_pix, msg

    def apply(self, notebook):
        return 0
