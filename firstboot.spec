Summary: Initial system configuration utility
Name: firstboot
Version: 0.1.0
Release: 1
URL: http://www.redhat.com/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source0: %{name}-%{version}.tar.gz
Requires: pygtk
Requires: python
Requires: pygnome
Requires: usermode >= 1.36
Requires: redhat-config-language
#Requires: redhat-config-mouse
Requires: redhat-config-keyboard
Requires: redhat-config-securitylevel
Requires: redhat-config-rootpassword


%description
firstboot is a utility that runs once after initial installation

%prep
%setup -q

%build
make

%install
make INSTROOT=$RPM_BUILD_ROOT install

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -d /usr/share/firstboot ] ; then
  rm -rf /usr/share/firstboot/*.pyc
fi

%files -f %{name}.lang
%defattr(-,root,root)
#%doc COPYING
#%doc doc/*
%dir /usr/share/firstboot/
%dir /usr/share/firstboot/modules
#%attr(0644,root,root) %{_mandir}/man8/dateconfig*
#%attr(0644,root,root) %{_mandir}/ja/man8/dateconfig*
#%attr(0644,root,root) %config /etc/X11/applnk/System/redhat-config-language.desktop
#%attr(0644,root,root) %config /etc/X11/sysconfig/dateconfig.desktop
#%attr(0644,root,root) %config /usr/share/pixmaps/dateconfig.png
#%attr(0644,root,root) %config /etc/security/console.apps/redhat-config-language
#%attr(0644,root,root) %config /etc/pam.d/redhat-config-language

%changelog
* Tue Nov 28 2001 Brent Fox <bfox@redhat.com>
- initial coding and packaging

