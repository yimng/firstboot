from gtk import *
import string
import gtk
import gobject
import os

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 130
    moduleName = "Red Hat Update Agent"

    def __init__(self):
        print "initializing welcome module"
                
    def launch(self):
        try:
            os.stat('/etc/sysconfig/rhn/rhn_register')
            self.vbox = gtk.VBox()
            self.vbox.set_usize(400, 200)

            label = gtk.Label("Red Hat Update Agent")
            label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

            titleBox = gtk.HBox()

            try:
                p = gtk.gdk.pixbuf_new_from_file("images/networking.png")
            except:
                pass

            if p:
                pix = gtk.Image()
                pix.set_from_pixbuf(p)
                titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)



            titleBox.pack_start(label)

            eventBox = gtk.EventBox()
            eventBox.add(titleBox)
            eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
            self.vbox.pack_start(eventBox, FALSE)

    #        self.vbox.pack_start(label, FALSE, TRUE, 30)
            a = gtk.Alignment()
            a.add(gtk.HSeparator())
            a.set(0.5, 0.5, 1.0, 1.0)

            self.vbox.pack_start(a, FALSE)

            internalVBox = gtk.VBox()
            internalVBox.set_border_width(10)

            label = gtk.Label("Now that you are registered with Red Hat Network, you can run "
                             "the Red Hat Update Agent to receive the latest software "
                             "packages directly from Red Hat.  Using this tool will allow you "
                             "to always have the most up-to-date Red Hat Linux system "
                             "with all the security patches, bug fixes, and software "
                             "package enhancements")
            label.set_line_wrap(TRUE)
            label.set_usize(400, -1)
            label.set_alignment(0.0, 0.5)
            internalVBox.pack_start(label, FALSE, TRUE)

            launchButton = gtk.Button("Start the Red Hat Update Agent")
            a = gtk.Alignment()
            a.add(launchButton)            
            a.set(0.3, 0.0, 0.3, 0.5)
            internalVBox.pack_start(a, gtk.FALSE, padding=10)

            launchButton.connect("clicked", self.up2date)

            eventBox = gtk.EventBox()
            eventBox.add(internalVBox)
            eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#EEEEEE"))
            self.vbox.pack_start(eventBox, TRUE)

            return self.vbox
        except:
            return

    def up2date(self, *args):
        win = os.fork()

        if (not win):
            print "launching up2date"
            path = "/usr/sbin/up2date"
            os.execv(path, [""])
            
    def write_file(self):
        pass

    def apply(self):
        pass
