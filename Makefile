PKGNAME=firstboot
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
TAG=r$(VERSION)-$(RELEASE)

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
	-rm src/*.pyc src/modules/*.pyc
	-rm ${PKGNAME}-$(VERSION).tar.bz2
	$(MAKE) -C po clean

install: all
	mkdir -p $(INSTROOT)/usr/sbin
	mkdir -p $(INSTROOT)/etc/rc.d/init.d
	mkdir -p $(INSTROOT)/${DATADIR}
	mkdir -p $(INSTROOT)/${MODULESDIR}
	mkdir -p $(INSTROOT)/${THEMESDIR}

	install -m 644 src/*.py $(INSTROOT)/${DATADIR}
	cp -r src/modules/* $(INSTROOT)/${MODULESDIR}
	cp -r themes/* $(INSTROOT)/${THEMESDIR}

	install -m 755 firstboot.init $(INSTROOT)/etc/rc.d/init.d/firstboot
	install -m 755 firstboot $(INSTROOT)/usr/sbin/
	$(MAKE) -C po install

tag:
	git tag -f $(TAG)

archive: tag
	git-archive --format=tar --prefix=${PKGNAME}-$(VERSION)/ $(TAG) > ${PKGNAME}-$(VERSION).tar
	bzip2 ${PKGNAME}-$(VERSION).tar
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.bz2
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@dir=$$PWD; cp -a $$dir /tmp/${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)/.git
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

.PHONY: check clean install tag archive local
