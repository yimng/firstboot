#
# Copyright 2001,2002 Red Hat, Inc.
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
import traceback
os.environ["PYGTK_DISABLE_THREADS"] = "1"
os.environ["PYGTK_FATAL_EXCEPTIONS"] = "1"
os.environ["GNOME_DISABLE_CRASH_DIALOG"] = "1"

import sys
import gtk
import gobject
import functions
import firstbootBackend

class firstbootWindow:
    def __init__(self, xserver_pid, wm_pid, doReconfig, doDebug, lowRes):
        self.xserver_pid = xserver_pid
        self.wm_pid = wm_pid
        self.doReconfig = doReconfig
        self.doDebug = doDebug
        self.lowRes = lowRes
        self.mainHBox = gtk.HBox(gtk.FALSE, 10)
        self.moduleList = []
        self.moduleDict = {}

        # Create the initial window and a vbox to fill it with.
        self.win = gtk.Window()
        self.win.connect("destroy", self.destroy)
        self.winHandler = self.win.connect ("key-release-event", self.keyRelease)
        self.win.realize()

        mainVBox = gtk.VBox()
        self.win.add(mainVBox)

        #This isn't debug mode, so jump through some hoops to go into fullscreen/root window mode
        self.win.set_decorated(gtk.FALSE)
        self.win.set_size_request(800, 600)
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.window.property_change ("_NET_WM_WINDOW_TYPE", "ATOM", 32, gtk.gdk.PROP_MODE_REPLACE, ("_NET_WM_WINDOW_TYPE_SPLASH",))

        #Set the background of the window
        pixbuf = functions.pixbufFromFile("bg.png")
        bgimage = gtk.gdk.Pixmap(self.win.window, 800, 600, -1)
        gc = bgimage.new_gc()
        pixbuf.render_to_drawable(bgimage, gc, 0, 0, 0, 0, 800, 600, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)
        self.win.set_app_paintable(gtk.TRUE)
        self.win.window.set_back_pixmap(bgimage, gtk.FALSE)
        self.win.realize()

        if gtk.gdk.screen_width() >= 800:            
            mainVBox.set_size_request(800, 600)
        else:
            mainVBox.set_size_request(gtk.gdk.screen_width(), gtk.gdk.screen_height())
            self.lowRes = 1
            
        # Create the notebook.  We use a ListView to control which page in the
        # notebook is displayed.
        self.notebook = gtk.Notebook()

        if self.doDebug:
            print "starting firstbootWindow", doReconfig, doDebug                    
            path = ('modules/')
            self.notebook.set_show_tabs(gtk.FALSE)
            self.notebook.set_scrollable(gtk.TRUE)
            self.notebook.set_show_border(gtk.FALSE)
        else:
            os.system('/usr/bin/xsri --scale-height=100 --scale-width=100 --set /usr/share/gdm/themes/Bluecurve/lightrays.png')
            path = ('/usr/share/firstboot/modules')
            self.notebook.set_show_tabs(gtk.FALSE)
            self.notebook.set_show_border(gtk.FALSE)

        sys.path.append(path)

