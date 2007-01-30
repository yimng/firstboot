## functions.py - some helper functions
##
## Copyright (C) 2002, 2003 Red Hat, Inc.
## Copyright (C) 2002, 2003 Brent Fox <bfox@redhat.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

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
            raise

    if (height is not None and width is not None
        and height != pixbuf.get_height()
        and width != pixbuf.get_width()):
        pixbuf = pixbuf.scale_simple(height, width,
                                     gtk.gdk.INTERP_BILINEAR)

    (pixmap, mask) = pixbuf.render_pixmap_and_mask()
    pixmap.draw_pixbuf(gtk.gdk.GC(pixmap), pixbuf, 0, 0, 0, 0,
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
