from gtk import *
import string
import gtk
import gobject
import os
import sys
import functions
sys.path.append('/usr/share/redhat-config-soundcard')
sys.path.append('/usr/share/redhat-config-keyboard')
import soundcardBackend
import rhpl.keyboard as keyboard

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
        if pix:
            titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

        self.table = gtk.Table(3, 4)
        self.table.set_border_width(6)
        self.table.set_col_spacings(6)
        self.table.set_row_spacings(6)
        self.vbox.pack_start(self.table)

        self.table_row = 0

        self.configureKeyboard()
        self.configureMouse()
        self.configureSoundcard()
        self.configureNetworking()
        self.configureDisplay()
        self.configurePrinters()

        return self.vbox, eventBox

    def apply(self, notebook):
        return 1

    def configureKeyboard(self):
        kbd = keyboard.Keyboard()
        kbd.read()
        layout, keymap, keys, variant = kbd.modelDict[kbd.get()]
        
        
        pix = functions.imageFromFile("keyboard.png")
        if pix:
            self.table.attach(pix, 0, 1, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Keyboard Map:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.keyboard_label = gtk.Label(layout)
        self.keyboard_label.set_alignment(0.0, 0.5)
        self.table.attach(self.keyboard_label, 2, 3, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.keyboard_button = gtk.Button(_("Configure..."))
        self.keyboard_button.connect("clicked", self.keyboard_button_clicked)
        self.table.attach(self.keyboard_button, 3, 4, self.table_row, self.table_row + 1, gtk.EXPAND, gtk.SHRINK)
        self.table_row = self.table_row + 1

    def configureMouse(self):
        pix = functions.imageFromFile("mouse.png")
        if pix:
            self.table.attach(pix, 0, 1, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Mouse:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.table_row = self.table_row + 1

    def configureSoundcard(self):
        self.soundcardBackend = soundcardBackend.soundcardBackend()
        cards = self.soundcardBackend.probeCards()
        if not cards:
            return
        self.device, self.module, self.description = self.soundcardBackend.getData(cards[0])

        pix = functions.imageFromFile("multimedia.png")
        if pix:
            self.table.attach(pix, 0, 1, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Sound card:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.soundcard_label = gtk.Label(_(""))
        self.soundcard_label.set_alignment(0.0, 0.5)
        self.table.attach(self.soundcard_label, 2, 3, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.soundcard_button = gtk.Button(_("Configure..."))
        self.soundcard_button.connect("clicked", self.soundcard_button_clicked)
        self.table.attach(self.soundcard_button, 3, 4, self.table_row, self.table_row + 1, gtk.EXPAND, gtk.SHRINK)
        self.table_row = self.table_row + 1

        self.device, self.module, self.description = self.soundcardBackend.getData(cards[0])
        maker, model = string.split(self.description, "|")
        self.soundcard_label.set_text(model)

    def configureNetworking(self):
        pix = functions.imageFromFile("networking.png")
        if pix:
            self.table.attach(pix, 0, 1, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Networking:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.table_row = self.table_row + 1

    def configureDisplay(self):
        pix = functions.imageFromFile("display.png")
        if pix:
            self.table.attach(pix, 0, 1, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Display:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.table_row = self.table_row + 1

    def configurePrinters(self):
        pix = functions.imageFromFile("printer.png")
        if pix:
            self.table.attach(pix, 0, 1, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        label = gtk.Label(_("Printers:"))
        label.set_alignment(0.0, 0.5)
        self.table.attach(label, 1, 2, self.table_row, self.table_row + 1, gtk.FILL, gtk.FILL)
        self.table_row = self.table_row + 1

        
    ############Event Handlers#############
    def keyboard_button_clicked(self, *args):
        pass
#        win = os.fork()

##         if (not win):
##             if self.doDebug:
##                 print "launching redhat-config-keyboard"
##             path = "/usr/share/redhat-config-keyboard/redhat-config-keyboard.py"
##             os.execv(path, [""])
#         import keyboard_gui
#         app = keyboard_gui.childWindow()
#         app.stand_alone()

        
    def soundcard_button_clicked(self, *args):
        win = os.fork()

        if (not win):
            if self.doDebug:
                print "launching redhat-config-soundcard"
            path = "/usr/share/redhat-config-soundcard/redhat-config-soundcard.py"
            os.execv(path, [""])
