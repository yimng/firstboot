#!/usr/bin/python

import signal
import sys

sys.path.append('/home/bfox/redhat/firstboot/modules')
print sys.path
import keyboard


if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


app = keyboard.childWindow()
app.stand_alone()
