#!/usr/bin/python

from gtk import *
import string
import sys

print "foodog"
sys.path.append('/home/bfox/redhat/redhat-config-nfs/src')
print "blagdoo"
import mainNfsWindow


class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 60
    moduleName = "NFS Server"

    def __init__(self):
        print "initializing NFS module"
                
    def launch(self):
#        self.vbox = GtkVBox()
#        label = GtkLabel("This is a template module")
#        self.vbox.pack_start(label, FALSE, TRUE, 30)
        win = mainNfsWindow.mainWindow()
        vbox = win.embed()
        return vbox

    def write_file(self):
        pass

    def stand_alone(self):
        toplevel = GtkWindow()
        toplevel.set_usize(300, 400)
        box = childWindow().launch()
        toplevel.add(box)
        toplevel.show_all()
        mainloop()
