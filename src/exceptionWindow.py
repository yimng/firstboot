#!/usr/bin/python2.2

import gtk
import os
import time

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

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
        text_view.set_editable(gtk.FALSE)
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

        win.vbox.pack_start(label, gtk.FALSE)
        win.vbox.pack_start(text_scroll, gtk.TRUE)

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
