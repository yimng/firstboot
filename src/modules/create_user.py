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
        label = gtk.Label("")
        label.set_markup("<span size='x-large'>%s</span>" % msg)
        label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse ("white"))
        label.set_alignment(0.4, 0.5)

        titleBox = gtk.HBox()

        pix = functions.imageFromFile("create-user.png")
        titleBox.pack_start(pix, gtk.FALSE, gtk.TRUE, 5)

        titleBox.pack_start(label)

        eventBox = gtk.EventBox()
        eventBox.add(titleBox)
        self.vbox.pack_start(eventBox, FALSE)

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

        return self.vbox, eventBox

    def grabFocus(self):
        self.usernameEntry.grab_focus()

    def apply(self, notebook):
        if self.doDebug:
            return 0

        username = self.usernameEntry.get_text()

        if username == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_YES_NO,
                                    (_("A user account was not created.  Are you sure that you want " \
                                       "to continue without creating a user account?.")))
            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            dlg.destroy()

            if rc == gtk.RESPONSE_YES:
                return 0
            else:
                return None

        if self.passwordEntry.get_text() != self.confirmEntry.get_text():
            self.showErrorMessage(_("The passwords do not match.  Please enter the password again."))
            self.passwordEntry.set_text("")
            self.confirmEntry.set_text("")
            self.passwordEntry.grab_focus()
            return None
        
        user = self.admin.lookupUserByName(username)

        if user != None:
            self.showErrorMessage(_("An account with username %s already exists.  Please " \
                                    "specify another username." % username))
            self.usernameEntry.set_text("")
            self.usernameEntry.grab_focus()
            return None

        #If we get to this point, all the input seems to be valid.  Let's add the user
        userEnt = self.admin.initUser(username)
        userEnt.set(libuser.GECOS, [self.fullnameEntry.get_text()])

        groupEnt = self.admin.initGroup(username)
        gidNumber = groupEnt.get(libuser.GIDNUMBER)[0]
        userEnt.set(libuser.GIDNUMBER, [gidNumber])


        self.admin.addUser(userEnt)
        self.admin.setpassUser(userEnt, self.passwordEntry.get_text(), 0)
        self.admin.addGroup(groupEnt)
        
        return 0

    def showErrorMessage(self, text):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(gtk.TRUE)
        rc = dlg.run()
        dlg.destroy()
        return None
        
