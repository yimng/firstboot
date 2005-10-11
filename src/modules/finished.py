from gtk import *
import string
import gtk
import gobject
import os
import sys
import functions
import glob

##
## I18N
## 
from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("firstboot")
class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 500
    moduleName = (_("Finish Setup"))

    def launch(self, doDebug = None):
        if doDebug:
            print "initializing finished module"

        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        title_pix = functions.imageFromFile("workstation.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        self.txt = _("Your system is now set up and ready to use.  Please "
                            "click the \"Next\" button in the lower right corner to continue.")

        self.post_txt = _("Please click the \"Next\" button in the lower right corner to continue.")
        self.label = gtk.Label(self.txt)
            
        self.label.set_line_wrap(True)
        self.label.set_alignment(0.0, 0.5)
        self.label.set_size_request(500, -1)
        internalVBox.pack_start(self.label, False, True)
        
        self.vbox.pack_start(internalVBox, False, 5)
        pix = functions.ditheredImageFromFile("splash-small.png")
        self.vbox.pack_start(pix, True, True, 5)

        return self.vbox, title_pix, self.moduleName

    def updatePage(self):
        if os.access("/var/tmp/firstboot", os.R_OK):
            files = glob.glob("/var/tmp/firstboot/*_firstboot_finish_message")
            # the file names are in the format 37_firstboot_finish_message with the
            # number indicating a sorting priority, so sort them...
            files.sort()
            for file in files:
                fd = open(file, "r")
                new_txt = fd.read()
                # markcom doesnt want the "you finished" message shown if there
                # are any other errors
                self.txt = "" + "\n"
                self.txt = self.txt + new_txt
                self.txt = self.txt + "\n" + self.post_txt

            # dont need these files anymore
            for file in files:
                os.unlink(file)
            
        self.label.set_text(self.txt)

    def apply(self, notebook):
        return 0
