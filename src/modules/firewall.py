#!/usr/bin/python

from gtk import *
import string
import libglade
import gtk

xml = libglade.GladeXML ("/home/devel/bfox/redhat/firstboot/glade/firewall.glade", domain="redhat-config-firewall")

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 40

    def __init__(self):
        self.toplevel = xml.get_widget("mainWindow")
        self.vbox = xml.get_widget("mainVBox")
        print "initializing module"

                
    def launch(self):
        print "launching firewall"
        #Hack to remove vbox from the toplevel window so it can
        #be packed into firstboot's main window
        print self.toplevel.children()

        if self.toplevel.children() != []:
            print "removing child"
            self.toplevel.remove(self.toplevel.children()[0])
        else:
            print "no child to remove"

        print self.vbox
        return self.vbox

#        label = GtkLabel("foo")
#        return label


    def write_file(self):
        pass

    def stand_alone(self):
#        box = childWindow().launch()
#        toplevel.add(box)
        self.toplevel.show_all()
        gtk.mainloop()
