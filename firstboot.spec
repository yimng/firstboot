Summary: Initial system configuration utility
Name: firstboot
Version: 0.1.0
Release: 7
URL: http://www.redhat.com/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source0: %{name}-%{version}.tar.gz
Obsoletes:anaconda-reconfig
Prereq: chkconfig /etc/init.d
Requires: pygtk2
Requires: python
Requires: usermode >= 1.36
Requires: redhat-config-language
#Requires: redhat-config-mouse
Requires: redhat-config-keyboard
Requires: redhat-config-securitylevel
Requires: redhat-config-rootpassword


%description
The firstboot utility runs after installation or upgrade.  It 
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
if [ -d /usr/share/firstboot ] ; then
  rm -rf /usr/share/firstboot/*.pyc
  rm -rf /usr/share/firstboot/modules/*.pyc
  chkconfig --del firstboot
fi

%files -f %{name}.lang
%defattr(-,root,root)
#%doc COPYING
#%doc doc/*
%dir /usr/share/firstboot/
%config /etc/rc.d/init.d/firstboot
/usr/share/firstboot/*
/usr/sbin/firstboot



%changelog
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

