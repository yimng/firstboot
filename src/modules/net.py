from gtk import *
import string
import gobject
import gtk
import os
from socket import gethostname
#from socket import gethostbyname

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 111
#    moduleName = "Network activate"

    def __init__(self):
        print "initializing page2"
#        self.launch()

    def launch(self):
        
        hbox = gtk.HBox()
        label = gtk.Label("Foobar")
        hbox.pack_start(label)
        return hbox

##         try:
##             os.stat('.networkcheck.lock2')
##             hbox = gtk.HBox()
##             label = gtk.Label("Hello")
##             hbox.pack_start(label)
##             return hbox

##         except:
##             hbox = gtk.HBox()
##             return hbox

    def apply (self, notebook):
        print "applying page2"

#        try:
#            os.stat('.networkcheck.lock2')
#        except:
#            notebook.next_page()
#            notebook.next_page()
