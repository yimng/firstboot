Summary: Initial system configuration utility
Name: firstboot
Version: 1.0.5
Release: 11
URL: http://www.redhat.com/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Source0: %{name}-%{version}.tar.bz2
Obsoletes: anaconda-reconfig
Prereq: chkconfig, /etc/init.d
BuildPreReq: python-tools
Requires: pygtk2
Requires: python
Requires: usermode >= 1.36
Requires: metacity
Requires: rhpl
Requires: redhat-config-date
Requires: redhat-config-language
Requires: redhat-config-mouse
Requires: redhat-config-keyboard
Requires: redhat-config-soundcard
Requires: redhat-config-securitylevel
Requires: redhat-config-rootpassword
Requires: redhat-config-packages
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
chkconfig --add firstboot
		
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

