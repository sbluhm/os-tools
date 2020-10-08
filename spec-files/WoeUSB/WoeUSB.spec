Name:		WoeUSB
Version:	3.3.1
Release:	1%{?dist}
Summary:	A Linux program to create a Windows USB stick installer from a real Windows DVD or image.

#Group:		
License:	GPL-3.0 License
URL:		https://github.com/slacka/WoeUSB
Source0:	https://github.com/slacka/%{name}/archive/v%{version}.tar.gz

BuildRequires:	autoconf
BuildRequires:	make
BuildRequires:  automake
BuildRequires:	libtool
BuildRequires:	wxGTK3-devel
Requires:	wxGTK3

%description
WoeUSB is a simple tool that enable you to create your own usb stick windows installer from an iso image or a real DVD. It is a fork of Congelli501's WinUSB. 

%prep
%setup -q WoeUSB-%{version}


%build
autoreconf --force --install
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc
/usr/bin/woeusb
/usr/bin/woeusbgui
/usr/lib/debug/usr/bin/woeusbgui-3.3.1-1.el8.x86_64.debug
/usr/share/applications/woeusbgui.desktop
/usr/share/man/man1/woeusb.1.gz
/usr/share/man/man1/woeusbgui.1.gz
/usr/share/pixmaps/woeusbgui-icon.png
/usr/share/woeusb/data/c501-logo.png
/usr/share/woeusb/data/icon.png
/usr/share/woeusb/data/listDvdDrive
/usr/share/woeusb/data/listUsb
/usr/share/woeusb/data/woeusb-logo.png
/usr/share/woeusb/locale/fr/LC_MESSAGES/woeusb.mo
/usr/share/woeusb/locale/fr/LC_MESSAGES/wxstd.mo
/usr/share/woeusb/locale/zh_TW/LC_MESSAGES/woeusb.mo



%changelog
* Thu Oct 08 2020 Stefan Bluhm <stefan.bluhm@clacee.eu> - 3.3.1-1
- Initial version
