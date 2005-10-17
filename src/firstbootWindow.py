## firstbootWindow.py - the main firstboot UI and framework.py
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
from firstboot import Firstboot
from rhpl.translate import cat
from rhpl import ethtool

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")

#
# Stuff for screenshots
#
screenshotDir = None
screenshotIndex = 0

class firstbootWindow:
    def __init__(self, fb):
        self.needsReboot = False
        self.xserver_pid = fb.xserver_pid
        self.wm_pid = fb.wm_pid
        self.doReconfig = fb.doReconfig
        self.doDebug = fb.doDebug
        self.lowRes = fb.lowRes
        self.autoscreenshot = fb.autoscreenshot
        self.mainHBox = gtk.HBox(False, 10)
        self.leftLabelVBox = gtk.VBox()

        self.leftLabelVBox.set_border_width(12)
        
        leftEventBox = gtk.EventBox()
        leftEventBox.add(self.leftLabelVBox)
        leftEventBox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#7e8ea0"))

        self.leftVBox = gtk.VBox()
        self.leftVBox.pack_start(leftEventBox, True)

        self.moduleList = []
        self.moduleDict = {}

        self.nextPage = None
        # Create the initial window and a vbox to fill it with.
        self.win = gtk.Window()
        self.win.connect("destroy", self.destroy)
        self.winHandler = self.win.connect ("key-release-event", self.keyRelease)
        self.win.realize()

        self.pageHistory = []

        mainVBox = gtk.VBox()

        #This isn't debug mode, so jump through some hoops to go into fullscreen/root window mode
        self.win.set_decorated(False)
        x_screen = gtk.gdk.screen_width()
        y_screen = gtk.gdk.screen_height()        

        #Let's draw the background
        pixbuf = functions.pixbufFromPath("/usr/share/firstboot/pixmaps/lightrays.png")
        if pixbuf is not None:
            pixbuf = pixbuf.scale_simple(x_screen, y_screen, gtk.gdk.INTERP_BILINEAR)
            bgimage = gtk.gdk.Pixmap(self.win.window, x_screen, y_screen, -1)
            bgimage.draw_pixbuf(gtk.gdk.GC(bgimage), pixbuf, 0, 0, 0, 0,
                                x_screen, y_screen)
            self.win.set_app_paintable(True)
            self.win.window.set_back_pixmap(bgimage, False)

            if not self.doDebug:
                self.win.set_size_request(x_screen, y_screen)

        align = gtk.Alignment(0.5, 0.5, 0.0, 0.0)
        eb = gtk.EventBox()
        eb.connect("realize", self.eb_realized)

        eb.add(mainVBox)

        if x_screen >= 800:            
            eb.set_size_request(800, 600)
        else:
            mainVBox.set_size_request(gtk.gdk.screen_width(), gtk.gdk.screen_height())
            self.lowRes = 1

        align.add(eb)
        self.win.add(align)
            
        # Create the notebook.  We use a ListView to control which page in the
        # notebook is displayed.
        self.notebook = gtk.Notebook()
        if self.doDebug:
            print "starting firstbootWindow", doReconfig, doDebug                    
            #self.modulePath = ('modules/')
            #self.modulePath = ('/usr/src/rhn/up2date/firstboot')
            self.modulePath = ('/usr/share/firstboot/modules')
            self.win.set_position(gtk.WIN_POS_CENTER)            
            self.notebook.set_show_tabs(False)
            self.notebook.set_scrollable(True)
            self.notebook.set_show_border(False)
        else:
            self.modulePath = ('/usr/share/firstboot/modules')
            self.win.set_position(gtk.WIN_POS_CENTER)
            self.notebook.set_show_tabs(False)
            self.notebook.set_show_border(False)

        self.notebook.connect("switch-page", self.switchPage)

        sys.path.append(self.modulePath)

        self.loadModules()

        self.notebook.set_current_page(0)
        self.setPointer(0)

        if not self.lowRes:
            # Add the box on the left to the window's HBox.
            self.mainHBox.pack_start(self.leftVBox, False)

        # Populate the right side of the window.  Add the notebook to a VBox.
        self.internalVBox = gtk.VBox()

        self.internalVBox.pack_start(self.notebook, True)

        # Now add the EventBox to the right-side VBox.
        self.rightVBox = gtk.VBox()
        self.rightVBox.set_size_request(400, -1)
        self.rightVBox.pack_start(self.internalVBox)

        # Add an Alignment widget to the top-level HBox, and place the right-side VBox into it.
        if not self.lowRes:
            alignment = gtk.Alignment()
            alignment.add(self.rightVBox)
            alignment.set(0.2, 0.3, 0.8, 0.8)
            self.mainHBox.pack_start(alignment, True)
        else:
            self.mainHBox.pack_start(self.rightVBox)

        # Create a button box to handle navigation.
        self.bb = gtk.HButtonBox()
        self.bb.set_layout(gtk.BUTTONBOX_END)
        self.bb.set_spacing(10)
        # Create the "go back" button, marking it insensitive by default.
        self.backButton = gtk.Button(stock='gtk-go-back')
        label = self.backButton.get_children()[0].get_children()[0].get_children()[1]
        label.set_text(_("_Back"))
        label.set_property("use_underline", True)
        self.backButton.connect('clicked', self.backClicked)
        self.backButton.set_sensitive(False)
        self.bb.pack_start(self.backButton)
        # Create the "go forward" button.
        self.nextButton = gtk.Button(stock='gtk-go-forward')
        self.nextLabel = self.nextButton.get_children()[0].get_children()[0].get_children()[1]
        self.nextLabel.set_text(_("_Next"))
        self.nextLabel.set_property("use_underline", True)
        
        self.nextHandler = self.nextButton.connect('clicked', self.nextClicked)

        self.bb.pack_start(self.nextButton)
        # Add the button box to the bottom of the box which contains the notebook.

        self.internalVBox.pack_start(self.bb, False)

        # Add the main HBox to a VBox which will sit in the window.
        mainVBox.pack_start(self.mainHBox)

        self.win.show_all()
        self.win.present()
        self.nextButton.grab_focus()
        gtk.main()

    def setPage(self, modulename):
        self.nextPage = self.moduleNameToNotebookIndex[modulename]

    def switchPage(self, notebook, page, page_num, *args):
        # catch the switch page signal, so we can re poke modules
        # that need a signal that they are being shown
        try:
            module = self.moduleList[page_num]
        except:
            pass

        if hasattr(module, "updatePage"):
            module.updatePage()

    def destroy(self, *args):
        #Exit the GTK loop
        gtk.main_quit()
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
        gtk.main_quit()
        if self.wm_pid:
        #Kill the window manager
            os.kill(self.wm_pid, 15)

        if self.xserver_pid:
            os.kill(self.xserver_pid, 15)

        #Give the X server a second to exit
        import time
        time.sleep(1)

        if self.needsReboot == True:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                    _("The system must now reboot for some of your selections to take effect."))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.show_all()
            rc = dlg.run()
            dlg.destroy()
            os.system("/sbin/reboot")
        else:
            #Exit firstboot.  This should take down the X server as well
            os._exit(0)

    def nextClicked(self, *args):
        try:
            module = self.moduleList[self.notebook.get_current_page()]
        except:
            pass

	if self.autoscreenshot:
            self.takeScreenShot()
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

        if hasattr(module, "needsReboot") and module.needsReboot == True:
            self.needsReboot = True

        # record the current page as the new previous page
        self.prevPage = self.moduleNameToNotebookIndex[module.__module__]

        if result != None:
            pgNum = self.moduleNameToNotebookIndex[module.__module__]
            self.pageHistory.append(pgNum)
