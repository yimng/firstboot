#!/bin/sh


cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-keyboard
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-language
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-mouse
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-rootpassword
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-securitylevel
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-soundcard
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-nfs
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-samba
cvs status 2>/dev/null| grep Status | grep -v Up