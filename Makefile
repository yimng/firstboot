#License: GPL
#Copyright Red Hat Inc.  Jan 2002

PKGNAME=firstboot
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
CVSTAG=r$(subst .,-,$(VERSION))
SUBDIRS=po

MANDIR=/usr/share/man
PREFIX=/usr
DATADIR=${PREFIX}/share
PKGDATADIR=${DATADIR}/${PKGNAME}
PKGIMAGESDIR=${PKGDATADIR}/images

PAMD_DIR        = /etc/pam.d
SECURITY_DIR    =/etc/security/console.apps

default: subdirs

subdirs:
	for d in $(SUBDIRS); do make -C $$d; [ $$? = 0 ] || exit 1; done

install:
	mkdir -p $(INSTROOT)/usr/sbin
	mkdir -p $(INSTROOT)/etc/rc.d/init.d
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)$(PAMD_DIR)
	mkdir -p $(INSTROOT)$(SECURITY_DIR)
	mkdir -p $(INSTROOT)$(PKGDATADIR)/pixmaps
	mkdir -p $(INSTROOT)/usr/share/firstboot/modules
	install src/*.py $(INSTROOT)$(PKGDATADIR)
#	for py in src/*.py ; do \
#		sed -e s,@VERSION@,$(VERSION),g $${py} > $(INSTROOT)$(PKGDATADIR)/`basename $${py}` ; \
#	done

	install -m 775 firstboot.init $(INSTROOT)/etc/rc.d/init.d/firstboot
	install src/modules/*.py $(INSTROOT)$(PKGDATADIR)/modules
	install src/pixmaps/*.png $(INSTROOT)$(PKGDATADIR)/pixmaps
#	install src/${PKGNAME} $(INSTROOT)$(PKGDATADIR)/${PKGNAME}
	install ${PKGNAME}.pam $(INSTROOT)$(PAMD_DIR)/${PKGNAME}
	install ${PKGNAME}.console $(INSTROOT)$(SECURITY_DIR)/${PKGNAME}
	install -m 755 src/firstboot $(INSTROOT)/usr/sbin/firstboot

archive:
	cvs tag -cFR $(CVSTAG) .
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@CVSROOT=`cat CVS/Root`; cd /tmp; cvs -d $$CVSROOT export -r$(CVSTAG) ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar cvzf $$dir/${PKGNAME}-$(VERSION).tar.gz ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.gz
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@cd /tmp; cp -a ~/redhat/${PKGNAME} ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar cvzf $$dir/${PKGNAME}-$(VERSION).tar.gz ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

clean:
	@rm -fv *~
	@rm -fv *.pyc



