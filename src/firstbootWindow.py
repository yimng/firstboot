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
#        self.hpane = gtk.HPaned()
        self.mainHBox = gtk.HBox()
        self.moduleList = []
        self.moduleDict = {}
        self.usedModuleList = []

#        root = _root_window ()
#        cursor = cursor_new (GDK.LEFT_PTR)
#        root.set_cursor (cursor)

#        width = screen_width()
        p = None
        
        win = gtk.Window()
        win.set_usize(800, 600)
        win.set_policy(gtk.FALSE, gtk.FALSE, gtk.FALSE)
        mainVBox = gtk.VBox()

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
#            sys.path.append('./modules')
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

        for module in tmpList:
            self.moduleList.append(self.moduleDict[module])
#            self.stepList.append([self.moduleDict[module].moduleName])

        for module in self.moduleList:
            box = module.launch()
            if box:
                self.notebook.append_page(box, gtk.Label(" "))

        label = gtk.Label("Hello")
        label.set_usize(200, -1)
#        self.hpane.add1(label)
        self.mainHBox.pack_start(label, gtk.FALSE)

#        self.hpane.add2(self.notebook)
        self.mainHBox.pack_start(self.notebook, gtk.TRUE)

        bb = gtk.HButtonBox()
        bb.set_layout(gtk.BUTTONBOX_END)
        backButton = gtk.Button("Back")
        backButton.connect('clicked', self.backClicked)
        nextButton = gtk.Button("Next")
        nextButton.connect('clicked', self.okClicked)
        group = gtk.AccelGroup()
#        nextButton.add_accelerator('clicked', group, GDK.F12,
#                                   GDK.RELEASE_MASK, 0)
#        backButton.add_accelerator('clicked', group, GDK.F11,
#                                   GDK.RELEASE_MASK, 0)
        win.add_accel_group(group)
        bb.pack_start(backButton)
        bb.pack_start(nextButton)

#        self.hpane.handle_size(0)
#        mainVBox.pack_start(self.hpane)
        mainVBox.pack_start(self.mainHBox)
#        mainVBox.pack_start(self.notebook)
        self.notebook.set_border_width(10)

#        a = GtkAlignment()
#        a.add(GtkHSeparator())
#        a.set(0.0, 0.0, 0.5, 0.5)
#        mainVBox.pack_start(gtk.HSeparator(), gtk.FALSE)

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

        mainVBox.pack_start(bb, gtk.FALSE, padding=10)
        win.add(mainVBox)
        win.show_all()
#        self.notebook.set_page(0)
#        self.stepList.select_row(0, 0)
        gtk.main()

    def okClicked(self, *args):
        module = self.moduleList[self.notebook.get_current_page()]
        #Call the apply method if it exists
        try:
            module.apply()
        except:
            pass
        self.notebook.next_page()
#        self.stepList.select_row(self.notebook.get_current_page(), 0)

    def backClicked(self, *args):
        self.notebook.prev_page()
#        self.stepList.select_row(self.notebook.get_current_page(), 0)

    def selectRow(self, list, row, col, event):
        self.notebook.set_page(row)

