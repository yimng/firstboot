## textWindow.py - the code for firstboot TUI
##
## Copyright (C) 2002, 2003 Red Hat, Inc.
## Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from snack import *
import os
from constants_text import *

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")


class TextWindow:
    def __call__(self, screen):
        toolList = [(_("Authentication"), ("/usr/sbin/authconfig-tui"), ("")),
                    (_("Firewall configuration"), ("/usr/bin/system-config-securitylevel-tui"), ("")),
                    (_("Keyboard configuration"), ("/usr/bin/system-config-keyboard"), ("--text")),
                    (_("Network configuration"), ("/usr/sbin/netconfig"), ("")),
                    (_("Printer configuration"), ("/usr/sbin/printconf-tui"), ("")),
                    (_("System services"), ("/usr/sbin/ntsysv"), ("")),
                    (_("Timezone configuration"), ("/usr/sbin/timeconfig"), (""))]

        bb = ButtonBar(screen, [_("Run Tool"), TEXT_EXIT_BUTTON])

        textbox = TextboxReflowed(50, _("Select the item that you wish to modify "))
        self.listbox = Listbox(8, scroll=1, returnExit=0)

        for name, tool, args in toolList:
            # Make sure we can access the program before adding it.
            if os.access(tool, os.X_OK):
                self.listbox.append(name, string.join([tool, args]))

        gridForm = GridFormHelp(screen, _("Setup Agent"), "", 1, 4)
        gridForm.add(textbox, 0, 0)
        gridForm.add(self.listbox, 0, 1, padding = (0, 1, 0, 1))
        gridForm.add(bb, 0, 3, growx = 1)

        #Set a timeout limit so that firstboot won't hang around forever on headless machines
        gridForm.setTimer(50000)

        answer = gridForm.runOnce()

        if answer == "TIMER":
            #We've reached the timeout limit.  Let's return -1
            return -2

        button = bb.buttonPressed(answer)

        if button == TEXT_EXIT_CHECK:
            return -1
        else:
            #They've selected to run a config tool.  Lauch it now
            choice = self.listbox.current()
            os.system(choice)
            return 0
        
