# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%global no64bit   0
%global winegecko 2.47.4
%global winemono  8.0.0
#global _default_patch_fuzz 2
%ifarch %{ix86}
%global winepedir i386-windows
%global winesodir i386-unix
%endif
%ifarch x86_64
%global winepedir x86_64-windows
%global winesodir x86_64-unix
%endif
%ifarch %{arm}
%global winepedir arm-windows
%global winesodir arm-unix
%endif
%ifarch aarch64
%global winepedir aarch64-windows
%global winesodir aarch64-unix
%global __brp_llvm_compile_lto_elf %nil
%global __brp_strip_lto %nil
%global __brp_strip_static_archive %nil
%endif

# build with wine-staging patches, see:  https://github.com/wine-staging/wine-staging
%if 0%{?fedora} || 0%{?rhel}
%global wine_staging 1
%endif
# 0%%{?fedora}

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

Name:           wine
Version:        8.18
Release:        1%{?dist}
Summary:        A compatibility layer for windows applications

License:        LGPL-2.1-or-later
URL:            https://www.winehq.org/
Source0:        https://dl.winehq.org/wine/source/8.0/wine-%{version}.tar.xz
Source10:       https://dl.winehq.org/wine/source/8.0/wine-%{version}.tar.xz.sign

Source1:        wine.systemd
Source2:        wine-README-Fedora

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop

# AppData files
Source150:      wine.appdata.xml

# wine bugs

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

# Autoconf 2.72 support - https://bugzilla.redhat.com/show_bug.cgi?id=2143724
Patch100:       wine-7.22-autoconf-2.72.patch

Patch511:       wine-cjk.patch

%if 0%{?wine_staging}
# wine-staging patches
# pulseaudio-patch is covered by that patch-set, too.
Source900: https://github.com/wine-staging/wine-staging/archive/v%{version}.tar.gz#/wine-staging-%{version}.tar.gz
%endif

%if !%{?no64bit}
%if 0%{?fedora} > 36
ExclusiveArch:  %{ix86} x86_64 aarch64
%else
# Fedora 36 Clang doesn't build PE binaries on ARM at the moment
ExclusiveArch:  %{ix86} x86_64
%endif
%else
ExclusiveArch:  %{ix86}
%endif

BuildRequires:  bison
BuildRequires:  flex
%ifarch  %{arm} aarch64
BuildRequires:  clang >= 5.0
BuildRequires:  lld
%else
BuildRequires:  gcc
%endif
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  freeglut-devel
BuildRequires:  libieee1284-devel

BuildRequires:  librsvg2
BuildRequires:  librsvg2-devel
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libusb-1.0)
%if 0%{?fedora}
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
%endif
BuildRequires:  openldap-devel
BuildRequires:  perl-generators
BuildRequires:  unixODBC-devel
BuildRequires:  sane-backends-devel
BuildRequires:  systemd-devel
BuildRequires:  fontforge freetype-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  libpcap-devel
# modular x
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel mesa-libOSMesa-devel
BuildRequires:  libXxf86dga-devel libXxf86vm-devel
BuildRequires:  libXrandr-devel libXrender-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  fontconfig-devel
BuildRequires:  giflib-devel
BuildRequires:  cups-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXi-devel
BuildRequires:  libXcursor-devel
BuildRequires:  dbus-devel
BuildRequires:  gnutls-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  gsm-devel
BuildRequires:  libv4l-devel
BuildRequires:  fontpackages-devel
BuildRequires:  gettext-devel
BuildRequires:  chrpath
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
%if 0%{?fedora} > 24
BuildRequires:  mpg123-devel
%endif
BuildRequires:  SDL2-devel
BuildRequires:  vulkan-devel
BuildRequires:  libappstream-glib

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
BuildRequires:  gtk3-devel
BuildRequires:  libattr-devel
BuildRequires:  libva-devel
%endif
# 0%%{?wine_staging}

BuildRequires:  icoutils

%ifarch %{ix86} x86_64
BuildRequires:  mingw32-FAudio
BuildRequires:  mingw64-FAudio
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-lcms2
BuildRequires:  mingw64-lcms2
BuildRequires:  mingw32-libpng
BuildRequires:  mingw64-libpng
BuildRequires:  mingw32-libtiff
BuildRequires:  mingw64-libtiff
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw64-libxml2
BuildRequires:  mingw32-libxslt
BuildRequires:  mingw64-libxslt
BuildRequires:  mingw32-vkd3d >= 1.9
BuildRequires:  mingw64-vkd3d >= 1.9
BuildRequires:  mingw32-vulkan-headers
BuildRequires:  mingw64-vulkan-headers
BuildRequires:  mingw32-zlib
BuildRequires:  mingw64-zlib
%endif

