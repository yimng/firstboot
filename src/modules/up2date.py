#!/usr/bin/python

from gtk import *
import string
import os

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 120
    moduleName = "up2date"

    def __init__(self):
        print "initializing up2date module"
                
    def launch(self):
        self.vbox = GtkVBox()
        label = GtkLabel("Keep your system up2date!")
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        launchButton = GtkButton("Update system now")
        launchButton.connect("clicked", self.rhn_register)
        self.vbox.pack_start(launchButton, FALSE)
        return self.vbox

    def rhn_register(self, *args):
        win = os.fork()

        if (not win):
            print "launching up2date"
            path = "/usr/sbin/up2date"
            os.execv(path, [])

    def write_file(self):
        pass

    def stand_alone(self):
        toplevel = GtkWindow()
        toplevel.set_usize(300, 400)
        box = childWindow().launch()
        toplevel.add(box)
        toplevel.show_all()
        mainloop()
