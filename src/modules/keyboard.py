#!/usr/bin/python

from gtk import *
import string

class childWindow:
    runPriority = 2
    moduleName = "Keyboard"
    moduleClass = "reconfig"

    def __init__(self):
        self.clist = GtkCList()
     
    def fill_list(self, langDict, defaultLang, installedLangs):
        list = langDict.keys()
        for lang in installedLangs:
            if lang in list:                
                row = self.clist.append([langDict[lang]])
                if lang == defaultLang:
                    self.clist.select_row(row, 0)
                
    def launch(self):
        self.vbox = GtkVBox()
        label = GtkLabel("Please select the keyboard to use.")
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        self.vbox.pack_start(self.clist)
        l = GtkLabel("foo")
        return self.vbox

    def write_file(self):
        pass


    def stand_alone(self):
        toplevel = GtkWindow()
        toplevel.set_usize(300, 400)
        box = childWindow().launch()
        toplevel.add(box)
        toplevel.show_all()
        mainloop()
