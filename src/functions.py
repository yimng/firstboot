#!/usr/bin/python2.2

import gtk

# Attempt to load a gtk.Image from a file.
def imageFromFile(filename):
    p = None        
    try:
        path = "pixmaps/" + filename
        p = gtk.gdk.pixbuf_new_from_file(path)
    except:
        try:
            path = "/usr/share/firstboot/pixmaps/" + filename
            p = gtk.gdk.pixbuf_new_from_file(path)
        except:
            pass

    if p:
        pix = gtk.Image()
        pix.set_from_pixbuf(p)        
        return pix

def imageFromPath(filename):
    p = None        
    try:
        path = filename
        p = gtk.gdk.pixbuf_new_from_file(path)
    except:
        pass

    if p:
        pix = gtk.Image()
        pix.set_from_pixbuf(p)        
        return pix
