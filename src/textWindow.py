#!/usr/bin/python

from snack import *

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")


class TextWindow:
    def __call__(self, screen):
        bb = ButtonBar(screen, [_("Yes"), _("No")])
        t = TextboxReflowed(50, 
                _("The Red Hat Setup Agent can assist you in configuring your machine "
                  "by guiding you through a series of steps.  Setup Agent requires the X Window System "
                  "to run.  \n\n"
                  "If you wish to run the Setup Agent, "
                  "please choose \"Yes\".  If you choose \"No\", the system will continue booting and "
                  "you will never see this message again.  Do you wish to run the Setup Agent now?"))

        g = GridFormHelp(screen, _("Red Hat Setup Agent"), "kbdtype", 1, 4)
        g.add(t, 0, 0)
        g.add(bb, 0, 3, growx = 1)

        g.setTimer(25000)
        
        rc = g.runOnce()

        button = bb.buttonPressed(rc)

        if button == "yes":
            return 0
        else:
            return -1

