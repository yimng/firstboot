#!/usr/bin/python

from gtk import *
import string
import os

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 30
    moduleName = "Register with Red Hat Network"

    def __init__(self):
        print "initializing RHN module"
                
    def launch(self):
        self.vbox = GtkVBox()
        label = GtkLabel("Register your system with Red Hat Network")
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        launchButton = GtkButton("Register system now")
        launchButton.connect("clicked", self.rhn_register)
        self.vbox.pack_start(launchButton, FALSE)
        return self.vbox

    def rhn_register(self, *args):
        win = os.fork()

        if (not win):
            print "launching rhn_register"
            path = "/usr/sbin/rhn_register"
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
