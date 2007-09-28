PKGNAME=firstboot
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
CVSTAG=r$(subst .,_,$(VERSION)-$(RELEASE))

PREFIX=/usr
DATADIR=${PREFIX}/share/firstboot
MODULESDIR=${DATADIR}/modules
THEMESDIR=${DATADIR}/themes

PYCHECKEROPTS=--no-shadowbuiltin --no-argsused --no-miximport --maxargs 0 --no-local -\# 0 --only

default: all

all:
	$(MAKE) -C po

check:
	PYTHONPATH=. pychecker $(PYCHECKEROPTS) firstboot/*.py firstboot/modules/*.py

clean:
	-rm firstboot/*.pyc firstboot/modules/*.pyc
	$(MAKE) -C po clean
	-rm ${PKGNAME}-$(VERSION).tar.bz2

install: all
	mkdir -p $(INSTROOT)/usr/sbin
	mkdir -p $(INSTROOT)/etc/rc.d/init.d
	mkdir -p $(INSTROOT)/${DATADIR}
	mkdir -p $(INSTROOT)/${MODULESDIR}
	mkdir -p $(INSTROOT)/${THEMESDIR}

	install src/*.py $(INSTROOT)/${DATADIR}
	install src/modules/ $(INSTROOT)/${MODULESDIR}
	install themes/ $(INSTROOT)/${THEMESDIR}

	install -m 755 firstboot.init $(INSTROOT)/etc/rc.d/init.d/firstboot
	install -m 755 firstboot $(INSTROOT)/usr/sbin/
	$(MAKE) -C po install

tag:
	cvs tag -FR $(CVSTAG)

archive: tag
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@CVSROOT=`cat CVS/Root`; cd /tmp; cvs -d $$CVSROOT export -r$(CVSTAG) ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar -cvjf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.bz2
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@dir=$$PWD; cp -a $$dir /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

.PHONY: check clean install tag archive local
