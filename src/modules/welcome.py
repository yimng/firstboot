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
#        print dir(self.vbox)
        label = gtk.Label("Welcome to Red Hat Linux 8.0!")
        white = gtk.gdk.color_parse ("white")
        label.modify_fg(gtk.STATE_NORMAL, white)
#        label.modify_bg(gtk.STATE_NORMAL, blue)
#        self.vbox.modify_base(gtk.STATE_NORMAL, blue)


        eventBox = gtk.EventBox()
        eventBox.add(label)
        blue = gtk.gdk.color_parse ("#0000BB")
        eventBox.modify_bg(gtk.STATE_NORMAL, blue)
        self.vbox.pack_start(eventBox, FALSE, 40)


#        self.vbox.pack_start(label, FALSE, TRUE, 30)
        a = gtk.Alignment()
        a.add(gtk.HSeparator())
        a.set(0.5, 0.5, 1.0, 1.0)
        
        self.vbox.pack_start(a, FALSE)

        a = gtk.Alignment()
        a.add(self.vbox)
        a.set(0.8, 0.5, 0.2, 1.0)

        return a
#        return self.vbox

    def write_file(self):
        pass

    def apply(self):
        pass
