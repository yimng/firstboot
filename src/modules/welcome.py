from gtk import *
import string
import gtk
import gobject

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 0
    moduleName = "Welcome"

    def __init__(self, doDebug = None):
        if doDebug:
            print "initializing welcome module"
                
    def launch(self):
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        label = gtk.Label("Welcome to Red Hat Linux Beta One!")
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = self.imageFromFile("shadowman-round-48.png")
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

        pix = self.imageFromFile("splash.png")
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

    # Attempt to load a gtk.Image from a file.
    def imageFromFile(self, filename):
        p = None        
        try:
            path = "../pixmaps/" + filename
            p = gtk.gdk.pixbuf_new_from_file(path)
        except:
            try:
                path = "/usr/share/firstboot/pixmaps/" + filename
                p = gtk.gdk.pixbuf_new_from_file(path)
            except:
                pass

        if p:
            pix = gtk.Image()
            pix.set_from_pixbuf(p)        
            return pix
        return None
