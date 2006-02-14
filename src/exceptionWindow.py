## exceptionWindow.py - the UI to display traceback information
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

import gtk
import time

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")

class ExceptionWindow:
    def __init__ (self, module, traceback):
        win = gtk.Dialog()
        win.set_size_request(400, 300)

        self.okButton = win.add_button('gtk-ok', 0)
        self.okButton.connect("clicked", self.destroy)

        text_scroll = gtk.ScrolledWindow()
        text_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        text_scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        
        text_view = gtk.TextView()
        text_view.set_editable(False)
        text_buf = gtk.TextBuffer(None)
        text_scroll.add(text_view)

        label = gtk.Label(_("An error has occurred in the %s module." % module.moduleName))
        label.set_alignment(0.0, 0.5)

        path = "/root/firstboot.%s" % time.time()

        explanation = (_("Since there is a problem with the %s module, \n"
                     "Red Hat Setup Agent will not load this module and \n"
                     "will attempt to run the remaining modules." % module.moduleName))

        bugzilla = (_("Please file a bug against 'firstboot' in the Red Hat \n"
                      "bug tracking system at http://www.redhat.com/bugzilla. \n"
                      "A copy of the debug output has been saved to %s \n"
                      "Be sure to attach that file to the bug report. \n" %path))

        text = traceback + "\n\n" + explanation + "\n\n" + bugzilla

        text_buf.set_text(text)
        text_view.set_buffer(text_buf)

        win.vbox.pack_start(label, False)
        win.vbox.pack_start(text_scroll, True)

        try:
            fd = open(path, "w")
            fd.write(traceback)
            fd.close()
        except:
            pass
        
        win.show_all()
        win.run()
        win.destroy()

    def destroy(self, *args):
        #Ok, we've displayed the traceback.  Return 1 so firstboot can go to the next screen
        #and try to complete the other steps successfully
        return 1
