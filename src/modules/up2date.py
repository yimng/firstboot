import string
import gtk
import gobject
import os
import functions
import time

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 130
    moduleName = (_("Update Agent"))
                
    def launch(self, doDebug=None):
        if doDebug:
            print "launching up2date module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        msg = (_("Red Hat Update Agent"))
        label = gtk.Label("")
        label.set_alignment(0.4, 0.5)
        label.set_markup("<span size='x-large'>%s</span>" % msg)
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("up2date.png")
        if pix:
            titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
        self.vbox.pack_start(eventBox, gtk.FALSE)

        a = gtk.Alignment()
        a.add(gtk.HSeparator())
        a.set(0.5, 0.5, 1.0, 1.0)

        self.vbox.pack_start(a, gtk.FALSE)

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        label = gtk.Label(_("The Red Hat Update Agent will register your machine with "
                            "Red Hat Network so that you can receive the latest software "
                            "packages directly from Red Hat.  Using this tool will allow you "
                            "to always have the most up-to-date Red Hat Linux system "
                            "with all the security patches, bug fixes, and software "
                            "package enhancements. \n\n"
                            "If you purchased this product, you are entitled to a free trial of Red "
                            "Hat Network Basic Service. To access the free trial, please refer to the "
                            "product activation card found in the box for detailed instructions. \n\n"
                            "If you did not purchase this product, visit http://rhn.redhat.com for "
                            "more information or to subscribe to Red Hat Network Basic Service. \n\n"))

        label.set_line_wrap(gtk.TRUE)
        label.set_size_request(400, -1)
        label.set_alignment(0.0, 0.5)
        internalVBox.pack_start(label, gtk.FALSE, gtk.TRUE)

        radioBox = gtk.VBox()

        self.radioYes = gtk.RadioButton(None, _("Yes, I would like to register with Red Hat Network"))
        radioNo = gtk.RadioButton(self.radioYes, _("No, I do not want to register my system."))

        radioBox.pack_start(self.radioYes, gtk.FALSE)
        radioBox.pack_start(radioNo, gtk.FALSE)

        if doDebug:
            radioNo.set_active(gtk.TRUE)

        a = gtk.Alignment()
        a.add(radioBox)
        a.set(0.3, 0.0, 0.3, 0.5)
        internalVBox.pack_start(a, gtk.FALSE, padding=10)

        self.vbox.pack_start(internalVBox, gtk.TRUE)

        return self.vbox, eventBox

    def run_up2date(self, *args):
        #Run rhn_register so they can register with RHN
        pid = self.start_process()

        flag = None
        while not flag:
            while gtk.events_pending():
                gtk.main_iteration_do()

            child_pid, status = os.waitpid(pid, os.WNOHANG)
            
            if child_pid == pid:
                flag = 1
            else:
                time.sleep(0.1)

    def start_process(self):
        path = "/usr/bin/up2date"
        args = [path]

        child = os.fork()

        if not child:
            os.execvp(path, args)
            os._exit(1)
            
        return child

    def apply(self, notebook):
        # If they want to register, then kick off rhn_register.  If not, then pass
        if self.radioYes.get_active() == gtk.TRUE:            
            #We can ping www.redhat.com, so the network is active
            self.run_up2date()
        return 1
            
