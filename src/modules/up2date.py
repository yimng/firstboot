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
    runPriority = 130
    moduleName = (_("Red Hat Update Agent"))
                
    def launch(self, doDebug=None):
        if doDebug:
            print "launching up2date module"

        try:
            os.stat('/etc/sysconfig/rhn/rhn_register')
            self.vbox = gtk.VBox()
            self.vbox.set_size_request(400, 200)

            label = gtk.Label(_("Red Hat Update Agent"))
            label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

            titleBox = gtk.HBox()

            pix = functions.imageFromFile("boxset_standard.png")
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

            label = gtk.Label(_("Now that you are registered with Red Hat Network, you can run "
                             "the Red Hat Update Agent to receive the latest software "
                             "packages directly from Red Hat.  Using this tool will allow you "
                             "to always have the most up-to-date Red Hat Linux system "
                             "with all the security patches, bug fixes, and software "
                             "package enhancements."))
            label.set_line_wrap(TRUE)
            label.set_size_request(400, -1)
            label.set_alignment(0.0, 0.5)
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

            self.vbox.pack_start(internalVBox, TRUE)

            return self.vbox, eventBox
        except:
            return

    def run_up2date(self, *args):
        #Run rhn_register so they can register with RHN
        path = "/usr/sbin/up2date"
        fd = os.popen(path)
        fd.close()

    def apply(self, notebook):
        # If they want to register, then kick off rhn_register.  If not, then pass
        if self.radioYes.get_active() == gtk.TRUE:            
            #We can ping www.redhat.com, so the network is active
            self.run_up2date()
        return 1
            
