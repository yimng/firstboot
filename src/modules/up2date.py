#!/usr/bin/python

from gtk import *
import string
import os

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 130
    moduleName = "up2date"

    def __init__(self):
        print "initializing up2date module"
                
    def launch(self):
        try:
            #If the system is registered with RHN, then show up2date screen
            os.stat('/etc/sysconfig/rhn/rhn_register')
            self.vbox = GtkVBox()
#            label = GtkLabel("Keep your system up2date!")
            label = GtkLabel("Now that you are registered with Red Hat Network, you can run "
                             "the Red Hat Update Agent to receive the latest software "
                             "packages directly from Red Hat.  Using this tool will allow you "
                             "to always have the most up-to-date Red Hat Linux system "
                             "with all the security patches, bug fixes, and software "
                             "package enhancements")
            label.set_line_wrap(TRUE)
            label.set_usize(600, -1)
            label.set_alignment(0.0, 0.5)
            self.vbox.pack_start(label, FALSE, TRUE)

            launchButton = GtkButton("Start the Red Hat Update Agent")
            a = GtkAlignment()
            a.add(launchButton)            
            a.set(0.3, 0.0, 0.3, 0.5)
            self.vbox.pack_start(a, FALSE, padding=10)

            launchButton.connect("clicked", self.rhn_register)
#            self.vbox.pack_start(launchButton, FALSE)
            return self.vbox
        except:
            #If the system is not registered with RHN, then don't run update screen
            return

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
