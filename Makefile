#License: GPL
#Copyright Red Hat Inc.  Jan 2004

PKGNAME=firstboot
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
CVSTAG=r$(subst .,_,$(VERSION)-$(RELEASE))
SUBDIRS=po

MANDIR=/usr/share/man
PREFIX=/usr
DATADIR=${PREFIX}/share
PKGDATADIR=${DATADIR}/${PKGNAME}
PKGIMAGESDIR=${PKGDATADIR}/images


default: subdirs

subdirs:
	for d in $(SUBDIRS); do make -C $$d; [ $$? = 0 ] || exit 1; done

install:
	mkdir -p $(INSTROOT)/usr/sbin
	mkdir -p $(INSTROOT)/etc/rc.d/init.d
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)$(PKGDATADIR)/pixmaps
	mkdir -p $(INSTROOT)/usr/share/firstboot/modules
	install src/*.py $(INSTROOT)$(PKGDATADIR)

	install -m 755 firstboot.init $(INSTROOT)/etc/rc.d/init.d/firstboot
	install src/modules/*.py $(INSTROOT)$(PKGDATADIR)/modules
	install src/pixmaps/*.png $(INSTROOT)$(PKGDATADIR)/pixmaps
	install -m 755 src/firstboot $(INSTROOT)/usr/sbin/firstboot
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE) INSTROOT=$(INSTROOT) MANDIR=$(MANDIR) install) \
		|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

archive:
	cvs tag -cFR $(CVSTAG) .
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@CVSROOT=`cat CVS/Root`; cd /tmp; cvs -d $$CVSROOT export -r$(CVSTAG) ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar cvjf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

snapsrc: create-snapshot
	@rpmbuild -ta --nodeps $(PKGNAME)-$(VERSION).tar.bz2

create-snapshot:
	@rm -rf /tmp/$(PKGNAME)
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@tag=`cvs status Makefile | awk ' /Sticky Tag/ { print $$3 } '` 2> /dev/null; \
        [ x"$$tag" = x"(none)" ] && tag=HEAD; \
        echo "*** Pulling off $$tag!"; \
        cd /tmp ; cvs -Q -d $(CVSROOT) export -r $$tag $(PKGNAME) || echo "Um... export aborted."
	@mv /tmp/$(PKGNAME) /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp ; tar --bzip2 -cSpf $(PKGNAME)-$(VERSION).tar.bz2 $(PKGNAME)-$(VERSION)
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@cp /tmp/$(PKGNAME)-$(VERSION).tar.bz2 .
	@rm -f /tmp/$(PKGNAME)-$(VERSION).tar.bz2
	@echo ""
	@echo "The final archive is in $(PKGNAME)-$(VERSION).tar.bz2"

local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.*
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@cd /tmp; cp -a ~/redhat/${PKGNAME} ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

clean:
	@rm -fv *~
	@rm -fv *.pyc


