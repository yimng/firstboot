Summary: Initial system configuration utility
Name: firstboot
Version: 1.3.14
Release: 1
URL: http://fedora.redhat.com/projects/config-tools/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Source0: %{name}-%{version}.tar.bz2
Obsoletes: anaconda-reconfig
Prereq: chkconfig, /etc/init.d
BuildPreReq: gettext
Requires: pygtk2
Requires: python
Requires: usermode >= 1.36
Requires: metacity
Requires: rhpl
Requires: system-config-date
Requires: system-config-display
Requires: system-config-language
Requires: system-config-keyboard
Requires: system-config-soundcard
Requires: system-config-securitylevel
Requires: system-config-rootpassword
Requires: system-config-packages
Requires: system-config-network
Requires: authconfig-gtk
Requires: libuser
Requires: up2date
Requires: redhat-logos
Requires: redhat-artwork
Requires: xsri
ExcludeArch: s390 s390x

%description
The firstboot utility runs after installation.  It 
guides the user through a series of steps that allows for easier 
configuration of the machine. 

%prep
%setup -q

%build
make

%install
make INSTROOT=$RPM_BUILD_ROOT install

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! [ -f /etc/sysconfig/firstboot ]
then
  chkconfig --add firstboot
fi
		
%preun
if [ $1 = 0 ]; then
  rm -rf /usr/share/firstboot/*.pyc
  rm -rf /usr/share/firstboot/modules/*.pyc
  chkconfig --del firstboot
fi

%files -f %{name}.lang
%defattr(-,root,root)
#%doc COPYING
#%doc doc/*
%config /etc/rc.d/init.d/firstboot
%dir /usr/share/firstboot/
/usr/share/firstboot/*
/usr/sbin/firstboot

%changelog
* Wed May 12 2004 Elliot Lee <sopwith@redhat.com> 1.3.14-1
- Fix initscript (#121489)

* Mon May  3 2004 Brent Fox <bfox@redhat.com> 1.3.13-1
- fix Norwegian translation bug (bug #122206)

* Thu Apr 22 2004 Brent Fox <bfox@redhat.com> 1.3.12-1
- look for xorg.conf, not XF86Config (bug #121489)

* Thu Apr 15 2004 Brent Fox <bfox@redhat.com> 1.3.11-1
- fix bug #120669

* Wed Apr  7 2004 Brent Fox <bfox@redhat.com> 1.3.10-2
- allow for correct text mode button translations (bug #120087)

* Wed Mar 17 2004 Jeremy Katz <katzj@redhat.com> 1.3.10-1
- fix password to be encrypted properly

* Wed Mar 17 2004 Jeremy Katz <katzj@redhat.com> 1.3.9-1
- more workarounds for selinux (don't use libuser at all for create_user.py 
  for right now)

* Wed Mar 17 2004 Brent Fox <bfox@redhat.com> 1.3.8-1
- workaround selinux - patch from jeremy

* Tue Mar  9 2004 Brent Fox <bfox@redhat.com> 1.3.7-2
- fix typo (bug #117867)

* Mon Mar  8 2004 Brent Fox <bfox@redhat.com> 1.3.7-1
- drop the verbose print statements

* Thu Mar  4 2004 Brent Fox <bfox@redhat.com> 1.3.6-1
- only call chkconfig -add if /etc/sysconfig/firstboot does not exist

* Mon Mar  1 2004 Brent Fox <bfox@redhat.com> 1.3.5-2
- remove Requires on system-config-mouse

* Tue Feb 17 2004 Brent Fox <bfox@redhat.com> 1.3.5-1
- call self.win.present() to allow initial keyboard input

* Mon Feb 16 2004 Brent Fox <bfox@redhat.com> 1.3.4-1
- UTF-8ify fr.po
- make sure the root window stays on the bottom (bug #105631)

* Tue Jan 27 2004 Tim Powers <timp@ragnarok.devel.redhat.com> 1.3.3-3
- fedora-logos -> redhat-logos since redhat-logos is a virtual
  provides (used so that we can switch out redhat-logos with
  fedora-logos easily). Will change to system-logos once the changes
  have been made.

* Fri Jan 23 2004 Bill Nottingham <notting@redhat.com> 1.3.3-2
- some more s/redhat/system/ on requires

* Mon Dec  1 2003 Brent Fox <bfox@redhat.com> 1.3.2-2
- redhat-logos hasn't been renamed to system-logos yet

* Mon Nov 24 2003 Brent Fox <bfox@redhat.com> 1.3.2-1
- make changes for Python2.3

* Sun Nov 23 2003 Brent Fox <bfox@redhat.com> 1.3.2-1
- update Requires for system-config name change
- make changes for Python2.3

* Mon Oct 27 2003 Brent Fox <bfox@redhat.com> 1.3.1-1
- fix initscript for text mode

* Fri Oct 24 2003 Brent Fox <bfox@redhat.com> 1.3.1-1
- bump version
- use CVS head now for Fedora Core 2
- made firstboot-cambridge branch for Fedora Core 1
- first stab at text mode

* Wed Oct 15 2003 Brent Fox <bfox@redhat.com> 1.2.4-1
- pull lightrays.png from a different location

* Wed Oct  8 2003 Brent Fox <bfox@redhat.com> 1.2.3-1
- override rhgb's background

* Wed Oct  8 2003 Brent Fox <bfox@redhat.com> 1.2.2-1
- remove up2date module from Fedora

* Mon Sep 22 2003 Brent Fox <bfox@redhat.com> 1.2.1-1
- remove some items from the additional cd's screen for now
- remove some references to Red Hat Linux from welcome.py and up2date.py

* Fri Aug 29 2003 Brent Fox <bfox@redhat.com> 1.1.16-2
- bump relnum and rebuild

* Fri Aug 29 2003 Brent Fox <bfox@redhat.com> 1.1.16-1
- call authconfig with --firstboot flag correctly (bug #103367)

* Thu Aug 28 2003 Brent Fox <bfox@bfox.devel.redhat.com> 1.1.15-2
- bump relnum and rebuild

* Thu Aug 28 2003 Brent Fox <bfox@bfox.devel.redhat.com> 1.1.15-1
- handle network timeouts better in the date.py screen

* Thu Aug 28 2003 Brent Fox <bfox@bfox.devel.redhat.com> 1.1.14-1
- handle cds without autorun files better in additional_cds.py

* Thu Aug 21 2003 Brent Fox <bfox@redhat.com> 1.1.13-3
- bump relnum and rebuild

* Thu Aug 21 2003 Brent Fox <bfox@redhat.com> 1.1.13-2
- bump relnum and rebuild

* Thu Aug 21 2003 Brent Fox <bfox@redhat.com> 1.1.13-1
- pass --firstboot flag to authconfig-gtk in create_user.py

* Tue Aug 19 2003 Brent Fox <bfox@redhat.com> 1.1.12-2
- bump relnum and rebuild

* Tue Aug 19 2003 Brent Fox <bfox@redhat.com> 1.1.12-1
- fix formatting bug in create_user.py

* Fri Aug 15 2003 Brent Fox <bfox@redhat.com> 1.1.11-2
- bump relnum and rebuild

* Fri Aug 15 2003 Brent Fox <bfox@redhat.com> 1.1.11-1
- run 'chkconfig --del firstboot' when it's done

* Thu Aug 14 2003 Brent Fox <bfox@redhat.com> 1.1.10-1
- allow underscores and dashes in usernames (bug #99115)

* Wed Aug 13 2003 Brent Fox <bfox@redhat.com> 1.1.9-1
- replace BuildRequires on python-tools with gettext

* Thu Jul 31 2003 Brent Fox <bfox@redhat.com> 1.1.8-2
- bump relnum and rebuild

* Thu Jul 31 2003 Brent Fox <bfox@redhat.com> 1.1.8-1
- apply patch from hfuchi@redhat.com for Japanese translation

* Thu Jul 31 2003 Brent Fox <bfox@redhat.com> 1.1.7-2
- bump relnum and rebuild

* Thu Jul 31 2003 Brent Fox <bfox@redhat.com> 1.1.7-1
- change runPriority in welcome module

* Tue Jul 22 2003 Brent Fox <bfox@redhat.com> 1.1.6-2
- bump relnum and rebuild

* Tue Jul 22 2003 Brent Fox <bfox@redhat.com> 1.1.6-1
- resolve conflict between "Next" and "Forward" (bug #100498)

* Fri Jul 18 2003 Brent Fox <bfox@redhat.com> 1.1.5-2
- bump relnum and rebuild

* Fri Jul 18 2003 Brent Fox <bfox@redhat.com> 1.1.5-1
- fix conficting nmemonics (bug #99279)

* Wed Jul  2 2003 Brent Fox <bfox@redhat.com> 1.1.4-2
- bump relnum and rebuild

* Wed Jul  2 2003 Brent Fox <bfox@redhat.com> 1.1.4-1
- remove unneeded code from the neworking module

* Thu Jun 26 2003 Brent Fox <bfox@redhat.com> 1.1.3-1
- first stab at getting locale changing working (#91984)

* Thu Jun 19 2003 Brent Fox <bfox@redhat.com> 1.1.2-2
- bump number and rebuild

* Thu Jun 19 2003 Brent Fox <bfox@redhat.com> 1.1.2-1
- implement networking screen for reconfig mode (bug #91984)

* Mon Jun 16 2003 Brent Fox <bfox@redhat.com> 1.1.1-2
- bump number and rebuild

* Mon Jun 16 2003 Brent Fox <bfox@redhat.com> 1.1.1-1
- create a timezone module (bug #91984)

* Tue Jun 10 2003 Brent Fox <bfox@redhat.com> 1.0.12-1
- change "Forward" button to "Next"

* Fri May 30 2003 Brent Fox <bfox@redhat.com> 1.0.11-1
- fix traceback in username verification

* Thu May 29 2003 Brent Fox <bfox@redhat.com> 1.0.10-1
- updated deprecated function call in functions.py
- don't grab the whole screen in debug mode

* Thu May 22 2003 Brent Fox <bfox@redhat.com> 1.0.9-1
- remove explicit vt7 argument to X (bug #87636)

* Thu May 22 2003 Brent Fox <bfox@redhat.com> 1.0.8-1
- pass rhgb status into firstbootWindow.py
- don't draw background if rhgb isn't running

* Mon May 19 2003 Brent Fox <bfox@redhat.com> 1.0.7-1
- check to see if rhgb is running
- if rhgb is running, start up metacity and merge X resources

* Fri May 16 2003 Brent Fox <bfox@redhat.com> 1.0.6-2
- Added a mnemonic for network login button (bug #90636)
- added more mnemonics create_user.py (bug #90865)

* Mon Mar 24 2003 Brent Fox <bfox@redhat.com> 1.0.6-1
- add a button to create_user.py to launch authconfig-gtk

* Fri Mar  7 2003 Brent Fox <bfox@redhat.com> 1.0.5-13
- bump rev for 3.0E

* Fri Feb 28 2003 Brent Fox <bfox@redhat.com> 1.0.5-12
- fix bug #85358

* Tue Feb 25 2003 Jeremy Katz <katzj@redhat.com> 1.0.5-11
- background image name changed (#85160)
- don't traceback if background doesn't exist

* Mon Feb 24 2003 Nalin Dahyabhai <nalin@redhat.com> 1.0.5-10
- compare text to string.whitespace, not whitespace (#85038)

* Mon Feb 24 2003 Brent Fox <bfox@redhat.com> 1.0.5-9
- apply initscript patch from mikem@redhat.com.  Avoids calling telinit (bug #84848)

* Fri Feb 21 2003 Brent Fox <bfox@redhat.com> 1.0.5-8
- call RGB_DITHER_MAX (bug #84850)

* Thu Feb 20 2003 Brent Fox <bfox@redhat.com> 1.0.5-7
- fix traceback in create_users.py (bug #84722)

* Tue Feb 18 2003 Brent Fox <bfox@redhat.com> 1.0.5-6
- add mnemonics to up2date.py (bug #84487)

* Wed Feb 12 2003 Brent Fox <bfox@redhat.com> 1.0.5-5
- only launch r-c-xfree86 if in runlevel 3 and XF86Config does not exist (bug #84135)

* Tue Feb 11 2003 Brent Fox <bfox@redhat.com> 1.0.5-4
- fix bug #84068

* Wed Feb  5 2003 Brent Fox <bfox@redhat.com> 1.0.5-3
- check for empty soundcard list, not list = None

* Mon Feb  3 2003 Brent Fox <bfox@redhat.com> 1.0.5-2
- notting fixed the initscript to pull in the locale

* Fri Jan 31 2003 Brent Fox <bfox@redhat.com> 1.0.5-1
- new strings in up2date module

* Wed Jan 29 2003 Brent Fox <bfox@redhat.com> 1.0.4-8
- don't run firstboot in runlevel 3 at all (bug #78239)
- fix return tuple if no soundcards are found in soundcard_gui.py
- use backslash instead of forward slash in the init script

* Wed Jan 29 2003 Brent Fox <bfox@redhat.com> 1.0.4-6
- give the X server 1 second to close before we exit firstboot (bug #81313)

* Tue Jan 28 2003 Brent Fox <bfox@redhat.com> 1.0.4-5
- don't use Yes/No dialogs in create_user.py (bug #82680)
- only use root window mode in non-debug mode
- make module titles consistent with each other

* Fri Jan 24 2003 Brent Fox <bfox@redhat.com> 1.0.4-4
- better validity checking for user name and password

* Tue Jan 21 2003 Brent Fox <bfox@redhat.com> 1.0.4-3
- remove print statement that was causing a traceback

* Mon Jan 20 2003 Brent Fox <bfox@redhat.com> 1.0.4-2
- use the gdm background as the background image

* Fri Jan 17 2003 Brent Fox <bfox@redhat.com> 1.0.4-1
- make hboxes transparent and use a new background

* Mon Jan 13 2003 Brent Fox <bfox@redhat.com> 1.0.3-6
- make it so that we can paint the root window

* Thu Jan  9 2003 Brent Fox <bfox@redhat.com> 1.0.3-5
- sleep .5 sec on exit (bug #81313)

* Mon Dec 23 2002 Brent Fox <bfox@redhat.com> 1.0.3-4
- enforce 6 char user passwords

* Sun Dec 22 2002 Brent Fox <bfox@redhat.com> 1.0.3-3
- require an NTP server if NTP selected in date.py

* Tue Dec 17 2002 Brent Fox <bfox@redhat.com> 1.0.3-2
- don't run x tool if /etc/sysconfig/firstboot exists

* Mon Dec 02 2002 Brent Fox <bfox@redhat.com> 1.0.3-1
- Create a message for machines that boot in runlevel 3

* Tue Nov 26 2002 Brent Fox <bfox@redhat.com> 1.0.2-4
- Mark initscript strings as internationalizable (bug 77826)

* Fri Nov 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe

* Wed Nov 13 2002 Brent Fox <bfox@redhat.com> 1.0.2-3
- fix soundcard and mouse problem

* Tue Nov 12 2002 Brent Fox <bfox@redhat.com> 1.0.2-2
- explicitly kill X server pid
- Latest translations

* Thu Sep 05 2002 Brent Fox <bfox@redhat.com> 1.0.1-10
- moved some pixmaps to redhat-logos package
- added a requires for redhat-logos package

* Tue Sep 03 2002 Brent Fox <bfox@redhat.com> 1.0.1-9
- call dithering magic to make new pixmaps appear correctly

* Tue Sep 03 2002 Brent Fox <bfox@redhat.com> 1.0.1-8
- get new pixmaps from garrett

* Fri Aug 30 2002 Brent Fox <bfox@redhat.com> 1.0.1-7
- Wrap umount in a try/except in additional_cds.py

* Fri Aug 30 2002 Brent Fox <bfox@redhat.com> 1.0.1-6
- run chkconfig on starting/stopping ntpd

* Thu Aug 29 2002 Brent Fox <bfox@redhat.com> 1.0.1-5
- Make the date screen update the time widgets when the screen is entered

* Thu Aug 29 2002 Brent Fox <bfox@redhat.com> 1.0.1-4
- Convert po files to UTF-8

* Thu Aug 29 2002 Brent Fox <bfox@redhat.com> 1.0.1-3
- created a flag so that failed connections to NTP servers don't advance the screens
- Don't try to display the parent window pixmap gradient
- Make the parent window background a little darker

* Wed Aug 28 2002 Brent Fox <bfox@redhat.com> 1.0.1-2
- Fix typo

* Wed Aug 28 2002 Brent Fox <bfox@redhat.com> 1.0.1-1
- Convert to noarch
- Add a root window mode for firstbootWindow
- Use a gtkInvisible dialog to block on up2date and the package screen

* Wed Aug 28 2002 Karsten Hopp <karsten@redhat.de> 1.0.0-5
- don't require config-mouse, config-keyboard, config-soundcard
  on S390

* Tue Aug 27 2002 Brent Fox <bfox@redhat.com> 1.0.0-4
- fix hang on unreponsive ntp servers
 
* Thu Aug 22 2002 Brent Fox <bfox@redhat.com> 1.0.0-3
- Don't draw window decorations

* Wed Aug 21 2002 Brent Fox <bfox@redhat.com> 1.0.0-2
- pull translation domains from rhpl

* Wed Aug 21 2002 Brent Fox <bfox@redhat.com> 1.0.0-1
- Implement a lowres mode for 640x480 screens

* Thu Aug 15 2002 Brent Fox <bfox@rehdat.com> 0.9.9-13
- Don't show up2date screen if machine is already registered

* Wed Aug 14 2002 Brent Fox <bfox@redhat.com> 0.9.9-12
- fix reconfig mode
- change pixmap on finished screen

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-11
- pass None into startNtpService

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-10
- If there's no XF86Config file, start redhat-config-xfree86 first

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-9
- only start in runlevel 5

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-8
- include cd.png

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-7
- improved UI on additional cd screen

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 0.9.9-6
- Require redhat-config-packages
- Change string in finished module

* Mon Aug 12 2002 Brent Fox <bfox@redhat.com> 0.9.9-5
- Print out a message if user tries to run firstboot again
- move firstboot to firstboot.py and create a shell script for firstboot
- applied a patch from dburcaw@terraplex.com to check to see if we're run as root

* Mon Aug 12 2002 Brent Fox <bfox@redhat.com> 0.9.9-4
- Try to fix race condition
- Have init script return 0 instead of 1
- Make Forward button grab the focus

* Wed Aug 07 2002 Brent Fox <bfox@redhat.com> 0.9.9-1
- Rebuild for Jay, who is being a punk ;)
  
* Fri Aug 02 2002 Brent Fox <bfox@redhat.com> 0.9.8-1
- Make changes for new pam timestamp policy

* Thu Aug 01 2002 Brent Fox <bfox@redhat.com> 0.9.7-1
- fix typo in finished module
- create better text in the exception screen
- save traceback info in /tmp/firstboot.txt

* Tue Jul 30 2002 Brent Fox <bfox@redhat.com> 0.9.6-5
- merge Xresources on startup.  Fixes bug #68724

* Thu Jul 25 2002 Brent Fox <bfox@redhat.com> 0.9.6-4
- change background color
- give some padding to the icon box
- put new splash and text on welcome and finished modules

* Wed Jul 24 2002 Brent Fox <bfox@redhat.com> 0.9.6-3
- fix Makefiles and spec files so that translations get installed

* Wed Jul 24 2002 Brent Fox <bfox@redhat.com> 0.9.6-2
- update spec file for public beta 2

* Tue Jul 23 2002 Brent Fox <bfox@redhat.com> 0.9.6-1
- removed register module
- added a finished module
- pulled in new icons

* Fri Jul 19 2002 Brent Fox <bfox@redhat.com> 0.9.5-1
- wire up register module
- wire up up2date module
- fix pointer pixmap bug
- create an exceptionWindow to capture tracebacks

* Tue Jul 16 2002 Brent Fox <bfox@redhat.com> 0.9.4-2
- bump rev num and rebuild

* Sat Jul 13 2002 Brent Fox <bfox@redhat.com> 0.9.4-1
- fixed preun script to not blow away runlevel symlinks on upgrades

* Thu Jul 11 2002 Brent Fox <bfox@redhat.com> 0.9.3-2
- Update changelogs and rebuild

* Thu Jul 11 2002 Brent Fox <bfox@redhat.com> 0.9.3-1
- Update changelogs and rebuild

* Mon Jul 01 2002 Brent Fox <bfox@redhat.com> 0.9.2-1
- Bump rev number

* Fri Jun 28 2002 Brent Fox <bfox@redhat.com> 0.9.1-4
- Require metacity

* Fri Jun 28 2002 Brent Fox <bfox@redhta.com> 0.9.1-3
- Backed out some changes from init script
- Fixed icon path in date module

* Thu Jun 27 2002 Brent Fox <bfox@redhat.com> 0.9.1-2
- Popup warning for unimplemented features

* Wed Jun 26 2002 Brent Fox <bfox@redhat.com> 0.9.1-1
- Only run in runlevel 5

* Tue Jun 25 2002 Brent Fox <bfox@redhat.com> 0.9.0-5
- Change initscript to not start firstboot on runlevel changes

* Mon Jun 24 2002 Brent Fox <bfox@redhat.com> 0.9.0-4
- Fix spec file

* Fri Jun 21 2002 Brent Fox <bfox@redhat.com> 0.9.0-3
- Added snapsrc to makefile
- Rebuild for completeness

* Wed Jun 12 2002 Brent Fox <bfox@redhat.com> 0.2.0-3
- Fixed a string error in the welcome module

* Fri May 31 2002 Brent Fox <bfox@redhat.com> 0.2.0-2
- Some additions to hardware screen

* Fri May 31 2002 Brent Fox <bfox@redhat.com> 0.2.0-1
- Fix hardare screen's run priority

* Thu May 30 2002 Brent Fox <bfox@redhat.com> 0.1.0-8
- Created the beginnings of the hardware screen

* Thu May 30 2002 Brent Fox <bfox@redhat.com> 0.1.0-7
- Fixed Requires to not pull in pygnome

* Tue May 28 2002 Brent Fox <bfox@redhat.com> 0.1.0-6
- Rebuild for completeness
- Fix bug in init script

* Sun May 26 2002 Brent Fox <bfox@redhat.com> 0.1.0-4
- Get startup scripts ready to go
- Prepare package for placement into newest tree
- Install init script into correct place

* Tue Nov 28 2001 Brent Fox <bfox@redhat.com>
- initial coding and packaging

