
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           diskimage-builder
Summary:        Image building tools for OpenStack
Version:        1.13.0
Release:        1%{?dist}
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://launchpad.net/diskimage-builder
Source0:        http://tarballs.openstack.org/diskimage-builder/%{name}-%{version}%{?milestone}.tar.gz
AutoReqProv: no

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr

Requires: kpartx
Requires: qemu-img
Requires: curl
Requires: python-argparse
Requires: python-babel
Requires: tar
Requires: dib-utils
Requires: /bin/bash
Requires: /bin/sh
Requires: /usr/bin/env
Requires: /usr/bin/python
Requires: python(abi) = 2.7

%global __requires_exclude /usr/local/bin/dib-python
%global __requires_exclude %__requires_exclude|/sbin/runscript

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}/lib
mkdir -p %{buildroot}%{_datadir}/%{name}/elements

install -p -D -m 644 lib/* %{buildroot}%{_datadir}/%{name}/lib
cp -vr elements/ %{buildroot}%{_datadir}/%{name}

# explicitly remove config-applier since it does a pip install
rm -rf %{buildroot}%{_datadir}/%{name}/elements/config-applier

# This file is being split out of diskimage-builder, so remove it to
# avoid conflicts with the new package.
rm -f %{buildroot}%{_bindir}/dib-run-parts

%description
Components of TripleO that are responsible for building disk images.

%files
%doc LICENSE
%doc doc/source/ci.md
%{_bindir}/*
%{python2_sitelib}/diskimage_builder*
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/elements

%changelog
* Wed Mar 30 2016 RDO <rdo-list@redhat.com> 1.13.0-0.1
-  Upstream 1.13.0 
