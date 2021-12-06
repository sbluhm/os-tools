%global debug_package %{nil}

Name:		os-agent	
Version:	1.2.2
Release:	1%{?dist}
Summary:	Home Assistant OS Agent

License:	Apache 2.0
URL:		https://www.home-assistant.io
Source0:	https://github.com/home-assistant/%{name}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	go

Requires:	udisk2

%description
The OS Agent for Home Assistant is used for Home Assistant OS and Home Assistant Supervised installation types.
It allows the Home Assistant Supervisor to communicate with the host operating system.

%prep
%setup -qn %{name}-%{version}


%build
go build -ldflags "-X main.version="

%install
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/dbus-1/system.d
cp contrib/haos-agent.service %{buildroot}/%{_unitdir}
cp contrib/io.hass.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d
cp os-agent %{buildroot}/%{_bindir}

%post
%systemd_post haos-agent.service

%preun
%systemd_preun haos-agent.service

%postun
%systemd_postun haos-agent.service


%files
%{_unitdir}/haos-agent.service
%{_sysconfdir}/dbus-1/system.d/io.hass.conf
%{_bindir}/os-agent



%changelog
* Mon Dec 06 2021 Stefan Bluhm <stefan.bluhm@clacee.eu> - 1.2.2-1
- Initial version.
