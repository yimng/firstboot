#!/usr/bin/python

from gtk import *
import string
import libglade
import gtk
import gnome.ui

xml = libglade.GladeXML ("/home/bfox/redhat/firstboot/glade/firewall.glade", domain="redhat-config-firewall")
#xml = libglade.GladeXML ("/usr/share/firstboot/glade/firewall.glade", domain="redhat-config-firewall")

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 40
    moduleName = "Firewall"
    moduleClass = "reconfig"
    
    def __init__(self):
        self.mainWindow = xml.get_widget("mainWindow")
        self.toplevel = xml.get_widget("topVBox")
        self.vbox = xml.get_widget("mainVBox")
#        self.deviceList = xml.get_widget("deviceList")
#        self.netdevices = []
                
    def launch(self):
        #Hack to remove vbox from the toplevel window so it can
        #be packed into firstboot's main window
        if self.toplevel.children() != []:
            self.toplevel.remove(self.toplevel.children()[0])
        else:
            pass

#        self.devices = self.availableDevices()
#        for device in self.devices:
#            self.deviceList.append([device])

        return self.vbox

    def write_file(self):
        pass

    def stand_alone(self):
        self.mainWindow.show_all()
        gtk.mainloop()
