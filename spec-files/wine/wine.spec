Name:		wine
Version:	5.20
Release:	1%{?dist}
Summary:	Wine with 32 and 64 bit libraries.

URL:		https://www.winehq.org
Source0:	https://dl.winehq.org/wine/source/5.x/wine-${ver}.tar.xz
License:	NONE
BuildRequires: alsa-lib-devel
BuildRequires: alsa-lib-devel.i686
BuildRequires: audiofile-devel
BuildRequires: audiofile-devel.i686
BuildRequires: cups-devel
BuildRequires: cups-devel.i686
BuildRequires: dbus-devel
BuildRequires: dbus-devel.i686
BuildRequires: fontconfig-devel
BuildRequires: fontconfig-devel.i686
BuildRequires: fontforge
Requires: fontforge
BuildRequires: fontpackages-devel
BuildRequires: freeglut-devel.i686
BuildRequires: freetype-devel
BuildRequires: freetype-devel.i686
BuildRequires: gettext-devel.i686
BuildRequires: giflib-devel
BuildRequires: giflib-devel.i686
BuildRequires: glib2-devel.i686
BuildRequires: glib2-devel
BuildRequires: vglibc-devel
BuildRequires: glibc-devel.i686
BuildRequires: gnutls-devel.i686
BuildRequires: gnutls-devel
BuildRequires: gsm-devel
BuildRequires: gsm-devel.i686
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-devel.i686
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: gstreamer1-plugins-base-devel.i686
BuildRequires: icoutils
Requires: icoutils
BuildRequires: ImageMagick-devel
BuildRequires: lcms2-devel
BuildRequires: lcms2-devel.i686
BuildRequires: libexif-devel.i686
BuildRequires: libgcc
Requires: libgcc
Requires: vlibgcc.i686
BuildRequires: vlibgcc.i686
BuildRequires: vlibgphoto2-devel
BuildRequires: libgphoto2-devel.i686
BuildRequires: libICE-devel.i686
BuildRequires: libieee1284-devel.i686
BuildRequires: libjpeg-turbo-devel
BuildRequires: libjpeg-turbo-devel.i686
BuildRequires: libmpg123-devel
BuildRequires: libpcap-devel
BuildRequires: libpcap-devel.i686
BuildRequires: libpng-devel.i686
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel.i686
BuildRequires: libsane-hpaio
Requires: libsane-hpaio
BuildRequires: libSM-devel
BuildRequires: libSM-devel.i686
BuildRequires: libstdc++-devel
BuildRequires: libstdc++-devel.i686
BuildRequires: libtiff-devel
BuildRequires: libtiff-devel.i686
BuildRequires: libusb-devel
BuildRequires: libusb-devel.i686
BuildRequires: libv4l-devel
BuildRequires: libv4l-devel.i686
BuildRequires: libX11-devel.i686
BuildRequires: libX11-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXcomposite-devel.i686
BuildRequires: libXcursor-devel
BuildRequires: libXcursor-devel.i686
BuildRequires: libXext-devel.i686
BuildRequires: libXfixes-devel.i686
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel
BuildRequires: libXi-devel.i686
BuildRequires: libXinerama-devel
BuildRequires: libXinerama-devel.i686
BuildRequires: libxml2-devel.i686
BuildRequires: libxml2-devel
BuildRequires: libXmu-devel.i686
BuildRequires: libXrandr-devel
BuildRequires: libXrandr-devel.i686
BuildRequires: libXrender-devel.i686
BuildRequires: libXrender-devel
BuildRequires: libxslt-devel
BuildRequires: libXxf86dga-devel
BuildRequires: libXxf86dga-devel.i686
BuildRequires: libXxf86vm-devel
BuildRequires: libXxf86vm-devel.i686
BuildRequires: mesa-libGL-devel.i686
BuildRequires: mesa-libGLU-devel
BuildRequires: mesa-libGLU-devel.i686
BuildRequires: mesa-libOSMesa-devel
BuildRequires: mesa-libOSMesa-devel.i686
BuildRequires: ncurses-devel
BuildRequires: ncurses-devel.i686
BuildRequires: ocl-icd
Requires: ocl-icd
BuildRequires: openal-soft-devel
BuildRequires: opencl-headers
BuildRequires: openldap-devel
BuildRequires: openldap-devel.i686
BuildRequires: pulseaudio-libs-devel
BuildRequires: pulseaudio-libs-devel.i686
BuildRequires: qt-devel.i686
BuildRequires: samba-winbind-clients
Requires: samba-winbind-clients
BuildRequires: sane-backends-devel.i686
BuildRequires: sane-backends-devel
BuildRequires: systemd-devel.i686
BuildRequires: systemd-devel
BuildRequires: unixODBC-devel.i686
Requires: unixODBC.i686
BuildRequires: unixODBC.i686
Requires: unixODBC.i686
BuildRequires: zlib-devel.i686

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

