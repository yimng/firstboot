from gtk import *
import string
import gtk
import gobject
import os
import functions
from socket import gethostname
from socket import gethostbyname

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 120
    moduleName = (_("Register with RHN"))

    def launch(self, doDebug=None):
        if doDebug:
            print "launching register module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        label = gtk.Label(_("Register your system with Red Hat Network"))
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("rhn.png")
        if pix:
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

        if self.networkAvailable() == TRUE:
            label = gtk.Label(_("Red Hat Network is an Internet solution for managing "
                             "one or more Red Hat Linux systems. All Security Alerts, "
                             "Bug Fix Alerts, and Enhancement Alerts (collectively known as "
                             "Errata Alerts) can be retreived directly from Red Hat. You can "
                             "even have updates automatically delivered directly to your system "
                             "as soon as they are released. \n\n"
                             "Because Red Hat Network keeps track of when Errata Updates are "
                             "released and sends you email notifications, it can:"))
            label.set_line_wrap(TRUE)
            label.set_size_request(400, -1)
            label.set_alignment(0.0, 0.5)
            internalVBox.pack_start(label, FALSE, TRUE)

            label = gtk.Label(_(" -- Reduce the time and effort required by system administrators "
                             "to stay on top of the Red Hat errata list\n"
                             " -- Minimize security vulnerabilities in your network by providing "
                             "the patches as soon as Red Hat releases them\n"
                             " -- Filter out package updates not relevant to your network\n"
                             " -- Schedule Errata Updates so that packages are delivered to "
                             "selected systems when you want it"))
            label.set_line_wrap(TRUE)
            label.set_alignment(0.1, 0.5)
            label.set_size_request(400, -1)

            internalVBox.pack_start(label, FALSE, TRUE)
            launchButton = gtk.Button(_("Register system now"))

            a = gtk.Alignment()
            a.add(launchButton)
            a.set(0.3, 0.0, 0.3, 0.5)
            internalVBox.pack_start(a, FALSE, padding=10)

            launchButton.connect("clicked", self.rhn_register)
#            internalVBox.pack_start(launchButton, FALSE, FALSE)
        else:
            label = gtk.Label(_("You currently have no network connection."))
            internalVBox.pack_start(label, FALSE, TRUE, 30)
#            launchButton = GtkButton("Register system now")
#            launchButton.connect("clicked", self.rhn_register)
#            internalVBox.pack_start(launchButton, FALSE)

        self.vbox.pack_start(internalVBox)

        return self.vbox, eventBox

    def networkAvailable(self):
        try:
            gethostbyname(gethostname())
            print gethostname()
            print gethostbyname(gethostname())
            print "network is functional"
            return TRUE
        except:
            print "no networking found"
            return FALSE

    def rhn_register(self, *args):
        win = os.fork()

        if (not win):
            print "launching rhn_register"
            path = "/usr/sbin/rhn_register"
            os.execv(path, [""])

    def apply(self, notebook):
        return 1
