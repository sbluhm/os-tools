Name: gnucash-docs
Summary: Help files and documentation for the GnuCash personal finance manager
Version: 4.2
URL: http://gnucash.org/
Release: 1%{?dist}
License: GFDL
Source: https://downloads.sourceforge.net/gnucash/%{name}-%{version}.tar.gz
BuildArchitectures: noarch
BuildRequires: libxslt
Requires: yelp

%description
GnuCash is a personal finance manager. gnucash-docs contains the
help files and documentation for GnuCash.

%prep
%setup -q

%build
touch configure.ac aclocal.m4 Makefile.in configure gnucash-docs.spec
%configure --without-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf	$RPM_BUILD_ROOT/var/scrollkeeper

%files
%{_datadir}/gnome/help/*
%doc AUTHORS ChangeLog* HACKING NEWS README
%license COPYING*

%pretrans -p <lua>
for _,d in pairs ({"gnucash-guide", "gnucash-help"}) do
  path = "%{_datadir}/gnome/help/" .. d
  if posix.stat(path, "type") == "link" then
    os.remove(path)
    posix.mkdir(path)
  end
end
return 0

%changelog
* Mon Sep 28 2020 Stefan Bluhm <stefan.bluhm@clacee.eu> - 4.2-1
- Updated to version 4.2

* Thu Aug 06 2020 Stefan Bluhm <stefan.bluhm@clacee.eu> - 4.1-2
- Updated Source url to https.

* Mon Jul 27 2020 Bill Nottingham <notting@splat.cc> - 4.1-1
- update to 4.1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Bill Nottingham <notting@splat.cc> - 4.0-1
- update to 4.0

* Mon Apr 13 2020 Bill Nottingham <notting@splat.cc> - 3.10-1
- update to 3.10

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Kalev Lember <klember@redhat.com> - 3.8-1
- Update to 3.8

* Mon Sep  9 2019 Bill Nottingham <notting@splat.cc> - 3.7-1
- update to 3.7

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul  5 2019 Bill Nottingham <notting@splat.cc> - 3.6-1
- update to 3.6

* Tue Apr  2 2019 Bill Nottingham <notting@splat.cc> - 3.5-1
- update to 3.5

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan  8 2019 Bill Nottingham <notting@splat.cc> - 3.4-1
- update to 3.4

* Mon Oct  1 2018 Bill Nottingham <notting@splat.cc> - 3.3-1
- update to 3.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Bill Nottingham <notting@splat.cc> - 3.2-1
- update to 3.2

* Mon Apr 30 2018 Bill Nottingham <notting@splat.cc> - 3.1-1
- update to 3.1

* Mon Apr 02 2018 Bill Nottingham <notting@splat.cc> - 3.0-1
- update to 3.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 26 2017 Bill Nottingham <notting@splat.cc> - 2.6.18-1
- update to 2.6.18

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul  5 2017 Bill Nottingham <notting@splat.cc> - 2.6.17-1
- update to 2.6.17

* Tue Apr 11 2017 Bill Nottingham <notting@splat.cc> - 2.6.16-1
- update to 2.6.16

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 18 2016 Bill Nottingham <notting@splat.cc> - 2.6.15-1
- update to 2.6.15

* Fri Nov 04 2016 Bill Nottingham <notting@splat.cc> - 2.6.14-1
- update to 2.6.14

* Thu Jul 07 2016 Bill Nottingham <notting@splat.cc> - 2.6.13-1
- update to 2.6.13

* Thu Apr 21 2016 Bill Nottingham <notting@splat.cc> - 2.6.12-1
- update to 2.6.12

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Bill Nottingham <notting@splat.cc> - 2.6.11-1
- update to 2.6.11

* Sun Dec 27 2015 Bill Nottingham <notting@splat.cc> - 2.6.10-1
- update to 2.6.10

* Wed Oct  7 2015 Bill Nottingham <notting@splat.cc> - 2.6.9-1
- update to 2.6.9

* Tue Oct  6 2015 Bill Nottingham <notting@splat.cc> - 2.6.8-1
- update to 2.6.8

* Mon Jun 29 2015 Bill Nottingham <notting@splat.cc> - 2.6.7-1
- update to 2.6.7

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Bill Nottingham <notting@splat.cc> - 2.6.6-1
- update to 2.6.6

* Thu Jan  8 2015 Bill Nottingham <notting@splat.cc> - 2.6.5-1
- update to 2.6.5

* Tue Sep 30 2014 Bill Nottingham <notting@splat.cc> - 2.6.4-1
- update to 2.6.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr  3 2014 Bill Nottingham <notting@splat.cc> - 2.6.3-1
- update to 2.6.3

* Mon Mar 10 2014 Bill Nottingham <notting@splat.cc> - 2.6.2-1
- update to 2.6.2

* Mon Jan 27 2014 Bill Nottingham <notting@redhat.com> - 2.6.1-1
- update to 2.6.1

* Tue Jan 21 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-2
- fix install (#1056046)

* Thu Jan 16 2014 Bill Nottingham <notting@redhat.com> - 2.6.0-1
- update to 2.6.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Bill Nottingham <notting@redhat.com> - 2.4.2-1
- update to 2.4.2
- drop scrollkeeper bits

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Bill Nottingham <notting@redhat.com> - 2.4.1-1
- update to 2.4.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 29 2007 Bill Nottingham <notting@redhat.com> - 2.2.0-2
- gnucash multilib fixes (#341331, #357161, #246382)

* Mon Jul 16 2007 Bill Nottingham <notting@redhat.com> - 2.2.0-1
- update to 2.2.0

* Tue Feb 13 2007 Bill Nottingham <notting@redhat.com> - 2.0.1-2
- move yelp requirement from gnucash to here

* Thu Feb  1 2007 Bill Nottingham <notting@redhat.com> - 2.0.1-1
- fork off from main gnucash package
