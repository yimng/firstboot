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
os.environ["PYGTK_DISABLE_THREADS"] = "1"
os.environ["PYGTK_FATAL_EXCEPTIONS"] = "1"
os.environ["GNOME_DISABLE_CRASH_DIALOG"] = "1"

import sys
import gtk
import gobject

class firstbootWindow:
    def __init__(self, wm_pid, doReconfig, doDebug):
        self.wm_pid = wm_pid
        self.doReconfig = doReconfig
        self.doDebug = doDebug
        self.mainHBox = gtk.HBox(gtk.FALSE, 10)
        self.moduleList = []
        self.moduleDict = {}
        self.moduleStore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT)

        # Create the initial window and a vbox to fill it with.
        win = gtk.Window()
        win.connect("destroy", self.destroy)

        if gtk.gdk.screen_width() >= 800:            
            win.set_size_request(800, 600)
        else:
            win.set_size_request(gtk.gdk.screen_width(), gtk.gdk.screen_height())
            
        win.set_resizable(gtk.FALSE)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_decorated(gtk.FALSE)
        mainVBox = gtk.VBox()

        # Create the notebook.  We use a ListView to control which page in the
        # notebook is displayed.
        self.notebook = gtk.Notebook()

        if self.doDebug:
            print "starting firstbootWindow", doReconfig, doDebug                    
            path = ('modules/')
            self.notebook.set_scrollable(gtk.TRUE)
        else:
            path = ('/usr/share/firstboot/modules')
            self.notebook.set_show_tabs(gtk.FALSE)
            self.notebook.set_show_border(gtk.FALSE)

        sys.path.append(path)

        #Code for an upper title bar like anaconda.  We may turn this on if we get some UI help
##         pix = self.imageFromFile("pixmaps/titlebar.png")
##         if pix:
##             mainVBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 0)
##             pass

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

	# Add the modules to the proper lists.
        pages = 0
        for priority in modulePriorityList:
            # Add the module to the list of modules.
            module = self.moduleDict[priority]
            # Launch the module's GUI.
            vbox = None
            eventbox = None

            if self.doDebug:
                print "calling", module.moduleName
                vbox, eventbox = module.launch(self.doDebug)
            else:
                try:
                    vbox, eventbox = module.launch()
                except:
                    continue

            if vbox and eventbox:
                # If it launched, add it to the mdoule list.
                self.moduleList.append(module)
                # Set the background of the header to a uniform color.
                eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#6d81a0"))
                # If the module has a name, add it to the ListStore as well, mapping
                # the module name to the page number.
                if hasattr(module, "moduleName"):
                    self.notebook.append_page(vbox, gtk.Label(module.moduleName))
                    iter = self.moduleStore.append()
                    self.moduleStore.set_value(iter, 0, module.moduleName)
                    self.moduleStore.set_value(iter, 1, pages)
                else:
                    self.notebook.append_page(vbox, gtk.Label(" "))
                pages = pages + 1

        # Create the TreeView widget and pack it into a box.
        self.moduleView = gtk.TreeView(self.moduleStore)
        if self.doDebug:
            self.moduleView.connect("cursor-changed", self.cursorChanged)
        leftVBox = gtk.VBox()
        leftVBox.pack_start(self.moduleView, gtk.TRUE)

        # Hook up a signal to highlight the selected page, and switch to page 0.
        self.notebook.connect("switch-page", self.switchPage)
        self.notebook.set_current_page(0)

        # Add our logo to the left box, below the TreeView.
        pix = self.imageFromFile("redhat-logo.png")
        if pix:
            leftVBox.pack_start(pix, gtk.FALSE)

        # Tell the TreeView how to display the ListStore.
        col = gtk.TreeViewColumn(None, gtk.CellRendererText(), text=0)
        self.moduleView.append_column(col)
        self.moduleView.set_property("headers-visible", gtk.FALSE)
        self.moduleView.set_size_request(195, -1)

        # Add the box on the left to the window's HBox.
        self.mainHBox.pack_start(leftVBox, gtk.FALSE)

        # Populate the right side of the window.  Add the notebook to a VBox.
        self.internalVBox = gtk.VBox()
        self.internalVBox.pack_start(self.notebook, gtk.TRUE)

        # Now add the VBox to an EventBox.
        eventBox = gtk.EventBox()
        eventBox.add(self.internalVBox)
        eventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#EEEEEE"))

        # Now add the EventBox to the right-side VBox.
        self.rightVBox = gtk.VBox()
        self.rightVBox.set_size_request(400, 200)
        self.rightVBox.pack_start(eventBox, gtk.TRUE)

        # Add an Alignment widget to the top-level HBox, and place the
	# right-side VBox into it.
        alignment = gtk.Alignment()
        alignment.add(self.rightVBox)
        alignment.set(0.5, 0.5, 0.9, 0.9)
        self.mainHBox.pack_start(alignment, gtk.TRUE)

        # Create a lower hbox that will contain the close button and button box
        self.lowerHBox = gtk.HBox()

        # Create an exit button
        self.left_bb = gtk.HButtonBox()
        self.left_bb.set_layout(gtk.BUTTONBOX_START)
        self.left_bb.set_border_width(10)
        self.left_bb.set_spacing(10)
        self.exitButton = gtk.Button(stock='gtk-quit')
        self.exitButton.connect("clicked", self.abortFirstboot)
        self.left_bb.pack_start(self.exitButton)
        self.lowerHBox.pack_start(self.left_bb, gtk.FALSE)
        
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
        # Create the "go forward" and "finish" buttons.
        self.nextButton = gtk.Button(stock='gtk-go-forward')
        self.nextButton.connect('clicked', self.nextClicked)
