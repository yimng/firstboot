from gtk import *
import string
import os
import time
import gtk
import gobject
import sys
import functions
import libuser
import kudzu

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

class childWindow:
    #You must specify a runPriority for the order in which you wish your module to run
    runPriority = 45
    moduleName = (_("Network Setup"))
    moduleClass = "reconfig"

    def launch(self, doDebug = None):
        self.doDebug = doDebug
        self.admin = libuser.admin()

        if doDebug:
            print "initializing networking module"

        self.usernameEntry = gtk.Entry()
        self.fullnameEntry = gtk.Entry()
        self.passwordEntry = gtk.Entry()
        self.passwordEntry.set_visibility(gtk.FALSE)
        self.confirmEntry = gtk.Entry()
        self.confirmEntry.set_visibility(gtk.FALSE)
        
        self.vbox = gtk.VBox()
        self.vbox.set_size_request(400, 200)

        title_pix = functions.imageFromFile("networking.png")

        internalVBox = gtk.VBox()
        internalVBox.set_border_width(10)
        internalVBox.set_spacing(10)

        label = gtk.Label(_("The following network devices have been detected on the system:"))

        label.set_line_wrap(gtk.TRUE)
        label.set_alignment(0.0, 0.5)
        label.set_size_request(500, -1)
        internalVBox.pack_start(label, FALSE, TRUE)

        self.deviceStore = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.deviceView = gtk.TreeView()
        self.deviceView.set_size_request(-1, 200)
        self.deviceView.set_model(self.deviceStore)
        self.deviceSW = gtk.ScrolledWindow()
        self.deviceSW.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.deviceSW.set_shadow_type(gtk.SHADOW_IN)
        self.deviceSW.add(self.deviceView)

        self.deviceBox = gtk.HBox()
        self.deviceBox.pack_start(self.deviceSW, gtk.TRUE)

        
        col = gtk.TreeViewColumn(_("Network Device"), gtk.CellRendererText(), text = 0)
        self.deviceView.append_column(col)
        col = gtk.TreeViewColumn(_("Boot protocol"), gtk.CellRendererText(), text = 1)        
        self.deviceView.append_column(col)
        
        internalVBox.pack_start(self.deviceBox, gtk.FALSE)
        self.updateLabels()

        networkButton = gtk.Button(_("_Change Network Configuration..."))
        networkButton.connect("clicked", self.run_neat)

        align = gtk.Alignment()
        align.add(networkButton)
        align.set(1.0, 0.5, 0.1, 1.0)
                             
        internalVBox.pack_start(align, gtk.FALSE)

        self.vbox.pack_start(internalVBox, gtk.FALSE, 15)

        users = self.admin.enumerateUsersFull()
        self.normalUsersList = []
        for userEnt in users:
            uidNumber = int(userEnt.get(libuser.UIDNUMBER)[0])
            if uidNumber == 500:
                self.usernameEntry.set_text(userEnt.get(libuser.USERNAME)[0])
                self.fullnameEntry.set_text(userEnt.get(libuser.GECOS)[0])

        return self.vbox, title_pix, self.moduleName

    def updateLabels(self):
        module_dict = {}
        lines = open("/etc/modules.conf").readlines()
        for line in lines:
            tokens = string.split(line)
            if string.strip(tokens[0]) == "alias" and string.strip(tokens[1][:3]) == "eth":
                module_dict[tokens[1]] = tokens[2]

        self.deviceStore.clear()
        
        for dev in module_dict.keys():
            path = '/etc/sysconfig/network-scripts/ifcfg-%s' % dev
            lines = open(path).readlines()
            bootproto = None
            for line in lines:
                if string.strip(line[:9]) == "BOOTPROTO":
                    key, value = string.split(line, "=")
                    key = string.strip(key)
                    value = string.strip(string.lower(value))
                    if value == "none":
                        iter = self.deviceStore.append()
                        self.deviceStore.set_value(iter, 0, dev)
                        self.deviceStore.set_value(iter, 1, (_("static")))
                    else:
                        iter = self.deviceStore.append()
                        self.deviceStore.set_value(iter, 0, dev)
                        self.deviceStore.set_value(iter, 1, value)

    def grabFocus(self):
        self.usernameEntry.grab_focus()

    def apply(self, notebook):
        if self.doDebug:
            return 0

        username = self.usernameEntry.get_text()
        username = string.strip(username)
        
        if username == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE,
                                    (_("It is highly recommended that a personal user account be "
                                       "created.  If you continue without an account, you "
                                       "can only log in with the root account, which is reserved "
                                       "for administrative use only.")))

            dlg.set_position(gtk.WIN_POS_CENTER)
            dlg.set_modal(gtk.TRUE)

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

        if not self.isUsernameOk(username, self.usernameEntry):
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
        
    def run_neat(self, *args):
        #Create a gtkInvisible dialog to block until up2date is complete
        i = gtk.Invisible ()
        i.grab_add ()

        #Run rhn_register so they can register with RHN
        pid = functions.start_process("/usr/bin/redhat-config-network")

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
        self.updateLabels()
