Summary: Initial system configuration utility
Name: firstboot
Version: 0.1.0
Release: 2
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
  rm -rf /usr/share/firstboot/modules/*.pyc
fi

%files -f %{name}.lang
%defattr(-,root,root)
#%doc COPYING
#%doc doc/*
%dir /usr/share/firstboot/
/usr/share/firstboot/*

%changelog
* Tue Nov 28 2001 Brent Fox <bfox@redhat.com>
- initial coding and packaging

