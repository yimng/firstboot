from gtk import *
import string
import gtk
import gobject

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 0
    moduleName = "Welcome"

    def __init__(self):
        print "initializing welcome module"
                
    def launch(self):
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        label = gtk.Label("Welcome to Red Hat Linux Beta One!")
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        p = None
        
        try:
            p = gtk.gdk.pixbuf_new_from_file("pixmaps/shadowman-round-48.png")
        except:
            pass

        if p:
            self.icon = gtk.Image()
            self.icon.set_from_pixbuf(p)
            titleBox.pack_start(self.icon, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

        try:
            p = gtk.gdk.pixbuf_new_from_file("pixmaps/splash.png")
        except:
            pass

        if p:
            self.splash = gtk.Image()
            self.splash.set_from_pixbuf(p)
            self.vbox.pack_start(self.splash, gtk.FALSE, gtk.TRUE, 5)


#        label = gtk.Label("Welcome message goes here")
#        self.vbox.pack_start(label, TRUE)

#        self.hbox = gtk.HBox()
#        self.hbox.pack_start(self.splash, gtk.FALSE)
#        self.hbox.pack_start(label, gtk.TRUE)
#        self.vbox.pack_start(self.hbox, gtk.TRUE)

            
        return self.vbox, eventBox

    def apply(self, notebook):
        return 1
