Summary: Initial system configuration utility
Name: firstboot
Version: 1.4.30
Release: 2%{?dist}
URL: http://fedora.redhat.com/projects/config-tools/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Source0: %{name}-%{version}.tar.bz2
Obsoletes: anaconda-reconfig

BuildRequires: gettext

Requires: pygtk2, metacity, rhpl, rhpxl >= 0.19, authconfig-gtk, libuser
Requires: system-config-language, system-config-soundcard
Requires: system-config-securitylevel, system-config-network
Requires: system-config-users, system-config-date >= 1.7.9
Requires: system-config-keyboard, chkconfig
Requires: system-logos, firstboot-tui = %{version}

ExcludeArch: s390 s390x ppc64

%description
The firstboot utility runs after installation.  It guides the user through
a series of steps that allows for easier configuration of the machine. 

%package tui
Summary: A text interface for firstboot
Group: System Environment/Base

BuildRequires: gettext

Requires: python, usermode >= 1.36, rhpl, system-config-securitylevel-tui
Requires: system-config-network-tui, ntsysv, authconfig, chkconfig

%description tui
firstboot-tui is a text interface for initial system configuration.

%prep
%setup -q

%build
make

%install
make INSTROOT=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post tui
if ! [ -f /etc/sysconfig/firstboot ]
then
  chkconfig --add firstboot
fi

