#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 
#
import gtk
import logging, os, sys, string

from constants import *
from moduleset import *
from rhpl.translate import _

class Control:
    def __init__(self):
        self.currentPage = 0
        self.history = []
        self.moduleList = []

class Interface:
    def __init__(self, autoscreenshot=False, moduleList=[], testing=False,
                 themeDir=None):
        """Create a new Interface instance.  Instance attributes:

           autoscreenshot -- If true, a screenshot will be taken after every
                             module is run.
           moduleList     -- A list of references to all the loaded modules.
                             This is not typically used, but is required to
                             make the interface work.
           testing        -- Is firstboot running under testing mode, where no
                             changes will be made to the disk?
           themeDir       -- The directory containing the set of artwork to be
                             used in firstboot.  This makes branding firstboot
                             much easier as it does not require extensive code
                             changes.
        """

        self._screenshotDir = "/root/firstboot-screenshots"
        self._screenshotIndex = 0

        # This is needed for ModuleSet to work.  We maintain a stack of control
        # states, creating a new state for navigation when we enter into a
        # ModuleSet, then popping it off when we leave.
        self._controlStack = [Control()]
        self._control = self._controlStack[0]
        self._control.moduleList = moduleList

        self._x_size = gtk.gdk.screen_width()
        self._y_size = gtk.gdk.screen_height()

        self.autoscreenshot = autoscreenshot
        self.moduleList = moduleList
        self.testing = testing
        self.themeDir = themeDir

    def _backClicked(self, *args):
        # If there's nowhere to go back to, we're either at the first page in
        # the module set or something went wrong (Back is enabled on the very
        # first page).  In the former case, revert back to the enclosing
        # control state for what page to display next.
        if len(self._control.history) == 0:
            if len(self._controlStack) == 1:
                logging.error("Attempted to go back, but history is empty.")
                return
            else:
                self._controlStack.pop()
                self._control = self._controlStack[-1]

        # Adjust everything to go to the previous page in the history.  But
        # don't set the sidebar pointer if we are in a ModuleSet.
        self._control.currentPage = self._control.history.pop()

        if len(self._controlStack) == 1:
            self._setPointer(self._control.currentPage)

        self._setBackSensitivity()
        self.displayModule()

    def _displayException(self):
        import exceptionWindow, traceback

        (ty, value, tb) = sys.exc_info()
        lst = traceback.format_exception(ty, value, tb)
        text = string.joinfields(lst, "")

        exceptionWindow.ExceptionWindow(text)
        self.destroy()

    def _keyRelease(self, window, event):
        if event.keyval == gtk.keysyms.F12:
            self.nextButton.clicked()
        elif event.keyval == gtk.keysyms.F11:
            self.backButton.clicked()
        elif event.keyval == gtk.keysyms.Print and event.state & gtk.gdk.SHIFT_MASK:
            self.takeScreenshot()

    def _loadPixbuf(self, fn):
        return gtk.gdk.pixbuf_new_from_file(fn)

    def _nextClicked(self, *args):
        if self.autoscreenshot:
            self.screenshot()

        try:
            self.advance()
        except:
            self._displayException()

    def _setBackSensitivity(self):
        self.backButton.set_sensitive(not(self._control.currentPage == 0 and len(self._controlStack) == 1))

    def _setPointer(self, number):
        # The sidebar pointer only works in terms of the top-level module list
        # as we don't display anything on the side for a ModuleSet and making
        # the pointer move around then would be confusing.
        for i in range(len(self.moduleList)):
            (alignment, label) = self.sidebar.get_children()[i].get_children()
            pix = alignment.get_children()[0]

            if i == number:
                pix.set_from_file("%s/%s" % (self.themeDir, "pointer-white.png"))
            else:
                pix.set_from_file("%s/%s" % (self.themeDir, "pointer-blank.png"))

    def _sidebarExposed(self, eb, event):
        pixbuf = self.sidebarBg.scale_simple(int(self._y_size * self.aspectRatio),
                                             self._y_size, gtk.gdk.INTERP_BILINEAR)
        cairo_context = eb.window.cairo_create()
        cairo_context.set_source_pixbuf(pixbuf, 0, self._y_size-pixbuf.get_height())
        cairo_context.paint()
        return False

    def advance(self):
        """Call the apply method on the currently displayed page, add it to
           the history, and move to the next page.  It is not safe to call this
           method from within firstboot modules.
        """
        module = self._control.moduleList[self._control.currentPage]
        self._control.history.append(self._control.currentPage)

        # This could fail, in which case the exception will propagate up to the
        # interface which will know the proper way to handle it.
        result = module.apply(self, self.testing)

        # If something went wrong in the module, don't advance.
        if result == RESULT_FAILURE:
            self._control.history.pop()
            return

        # If the apply action from the current page jumped us to another page,
        # don't try to jump again.
        if result != RESULT_JUMP:
            self.moveToPage(pageNum=self._control.currentPage+1)

            # Is this the last page, or are we actually in a ModuleSet and
            # there are possibly other pages to go to next?
            if self._control.currentPage == len(self._control.moduleList):
                if len(self._controlStack) == 1:
                    self.destroy()
                else:
                    self._controlStack.pop()
                    self._control = self._controlStack[-1]

    def createMainWindow(self):
        """Create and initialize the main window.  This includes switching to
           fullscreen mode if necessary, adding buttons, displaying artwork,
           and other functions.  This method should also create the UI elements
           that make up the sidebar.  This method returns a gtk.Window.
        """
        # Create the initial window and a vbox to fill it with.
        self.win = gtk.Window()
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.set_decorated(False)

        # Create a box that will hold all other widgets.
        self.mainHBox = gtk.HBox(False, 10)

        # Create the sidebar box.
        self.sidebar = gtk.VBox()
        self.sidebar.set_border_width(5)

        # Load this background now so we can figure out how big to make
        # the left side.
        self.sidebarBg = self._loadPixbuf("%s/%s" % (self.themeDir, "firstboot-left.png"))
        self.aspectRatio = (1.0 * self.sidebarBg.get_width()) / (1.0 * self.sidebarBg.get_height())

        # leftEventBox exists only so we have somewhere to paint an image.
        self.leftEventBox = gtk.EventBox()
        self.leftEventBox.add(self.sidebar)
        self.sidebar.connect("expose-event", self._sidebarExposed)

        # Create the box for the right side of the screen.  This holds the
        # display for the current module and the button box.
        self.rightBox = gtk.VBox()
        self.rightBox.set_border_width(5)

        # lowres mode is dead.  Grow the right hand box to take up the entire
        # rest of the screen and go into fullscreen mode.
        leftWidth = int(self._x_size * self.aspectRatio)
        self.leftEventBox.set_size_request(leftWidth, self._y_size)
        self.rightBox.set_size_request(self._x_size - leftWidth, self._y_size)
        self.win.fullscreen()

        # Create a button box to handle navigation.
        self.buttonBox = gtk.HButtonBox()
        self.buttonBox.set_layout(gtk.BUTTONBOX_END)
        self.buttonBox.set_spacing(10)
        self.buttonBox.set_border_width(10)

        # Create the Back button, marking it insensitive by default since we
        # start at the first page.
        self.backButton = gtk.Button(use_underline=True, stock="gtk-go-back",
                                     label=_("_Back"))
        self._setBackSensitivity()
        self.backButton.connect("clicked", self._backClicked)
        self.buttonBox.pack_start(self.backButton)

        # Create the Forward button.
        self.nextButton = gtk.Button(use_underline=True, stock="gtk-go-forward",
                                     label=_("_Forward"))
        self.nextButton.connect("clicked", self._nextClicked)
        self.buttonBox.pack_start(self.nextButton)

        # Add the widgets into the right side.
        self.rightBox.pack_end(self.buttonBox, expand=False)

        # Add the widgets into the main hbox widget.
        self.mainHBox.pack_start(self.leftEventBox)
        self.mainHBox.pack_start(self.rightBox)

        self.win.add(self.mainHBox)
        self.win.connect("destroy", self.destroy)
        self.win.connect("key-release-event", self._keyRelease)

        return self.win

    def createScreens(self):
        """Call the createScreen method on all loaded modules.  This loads the
           UI elements for each page and stuffs the rendered page into a UI
           wrapper containing the module's title and icon.
        """
        for module in self.moduleList:
            try:
                module.createScreen()

                if isinstance(module, Module) and module.vbox is None:
                    logging.error("module %s did not set up its UI, removing" % module.title)
                    self.moduleList.remove(module)

                module.renderModule(self)
            except:
                self.moduleList.remove(module)
                self._displayException()
                continue

    def createSidebar(self):
        """Add the sidebarTitle from every module to the sidebar."""
        for module in self.moduleList:
            hbox = gtk.HBox(False, 5)
            pix = self._loadPixbuf("%s/%s" % (self.themeDir, "pointer-blank.png"))

            pixWidget = gtk.Image()
            pixWidget.set_from_pixbuf(pix)

            label = gtk.Label("")
            label.set_markup("<span foreground='#FFFFFF'><b>%s</b></span>" % module.sidebarTitle)
            label.set_alignment(0.0, 0.5)

            # Wrap the sidebar title if it's too long.
            label.set_line_wrap(True)
            (w, h) = self.leftEventBox.get_size_request()
            label.set_size_request((int)(w*0.8), -1)

            # Make sure the arrow is at the top of any wrapped line.
            alignment = gtk.Alignment(yalign=0.2)
            alignment.add(pixWidget)

            hbox.pack_start(alignment, False)
            hbox.pack_end(label, True)
            self.sidebar.pack_start(hbox, False, True, 3)

        # Initialize sidebar pointer
        self._setPointer(0)

    def destroy(self, *args):
        """Destroy the UI, but do not take any other action to quit firstboot."""
        gtk.main_quit()

    def displayModule(self):
        """Display the current module on the main portion of the screen.  This
           method should take into account that a module might be displayed
           already and should be removed first.
        """
        # Remove any module that was already being displayed.
        if len(self.rightBox.get_children()) == 2:
            oldModule = self.rightBox.get_children()[0]
            self.rightBox.remove(oldModule)

        # Initialize the module's UI (sync up with the state of some file on
        # disk, or whatever) and then pack it into the right side of the
        # screen for display.
        currentModule = self._control.moduleList[self._control.currentPage]

        currentModule.initializeUI()
        self.rightBox.pack_start(currentModule.vbox)
        self.win.show_all()

    def moveToPage(self, moduleTitle=None, pageNum=None):
        """Move to and display the page given either by title or page number.
           This method raises SystemError if neither is provided, or if no
           page is found.  It is safe to call this method from within the apply
           method of modules, unlike advance().
        """
        if moduleTitle is None and pageNum is None:
            logging.error("moveToPage must be given a module title or page number")
            raise SystemError, "moveToPage must be given a module title or page number"

        if moduleTitle is not None:
            pageNum = 0

            while True:
                try:
                    if self._control.moduleList[pageNum].title == moduleTitle:
                        break

                    pageNum += 1
                except IndexError:
                    logging.error("No module exists with the title %s" % moduleTitle)
                    raise SystemError, "No module exists with the title %s" % moduleTitle

        if pageNum == len(self._control.moduleList):
            if len(self._controlStack) > 1:
                self._controlStack.pop()
                self._control = self._controlStack[-1]
                self.moveToPage(pageNum=self._control.currentPage+1)
                return
            else:
                self._control.currentPage += 1
                return

        # Set this regardless so we know where we are on the way back out of
        # a ModuleSet.
        self._control.currentPage = pageNum

        if isinstance(self._control.moduleList[pageNum], ModuleSet):
            newControl = Control()
            newControl.currentPage = 0
            newControl.history = []
            newControl.moduleList = self._control.moduleList[pageNum].moduleList

            self._controlStack.append(newControl)
            self._control = newControl
        else:
            self._setBackSensitivity()

        self._setPointer(self._controlStack[0].currentPage)
        self.displayModule()

    def run(self):
        """Given an interface that has had all its UI components loaded and
           initialized, run the interface.  Because this method must call into
           the UI toolkit to handle events and such, it is assumed that this
           method does not exit until the UI is unloaded.  From this point on,
           all interaction must take place in callbacks.
        """
        self.displayModule()
        self.win.present()
        self.nextButton.grab_focus()
        gtk.main()

    def takeScreenshot(self):
        """Take a screenshot."""
        if not os.access(self._screenshotDir, os.R_OK):
            try:
                os.mkdir(self._screenshotDir)
            except:
                logging.error("unable to create the screenshot dir; skipping")
                return

        screenshot = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8,
                                    self._x_size, self._y_size)
        screenshot.get_from_drawable(gtk.gdk.get_default_root_window(),
                                     gtk.gdk.colormap_get_system(),
                                     0, 0, 0, 0, self._x_size, self._y_size)

        if screenshot:
            while True:
                sname = "screenshot-%04d.png" % self._screenshotIndex
                if not os.access("%s/%s" % (self._screenshotDir, sname), os.R_OK):
                    break

                self._screenshotIndex += 1

            screenshot.save("%s/%s" % (self._screenshotDir, sname), "png")
            self._screenshotIndex += 1
