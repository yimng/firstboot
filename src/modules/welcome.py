#!/usr/bin/python

from gtk import *
import string

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 100
    moduleName = "Welcome"

    def __init__(self):
        print "initializing welcome module"
                
    def launch(self):
        self.vbox = GtkVBox()
        label = GtkLabel("Welcome to Red Hat Linux 8.0!")
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        return self.vbox

    def write_file(self):
        pass

    def apply(self):
        pass
