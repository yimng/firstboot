# Copyright 2001 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import string
import os
os.environ["PYGTK_DISABLE_THREADS"] = "1"
os.environ["PYGTK_FATAL_EXCEPTIONS"] = "1"
os.environ["GNOME_DISABLE_CRASH_DIALOG"] = "1"

import sys
import gtk
import gobject

doReconfig = 1

for arg in sys.argv:
    if arg == '--reconfig':
        print "starting reconfig mode"
        doReconfig = 0

sys.argv = sys.argv[:1]

print doReconfig

class firstbootWindow:
    def __init__(self):
        self.mainHBox = gtk.HBox()
        self.moduleList = []
        self.moduleDict = {}
        self.moduleStore = gtk.ListStore(gobject.TYPE_STRING)

#        root = _root_window ()
#        cursor = cursor_new (GDK.LEFT_PTR)
#        root.set_cursor (cursor)

        win = gtk.Window()
        win.set_usize(800, 600)
        win.set_policy(gtk.FALSE, gtk.FALSE, gtk.FALSE)
        mainVBox = gtk.VBox()

        p = None        
        try:
            p = gtk.gdk.pixbuf_new_from_file("images/titlebar.png")
        except:
            pass

        if p:
            pix = gtk.Image()
            pix.set_from_pixbuf(p)
#            mainVBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 0)
        
        self.notebook = gtk.Notebook()
        self.notebook.set_show_tabs(gtk.FALSE)
        self.notebook.set_show_border(gtk.FALSE)

#        path = ('/usr/share/firstboot/modules')
        path = ('/home/devel/bfox/redhat/firstboot/src/modules')
        files = os.listdir(path)
        list = []

        for file in files:
            if file[0] == '.':
                continue
            if file[-3:] != ".py":
                continue
            list.append(file[:-3])

        for module in list:
            print module
#            sys.path.append('/usr/share/firstboot/modules')
            sys.path.append('/home/devel/bfox/redhat/firstboot/src/modules')
            cmd = ("import %s\nif %s.__dict__.has_key('childWindow'):"
                   "obj = %s.childWindow()") % (module, module, module)
            exec(cmd)

            if doReconfig == 1:
                try:
                    if obj.moduleClass == "reconfig":
                        pass
                    else:
                        self.moduleDict[int(obj.runPriority)] = obj
                except:
                    self.moduleDict[int(obj.runPriority)] = obj
                    pass
                
            else:
                self.moduleDict[int(obj.runPriority)] = obj

        tmpList = self.moduleDict.keys()
        tmpList.sort()

        print self.moduleDict
        print tmpList

        for module in tmpList:
            self.moduleList.append(self.moduleDict[module])

            try:
                if self.moduleDict[module].moduleName:
                    print self.moduleDict[module].moduleName
                    iter = self.moduleStore.append()
                    self.moduleStore.set_value(iter, 0, self.moduleDict[module].moduleName)

            except:
                pass

        for module in self.moduleList:
             box = module.launch()
             if box:
                 self.notebook.append_page(box, gtk.Label(" "))

        self.moduleView = gtk.TreeView(self.moduleStore)
#        selection = self.moduleView.get_selection()
#        selection.connect("changed", self.selectRow)

        col = gtk.TreeViewColumn(None, gtk.CellRendererText(), text=0)
        self.moduleView.append_column(col)
        self.moduleView.set_property("headers-visible", gtk.FALSE)
        self.moduleView.set_usize(200, -1)
        self.mainHBox.pack_start(self.moduleView, gtk.FALSE)


#########################################
        self.rightVBox = gtk.VBox()
        self.rightVBox.set_usize(400, 200)

        eventBox = gtk.EventBox()
        self.internalVBox = gtk.VBox()
        self.internalVBox.pack_start(self.notebook, gtk.TRUE)
        eventBox.add(self.internalVBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#EEEEEE"))
        self.rightVBox.pack_start(eventBox, gtk.TRUE)

        a = gtk.Alignment()
        a.add(self.rightVBox)
        a.set(0.5, 0.5, 0.9, 0.9)
        self.mainHBox.pack_start(a, gtk.TRUE)

        self.bb = gtk.HButtonBox()
        self.bb.set_layout(gtk.BUTTONBOX_END)
        self.bb.set_border_width(10)
        self.bb.set_spacing(10)
        self.backButton = gtk.Button(stock='gtk-go-back')
        self.backButton.connect('clicked', self.backClicked)
        self.backButton.set_sensitive(gtk.FALSE)
        self.nextButton = gtk.Button(stock='gtk-go-forward')
        self.finishButton = gtk.Button(stock='gtk-close')
        self.finishButton.connect('clicked', self.finishClicked)
        group = gtk.AccelGroup()
        self.nextButton.connect('clicked', self.okClicked)

        self.internalVBox.pack_start(self.bb, gtk.FALSE, 10)

        #Accelerators aren't currently working in GTK 2.0   Grrrrrrr.
#        self.nextButton.add_accelerator('clicked', group, gtk.keysyms.F12,
#                                   gtk.gdk.RELEASE_MASK, 0)
#        self.backButton.add_accelerator('clicked', group, GDK.F11,
#                                   GDK.RELEASE_MASK, 0)
        win.add_accel_group(group)
        self.bb.pack_start(self.backButton)
        self.bb.pack_start(self.nextButton)

        mainVBox.pack_start(self.mainHBox)

        try:
            p = gtk.gdk.pixbuf_new_from_file("images/bg.png")
        except:
            pass

        if p:
            pix = gtk.Image()
            pix.set_from_pixbuf(p)

        win.realize()
        win.set_app_paintable(gtk.TRUE)

        bgimage = gtk.gdk.Pixmap(win.window, 800, 600, -1)
        gc = bgimage.new_gc ()
        p.render_to_drawable(bgimage, gc, 0, 0, 0, 0, 800, 600, gtk.gdk.RGB_DITHER_MAX, 0, 0)
        win.window.set_back_pixmap (bgimage, gtk.FALSE)
        
        win.add(mainVBox)
        win.show_all()
        gtk.main()

    def selectRow(self, *args):
        print "select Row"

    def finishClicked(self, *args):
        print "exiting"
        
        try:
            module = self.moduleList[self.notebook.get_current_page()]
        except:
            pass

        #Call the apply method if it exists
        try:
            module.apply(self.notebook)
        except:
            print "apply failed"
            pass

        gtk.mainquit()
        print "closing"

    def okClicked(self, *args):
        print self.moduleList
        print "we're leaving page ", self.notebook.get_current_page()
        try:
            module = self.moduleList[self.notebook.get_current_page()]
        except:
            pass

        #Call the apply method if it exists
        try:
            module.apply(self.notebook)
        except:
            pass

        self.notebook.next_page()

        #Check to see if we're on the last page.  
        tmp = self.notebook.get_nth_page(self.notebook.get_current_page() + 1)        
        if not tmp:
            self.bb.remove(self.nextButton)
            self.bb.pack_end(self.finishButton)
            self.bb.show_all()

        self.backButton.set_sensitive(gtk.TRUE)

    def backClicked(self, *args):
        self.notebook.prev_page()
        if self.notebook.get_current_page() == 0:
            self.backButton.set_sensitive(gtk.FALSE)

        print self.bb.children()
        if self.finishButton in self.bb.children():
            self.bb.remove(self.finishButton)
            self.bb.pack_end(self.nextButton)
            self.bb.show_all()

#        self.stepList.select_row(self.notebook.get_current_page(), 0)

    def selectRow(self, list, row, col, event):
        self.notebook.set_page(row)



