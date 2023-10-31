Name:           guacamole-server
Version:        1.5.3 
Release:        1%{?dist}
Summary:        summary

License:        Apache-2.0
URL:            https://guacamole.apache.org
Source0:        https://apache.org/dyn/closer.lua/guacamole/1.5.3/source/guacamole-server-1.5.3.tar.gz

BuildRequires:  cairo-devel
BuildRequires:  freerdp-devel
BuildRequires:  libavcodec-free-devel
BuildRequires:  libavformat-free-devel
BuildRequires:  libavutil-free-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  libssh2-devel
BuildRequires:  libswscale-free-devel
BuildRequires:  libtelnet-devel
BuildRequires:  libvncserver-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libwebp-devel
BuildRequires:  libwebsockets-devel
BuildRequires:  openssl-devel
BuildRequires:  pango-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  uuid-devel

%description
test

%prep
%autosetup


%build
export CFLAGS="-Wno-error"
%configure --with-systemd-dir=/etc/systemd/system/
%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%files
%license LICENSE
%doc README



%changelog
* Fri Oct 20 2023 Stefan Bluhm <stefan.bluhm@clacee.eu>
- 

