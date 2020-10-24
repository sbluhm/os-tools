Name:		wine
Version:	5.20
Release:	1%{?dist}
Summary:	Wine with 32 and 64 bit libraries.

URL:		https://www.winehq.org
Source0:	http://dl.winehq.org/wine/source/5.x/wine-${ver}.tar.xz

BuildRequires:	
Requires:	

%description
Wine with 32 and 64 bit libraries.

%prep
%setup -q


%build
mkdir -p wine32 wine64 
cd wine64
../configure --enable-win64
make
cd ../wine32
../configure
make
PKG_CONFIG_PATH=/usr/lib/pkgconfig ../configure --with-wine64=../wine64
make


%install
%make_install
cd ../wine64
%make_install

%files
%doc



%changelog

