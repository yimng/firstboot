#
# constants_text.py: text mode constants
#
# Copyright 2000-2002 Red Hat, Inc.
#
# This software may be freely redistributed under the terms of the GNU
# library public license.
#
# You should have received a copy of the GNU Library Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

from rhpl.translate import _, N_

INSTALL_OK = 0
INSTALL_BACK = -1
INSTALL_NOOP = -2

class Translator:
    """A simple class to facilitate on-the-fly translation for newt buttons"""
    def __init__(self, button, check):
        self.button = button
        self.check = check

    def __getitem__(self, which):
        if which == 0:
            return _(self.button)
        elif which == 1:
            return self.check
        raise IndexError

    def __len__(self):
        return 2

TEXT_EXIT_STR = N_("Exit")
TEXT_EXIT_CHECK  = "exit"
TEXT_EXIT_BUTTON = Translator(TEXT_EXIT_STR, TEXT_EXIT_CHECK)
