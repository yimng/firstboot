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
from module import *
import loader

import logging

# XXX: This is currently unused.
class ModuleSet:
    """The base class for a set of firstboot modules.  This is an abstract
       class.  This class is a container that holds several related modules
       that may need their own special navigation.  The ModuleSet holds many
       of the same attributes as a Module, but with added responsibilities.
    """
    def __init__(self):
        """Create a new ModuleSet instance.  This method must be provided by
           all subclasses.  Instance attributes:

           mode         -- The mode of firstboot operation that this module
                           set should appear in.
           moduleList   -- The list of modules contained in this set.  This
                           list will be populated automatically.  It is for
                           read-only use here.
           path         -- The directory containing the modules within this
                           set.
           priority     -- An integer specifying when this module set should
                           be loaded and appear in firstboot.  The higher the
                           number, the later this set will be run.  All
                           modules with the same priority will be run
                           alphabetically by title.
           sidebarTitle -- The words that should appear in the firstboot
                           sidebar (the left side of the screen).  This should
                           be rather short.
        """

        if self.__class__ is ModuleSet:
            raise TypeError, "ModuleSet is an abstract class."

        self.mode = MODE_REGULAR
        self.moduleList = []
        self.path = None
        self.priority = 0
        self.sidebarTitle = None

    def createScreen(self):
        """A convenience method for running createScreen on all the modules
           contained within this set.  Subclasses do not typically need to
           override this method.
        """
        for module in self.moduleList:
            module.createScreen()

            if isinstance(module, Module) and module.vbox is None:
                logging.error("module %s did not set up its UI, removing" % module.title)
                self.moduleList.remove(module)

    def initializeUI(self):
        """A convenience method for running initializeUI on all the modules
           contained within this set.  Subclasses do not typically need to
           override this method.
        """
        for module in self.moduleList:
            module.initializeUI()

    def loadModules(self, mode=MODE_REGULAR):
        """Load all the modules contained by this module set.  Subclasses do
           not typically need to override this method.
        """
        if self.path is not None:
            self.moduleList = loader.loadModules(self.path, mode)

    def needsNetwork(self):
        """Does this module require the network to be active in order to run?
           By default, no modules need networking.  Subclasses requiring other
           behavoir should override this method.
        """
        return False

    def renderModule(self, interface):
        """A convenience method for running renderModule on all the modules
           contained within this set.  Subclasses do not typically need to
           override this method.
        """
        for module in self.moduleList:
            module.renderModule(interface)

    def shouldAppear(self):
        """Should this module appear in firstboot?  This method will be called
           after the module is loaded, but before any UI work is performed.
           If False, the screen will not be created and the module will not
           be displayed.  By default, all modules will be displayed.  Subclasses
           requiring other behavior should override this method.
        """
        return True
