%bcond_with bootstrap

# Build requires bazel. If you do not have bazel, use the option bootstrap.
# This spec file is targeted at RHEL/CentOS 8

Name:		bazel
Version:	3.3.0
Release:	1%{?dist}
Epoch:		1
Summary:	A fast, scalable, multi-language and extensible build system

License:	Apache License 2.0
URL:		https://www.bazel.build/
Source0:	https://github.com/bazelbuild/bazel/releases/download/%{version}/bazel-%{version}-dist.zip
Source1:	https://github.com/bazelbuild/bazel/archive/%{version}.tar.gz

Conflicts:      bazel
Conflicts:      bazel2

%if !%{with bootstrap}
BuildRequires:  bazel
%endif
BuildRequires:	gcc
BuildRequires:	gcc-c++	
BuildRequires:	java-11-openjdk
BuildRequires:	java-11-openjdk-devel
BuildRequires:	unzip
BuildRequires:  zip

#Requires:	

%description
Bazel is an open-source build and test tool similar to Make, Maven, and Gradle. It uses a human-readable, high-level build language. Bazel supports projects in multiple languages and builds outputs for multiple platforms. Bazel supports large codebases across multiple repositories, and large numbers of users.

%global debug_package %{nil}

%prep
%setup -q -c -n bazel-%{version}


%build
%if %{with bootstrap}
%{__mkdir_p} ./bin-hack
%{__ln_s} /usr/bin/python3 ./bin-hack/python
export PATH=$(pwd)/bin-hack:$PATH
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export CPATH=/usr/lib/jvm/java-11-openjdk/include/
export BAZEL_JAVAC_OPTS="-J-Xms384m -J-Xmx512m"
export EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk"
env EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk" bash ./compile.sh
%endif
env ./output/bazel build //src:bazel-dev

%install
install -d %{buildroot}/%{_bindir}
mv bazel-bin/src/bazel-dev %{buildroot}/%{_bindir}/bazel  # location of final build

%files
%{_bindir}/bazel

%clean
rm -Rf %{buildroot}

%changelog
* Mon Jun 29 2020 Stefan Bluhn <stefan.bluhm@clacee.eu> 3.3.0-1
- Initial version