%preun
if [ $1 = 0 ]; then
  rm -rf /usr/share/firstboot/*.pyc
  rm -rf /usr/share/firstboot/modules/*.pyc
fi

%preun tui
if [ $1 = 0 ]; then
  chkconfig --del firstboot
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/firstboot
%dir %{_datadir}/firstboot/modules/
%dir %{_datadir}/firstboot/pixmaps/
%{_datadir}/firstboot/exceptionWindow.py*
%{_datadir}/firstboot/firstbootWindow.py*
%{_datadir}/firstboot/firstboot_module_window.py*
%{_datadir}/firstboot/xfirstboot.py*
%{_datadir}/firstboot/modules/*
%{_datadir}/firstboot/pixmaps/*

%files -f %{name}.lang tui
%defattr(-,root,root,-)
%config %{_initrddir}/firstboot
%dir %{_datadir}/firstboot/
%{_sbindir}/firstboot
%{_datadir}/firstboot/constants_text.py*
%{_datadir}/firstboot/eula_strings.py*
%{_datadir}/firstboot/firstboot.py*
%{_datadir}/firstboot/firstbootBackend.py*
%{_datadir}/firstboot/functions.py*
%{_datadir}/firstboot/textWindow.py*


%changelog
* Tue Feb 13 2007 Chris Lumens <clumens@redhat.com> 1.4.30-2
- Fix typo in dependencies.

* Mon Feb 12 2007 Chris Lumens <clumens@redhat.com> 1.4.30-1
- Focus the next button by default (#227867).
- Enable fullscreen mode again; scale sidebar graphics (#211198).
- Bring spec file more in line with the packaging guidelines.

* Wed Jan 24 2007 Chris Lumens <clumens@redhat.com> 1.4.29-1
- Fix disabling the soundcard panel if no soundcard are available
  (#221177).
- Remove the display module and the dependency on system-config-display.

* Wed Dec 20 2006 Chris Lumens <clumens@redhat.com> 1.4.28-2
- Revert spec file changes for s390, s390x, and ppc64 for now.

* Mon Dec 18 2006 Chris Lumens <clumens@redhat.com> 1.4.28-1
- Remove unused graphics (#218118).
- Allow running on s390 and ppc64 under reconfig mode (#217921).
- Don't leave a bunch of defunct processes around.
- Correctly shut down if not running under rhgb.

* Wed Dec 13 2006 Chris Lumens <clumens@redhat.com> 1.4.27-1
- More translation updates (#212958, #198872).

* Thu Nov 30 2006 Chris Lumens <clumens@redhat.com> 1.4.26-1
- Update translations (#198872).

* Thu Oct 26 2006 Chris Lumens <clumens@redhat.com> 1.4.25-1
- Require matching versions of firstboot and firstboot-tui.
- Fix language in non-rhgb graphical case (notting).

* Wed Oct 25 2006 Chris Lumens <clumens@redhat.com> 1.4.24-1
- Pick up new si_LK translation (#200532).
- Support noSidebar value for modules (#210697).
- Fix release number.
- Do start up in English on CJKI installs in text mode (#211936).

* Mon Oct 02 2006 Chris Lumens <clumens@redhat.com> - 1.4.23-1
- runPriority can now be a float.
- Pick up new translations (#208867).
- Set window to 800x600 instead of fullscreening (#208331, #208620).

* Wed Sep 20 2006 Chris Lumens <clumens@redhat.com> 1.4.22-1
- Add help output to /etc/init.d/firstboot (#207043).
- Fix a window manager warning (#206369).
- Don't start up in English on CJKI installs (#206600).

* Fri Sep 15 2006 Chris Lumens <clumens@redhat.com> 1.4.21-1
- Use system-config-network-tui instead of netconfig in the text
  interface.
- Remove unused methods in the modules.

* Tue Sep 12 2006 Chris Lumens <clumens@redhat.com> 1.4.20-1
- Don't specify a default color depth.
- Pull in new translations (#199090).

* Tue Aug 08 2006 Chris Lumens <clumens@redhat.com> 1.4.19-1
- Don't fill in the Create User UI with whatever user happens to have
  UID 500 (#200695).

* Wed Aug 02 2006 Chris Lumens <clumens@redhat.com> 1.4.18-1
- Remove ddc probe support that rhpxl no longer provides.

* Fri Jul 28 2006 Chris Lumens <clumens@redhat.com> 1.4.17-1
- Pick up new or_IN translation (#200210).
- Use new rhpxl X startup code.

* Mon Jul 24 2006 Chris Lumens <clumens@redhat.com> 1.4.16-1
- Fix system-config-soundcard API change.
- Make sure firstboot starts after HAL (#199899).

* Thu Jul 20 2006 Chris Lumens <clumens@redhat.com> 1.4.15-1
- Really disable the display module.

* Wed Jul 19 2006 Chris Lumens <clumens@redhat.com> 1.4.14-1
- Disable the display module for now.

* Fri Jul 10 2006 Chris Lumens <clumens@redhat.com> 1.4.13-1
- Better fix for the no display hardware case (#192808).

* Wed Jun 21 2006 Chris Lumens <clumens@redhat.com> 1.4.12-1
- Update translation files (#195010).
- Fix traceback on exiting (#196128).

* Mon Jun 12 2006 Chris Lumens <clumens@redhat.com> 1.4.11-1
- Don't traceback on the display module if there's no display hardware
  (#142522).
- Don't forget about reconfig mode if the timer expires (#170609).

* Fri May 26 2006 Chris Lumens <clumens@redhat.com> 1.4.10-1
- Fix reconfig mode.

* Fri May 19 2006 Chris Lumens <clumens@redhat.com> 1.4.9-1
- Make /etc/modprobe.conf reading more robust (#191819).
- Don't try to call readHTML from anaconda's ICS.

* Mon May 15 2006 Chris Lumens <clumens@redhat.com> 1.4.8-2
- Require system-logos instead of an OS-specific package (#191407).

* Tue Apr 04 2006 Chris Lumens <clumens@redhat.com> 1.4.8-1
- Allow firstboot to run in kadischi (#186870).
- Updated for rhpxl changes.

* Mon Mar 20 2006 Martin Stransky <stransky@redhat.com> 1.4.7-1
- replaced "Play test button" by "Play" button for s-c-s (#185931)
- Fix soundcard string (#177425).
- Fix label inconsistency on welcome screen (#183899).
- Rework "System User" string (#177940).
- Don't create a user if a homedir with that username already exists
  (#143150).

* Fri Mar 03 2006 Chris Lumens <clumens@redhat.com> 1.4.6-1
- Revert UI changes that broke s-c-keyboard (#183718).

* Wed Mar 01 2006 Chris Lumens <clumens@redhat.com> 1.4.5-1
- Run if RUN_FIRSTBOOT != "NO" (#180520).
- Don't let dialog windows hide behind the main window.
- Remove timeout waiting for server to start.

* Wed Feb 08 2006 Chris Lumens <clumens@redhat.com> 1.4.4-1
- Get rid of chkconfig --off calls.
- Smarter checking for if we need to reboot or not.

* Mon Feb 06 2006 Chris Lumens <clumens@redhat.com> 1.4.3-1
- Tweak firstboot-tui requires to not require X (#180046).
- Wrap left side labels if they're too long.
- Remove "Click to Finish" module (#178109).
- Try to prevent running in runlevel 3 if we failed in runlevel 5
  (#145169).

* Fri Jan 27 2006 Chris Lumens <clumens@redhat.com> 1.4.2-1
- Layout cleanups and simplification.
- Use GTK styles to display the new artwork in non-debug mode.

* Wed Jan 25 2006 Chris Lumens <clumens@redhat.com> 1.4.1-1
- Fix debug mode.
- Use the new bubbly artwork (#178106).

* Thu Jan 19 2006 Chris Lumens <clumens@redhat.com> 1.4.0-1
- Split into separate packages for X and no X (#178216).

* Mon Jan 09 2006 Chris Lumens <clumens@redhat.com> 1.3.57-1
- Use scdMainWindow instead of mainWindow to fix random python import
  tracebacks.

* Mon Jan 09 2006 Chris Lumens <clumens@redhat.com> 1.3.56-2
- Remove dependancy on system-config-packages.

* Thu Jan 09 2006 Chris Lumens <clumens@redhat.com> 1.3.56-1
- Increase timeout on waiting for X to start (#176782).
- Update translations.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 08 2005 Chris Lumens <clumens@redhat.com> 1.3.55-1
- Fix grammar problems (#143953).
- Fix traceback on user screen (#175227).

* Wed Nov 30 2005 Chris Lumens <clumens@redhat.com> 1.3.54-1
- Use system-config-users for user/group/password validation (#174255).

* Wed Nov 16 2005 Chris Lumens <clumens@redhat.com> 1.3.53-1
- Disable Additional CDs module for now.

* Fri Oct 28 2005 Chris Lumens <clumens@redhat.com> 1.3.52-1
- Set a timeout on waiting for the window manager to start.
- Correct ps output.
- Move keyboard initialization to after the modules have been loaded
  (#133074, #157870).

* Mon Oct 17 2005 Chris Lumens <clumens@redhat.com> 1.3.51-1
- Fix whrandom deprecation warnings.
- Fix render_to_drawable deprecation warnings.
- Change "Next" button on last page to "Finish".

* Tue Oct 11 2005 Chris Lumens <clumens@redhat.com> 1.3.50-1
- Decrease blank space on finished screen (#144496).
- Fix import of rhpxl.videocard.

* Fri Oct 07 2005 Chris Lumens <clumens@redhat.com> 1.3.49-1
- Use rhpxl instead of rhpl for X stuff.

* Fri Sep 23 2005 Chris Lumens <clumens@redhat.com> 1.3.48-1
- Fix autoscreenshot test (#169102).
- Allow unicode letters in full user names (#169043).

* Thu Sep 15 2005 Jeremy Katz <katzj@redhat.com> - 1.3.47-2
- exclude arch ppc64 to stop from being included in ppc64 compose where 
  we don't have X

* Thu Sep 15 2005 Chris Lumens <clumens@redhat.com> 1.3.47-1
- Moved firstboot_gui_window here from rhpl and renamed it to
  firstboot_module_window.
- Converted /usr/sbin/firstboot into a python script.
- Converted the rest of firstboot into a module suitable for importing.

* Tue Sep 13 2005 Chris Lumens <clumens@redhat.com> 1.3.46-1
- Remove dependancy on up2date (#167663).
- Use rhpl's X startup code instead of using something different.

* Wed Aug 17 2005 Chris Lumens <clumens@redhat.com> 1.3.45-1
- Don't fail if no ifcfg script exists for a NIC found in modprobe.conf
  (#164874).
- Restore focus after closing dialogs (#143388, #143711).

* Tue Aug 02 2005 Chris Lumens <clumens@redhat.com> 1.3.44-1
- Allow modules to specify that the system should be rebooted after
  firstboot has run via the needsReboot module attribute.
- Enable checking for capital letters in usernames again to be consistent
  with system-config-users (#164852).
- Use libuser for adding users again (#164160).
- Rebuilt translations.

* Thu Jul 07 2005 Chris Lumens <clumens@redhat.com> 1.3.43-1
- Remove dependancy on xsri (#145807).
- Fix typo in "additional" (#158435).
- Tabs vs. spaces consistency (#156456).
- Don't require system-config-display on ppc64.

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 1.3.42-1
- Stop using deprecated gtk.{TRUE,FALSE} (#153033)

* Tue May 24 2005 Adrian Likins <alikins@redhat.com> - 1.3.41
- fix #158095 - Subscription Alert (on first login) on non network installs

* Thu May 19 2005 Adrian Likins <alikins@redhat.com> - 1.3.40
- fix #154606 - First boot displays "please insert the red hat enterprise linux extras disk"

* Fri Dec 14 2004 Adrian Likins <alikins@redhat.com> - 1.3.39-2
- really fix #138727 (was looking for cdroms in the wrong place)

* Fri Dec 14 2004 Adrian Likins <alikins@redhat.com> - 1.3.38-1
- fix #138727 (patch from katzj)
- latest translations

* Fri Nov 12 2004 Adrian Likins <alikins@redhat.com> - 1.3.37-2
- fix #139060

* Wed Nov 10 2004 Adrian Likins <alikins@redhat.com> - 1.3.35-1
- fix #137151
- fix #138541

* Wed Oct 27 2004 Adrian Likins <alikins@redhat.com> - 1.3.34-1
- add code to detect if a module wants to be skipped
  (basically, stuff to me not show RHN modules on fedora)

* Mon Oct 18 2004 Adrian Likins <alikins@redhat.com> - 1.3.33-1
- #129885 (do the right thing on ia64)
- #129532 (typo in display file location)

* Fri Oct 15 2004 Adrian Likins <alikins@redhat.com> - 1.3.30-1
- merge some updates from rhel3 branch
- try enabling tui stuff again

* Tue Oct 5 2004 Adrian Likins <alikins@redhat.com> - 1.3.28-1
- text changes for #129885
- get rid of some deprecation warnings

* Tue Sep 28 2004 Nils Philippsen <nphilipp@redhat.com> - 1.3.27-1
- let timezone only be configured on --reconfig (#133748)
- require system-config-date >= 1.7.9

* Thu Sep 23 2004 Adrian Likins <alikins@redhat.com> - 1.3.26-1
- applied patch from #132736

* Tue Sep 14 2004 Adrian Likins <alikins@redhat.com> - 1.3.25-1
- change finish screen to not show default "success" 
  message if were also showing errors
- fix forward/back behaviour

* Fri Sep 10 2004 Adrian Likins <alikins@redhat.com> - 1.3.23-1
- fix for finish screen
- ignore modules that throw exceptions on import
  (#129532 and other variations of "firstboot doesnt start)
* Fri Sep 3 2004 Adrian Likins <alikins@redhat.com> - 1.3.21-1
- more fixes for #131308

* Wed Sep 1 2004 Adrian Likins <alikins@redhat.com> - 1.3.20-1
- better fix for #131308 (works now, but needs some
  screen resizing)

* Tue Aug 31 2004 Adrian Likins <alikins@redhat.com> - 1.3.19-1
- #131308 (system-config-date changed, working to not
  traceback, still needs more fixing)

* Thu Jul 15 2004 Adrian Likins <alikins@redhat.com> - 1.3.17-1
- allow screens to catch a signal when they are shown

* Wed Jun 30 2004 Adrian Likins <alikins@redhat.com> - 1.3.16-1
- apply patch to allow modules to go forward/back in
  the module order

* Mon Jun 21 2004 Brent Fox <bfox@redhat.com> - 1.3.15-1
- apply patch from mikem in bug #121489

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

