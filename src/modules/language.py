#!/usr/bin/python

from gtk import *
import string

class childWindow:
    runPriority = 1
    moduleName = "Language"
    moduleClass = "reconfig"

    def __init__(self):
        self.clist = GtkCList()

        langDict = self.read_table()
        defaultLang, installedLangs = self.get_installed_langs()
        self.fill_list(langDict, defaultLang, installedLangs)

    def fill_list(self, langDict, defaultLang, installedLangs):
        list = langDict.keys()
        for lang in installedLangs:
            if lang in list:                
                row = self.clist.append([langDict[lang]])
                if lang == defaultLang:
                    self.clist.select_row(row, 0)
                
    def launch(self):
        self.vbox = GtkVBox()
        label = GtkLabel("Please select the language to use.")
        self.vbox.pack_start(label, FALSE, TRUE, 30)
        self.vbox.pack_start(self.clist)
        l = GtkLabel("foo")
        return self.vbox

    def get_installed_langs(self):
        fd = open("/etc/sysconfig/i18n", "r")
#        fd = open("i18n", "r")
        lines = fd.readlines()
        for line in lines:
            if line[:4] == "LANG":
                defaultLang = string.replace(line[5:], '"', '')
                defaultLang = string.strip(defaultLang)
            if line[:9] == "SUPPORTED":
                langs = string.replace(line[10:], '"', '')
                langs = string.strip(langs)
                langs = string.split(langs, ':')
        return defaultLang, langs


    def read_table(self):
        avail_langs = {}

        fd = open("lang-table", "r")
        lines = fd.readlines()
        for line in lines:
            tokens = string.split(line)
            avail_langs[tokens[4]] = tokens[0]

        fd.close()
        return avail_langs

    def write_file(self):
        pass


    def apply(self):
        print "applying language"
        pass

    def stand_alone(self):
        toplevel = GtkWindow()
        toplevel.set_usize(300, 400)
        box = childWindow().launch()
        toplevel.add(box)
        toplevel.show_all()
        mainloop()
