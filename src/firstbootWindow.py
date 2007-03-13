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

import glob
import string
import os
import os.path
import traceback
os.environ["PYGTK_DISABLE_THREADS"] = "1"
os.environ["PYGTK_FATAL_EXCEPTIONS"] = "1"
os.environ["GNOME_DISABLE_CRASH_DIALOG"] = "1"

import imputil
import sys
import cairo
import gtk
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
        self.needsReboot = []
        self.xserver_pid = fb.xserver_pid
        self.wm_pid = fb.wm_pid
        self.doReconfig = fb.doReconfig
        self.doDebug = fb.doDebug
        self.lowRes = fb.lowRes
        self.autoscreenshot = fb.autoscreenshot

        self.moduleList = []
        self.moduleDict = {}
        self.pageHistory = []
        self.nextPage = None

        # Create the initial window and a vbox to fill it with.
        self.win = gtk.Window()
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.set_decorated(False)

        if not self.doReconfig:
            self.win.set_keep_below(True)

        self.x_screen = gtk.gdk.screen_width()
        self.y_screen = gtk.gdk.screen_height()

        # Create a box that will hold all other widgets.
        self.mainHBox = gtk.HBox(False, 10)

        # leftVBox holds the labels for the various modules.
        self.leftVBox = gtk.VBox()
        self.leftVBox.set_border_width(5)

        # leftEventBox exists only so we have somewhere to paint an image.
        self.leftEventBox = gtk.EventBox()
        self.leftEventBox.add(self.leftVBox)
        self.leftVBox.connect("expose-event", self.leb_exposed)

        # rightVBox holds the notebook and the button box.
        self.rightVBox = gtk.VBox()
        self.rightVBox.set_border_width(5)

        # If we're in low res mode, grow the right hand box to take up the
        # entire window.
        if self.x_screen >= 800:            
            self.leftEventBox.set_size_request(int(0.2*self.x_screen),
                                               self.y_screen)
            self.rightVBox.set_size_request(int(0.8*self.x_screen),
                                            self.y_screen)
            self.win.fullscreen()
        else:
            self.rightVBox.set_size_request(self.x_screen, self.y_screen)
            self.win.set_size_request(self.x_screen, self.y_screen)
            self.lowRes = 1

        # Create a button box to handle navigation.
        self.buttonBox = gtk.HButtonBox()
        self.buttonBox.set_layout(gtk.BUTTONBOX_END)
        self.buttonBox.set_spacing(10)

        # Create the "go back" button, marking it insensitive by default.
        self.backButton = gtk.Button(use_underline=True, stock='gtk-go-back',
                                     label=_("_Back"))
        self.backButton.set_sensitive(False)
        self.backButton.connect('clicked', self.backClicked)

        self.buttonBox.set_border_width(10)
        self.buttonBox.pack_start(self.backButton)

        # Create the "go forward" button.
        self.nextButton = gtk.Button(use_underline=True, stock='gtk-go-forward',
                                     label=_("_Forward"))
        self.nextHandler = self.nextButton.connect('clicked', self.nextClicked)
        self.buttonBox.pack_start(self.nextButton)

        # Create the notebook.  We use a ListView to control which page in the
        # notebook is displayed.
        self.notebook = gtk.Notebook()
        if self.doDebug:
            #self.modulePath = ('/usr/src/rhn/up2date/firstboot')
            self.modulePath = ('/usr/share/firstboot/modules')
            self.notebook.set_show_tabs(False)
            self.notebook.set_scrollable(True)
            self.notebook.set_show_border(False)
        else:
            self.modulePath = ('/usr/share/firstboot/modules')
            self.notebook.set_show_tabs(False)
            self.notebook.set_show_border(False)

        self.notebook.connect("switch-page", self.switchPage)

        sys.path.append(self.modulePath)

        self.loadModules()

        self.notebook.set_current_page(0)
        self.setPointer(0)

        # Add the widgets into the right side.
        self.rightVBox.pack_start(self.notebook)
        self.rightVBox.pack_start(self.buttonBox, expand=False)

        # Add the widgets into the main widget.
        if not self.lowRes:
            self.mainHBox.pack_start(self.leftEventBox)

        self.mainHBox.pack_start(self.rightVBox)
        self.win.add(self.mainHBox)

        self.win.connect("destroy", self.destroy)
        self.winHandler = self.win.connect ("key-release-event",
                                            self.keyRelease)

        # This should really be in firstboot.py, but something about
        # importing all the modules screws the keyboard up only when we
        # start from rhgb.  So here it is.
        if not fb.doDebug:
            from rhpl.keyboard import Keyboard
            kbd = Keyboard()
            kbd.read()
            kbd.activate()

        self.win.show_all()
        self.win.present()
        self.nextButton.grab_focus()
        gtk.main()

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
        if self.wm_pid and not self.doDebug:
            os.kill(self.wm_pid, 15)

        if self.xserver_pid and not self.doDebug:
            os.kill(self.xserver_pid, 15)

        #Exit firstboot.  This should take down the X server as well
        os._exit(0)

    # A screen has already been displayed.  Try to apply it.  If the result of
    # the application is None (either because there was some sort of error or
    # or because the user didn't do what they were supposed to) then return
    # False.  This tells the caller that we didn't advance to the next page
    # and the caller shouldn't take further action.  Otherwise, set up the
    # next screen.
    def _runAndAdvance(self):
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
            (ty, value, tb) = sys.exc_info()
            lst = traceback.format_exception(ty, value, tb)
            text = string.joinfields(lst, "")
            result = exceptionWindow.ExceptionWindow(module, text)
            pass

        # Store the name of every module that requires a reboot.  This allows
        # us to remove a single module if the user moves back and forth through
        # the UI while still knowing that other modules still require reboot.
        if hasattr(module, "needsReboot") and module.needsReboot:
            print "adding needsReboot for %s" % module.moduleName
            self.needsReboot.append(module.moduleName)
        elif hasattr(module, "needsReboot") and not module.needsReboot:
            if module.moduleName in self.needsReboot:
                print "removing needsReboot for %s" % module.moduleName
                self.needsReboot.remove(module.moduleName)

        # record the current page as the new previous page
        self.prevPage = self.moduleNameToIndex[module.__module__][0]

        if result != None:
            pgNum = self.moduleNameToIndex[module.__module__][0]
            self.pageHistory.append(pgNum)

            if self.nextPage:
                self.notebook.set_current_page(self.nextPage)
                module = self.moduleList[self.nextPage]
                self.nextPage = None
            else:
                self.notebook.next_page()
                module = self.moduleList[self.notebook.get_current_page()]

            #Call setPointer to make the left hand pointer move to the correct pointer
            self.setPointer(self.moduleNameToIndex[module.__module__][1])

            if "grabFocus" in dir(module):
                #If the module needs to grab the focus, let it
                module.grabFocus()
            else:
                self.nextButton.grab_focus()

            return True
        else:
            #Something went wrong in the module.  Don't advance
            return False

    def finishClicked(self, *args):
        advanced = self._runAndAdvance()

        if advanced:
            #Call exitFirstboot to do some cleanup before exiting
            self.exitFirstboot()

    def exitFirstboot(self, *args):
        # Write the /etc/sysconfig/firstboot file to make sure firstboot doesn't run again
        firstbootBackend.writeSysconfigFile(self.doDebug)

        if len(self.needsReboot) > 0 and not self.doDebug:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                    _("The system must now reboot for some of your selections to take effect."))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.show_all()
            dlg.run()
            dlg.destroy()
            os.system("/sbin/reboot")

        # Exit the GTK loop
        gtk.main_quit()

        # Kill the window manager
        if self.wm_pid and not self.doDebug:
            os.kill(self.wm_pid, 15)

        if self.doReconfig:
            try:
                os.unlink("/etc/reconfigSys")
            except:
                pass

        if self.xserver_pid and not self.doDebug:
            os.kill(self.xserver_pid, 15)

        # Give the X server a second to exit
        import time
        time.sleep(1)

        os._exit(0)

    def nextClicked(self, *args):
        advanced = self._runAndAdvance()

        if advanced:
            #Check to see if we're on the last page. 
            items = self.leftVBox.get_children()
            current_page = self.notebook.get_current_page()
            if (current_page + 1) == len(items):
     
                self.nextButton.disconnect(self.nextHandler)
                self.nextHandler = self.nextButton.connect('clicked', self.finishClicked)
                self.nextButton.set_label(_("_Finish"))
                self.nextButton.set_use_underline(True)
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

        try:
            module = self.moduleList[self.notebook.get_current_page()]
        except:
            pass
            
        #Call setPointer to make the left hand pointer move to the correct pointer
        self.setPointer(self.moduleNameToIndex[module.__module__][1])

        if self.notebook.get_current_page() == 0:
            self.backButton.set_sensitive(False)

        self.nextButton.disconnect(self.nextHandler)
        self.nextHandler = self.nextButton.connect('clicked', self.nextClicked)
        self.nextButton.set_label('gtk-go-forward')
        self.nextButton.set_use_stock(True)
        self.nextButton.set_use_underline(True)
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
        items = self.leftVBox.get_children()

        for i in range(len(items)):
            alignment, label = self.leftVBox.get_children()[i].get_children()
            pix = alignment.get_children()[0]

            if i == number:
                pix.set_from_file("/usr/share/firstboot/pixmaps/pointer-white.png")
            else:
                pix.set_from_file("/usr/share/firstboot/pixmaps/pointer-blank.png")

    def leb_exposed(self, eb, event):
        pixbuf = functions.pixbufFromPath("/usr/share/firstboot/pixmaps/firstboot-left.png")
        aspect_ratio = (1.0 * pixbuf.get_width ()) / (1.0 * pixbuf.get_height())
	pixbuf = pixbuf.scale_simple(int(self.y_screen * aspect_ratio),
                                     self.y_screen, gtk.gdk.INTERP_BILINEAR)

        cairo_context = eb.window.cairo_create()
        cairo_context.set_source_pixbuf(pixbuf, 0, self.y_screen - pixbuf.get_height())
        cairo_context.paint()
        return False

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
        lst = map(lambda x: os.path.splitext(os.path.basename(x))[0],
                  glob.glob(self.modulePath + "/*.py"))

        # Import each module, and filter out those
        for module in lst:
            # If we can't find the module, skip it
            try:
                found = imputil.imp.find_module(module)
            except:
                print _("module import of %s failed: %s") % (module,sys.exc_type)
                continue

            loaded = imputil.imp.load_module(module, found[0], found[1], found[2])

            if loaded.__dict__.has_key("childWindow"):
                obj = loaded.childWindow()

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
                    self.moduleDict[float(obj.runPriority)] = obj
                elif (not self.doReconfig and (obj.moduleClass != "reconfig")):
                    self.moduleDict[float(obj.runPriority)] = obj
            else:
                self.moduleDict[float(obj.runPriority)] = obj

        # Get the list of module priorities, sort them to determine a run
        # order, and build a list with the modules in the proper order.
        modulePriorityList = self.moduleDict.keys()
        modulePriorityList.sort()

        # Add the modules to the proper lists.
        pages = 0
        sidebarIndex = -1
        self.moduleNameToIndex = {}
        for priority in modulePriorityList:
            # Add the module to the list of modules.
            module = self.moduleDict[priority]
            # Launch the module's GUI.
            vbox = None

            if self.doDebug:
                try:
                    print "calling", module.moduleName
                    result = module.launch(self.doDebug)

                    if result is None:
                        continue
                    else:
                        vbox, pix, title = result
                except:
                    import exceptionWindow
                    (ty, value, tb) = sys.exc_info()
                    lst = traceback.format_exception(ty, value, tb)
                    text = string.joinfields(lst, "")
                    exceptionWindow.ExceptionWindow(module, text)
                    pass                    
            else:
                try:
                    result = module.launch()

                    if result is None:
                        continue
                    else:
                        vbox, pix, title = result
                except:
                    import exceptionWindow
                    (ty, value, tb) = sys.exc_info()
                    lst = traceback.format_exception(ty, value, tb)
                    text = string.joinfields(lst, "")
                    exceptionWindow.ExceptionWindow(module, text)
                    pass
                    continue

            if vbox and title:
                # If it launched, add it to the module list.
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
                    if not hasattr(module, "noSidebar") or not getattr(module, "noSidebar"):
                        hbox = gtk.HBox(False, 5)
                        pix = functions.imageFromFile("pointer-blank.png")
                        label = gtk.Label("")
                        label.set_markup("<span foreground='#FFFFFF'><b>%s</b></span>" % (_(module.moduleName)))
                        label.set_alignment(0.0, 0.5)

                        # Wrap the lines if they're too long
                        label.set_line_wrap(True)
                        (w, h) = self.leftEventBox.get_size_request()
                        label.set_size_request((int)(w*0.8), -1)

                        # Make sure the arrow is at the top of any wrapped line
                        alignment = gtk.Alignment(yalign=0.2)
                        alignment.add(pix)
                        hbox.pack_start(alignment, False)

                        hbox.pack_end(label, True)
                        self.leftVBox.pack_start(hbox, False, True, 3)

                        sidebarIndex += 1

                    # we need a non tranlated name for each module so we can
                    # jump around
                    self.moduleNameToIndex[module.__module__] = (pages, sidebarIndex)
                    self.notebook.insert_page(vbox, gtk.Label(_(module.moduleName)),sidebarIndex)
                else:
                    self.notebook.append_page(vbox, gtk.Label(" "))
                    self.moduleNameToIndex["unamemodule-%s" % pages] = (pages, sidebarIndex)

                pages += 1

    def clearNotebook(self):
        for widget in self.leftVBox.get_children():
            self.leftVBox.remove(widget)

        pageNum = len(self.notebook.get_children())
        for i in range(pageNum):
            self.notebook.hide()
            self.notebook.remove_page(i)
            
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

        self.leftVBox.get_children()[0].get_children()[1].set_text(_("Welcome"))

        # Change the locale on the buttons.
        self.backButton.set_label('gtk-go-back')
        self.backButton.set_use_stock(True)
        self.backButton.set_use_underline(True)
        self.nextButton.set_label('gtk-go-forward')
        self.nextButton.set_use_stock(True)
        self.nextButton.set_use_underline(True)

        self.clearNotebook()
        self.loadModules()

        self.leftVBox.show_all()
        self.notebook.show_all()
        self.notebook.set_current_page(0)

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
