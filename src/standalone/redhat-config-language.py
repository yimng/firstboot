#!/usr/bin/python

import language
import signal

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)


app = language.childWindow()
app.stand_alone()