#        group = gtk.AccelGroup()
#        self.nextButton.add_accelerator("clicked", group, gtk.gdk.keyval_from_name("p"), gtk.gdk.RELEASE_MASK, 0)
#        win.add_accel_group(group)

        self.bb.pack_start(self.nextButton)
        self.finishButton = gtk.Button(stock='gtk-close')
        self.finishButton.connect('clicked', self.finishClicked)
	# Add the button box to the bottom of the box which contains the
	# notebook.
        self.lowerHBox.pack_start(self.bb, gtk.TRUE)
        
#        self.internalVBox.pack_start(self.bb, gtk.FALSE, 10)
        self.internalVBox.pack_start(self.lowerHBox, gtk.FALSE, 10)


        #Accelerators aren't currently working in GTK 2.0   Grrrrrrr.
        group = gtk.AccelGroup()
        self.nextButton.add_accelerator('clicked', group, gtk.keysyms.F12,
                                   gtk.gdk.RELEASE_MASK, 0)
        self.backButton.add_accelerator('clicked', group, gtk.keysyms.F11,
                                   gtk.gdk.RELEASE_MASK, 0)
        win.add_accel_group(group)

	# Add the main HBox to a VBox which will sit in the window.
        mainVBox.pack_start(self.mainHBox)

        pix = self.imageFromFile("bg.png")
	if pix:
            win.realize()
            win.set_app_paintable(gtk.TRUE)

            bgimage = gtk.gdk.Pixmap(win.window, 800, 600, -1)
            gc = bgimage.new_gc ()
            pix.get_pixbuf().render_to_drawable(bgimage, gc, 0, 0, 0, 0, 800, 600, gtk.gdk.RGB_DITHER_MAX, 0, 0)
            win.window.set_back_pixmap (bgimage, gtk.FALSE)

        # Show the main window and go for it.
        win.add(mainVBox)
        win.show_all()
        gtk.main()

    def destroy(self, *args):
        #Exit the GTK loop
        gtk.mainquit()
        #Kill the window manager
        os.kill(self.wm_pid, 15)
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

        #Write the /etc/sysconfig/firstboot file to tell firstboot not to run again
        if (not self.doDebug):
            fd = open("/etc/sysconfig/firstboot", "w")
            fd.write("RUN_FIRSTBOOT=NO\n")
            fd.close()

        #Exit the GTK loop
        gtk.mainquit()
        if self.wm_pid:
        #Kill the window manager
            os.kill(self.wm_pid, 15)
        #Exit firstboot.  This should take down the X server as well
        os._exit(0)

    def abortFirstboot(self, *args):
        #Write the /etc/sysconfig/firstboot file to tell firstboot not to run again
        if (not self.doDebug):
            fd = open("/etc/sysconfig/firstboot", "w")
            fd.write("RUN_FIRSTBOOT=NO\n")
            fd.close()

        #Exit the GTK loop
        gtk.mainquit()
        if self.wm_pid:
        #Kill the window manager
            os.kill(self.wm_pid, 15)
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
            pass

        if result:
            self.notebook.next_page()
            module = self.moduleList[self.notebook.get_current_page()]

            if "grabFocus" in dir(module):
                #If the module needs to grab the focus, let it
                module.grabFocus()

        else:
            #Something went wrong in the module.  Don't advance
            return

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

        if self.finishButton in self.bb.get_children():
            self.bb.remove(self.finishButton)
            self.bb.pack_end(self.nextButton)
            self.bb.show_all()

#        self.stepList.select_row(self.notebook.get_current_page(), 0)

    # When a row in the list is selected, select the corresponding page in
    # the notebook.
    def cursorChanged(self, list):
        selection = self.moduleView.get_selection()
        model, iter = selection.get_selected()
        if model and iter:
            row = model.get_value(iter, 1)
            self.notebook.set_current_page(row)

    # When the notebook page is changed, select the right item in the list.
    def switchPage(self, notebook, page_widget, page):
        iter = self.moduleStore.get_iter_root()
        selection = self.moduleView.get_selection()
        pnum = self.moduleStore.get_value(iter, 1)
        if (pnum == page):
            selection.select_iter(iter)
            return
	while self.moduleStore.iter_next(iter):
            pnum = self.moduleStore.get_value(iter, 1)
            if (pnum == page):
                selection.select_iter(iter)
                break;

    # Attempt to load a gtk.Image from a file.
    def imageFromFile(self, filename):
        p = None        
        try:
            path = "pixmaps/" + filename
            p = gtk.gdk.pixbuf_new_from_file(path)
        except:
            try:
                path = "/usr/share/firstboot/pixmaps/" + filename
                p = gtk.gdk.pixbuf_new_from_file(path)
            except:
                pass


        if p:
            pix = gtk.Image()
            pix.set_from_pixbuf(p)        
            return pix
        return None
