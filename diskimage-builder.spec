# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pydefault 3
%else
%global pydefault 2
%endif

%global pydefault_bin python%{pydefault}
%global pydefault_sitelib %python%{pydefault}_sitelib
%global pydefault_install %py%{pydefault}_install
%global pydefault_build %py%{pydefault}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           diskimage-builder
Summary:        Image building tools for OpenStack
Version:        XXX
Release:        XXX
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://launchpad.net/diskimage-builder
Source0:        https://tarballs.openstack.org/diskimage-builder/%{name}-%{upstream_version}.tar.gz
AutoReqProv: no

BuildArch: noarch

BuildRequires: python%{pydefault}-devel
BuildRequires: python%{pydefault}-setuptools
BuildRequires: python%{pydefault}-pbr
%if %{pydefault} == 2
BuildRequires: python-d2to1
%else
BuildRequires: python%{pydefault}-d2to1
%endif

Requires: kpartx
Requires: qemu-img
Requires: curl
Requires: tar
Requires: git
Requires: /bin/bash
Requires: /bin/sh
Requires: /usr/bin/env
Requires: python%{pydefault}
Requires: python%{pydefault}-flake8
Requires: python%{pydefault}-pbr
Requires: python%{pydefault}-six
Requires: python%{pydefault}-stevedore
%if %{pydefault} == 2
Requires: python-babel
Requires: python-networkx
Requires: PyYAML
%else
Requires: python%{pydefault}-babel
Requires: python%{pydefault}-networkx
Requires: python%{pydefault}-PyYAML
%endif

%global __requires_exclude /usr/local/bin/dib-python
%global __requires_exclude %__requires_exclude|/sbin/runscript

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%{pydefault_build}

%install
%{pydefault_install}

# explicitly remove config-applier since it does a pip install
rm -rf %{buildroot}%{_datadir}/%{name}/elements/config-applier

%description
Components of TripleO that are responsible for building disk images.

%files
%doc LICENSE
%doc doc/source/ci.md
%{_bindir}/*
%{pydefault_sitelib}/diskimage_builder*

%changelog
