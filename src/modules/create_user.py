from gtk import *
import string
import gtk
import gobject
import sys
import functions
import libuser

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 80
    moduleName = (_("Create A User"))

    def launch(self, doDebug = None):
        self.doDebug = doDebug
        self.admin = libuser.admin()

        if doDebug:
            print "initializing newuser module"

        self.usernameEntry = gtk.Entry()
        self.fullnameEntry = gtk.Entry()
        self.passwordEntry = gtk.Entry()
        self.passwordEntry.set_visibility(gtk.FALSE)
        self.confirmEntry = gtk.Entry()
        self.confirmEntry.set_visibility(gtk.FALSE)
        
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        msg = (_("Create A User"))

        title_pix = functions.imageFromFile("create-user.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)

        label = gtk.Label(_("A user account is required to use the system.  "
                            "Create a user account by filling in the information below."))

        label.set_line_wrap(gtk.TRUE)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        internalVBox.pack_start(label, FALSE, TRUE)

        table = gtk.Table(2, 4)
        label = gtk.Label(_("Username:"))
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 0, 1, gtk.FILL)
        table.attach(self.usernameEntry, 1, 2, 0, 1, gtk.SHRINK, gtk.FILL, 5, 5)

        label = gtk.Label(_("Full Name:"))
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 1, 2, gtk.FILL)
        table.attach(self.fullnameEntry, 1, 2, 1, 2, gtk.SHRINK, gtk.FILL, 5, 5)

        label = gtk.Label(_("Password:"))
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 2, 3, gtk.FILL)
        table.attach(self.passwordEntry, 1, 2, 2, 3, gtk.SHRINK, gtk.FILL, 5, 5)

        label = gtk.Label(_("Confirm Password:"))
        label.set_alignment(0.0, 0.5)
        table.attach(label, 0, 1, 3, 4, gtk.FILL)
        table.attach(self.confirmEntry, 1, 2, 3, 4, gtk.SHRINK, gtk.FILL, 5, 5)

        internalVBox.pack_start(table, gtk.TRUE, 15)
        self.vbox.pack_start(internalVBox, gtk.FALSE, 5)

        users = self.admin.enumerateUsersFull()
        self.normalUsersList = []
        for userEnt in users:
            uidNumber = int(userEnt.get(libuser.UIDNUMBER)[0])
            if uidNumber == 500:
                self.usernameEntry.set_text(userEnt.get(libuser.USERNAME)[0])
                self.fullnameEntry.set_text(userEnt.get(libuser.GECOS)[0])

        return self.vbox, title_pix, msg

    def grabFocus(self):
        self.usernameEntry.grab_focus()

    def apply(self, notebook):
        if self.doDebug:
            return 0

        username = self.usernameEntry.get_text()

        if not self.isUsernameOk(username, self.usernameEntry):
            return None

        if username == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,
                                    (_("A user account was not created.  Are you sure that you want " \
                                       "to continue without creating a user account?")))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            dlg.destroy()

            if rc == gtk.RESPONSE_YES:
                return 0
            else:
                self.usernameEntry.grab_focus()
                return None

        password = self.passwordEntry.get_text()
        confirm = self.confirmEntry.get_text()

        #Check for ascii-only strings
        if not self.isPasswordOk(password, self.passwordEntry):
            return None
        
        if not self.isPasswordOk(confirm, self.confirmEntry):
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
            self.showErrorMessage(_("The username '%s' is a reserved system account.  Please " \
                                    "specify another username." % username))
            self.usernameEntry.set_text("")
            self.usernameEntry.grab_focus()
            return None

        fullName = self.fullnameEntry.get_text()

        #Check for ascii-only strings
        if not self.isNameOk(fullName, self.fullnameEntry):
            return None

        #If we get to this point, all the input seems to be valid.  Let's add the user
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
        dlg.set_modal(gtk.TRUE)
        rc = dlg.run()
        dlg.destroy()
        return None
        
    def isUsernameOk(self, str, widget):
        tag = _("user name")
        for i in str:
            if i in string.whitespace:
                #Check for whitespace
                self.showErrorMessage(_("The %s '%s' contains whitespace.  "
                                        "Please do not include whitespace in the %s.")
                                      % (tag, str, tag))
                widget.set_text("")
                widget.grab_focus()
                return None
                
            if i not in string.ascii_letters:
                if i not in string.digits:
                    self.showErrorMessage(_("The %s '%s' contains non-ASCII "
                                            "characters.  Please use only ASCII characters.")
                                          % (tag, str))
                    widget.set_text("")
                    widget.grab_focus()
                    return None
        return 1

    def isPasswordOk(self, str, widget):
        tag = _("password")
        for i in str:
            if i not in string.ascii_letters:
                if i not in string.digits:
                    self.showErrorMessage(_("The %s contains non-ASCII characters.  "
                                            "Please use only ASCII characters.") % tag)
                    widget.set_text("")
                    widget.grab_focus()
                    return None
        return 1

    def isNameOk(self, str, widget):
        tag = ("name")
        for i in str:
            if i not in string.ascii_letters:
                if i not in string.digits:
                    #have to check for whitespace for gecos, since whitespace is ok
                    if i not in string.whitespace:
                        self.showErrorMessage(_("The %s '%s' contains non-ASCII characters.  "
                                                "Please use only ASCII characters.")
                                              % (tag, str))
                        widget.set_text("")
                        widget.grab_focus()
                        return None
        return 1

