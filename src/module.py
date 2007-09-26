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
from constants import *
import gtk

class Module:
    """The base class for all firstboot modules.  This is an abstract class.
       Subclasses of this one should define a single screen that may appear
       in firstboot.
    """
    def __init__(self):
        """Create a new Module instance.  This method must be provided by
           all subclasses.  Instance attributes:

           icon         -- Any icon that should appear next to the title.
           mode         -- The mode of firstboot operation that this module
                           should appear in.
           priority     -- An integer specifying when this module should
                           be loaded and appear in firstboot.  The higher the
                           number, the later this module will be run.  All
                           modules with the same priority will be run
                           alphabetically by title.
           sidebarTitle -- The words that should appear in the firstboot
                           sidebar (the left side of the screen).  This should
                           be rather short.
           title        -- The title of the module that should appear in
                           large bold letters at the top of the screen.
           vbox         -- A reference to a gtk.VBox, which is the top-level
                           UI widget for each module.  It is up to the module's
                           createScreen method to set this up.
        """

        if self.__class__ is Module:
            raise TypeError, "Module is an abstract class."

        self.icon = None
        self.mode = MODE_REGULAR
        self.priority = 0
        self.sidebarTitle = None
        self.title = None
        self.vbox = None

    def apply(self, interface, testing=False):
        """Called when the Next button is clicked on the interface.  This
           method takes whatever action is appropriate based on the state
           of the UI.  This can include writing things to disk or running
           programs.  It returns any of the RESULT_* values from constants.
           This method must be provided by all subclasses.

           interface -- A reference to the running Interface class.
           testing   -- If True, this method must not make any permanent
                        changes to disk.
        """
        raise TypeError, "apply() not implemented for Module."

    def createScreen(self):
        """Create the UI elements required for this module, but do not take
           any action or write anything to disk.  This method must set up the
           self.vbox attribute but does not return anything.  This method
           must be provided by all subclasses.
        """
        raise TypeError, "createScreen() not implemented for Module."

    def initializeUI(self):
        """Synchronizes the state of the UI with whatever's present on disk
           or wherever else the module looks for its defaults.  This method
           will be called after createScreen.  This method must be provided
           by all subclasses.
        """
        raise TypeError, "initializeUI() not implemented for Module."

    def needsNetwork(self):
        """Does this module require the network to be active in order to run?
           By default, no modules need networking.  Subclasses requiring other
           behavoir should override this method.
        """
        return False

    def needsReboot(self):
        """Does whatever action happened in this module's apply() method
           require rebooting the computer?  By default, no modules require
           rebooting.  Subclasses requiring other behavior should override
           this method.
        """
        return False

    def renderModule(self, interface):
        """Wrap the module's top-level UI element in the other elements
           required to make sure all modules have the same common look.  This
           method should not be overridden by any subclass.
        """
        # Create the large label that goes at the top of the right side.
        label = gtk.Label("")
        label.set_alignment(0.0, 0.5)
        label.set_markup("<span foreground='#000000' size='30000' font_family='Helvetica'><b>%s</b></span>" % self.title)

        titleBox = gtk.HBox()

        if self.icon:
            titleBox.pack_start(interface._loadPixbuf("%s/%s" % (modulePath, self.icon)), False)

        titleBox.pack_start(label, True)
        titleBox.set_spacing(8)

        self.vbox.pack_start(titleBox, False)
        self.vbox.reorder_child(titleBox, 0)

    def shouldAppear(self):
        """Should this module appear in firstboot?  This method will be called
           after the module is loaded, but before any UI work is performed.
           If False, the screen will not be created and the module will not
           be displayed.  By default, all modules will be displayed.  Subclasses
           requiring other behavior should override this method.
        """
        return True
