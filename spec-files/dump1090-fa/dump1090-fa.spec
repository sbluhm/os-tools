Name:           dump1090-fa
Version:        8.2
Release:        1%{?dist}
Summary:        dump1090-fa is a simple Mode S decoder for RTLSDR devices.

License:        BSD
URL:            https://github.com/flightaware/dump1090
Source0:        https://github.com/flightaware/dump1090/archive/refs/tags/v8.2.tar.gz
# Man page
Source1:        dump1090.md
Source2:        %{name}.service

BuildRequires:  gcc
BuildRequires:  ncurses-devel
BuildRequires:  pandoc
BuildRequires:  rtl-sdr-devel

%description
dump1090-fa is a ADS-B, Mode S, and Mode 3A/3C demodulator and decoder that will receive and decode aircraft transponder messages received via a directly connected software defined radio, or from data provided over a network connection.

It is the successor to dump1090-mutability and is maintained by FlightAware.

It can provide a display of locally received aircraft data in a terminal or via a browser map. Together with PiAware it can be used to contribute crowd-sourced flight tracking data to FlightAware.

%prep
%autosetup  -n dump1090-%{version}
pandoc -s -tman -o %{name}.1 %{SOURCE1}

%build
%set_build_flags
%make_build 

%install
#mkdir -p %{buildroot}%{_bindir}
#mkdir -p %{buildroot}%{_datadir}/%{name}
install -D -pm 755 dump1090  %{buildroot}%{_bindir}/dump1090
#install -d -m 0755 %{buildroot}%{_unitdir}
install -d %{buildroot}%{_datadir}/%{name}
cp -r tools %{buildroot}%{_datadir}/%{name}
install -D %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
#mkdir -p %{buildroot}%{_mandir}/man1
install -Dpm 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

%check

%files
%license LICENSE
%doc README.md
%{_bindir}/dump1090
%{_datadir}/%{name}
%{_unitdir}/%{name}.service
%{_mandir}/man1/%{name}.1.gz

%changelog
* Tue Oct 31 2023 Stefan Bluhm <stefan.bluhm@clacee.eu> 8.2-1
- Initial RPM
