#!/usr/bin/python

from gtk import *
import string
import gdkpixbuf
from socket import gethostname
#from socket import gethostbyname

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 110
    moduleName = "Network check"

    def __init__(self):
        print "initializing network check module"
        self.netDevs = self.networkDevices()
                
    def launch(self):
        network = self.networkAvailable()
        print network

        if network:
            print "networking already setup"
            return
        else:
            print "set up networking now"

            self.vbox = GtkVBox(FALSE)
            hbox = GtkHBox(FALSE, 10)
            label = GtkLabel("A network connection was not detected.  A network connection "
                             "is necessary for registering with RHN and for using up2date "
                             "to update your system.\n\n ")
            label.set_line_wrap(TRUE)
            label.set_usize(500, -1)
            label.set_alignment(0.0, 0.5)

            p = None
            try:
                p = gdkpixbuf.new_from_file("images/networking.png")
            except:
                pass

            if p:
                pix = apply (GtkPixmap, p.render_pixmap_and_mask())
                align = GtkAlignment()
                align.add(pix)
                align.set(0.0, 0.0, 0.0, 0.0)
                hbox.pack_start(align, FALSE, TRUE, 0)


            hbox.pack_start(label, FALSE, TRUE)

            self.vbox.pack_start(hbox, FALSE, TRUE)
#            self.vbox.pack_start(label, FALSE, TRUE, 30)
            label = GtkLabel("Would you like to set up networking now?")
            label.set_line_wrap(TRUE)
            label.set_alignment(0.1, 0.5)
            self.vbox.pack_start(label, FALSE, TRUE)
#            return self.vbox

            radioVbox = GtkVBox()
            yesRadio = GtkRadioButton(None, "Yes")
            noRadio = GtkRadioButton(yesRadio, "No")
            radioVbox.pack_start(yesRadio, FALSE)
            radioVbox.pack_start(noRadio, FALSE)
            a = GtkAlignment()
            a.add(radioVbox)
            a.set(0.2, 0.5, 0.5, 1.0)
            self.vbox.pack_start(a, FALSE, TRUE)


            notebook = GtkNotebook()
#            self.vbox.pack_start(notebook, FALSE, FALSE)
            align = GtkAlignment(0.0, 0.5, 0.3, 1.0)
            align.add(notebook)
            self.vbox.pack_start(align, FALSE, FALSE)

            for dev in self.netDevs:
                devbox = GtkVBox()
                align = GtkAlignment()
                DHCPcb = GtkCheckButton(("Configure using DHCP"))

                align.add(DHCPcb)
                devbox.pack_start(align, FALSE)

                align = GtkAlignment()
                bootcb = GtkCheckButton(("Activate on boot"))
    #            onboot = devs[i].get("onboot")
    #	    bootcb.connect("toggled", self.onBootToggled, devs[i])
    #            bootcb.set_active((num == 0 and not onboot)
    #                               or onboot == "yes")
                align.add(bootcb)

                devbox.pack_start(align, FALSE)

                devbox.pack_start(GtkHSeparator(), FALSE, padding=3)

                options = [(("IP Address"), "ipaddr"),
                           (("Netmask"),    "netmask"),
                           (("Network"),    "network"),
                           (("Broadcast"),  "broadcast")]
                ipTable = GtkTable(len(options), 2)
                # this is the iptable used for DNS, et. al
                self.ipTable = GtkTable(len(options), 2)

    #            DHCPcb.connect("toggled", self.DHCPtoggled, (devs[i], ipTable))
    #            bootproto = devs[i].get("bootproto")
                # go ahead and set up DHCP on the first device
    #            DHCPcb.set_active((num == 0 and not bootproto) or
    #                              bootproto == "dhcp")

    #            num = num + 1

    #            forward = lambda widget, box=box: box.focus(DIR_TAB_FORWARD)

                for t in range(len(options)):
                    label = GtkLabel("%s:" %(options[t][0],))
                    label.set_alignment(0.0, 0.5)
                    ipTable.attach(label, 0, 1, t, t+1, FILL, 0, 10)
                    entry = GtkEntry(15)
              # entry.set_usize(gdk_char_width(entry.get_style().font, '0')*15, -1)
                    entry.set_usize(7 * 15, -1)
    #                entry.connect("activate", forward)

    #                entry.set_text(devs[i].get(options[t][1]))
                    options[t] = entry
                    ipTable.attach(entry, 1, 2, t, t+1, 0, FILL|EXPAND)

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

                devbox.pack_start(ipTable, FALSE, FALSE, 5)

                devbox.show_all()
                notebook.append_page(devbox, GtkLabel(dev))

#            a = GtkAlignment()
#            a.add(GtkHSeparator())
#            a.set(0.0, 0.0, 0.5, 0.5)
#            self.vbox.pack_start(a, FALSE, padding=10)


        options = [("Hostname"), ("Gateway"), ("Primary DNS"),
                   ("Secondary DNS"), ("Ternary DNS")]

        for i in range(len(options)):
            label = GtkLabel("%s:" %(options[i],))
            label.set_alignment(0.0, 0.0)
            self.ipTable.attach(label, 0, 1, i, i+1, FILL, 0, 10)
            if i == 0:
                options[i] = GtkEntry()
                options[i].set_usize(7 * 30, -1)
            else:
                options[i] = GtkEntry(15)
                options[i].set_usize(7 * 15, -1)
#            options[i].connect("activate", forward)
            align = GtkAlignment(0, 0.5)
            align.add(options[i])
            self.ipTable.attach(align, 1, 2, i, i+1, FILL, 0)
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
        self.vbox.pack_start(self.ipTable, FALSE, FALSE, 5)




        return self.vbox

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
        print netdevices
        return netdevices        


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

    def write_file(self):
        pass

    def apply(self):
        print "applying template changes"
        pass


