Name:		wine
Version:	5.20
Release:	1%{?dist}
Summary:	Wine with 32 and 64 bit libraries.

URL:		https://www.winehq.org
Source0:	https://dl.winehq.org/wine/source/5.x/wine-%{version}.tar.xz
License:	NONE
BuildRequires: alsa-lib-devel
BuildRequires: alsa-lib-devel(x86-32)
BuildRequires: audiofile-devel
#BuildRequires: audiofile-devel(x86-32) # does not seem to exist
BuildRequires: cups-devel
BuildRequires: cups-devel(x86-32)
BuildRequires: dbus-devel
BuildRequires: dbus-devel(x86-32)
BuildRequires: fontconfig-devel
BuildRequires: fontconfig-devel(x86-32)
BuildRequires: fontforge
Requires: fontforge
BuildRequires: fontpackages-devel
BuildRequires: freeglut-devel(x86-32)
BuildRequires: freetype-devel
BuildRequires: freetype-devel(x86-32)
BuildRequires: gettext-devel(x86-32)
BuildRequires: giflib-devel
BuildRequires: giflib-devel(x86-32)
BuildRequires: glib2-devel(x86-32)
BuildRequires: glib2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-devel(x86-32)
BuildRequires: gnutls-devel(x86-32)
BuildRequires: gnutls-devel
BuildRequires: gsm-devel
BuildRequires: gsm-devel(x86-32)
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-devel(x86-32)
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: gstreamer1-plugins-base-devel(x86-32)
BuildRequires: icoutils
Requires: icoutils
BuildRequires: ImageMagick-devel
BuildRequires: lcms2-devel
BuildRequires: lcms2-devel(x86-32)
BuildRequires: libexif-devel(x86-32)
BuildRequires: libgcc
Requires: libgcc
Requires: libgcc(x86-32)
BuildRequires: libgcc(x86-32)
BuildRequires: libgphoto2-devel
BuildRequires: libgphoto2-devel(x86-32)
BuildRequires: libICE-devel(x86-32)
BuildRequires: libieee1284-devel(x86-32)
BuildRequires: libjpeg-turbo-devel
BuildRequires: libjpeg-turbo-devel(x86-32)
BuildRequires: libmpg123-devel
BuildRequires: libpcap-devel
BuildRequires: libpcap-devel(x86-32)
BuildRequires: libpng-devel(x86-32)
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel(x86-32)
BuildRequires: libsane-hpaio
Requires: libsane-hpaio
BuildRequires: libSM-devel
BuildRequires: libSM-devel(x86-32)
BuildRequires: libstdc++-devel
BuildRequires: libstdc++-devel(x86-32)
BuildRequires: libtiff-devel
BuildRequires: libtiff-devel(x86-32)
BuildRequires: libusb-devel
BuildRequires: libusb-devel(x86-32)
BuildRequires: libv4l-devel
BuildRequires: libv4l-devel(x86-32)
BuildRequires: libX11-devel(x86-32)
BuildRequires: libX11-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXcomposite-devel(x86-32)
BuildRequires: libXcursor-devel
BuildRequires: libXcursor-devel(x86-32)
BuildRequires: libXext-devel(x86-32)
BuildRequires: libXfixes-devel(x86-32)
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel
BuildRequires: libXi-devel(x86-32)
BuildRequires: libXinerama-devel
BuildRequires: libXinerama-devel(x86-32)
BuildRequires: libxml2-devel(x86-32)
BuildRequires: libxml2-devel
BuildRequires: libXmu-devel(x86-32)
BuildRequires: libXrandr-devel
BuildRequires: libXrandr-devel(x86-32)
BuildRequires: libXrender-devel(x86-32)
BuildRequires: libXrender-devel
BuildRequires: libxslt-devel
BuildRequires: libXxf86dga-devel
BuildRequires: libXxf86dga-devel(x86-32)
BuildRequires: libXxf86vm-devel
BuildRequires: libXxf86vm-devel(x86-32)
BuildRequires: mesa-libGL-devel(x86-32)
BuildRequires: mesa-libGLU-devel
BuildRequires: mesa-libGLU-devel(x86-32)
BuildRequires: mesa-libOSMesa-devel
BuildRequires: mesa-libOSMesa-devel(x86-32)
BuildRequires: ncurses-devel
BuildRequires: ncurses-devel(x86-32)
BuildRequires: ocl-icd
Requires: ocl-icd
BuildRequires: openal-soft-devel
BuildRequires: opencl-headers
BuildRequires: openldap-devel
BuildRequires: openldap-devel(x86-32)
BuildRequires: pulseaudio-libs-devel
BuildRequires: pulseaudio-libs-devel(x86-32)
BuildRequires: samba-winbind-clients
Requires: samba-winbind-clients
BuildRequires: sane-backends-devel(x86-32)
BuildRequires: sane-backends-devel
BuildRequires: systemd-devel(x86-32)
BuildRequires: systemd-devel
BuildRequires: unixODBC-devel(x86-32)
Requires: unixODBC(x86-32)
BuildRequires: unixODBC(x86-32)
Requires: unixODBC(x86-32)
BuildRequires: zlib-devel(x86-32)

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

