#!/usr/bin/python2.2

import os

def writeSysconfigFile(doDebug):
    #Write the /etc/sysconfig/firstboot file to tell firstboot not to run again
    if (not doDebug):
        fd = open("/etc/sysconfig/firstboot", "w")
        fd.write("RUN_FIRSTBOOT=NO\n")
        fd.close()

        #Turn off the firstboot init script
        path = "/sbin/chkconfig --level 35 firstboot off"
        os.system(path)
