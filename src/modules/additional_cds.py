from gtk import *
import string
import gtk
import gobject
import os

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 1000
    moduleName = "Additional CDs"

    def __init__(self):
        print "initializing additional_cd module"
                
    def launch(self):
        os.stat('/etc/sysconfig/rhn/rhn_register')
        self.vbox = gtk.VBox()
        self.vbox.set_usize(400, 200)

        label = gtk.Label("Install additional software")

        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        try:
            p = gtk.gdk.pixbuf_new_from_file("images/boxset_standard.png")
        except:
            pass

        if p:
            pix = gtk.Image()
            pix.set_from_pixbuf(p)
            titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)



        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#cc0000"))
        self.vbox.pack_start(eventBox, FALSE)

#        self.vbox.pack_start(label, FALSE, TRUE, 30)
        a = gtk.Alignment()
        a.add(gtk.HSeparator())
        a.set(0.5, 0.5, 1.0, 1.0)

        self.vbox.pack_start(a, FALSE)

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        label = gtk.Label("If you have additional CDs from the Red Hat Linux box "
                          "set, such as the Red Hat Linux Documentation CD or the "
                          "Linux Applications CD, please insert the disc now and "
                          "click the button below.")
        
        label.set_line_wrap(TRUE)
        label.set_usize(400, -1)
        label.set_alignment(0.0, 0.5)
        internalVBox.pack_start(label, FALSE, TRUE)

        launchButton = gtk.Button("Install additional software")
        a = gtk.Alignment()
        a.add(launchButton)            
        a.set(0.3, 0.0, 0.3, 0.5)

#            eventBox = gtk.EventBox()
#            eventBox.add(a)
#            eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("#0000BB"))

        internalVBox.pack_start(a, gtk.FALSE, padding=10)
#            internalVBox.pack_start(eventBox, gtk.FALSE, padding=10)

        launchButton.connect("clicked", self.autorun)

        eventBox = gtk.EventBox()
        eventBox.add(internalVBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#EEEEEE"))
        self.vbox.pack_start(eventBox, TRUE)

        return self.vbox

    def autorun(self, *args):
        mount = os.fork()
        print mount
        if (not mount):
            os.execv("/bin/mount", ["mount", "/dev/cdrom"])
            print "I'm finished"

        print "Here", mount


        pid, status = os.waitpid(mount, 0)
        print "First", pid, status

        if os.WIFEXITED(status) and (os.WEXITSTATUS(status) == 0):
            try:
                os.stat('/mnt/cdrom/autorun')
                print "CD is mounted"

                win = os.fork()
                if not win:
                    print "launching cd installer"
                    os.execv("/mnt/cdrom/autorun", ["autorun"])
            except:
                print "not mounted yet"
                

#        pid, status = os.waitpid(mount, 0)
#        print "First", pid, status
            
#        import time
#        time.sleep(5)

#        pid, status = os.waitpid(mount, 0)
#        print "Second", pid, status, os.WIFEXITED(status)


##         if mount > 0:
##             try:
##                 os.stat('/mnt/cdrom/autorun')

##                 win = os.fork()
##                 if not win:
##                     print "launching cd installer"
##                     os.execv("/mnt/cdrom/autorun", ["autorun"])
##             except:
##                 print "no cdrom mounted"
            
    def write_file(self):
        pass

    def apply(self, notebook):
        print "nothing to do"
        pass
