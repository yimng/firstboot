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

import os
os.environ["PYGTK_DISABLE_THREADS"] = "1"
os.environ["PYGTK_FATAL_EXCEPTIONS"] = "1"
os.environ["GNOME_DISABLE_CRASH_DIALOG"] = "1"

import sys
from gtk import *
from gtk import _root_window
#from flags import flags
import GDK
import gdkpixbuf

splashwindow = None

hpane = GtkHPaned()
moduleList = []
moduleDict = {}
count = 2
asd = 4

def showWindow():
##     #set the background to a dark gray
##     if flags.setupFilesystems:
##         path = ("/usr/X11R6/bin/xsetroot",)
##         args = ("-solid", "gray45")

##         child = os.fork ()
##         if (child == 0):
##             os.execv (path[0], path + args)
##         try:
##             pid, status = os.waitpid(child, 0)
##         except OSError, (errno, msg):
##             print __name__, "waitpid:", msg

    root = _root_window ()
    cursor = cursor_new (GDK.LEFT_PTR)
    root.set_cursor (cursor)

    def load_image(file):
        try:
            p = gdkpixbuf.new_from_file(file)
        except:
            try:
                p = gdkpixbuf.new_from_file("" + file)
            except:
                p = None
                print "Unable to load", file

        return p

    global splashwindow
    
    width = screen_width()
    p = None

    def ok(self, *args):
        #win = GtkWindow()
        #win.set_title("popup")
        #win.show_all()
  	ks = os.fork()
	if (not ks):
	    path = '/usr/sbin/ksconfig'
	    os.execv(path, [])
            print "launching"


    win = GtkWindow()
    win.set_usize(800, 600)
    mainVBox = GtkVBox()
    stepList = GtkCList()
    stepList.append(["Language"])
#    hpane = GtkHPaned()
    hpane.set_position(200)
    hpane.add1(stepList)

    notebook = GtkNotebook()

    path = ('modules/')
    files = os.listdir(path)
    print files
    list = []

    for file in files:
        if file[0] == '.':
            continue
        if file[-3:] != ".py":
            continue
        print "appending ", file
        list.append(file[:-3])

    print list

    for module in list:
#        print sys.path
        sys.path.append('./modules')
        cmd = "import %s\nif %s.__dict__.has_key('childWindow'): obj = %s.childWindow()" % (module, module, module)
        exec(cmd)
        print "runPriority for ", module, "is ", obj.runPriority
        moduleDict[int(obj.runPriority)] = obj
#        moduleList.append(obj)


    tmpList = moduleDict.keys()
    tmpList.sort()
    print tmpList

    for module in tmpList:
        moduleList.append(moduleDict[module])

    asd = asd + 33
    print asd

    print moduleList
    mod = moduleList[0]
    box = mod.launch()

    print count    
    count = 130
    print count    

    hpane.add2(box)
    
    bb = GtkHButtonBox()
    bb.set_layout(BUTTONBOX_END)
    backButton = GtkButton("Back")
    nextButton = GtkButton("Next")
    nextButton.connect('clicked', okClicked)
    bb.pack_start(backButton)
    bb.pack_start(nextButton)


    mainVBox.pack_start(hpane)
    mainVBox.pack_start(bb, FALSE, 20)
    win.add(mainVBox)

    win.show_all()
                        
    mainloop()

def okClicked(self, *args):
    hpane.children()[1].destroy()
    box = moduleList[count].launch()
    count = count + 1
    hpane.add2(box)
    hpane.show_all()

def splashScreenPop():
    global splashwindow
    if splashwindow:
        splashwindow.destroy ()
