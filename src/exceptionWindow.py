#!/usr/bin/python2.2

import gtk

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class ExceptionWindow:
    def __init__ (self, module, text):
        win = gtk.Dialog()
        win.set_size_request(400, 300)

        self.okButton = win.add_button('gtk-quit', 0)
        self.okButton.connect("clicked", self.destroy)

        text_scroll = gtk.ScrolledWindow()
        text_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        text_scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        
        text_view = gtk.TextView()
        text_view.set_editable(gtk.FALSE)
        text_buf = gtk.TextBuffer(None)
        text_scroll.add(text_view)

        label = gtk.Label(_("An error has occured in module %s." % module.moduleName))
        label.set_alignment(0.0, 0.5)
        text_buf.set_text(text)
        text_view.set_buffer(text_buf)

        win.vbox.pack_start(label, gtk.FALSE)
        win.vbox.pack_start(text_scroll, gtk.TRUE)
        
        win.show_all()
        win.run()
        win.destroy()

    def destroy(self, *args):
        gtk.mainquit()
