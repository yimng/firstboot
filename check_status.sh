#!/bin/sh

echo "Checking firstboot"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-keyboard
echo "Checking redhat-config-keyboard"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-language
echo "Checking redhat-config-language"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-mouse
echo "Checking redhat-config-mouse"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-rootpassword
echo "Checking redhat-config-rootpassword"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-securitylevel
echo "Checking redhat-config-securitylevel"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-soundcard
echo "Checking redhat-config-soundcard"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-nfs
echo "Checking redhat-config-nfs"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-samba
echo "Checking redhat-config-samba"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-date
echo "Checking redhat-config-date"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-kickstart
echo "Checking redhat-config-kickstart"
cvs status 2>/dev/null| grep Status | grep -v Up
cd ..
cd redhat-config-users
echo "Checking redhat-config-users"
cvs status 2>/dev/null| grep Status | grep -v Up
