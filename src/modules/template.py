#!/usr/bin/python

from gtk import *
import string

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 10
    moduleName = "Template"

    def __init__(self):
        print "initializing template module"
                
    def launch(self):
        self.vbox = GtkVBox()
        label = GtkLabel("This is a template module")
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        return self.vbox

    def write_file(self):
        pass

    def stand_alone(self):
        toplevel = GtkWindow()
        toplevel.set_usize(300, 400)
        box = childWindow().launch()
        toplevel.add(box)
        toplevel.show_all()
        mainloop()
