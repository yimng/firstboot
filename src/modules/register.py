#!/usr/bin/python

from gtk import *
import string
import os
from socket import gethostname
from socket import gethostbyname

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 120
    moduleName = "Register with RHN"

    def __init__(self):
        print "initializing RHN module"

    def launch(self):
        self.vbox = GtkVBox()

        if self.networkAvailable() == TRUE:
#            label = GtkLabel("Register your system with Red Hat Network")


            label = GtkLabel("Red Hat Network is an Internet solution for managing "
                             "one or more Red Hat Linux systems. All Security Alerts, "
                             "Bug Fix Alerts, and Enhancement Alerts (collectively known as "
                             "Errata Alerts) can be retreived directly from Red Hat. You can "
                             "even have updates automatically delivered directly to your system "
                             "as soon as they are released. \n\n"
                             "Because Red Hat Network keeps track of when Errata Updates are "
                             "released and sends you email notifications, it can:")
            label.set_line_wrap(TRUE)
            label.set_usize(600, -1)
            label.set_alignment(0.0, 0.5)
            self.vbox.pack_start(label, FALSE, TRUE)

            label = GtkLabel("* Reduce the time and effort required by system administrators "
                             "to stay on top of the Red Hat errata list\n"
                             "* Minimize security vulnerabilities in your network by providing "
                             "the patches as soon as Red Hat releases them\n"
                             "* Filter out package updates not relevant to your network\n"
                             "* Schedule Errata Updates so that packages are delivered to "
                             "selected systems when you want it")
            label.set_line_wrap(TRUE)
            label.set_alignment(0.1, 0.5)
            label.set_usize(600, -1)
#To start using Red Hat Network today, follow these steps:

            self.vbox.pack_start(label, FALSE, TRUE)
            launchButton = GtkButton("Register system now")

            a = GtkAlignment()
            a.add(launchButton)
            a.set(0.3, 0.0, 0.3, 0.5)
            self.vbox.pack_start(a, FALSE, padding=10)

            launchButton.connect("clicked", self.rhn_register)
#            self.vbox.pack_start(launchButton, FALSE, FALSE)
        else:
            label = GtkLabel("You currently have no network.")
            self.vbox.pack_start(label, FALSE, TRUE, 30)
#            launchButton = GtkButton("Register system now")
#            launchButton.connect("clicked", self.rhn_register)
#            self.vbox.pack_start(launchButton, FALSE)


        return self.vbox

    def networkAvailable(self):
        try:
            gethostbyname(gethostname())
            print gethostname()
            print gethostbyname(gethostname())
            print "network is functional"
            return TRUE
        except:
            print "no networking found"
            return FALSE

    def rhn_register(self, *args):
        win = os.fork()

        if (not win):
            print "launching rhn_register"
            path = "/usr/sbin/rhn_register"
            os.execv(path, [])

    def write_file(self):
        pass

