#!/usr/bin/python

import signal
import sys

sys.path.append('/home/devel/bfox/redhat/firstboot/src/modules')
import firewall


if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


app = firewall.childWindow()
app.stand_alone()
