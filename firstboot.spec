Summary: Initial system configuration utility
Name: firstboot
Version: 0.9.6
Release: 5
URL: http://www.redhat.com/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source0: %{name}-%{version}.tar.bz2
Obsoletes:anaconda-reconfig
Prereq: chkconfig, /etc/init.d
Requires: pygtk2
Requires: python
Requires: usermode >= 1.36
Requires: metacity
Requires: redhat-config-date
Requires: redhat-config-language
Requires: redhat-config-mouse
Requires: redhat-config-keyboard
Requires: redhat-config-securitylevel
Requires: redhat-config-rootpassword
Requires: redhat-config-soundcard
Requires: up2date

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

