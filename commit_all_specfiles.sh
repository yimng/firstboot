#!/bin/sh

cd ..
cvs commit -m 'updated changelog and bump rev number' firstboot/firstboot.spec redhat-config-keyboard/redhat-config-keyboard.spec redhat-config-language/redhat-config-language.spec redhat-config-mouse/redhat-config-mouse.spec redhat-config-rootpassword/redhat-config-rootpassword.spec redhat-config-securitylevel/redhat-config-securitylevel.spec redhat-config-soundcard/redhat-config-soundcard.spec redhat-config-nfs/redhat-config-nfs.spec redhat-config-samba/redhat-config-samba.spec
