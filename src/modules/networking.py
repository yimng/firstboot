import string
import gobject
import gtk
import os
from socket import gethostname
from socket import gethostbyname

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 110
    moduleName = "Network check"

    def __init__(self):
        self.netDevs = self.networkDevices()
        self.page = None
                
    def launch(self, doDebug=None):
        if doDebug:
            print "launching networking module"

        network = self.networkAvailable()

        if network:
            print "network is functional...skipping screen"
            return None, None
        else:
            print "network is not functional...showing screen"
            self.mainVBox = gtk.VBox()

            title = gtk.Label("Set up Networking")
            title.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

            titleBox = gtk.HBox()

            p = None
            try:
                p = gtk.gdk.pixbuf_new_from_file("pixmaps/networking.png")
            except:
                pass

            if p:
                pix = gtk.Image()
                pix.set_from_pixbuf(p)
                titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

            titleBox.pack_start(title)

            eventBox = gtk.EventBox()
            eventBox.add(titleBox)
            eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
            self.mainVBox.pack_start(eventBox, gtk.FALSE)

            internalVBox = gtk.VBox(gtk.FALSE, 10)
            internalVBox.set_border_width(10)

            label = gtk.Label("A network connection was not detected.  Network connectivity "
                             "is necessary for registering your system with RHN and for using "
                              "the Red Hat Update Agent to update your system.  "
                              "To set up a network connection, please click on the button below.\n")

            label.set_line_wrap(gtk.TRUE)
            label.set_size_request(500, -1)
            label.set_alignment(0.0, 0.5)

            self.mainVBox.pack_start(internalVBox, gtk.FALSE)
            internalVBox.pack_start(label, gtk.FALSE, gtk.TRUE)


            internalVBox.pack_start(self.page1())
            
        return self.mainVBox, eventBox

    def networkDevices(self):
        netdevices = []
        f = open("/proc/net/dev")
        lines = f.readlines()
        f.close()

        # skip first two lines, they are header
        lines = lines[2:]
        for line in lines:
            dev = string.strip(line[0:6])
            if dev != "lo":
                netdevices.append (dev)
        return netdevices        


    def networkAvailable(self):
        try:
            gethostbyname(gethostname())
            return gtk.TRUE
        except:
            return gtk.FALSE

    def write_file(self):
        pass

    def apply(self, notebook):
         print "applying network changes"

    def page1(self):
        bb = gtk.HButtonBox()
        bb.set_layout(gtk.BUTTONBOX_END)
        bb.set_border_width(10)
#        bb.set_spacing(10)
        self.yesButton = gtk.Button("Set up networking...")
        self.yesButton.connect("clicked", self.setupNetwork)
        bb.pack_start(self.yesButton, gtk.FALSE)
        a = gtk.Alignment()
        a.add(bb)
        a.set(0.1, 0.0, 0.1, 1.0)

        box = gtk.VBox() 
#        box.pack_start(label, gtk.FALSE, gtk.TRUE)
        box.pack_start(a, gtk.FALSE)
        return box

    def page2(self):
        box = gtk.VBox()
#        label = gtk.Label("Adding page")
#        box.pack_start(label)

        notebook = gtk.Notebook()
        align = gtk.Alignment(0.0, 0.5, 0.3, 1.0)
        align.add(notebook)

        internalVBox = gtk.VBox()
        internalVBox.pack_start(align, gtk.FALSE, gtk.FALSE)

        align = gtk.Alignment(0.0, 0.5, 0.6, 1.0)
        align.add(gtk.HSeparator())
        internalVBox.pack_start(align, gtk.FALSE, gtk.FALSE, 10)
        internalVBox.set_border_width(10)
        
        box.pack_start(internalVBox, gtk.FALSE)



        for dev in self.netDevs:
            devbox = gtk.VBox()
            align = gtk.Alignment()
            DHCPcb = gtk.CheckButton(("Configure using DHCP"))

            align.add(DHCPcb)
            devbox.pack_start(align, gtk.FALSE)

            align = gtk.Alignment()
            bootcb = gtk.CheckButton(("Activate on boot"))
