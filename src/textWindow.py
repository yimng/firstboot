#!/usr/bin/python

from snack import *
import os

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")


class TextWindow:
    def __call__(self, screen):
        toolList = [(_("Authentication"), ("/usr/sbin/authconfig")),
                    (_("Firewall configuration "), ("/usr/bin/redhat-config-securitylevel-tui")),
                    (_("Keyboard configuration "), ("/usr/bin/redhat-config-keyboard --text")),
                    (_("Mouse configuration "), ("/usr/bin/redhat-config-mouse --text")),
                    (_("Network configuration "), ("/usr/sbin/netconfig")),
                    (_("Printer configuration "), ("/usr/sbin/printconf-tui")),
                    (_("System services "), ("/usr/sbin/ntsysv")),
                    (_("Sound card configuration "), ("/usr/sbin/sndconfig")),
                    (_("Timezone configuration "), ("/usr/sbin/timeconfig"))]

        bb = ButtonBar(screen, [_("Run Tool"), _("Exit")])

        textbox = TextboxReflowed(50, _("Select the item that you wish to modify "))
        self.listbox = Listbox(8, scroll=1, returnExit=0)

        for name, tool in toolList:
            self.listbox.append(name, tool)

        gridForm = GridFormHelp(screen, _("Setup Agent"), "", 1, 4)
        gridForm.add(textbox, 0, 0)
        gridForm.add(self.listbox, 0, 1, padding = (0, 1, 0, 1))
        gridForm.add(bb, 0, 3, growx = 1)

        #Set a timeout limit so that firstboot won't hang around forever on headless machines
        gridForm.setTimer(50000)

        answer = gridForm.runOnce()

        if answer == "TIMER":
            #We've reached the timeout limit.  Let's return -1
            return -1

        button = bb.buttonPressed(answer)

        if button == "exit":
            return -1
        else:
            #They've selected to run a config tool.  Lauch it now
            choice = self.listbox.current()
            os.system(choice)
            return 0
        
