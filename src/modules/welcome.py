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
        print dir(self.vbox)
        label = gtk.Label("Welcome to Red Hat Linux 8.0!")
        blue = gtk.gdk.color_parse ("#000055")
        label.modify_fg(gtk.STATE_NORMAL, blue)
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        return self.vbox

    def write_file(self):
        pass

    def apply(self):
        pass
