from gtk import *
import string
import gtk
import gobject

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 100
    moduleName = "Welcome"

    def __init__(self):
        print "initializing welcome module"
                
    def launch(self):
        self.vbox = gtk.VBox()
        self.vbox.set_usize(400, 200)


        label = gtk.Label("Welcome to Red Hat Linux Son of Enigma!")
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        try:
            p = gtk.gdk.pixbuf_new_from_file("images/shadowman-round-48.png")
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

        label = gtk.Label("Welcome message goes here")
        eventBox = gtk.EventBox()
        eventBox.add(label)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#EEEEEE"))
        self.vbox.pack_start(eventBox, TRUE)

        return self.vbox

    def write_file(self):
        pass

    def apply(self, notebook):
        print "nothing to do in welcome"
        pass
