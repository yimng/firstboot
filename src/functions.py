import gtk

def loadPixbuf(fn):
    return gtk.gdk.pixbuf_new_from_file(fn)

def loadToImage(fn):
    pix = loadPixbuf(fn)

    pixWidget = gtk.Image()
    pixWidget.set_from_pixbuf(pix)
    return pixWidget