#            print "self.pageHistory: %s" % self.pageHistory
            if self.nextPage:
                self.notebook.set_current_page(self.nextPage)
                module = self.moduleList[self.nextPage]
                self.nextPage = None
            else:
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
            self.nextLabel.set_text(_("_Finish"))
            self.nextLabel.set_property("use_underline", True)
            self.win.disconnect(self.winHandler)
            self.winHandler = self.win.connect ("key-release-event", self.closeRelease)

        self.backButton.set_sensitive(True)

    def backClicked(self, *args):
#        print "back: %s" % self.pageHistory
        if len(self.pageHistory):
            self.notebook.set_current_page(self.pageHistory[-1])
            del self.pageHistory[-1]
        else:
            self.notebook.prev_page()
            
        #Call setPointer to make the left hand pointer move to the correct pointer
        self.setPointer(self.notebook.get_current_page())

        if self.notebook.get_current_page() == 0:
            self.backButton.set_sensitive(False)

        self.nextButton.disconnect(self.nextHandler)
        self.nextHandler = self.nextButton.connect('clicked', self.nextClicked)
        self.nextLabel.set_text(_("_Next"))
        self.nextLabel.set_property("use_underline", True)
        self.win.disconnect(self.winHandler)
        self.winHandler = self.win.connect ("key-release-event", self.keyRelease)

    def keyRelease(self, window, event):
        if (event.keyval == gtk.keysyms.F12):
            self.nextClicked()
        if (event.keyval == gtk.keysyms.F11):
            self.backClicked()
        if (event.keyval == gtk.keysyms.Print and event.state & gtk.gdk.SHIFT_MASK):
            self.takeScreenShot()

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

    def eb_realized(self, eb):
        pixbuf = functions.pixbufFromFile("bg.png")
        bgimage = gtk.gdk.Pixmap(eb.window, 800, 600, -1)
        bgimage.draw_pixbuf(gtk.gdk.GC(bgimage), pixbuf, 0, 0, 0, 0, 800,
                            600, gtk.gdk.RGB_DITHER_MAX)
        eb.set_app_paintable(True)
        eb.window.set_back_pixmap(bgimage, False)

    def checkNetwork(self):
        # see if we have a non loopback interface up
        intfs = ethtool.get_active_devices()
        for intf in intfs:
            if intf != "lo":
                return 1
        return 0

    def loadModules(self):
        self.moduleList = []
        self.moduleDict = {}

        # Generate a list of all of the module files (which becomes the list of
        # all non-hidden files in the directory with extensions other than .py.
        files = os.listdir(self.modulePath)
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

            try:
                exec(cmd)
            except:
                print _("module import of %s failed: %s") % (module,sys.exc_type)
                continue

            # if the exec fails, skip this module
            try:
                obj = obj
            except NameError:
                continue

            # XXX - hack to allow firstboot to pass in the parent class into language
            # this will allow the language module to change firstboot's current locale
            if module == "language" or hasattr(obj, "needsparent"):
                obj.passInParent(self)

            # if a module decides not to run, skip it first before trying any
            # of the other hooks. bz #158095
            if hasattr(obj, "skipme"):
                # the module itself has decided for some reason that
                # that it should not be shown, so skip it
                continue

            # if the module needs network access, and we dont have it, skip
            # the module
            if hasattr(obj, "needsnetwork"):
                if not self.checkNetwork():
                    # we need a way to run some stuff from the modules
                    # if they have no network
                    if hasattr(obj, "noNetwork"):
                        obj.noNetwork()
                    continue

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
        self.moduleNameToNotebookIndex = {}
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
                title_label.set_markup("<span foreground='#000000' size='30000' font_family='Helvetica'><b>%s</b></span>" % (_(title)))

                titleBox = gtk.HBox()
                if pix:
                    titleBox.pack_start(pix, False)
                titleBox.pack_start(title_label, True)
                titleBox.set_spacing(8)

                vbox.pack_start(titleBox, False)
                vbox.reorder_child(titleBox, 0)
                
                if self.lowRes:
                    # If we're in 640x480 mode, remove the title bars
                    vbox.remove(vbox.get_children()[0])

                # If the module has a name, add it to the list of labels
                if hasattr(module, "moduleName"):
                    # we need a non tranlated name for each module so we can
                    # jump around
                    self.moduleNameToNotebookIndex[module.__module__] = pages
                    self.notebook.append_page(vbox, gtk.Label(_(module.moduleName)))
                    hbox = gtk.HBox(False, 5)
                    pix = functions.imageFromFile("pointer-blank.png")
                    label = gtk.Label("")
                    label.set_markup("<span foreground='#FFFFFF'><b>%s</b></span>" % (_(module.moduleName)))
                    label.set_alignment(0.0, 0.5)
                    hbox.pack_start(pix, False)

                    hbox.pack_end(label, True)
                    self.leftLabelVBox.pack_start(hbox, False, True, 3)
                else:
                    self.notebook.append_page(vbox, gtk.Label(" "))
                    self.moduleNameToNotebookIndex["unamemodule-%s" % pages] = pages
                pages = pages + 1

    def clearNotebook(self):
        for widget in self.leftLabelVBox.get_children():
            self.leftLabelVBox.remove(widget)

        pageNum = len(self.notebook.get_children())
        for i in range(pageNum):
            self.notebook.hide()
            self.notebook.remove_page(0)
            
    def changeLocale(self, lang, fullName):
        lc, encoding = string.split(lang, ".")
        prefix, suffix = string.split(lc, "_")

        os.environ["RUNTIMELANG"] = fullName
        os.environ["LANG"] = lc
        os.environ["LC_NUMERIC"] = "C"
        import locale
        locale.setlocale(locale.LC_ALL, "")

        newlangs = [lang, lc, prefix]
        cat.setlangs(newlangs)

        self.leftLabelVBox.get_children()[0].get_children()[1].set_text(_("Welcome"))

        # Change the locale on the buttons.
        label = self.backButton.get_children()[0].get_children()[0].get_children()[1]
        label.set_text(_("_Back"))
        label.set_property("use_underline", True)

        label = self.nextButton.get_children()[0].get_children()[0].get_children()[1]
        label.set_text(_("_Next"))
        label.set_property("use_underline", True)
        
        self.clearNotebook()
        self.loadModules()

        self.leftLabelVBox.show_all()
        self.notebook.show_all()
        self.notebook.set_current_page(1)

    def takeScreenShot(self):
        global screenshotIndex
        global screenshotDir

        #Let's take some screenshots
        if screenshotDir is None:
            screenshotDir = "/root/firstboot-screenshots"

            if not os.access(screenshotDir, os.R_OK):
                try:
                    os.mkdir(screenshotDir)
                except:
                    screenshotDir = None

        screen_width = gtk.gdk.screen_width()
        screen_height = gtk.gdk.screen_height()

        src_x = (screen_width - 800) / 2
        src_y = (screen_height - 600) / 2

        screenshot = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                    800, 600)

        screenshot.get_from_drawable(gtk.gdk.get_default_root_window(),
                                     gtk.gdk.colormap_get_system(),
                                     src_x, src_y, 0, 0,
                                     800, 600)

        if screenshot:
            while (1):
                sname = "screenshot-%04d.png" % ( screenshotIndex,)
                if not os.access(screenshotDir + '/' + sname, os.R_OK):
                    break

                screenshotIndex = screenshotIndex + 1

            screenshot.save (screenshotDir + '/' + sname, "png")
            screenshotIndex = screenshotIndex + 1
    
