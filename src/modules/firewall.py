#!/usr/bin/python

from gtk import *
import string
import libglade
import gtk

xml = libglade.GladeXML ("../glade/firewall.glade", domain="redhat-config-firewall")
#xml = libglade.GladeXML ("/usr/share/firstboot/glade/firewall.glade", domain="redhat-config-firewall")

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 40
    moduleName = "Firewall"

    def __init__(self):
        self.toplevel = xml.get_widget("mainWindow")
        self.vbox = xml.get_widget("mainVBox")
                
    def launch(self):
        #Hack to remove vbox from the toplevel window so it can
        #be packed into firstboot's main window
        if self.toplevel.children() != []:
            self.toplevel.remove(self.toplevel.children()[0])
        else:
            pass

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
