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

        label = gtk.Label(_("Welcome to Red Hat Linux Beta!"))
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("shadowman-round-48.png")
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

        pix = functions.imageFromFile("splash.png")
        self.vbox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)


#        label = gtk.Label("Welcome message goes here")
#        self.vbox.pack_start(label, TRUE)

#        self.hbox = gtk.HBox()
#        self.hbox.pack_start(self.splash, gtk.FALSE)
#        self.hbox.pack_start(label, gtk.TRUE)
#        self.vbox.pack_start(self.hbox, gtk.TRUE)

            
        return self.vbox, eventBox

    def apply(self, notebook):
        return 1
