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

        pix = functions.imageFromFile("rhn_register.png")
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

        radioBox = gtk.VBox()

        self.radioYes = gtk.RadioButton(None, _("Yes, I would like to register with Red Hat Network"))
        radioNo = gtk.RadioButton(self.radioYes, _("No, I do not want to register my system."))

        radioBox.pack_start(self.radioYes, gtk.FALSE)
        radioBox.pack_start(radioNo, gtk.FALSE)

        a = gtk.Alignment()
        a.add(radioBox)
        a.set(0.3, 0.0, 0.3, 0.5)
        internalVBox.pack_start(a, FALSE, padding=10)


        self.vbox.pack_start(internalVBox)

        return self.vbox, eventBox

    def networkAvailable(self):
        #First, check to see if we can communicate with the requested server
        server = "www.redhat.com"

        data = os.popen("ping -c 2 %s" % server)
        rc = data.close()
        
        if rc == None:
            #Server was contacted, so write out the correct files and start up the service
            return 1
        else:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
_("A connection with %s could not be established.  Either %s is not available or the firewall settings "
  "on your computer are preventing the connections." % (server, server)))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            dlg.destroy()
            print "no networking found"
            return 0

    def run_rhn_register(self, *args):
        #Run rhn_register so they can register with RHN
        path = "/usr/sbin/rhn_register"
        fd = os.popen(path)
        fd.close()

    def apply(self, notebook):
        # If they want to register, then kick off rhn_register.  If not, then pass
        if self.radioYes.get_active() == gtk.TRUE:            
            if self.networkAvailable():
                #We can ping www.redhat.com, so the network is active
                self.run_rhn_register()
        return 1
