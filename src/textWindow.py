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
        t = TextboxReflowed(40, 
                _("Some text for firstboot here.  Do you wish to run firstboot now?"))

        g = GridFormHelp(screen, _("Red Hat Setup Agent"), "kbdtype", 1, 4)
        g.add(t, 0, 0)
        g.add(bb, 0, 3, growx = 1)

        g.setTimer(20000)
        
        rc = g.runOnce()

        button = bb.buttonPressed(rc)

        if button == "yes":
            return 0
        else:
            return -1

