#!/usr/bin/python2.2

import gtk
import os

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

def pixbufFromFile(filename):
    pixbuf = None
    try:
        path = "pixmaps/" + filename
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    except:
        try:
            path = "/usr/share/firstboot/pixmaps/" + filename
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        except:
            pass

    return pixbuf

def pixbufFromPath(filename):
    pixbuf = None
    try:
        path = filename
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    except:
        pass

    return pixbuf

# Attempt to load a gtk.Image from a file.
def ditheredImageFromFile(filename, height = None, width = None):
    try:
        path = "pixmaps/" + filename
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    except:
        try:
            path = "/usr/share/firstboot/pixmaps/" + filename
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        except:
            pass

    if (height is not None and width is not None
        and height != pixbuf.get_height()
        and width != pixbuf.get_width()):
        pixbuf = pixbuf.scale_simple(height, width,
                                     gtk.gdk.INTERP_BILINEAR)

    (pixmap, mask) = pixbuf.render_pixmap_and_mask()
    pixbuf.render_to_drawable(pixmap, gtk.gdk.gc_new(pixmap), 0, 0, 0, 0,
                              pixbuf.get_width(), pixbuf.get_height(),
                              gtk.gdk.RGB_DITHER_MAX, 0, 0)

    pix = gtk.Image()
    pix.set_from_pixmap(pixmap, mask)
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

def start_process(path):
    args = [path]

    child = os.fork()

    if not child:
        os.execvp(path, args)
        os._exit(1)
            
    return child

