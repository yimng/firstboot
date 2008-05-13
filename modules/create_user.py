#
# Chris Lumens <clumens@redhat.com>
#
# Copyright 2008 Red Hat, Inc.
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
import libuser
import os, string, sys, time
import os.path

from firstboot.config import *
from firstboot.constants import *
from firstboot.functions import *
from firstboot.module import *

from rhpl.translate import _, N_
import rhpl.translate as translate
translate.textdomain ("firstboot")

sys.path.append("/usr/share/system-config-users")
import userGroupCheck

def _chown(arg, dirname, names):
    for n in names:
        os.lchown("%s/%s" % (dirname, n), arg[0], arg[1])

class moduleClass(Module):
    def __init__(self):
        Module.__init__(self)
        self.priority = 100
        self.sidebarTitle = N_("Create User")
        self.title = N_("Create User")
        self.icon = "create-user.png"

        self.admin = libuser.admin()
        self.nisFlag = None

    def apply(self, interface, testing=False):
        if testing:
            return RESULT_SUCCESS

        username = self.usernameEntry.get_text()
        username = string.strip(username)

        if username == "" and self.nisFlag:
            # If they've run authconfig, don't pop up messageDialog
            return RESULT_SUCCESS

        if username == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE,
                                    _("It is highly recommended that a personal user account be "
                                      "created.  If you continue without an account, you "
                                      "can only log in with the root account, which is reserved "
                                      "for administrative use only."))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)

            dlg.add_button(_("_Continue"), 0)
            b = dlg.add_button(_("Create _account"), 1)
            b.grab_focus()

            rc = dlg.run()
            dlg.destroy()

            if rc == 0:
                return RESULT_SUCCESS
            else:
                self.usernameEntry.grab_focus()
                return RESULT_FAILURE

        if not userGroupCheck.isUsernameOk(username, self.usernameEntry):
            return RESULT_FAILURE

        password = self.passwordEntry.get_text()
        confirm = self.confirmEntry.get_text()

        if not password or not confirm:
            return RESULT_FAILURE

        if password != confirm:
            self._showErrorMessage(_("The passwords do not match.  Please enter "
                                     "the password again."))
            self.passwordEntry.set_text("")
            self.confirmEntry.set_text("")
            self.passwordEntry.grab_focus()
            return RESULT_FAILURE
        elif not userGroupCheck.isPasswordOk(password, self.passwordEntry):
            return RESULT_FAILURE

        user = self.admin.lookupUserByName(username)

        if user != None and user.get(libuser.UIDNUMBER)[0] < 500:
            self._showErrorMessage(_("The username '%s' is a reserved system "
                                     "account.  Please specify another username."
                                     % username))
            self.usernameEntry.set_text("")
            self.usernameEntry.grab_focus()
            return RESULT_FAILURE

        fullName = self.fullnameEntry.get_text()

        # Check for valid strings
        if not userGroupCheck.isNameOk(fullName, self.fullnameEntry):
            return RESULT_FAILURE

        # If a home directory for the user already exists, offer to reuse it
        # for the new user.
        try:
            os.stat("/home/%s" % username)

            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,
                                    _("A home directory for user %s already exists. "
                                      "Would you like to reuse this home directory?  "
                                      "If not, please choose a different username.") % username)
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)

            rc = dlg.run()
            dlg.destroy()

            if rc == gtk.RESPONSE_NO:
                self.usernameEntry.set_text("")
                self.usernameEntry.grab_focus()
                return RESULT_FAILURE

            mkhomedir = False
        except:
            mkhomedir = True

        # If we get to this point, all the input seems to be valid.
        # Let's add the user.
        if user == None:
            #if the user doesn't already exist
            userEnt = self.admin.initUser(username)
        else:
            userEnt = user

        userEnt.set(libuser.GECOS, [fullName])
        uidNumber = userEnt.get(libuser.UIDNUMBER)[0]

        groupEnt = self.admin.initGroup(username)
        gidNumber = groupEnt.get(libuser.GIDNUMBER)[0]
        userEnt.set(libuser.GIDNUMBER, [gidNumber])

        if user == None:
            self.admin.addUser(userEnt, mkhomedir=mkhomedir)
            self.admin.addGroup(groupEnt)

            if not mkhomedir:
                os.chown("/home/%s" % username, uidNumber, gidNumber)
                os.path.walk("/home/%s" % username, _chown, (uidNumber, gidNumber))
        else:
            self.admin.modifyUser(userEnt)
            self.admin.modifyGroup(groupEnt)
            os.chown(userEnt.get(libuser.HOMEDIRECTORY)[0],
                     userEnt.get(libuser.UIDNUMBER)[0],
                     userEnt.get(libuser.GIDNUMBER)[0])

        self.admin.setpassUser(userEnt, self.passwordEntry.get_text(), 0)

        return RESULT_SUCCESS

    def createScreen(self):
        self.vbox = gtk.VBox(spacing=5)

        label = gtk.Label(_("It is recommended that you create a 'username' for regular "
                            "(non-administrative) use of your system. To create a system 'username,' "
                            "please provide the information requested below."))

        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)

        self.usernameEntry = gtk.Entry()
        self.fullnameEntry = gtk.Entry()
        self.passwordEntry = gtk.Entry()
        self.passwordEntry.set_visibility(False)
        self.confirmEntry = gtk.Entry()
        self.confirmEntry.set_visibility(False)

        self.vbox.pack_start(label, False, True)

        table = gtk.Table(2, 4)
        label = gtk.Label(_("_Username:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.usernameEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.usernameEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5)

        label = gtk.Label(_("Full Nam_e:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.fullnameEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.fullnameEntry, 1, 2, 1, 2, gtk.SHRINK, gtk.FILL, 5)

        label = gtk.Label(_("_Password:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.passwordEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 2, 3, gtk.FILL)
        table.attach(self.passwordEntry, 1, 2, 2, 3, gtk.SHRINK, gtk.FILL, 5)

        label = gtk.Label(_("Confir_m Password:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.confirmEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 3, 4, gtk.FILL)
        table.attach(self.confirmEntry, 1, 2, 3, 4, gtk.SHRINK, gtk.FILL, 5)

        self.vbox.pack_start(table, False)

        label = gtk.Label(_("If you need to use network authentication, such as Kerberos or NIS, "
                            "please click the Use Network Login button."))

        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        self.vbox.pack_start(label, False, True, padding=20)

        authHBox = gtk.HBox()
        authButton = gtk.Button(_("Use Network _Login..."))
        authButton.connect("clicked", self._runAuthconfig)
        align = gtk.Alignment()
        align.add(authButton)
        align.set(0.9, 0.5, 0.0, 1.0)
        authHBox.pack_start(align, True)
        self.vbox.pack_start(authHBox, False, False)

    def initializeUI(self):
        pass

    def _runAuthconfig(self, *args):
        self.nisFlag = 1

        # Create a gtkInvisible to block until authconfig is done.
        i = gtk.Invisible()
        i.grab_add()

        pid = start_process("/usr/bin/authconfig-gtk", "--firstboot")

        while True:
            while gtk.events_pending():
                gtk.main_iteration_do()

            child_pid, status = os.waitpid(pid, os.WNOHANG)
            if child_pid == pid:
                break
            else:
                time.sleep(0.1)

        i.grab_remove()

    def _showErrorMessage(self, text):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(True)
        rc = dlg.run()
        dlg.destroy()
        return None
