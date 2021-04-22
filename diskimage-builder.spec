# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           diskimage-builder
Summary:        Image building tools for OpenStack
Version:        2.38.0
Release:        2%{?dist}
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://launchpad.net/diskimage-builder
Source0:        https://tarballs.openstack.org/diskimage-builder/%{name}-%{upstream_version}.tar.gz
# workaround for handling py2 and py3 metaclass issue
%if %{pyver} == 2
Patch0001: 0001-Revert-Drop-six-usage.patch
%endif
AutoReqProv: no

BuildArch: noarch

BuildRequires: git
BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr
%if %{pyver} == 3
BuildRequires: /usr/bin/pathfix.py
%endif

Requires: kpartx
Requires: qemu-img
Requires: curl
Requires: tar
Requires: gdisk
Requires: lvm2
Requires: git
Requires: dib-utils
Requires: xfsprogs
Requires: /bin/bash
Requires: /bin/sh
Requires: /usr/bin/env
Requires: python%{pyver}
Requires: python%{pyver}-flake8
Requires: python%{pyver}-pbr
Requires: python%{pyver}-six
Requires: python%{pyver}-stevedore
%if %{pyver} == 2
Requires: python-babel
Requires: python-networkx
Requires: PyYAML
%else
Requires: python%{pyver}-babel
Requires: python%{pyver}-networkx
Requires: python%{pyver}-PyYAML
%endif

%global __requires_exclude /usr/local/bin/dib-python
%global __requires_exclude %__requires_exclude|/sbin/runscript

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -r diskimage_builder.egg-info

%build
%{pyver_build}

%install
%{pyver_install}

mkdir -p %{buildroot}%{_datadir}/%{name}/elements

cp -vr diskimage_builder/elements/ %{buildroot}%{_datadir}/%{name}

# explicitly remove config-applier since it does a pip install
rm -rf %{buildroot}%{_datadir}/%{name}/elements/config-applier

# This file is being split out of diskimage-builder, so remove it to
# avoid conflicts with the new package.
rm -f %{buildroot}%{_bindir}/dib-run-parts

%if %{pyver} == 3
# Fix shebangs for Python 3-only distros
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/elements/pypi/pre-install.d/04-configure-pypi-mirror
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/elements/deploy-targetcli/extra-data.d/module/targetcli-wrapper
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/elements/package-installs/bin/package-installs-squash
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/elements/svc-map/extra-data.d/10-merge-svc-map-files
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{_datadir}/%{name}/elements/svc-map/bin/svc-map
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{pyver_sitelib}/diskimage_builder/elements/pypi/pre-install.d/04-configure-pypi-mirror
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{pyver_sitelib}/diskimage_builder/elements/deploy-targetcli/extra-data.d/module/targetcli-wrapper
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{pyver_sitelib}/diskimage_builder/elements/package-installs/bin/package-installs-squash
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{pyver_sitelib}/diskimage_builder/elements/svc-map/extra-data.d/10-merge-svc-map-files
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{pyver_sitelib}/diskimage_builder/elements/svc-map/bin/svc-map
%endif

%description
Components of TripleO that are responsible for building disk images.

%files
%doc LICENSE
%doc doc/source/ci.md
%{_bindir}/*
%{pyver_sitelib}/diskimage_builder*
%{_datadir}/%{name}/elements

%changelog
* Mon Apr 12 2021 Chandan Kumar <chkumar@redhat.com> 2.38.0-2
- Added revert patch for six

* Tue Jun 09 2020 RDO <dev@lists.rdoproject.org> 2.38.0-1
- Update to 2.38.0

* Tue Oct 01 2019 RDO <dev@lists.rdoproject.org> 2.27.2-1
- Update to 2.27.2

