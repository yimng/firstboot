#
# splashscreen.py: a quick splashscreen window that displays during ipl
#
# Matt Wilson <msw@redhat.com>
#
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
from gtk import *
from gtk import _root_window
import GDK
import gdkpixbuf

class mainWindow:
    def __init__(self):
        self.hpane = GtkHPaned()
        self.moduleList = []
        self.moduleDict = {}
        self.moduleIter = 0
        self.usedModuleList = []

        root = _root_window ()
        cursor = cursor_new (GDK.LEFT_PTR)
        root.set_cursor (cursor)

        width = screen_width()
        p = None

        
        win = GtkWindow()
        win.set_usize(800, 600)
        mainVBox = GtkVBox()
        self.stepList = GtkCList()
        self.hpane.set_position(200)
        self.hpane.add1(self.stepList)

        self.notebook = GtkNotebook()

        path = ('modules/')
        files = os.listdir(path)
        list = []

        for file in files:
            if file[0] == '.':
                continue
            if file[-3:] != ".py":
                continue
            list.append(file[:-3])

        print list

        for module in list:
            sys.path.append('./modules')
            cmd = "import %s\nif %s.__dict__.has_key('childWindow'): obj = %s.childWindow()" % (module, module, module)
            exec(cmd)
            self.moduleDict[int(obj.runPriority)] = obj


            self.stepList.append([string.capitalize(module)])


        tmpList = self.moduleDict.keys()
        tmpList.sort()
        print tmpList

        for module in tmpList:
            self.moduleList.append(self.moduleDict[module])


        mod = self.moduleList[0]
        box = mod.launch()

        print self.moduleIter
        self.moduleIter = self.moduleIter + 1
        print self.moduleIter

#        self.hpane.add2(box)
        self.hpane.add2(self.notebook)
        
        self.notebook.append_page(box, GtkLabel("foo"))
    
        bb = GtkHButtonBox()
        bb.set_layout(BUTTONBOX_END)
        backButton = GtkButton("Back")
        backButton.connect('clicked', self.backClicked)
        nextButton = GtkButton("Next")
        nextButton.connect('clicked', self.okClicked)
        bb.pack_start(backButton)
        bb.pack_start(nextButton)

        mainVBox.pack_start(self.hpane)
        mainVBox.pack_start(bb, FALSE, 20)
        win.add(mainVBox)
        win.show_all()
        mainloop()

    def okClicked(self, *args):
        self.usedModuleList.append(self.hpane.children()[1])
#        print self.usedModuleList
        self.hpane.remove(self.hpane.children()[1])       
        box = self.moduleList[self.moduleIter].launch()
        self.moduleIter = self.moduleIter + 1
        self.hpane.add2(box)
        self.hpane.show_all()

    def backClicked(self, *args):
#        print "going back, list is", self.usedModuleList
        self.hpane.children()[1].destroy()
#        self.hpane.children()[1].hide()
        self.moduleIter = self.moduleIter - 1
        self.hpane.add2(self.usedModuleList.pop())
        self.hpane.show_all()
