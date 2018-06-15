%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           diskimage-builder
Summary:        Image building tools for OpenStack
Version:        2.12.0
Release:        1%{?dist}
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://launchpad.net/diskimage-builder
Source0:        https://tarballs.openstack.org/diskimage-builder/%{name}-%{upstream_version}.tar.gz
AutoReqProv: no

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python-d2to1
BuildRequires: python2-pbr

Requires: kpartx
Requires: qemu-img
Requires: curl
Requires: python-babel
Requires: tar
Requires: git
Requires: dib-utils
Requires: /bin/bash
Requires: /bin/sh
Requires: /usr/bin/env
Requires: /usr/bin/python
Requires: python(abi) = 2.7
Requires: python2-flake8
Requires: python-networkx
Requires: python2-pbr
Requires: python2-six
Requires: python2-stevedore
Requires: PyYAML

%global __requires_exclude /usr/local/bin/dib-python
%global __requires_exclude %__requires_exclude|/sbin/runscript

%prep
%setup -q -n %{name}-%{upstream_version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}/elements

cp -vr diskimage_builder/elements/ %{buildroot}%{_datadir}/%{name}

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
%{_datadir}/%{name}/elements

%changelog
* Tue Mar 14 2018 RDO <dev@lists.rdoproject.org> 2.12.0-1
- Update to 2.12.0

* Tue Mar 13 2018 RDO <dev@lists.rdoproject.org> 2.11.0-1
- Update to 2.11.0

* Thu Feb 15 2018 Haikel Guemar <hguemar@fedoraproject.org> 2.10.1-1
- Update to 2.10.1