Requires:       wine-common = %{version}-%{release}
Requires:       wine-desktop = %{version}-%{release}
Requires:       wine-fonts = %{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
%if 0%{?fedora} || 0%{?rhel}
Requires:       wine-core(x86-32) = %{version}-%{release}
Requires:       wine-cms(x86-32) = %{version}-%{release}
Requires:       wine-ldap(x86-32) = %{version}-%{release}
Requires:       wine-twain(x86-32) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{version}-%{release}
%if 0%{?fedora}
Requires:       wine-opencl(x86-32) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
#  wait for rhbz#968860 to require arch-specific samba-winbind-clients
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif
%if 0%{?fedora} >= 33
Recommends:     wine-dxvk(x86-32)
Recommends:     dosbox-staging
%endif
Recommends:     gstreamer1-plugins-good(x86-32)
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}-%{release}
Requires:       wine-cms(x86-64) = %{version}-%{release}
Requires:       wine-ldap(x86-64) = %{version}-%{release}
Requires:       wine-twain(x86-64) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{version}-%{release}
%if 0%{?fedora}
Requires:       wine-opencl(x86-64) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
Requires:       mesa-dri-drivers(x86-64)
%if 0%{?fedora} >= 33
Recommends:     wine-dxvk(x86-64)
Recommends:     dosbox-staging
%endif
Recommends:     gstreamer1-plugins-good(x86-64)
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{version}-%{release}
Requires:       wine-cms = %{version}-%{release}
Requires:       wine-ldap = %{version}-%{release}
Requires:       wine-twain = %{version}-%{release}
Requires:       wine-pulseaudio = %{version}-%{release}
%if 0%{?fedora}
Requires:       wine-opencl = %{version}-%{release}
%endif
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{version}-%{release}
Requires:       wine-cms(aarch-64) = %{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{version}-%{release}
Requires:       wine-twain(aarch-64) = %{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       mesa-dri-drivers(aarch-64)
%endif

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%package core
Summary:        Wine core package
Requires(postun): /sbin/ldconfig
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       (nss-mdns(x86-32) if nss-mdns(x86-64))
Requires:       gnutls(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXinerama(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       libva(x86-32)
%endif
Requires:  mingw32-FAudio
Requires:  mingw32-lcms2
Requires:  mingw32-libjpeg-turbo
Requires:  mingw32-libpng
Requires:  mingw32-libtiff
Requires:  mingw32-libxml2
Requires:  mingw32-libxslt
Requires:  mingw32-vkd3d >= 1.9
Requires:  mingw32-win-iconv
Requires:  mingw32-zlib
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       (nss-mdns(x86-64) if nss-mdns(x86-32))
Requires:       gnutls(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXinerama(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       libva(x86-64)
%endif
Requires:  mingw64-FAudio
Requires:  mingw64-lcms2
Requires:  mingw64-libjpeg-turbo
Requires:  mingw64-libpng
Requires:  mingw64-libtiff
Requires:  mingw64-libxml2
Requires:  mingw64-libxslt
Requires:  mingw64-vkd3d >= 1.9
Requires:  mingw64-win-iconv
Requires:  mingw64-zlib
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       libXrender
Requires:       libXcursor
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
Requires:       libva
%endif
%endif

Provides:       bundled(libjpeg) = 9e
Provides:       bundled(mpg123-libs) = 1.29.3

# removed as of 7.21
Obsoletes:      wine-openal < 7.21
Provides:       wine-openal = %{version}-%{release}

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%package systemd
Summary:        Systemd config for the wine binfmt handler
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}

%description systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.

%package filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description filesystem
Filesystem directories and basic configuration for wine.

%package common
Summary:        Common files
Requires:       wine-core = %{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package desktop
Summary:        Desktop integration features for wine
Requires(post): desktop-file-utils >= 0.8
Requires(postun): desktop-file-utils >= 0.8
Requires:       wine-core = %{version}-%{release}
Requires:       wine-common = %{version}-%{release}
Requires:       wine-systemd = %{version}-%{release}
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with wine-staging patchset, only.
%if 0%{?wine_staging}
Requires:      wine-arial-fonts = %{version}-%{release}
%else
# 0%%{?wine_staging}
Obsoletes:     wine-arial-fonts <= %{version}-%{release}
%endif
# 0%%{?wine_staging}
Requires:      wine-courier-fonts = %{version}-%{release}
Requires:      wine-fixedsys-fonts = %{version}-%{release}
Requires:      wine-small-fonts = %{version}-%{release}
Requires:      wine-system-fonts = %{version}-%{release}
Requires:      wine-marlett-fonts = %{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{version}-%{release}
Requires:      wine-tahoma-fonts = %{version}-%{release}
# times-new-roman-fonts are available with wine_staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-times-new-roman-fonts = %{version}-%{release}
%else
# 0%%{?wine_staging}
Obsoletes:     wine-times-new-roman-fonts <= %{version}-%{release}
Obsoletes:     wine-times-new-roman-fonts-system <= %{version}-%{release}
%endif
# 0%%{?wine_staging}
Requires:      wine-symbol-fonts = %{version}-%{release}
Requires:      wine-webdings-fonts = %{version}-%{release}
Requires:      wine-wingdings-fonts = %{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
Requires:      liberation-narrow-fonts

%description fonts
%{summary}

%if 0%{?wine_staging}
%package arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description arial-fonts
%{summary}
%endif
# 0%%{?wine_staging}

%package courier-fonts
Summary:       Wine Courier font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description courier-fonts
%{summary}

%package fixedsys-fonts
Summary:       Wine Fixedsys font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description fixedsys-fonts
%{summary}

%package small-fonts
Summary:       Wine Small font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description small-fonts
%{summary}

%package system-fonts
Summary:       Wine System font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description system-fonts
%{summary}


%package marlett-fonts
Summary:       Wine Marlett font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description marlett-fonts
%{summary}


%package ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description ms-sans-serif-fonts
%{summary}

# rhbz#693180
# http://lists.fedoraproject.org/pipermail/devel/2012-June/168153.html
%package tahoma-fonts
Summary:       Wine Tahoma font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{version}-%{release}

%description tahoma-fonts-system
%{summary}

%if 0%{?wine_staging}
%package times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{version}-%{release}

%description times-new-roman-fonts-system
%{summary}
%endif

%package symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
%{summary}

%package webdings-fonts
Summary:       Wine Webdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description webdings-fonts
%{summary}

%package wingdings-fonts
Summary:       Wine Wingdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description wingdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-wingdings-fonts-system package.

%package wingdings-fonts-system
Summary:       Wine Wingdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-wingdings-fonts = %{version}-%{release}

%description wingdings-fonts-system
%{summary}


%package ldap
Summary: LDAP support for wine
Requires: wine-core = %{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Requires: wine-core = %{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Requires: wine-core = %{version}-%{release}
%ifarch %{ix86}
Requires: sane-backends-libs(x86-32)
%endif
%ifarch x86_64
Requires: sane-backends-libs(x86-64)
%endif
%ifarch %{arm} aarch64
Requires: sane-backends-libs
%endif

%description twain
Twain support for wine

%package devel
Summary: Wine development environment
Requires: wine-core = %{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{version}-%{release}

%description pulseaudio
This package adds a pulseaudio driver for wine.

%package alsa
Summary: Alsa support for wine
Requires: wine-core = %{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%if 0%{?fedora}
%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{version}-%{release}

%Description opencl
This package adds the opencl driver for wine.
%endif

%prep
%setup -qn wine-%{version}
%patch -P 100 -p1 -b.autoconf
%patch -P 511 -p1 -b.cjk

%if 0%{?wine_staging}
# setup and apply wine-staging patches
gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

# https://bugs.winehq.org/show_bug.cgi?id=54868
sed -i 's/DWORD pitch_in, DWORD pitch_out/unsigned int pitch_in, unsigned int pitch_out/' patches/wined3d-WINED3DFMT_B8G8R8X8_UNORM/0001-wined3d-Implement-WINED3DFMT_B8G8R8X8_UNORM-to-WINED.patch
staging/patchinstall.py DESTDIR="`pwd`" --all

%endif
# 0%%{?wine_staging}

%build
# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _lto_cflags %{nil}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
%undefine _fortify_level
# Disable Red Hat specs for package notes (Fedora 38+) and annobin.
# MinGW GCC does not support these options.
%if 0%{?fedora_version} == 36
export LDFLAGS="$(echo "%{build_ldflags}" | sed -e 's/-Wl,-z,relro//' -e 's/-Wl,--build-id=sha1//' -e 's/-Wl,-dT,\/home\/abuild\/rpmbuild\/BUILD\/wine.*//' -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//')"
%else
export LDFLAGS="$(echo "%{build_ldflags}" | sed -e 's/-Wl,-z,relro//' -e 's/-Wl,--build-id=sha1//' -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-package-notes//' -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//')"
%endif
%ifarch x86_64
export CFLAGS="$(echo "%{optflags}" | sed -e 's/-O2//' -e 's/-fcf-protection//' -e 's/-fstack-protector-strong//' -e 's/-fstack-clash-protection//' -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//') -O2"
%else
export CFLAGS="$(echo "%{optflags}" | sed -e 's/-fcf-protection//' -e 's/-fstack-protector-strong//' -e 's/-fstack-clash-protection//' -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//')"
%endif

%ifarch  %{arm} aarch64
# Wine enabled -Wl,-WX that turns linker warnings into errors
# Fedora passes '--as-needed' for all binaries and this is a warning from the linker, now an error, so disable flag for now
sed -i 's/-Wl,-WX//g' configure
%if 0%{?fedora} >= 33
%global toolchain clang
%else
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
# Fedora's default compiler flags now conflict with what clang supports
# https://bugzilla.redhat.com/show_bug.cgi?id=1658311
export CFLAGS="`echo $CFLAGS | sed -e 's/-fstack-clash-protection//'`"
%endif
%endif
%ifarch armv7hl
export CFLAGS="`echo $CFLAGS | sed -e 's/-fexceptions//'`"
%endif

# required so that both Linux and Windows development files can be found
unset PKG_CONFIG_PATH

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --with-dbus \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%ifarch x86_64
 --with-system-dllpath=%{mingw64_bindir} \
%endif
%endif
%ifarch %{ix86}
 --with-system-dllpath=%{mingw32_bindir} \
%endif
%{?wine_staging: --with-xattr} \
 --disable-tests

%make_build TARGETFLAGS=""

%install

%make_install \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
%ifarch aarch64
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine64-preloader
%endif
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
%endif
%ifnarch aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
touch %{buildroot}%{_bindir}/wine-preloader
touch %{buildroot}%{_bindir}/wineserver
mv %{buildroot}%{_libdir}/wine/%{winepedir}/dxgi.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-dxgi.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d9.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d9.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10_1.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10_1.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10core.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10core.dll
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d11.dll %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d11.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/dxgi.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d9.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10_1.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10core.dll
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d11.dll

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
%ifarch x86_64 aarch64
chrpath --delete %{buildroot}%{_bindir}/wine64
chrpath --delete %{buildroot}%{_bindir}/wineserver64
%else
chrpath --delete %{buildroot}%{_bindir}/wine32
chrpath --delete %{buildroot}%{_bindir}/wineserver32
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE1} %{buildroot}%{_binfmtdir}/wine.conf

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# add mono dir
mkdir -p %{buildroot}%{_datadir}/wine/mono

# extract and install icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'
MAIN_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="8"\n'\
'   y="8"\n'\
'   viewBox="8, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

# The rest come from programs/, and contain larger scalable icons
# with a new layout that requires the PROGRAM_ICONFIX sed adjustment
install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

# install desktop files
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

cp -p %{SOURCE2} README-FEDORA

cp -p %{SOURCE502} README-tahoma

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/


# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf \
      %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?wine_staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

# install Wingdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
ln -s ../../wine/fonts/wingding.ttf wingding.ttf
popd

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

rm -f %{buildroot}%{_initrddir}/wine

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1

# install and validate AppData file
mkdir -p %{buildroot}/%{_metainfodir}/
install -p -m 0644 %{SOURCE150} %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml


%post systemd
%binfmt_apply wine.conf

%postun systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi

%ldconfig_post core

%posttrans core
# handle upgrades for a few package updates
%{_sbindir}/alternatives --remove 'wine-dxgi%{?_isa}' %{_libdir}/wine/wine-dxgi.dll 2>/dev/null
%{_sbindir}/alternatives --remove 'wine-d3d9%{?_isa}' %{_libdir}/wine/wine-d3d9.dll 2>/dev/null
%{_sbindir}/alternatives --remove 'wine-d3d10%{?_isa}' %{_libdir}/wine/wine-d3d10.dll 2>/dev/null
%{_sbindir}/alternatives --remove 'wine-d3d11%{?_isa}' %{_libdir}/wine/wine-d3d11.dll 2>/dev/null
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/dxgi.dll \
  'wine-dxgi%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-dxgi.dll 10
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d9.dll \
  'wine-d3d9%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d9.dll 10
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d10.dll \
  'wine-d3d10%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10.dll 10 \
  --slave  %{_libdir}/wine/%{winepedir}/d3d10_1.dll 'wine-d3d10_1%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10_1.dll \
  --slave  %{_libdir}/wine/%{winepedir}/d3d10core.dll 'wine-d3d10core%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10core.dll
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d11.dll \
  'wine-d3d11%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d11.dll 10

%postun core
%{?ldconfig}
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
  %{_sbindir}/alternatives --remove 'wine-dxgi%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-dxgi.dll
  %{_sbindir}/alternatives --remove 'wine-d3d9%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d9.dll
  %{_sbindir}/alternatives --remove 'wine-d3d10%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10.dll
  %{_sbindir}/alternatives --remove 'wine-d3d11%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d11.dll
fi

%ldconfig_scriptlets ldap

%ldconfig_scriptlets cms

%ldconfig_scriptlets twain

%ldconfig_scriptlets alsa

%files
# meta package

%files core
%doc ANNOUNCE
%doc COPYING.LIB
%doc LICENSE
%doc LICENSE.OLD
%doc AUTHORS
%doc README-FEDORA
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%{_bindir}/msidb
%{_bindir}/winedump
%{_libdir}/wine/%{winepedir}/explorer.exe
%{_libdir}/wine/%{winepedir}/cabarc.exe
%{_libdir}/wine/%{winepedir}/control.exe
%{_libdir}/wine/%{winepedir}/cmd.exe
%{_libdir}/wine/%{winepedir}/dxdiag.exe
%{_libdir}/wine/%{winepedir}/notepad.exe
%{_libdir}/wine/%{winepedir}/plugplay.exe
%{_libdir}/wine/%{winepedir}/progman.exe
%{_libdir}/wine/%{winepedir}/taskmgr.exe
%{_libdir}/wine/%{winepedir}/winedbg.exe
%{_libdir}/wine/%{winepedir}/winefile.exe
%{_libdir}/wine/%{winepedir}/winemine.exe
%{_libdir}/wine/%{winepedir}/winemsibuilder.exe
%{_libdir}/wine/%{winepedir}/winepath.exe
%{_libdir}/wine/%{winepedir}/winmgmt.exe
%{_libdir}/wine/%{winepedir}/winver.exe
%{_libdir}/wine/%{winepedir}/wordpad.exe
%{_libdir}/wine/%{winepedir}/write.exe
%{_libdir}/wine/%{winepedir}/wusa.exe

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%{_bindir}/wine32-preloader
%{_bindir}/wineserver32
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{_bindir}/wineserver64
%endif
%ifarch x86_64 aarch64
%{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ghost %{_bindir}/wine-preloader
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine

%{_libdir}/wine/%{winepedir}/attrib.exe
%{_libdir}/wine/%{winepedir}/arp.exe
%{_libdir}/wine/%{winepedir}/aspnet_regiis.exe
%{_libdir}/wine/%{winepedir}/cacls.exe
%{_libdir}/wine/%{winepedir}/certutil.exe
%{_libdir}/wine/%{winepedir}/conhost.exe
%{_libdir}/wine/%{winepedir}/cscript.exe
%{_libdir}/wine/%{winepedir}/dism.exe
%{_libdir}/wine/%{winepedir}/dllhost.exe
%{_libdir}/wine/%{winepedir}/dplaysvr.exe
%{_libdir}/wine/%{winepedir}/dpnsvr.exe
%{_libdir}/wine/%{winepedir}/dpvsetup.exe
%{_libdir}/wine/%{winepedir}/eject.exe
%{_libdir}/wine/%{winepedir}/expand.exe
%{_libdir}/wine/%{winepedir}/extrac32.exe
%{_libdir}/wine/%{winepedir}/fc.exe
%{_libdir}/wine/%{winepedir}/find.exe
%{_libdir}/wine/%{winepedir}/findstr.exe
%{_libdir}/wine/%{winepedir}/fsutil.exe
%{_libdir}/wine/%{winepedir}/hostname.exe
%{_libdir}/wine/%{winepedir}/ipconfig.exe
%{_libdir}/wine/%{winepedir}/klist.exe
%{_libdir}/wine/%{winepedir}/mshta.exe
%{_libdir}/wine/%{winepedir}/msidb.exe
%{_libdir}/wine/%{winepedir}/msiexec.exe
%{_libdir}/wine/%{winepedir}/net.exe
%{_libdir}/wine/%{winepedir}/netstat.exe
%{_libdir}/wine/%{winepedir}/ngen.exe
%{_libdir}/wine/%{winepedir}/ntoskrnl.exe
%{_libdir}/wine/%{winepedir}/oleview.exe
%{_libdir}/wine/%{winepedir}/ping.exe
%{_libdir}/wine/%{winepedir}/pnputil.exe
%{_libdir}/wine/%{winepedir}/powershell.exe
%{_libdir}/wine/%{winepedir}/reg.exe
%{_libdir}/wine/%{winepedir}/regasm.exe
%{_libdir}/wine/%{winepedir}/regedit.exe
%{_libdir}/wine/%{winepedir}/regsvcs.exe
%{_libdir}/wine/%{winepedir}/regsvr32.exe
%{_libdir}/wine/%{winepedir}/rpcss.exe
%{_libdir}/wine/%{winepedir}/rundll32.exe
%{_libdir}/wine/%{winepedir}/schtasks.exe
%{_libdir}/wine/%{winepedir}/sdbinst.exe
%{_libdir}/wine/%{winepedir}/secedit.exe
%{_libdir}/wine/%{winepedir}/servicemodelreg.exe
%{_libdir}/wine/%{winepedir}/services.exe
%{_libdir}/wine/%{winepedir}/setx.exe
%{_libdir}/wine/%{winepedir}/start.exe
%{_libdir}/wine/%{winepedir}/tasklist.exe
%{_libdir}/wine/%{winepedir}/termsv.exe
%{_libdir}/wine/%{winepedir}/view.exe
%{_libdir}/wine/%{winepedir}/wevtutil.exe
%{_libdir}/wine/%{winepedir}/where.exe
%{_libdir}/wine/%{winepedir}/whoami.exe
%{_libdir}/wine/%{winepedir}/wineboot.exe
%{_libdir}/wine/%{winepedir}/winebrowser.exe
%{_libdir}/wine/%{winepedir}/wineconsole.exe
%{_libdir}/wine/%{winepedir}/winemenubuilder.exe
%{_libdir}/wine/%{winepedir}/winecfg.exe
%{_libdir}/wine/%{winepedir}/winedevice.exe
%{_libdir}/wine/%{winepedir}/winhlp32.exe
%{_libdir}/wine/%{winepedir}/wmplayer.exe
%{_libdir}/wine/%{winepedir}/wscript.exe
%{_libdir}/wine/%{winepedir}/uninstaller.exe

%{_libdir}/wine/%{winepedir}/acledit.dll
%{_libdir}/wine/%{winepedir}/aclui.dll
%{_libdir}/wine/%{winepedir}/activeds.dll
%{_libdir}/wine/%{winepedir}/activeds.tlb
%{_libdir}/wine/%{winepedir}/actxprxy.dll
%{_libdir}/wine/%{winepedir}/adsldp.dll
%{_libdir}/wine/%{winepedir}/adsldpc.dll
%{_libdir}/wine/%{winepedir}/advapi32.dll
%{_libdir}/wine/%{winepedir}/advpack.dll
%{_libdir}/wine/%{winepedir}/amsi.dll
%{_libdir}/wine/%{winepedir}/amstream.dll
%{_libdir}/wine/%{winepedir}/apisetschema.dll
%{_libdir}/wine/%{winepedir}/apphelp.dll
%{_libdir}/wine/%{winepedir}/appwiz.cpl
%{_libdir}/wine/%{winepedir}/appxdeploymentclient.dll
%{_libdir}/wine/%{winepedir}/atl.dll
%{_libdir}/wine/%{winepedir}/atl80.dll
%{_libdir}/wine/%{winepedir}/atl90.dll
%{_libdir}/wine/%{winepedir}/atl100.dll
%{_libdir}/wine/%{winepedir}/atl110.dll
%{_libdir}/wine/%{winepedir}/atlthunk.dll
%{_libdir}/wine/%{winepedir}/atmlib.dll
%{_libdir}/wine/%{winepedir}/authz.dll
%{_libdir}/wine/%{winepedir}/avicap32.dll
%{_libdir}/wine/%{winesodir}/avicap32.so
%{_libdir}/wine/%{winepedir}/avifil32.dll
%{_libdir}/wine/%{winepedir}/avrt.dll
%{_libdir}/wine/%{winesodir}/bcrypt.so
%{_libdir}/wine/%{winepedir}/bcrypt.dll
%{_libdir}/wine/%{winepedir}/bcryptprimitives.dll
%{_libdir}/wine/%{winepedir}/bluetoothapis.dll
%{_libdir}/wine/%{winepedir}/browseui.dll
%{_libdir}/wine/%{winepedir}/bthprops.cpl
%{_libdir}/wine/%{winepedir}/cabinet.dll
%{_libdir}/wine/%{winepedir}/cards.dll
%{_libdir}/wine/%{winepedir}/cdosys.dll
%{_libdir}/wine/%{winepedir}/cfgmgr32.dll
%{_libdir}/wine/%{winepedir}/chcp.com
%{_libdir}/wine/%{winepedir}/clock.exe
%{_libdir}/wine/%{winepedir}/clusapi.dll
%{_libdir}/wine/%{winepedir}/cng.sys
%{_libdir}/wine/%{winepedir}/combase.dll
%{_libdir}/wine/%{winepedir}/comcat.dll
%{_libdir}/wine/%{winepedir}/comctl32.dll
%{_libdir}/wine/%{winepedir}/comdlg32.dll
%{_libdir}/wine/%{winepedir}/compstui.dll
%{_libdir}/wine/%{winepedir}/comsvcs.dll
%{_libdir}/wine/%{winepedir}/concrt140.dll
%{_libdir}/wine/%{winepedir}/connect.dll
%{_libdir}/wine/%{winepedir}/credui.dll
%{_libdir}/wine/%{winepedir}/crtdll.dll
%{_libdir}/wine/%{winesodir}/crypt32.so
%{_libdir}/wine/%{winepedir}/crypt32.dll
%{_libdir}/wine/%{winepedir}/cryptdlg.dll
%{_libdir}/wine/%{winepedir}/cryptdll.dll
%{_libdir}/wine/%{winepedir}/cryptext.dll
%{_libdir}/wine/%{winepedir}/cryptnet.dll
%{_libdir}/wine/%{winepedir}/cryptowinrt.dll
%{_libdir}/wine/%{winepedir}/cryptsp.dll
%{_libdir}/wine/%{winepedir}/cryptui.dll
%{_libdir}/wine/%{winepedir}/ctapi32.dll
%{_libdir}/wine/%{winesodir}/ctapi32.so
%{_libdir}/wine/%{winepedir}/ctl3d32.dll
%{_libdir}/wine/%{winepedir}/d2d1.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d10.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d10_1.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d10core.dll
%{_libdir}/wine/%{winepedir}/wine-d3d10.dll
%{_libdir}/wine/%{winepedir}/wine-d3d10_1.dll
%{_libdir}/wine/%{winepedir}/wine-d3d10core.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d11.dll
%{_libdir}/wine/%{winepedir}/wine-d3d11.dll
%{_libdir}/wine/%{winepedir}/d3d12.dll
%{_libdir}/wine/%{winepedir}/d3d12core.dll
%{_libdir}/wine/%{winepedir}/d3dcompiler_*.dll
%{_libdir}/wine/%{winepedir}/d3dim.dll
%{_libdir}/wine/%{winepedir}/d3dim700.dll
%{_libdir}/wine/%{winepedir}/d3drm.dll
%{_libdir}/wine/%{winepedir}/d3dx9_*.dll
%{_libdir}/wine/%{winepedir}/d3dx10_*.dll
%{_libdir}/wine/%{winepedir}/d3dx11_42.dll
%{_libdir}/wine/%{winepedir}/d3dx11_43.dll
%{_libdir}/wine/%{winepedir}/d3dxof.dll
%{_libdir}/wine/%{winepedir}/davclnt.dll
%{_libdir}/wine/%{winepedir}/dbgeng.dll
%{_libdir}/wine/%{winepedir}/dbghelp.dll
%{_libdir}/wine/%{winepedir}/dciman32.dll
%{_libdir}/wine/%{winepedir}/dcomp.dll
%{_libdir}/wine/%{winepedir}/ddraw.dll
%{_libdir}/wine/%{winepedir}/ddrawex.dll
%{_libdir}/wine/%{winepedir}/devenum.dll
%{_libdir}/wine/%{winepedir}/dhcpcsvc.dll
%{_libdir}/wine/%{winepedir}/dhcpcsvc6.dll
%{_libdir}/wine/%{winepedir}/dhtmled.ocx
%{_libdir}/wine/%{winepedir}/diasymreader.dll
%{_libdir}/wine/%{winepedir}/difxapi.dll
%{_libdir}/wine/%{winepedir}/dinput.dll
%{_libdir}/wine/%{winepedir}/dinput8.dll
%{_libdir}/wine/%{winepedir}/directmanipulation.dll
%{_libdir}/wine/%{winepedir}/dispex.dll
%{_libdir}/wine/%{winepedir}/dmband.dll
%{_libdir}/wine/%{winepedir}/dmcompos.dll
%{_libdir}/wine/%{winepedir}/dmime.dll
%{_libdir}/wine/%{winepedir}/dmloader.dll
%{_libdir}/wine/%{winepedir}/dmscript.dll
%{_libdir}/wine/%{winepedir}/dmstyle.dll
%{_libdir}/wine/%{winepedir}/dmsynth.dll
%{_libdir}/wine/%{winepedir}/dmusic.dll
%{_libdir}/wine/%{winepedir}/dmusic32.dll
%{_libdir}/wine/%{winepedir}/dplay.dll
%{_libdir}/wine/%{winepedir}/dplayx.dll
%{_libdir}/wine/%{winepedir}/dpnaddr.dll
%{_libdir}/wine/%{winepedir}/dpnet.dll
%{_libdir}/wine/%{winepedir}/dpnhpast.dll
%{_libdir}/wine/%{winepedir}/dpnhupnp.dll
%{_libdir}/wine/%{winepedir}/dpnlobby.dll
%{_libdir}/wine/%{winepedir}/dpvoice.dll
%{_libdir}/wine/%{winepedir}/dpwsockx.dll
%{_libdir}/wine/%{winepedir}/drmclien.dll
%{_libdir}/wine/%{winepedir}/dsound.dll
%{_libdir}/wine/%{winepedir}/dsdmo.dll
%{_libdir}/wine/%{winepedir}/dsquery.dll
%{_libdir}/wine/%{winepedir}/dssenh.dll
%{_libdir}/wine/%{winepedir}/dsuiext.dll
%{_libdir}/wine/%{winepedir}/dswave.dll
%{_libdir}/wine/%{winepedir}/dwmapi.dll
%{_libdir}/wine/%{winepedir}/dwrite.dll
%{_libdir}/wine/%{winesodir}/dwrite.so
%{_libdir}/wine/%{winepedir}/dx8vb.dll
%{_libdir}/wine/%{winepedir}/dxcore.dll
%{_libdir}/wine/%{winepedir}/dxdiagn.dll
%ghost %{_libdir}/wine/%{winepedir}/dxgi.dll
%{_libdir}/wine/%{winepedir}/wine-dxgi.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/dxgkrnl.sys
%{_libdir}/wine/%{winepedir}/dxgmms1.sys
%endif
%{_libdir}/wine/%{winepedir}/dxtrans.dll
%{_libdir}/wine/%{winepedir}/dxva2.dll
%{_libdir}/wine/%{winepedir}/esent.dll
%{_libdir}/wine/%{winepedir}/evr.dll
%{_libdir}/wine/%{winepedir}/explorerframe.dll
%{_libdir}/wine/%{winepedir}/faultrep.dll
%{_libdir}/wine/%{winepedir}/feclient.dll
%{_libdir}/wine/%{winepedir}/fltlib.dll
%{_libdir}/wine/%{winepedir}/fltmgr.sys
%{_libdir}/wine/%{winepedir}/fntcache.dll
%{_libdir}/wine/%{winepedir}/fontsub.dll
%{_libdir}/wine/%{winepedir}/fusion.dll
%{_libdir}/wine/%{winepedir}/fwpuclnt.dll
%{_libdir}/wine/%{winepedir}/gameux.dll
%{_libdir}/wine/%{winepedir}/gamingtcui.dll
%{_libdir}/wine/%{winepedir}/gdi32.dll
%{_libdir}/wine/%{winepedir}/gdiplus.dll
%{_libdir}/wine/%{winepedir}/geolocation.dll
%{_libdir}/wine/%{winepedir}/glu32.dll
%{_libdir}/wine/%{winepedir}/gphoto2.ds
%{_libdir}/wine/%{winesodir}/gphoto2.so
%{_libdir}/wine/%{winepedir}/gpkcsp.dll
%{_libdir}/wine/%{winepedir}/graphicscapture.dll
%{_libdir}/wine/%{winepedir}/hal.dll
%{_libdir}/wine/%{winepedir}/hh.exe
%{_libdir}/wine/%{winepedir}/hhctrl.ocx
%{_libdir}/wine/%{winepedir}/hid.dll
%{_libdir}/wine/%{winepedir}/hidclass.sys
%{_libdir}/wine/%{winepedir}/hidparse.sys
%{_libdir}/wine/%{winepedir}/hlink.dll
%{_libdir}/wine/%{winepedir}/hnetcfg.dll
%{_libdir}/wine/%{winepedir}/hrtfapo.dll
%{_libdir}/wine/%{winepedir}/http.sys
%{_libdir}/wine/%{winepedir}/httpapi.dll
%{_libdir}/wine/%{winepedir}/hvsimanagementapi.dll
%{_libdir}/wine/%{winepedir}/ia2comproxy.dll
%{_libdir}/wine/%{winepedir}/icacls.exe
%{_libdir}/wine/%{winepedir}/iccvid.dll
%{_libdir}/wine/%{winepedir}/icinfo.exe
%{_libdir}/wine/%{winepedir}/icmp.dll
%{_libdir}/wine/%{winepedir}/ieframe.dll
%{_libdir}/wine/%{winepedir}/ieproxy.dll
%{_libdir}/wine/%{winepedir}/imaadp32.acm
%{_libdir}/wine/%{winepedir}/imagehlp.dll
%{_libdir}/wine/%{winepedir}/imm32.dll
%{_libdir}/wine/%{winepedir}/inetcomm.dll
%{_libdir}/wine/%{winepedir}/inetcpl.cpl
%{_libdir}/wine/%{winepedir}/inetmib1.dll
%{_libdir}/wine/%{winepedir}/infosoft.dll
%{_libdir}/wine/%{winepedir}/initpki.dll
%{_libdir}/wine/%{winepedir}/inkobj.dll
%{_libdir}/wine/%{winepedir}/inseng.dll
%{_libdir}/wine/%{winepedir}/iphlpapi.dll
%{_libdir}/wine/%{winepedir}/iprop.dll
%{_libdir}/wine/%{winepedir}/irprops.cpl
%{_libdir}/wine/%{winepedir}/ir50_32.dll
%{_libdir}/wine/%{winepedir}/itircl.dll
%{_libdir}/wine/%{winepedir}/itss.dll
%{_libdir}/wine/%{winepedir}/joy.cpl
%{_libdir}/wine/%{winepedir}/jscript.dll
%{_libdir}/wine/%{winepedir}/jsproxy.dll
%{_libdir}/wine/%{winesodir}/kerberos.so
%{_libdir}/wine/%{winepedir}/kerberos.dll
%{_libdir}/wine/%{winepedir}/kernel32.dll
%{_libdir}/wine/%{winepedir}/kernelbase.dll
%{_libdir}/wine/%{winepedir}/ksecdd.sys
%{_libdir}/wine/%{winepedir}/ksproxy.ax
%{_libdir}/wine/%{winepedir}/ksuser.dll
%{_libdir}/wine/%{winepedir}/ktmw32.dll
%{_libdir}/wine/%{winepedir}/l3codeca.acm
%{_libdir}/wine/%{winepedir}/light.msstyles
%{_libdir}/wine/%{winepedir}/loadperf.dll
%{_libdir}/wine/%{winesodir}/localspl.so
%{_libdir}/wine/%{winepedir}/localspl.dll
%{_libdir}/wine/%{winepedir}/localui.dll
%{_libdir}/wine/%{winepedir}/lodctr.exe
%{_libdir}/wine/%{winepedir}/lz32.dll
%{_libdir}/wine/%{winepedir}/magnification.dll
%{_libdir}/wine/%{winepedir}/mapi32.dll
%{_libdir}/wine/%{winepedir}/mapistub.dll
%{_libdir}/wine/%{winepedir}/mciavi32.dll
%{_libdir}/wine/%{winepedir}/mcicda.dll
%{_libdir}/wine/%{winepedir}/mciqtz32.dll
%{_libdir}/wine/%{winepedir}/mciseq.dll
%{_libdir}/wine/%{winepedir}/mciwave.dll
%{_libdir}/wine/%{winepedir}/mf.dll
%{_libdir}/wine/%{winepedir}/mf3216.dll
%{_libdir}/wine/%{winepedir}/mferror.dll
%{_libdir}/wine/%{winepedir}/mfmediaengine.dll
%{_libdir}/wine/%{winepedir}/mfplat.dll
%{_libdir}/wine/%{winepedir}/mfplay.dll
%{_libdir}/wine/%{winepedir}/mfreadwrite.dll
%{_libdir}/wine/%{winepedir}/mfsrcsnk.dll
%{_libdir}/wine/%{winepedir}/mgmtapi.dll
%{_libdir}/wine/%{winepedir}/midimap.dll
%{_libdir}/wine/%{winepedir}/mlang.dll
%{_libdir}/wine/%{winepedir}/mmcndmgr.dll
%{_libdir}/wine/%{winepedir}/mmdevapi.dll
%{_libdir}/wine/%{winepedir}/mofcomp.exe
%{_libdir}/wine/%{winesodir}/mountmgr.so
%{_libdir}/wine/%{winepedir}/mountmgr.sys
%{_libdir}/wine/%{winepedir}/mp3dmod.dll
%{_libdir}/wine/%{winepedir}/mpr.dll
%{_libdir}/wine/%{winepedir}/mprapi.dll
%{_libdir}/wine/%{winepedir}/msacm32.dll
%{_libdir}/wine/%{winepedir}/msacm32.drv
%{_libdir}/wine/%{winepedir}/msado15.dll
%{_libdir}/wine/%{winepedir}/msadp32.acm
%{_libdir}/wine/%{winepedir}/msasn1.dll
%{_libdir}/wine/%{winepedir}/msauddecmft.dll
%{_libdir}/wine/%{winepedir}/mscat32.dll
%{_libdir}/wine/%{winepedir}/mscoree.dll
%{_libdir}/wine/%{winepedir}/mscorwks.dll
%{_libdir}/wine/%{winepedir}/msctf.dll
%{_libdir}/wine/%{winepedir}/msctfmonitor.dll
%{_libdir}/wine/%{winepedir}/msctfp.dll
%{_libdir}/wine/%{winepedir}/msdaps.dll
%{_libdir}/wine/%{winepedir}/msdasql.dll
%{_libdir}/wine/%{winepedir}/msdelta.dll
%{_libdir}/wine/%{winepedir}/msdmo.dll
%{_libdir}/wine/%{winepedir}/msdrm.dll
%{_libdir}/wine/%{winepedir}/msftedit.dll
%{_libdir}/wine/%{winepedir}/msg711.acm
%{_libdir}/wine/%{winepedir}/msgsm32.acm
%{_libdir}/wine/%{winepedir}/mshtml.dll
%{_libdir}/wine/%{winepedir}/mshtml.tlb
%{_libdir}/wine/%{winepedir}/msi.dll
%{_libdir}/wine/%{winepedir}/msident.dll
%{_libdir}/wine/%{winepedir}/msimtf.dll
%{_libdir}/wine/%{winepedir}/msimg32.dll
%{_libdir}/wine/%{winepedir}/msimsg.dll
%{_libdir}/wine/%{winepedir}/msinfo32.exe
%{_libdir}/wine/%{winepedir}/msisip.dll
%{_libdir}/wine/%{winepedir}/msisys.ocx
%{_libdir}/wine/%{winepedir}/msls31.dll
%{_libdir}/wine/%{winepedir}/msmpeg2vdec.dll
%{_libdir}/wine/%{winepedir}/msnet32.dll
%{_libdir}/wine/%{winepedir}/mspatcha.dll
%{_libdir}/wine/%{winepedir}/msports.dll
%{_libdir}/wine/%{winepedir}/msscript.ocx
%{_libdir}/wine/%{winepedir}/mssign32.dll
%{_libdir}/wine/%{winepedir}/mssip32.dll
%{_libdir}/wine/%{winepedir}/msrle32.dll
%{_libdir}/wine/%{winepedir}/mstask.dll
%{_libdir}/wine/%{winepedir}/msv1_0.dll
%{_libdir}/wine/%{winesodir}/msv1_0.so
%{_libdir}/wine/%{winepedir}/msvcirt.dll
%{_libdir}/wine/%{winepedir}/msvcm80.dll
%{_libdir}/wine/%{winepedir}/msvcm90.dll
%{_libdir}/wine/%{winepedir}/msvcp_win.dll
%{_libdir}/wine/%{winepedir}/msvcp60.dll
%{_libdir}/wine/%{winepedir}/msvcp70.dll
%{_libdir}/wine/%{winepedir}/msvcp71.dll
%{_libdir}/wine/%{winepedir}/msvcp80.dll
%{_libdir}/wine/%{winepedir}/msvcp90.dll
%{_libdir}/wine/%{winepedir}/msvcp100.dll
%{_libdir}/wine/%{winepedir}/msvcp110.dll
%{_libdir}/wine/%{winepedir}/msvcp120.dll
%{_libdir}/wine/%{winepedir}/msvcp120_app.dll
%{_libdir}/wine/%{winepedir}/msvcp140.dll
%{_libdir}/wine/%{winepedir}/msvcp140_1.dll
%{_libdir}/wine/%{winepedir}/msvcp140_2.dll
%{_libdir}/wine/%{winepedir}/msvcp140_atomic_wait.dll
%{_libdir}/wine/%{winepedir}/msvcp140_codecvt_ids.dll
%{_libdir}/wine/%{winepedir}/msvcr70.dll
%{_libdir}/wine/%{winepedir}/msvcr71.dll
%{_libdir}/wine/%{winepedir}/msvcr80.dll
%{_libdir}/wine/%{winepedir}/msvcr90.dll
%{_libdir}/wine/%{winepedir}/msvcr100.dll
%{_libdir}/wine/%{winepedir}/msvcr110.dll
%{_libdir}/wine/%{winepedir}/msvcr120.dll
%{_libdir}/wine/%{winepedir}/msvcr120_app.dll
%{_libdir}/wine/%{winepedir}/msvcrt.dll
%{_libdir}/wine/%{winepedir}/msvcrt20.dll
%{_libdir}/wine/%{winepedir}/msvcrt40.dll
%{_libdir}/wine/%{winepedir}/msvcrtd.dll
%{_libdir}/wine/%{winepedir}/msvfw32.dll
%{_libdir}/wine/%{winepedir}/msvidc32.dll
%{_libdir}/wine/%{winepedir}/mswsock.dll
%{_libdir}/wine/%{winepedir}/msxml.dll
%{_libdir}/wine/%{winepedir}/msxml2.dll
%{_libdir}/wine/%{winepedir}/msxml3.dll
%{_libdir}/wine/%{winepedir}/msxml4.dll
%{_libdir}/wine/%{winepedir}/msxml6.dll
%{_libdir}/wine/%{winepedir}/mtxdm.dll
%{_libdir}/wine/%{winepedir}/nddeapi.dll
%{_libdir}/wine/%{winepedir}/ncrypt.dll
%{_libdir}/wine/%{winepedir}/ndis.sys
%{_libdir}/wine/%{winesodir}/netapi32.so
%{_libdir}/wine/%{winepedir}/netapi32.dll
%{_libdir}/wine/%{winepedir}/netcfgx.dll
%{_libdir}/wine/%{winepedir}/netio.sys
%{_libdir}/wine/%{winepedir}/netprofm.dll
%{_libdir}/wine/%{winepedir}/netsh.exe
%{_libdir}/wine/%{winepedir}/netutils.dll
%{_libdir}/wine/%{winepedir}/newdev.dll
%{_libdir}/wine/%{winepedir}/ninput.dll
%{_libdir}/wine/%{winepedir}/normaliz.dll
%{_libdir}/wine/%{winepedir}/npmshtml.dll
%{_libdir}/wine/%{winepedir}/npptools.dll
%{_libdir}/wine/%{winepedir}/nsi.dll
%{_libdir}/wine/%{winesodir}/nsiproxy.so
%{_libdir}/wine/%{winepedir}/nsiproxy.sys
%{_libdir}/wine/%{winesodir}/ntdll.so
%{_libdir}/wine/%{winepedir}/ntdll.dll
%{_libdir}/wine/%{winepedir}/ntdsapi.dll
%{_libdir}/wine/%{winepedir}/ntprint.dll
%if 0%{?wine_staging}
#%%{_libdir}/wine/%%{winepedir}/nvcuda.dll
#%%{_libdir}/wine/%%{winesodir}/nvcuda.dll.so
#%%{_libdir}/wine/%%{winepedir}/nvcuvid.dll
#%%{_libdir}/wine/%%{winesodir}/nvcuvid.dll.so
%endif
%{_libdir}/wine/%{winepedir}/objsel.dll
%{_libdir}/wine/%{winesodir}/odbc32.so
%{_libdir}/wine/%{winepedir}/odbc32.dll
%{_libdir}/wine/%{winepedir}/odbcbcp.dll
%{_libdir}/wine/%{winepedir}/odbccp32.dll
%{_libdir}/wine/%{winepedir}/odbccu32.dll
%{_libdir}/wine/%{winepedir}/ole32.dll
%{_libdir}/wine/%{winepedir}/oleacc.dll
%{_libdir}/wine/%{winepedir}/oleaut32.dll
%{_libdir}/wine/%{winepedir}/olecli32.dll
%{_libdir}/wine/%{winepedir}/oledb32.dll
%{_libdir}/wine/%{winepedir}/oledlg.dll
%{_libdir}/wine/%{winepedir}/olepro32.dll
%{_libdir}/wine/%{winepedir}/olesvr32.dll
%{_libdir}/wine/%{winepedir}/olethk32.dll
%{_libdir}/wine/%{winepedir}/opcservices.dll
%{_libdir}/wine/%{winepedir}/packager.dll
%{_libdir}/wine/%{winepedir}/pdh.dll
%{_libdir}/wine/%{winepedir}/photometadatahandler.dll
%{_libdir}/wine/%{winepedir}/pidgen.dll
%{_libdir}/wine/%{winepedir}/powrprof.dll
%{_libdir}/wine/%{winepedir}/presentationfontcache.exe
%{_libdir}/wine/%{winepedir}/printui.dll
%{_libdir}/wine/%{winepedir}/prntvpt.dll
%{_libdir}/wine/%{winepedir}/propsys.dll
%{_libdir}/wine/%{winepedir}/psapi.dll
%{_libdir}/wine/%{winepedir}/pstorec.dll
%{_libdir}/wine/%{winepedir}/pwrshplugin.dll
%{_libdir}/wine/%{winepedir}/qasf.dll
%{_libdir}/wine/%{winepedir}/qcap.dll
%{_libdir}/wine/%{winesodir}/qcap.so
%{_libdir}/wine/%{winepedir}/qdvd.dll
%{_libdir}/wine/%{winepedir}/qedit.dll
%{_libdir}/wine/%{winepedir}/qmgr.dll
%{_libdir}/wine/%{winepedir}/qmgrprxy.dll
%{_libdir}/wine/%{winepedir}/quartz.dll
%{_libdir}/wine/%{winepedir}/query.dll
%{_libdir}/wine/%{winepedir}/qwave.dll
%{_libdir}/wine/%{winepedir}/rasapi32.dll
%{_libdir}/wine/%{winepedir}/rasdlg.dll
%{_libdir}/wine/%{winepedir}/regapi.dll
%{_libdir}/wine/%{winepedir}/regini.exe
%{_libdir}/wine/%{winepedir}/resutils.dll
%{_libdir}/wine/%{winepedir}/riched20.dll
%{_libdir}/wine/%{winepedir}/riched32.dll
%{_libdir}/wine/%{winepedir}/robocopy.exe
%{_libdir}/wine/%{winepedir}/rpcrt4.dll
%{_libdir}/wine/%{winepedir}/rsabase.dll
%{_libdir}/wine/%{winepedir}/rsaenh.dll
%{_libdir}/wine/%{winepedir}/rstrtmgr.dll
%{_libdir}/wine/%{winepedir}/rtutils.dll
%{_libdir}/wine/%{winepedir}/rtworkq.dll
%{_libdir}/wine/%{winepedir}/samlib.dll
%{_libdir}/wine/%{winepedir}/sapi.dll
%{_libdir}/wine/%{winepedir}/sas.dll
%{_libdir}/wine/%{winepedir}/sc.exe
%{_libdir}/wine/%{winepedir}/scarddlg.dll
%{_libdir}/wine/%{winepedir}/scardsvr.dll
%{_libdir}/wine/%{winepedir}/sccbase.dll
%{_libdir}/wine/%{winepedir}/schannel.dll
%{_libdir}/wine/%{winepedir}/scrobj.dll
%{_libdir}/wine/%{winepedir}/scrrun.dll
%{_libdir}/wine/%{winepedir}/scsiport.sys
%{_libdir}/wine/%{winepedir}/sechost.dll
%{_libdir}/wine/%{winepedir}/secur32.dll
%{_libdir}/wine/%{winesodir}/secur32.so
%{_libdir}/wine/%{winepedir}/sensapi.dll
%{_libdir}/wine/%{winepedir}/serialui.dll
%{_libdir}/wine/%{winepedir}/setupapi.dll
%{_libdir}/wine/%{winepedir}/sfc_os.dll
%{_libdir}/wine/%{winepedir}/shcore.dll
%{_libdir}/wine/%{winepedir}/shdoclc.dll
%{_libdir}/wine/%{winepedir}/shdocvw.dll
%{_libdir}/wine/%{winepedir}/schedsvc.dll
%{_libdir}/wine/%{winepedir}/shell32.dll
%{_libdir}/wine/%{winepedir}/shfolder.dll
%{_libdir}/wine/%{winepedir}/shlwapi.dll
%{_libdir}/wine/%{winepedir}/shutdown.exe
%{_libdir}/wine/%{winepedir}/slbcsp.dll
%{_libdir}/wine/%{winepedir}/slc.dll
%{_libdir}/wine/%{winepedir}/snmpapi.dll
%{_libdir}/wine/%{winepedir}/softpub.dll
%{_libdir}/wine/%{winepedir}/spoolsv.exe
%{_libdir}/wine/%{winepedir}/sppc.dll
%{_libdir}/wine/%{winepedir}/srclient.dll
%{_libdir}/wine/%{winepedir}/srvcli.dll
%{_libdir}/wine/%{winepedir}/srvsvc.dll
%{_libdir}/wine/%{winepedir}/sspicli.dll
%{_libdir}/wine/%{winepedir}/stdole2.tlb
%{_libdir}/wine/%{winepedir}/stdole32.tlb
%{_libdir}/wine/%{winepedir}/sti.dll
%{_libdir}/wine/%{winepedir}/strmdll.dll
%{_libdir}/wine/%{winepedir}/subst.exe
%{_libdir}/wine/%{winepedir}/svchost.exe
%{_libdir}/wine/%{winepedir}/svrapi.dll
%{_libdir}/wine/%{winepedir}/sxs.dll
%{_libdir}/wine/%{winepedir}/systeminfo.exe
%{_libdir}/wine/%{winepedir}/t2embed.dll
%{_libdir}/wine/%{winepedir}/tapi32.dll
%{_libdir}/wine/%{winepedir}/taskkill.exe
%{_libdir}/wine/%{winepedir}/taskschd.dll
%{_libdir}/wine/%{winepedir}/tbs.dll
%{_libdir}/wine/%{winepedir}/tdh.dll
%{_libdir}/wine/%{winepedir}/tdi.sys
%{_libdir}/wine/%{winepedir}/threadpoolwinrt.dll
%{_libdir}/wine/%{winepedir}/traffic.dll
%{_libdir}/wine/%{winepedir}/twinapi.appcore.dll
%{_libdir}/wine/%{winepedir}/tzres.dll
%{_libdir}/wine/%{winepedir}/ucrtbase.dll
%{_libdir}/wine/%{winepedir}/uianimation.dll
%{_libdir}/wine/%{winepedir}/uiautomationcore.dll
%{_libdir}/wine/%{winepedir}/uiribbon.dll
%{_libdir}/wine/%{winepedir}/unicows.dll
%{_libdir}/wine/%{winepedir}/unlodctr.exe
%{_libdir}/wine/%{winepedir}/updspapi.dll
%{_libdir}/wine/%{winepedir}/url.dll
%{_libdir}/wine/%{winepedir}/urlmon.dll
%{_libdir}/wine/%{winepedir}/usbd.sys
%{_libdir}/wine/%{winepedir}/user32.dll
%{_libdir}/wine/%{winepedir}/usp10.dll
%{_libdir}/wine/%{winepedir}/utildll.dll
%{_libdir}/wine/%{winepedir}/uxtheme.dll
%{_libdir}/wine/%{winepedir}/userenv.dll
%{_libdir}/wine/%{winepedir}/vbscript.dll
%{_libdir}/wine/%{winepedir}/vcomp.dll
%{_libdir}/wine/%{winepedir}/vcomp90.dll
%{_libdir}/wine/%{winepedir}/vcomp100.dll
%{_libdir}/wine/%{winepedir}/vcomp110.dll
%{_libdir}/wine/%{winepedir}/vcomp120.dll
%{_libdir}/wine/%{winepedir}/vcomp140.dll
%{_libdir}/wine/%{winepedir}/vcruntime140.dll
%{_libdir}/wine/%{winepedir}/vcruntime140_1.dll
%{_libdir}/wine/%{winepedir}/vdmdbg.dll
%{_libdir}/wine/%{winepedir}/version.dll
%{_libdir}/wine/%{winepedir}/vga.dll
%{_libdir}/wine/%{winepedir}/virtdisk.dll
%{_libdir}/wine/%{winepedir}/vssapi.dll
%{_libdir}/wine/%{winepedir}/vulkan-1.dll
%{_libdir}/wine/%{winepedir}/wbemdisp.dll
%{_libdir}/wine/%{winepedir}/wbemprox.dll
%{_libdir}/wine/%{winepedir}/wdscore.dll
%{_libdir}/wine/%{winepedir}/webservices.dll
%{_libdir}/wine/%{winepedir}/websocket.dll
%{_libdir}/wine/%{winepedir}/wer.dll
%{_libdir}/wine/%{winepedir}/wevtapi.dll
%{_libdir}/wine/%{winepedir}/wevtsvc.dll
%{_libdir}/wine/%{winepedir}/wiaservc.dll
%{_libdir}/wine/%{winepedir}/wimgapi.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/win32k.sys
%endif
%{_libdir}/wine/%{winepedir}/win32u.dll
%{_libdir}/wine/%{winepedir}/windows.applicationmodel.dll
%{_libdir}/wine/%{winepedir}/windows.devices.bluetooth.dll
%{_libdir}/wine/%{winepedir}/windows.devices.enumeration.dll
%{_libdir}/wine/%{winepedir}/windows.devices.usb.dll
%{_libdir}/wine/%{winepedir}/windows.gaming.ui.gamebar.dll
%{_libdir}/wine/%{winepedir}/windows.gaming.input.dll
%{_libdir}/wine/%{winepedir}/windows.globalization.dll
%{_libdir}/wine/%{winepedir}/windows.media.dll
%{_libdir}/wine/%{winepedir}/windows.media.devices.dll
%{_libdir}/wine/%{winepedir}/windows.media.mediacontrol.dll
%{_libdir}/wine/%{winepedir}/windows.media.speech.dll
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/windows.networking.connectivity
%endif
%{_libdir}/wine/%{winepedir}/windows.networking.dll
%{_libdir}/wine/%{winepedir}/windows.networking.hostname.dll
%{_libdir}/wine/%{winepedir}/windows.perception.stub.dll
%{_libdir}/wine/%{winepedir}/windows.security.credentials.ui.userconsentverifier.dll
%{_libdir}/wine/%{winepedir}/windows.storage.applicationdata.dll
%{_libdir}/wine/%{winepedir}/windows.system.profile.systemmanufacturers.dll
%{_libdir}/wine/%{winepedir}/windows.ui.dll
%{_libdir}/wine/%{winepedir}/windowscodecs.dll
%{_libdir}/wine/%{winepedir}/windowscodecsext.dll
%{_libdir}/wine/%{winepedir}/winebus.sys
%{_libdir}/wine/%{winesodir}/winegstreamer.so
%{_libdir}/wine/%{winepedir}/winegstreamer.dll
%{_libdir}/wine/%{winepedir}/winehid.sys
%{_libdir}/wine/%{winepedir}/winemapi.dll
%{_libdir}/wine/%{winepedir}/wineusb.sys
%{_libdir}/wine/%{winesodir}/wineusb.so
%{_libdir}/wine/%{winesodir}/winevulkan.so
%{_libdir}/wine/%{winepedir}/winevulkan.dll
%{_libdir}/wine/%{winepedir}/winewayland.drv
%{_libdir}/wine/%{winesodir}/winewayland.so
%{_libdir}/wine/%{winepedir}/winex11.drv
%{_libdir}/wine/%{winesodir}/winex11.so
%{_libdir}/wine/%{winepedir}/wing32.dll
%{_libdir}/wine/%{winepedir}/winhttp.dll
%{_libdir}/wine/%{winepedir}/wininet.dll
%{_libdir}/wine/%{winepedir}/winmm.dll
%{_libdir}/wine/%{winepedir}/winnls32.dll
%{_libdir}/wine/%{winepedir}/winprint.dll
%{_libdir}/wine/%{winepedir}/winspool.drv
%{_libdir}/wine/%{winesodir}/winspool.so
%{_libdir}/wine/%{winepedir}/winsta.dll
%{_libdir}/wine/%{winepedir}/wintypes.dll
%{_libdir}/wine/%{winepedir}/wldp.dll
%{_libdir}/wine/%{winepedir}/wmasf.dll
%{_libdir}/wine/%{winepedir}/wmi.dll
%{_libdir}/wine/%{winepedir}/wmic.exe
%{_libdir}/wine/%{winepedir}/wmiutils.dll
%{_libdir}/wine/%{winepedir}/wmp.dll
%{_libdir}/wine/%{winepedir}/wmvcore.dll
%{_libdir}/wine/%{winepedir}/spoolss.dll
%{_libdir}/wine/%{winesodir}/win32u.so
%{_libdir}/wine/%{winesodir}/winebus.so
%{_libdir}/wine/%{winepedir}/winexinput.sys
%{_libdir}/wine/%{winepedir}/wintab32.dll
%{_libdir}/wine/%{winepedir}/wintrust.dll
%{_libdir}/wine/%{winepedir}/winusb.dll
%{_libdir}/wine/%{winepedir}/wlanapi.dll
%{_libdir}/wine/%{winepedir}/wlanui.dll
%{_libdir}/wine/%{winepedir}/wmphoto.dll
%{_libdir}/wine/%{winepedir}/wnaspi32.dll
%{_libdir}/wine/%{winepedir}/wofutil.dll
%ifarch x86_64 aarch64
%{_libdir}/wine/%{winepedir}/wow64.dll
%{_libdir}/wine/%{winepedir}/wow64win.dll
%endif
%ifarch x86_64
%{_libdir}/wine/%{winepedir}/wow64cpu.dll
%endif
%{_libdir}/wine/%{winepedir}/wpc.dll
%{_libdir}/wine/%{winepedir}/wpcap.dll
%{_libdir}/wine/%{winesodir}/wpcap.so
%{_libdir}/wine/%{winepedir}/ws2_32.dll
%{_libdir}/wine/%{winesodir}/ws2_32.so
%{_libdir}/wine/%{winepedir}/wsdapi.dll
%{_libdir}/wine/%{winepedir}/wshom.ocx
%{_libdir}/wine/%{winepedir}/wsnmp32.dll
%{_libdir}/wine/%{winepedir}/wsock32.dll
%{_libdir}/wine/%{winepedir}/wtsapi32.dll
%{_libdir}/wine/%{winepedir}/wuapi.dll
%{_libdir}/wine/%{winepedir}/wuaueng.dll
%{_libdir}/wine/%{winepedir}/wuauserv.exe
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/wuauserv.exe.so
%endif
%{_libdir}/wine/%{winepedir}/security.dll
%{_libdir}/wine/%{winepedir}/sfc.dll
%{_libdir}/wine/%{winepedir}/wineps.drv
%{_libdir}/wine/%{winesodir}/wineps.so
%{_libdir}/wine/%{winepedir}/d3d8.dll
%{_libdir}/wine/%{winepedir}/d3d8thk.dll
%ghost %{_libdir}/wine/%{winepedir}/d3d9.dll
%{_libdir}/wine/%{winepedir}/wine-d3d9.dll
%{_libdir}/wine/%{winesodir}/opengl32.so
%{_libdir}/wine/%{winepedir}/opengl32.dll
%{_libdir}/wine/%{winepedir}/wined3d.dll
%{_libdir}/wine/%{winepedir}/dnsapi.dll
%{_libdir}/wine/%{winesodir}/dnsapi.so
%{_libdir}/wine/%{winepedir}/iexplore.exe
%{_libdir}/wine/%{winepedir}/x3daudio1_0.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_1.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_2.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_3.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_4.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_5.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_6.dll
%{_libdir}/wine/%{winepedir}/x3daudio1_7.dll
%{_libdir}/wine/%{winepedir}/xactengine2_0.dll
%{_libdir}/wine/%{winepedir}/xactengine2_4.dll
%{_libdir}/wine/%{winepedir}/xactengine2_7.dll
%{_libdir}/wine/%{winepedir}/xactengine2_9.dll
%{_libdir}/wine/%{winepedir}/xactengine3_0.dll
%{_libdir}/wine/%{winepedir}/xactengine3_1.dll
%{_libdir}/wine/%{winepedir}/xactengine3_2.dll
%{_libdir}/wine/%{winepedir}/xactengine3_3.dll
%{_libdir}/wine/%{winepedir}/xactengine3_4.dll
%{_libdir}/wine/%{winepedir}/xactengine3_5.dll
%{_libdir}/wine/%{winepedir}/xactengine3_6.dll
%{_libdir}/wine/%{winepedir}/xactengine3_7.dll
%{_libdir}/wine/%{winepedir}/xapofx1_1.dll
%{_libdir}/wine/%{winepedir}/xapofx1_2.dll
%{_libdir}/wine/%{winepedir}/xapofx1_3.dll
%{_libdir}/wine/%{winepedir}/xapofx1_4.dll
%{_libdir}/wine/%{winepedir}/xapofx1_5.dll
%{_libdir}/wine/%{winepedir}/xaudio2_0.dll
%{_libdir}/wine/%{winepedir}/xaudio2_1.dll
%{_libdir}/wine/%{winepedir}/xaudio2_2.dll
%{_libdir}/wine/%{winepedir}/xaudio2_3.dll
%{_libdir}/wine/%{winepedir}/xaudio2_4.dll
%{_libdir}/wine/%{winepedir}/xaudio2_5.dll
%{_libdir}/wine/%{winepedir}/xaudio2_6.dll
%{_libdir}/wine/%{winepedir}/xaudio2_7.dll
%{_libdir}/wine/%{winepedir}/xaudio2_8.dll
%{_libdir}/wine/%{winepedir}/xaudio2_9.dll
%{_libdir}/wine/%{winepedir}/xcopy.exe
%{_libdir}/wine/%{winepedir}/xinput1_1.dll
%{_libdir}/wine/%{winepedir}/xinput1_2.dll
%{_libdir}/wine/%{winepedir}/xinput1_3.dll
%{_libdir}/wine/%{winepedir}/xinput1_4.dll
%{_libdir}/wine/%{winepedir}/xinput9_1_0.dll
%{_libdir}/wine/%{winepedir}/xinputuap.dll
%{_libdir}/wine/%{winepedir}/xmllite.dll
%{_libdir}/wine/%{winepedir}/xolehlp.dll
%{_libdir}/wine/%{winepedir}/xpsprint.dll
%{_libdir}/wine/%{winepedir}/xpssvcs.dll

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
#%%{_libdir}/wine/%%{winepedir}/nvapi64.dll
#%%{_libdir}/wine/%%{winepedir}/nvencodeapi64.dll
#%%{_libdir}/wine/%%{winesodir}/nvencodeapi64.dll.so
%else
#%%{_libdir}/wine/%%{winepedir}/nvapi.dll
%ifarch %{arm}
#%%{_libdir}/wine/%%{winesodir}/nvapi.dll.so
%endif
#%%{_libdir}/wine/%%{winepedir}/nvencodeapi.dll
#%%{_libdir}/wine/%%{winesodir}/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/%{winepedir}/winevdm.exe
%{_libdir}/wine/%{winepedir}/ifsmgr.vxd
%{_libdir}/wine/%{winepedir}/mmdevldr.vxd
%{_libdir}/wine/%{winepedir}/monodebg.vxd
%{_libdir}/wine/%{winepedir}/rundll.exe16
%{_libdir}/wine/%{winepedir}/vdhcp.vxd
%{_libdir}/wine/%{winepedir}/user.exe16
%{_libdir}/wine/%{winepedir}/vmm.vxd
%{_libdir}/wine/%{winepedir}/vnbt.vxd
%{_libdir}/wine/%{winepedir}/vnetbios.vxd
%{_libdir}/wine/%{winepedir}/vtdapi.vxd
%{_libdir}/wine/%{winepedir}/vwin32.vxd
%{_libdir}/wine/%{winepedir}/w32skrnl.dll
%{_libdir}/wine/%{winepedir}/avifile.dll16
%{_libdir}/wine/%{winepedir}/comm.drv16
%{_libdir}/wine/%{winepedir}/commdlg.dll16
%{_libdir}/wine/%{winepedir}/compobj.dll16
%{_libdir}/wine/%{winepedir}/ctl3d.dll16
%{_libdir}/wine/%{winepedir}/ctl3dv2.dll16
%{_libdir}/wine/%{winepedir}/ddeml.dll16
%{_libdir}/wine/%{winepedir}/dispdib.dll16
%{_libdir}/wine/%{winepedir}/display.drv16
%{_libdir}/wine/%{winepedir}/gdi.exe16
%{_libdir}/wine/%{winepedir}/imm.dll16
%{_libdir}/wine/%{winepedir}/krnl386.exe16
%{_libdir}/wine/%{winepedir}/keyboard.drv16
%{_libdir}/wine/%{winepedir}/lzexpand.dll16
%{_libdir}/wine/%{winepedir}/mmsystem.dll16
%{_libdir}/wine/%{winepedir}/mouse.drv16
%{_libdir}/wine/%{winepedir}/msacm.dll16
%{_libdir}/wine/%{winepedir}/msvideo.dll16
%{_libdir}/wine/%{winepedir}/ole2.dll16
%{_libdir}/wine/%{winepedir}/ole2conv.dll16
%{_libdir}/wine/%{winepedir}/ole2disp.dll16
%{_libdir}/wine/%{winepedir}/ole2nls.dll16
%{_libdir}/wine/%{winepedir}/ole2prox.dll16
%{_libdir}/wine/%{winepedir}/ole2thk.dll16
%{_libdir}/wine/%{winepedir}/olecli.dll16
%{_libdir}/wine/%{winepedir}/olesvr.dll16
%{_libdir}/wine/%{winepedir}/rasapi16.dll16
%{_libdir}/wine/%{winepedir}/setupx.dll16
%{_libdir}/wine/%{winepedir}/shell.dll16
%{_libdir}/wine/%{winepedir}/sound.drv16
%{_libdir}/wine/%{winepedir}/storage.dll16
%{_libdir}/wine/%{winepedir}/stress.dll16
%{_libdir}/wine/%{winepedir}/system.drv16
%{_libdir}/wine/%{winepedir}/toolhelp.dll16
%{_libdir}/wine/%{winepedir}/twain.dll16
%{_libdir}/wine/%{winepedir}/typelib.dll16
%{_libdir}/wine/%{winepedir}/ver.dll16
%{_libdir}/wine/%{winepedir}/w32sys.dll16
%{_libdir}/wine/%{winepedir}/win32s16.dll16
%{_libdir}/wine/%{winepedir}/win87em.dll16
%{_libdir}/wine/%{winepedir}/winaspi.dll16
%{_libdir}/wine/%{winepedir}/windebug.dll16
%{_libdir}/wine/%{winepedir}/wineps16.drv16
%{_libdir}/wine/%{winepedir}/wing.dll16
%{_libdir}/wine/%{winepedir}/winhelp.exe16
%{_libdir}/wine/%{winepedir}/winnls.dll16
%{_libdir}/wine/%{winepedir}/winoldap.mod16
%{_libdir}/wine/%{winepedir}/winsock.dll16
%{_libdir}/wine/%{winepedir}/wintab.dll16
%{_libdir}/wine/%{winepedir}/wow32.dll
%endif

# ARM SOs
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/explorer.exe.so
%{_libdir}/wine/%{winesodir}/cabarc.exe.so
%{_libdir}/wine/%{winesodir}/control.exe.so
%{_libdir}/wine/%{winesodir}/cmd.exe.so
%{_libdir}/wine/%{winesodir}/dxdiag.exe.so
%{_libdir}/wine/%{winesodir}/notepad.exe.so
%{_libdir}/wine/%{winesodir}/plugplay.exe.so
%{_libdir}/wine/%{winesodir}/progman.exe.so
%{_libdir}/wine/%{winesodir}/taskmgr.exe.so
%{_libdir}/wine/%{winesodir}/winebrowser.exe.so
%{_libdir}/wine/%{winesodir}/winecfg.exe.so
%{_libdir}/wine/%{winesodir}/winedbg.exe.so
%{_libdir}/wine/%{winesodir}/winefile.exe.so
%{_libdir}/wine/%{winesodir}/winemenubuilder.exe.so
%{_libdir}/wine/%{winesodir}/winemine.exe.so
%{_libdir}/wine/%{winesodir}/winemsibuilder.exe.so
%{_libdir}/wine/%{winesodir}/winepath.exe.so
%{_libdir}/wine/%{winesodir}/winmgmt.exe.so
%{_libdir}/wine/%{winesodir}/winver.exe.so
%{_libdir}/wine/%{winesodir}/wordpad.exe.so
%{_libdir}/wine/%{winesodir}/write.exe.so
%{_libdir}/wine/%{winesodir}/wusa.exe.so
%{_libdir}/wine/%{winesodir}/attrib.exe.so
%{_libdir}/wine/%{winesodir}/arp.exe.so
%{_libdir}/wine/%{winesodir}/aspnet_regiis.exe.so
%{_libdir}/wine/%{winesodir}/cacls.exe.so
%{_libdir}/wine/%{winesodir}/conhost.exe.so
%{_libdir}/wine/%{winesodir}/cscript.exe.so
%{_libdir}/wine/%{winesodir}/dism.exe.so
%{_libdir}/wine/%{winesodir}/dllhost.exe.so
%{_libdir}/wine/%{winesodir}/dplaysvr.exe.so
%{_libdir}/wine/%{winesodir}/dpnsvr.exe.so
%{_libdir}/wine/%{winesodir}/dpvsetup.exe.so
%{_libdir}/wine/%{winesodir}/eject.exe.so
%{_libdir}/wine/%{winesodir}/expand.exe.so
%{_libdir}/wine/%{winesodir}/extrac32.exe.so
%{_libdir}/wine/%{winesodir}/fc.exe.so
%{_libdir}/wine/%{winesodir}/find.exe.so
%{_libdir}/wine/%{winesodir}/findstr.exe.so
%{_libdir}/wine/%{winesodir}/fsutil.exe.so
%{_libdir}/wine/%{winesodir}/hostname.exe.so
%{_libdir}/wine/%{winesodir}/ipconfig.exe.so
%{_libdir}/wine/%{winesodir}/klist.exe.so
%{_libdir}/wine/%{winesodir}/winhlp32.exe.so
%{_libdir}/wine/%{winesodir}/mshta.exe.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/msidb.exe.so
%endif
%{_libdir}/wine/%{winesodir}/msiexec.exe.so
%{_libdir}/wine/%{winesodir}/net.exe.so
%{_libdir}/wine/%{winesodir}/netstat.exe.so
%{_libdir}/wine/%{winesodir}/ngen.exe.so
%{_libdir}/wine/%{winesodir}/ntoskrnl.exe.so
%{_libdir}/wine/%{winesodir}/oleview.exe.so
%{_libdir}/wine/%{winesodir}/ping.exe.so
%{_libdir}/wine/%{winesodir}/pnputil.exe.so
%{_libdir}/wine/%{winesodir}/powershell.exe.so
%{_libdir}/wine/%{winesodir}/reg.exe.so
%{_libdir}/wine/%{winesodir}/regasm.exe.so
%{_libdir}/wine/%{winesodir}/regedit.exe.so
%{_libdir}/wine/%{winesodir}/regsvcs.exe.so
%{_libdir}/wine/%{winesodir}/regsvr32.exe.so
%{_libdir}/wine/%{winesodir}/rpcss.exe.so
%{_libdir}/wine/%{winesodir}/rundll32.exe.so
%{_libdir}/wine/%{winesodir}/schtasks.exe.so
%{_libdir}/wine/%{winesodir}/sdbinst.exe.so
%{_libdir}/wine/%{winesodir}/secedit.exe.so
%{_libdir}/wine/%{winesodir}/servicemodelreg.exe.so
%{_libdir}/wine/%{winesodir}/services.exe.so
%{_libdir}/wine/%{winesodir}/start.exe.so
%{_libdir}/wine/%{winesodir}/tasklist.exe.so
%{_libdir}/wine/%{winesodir}/termsv.exe.so
%{_libdir}/wine/%{winesodir}/view.exe.so
%{_libdir}/wine/%{winesodir}/wevtutil.exe.so
%{_libdir}/wine/%{winesodir}/where.exe.so
%{_libdir}/wine/%{winesodir}/whoami.exe.so
%{_libdir}/wine/%{winesodir}/wineboot.exe.so
%{_libdir}/wine/%{winesodir}/wineconsole.exe.so
%{_libdir}/wine/%{winesodir}/winedevice.exe.so
%{_libdir}/wine/%{winesodir}/wmplayer.exe.so
%{_libdir}/wine/%{winesodir}/wscript.exe.so
%{_libdir}/wine/%{winesodir}/uninstaller.exe.so
%{_libdir}/wine/%{winesodir}/acledit.dll.so
%{_libdir}/wine/%{winesodir}/aclui.dll.so
%{_libdir}/wine/%{winesodir}/activeds.dll.so
%{_libdir}/wine/%{winesodir}/actxprxy.dll.so
%{_libdir}/wine/%{winesodir}/adsldp.dll.so
%{_libdir}/wine/%{winesodir}/adsldpc.dll.so
%{_libdir}/wine/%{winesodir}/advapi32.dll.so
%{_libdir}/wine/%{winesodir}/advpack.dll.so
%{_libdir}/wine/%{winesodir}/amsi.dll.so
%{_libdir}/wine/%{winesodir}/amstream.dll.so
%{_libdir}/wine/%{winesodir}/apphelp.dll.so
%{_libdir}/wine/%{winesodir}/appwiz.cpl.so
%{_libdir}/wine/%{winesodir}/appxdeploymentclient.dll.so
%{_libdir}/wine/%{winesodir}/atl.dll.so
%{_libdir}/wine/%{winesodir}/atl80.dll.so
%{_libdir}/wine/%{winesodir}/atl90.dll.so
%{_libdir}/wine/%{winesodir}/atl100.dll.so
%{_libdir}/wine/%{winesodir}/atl110.dll.so
%{_libdir}/wine/%{winesodir}/atlthunk.dll.so
%{_libdir}/wine/%{winesodir}/atmlib.dll.so
%{_libdir}/wine/%{winesodir}/authz.dll.so
%{_libdir}/wine/%{winesodir}/avicap32.dll.so
%{_libdir}/wine/%{winesodir}/avifil32.dll.so
%{_libdir}/wine/%{winesodir}/avrt.dll.so
%{_libdir}/wine/%{winesodir}/bcrypt.dll.so
%{_libdir}/wine/%{winesodir}/bcryptprimitives.dll.so
%{_libdir}/wine/%{winesodir}/bluetoothapis.dll.so
%{_libdir}/wine/%{winesodir}/browseui.dll.so
%{_libdir}/wine/%{winesodir}/bthprops.cpl.so
%{_libdir}/wine/%{winesodir}/cabinet.dll.so
%{_libdir}/wine/%{winesodir}/cards.dll.so
%{_libdir}/wine/%{winesodir}/cdosys.dll.so
%{_libdir}/wine/%{winesodir}/cfgmgr32.dll.so
%{_libdir}/wine/%{winesodir}/chcp.com.so
%{_libdir}/wine/%{winesodir}/clock.exe.so
%{_libdir}/wine/%{winesodir}/clusapi.dll.so
%{_libdir}/wine/%{winesodir}/cng.sys.so
%{_libdir}/wine/%{winesodir}/combase.dll.so
%{_libdir}/wine/%{winesodir}/comcat.dll.so
%{_libdir}/wine/%{winesodir}/comctl32.dll.so
%{_libdir}/wine/%{winesodir}/comdlg32.dll.so
%{_libdir}/wine/%{winesodir}/compstui.dll.so
%{_libdir}/wine/%{winesodir}/comsvcs.dll.so
%{_libdir}/wine/%{winesodir}/concrt140.dll.so
%{_libdir}/wine/%{winesodir}/connect.dll.so
%{_libdir}/wine/%{winesodir}/credui.dll.so
%{_libdir}/wine/%{winesodir}/crtdll.dll.so
%{_libdir}/wine/%{winesodir}/crypt32.dll.so
%{_libdir}/wine/%{winesodir}/cryptdlg.dll.so
%{_libdir}/wine/%{winesodir}/cryptdll.dll.so
%{_libdir}/wine/%{winesodir}/cryptext.dll.so
%{_libdir}/wine/%{winesodir}/cryptnet.dll.so
%{_libdir}/wine/%{winesodir}/cryptowinrt.dll.so
%{_libdir}/wine/%{winesodir}/cryptsp.dll.so
%{_libdir}/wine/%{winesodir}/cryptui.dll.so
%{_libdir}/wine/%{winesodir}/ctapi32.dll.so
%{_libdir}/wine/%{winesodir}/ctl3d32.dll.so
%{_libdir}/wine/%{winesodir}/d2d1.dll.so
%{_libdir}/wine/%{winesodir}/d3d10.dll.so
%{_libdir}/wine/%{winesodir}/d3d10_1.dll.so
%{_libdir}/wine/%{winesodir}/d3d10core.dll.so
%{_libdir}/wine/%{winesodir}/d3d11.dll.so
%{_libdir}/wine/%{winesodir}/d3d12.dll.so
%{_libdir}/wine/%{winesodir}/d3d12core.dll.so
%{_libdir}/wine/%{winesodir}/d3dcompiler_*.dll.so
%{_libdir}/wine/%{winesodir}/d3dim.dll.so
%{_libdir}/wine/%{winesodir}/d3dim700.dll.so
%{_libdir}/wine/%{winesodir}/d3drm.dll.so
%{_libdir}/wine/%{winesodir}/d3dx9_*.dll.so
%{_libdir}/wine/%{winesodir}/d3dx10_*.dll.so
%{_libdir}/wine/%{winesodir}/d3dx11_42.dll.so
%{_libdir}/wine/%{winesodir}/d3dx11_43.dll.so
%{_libdir}/wine/%{winesodir}/d3dxof.dll.so
%{_libdir}/wine/%{winesodir}/davclnt.dll.so
%{_libdir}/wine/%{winesodir}/dbgeng.dll.so
%{_libdir}/wine/%{winesodir}/dbghelp.dll.so
%{_libdir}/wine/%{winesodir}/dciman32.dll.so
%{_libdir}/wine/%{winesodir}/dcomp.dll.so
%{_libdir}/wine/%{winesodir}/ddraw.dll.so
%{_libdir}/wine/%{winesodir}/ddrawex.dll.so
%{_libdir}/wine/%{winesodir}/devenum.dll.so
%{_libdir}/wine/%{winesodir}/dhcpcsvc.dll.so
%{_libdir}/wine/%{winesodir}/dhcpcsvc6.dll.so
%{_libdir}/wine/%{winesodir}/dhtmled.ocx.so
%{_libdir}/wine/%{winesodir}/diasymreader.dll.so
%{_libdir}/wine/%{winesodir}/difxapi.dll.so
%{_libdir}/wine/%{winesodir}/dinput.dll.so
%{_libdir}/wine/%{winesodir}/dinput8.dll.so
%{_libdir}/wine/%{winesodir}/directmanipulation.dll.so
%{_libdir}/wine/%{winesodir}/dispex.dll.so
%{_libdir}/wine/%{winesodir}/dmband.dll.so
%{_libdir}/wine/%{winesodir}/dmcompos.dll.so
%{_libdir}/wine/%{winesodir}/dmime.dll.so
%{_libdir}/wine/%{winesodir}/dmloader.dll.so
%{_libdir}/wine/%{winesodir}/dmscript.dll.so
%{_libdir}/wine/%{winesodir}/dmstyle.dll.so
%{_libdir}/wine/%{winesodir}/dmsynth.dll.so
%{_libdir}/wine/%{winesodir}/dmusic.dll.so
%{_libdir}/wine/%{winesodir}/dmusic32.dll.so
%{_libdir}/wine/%{winesodir}/dplay.dll.so
%{_libdir}/wine/%{winesodir}/dplayx.dll.so
%{_libdir}/wine/%{winesodir}/dpnaddr.dll.so
%{_libdir}/wine/%{winesodir}/dpnet.dll.so
%{_libdir}/wine/%{winesodir}/dpnhpast.dll.so
%{_libdir}/wine/%{winesodir}/dpnhupnp.dll.so
%{_libdir}/wine/%{winesodir}/dpnlobby.dll.so
%{_libdir}/wine/%{winesodir}/dpvoice.dll.so
%{_libdir}/wine/%{winesodir}/dpwsockx.dll.so
%{_libdir}/wine/%{winesodir}/drmclien.dll.so
%{_libdir}/wine/%{winesodir}/dsound.dll.so
%{_libdir}/wine/%{winesodir}/dsdmo.dll.so
%{_libdir}/wine/%{winesodir}/dsquery.dll.so
%{_libdir}/wine/%{winesodir}/dssenh.dll.so
%{_libdir}/wine/%{winesodir}/dsuiext.dll.so
%{_libdir}/wine/%{winesodir}/dswave.dll.so
%{_libdir}/wine/%{winesodir}/dwmapi.dll.so
%{_libdir}/wine/%{winesodir}/dwrite.dll.so
%{_libdir}/wine/%{winesodir}/dx8vb.dll.so
%{_libdir}/wine/%{winesodir}/dxcore.dll.so
%{_libdir}/wine/%{winesodir}/dxdiagn.dll.so
%ghost %{_libdir}/wine/%{winesodir}/dxgi.dll.so
%{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
%{_libdir}/wine/%{winesodir}/dxgkrnl.sys.so
%{_libdir}/wine/%{winesodir}/dxgmms1.sys.so
%{_libdir}/wine/%{winesodir}/dxtrans.dll.so
%{_libdir}/wine/%{winesodir}/dxva2.dll.so
%{_libdir}/wine/%{winesodir}/esent.dll.so
%{_libdir}/wine/%{winesodir}/evr.dll.so
%{_libdir}/wine/%{winesodir}/explorerframe.dll.so
%{_libdir}/wine/%{winesodir}/faultrep.dll.so
%{_libdir}/wine/%{winesodir}/feclient.dll.so
%{_libdir}/wine/%{winesodir}/fltlib.dll.so
%{_libdir}/wine/%{winesodir}/fltmgr.sys.so
%{_libdir}/wine/%{winesodir}/fntcache.dll.so
%{_libdir}/wine/%{winesodir}/fontsub.dll.so
%{_libdir}/wine/%{winesodir}/fusion.dll.so
%{_libdir}/wine/%{winesodir}/fwpuclnt.dll.so
%{_libdir}/wine/%{winesodir}/gameux.dll.so
%{_libdir}/wine/%{winesodir}/gamingtcui.dll.so
%{_libdir}/wine/%{winesodir}/gdi32.dll.so
%{_libdir}/wine/%{winesodir}/gdiplus.dll.so
%{_libdir}/wine/%{winesodir}/geolocation.dll.so
%{_libdir}/wine/%{winesodir}/glu32.dll.so
%{_libdir}/wine/%{winesodir}/gphoto2.ds.so
%{_libdir}/wine/%{winesodir}/gpkcsp.dll.so
%{_libdir}/wine/%{winesodir}/graphicscapture.dll.so
%{_libdir}/wine/%{winesodir}/hal.dll.so
%{_libdir}/wine/%{winesodir}/hh.exe.so
%{_libdir}/wine/%{winesodir}/hhctrl.ocx.so
%{_libdir}/wine/%{winesodir}/hid.dll.so
%{_libdir}/wine/%{winesodir}/hidclass.sys.so
%{_libdir}/wine/%{winesodir}/hidparse.sys.so
%{_libdir}/wine/%{winesodir}/hlink.dll.so
%{_libdir}/wine/%{winesodir}/hnetcfg.dll.so
%{_libdir}/wine/%{winesodir}/hrtfapo.dll.so
%{_libdir}/wine/%{winesodir}/http.sys.so
%{_libdir}/wine/%{winesodir}/httpapi.dll.so
%{_libdir}/wine/%{winesodir}/hvsimanagementapi.dll.so
%{_libdir}/wine/%{winesodir}/ia2comproxy.dll.so
%{_libdir}/wine/%{winesodir}/icacls.exe.so
%{_libdir}/wine/%{winesodir}/iccvid.dll.so
%{_libdir}/wine/%{winesodir}/icinfo.exe.so
%{_libdir}/wine/%{winesodir}/ieframe.dll.so
%{_libdir}/wine/%{winesodir}/ieproxy.dll.so
%{_libdir}/wine/%{winesodir}/imaadp32.acm.so
%{_libdir}/wine/%{winesodir}/imagehlp.dll.so
%{_libdir}/wine/%{winesodir}/imm32.dll.so
%{_libdir}/wine/%{winesodir}/inetcomm.dll.so
%{_libdir}/wine/%{winesodir}/inetcpl.cpl.so
%{_libdir}/wine/%{winesodir}/inetmib1.dll.so
%{_libdir}/wine/%{winesodir}/infosoft.dll.so
%{_libdir}/wine/%{winesodir}/initpki.dll.so
%{_libdir}/wine/%{winesodir}/inkobj.dll.so
%{_libdir}/wine/%{winesodir}/inseng.dll.so
%{_libdir}/wine/%{winesodir}/iphlpapi.dll.so
%{_libdir}/wine/%{winesodir}/iprop.dll.so
%{_libdir}/wine/%{winesodir}/irprops.cpl.so
%{_libdir}/wine/%{winesodir}/ir50_32.dll.so
%{_libdir}/wine/%{winesodir}/itircl.dll.so
%{_libdir}/wine/%{winesodir}/itss.dll.so
%{_libdir}/wine/%{winesodir}/joy.cpl.so
%{_libdir}/wine/%{winesodir}/jscript.dll.so
%{_libdir}/wine/%{winesodir}/jsproxy.dll.so
%{_libdir}/wine/%{winesodir}/kerberos.dll.so
%{_libdir}/wine/%{winesodir}/kernel32.dll.so
%{_libdir}/wine/%{winesodir}/kernelbase.dll.so
%{_libdir}/wine/%{winesodir}/ksecdd.sys.so
%{_libdir}/wine/%{winesodir}/ksproxy.ax.so
%{_libdir}/wine/%{winesodir}/ksuser.dll.so
%{_libdir}/wine/%{winesodir}/ktmw32.dll.so
%{_libdir}/wine/%{winesodir}/l3codeca.acm.so
%{_libdir}/wine/%{winesodir}/loadperf.dll.so
%{_libdir}/wine/%{winesodir}/localspl.dll.so
%{_libdir}/wine/%{winesodir}/localui.dll.so
%{_libdir}/wine/%{winesodir}/lodctr.exe.so
%{_libdir}/wine/%{winesodir}/magnification.dll.so
%{_libdir}/wine/%{winesodir}/mapi32.dll.so
%{_libdir}/wine/%{winesodir}/mapistub.dll.so
%{_libdir}/wine/%{winesodir}/mciavi32.dll.so
%{_libdir}/wine/%{winesodir}/mcicda.dll.so
%{_libdir}/wine/%{winesodir}/mciqtz32.dll.so
%{_libdir}/wine/%{winesodir}/mciseq.dll.so
%{_libdir}/wine/%{winesodir}/mciwave.dll.so
%{_libdir}/wine/%{winesodir}/mf.dll.so
%{_libdir}/wine/%{winesodir}/mf3216.dll.so
%{_libdir}/wine/%{winesodir}/mfmediaengine.dll.so
%{_libdir}/wine/%{winesodir}/mfplat.dll.so
%{_libdir}/wine/%{winesodir}/mfplay.dll.so
%{_libdir}/wine/%{winesodir}/mfreadwrite.dll.so
%{_libdir}/wine/%{winesodir}/mfsrcsnk.dll.so
%{_libdir}/wine/%{winesodir}/mgmtapi.dll.so
%{_libdir}/wine/%{winesodir}/midimap.dll.so
%{_libdir}/wine/%{winesodir}/mlang.dll.so
%{_libdir}/wine/%{winesodir}/mmcndmgr.dll.so
%{_libdir}/wine/%{winesodir}/mmdevapi.dll.so
%{_libdir}/wine/%{winesodir}/mofcomp.exe.so
%{_libdir}/wine/%{winesodir}/mountmgr.sys.so
%{_libdir}/wine/%{winesodir}/mp3dmod.dll.so
%{_libdir}/wine/%{winesodir}/mpr.dll.so
%{_libdir}/wine/%{winesodir}/mprapi.dll.so
%{_libdir}/wine/%{winesodir}/msacm32.dll.so
%{_libdir}/wine/%{winesodir}/msacm32.drv.so
%{_libdir}/wine/%{winesodir}/msado15.dll.so
%{_libdir}/wine/%{winesodir}/msadp32.acm.so
%{_libdir}/wine/%{winesodir}/msasn1.dll.so
%{_libdir}/wine/%{winesodir}/msauddecmft.dll.so
%{_libdir}/wine/%{winesodir}/mscat32.dll.so
%{_libdir}/wine/%{winesodir}/mscoree.dll.so
%{_libdir}/wine/%{winesodir}/mscorwks.dll.so
%{_libdir}/wine/%{winesodir}/msctf.dll.so
%{_libdir}/wine/%{winesodir}/msctfmonitor.dll.so
%{_libdir}/wine/%{winesodir}/msctfp.dll.so
%{_libdir}/wine/%{winesodir}/msdaps.dll.so
%{_libdir}/wine/%{winesodir}/msdasql.dll.so
%{_libdir}/wine/%{winesodir}/msdelta.dll.so
%{_libdir}/wine/%{winesodir}/msdmo.dll.so
%{_libdir}/wine/%{winesodir}/msdrm.dll.so
%{_libdir}/wine/%{winesodir}/msftedit.dll.so
%{_libdir}/wine/%{winesodir}/msg711.acm.so
%{_libdir}/wine/%{winesodir}/mshtml.dll.so
%{_libdir}/wine/%{winesodir}/msgsm32.acm.so
%{_libdir}/wine/%{winesodir}/msi.dll.so
%{_libdir}/wine/%{winesodir}/msident.dll.so
%{_libdir}/wine/%{winesodir}/msimtf.dll.so
%{_libdir}/wine/%{winesodir}/msimg32.dll.so
%{_libdir}/wine/%{winesodir}/msinfo32.exe.so
%{_libdir}/wine/%{winesodir}/msisip.dll.so
%{_libdir}/wine/%{winesodir}/msisys.ocx.so
%{_libdir}/wine/%{winesodir}/msls31.dll.so
%{_libdir}/wine/%{winesodir}/msmpeg2vdec.dll.so
%{_libdir}/wine/%{winesodir}/msnet32.dll.so
%{_libdir}/wine/%{winesodir}/mspatcha.dll.so
%{_libdir}/wine/%{winesodir}/msports.dll.so
%{_libdir}/wine/%{winesodir}/msscript.ocx.so
%{_libdir}/wine/%{winesodir}/mssign32.dll.so
%{_libdir}/wine/%{winesodir}/mssip32.dll.so
%{_libdir}/wine/%{winesodir}/msrle32.dll.so
%{_libdir}/wine/%{winesodir}/mstask.dll.so
%{_libdir}/wine/%{winesodir}/msv1_0.dll.so
%{_libdir}/wine/%{winesodir}/msvcirt.dll.so
%{_libdir}/wine/%{winesodir}/msvcm80.dll.so
%{_libdir}/wine/%{winesodir}/msvcm90.dll.so
%{_libdir}/wine/%{winesodir}/msvcp_win.dll.so
%{_libdir}/wine/%{winesodir}/msvcp60.dll.so
%{_libdir}/wine/%{winesodir}/msvcp70.dll.so
%{_libdir}/wine/%{winesodir}/msvcp71.dll.so
%{_libdir}/wine/%{winesodir}/msvcp80.dll.so
%{_libdir}/wine/%{winesodir}/msvcp90.dll.so
%{_libdir}/wine/%{winesodir}/msvcp100.dll.so
%{_libdir}/wine/%{winesodir}/msvcp110.dll.so
%{_libdir}/wine/%{winesodir}/msvcp120.dll.so
%{_libdir}/wine/%{winesodir}/msvcp120_app.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140_1.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140_2.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140_atomic_wait.dll.so
%{_libdir}/wine/%{winesodir}/msvcp140_codecvt_ids.dll.so
%{_libdir}/wine/%{winesodir}/msvcr70.dll.so
%{_libdir}/wine/%{winesodir}/msvcr71.dll.so
%{_libdir}/wine/%{winesodir}/msvcr80.dll.so
%{_libdir}/wine/%{winesodir}/msvcr90.dll.so
%{_libdir}/wine/%{winesodir}/msvcr100.dll.so
%{_libdir}/wine/%{winesodir}/msvcr110.dll.so
%{_libdir}/wine/%{winesodir}/msvcr120.dll.so
%{_libdir}/wine/%{winesodir}/msvcr120_app.dll.so
%{_libdir}/wine/%{winesodir}/msvcrt.dll.so
%{_libdir}/wine/%{winesodir}/msvcrt20.dll.so
%{_libdir}/wine/%{winesodir}/msvcrt40.dll.so
%{_libdir}/wine/%{winesodir}/msvcrtd.dll.so
%{_libdir}/wine/%{winesodir}/msvfw32.dll.so
%{_libdir}/wine/%{winesodir}/msvidc32.dll.so
%{_libdir}/wine/%{winesodir}/mswsock.dll.so
%{_libdir}/wine/%{winesodir}/msxml.dll.so
%{_libdir}/wine/%{winesodir}/msxml2.dll.so
%{_libdir}/wine/%{winesodir}/msxml3.dll.so
%{_libdir}/wine/%{winesodir}/msxml4.dll.so
%{_libdir}/wine/%{winesodir}/msxml6.dll.so
%{_libdir}/wine/%{winesodir}/mtxdm.dll.so
%{_libdir}/wine/%{winesodir}/nddeapi.dll.so
%{_libdir}/wine/%{winesodir}/ncrypt.dll.so
%{_libdir}/wine/%{winesodir}/ndis.sys.so
%{_libdir}/wine/%{winesodir}/netapi32.dll.so
%{_libdir}/wine/%{winesodir}/netcfgx.dll.so
%{_libdir}/wine/%{winesodir}/netio.sys.so
%{_libdir}/wine/%{winesodir}/netprofm.dll.so
%{_libdir}/wine/%{winesodir}/netsh.exe.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/netutils.dll.so
%endif
%{_libdir}/wine/%{winesodir}/newdev.dll.so
%{_libdir}/wine/%{winesodir}/ninput.dll.so
%{_libdir}/wine/%{winesodir}/npmshtml.dll.so
%{_libdir}/wine/%{winesodir}/npptools.dll.so
%{_libdir}/wine/%{winesodir}/nsi.dll.so
%{_libdir}/wine/%{winesodir}/nsiproxy.sys.so
%{_libdir}/wine/%{winesodir}/ntdll.dll.so
%{_libdir}/wine/%{winesodir}/ntdsapi.dll.so
%{_libdir}/wine/%{winesodir}/ntprint.dll.so
%{_libdir}/wine/%{winesodir}/objsel.dll.so
%{_libdir}/wine/%{winesodir}/odbc32.dll.so
%{_libdir}/wine/%{winesodir}/odbcbcp.dll.so
%{_libdir}/wine/%{winesodir}/odbccp32.dll.so
%{_libdir}/wine/%{winesodir}/odbccu32.dll.so
%{_libdir}/wine/%{winesodir}/ole32.dll.so
%{_libdir}/wine/%{winesodir}/oleacc.dll.so
%{_libdir}/wine/%{winesodir}/oleaut32.dll.so
%{_libdir}/wine/%{winesodir}/olecli32.dll.so
%{_libdir}/wine/%{winesodir}/oledb32.dll.so
%{_libdir}/wine/%{winesodir}/oledlg.dll.so
%{_libdir}/wine/%{winesodir}/olepro32.dll.so
%{_libdir}/wine/%{winesodir}/olesvr32.dll.so
%{_libdir}/wine/%{winesodir}/olethk32.dll.so
%{_libdir}/wine/%{winesodir}/opcservices.dll.so
%{_libdir}/wine/%{winesodir}/opengl32.dll.so
%{_libdir}/wine/%{winesodir}/packager.dll.so
%{_libdir}/wine/%{winesodir}/pdh.dll.so
%{_libdir}/wine/%{winesodir}/photometadatahandler.dll.so
%{_libdir}/wine/%{winesodir}/pidgen.dll.so
%{_libdir}/wine/%{winesodir}/powrprof.dll.so
%{_libdir}/wine/%{winesodir}/presentationfontcache.exe.so
%{_libdir}/wine/%{winesodir}/printui.dll.so
%{_libdir}/wine/%{winesodir}/prntvpt.dll.so
%{_libdir}/wine/%{winesodir}/propsys.dll.so
%{_libdir}/wine/%{winesodir}/psapi.dll.so
%{_libdir}/wine/%{winesodir}/pstorec.dll.so
%{_libdir}/wine/%{winesodir}/pwrshplugin.dll.so
%{_libdir}/wine/%{winesodir}/qasf.dll.so
%{_libdir}/wine/%{winesodir}/qcap.dll.so
%{_libdir}/wine/%{winesodir}/qdvd.dll.so
%{_libdir}/wine/%{winesodir}/qedit.dll.so
%{_libdir}/wine/%{winesodir}/qmgr.dll.so
%{_libdir}/wine/%{winesodir}/qmgrprxy.dll.so
%{_libdir}/wine/%{winesodir}/quartz.dll.so
%{_libdir}/wine/%{winesodir}/query.dll.so
%{_libdir}/wine/%{winesodir}/qwave.dll.so
%{_libdir}/wine/%{winesodir}/rasapi32.dll.so
%{_libdir}/wine/%{winesodir}/rasdlg.dll.so
%{_libdir}/wine/%{winesodir}/regapi.dll.so
%{_libdir}/wine/%{winesodir}/regini.exe.so
%{_libdir}/wine/%{winesodir}/resutils.dll.so
%{_libdir}/wine/%{winesodir}/riched20.dll.so
%{_libdir}/wine/%{winesodir}/riched32.dll.so
%{_libdir}/wine/%{winesodir}/robocopy.exe.so
%{_libdir}/wine/%{winesodir}/rpcrt4.dll.so
%{_libdir}/wine/%{winesodir}/rsabase.dll.so
%{_libdir}/wine/%{winesodir}/rsaenh.dll.so
%{_libdir}/wine/%{winesodir}/rstrtmgr.dll.so
%{_libdir}/wine/%{winesodir}/rtutils.dll.so
%{_libdir}/wine/%{winesodir}/rtworkq.dll.so
%{_libdir}/wine/%{winesodir}/samlib.dll.so
%{_libdir}/wine/%{winesodir}/sapi.dll.so
%{_libdir}/wine/%{winesodir}/sas.dll.so
%{_libdir}/wine/%{winesodir}/sc.exe.so
%{_libdir}/wine/%{winesodir}/scarddlg.dll.so
%{_libdir}/wine/%{winesodir}/scardsvr.dll.so
%{_libdir}/wine/%{winesodir}/sccbase.dll.so
%{_libdir}/wine/%{winesodir}/schannel.dll.so
%{_libdir}/wine/%{winesodir}/scrobj.dll.so
%{_libdir}/wine/%{winesodir}/scrrun.dll.so
%{_libdir}/wine/%{winesodir}/scsiport.sys.so
%{_libdir}/wine/%{winesodir}/sechost.dll.so
%{_libdir}/wine/%{winesodir}/secur32.dll.so
%{_libdir}/wine/%{winesodir}/sensapi.dll.so
%{_libdir}/wine/%{winesodir}/serialui.dll.so
%{_libdir}/wine/%{winesodir}/setupapi.dll.so
%{_libdir}/wine/%{winesodir}/sfc_os.dll.so
%{_libdir}/wine/%{winesodir}/shcore.dll.so
%{_libdir}/wine/%{winesodir}/shdocvw.dll.so
%{_libdir}/wine/%{winesodir}/schedsvc.dll.so
%{_libdir}/wine/%{winesodir}/shell32.dll.so
%{_libdir}/wine/%{winesodir}/shfolder.dll.so
%{_libdir}/wine/%{winesodir}/shlwapi.dll.so
%{_libdir}/wine/%{winesodir}/shutdown.exe.so
%{_libdir}/wine/%{winesodir}/slbcsp.dll.so
%{_libdir}/wine/%{winesodir}/slc.dll.so
%{_libdir}/wine/%{winesodir}/snmpapi.dll.so
%{_libdir}/wine/%{winesodir}/softpub.dll.so
%{_libdir}/wine/%{winesodir}/spoolsv.exe.so
%{_libdir}/wine/%{winesodir}/sppc.dll.so
%{_libdir}/wine/%{winesodir}/srclient.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/srvcli.dll.so
%endif
%{_libdir}/wine/%{winesodir}/srvsvc.dll.so
%{_libdir}/wine/%{winesodir}/sspicli.dll.so
%{_libdir}/wine/%{winesodir}/sti.dll.so
%{_libdir}/wine/%{winesodir}/strmdll.dll.so
%{_libdir}/wine/%{winesodir}/subst.exe.so
%{_libdir}/wine/%{winesodir}/svchost.exe.so
%{_libdir}/wine/%{winesodir}/svrapi.dll.so
%{_libdir}/wine/%{winesodir}/sxs.dll.so
%{_libdir}/wine/%{winesodir}/systeminfo.exe.so
%{_libdir}/wine/%{winesodir}/t2embed.dll.so
%{_libdir}/wine/%{winesodir}/tapi32.dll.so
%{_libdir}/wine/%{winesodir}/taskkill.exe.so
%{_libdir}/wine/%{winesodir}/taskschd.dll.so
%{_libdir}/wine/%{winesodir}/tbs.dll.so
%{_libdir}/wine/%{winesodir}/tdh.dll.so
%{_libdir}/wine/%{winesodir}/tdi.sys.so
%{_libdir}/wine/%{winesodir}/threadpoolwinrt.dll.so
%{_libdir}/wine/%{winesodir}/traffic.dll.so
%{_libdir}/wine/%{winesodir}/twinapi.appcore.dll.so
%{_libdir}/wine/%{winesodir}/ucrtbase.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/uianimation.dll.so
%endif
%{_libdir}/wine/%{winesodir}/uiautomationcore.dll.so
%{_libdir}/wine/%{winesodir}/uiribbon.dll.so
%{_libdir}/wine/%{winesodir}/unicows.dll.so
%{_libdir}/wine/%{winesodir}/unlodctr.exe.so
%{_libdir}/wine/%{winesodir}/updspapi.dll.so
%{_libdir}/wine/%{winesodir}/url.dll.so
%{_libdir}/wine/%{winesodir}/urlmon.dll.so
%{_libdir}/wine/%{winesodir}/usbd.sys.so
%{_libdir}/wine/%{winesodir}/user32.dll.so
%{_libdir}/wine/%{winesodir}/utildll.dll.so
%{_libdir}/wine/%{winesodir}/uxtheme.dll.so
%{_libdir}/wine/%{winesodir}/userenv.dll.so
%{_libdir}/wine/%{winesodir}/vbscript.dll.so
%{_libdir}/wine/%{winesodir}/vcomp.dll.so
%{_libdir}/wine/%{winesodir}/vcomp90.dll.so
%{_libdir}/wine/%{winesodir}/vcomp100.dll.so
%{_libdir}/wine/%{winesodir}/vcomp110.dll.so
%{_libdir}/wine/%{winesodir}/vcomp120.dll.so
%{_libdir}/wine/%{winesodir}/vcomp140.dll.so
%{_libdir}/wine/%{winesodir}/vcruntime140.dll.so
%{_libdir}/wine/%{winesodir}/vcruntime140_1.dll.so
%{_libdir}/wine/%{winesodir}/vdmdbg.dll.so
%{_libdir}/wine/%{winesodir}/version.dll.so
%{_libdir}/wine/%{winesodir}/vga.dll.so
%{_libdir}/wine/%{winesodir}/virtdisk.dll.so
%{_libdir}/wine/%{winesodir}/vssapi.dll.so
%{_libdir}/wine/%{winesodir}/vulkan-1.dll.so
%{_libdir}/wine/%{winesodir}/wbemdisp.dll.so
%{_libdir}/wine/%{winesodir}/wbemprox.dll.so
%{_libdir}/wine/%{winesodir}/wdscore.dll.so
%{_libdir}/wine/%{winesodir}/webservices.dll.so
%{_libdir}/wine/%{winesodir}/websocket.dll.so
%{_libdir}/wine/%{winesodir}/wer.dll.so
%{_libdir}/wine/%{winesodir}/wevtapi.dll.so
%{_libdir}/wine/%{winesodir}/wevtsvc.dll.so
%{_libdir}/wine/%{winesodir}/wiaservc.dll.so
%{_libdir}/wine/%{winesodir}/wimgapi.dll.so
%{_libdir}/wine/%{winesodir}/win32k.sys.so
%{_libdir}/wine/%{winesodir}/win32u.dll.so
%{_libdir}/wine/%{winesodir}/windows.applicationmodel.dll.so
%{_libdir}/wine/%{winesodir}/windows.devices.bluetooth.dll.so
%{_libdir}/wine/%{winesodir}/windows.devices.enumeration.dll.so
%{_libdir}/wine/%{winesodir}/windows.devices.usb.dll.so
%{_libdir}/wine/%{winesodir}/windows.gaming.ui.gamebar.dll.so
%{_libdir}/wine/%{winesodir}/windows.gaming.input.dll.so
%{_libdir}/wine/%{winesodir}/windows.globalization.dll.so
%{_libdir}/wine/%{winesodir}/windows.media.dll.so
%{_libdir}/wine/%{winesodir}/windows.media.devices.dll.so
%{_libdir}/wine/%{winesodir}/windows.media.media.mediacontrol.dll.so
%{_libdir}/wine/%{winesodir}/windows.media.speech.dll.so
%{_libdir}/wine/%{winesodir}/windows.networking.connectivity.so
%{_libdir}/wine/%{winesodir}/windows.networking.dll.so
%{_libdir}/wine/%{winesodir}/windows.networking.hostname.dll.so
%{_libdir}/wine/%{winesodir}/windows.perception.stub.dll.so
%{_libdir}/wine/%{winesodir}/windows.security.credentials.ui.userconsentverifier.dll.so
%{_libdir}/wine/%{winesodir}/windows.storage.applicationdata.dll.so
%{_libdir}/wine/%{winesodir}/windows.system.profile.systemmanufacturers.dll.so
%{_libdir}/wine/%{winesodir}/windows.ui.so
%{_libdir}/wine/%{winesodir}/windowscodecs.dll.so
%{_libdir}/wine/%{winesodir}/windowscodecsext.dll.so
%{_libdir}/wine/%{winesodir}/winebus.sys.so
%{_libdir}/wine/%{winesodir}/wined3d.dll.so
%{_libdir}/wine/%{winesodir}/winegstreamer.dll.so
%{_libdir}/wine/%{winesodir}/winehid.sys.so
%{_libdir}/wine/%{winesodir}/winemapi.dll.so
%{_libdir}/wine/%{winesodir}/wineusb.sys.so
%{_libdir}/wine/%{winesodir}/winevulkan.dll.so
%{_libdir}/wine/%{winesodir}/winexinput.sys.so
%{_libdir}/wine/%{winesodir}/wing32.dll.so
%{_libdir}/wine/%{winesodir}/winhttp.dll.so
%{_libdir}/wine/%{winesodir}/wininet.dll.so
%{_libdir}/wine/%{winesodir}/winmm.dll.so
%{_libdir}/wine/%{winesodir}/winnls32.dll.so
%{_libdir}/wine/%{winesodir}/winprint.dll.so
%{_libdir}/wine/%{winesodir}/winspool.drv.so
%{_libdir}/wine/%{winesodir}/winsta.dll.so
%{_libdir}/wine/%{winesodir}/wldp.dll.so
%{_libdir}/wine/%{winesodir}/wmasf.dll.so
%{_libdir}/wine/%{winesodir}/wmic.exe.so
%{_libdir}/wine/%{winesodir}/wmiutils.dll.so
%{_libdir}/wine/%{winesodir}/wmp.dll.so
%{_libdir}/wine/%{winesodir}/wmvcore.dll.so
%{_libdir}/wine/%{winesodir}/spoolss.dll.so
%{_libdir}/wine/%{winesodir}/wintab32.dll.so
%{_libdir}/wine/%{winesodir}/wintrust.dll.so
%{_libdir}/wine/%{winesodir}/wintypes.dll.so
%{_libdir}/wine/%{winesodir}/winusb.dll.so
%{_libdir}/wine/%{winesodir}/wlanapi.dll.so
%{_libdir}/wine/%{winesodir}/wlanui.dll.so
%{_libdir}/wine/%{winesodir}/wmphoto.dll.so
%{_libdir}/wine/%{winesodir}/wnaspi32.dll.so
%{_libdir}/wine/%{winesodir}/wofutil.dll.so
%{_libdir}/wine/%{winesodir}/wpc.dll.so
%{_libdir}/wine/%{winesodir}/wpcap.dll.so
%{_libdir}/wine/%{winesodir}/ws2_32.dll.so
%{_libdir}/wine/%{winesodir}/wsdapi.dll.so
%{_libdir}/wine/%{winesodir}/wshom.ocx.so
%{_libdir}/wine/%{winesodir}/wsnmp32.dll.so
%{_libdir}/wine/%{winesodir}/wsock32.dll.so
%{_libdir}/wine/%{winesodir}/wtsapi32.dll.so
%{_libdir}/wine/%{winesodir}/wuapi.dll.so
%{_libdir}/wine/%{winesodir}/wuaueng.dll.so
%{_libdir}/wine/%{winesodir}/wineps.drv.so
%{_libdir}/wine/%{winesodir}/d3d8.dll.so
%{_libdir}/wine/%{winesodir}/d3d8thk.dll.so
%{_libdir}/wine/%{winesodir}/d3d9.dll.so
%{_libdir}/wine/%{winesodir}/dnsapi.dll.so
%{_libdir}/wine/%{winesodir}/iexplore.exe.so
%{_libdir}/wine/%{winesodir}/xcopy.exe.so
%{_libdir}/wine/%{winesodir}/x3daudio1_0.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_1.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_2.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_3.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_4.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_5.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_6.dll.so
%{_libdir}/wine/%{winesodir}/x3daudio1_7.dll.so
%{_libdir}/wine/%{winesodir}/xactengine2_0.dll.so
%{_libdir}/wine/%{winesodir}/xactengine2_4.dll.so
%{_libdir}/wine/%{winesodir}/xactengine2_7.dll.so
%{_libdir}/wine/%{winesodir}/xactengine2_9.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_0.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_1.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_2.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_3.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_4.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_5.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_6.dll.so
%{_libdir}/wine/%{winesodir}/xactengine3_7.dll.so
%{_libdir}/wine/%{winesodir}/xapofx1_1.dll.so
%{_libdir}/wine/%{winesodir}/xapofx1_2.dll.so
%{_libdir}/wine/%{winesodir}/xapofx1_3.dll.so
%{_libdir}/wine/%{winesodir}/xapofx1_4.dll.so
%{_libdir}/wine/%{winesodir}/xapofx1_5.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_0.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_1.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_2.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_3.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_4.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_5.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_6.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_7.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_8.dll.so
%{_libdir}/wine/%{winesodir}/xaudio2_9.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_1.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_2.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_3.dll.so
%{_libdir}/wine/%{winesodir}/xinput1_4.dll.so
%{_libdir}/wine/%{winesodir}/xinput9_1_0.dll.so
%{_libdir}/wine/%{winesodir}/xinputuap.dll.so
%{_libdir}/wine/%{winesodir}/xmllite.dll.so
%{_libdir}/wine/%{winesodir}/xolehlp.dll.so
%{_libdir}/wine/%{winesodir}/xpsprint.dll.so
%{_libdir}/wine/%{winesodir}/xpssvcs.dll.so
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/nls/

%files common
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*

%files fonts
# meta package

%if 0%{?wine_staging}
%files arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif
#0%%{?wine_staging}

%files courier-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cou*

%files fixedsys-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/*vgafix.fon

%files system-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cvgasys.fon
%{_datadir}/wine/fonts/hvgasys.fon
%{_datadir}/wine/fonts/jvgasys.fon
%{_datadir}/wine/fonts/svgasys.fon
%{_datadir}/wine/fonts/vgas1255.fon
%{_datadir}/wine/fonts/vgas1256.fon
%{_datadir}/wine/fonts/vgas1257.fon
%{_datadir}/wine/fonts/vgas874.fon
%{_datadir}/wine/fonts/vgasys.fon
%{_datadir}/wine/fonts/vgasyse.fon
%{_datadir}/wine/fonts/vgasysg.fon
%{_datadir}/wine/fonts/vgasysr.fon
%{_datadir}/wine/fonts/vgasyst.fon

%files small-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sma*
%{_datadir}/wine/fonts/jsma*

%files marlett-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/marlett.ttf

%files ms-sans-serif-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sse*
%if 0%{?wine_staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files tahoma-fonts-system
%doc README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?wine_staging}
%files times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

%files webdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/webdings.ttf

%files wingdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/wingding.ttf

%files wingdings-fonts-system
%{_datadir}/fonts/wine-wingdings-fonts

%files desktop
%{_datadir}/applications/wine-notepad.desktop
%{_datadir}/applications/wine-winefile.desktop
%{_datadir}/applications/wine-winemine.desktop
%{_datadir}/applications/wine-mime-msi.desktop
%{_datadir}/applications/wine.desktop
%{_datadir}/applications/wine-regedit.desktop
%{_datadir}/applications/wine-uninstaller.desktop
%{_datadir}/applications/wine-winecfg.desktop
%{_datadir}/applications/wine-wineboot.desktop
%{_datadir}/applications/wine-winhelp.desktop
%{_datadir}/applications/wine-wordpad.desktop
%{_datadir}/applications/wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/icons/hicolor/scalable/apps/*svg

%files systemd
%config %{_binfmtdir}/wine.conf

# ldap subpackage
%files ldap
%{_libdir}/wine/%{winepedir}/wldap32.dll
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/wldap32.dll.so
%endif

# cms subpackage
%files cms
%{_libdir}/wine/%{winepedir}/mscms.dll
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/mscms.dll.so
%endif

# twain subpackage
%files twain
%{_libdir}/wine/%{winepedir}/twain_32.dll
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/twain_32.dll.so
%endif
%{_libdir}/wine/%{winepedir}/sane.ds
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/sane.ds.so
%endif
%{_libdir}/wine/%{winesodir}/sane.so

%files devel
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%ifarch %{ix86} x86_64 aarch64
%{_libdir}/wine/%{winepedir}/*.a
%endif
%ifarch %{ix86} x86_64
%{_libdir}/wine/%{winesodir}/*.a
%endif


%files pulseaudio
%{_libdir}/wine/%{winepedir}/winepulse.drv
%{_libdir}/wine/%{winesodir}/winepulse.so
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/winepulse.drv.so
%endif

%files alsa
%{_libdir}/wine/%{winepedir}/winealsa.drv
%{_libdir}/wine/%{winesodir}/winealsa.so
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/winealsa.drv.so
%endif

%if 0%{?fedora}
%files opencl
%{_libdir}/wine/%{winepedir}/opencl.dll
%ifarch %{arm}
%{_libdir}/wine/%{winesodir}/opencl.dll.so
%endif
%{_libdir}/wine/%{winesodir}/opencl.so
%endif

%changelog
* Sun Oct 15 2023 Michael Cronenworth <mike@cchtml.com> - 8.18-1
- version update

* Sun Oct 01 2023 Michael Cronenworth <mike@cchtml.com> - 8.17-1
- version update

* Tue Aug 22 2023 Michael Cronenworth <mike@cchtml.com> - 8.14-1
- version update

* Thu Aug 17 2023 Michael Cronenworth <mike@cchtml.com> - 8.13-1
- version update

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Michael Cronenworth <mike@cchtml.com> - 8.12-1
- version update

* Sun Jun 25 2023 Michael Cronenworth <mike@cchtml.com> - 8.11-1
- version update

* Wed Apr 19 2023 Michael Cronenworth <mike@cchtml.com> - 8.6-1
- version update

* Sat Apr 01 2023 Michael Cronenworth <mike@cchtml.com> - 8.5-1
- version update

* Tue Mar 21 2023 Michael Cronenworth <mike@cchtml.com> - 8.4-1
- version update

* Wed Feb 22 2023 Michael Cronenworth <mike@cchtml.com> - 8.2-3
- fix missing requires for win-iconv

* Tue Feb 21 2023 Michael Cronenworth <mike@cchtml.com> - 8.2-2
- fix missing requires for libjpeg and libtiff

* Mon Feb 20 2023 Michael Cronenworth <mike@cchtml.com> - 8.2-1
- version update

* Mon Feb 06 2023 Michael Cronenworth <mike@cchtml.com> - 8.1-1
- version update

* Tue Jan 24 2023 Michael Cronenworth <mike@cchtml.com> - 8.0-1
- version update

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-0.rc4.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Michael Cronenworth <mike@cchtml.com> - 8.0-0.rc4.1
- version update

* Mon Nov 28 2022 Michael Cronenworth <mike@cchtml.com> - 7.22-2
- fix typo in openal obsoletes

* Sun Nov 27 2022 Michael Cronenworth <mike@cchtml.com> - 7.22-1
- version update
- drop openal package

* Mon Oct 31 2022 Michael Cronenworth <mike@cchtml.com> - 7.20-1
- version update

* Mon Oct 24 2022 Michael Cronenworth <mike@cchtml.com> - 7.19-1
- version update

* Thu Oct 13 2022 Michael Cronenworth <mike@cchtml.com> - 7.18-2
- Require MinGW FAudio

* Tue Oct 11 2022 Michael Cronenworth <mike@cchtml.com> - 7.18-1
- version update
- Drop isdn4k-utils from Recommends

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Michael Cronenworth <mike@cchtml.com> - 7.12-2
- Requires on vkd3d

* Tue Jul 05 2022 Michael Cronenworth <mike@cchtml.com> - 7.12-1
- versuon update
- Unbundle vkd3d

* Wed Jun 22 2022 Michael Cronenworth <mike@cchtml.com> - 7.11-1
- version update

* Mon Jun 06 2022 Michael Cronenworth <mike@cchtml.com> - 7.10-2
- Require new Mono

* Mon Jun 06 2022 Michael Cronenworth <mike@cchtml.com> - 7.10-1
- version update

* Mon May 23 2022 Michael Cronenworth <mike@cchtml.com> - 7.9-1
- version update

* Tue Mar 29 2022 Michael Cronenworth <mike@cchtml.com> - 7.5-1
- version update
- drop 32-bit ARM
- require on Fedora MinGW dependencies

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 7.3-2
- Rebuild with mingw-gcc-12

* Fri Mar 11 2022 Michael Cronenworth <mike@cchtml.com> - 7.3-1
- version update

* Sun Feb 13 2022 Björn Esser <besser82@fedoraproject.org> - 7.2-1
- version update

* Mon Jan 31 2022 Björn Esser <besser82@fedoraproject.org> - 7.1-2
- Revert to wine-mono 7.0.0

* Sat Jan 29 2022 Björn Esser <besser82@fedoraproject.org> - 7.1-1
- version update

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Björn Esser <besser82@fedoraproject.org> - 7.0-1
- version update

* Sat Jan 15 2022 Björn Esser <besser82@fedoraproject.org> - 7.0-0.6rc6
- version update

* Sun Jan 09 2022 Björn Esser <besser82@fedoraproject.org> - 7.0-0.5rc5
- version update

* Mon Jan 03 2022 Michael Cronenworth <mike@cchtml.com> 7.0-0.4rc4
- version update

* Mon Jan 03 2022 FeRD (Frank Dana) <ferdnyc@gmail.com> 7.0-0.3rc3
- Silence messages from expected failures during rpm scriptlets

* Mon Dec 27 2021 Björn Esser <besser82@fedoraproject.org> - 7.0-0.2rc3
- version update

* Mon Dec 20 2021 Michael Cronenworth <mike@cchtml.com> 7.0-0.1rc2
- version update

* Wed Nov 10 2021 Michael Cronenworth <mike@cchtml.com> 6.21-1
- version update

* Mon Oct 04 2021 Michael Cronenworth <mike@cchtml.com> 6.18-1
- version update

* Mon Aug 30 2021 Michael Cronenworth <mike@cchtml.com> 6.16-1
- version update

* Wed Jul 07 2021 Michael Cronenworth <mike@cchtml.com> 6.12-1
- version update

* Sat Jun 19 2021 Michael Cronenworth <mike@cchtml.com> 6.11-1
- version update

* Mon Jun 07 2021 Michael Cronenworth <mike@cchtml.com> 6.10-1
- version update

* Mon May 24 2021 Michael Cronenworth <mike@cchtml.com> 6.9-1
- version update

* Sat May 08 2021 Michael Cronenworth <mike@cchtml.com> 6.8-1
- version update

* Sat Apr 24 2021 Michael Cronenworth <mike@cchtml.com> 6.7-1
- version update

* Sun Apr 11 2021 Michael Cronenworth <mike@cchtml.com> 6.6-1
- version update

* Mon Mar 15 2021 Michael Cronenworth <mike@cchtml.com> 6.4-1
- version update

* Sat Feb 27 2021 Michael Cronenworth <mike@cchtml.com> 6.3-1
- version update

* Sat Feb 13 2021 Michael Cronenworth <mike@cchtml.com> 6.2-1
- version update

* Mon Feb 01 2021 Michael Cronenworth <mike@cchtml.com> 6.1-1
- version update

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Michael Cronenworth <mike@cchtml.com> 6.0-1
- version update

* Sun Jan 10 2021 Michael Cronenworth <mike@cchtml.com> 6.0-0.6rc6
- version update

* Thu Jan 07 2021 Michael Cronenworth <mike@cchtml.com> 6.0-0.5rc5
- version update

* Sat Dec 26 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.4rc4
- version update

* Sat Dec 19 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.3rc3
- version update

* Sat Dec 12 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.2rc2
- version update

* Tue Dec 08 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.1rc1
- version update

