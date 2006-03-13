import sys
sys.path.append('/usr/share/system-config-users/')

from gtk import *
import string
import os
import os.path
import time
import gtk
import gobject
import functions
import libuser
import rhpl.executil as executil
import userGroupCheck
from firstboot import start_process

from rhpl.translate import _, N_
from rhpl import translate
translate.textdomain("firstboot")

import crypt,random

def cryptPassword(password, useMD5 = 1):
    if useMD5:
        salt = "$1$"
        saltLen = 8
    else:
        salt = ""
        saltLen = 2

    for i in range(saltLen):
        salt = salt + random.choice (string.letters + string.digits + './')

    return crypt.crypt (password, salt)

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 110
    moduleName = _("Create User")
    windowName = moduleName

    def launch(self, doDebug = None):
        self.doDebug = doDebug
        self.admin = libuser.admin()
        self.nisFlag = None

        if doDebug:
            print "initializing newuser module"

        self.usernameEntry = gtk.Entry()
        self.fullnameEntry = gtk.Entry()
        self.passwordEntry = gtk.Entry()
        self.passwordEntry.set_visibility(False)
        self.confirmEntry = gtk.Entry()
        self.confirmEntry.set_visibility(False)
        
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        title_pix = functions.imageFromFile("create-user.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)
        internalVBox.set_spacing(10)

        label = gtk.Label(_("It is recommended that you create a 'username' for regular "
                            "(non-administrative) use of your system. To create a system 'username,' "
                            "please provide the information requested below."))

        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        internalVBox.pack_start(label, False, True)

        table = gtk.Table(2, 4)
        label = gtk.Label(_("_Username:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.usernameEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.usernameEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5, 5)

        label = gtk.Label(_("Full Nam_e:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.fullnameEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.fullnameEntry, 1, 2, 1, 2, gtk.SHRINK, gtk.FILL, 5, 5)

        label = gtk.Label(_("_Password:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.passwordEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 2, 3, gtk.FILL)
        table.attach(self.passwordEntry, 1, 2, 2, 3, gtk.SHRINK, gtk.FILL, 5, 5)

        label = gtk.Label(_("Confir_m Password:"))
        label.set_use_underline(True)
        label.set_mnemonic_widget(self.confirmEntry)
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 3, 4, gtk.FILL)
        table.attach(self.confirmEntry, 1, 2, 3, 4, gtk.SHRINK, gtk.FILL, 5, 5)

        internalVBox.pack_start(table, True, 15)

#        internalVBox.pack_start(gtk.HSeparator())

        align = gtk.Alignment()
        align.set(0.9, 0.5, 0.0, 1.0)
        align.set_size_request(-1, 30)
        internalVBox.pack_start(align, False)

        label = gtk.Label(_("If you need to use network authentication, such as Kerberos or NIS, "
                            "please click the Use Network Login button."))

        label.set_line_wrap(True)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        internalVBox.pack_start(label, False, True)


        authHBox = gtk.HBox()
        authButton = gtk.Button(_("Use Network _Login..."))
        authButton.connect("clicked", self.run_authconfig)
        align = gtk.Alignment()
        align.add(authButton)
        align.set(0.9, 0.5, 0.0, 1.0)
        authHBox.pack_start(align, True)
        internalVBox.pack_start(authHBox, True, True)

        self.vbox.pack_start(internalVBox, False, 15)

        users = self.admin.enumerateUsersFull()
        self.normalUsersList = []
        for userEnt in users:
            uidNumber = int(userEnt.get(libuser.UIDNUMBER)[0])
            if uidNumber == 500:
                self.usernameEntry.set_text(userEnt.get(libuser.USERNAME)[0])
                self.fullnameEntry.set_text(userEnt.get(libuser.GECOS)[0])

        return self.vbox, title_pix, self.moduleName

    def grabFocus(self):
        self.usernameEntry.grab_focus()

    def apply(self, notebook):
        if self.doDebug:
            return 0

        username = self.usernameEntry.get_text()
        username = string.strip(username)

        if username == "" and self.nisFlag != None:
            #If they've run authconfig, don't pop up messageDialog
            return 0
        
        if username == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE,
                                    (_("It is highly recommended that a personal user account be "
                                       "created.  If you continue without an account, you "
                                       "can only log in with the root account, which is reserved "
                                       "for administrative use only.")))

            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(True)

            dlg.add_button(_("_Continue"), 0)
            b = dlg.add_button(_("Create _account"), 1)
            b.grab_focus()

            rc = dlg.run()
            dlg.destroy()

            if rc == 0:
                return 0
            else:
                self.usernameEntry.grab_focus()
                return None

        if not userGroupCheck.isUsernameOk(username, self.usernameEntry):
            return None

        password = self.passwordEntry.get_text()
        confirm = self.confirmEntry.get_text()

        if not userGroupCheck.isPasswordOk(password, self.passwordEntry) or \
           not userGroupCheck.isPasswordOk(confirm, self.confirmEntry):
            return None

        if password != confirm:
            self.showErrorMessage(_("The passwords do not match.  Please enter "
                                    "the password again."))
            self.passwordEntry.set_text("")
            self.confirmEntry.set_text("")
            self.passwordEntry.grab_focus()
            return None
        
        elif len (password) < 6:
            self.showErrorMessage(_("The password is too short.  Please use at "
                                    "least 6 characters."))

            self.passwordEntry.set_text("")
            self.confirmEntry.set_text("")
            self.passwordEntry.grab_focus()                
            return None

        user = self.admin.lookupUserByName(username)

        if user != None and user.get(libuser.UIDNUMBER)[0] < 500:
            self.showErrorMessage(_("The username '%s' is a reserved system "
                                    "account.  Please specify another username."
                                    % username))
            self.usernameEntry.set_text("")
            self.usernameEntry.grab_focus()
            return None

        fullName = self.fullnameEntry.get_text()

        #Check for valid strings
        if not userGroupCheck.isNameOk(fullName, self.fullnameEntry):
            return None

        # Shouldn't create a user if there's already a home directory with
        # their name.
        try:
            os.path.stat("/home/%s" % username)

            self.showErrorMessage(_("A home directory for the username '%s' "
                                    "already exists.  Please specify another "
                                    "username." % username))
            self.usernameEntry.set_text("")
            self.usernameEntry.grab_focus()
            return None
        except:
            pass

        #If we get to this point, all the input seems to be valid.
        #Let's add the user.
        if user == None:
            #if the user doesn't already exist
            userEnt = self.admin.initUser(username)
        else:
            userEnt = user
            
        userEnt.set(libuser.GECOS, [fullName])

        groupEnt = self.admin.initGroup(username)
        gidNumber = groupEnt.get(libuser.GIDNUMBER)[0]
        userEnt.set(libuser.GIDNUMBER, [gidNumber])

        if user == None:
            self.admin.addUser(userEnt)
            self.admin.addGroup(groupEnt)
        else:
            self.admin.modifyUser(userEnt)
            self.admin.modifyGroup(groupEnt)
            
        self.admin.setpassUser(userEnt, self.passwordEntry.get_text(), 0)
        
        return 0

    def showErrorMessage(self, text):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(True)
        rc = dlg.run()
        dlg.destroy()
        return None

    def run_authconfig(self, *args):
        self.nisFlag = 1
        
        #Create a gtkInvisible dialog to block until up2date is complete
        i = gtk.Invisible ()
        i.grab_add ()

        #Run rhn_register so they can register with RHN
        pid = start_process("/usr/bin/authconfig-gtk", "--firstboot")

        flag = None
        while not flag:
            while gtk.events_pending():
                gtk.main_iteration_do()

            child_pid, status = os.waitpid(pid, os.WNOHANG)
            
            if child_pid == pid:
                flag = 1
            else:
                time.sleep(0.1)

        i.grab_remove ()
