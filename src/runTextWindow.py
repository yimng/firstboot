#!/usr/bin/python2.2

from snack import *
import textWindow

result = 0

while result != -1:
    screen = SnackScreen()
    result = textWindow.TextWindow()(screen)
    screen.finish()

