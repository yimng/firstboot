from gtk import *
import string
import gtk
import gobject
import os
import sys
import functions
sys.path.append('/usr/share/redhat-config-soundcard')
import soundcardBackend

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext


class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 100
    moduleName = "Configure hardware"

    def __init__(self, doDebug = None):
        self.doDebug = doDebug
        if doDebug:
            print "initializing hardware module"
                
    def launch(self):
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        label = gtk.Label("Configure the hardware on your system")
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("hwbrowser.png")
        print pix
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

        self.table = gtk.Table(3, 4)
        self.table.set_col_spacings(6)
        self.table.set_row_spacings(6)
        self.vbox.pack_start(self.table)

        pix = functions.imageFromFile("networking.png")
        self.table.attach(pix, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Networking:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, 1, 2, gtk.FILL, gtk.FILL)

        pix = functions.imageFromFile("display.png")
        self.table.attach(pix, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Display:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, 2, 3, gtk.FILL, gtk.FILL)

        pix = functions.imageFromFile("printer.png")
        self.table.attach(pix, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Printers:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, 3, 4, gtk.FILL, gtk.FILL)


        self.configureSoundcard()
        
#        pix = self.imageFromFile("splash.png")
#        self.vbox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)


#        label = gtk.Label("Welcome message goes here")
#        self.vbox.pack_start(label, TRUE)

#        self.hbox = gtk.HBox()
#        self.hbox.pack_start(self.splash, gtk.FALSE)
#        self.hbox.pack_start(label, gtk.TRUE)
#        self.vbox.pack_start(self.hbox, gtk.TRUE)

            
        return self.vbox, eventBox

    def apply(self, notebook):
        return 1

    def configureSoundcard(self):
        self.soundcardBackend = soundcardBackend.soundcardBackend()
        cards = self.soundcardBackend.probeCards()
        if not cards:
            return
        print cards
        self.device, self.module, self.description = self.soundcardBackend.getData(cards[0])

        pix = functions.imageFromFile("multimedia.png")
        self.table.attach(pix, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Sound card:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
        self.soundcard_label = gtk.Label(_("Sound card:"))
        self.soundcard_label.set_alignment(0.0, 0.5)
        self.table.attach(self.soundcard_label, 2, 3, 0, 1, gtk.FILL, gtk.FILL)
        self.soundcard_button = gtk.Button(_("Configure..."))
        self.soundcard_button.connect("clicked", self.soundcard_button_clicked)
        self.table.attach(self.soundcard_button, 3, 4, 0, 1, gtk.EXPAND, gtk.SHRINK)


        self.device, self.module, self.description = self.soundcardBackend.getData(cards[0])
        maker, model = string.split(self.description, "|")
        self.soundcard_label.set_text(model)

        
    def soundcard_button_clicked(self, *args):
        win = os.fork()

        if (not win):
            if self.doDebug:
                print "launching redhat-config-soundcard"
            path = "/usr/share/redhat-config-soundcard/redhat-config-soundcard.py"
            os.execv(path, [""])