#            onboot = devs[i].get("onboot")
#	    bootcb.connect("toggled", self.onBootToggled, devs[i])
#            bootcb.set_active((num == 0 and not onboot)
#                               or onboot == "yes")
            align.add(bootcb)

            devbox.pack_start(align, gtk.FALSE)

            devbox.pack_start(gtk.HSeparator(), gtk.FALSE, padding=3)

            options = [(("IP Address"), "ipaddr"),
                       (("Netmask"),    "netmask"),
                       (("Network"),    "network"),
                       (("Broadcast"),  "broadcast")]
            ipTable = gtk.Table(len(options), 2)
            # this is the iptable used for DNS, et. al
            self.ipTable = gtk.Table(len(options), 2)

#            DHCPcb.connect("toggled", self.DHCPtoggled, (devs[i], ipTable))
#            bootproto = devs[i].get("bootproto")
            # go ahead and set up DHCP on the first device
#            DHCPcb.set_active((num == 0 and not bootproto) or
#                              bootproto == "dhcp")

#            num = num + 1

#            forward = lambda widget, box=box: box.focus(DIR_TAB_FORWARD)

            for t in range(len(options)):
                label = gtk.Label("%s:" %(options[t][0],))
                label.set_alignment(0.0, 0.5)
                ipTable.attach(label, 0, 1, t, t+1, gtk.FILL, 0, 10)
                entry = gtk.Entry(15)
          # entry.set_usize(gdk_char_width(entry.get_style().font, '0')*15, -1)
                entry.set_size_request(7 * 15, -1)
#                entry.connect("activate", forward)

#                entry.set_text(devs[i].get(options[t][1]))
                options[t] = entry
                ipTable.attach(entry, 1, 2, t, t+1, 0, gtk.FILL|gtk.EXPAND)

#            for t in range(len(options)):
#                if t == 0 or t == 1:
#                    options[t].connect("changed", self.calcNWBC,
#                                       (devs[i],) + tuple(options))

#            options[0].ipCalcNMHandler = None

#            self.focusOutNM(None, None, (devs[i],) + tuple(options))

##             # add event handlers for the main IP widget to calcuate the netmask
##             options[0].connect("focus_in_event", self.focusInIP,
##                                (options[0], options[1]))
##             options[0].connect("focus_out_event", self.focusOutIP, options[0])
##             options[1].connect("focus_out_event", self.focusOutNM,
##                                (devs[i],) + tuple(options))
##             options[2].connect("focus_out_event", self.focusOutNW, devs[i])
##             options[3].connect("focus_out_event", self.focusOutBC, devs[i])

            devbox.pack_start(ipTable, gtk.FALSE, gtk.FALSE, 5)

            devbox.show_all()
            notebook.append_page(devbox, gtk.Label(dev))

#            a = GtkAlignment()
#            a.add(GtkHSeparator())
#            a.set(0.0, 0.0, 0.5, 0.5)
#            box.pack_start(a, gtk.FALSE, padding=10)


        options = [("Hostname"), ("Gateway"), ("Primary DNS"),
                   ("Secondary DNS"), ("Ternary DNS")]

        for i in range(len(options)):
            label = gtk.Label("%s:" %(options[i],))
            label.set_alignment(0.0, 0.0)
            self.ipTable.attach(label, 0, 1, i, i+1, gtk.FILL, 0, 10)
            if i == 0:
                options[i] = gtk.Entry()
                options[i].set_size_request(7 * 30, -1)
            else:
                options[i] = gtk.Entry(15)
                options[i].set_size_request(7 * 15, -1)
#            options[i].connect("activate", forward)
            align = gtk.Alignment(0, 0.5)
            align.add(options[i])
            self.ipTable.attach(align, 1, 2, i, i+1, gtk.FILL, 0)
        self.ipTable.set_row_spacing(0, 5)

        self.hostname = options[0]

        # bring over the value from the loader
#        if(self.network.hostname != "localhost.localdomain"):
#            self.hostname.set_text(self.network.hostname)

        self.gw = options[1]
#        self.gw.set_text(self.network.gateway)

        self.ns = options[2]
#        self.ns.set_text(self.network.primaryNS)

        self.ns2 = options[3]
#        self.ns2.set_text(self.network.secondaryNS)

        self.ns3 = options[4]
#        self.ns3.set_text(self.network.ternaryNS)
        box.pack_start(self.ipTable, gtk.FALSE, gtk.FALSE, 5)


        return box


    def setupNetwork(self, *args):
        win = os.fork()

        if (not win):
            print "launching internet-druid"
            path = "/usr/sbin/internet-druid"
            os.execv(path, [""])