#        if not self.lowRes:
#            #Code for an upper title bar like anaconda.  We may turn this on if we get some UI help
#            pix = functions.imageFromFile("firstboot-header.png")
#            if pix:
#                mainVBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 0)
#                pass

        # Generate a list of all of the module files (which becomes the list of
        # all non-hidden files in the directory with extensions other than .py.
        files = os.listdir(path)
        list = []
        for file in files:
            if file[0] == '.':
                continue
            if file[-3:] != ".py":
                continue
            list.append(file[:-3])

        # Import each module, and filter out those
        for module in list:
            cmd = ("import %s\nif %s.__dict__.has_key('childWindow'):"
                   "obj = %s.childWindow()") % (module, module, module)
            exec(cmd)

            # If the module defines a moduleClass, it has to match the mode
            # we're starting up in, otherwise it's always used.  Add it to
            # a dictionary keyed by the module's declared priority.
            if hasattr(obj, "moduleClass"):
                if (self.doReconfig and (obj.moduleClass == "reconfig")):
                    self.moduleDict[int(obj.runPriority)] = obj
                elif (not self.doReconfig and (obj.moduleClass != "reconfig")):
                    self.moduleDict[int(obj.runPriority)] = obj
            else:
                self.moduleDict[int(obj.runPriority)] = obj

        # Get the list of module priorities, sort them to determine a run
	# order, and build a list with the modules in the proper order.
        modulePriorityList = self.moduleDict.keys()
        modulePriorityList.sort()

        self.leftLabelVBox = gtk.VBox()
        self.leftLabelVBox.set_border_width(12)
        
        leftEventBox = gtk.EventBox()
        leftEventBox.add(self.leftLabelVBox)
        leftEventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#7383a3"))

        leftVBox = gtk.VBox()
        leftVBox.pack_start(leftEventBox, gtk.TRUE)

	# Add the modules to the proper lists.
        pages = 0
        for priority in modulePriorityList:
            # Add the module to the list of modules.
            module = self.moduleDict[priority]
            # Launch the module's GUI.
            vbox = None
            eventbox = None

            if self.doDebug:
                try:
                    print "calling", module.moduleName
                    vbox, pix, title = module.launch(self.doDebug)
                except:
                    import exceptionWindow
                    (type, value, tb) = sys.exc_info()
                    list = traceback.format_exception(type, value, tb)
                    text = string.joinfields(list, "")
                    exceptionWindow.ExceptionWindow(module, text)
                    pass                    
            else:
                try:
                    vbox, pix, title = module.launch() 
                except:
                    import exceptionWindow
                    (type, value, tb) = sys.exc_info()
                    list = traceback.format_exception(type, value, tb)
                    text = string.joinfields(list, "")
                    exceptionWindow.ExceptionWindow(module, text)
                    pass
                    continue

            if vbox and title:
                # If it launched, add it to the mdoule list.
                self.moduleList.append(module)

                title_label = gtk.Label("")
                title_label.set_alignment(0.0, 0.5)
                title_label.set_markup("<span foreground='#000000' size='30000' font_family='Helvetica'><b>%s</b></span>" % title)

                titleBox = gtk.HBox()
                titleBox.pack_start(pix, gtk.FALSE)
                titleBox.pack_start(title_label, gtk.TRUE)
                titleBox.set_spacing(8)

                vbox.pack_start(titleBox, gtk.FALSE)
                vbox.reorder_child(titleBox, 0)
                
                if self.lowRes:
                    # If we're in 640x480 mode, remove the title bars
                    vbox.remove(vbox.get_children()[0])

                # If the module has a name, add it to the list of labels
                if hasattr(module, "moduleName"):
                    self.notebook.append_page(vbox, gtk.Label(module.moduleName))
                    hbox = gtk.HBox(gtk.FALSE, 5)
                    pix = functions.imageFromFile("pointer-blank.png")
                    label = gtk.Label("")
                    label.set_markup("<span foreground='#FFFFFF'><b>%s</b></span>" % module.moduleName)
                    label.set_alignment(0.0, 0.5)
                    hbox.pack_start(pix, gtk.FALSE)

                    hbox.pack_end(label, gtk.TRUE)
                    self.leftLabelVBox.pack_start(hbox, gtk.FALSE, gtk.TRUE, 3)
                else:
                    self.notebook.append_page(vbox, gtk.Label(" "))
                pages = pages + 1

        self.notebook.set_current_page(0)
        self.setPointer(0)

        if not self.lowRes:
            # Add the box on the left to the window's HBox.
            self.mainHBox.pack_start(leftVBox, gtk.FALSE)

        # Populate the right side of the window.  Add the notebook to a VBox.
        self.internalVBox = gtk.VBox()

        self.internalVBox.pack_start(self.notebook, gtk.TRUE)

        # Now add the EventBox to the right-side VBox.
        self.rightVBox = gtk.VBox()
        self.rightVBox.set_size_request(400, 200)
        self.rightVBox.pack_start(self.internalVBox)

        # Add an Alignment widget to the top-level HBox, and place the right-side VBox into it.
        if not self.lowRes:
            alignment = gtk.Alignment()
            alignment.add(self.rightVBox)
            alignment.set(0.2, 0.3, 0.8, 0.8)
            self.mainHBox.pack_start(alignment, gtk.TRUE)
        else:
            self.mainHBox.pack_start(self.rightVBox)

        # Create a lower hbox that will contain the close button and button box
        self.lowerHBox = gtk.HBox()

        # Create a button box to handle navigation.
        self.bb = gtk.HButtonBox()
        self.bb.set_layout(gtk.BUTTONBOX_END)
        self.bb.set_border_width(10)
        self.bb.set_spacing(10)
        # Create the "go back" button, marking it insensitive by default.
        self.backButton = gtk.Button(stock='gtk-go-back')
        self.backButton.connect('clicked', self.backClicked)
        self.backButton.set_sensitive(gtk.FALSE)
        self.bb.pack_start(self.backButton)
        # Create the "go forward" button.
        self.nextButton = gtk.Button(stock='gtk-go-forward')
        self.nextHandler = self.nextButton.connect('clicked', self.nextClicked)

        self.bb.pack_start(self.nextButton)
	# Add the button box to the bottom of the box which contains the notebook.
        self.lowerHBox.pack_start(self.bb, gtk.TRUE)        
        self.internalVBox.pack_start(self.lowerHBox, gtk.FALSE, 10)

	# Add the main HBox to a VBox which will sit in the window.
        mainVBox.pack_start(self.mainHBox)

        self.win.show_all()
        self.nextButton.grab_focus()
        gtk.main()


    def destroy(self, *args):
        #Exit the GTK loop
        gtk.mainquit()
        #Kill the window manager
        if self.wm_pid:
            os.kill(self.wm_pid, 15)

        if self.xserver_pid:
            os.kill(self.xserver_pid, 15)

        #Exit firstboot.  This should take down the X server as well
        os._exit(0)

    def finishClicked(self, *args):
        try:
            module = self.moduleList[self.notebook.get_current_page()]
        except:
            pass

        #Call the apply method if it exists
        try:
            module.apply(self.notebook)
        except:
            pass

        #Call exitFirstboot to do some cleanup before exiting
        self.exitFirstboot()

    def exitFirstboot(self, *args):
        #Write the /etc/sysconfig/firstboot file to make sure firstboot doesn't run again
        firstbootBackend.writeSysconfigFile(self.doDebug)

        #Exit the GTK loop
        gtk.mainquit()
        if self.wm_pid:
        #Kill the window manager
            os.kill(self.wm_pid, 15)

        if self.xserver_pid:
            os.kill(self.xserver_pid, 15)

        import time
        time.sleep(0.5)

        #Exit firstboot.  This should take down the X server as well
        os._exit(0)

    def nextClicked(self, *args):
        try:
            module = self.moduleList[self.notebook.get_current_page()]
        except:
            pass

        result = None
        #Call the apply method if it exists
        try:
            result = module.apply(self.notebook)
        except:
            import exceptionWindow
            (type, value, tb) = sys.exc_info()
            list = traceback.format_exception(type, value, tb)
            text = string.joinfields(list, "")
            result = exceptionWindow.ExceptionWindow(module, text)
            pass

        if result != None:
            self.notebook.next_page()
            module = self.moduleList[self.notebook.get_current_page()]
            #Call setPointer to make the left hand pointer move to the correct pointer
            self.setPointer(self.notebook.get_current_page())

            if "grabFocus" in dir(module):
                #If the module needs to grab the focus, let it
                module.grabFocus()

        else:
            #Something went wrong in the module.  Don't advance
            return

        #Check to see if we're on the last page.  
        tmp = self.notebook.get_nth_page(self.notebook.get_current_page() + 1)        
        if not tmp:
            self.nextButton.disconnect(self.nextHandler)
            self.nextHandler = self.nextButton.connect('clicked', self.finishClicked)
            self.win.disconnect(self.winHandler)
            self.winHandler = self.win.connect ("key-release-event", self.closeRelease)

        self.backButton.set_sensitive(gtk.TRUE)

    def backClicked(self, *args):
        self.notebook.prev_page()
        #Call setPointer to make the left hand pointer move to the correct pointer
        self.setPointer(self.notebook.get_current_page())

        if self.notebook.get_current_page() == 0:
            self.backButton.set_sensitive(gtk.FALSE)

        self.nextButton.disconnect(self.nextHandler)
        self.nextHandler = self.nextButton.connect('clicked', self.nextClicked)
        self.win.disconnect(self.winHandler)
        self.winHandler = self.win.connect ("key-release-event", self.keyRelease)

    def keyRelease(self, window, event):
        if (event.keyval == gtk.keysyms.F12):
            self.nextClicked()
        if (event.keyval == gtk.keysyms.F11):
            self.backClicked()

    def closeRelease(self, window, event):
        if (event.keyval == gtk.keysyms.F12):
            self.finishClicked()
        if (event.keyval == gtk.keysyms.F11):
            self.backClicked()

    def setPointer(self, number):
        items = self.leftLabelVBox.get_children()

        for i in range(len(items)):
            pix, label = self.leftLabelVBox.get_children()[i].get_children()

            if i == number:
                pix.set_from_file("/usr/share/firstboot/pixmaps/pointer-white.png")
            else:
                pix.set_from_file("/usr/share/firstboot/pixmaps/pointer-blank.png")
