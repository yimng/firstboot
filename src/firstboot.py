#!/usr/bin/python2.2

import sys
import os
import string
import signal
import time

sys.path.append("/usr/share/firstboot")

##
## I18N
## 
import gettext
gettext.bindtextdomain ("firstboot", "/usr/share/locale")
gettext.textdomain ("firstboot")
_=gettext.gettext

wm_pid = None
doDebug = None
doReconfig = None
FILENAME = "/etc/sysconfig/firstboot"

for arg in sys.argv:
    if arg == '--reconfig':
        print "starting reconfig mode"
        doReconfig = 1
    if arg == '--debug':
        print "starting with debugging options"
        doDebug = 1

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


def startWindowManager():    
    wm_pid = os.fork()

    if (not wm_pid):
        path = '/usr/bin/metacity'
        args = ['--display=:1']
        os.execvp(path, args)

    status = 0
    try:
        pid, status = os.waitpid (wm_pid, os.WNOHANG)
        
    except OSError, (errno, msg):
        print "in except"
        print __name__, "waitpid:", msg

    if status:
        raise RuntimeError, "Window manager failed to start"

    return wm_pid

def mergeXresources():
    path = "/usr/X11R6/bin/xrdb"

    merge_pid = os.fork()

    if not merge_pid:
        args = ['-merge /etc/X11/Xresources']
        os.execvp(path, args)

    status = 0
    try:
        pid, status = os.waitpid (merge_pid, os.WNOHANG)
        
    except OSError, (errno, msg):
        print __name__, "waitpid:", msg

    if status:
        raise RuntimeError, "Failed to merge Xresources"


def fork_off_server(xconfig =None):
#    tmp_config = tempfile.mktemp("xf86config")
#    verbose(_("Writing temporary config file to %s") % tmp_config)
#    xconfig.write(tmp_config)
    os.environ["DISPLAY"]=":1.0"
    args = ["/usr/X11R6/bin/XFree86", ':1', 'vt7', '-s', '1440', '-terminate', '-dpms', '-v', '-quiet']    

    serverpid = os.fork()
    if serverpid == 0: #child
        logFile = "/tmp/X-Test.log"
        try:
            err = os.open(logFile, os.O_RDWR | os.O_CREAT)
            if err < 0:
                sys.stderr.write(_("error opening /tmp/X.log\n"))
            else:
                os.dup2(err, 2)
                os.close(err)
        except:
            # oh well
            pass
        
        os.execv(args[0], args)
        sys.exit (1)
            
#    return (serverpid, tmp_config)
    return serverpid


#Let's check to see if firstboot should be run or not
#If we're in debug mode, run anyway.  Even if the file exists
if (not doDebug):
    #Well first, is this even being run as root?
    if os.getuid() > 0 or os.geteuid() > 0:
       print "You must be root to run firstboot."
       sys.exit(0)

    #We're not in debug mode, so do some checking
    #First, look and see if /etc/sysconfig/firstboot exists
    if os.access(FILENAME, os.R_OK):
        fd = open(FILENAME, 'r')
        lines = fd.readlines()
        fd.close()

        #If /etc/sysconfig/firstboot exists, parse the file
        #If we find 'RUN_FIRSTBOOT=NO' in the file, then don't run firstboot
        for line in lines:            
            line = string.strip(line)
            if (string.find(line, "RUN_FIRSTBOOT") > -1) and line[0] != "#":
                if string.find(line, "="):
                    key, value = string.split(line, "=")
		    value = string.strip(value)
                    if value == "NO":
                        #Firstboot should not be run
			print (_("Firstboot has already been run once on this system.\n"))
			print (_("In order to run firstboot from the command line, "
                                 "run the following commands:"))
			print ("1) rm /etc/sysconfig/firstboot")
			print ("2) /usr/sbin/firstboot\n")

			print (_("In order to run firstboot during system bootup, run the "
                                 "following commands:"))
			print ("1) rm /etc/sysconfig/firstboot")
			print ("2) chkconfig --level 5 firstboot on")
			print ("3) reboot")
                        os._exit(0)
                    
    else:
        #Firstboot has never been run before, so start it up
        pass

    #Let's see if /etc/reconfigSys exists.  If it does, we need to enter reconfig mode
    try:	
        os.stat("/etc/reconfigSys")
        #It exists, so set reconfig mode flag to 1
        doReconfig = 1
    except:
        #It doesn't exist, so set reconfig mode flag to 0
        doReconfig = 0

#If there's no X Server running, let's start one
if not os.environ.has_key('DISPLAY'):
    
     if os.access("/etc/X11/XF86Config", os.R_OK):
          #set the display environment variable
          os.environ['DISPLAY'] = ':1'

         try:
             server = fork_off_server()
         except:
             import traceback
             server = None
             (type, value, tb) = sys.exc_info()
             list = traceback.format_exception (type, value, tb)
             text = string.joinfields (list, "")
             print text

         if not server:
             print "X server failed"
             raise RuntimeError, "X server failed to start"

         count = 0

         sys.stdout.write(_("Waiting for X server to start...log located in /tmp/X.log\n"))
         sys.stdout.flush()

         for i in range(5):
             time.sleep(1)
             sys.stdout.write("%s..." % (i+1))
             sys.stdout.flush()
             
         while count < 10:
             sys.stdout.write(".")
             sys.stdout.flush()

             pid = 0
             try:
                 pid, status = os.waitpid(server, os.WNOHANG)
             except OSError, (errno, msg):
                 print __name__, "waitpid:", msg

             if pid:
                 raise RuntimeError, "X server failed to start"
             try:
                 os.stat("/tmp/.X11-unix/X1")
                 break
             except OSError:
                 pass
             time.sleep(1)
             count = count + 1


     wm_pid = None
     wm_pid = startWindowManager()
     mergeXresources()

if count < 10:
    import firstbootWindow
    firstbootWindow.firstbootWindow(wm_pid, doReconfig, doDebug)
else:
    print "Firstboot cannot start because of a problem with the X server."
    sys.exit(0)
