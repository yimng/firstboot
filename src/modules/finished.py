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
    runPriority = 500
    moduleName = (_("Finish Installation"))

    def launch(self, doDebug = None):
        if doDebug:
            print "initializing finished module"

        self.vbox = gtk.VBox(gtk.FALSE, 10)
        self.vbox.set_size_request(400, 200)

        label = gtk.Label(_("Finished installation!"))
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("shadowman-round-48.png")
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

        label = gtk.Label(_("Contratulations!  Your Red Hat Linux system is now set up and ready to "
                          "use.  We hope that you will have a pleasant computing experience.  Please "
                            "click the \"Forward\" button in the lower right corner to continue."))

        label.set_alignment(0.1, 0.5)
        label.set_line_wrap(gtk.TRUE)
        label.set_size_request(500, -1)

        self.vbox.pack_start(label, gtk.FALSE, 5)
        pix = functions.imageFromFile("splash-small.png")
        self.vbox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

            
        return self.vbox, eventBox

    def apply(self, notebook):
        return 1
