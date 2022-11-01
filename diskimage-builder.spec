%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           diskimage-builder
Summary:        Image building tools for OpenStack
Version:        XXX
Release:        XXX
License:        ASL 2.0
Group:          System Environment/Base
URL:            https://launchpad.net/diskimage-builder
Source0:        https://tarballs.openstack.org/diskimage-builder/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/diskimage-builder/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
AutoReqProv: no

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires: git-core
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires: kpartx
Requires: qemu-img
Requires: curl
Requires: tar
Requires: gdisk
Requires: lvm2
Requires: git-core
Requires: /usr/sbin/mkfs.ext2
Requires: /usr/sbin/mkfs.ext3
Requires: /usr/sbin/mkfs.ext4
Requires: /usr/sbin/mkfs.xfs
Requires: /usr/sbin/mkfs.vfat
Requires: /bin/bash
Requires: /bin/sh
Requires: /usr/bin/env
Requires: python3
Requires: python3-flake8 >= 3.6.0
Requires: python3-pbr >= 2.0.0
Requires: python3-stevedore >= 1.20.0
Requires: python3-networkx >= 2.3.0
Requires: python3-yaml >= 3.12

%global __requires_exclude /usr/local/bin/dib-python
%global __requires_exclude %__requires_exclude|/sbin/runscript

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -r diskimage_builder.egg-info

%build
%{py3_build}

%install
%{py3_install}

mkdir -p %{buildroot}%{_datadir}/%{name}/elements

cp -vr diskimage_builder/elements/ %{buildroot}%{_datadir}/%{name}

# explicitly remove config-applier since it does a pip install
rm -rf %{buildroot}%{_datadir}/%{name}/elements/config-applier

# This file is being split out of diskimage-builder, so remove it to
# avoid conflicts with the new package.
rm -f %{buildroot}%{_bindir}/dib-run-parts

# Fix shebangs for Python 3-only distros
%py3_shebang_fix %{buildroot}%{_datadir}/%{name}/elements/pypi/pre-install.d/04-configure-pypi-mirror
%py3_shebang_fix %{buildroot}%{_datadir}/%{name}/elements/deploy-targetcli/extra-data.d/module/targetcli-wrapper
%py3_shebang_fix %{buildroot}%{_datadir}/%{name}/elements/package-installs/bin/package-installs-squash
%py3_shebang_fix %{buildroot}%{_datadir}/%{name}/elements/svc-map/extra-data.d/10-merge-svc-map-files
%py3_shebang_fix %{buildroot}%{_datadir}/%{name}/elements/svc-map/bin/svc-map
%py3_shebang_fix %{buildroot}%{python3_sitelib}/diskimage_builder/elements/pypi/pre-install.d/04-configure-pypi-mirror
%py3_shebang_fix %{buildroot}%{python3_sitelib}/diskimage_builder/elements/deploy-targetcli/extra-data.d/module/targetcli-wrapper
%py3_shebang_fix %{buildroot}%{python3_sitelib}/diskimage_builder/elements/package-installs/bin/package-installs-squash
%py3_shebang_fix %{buildroot}%{python3_sitelib}/diskimage_builder/elements/svc-map/extra-data.d/10-merge-svc-map-files
%py3_shebang_fix %{buildroot}%{python3_sitelib}/diskimage_builder/elements/svc-map/bin/svc-map

%description
Components of TripleO that are responsible for building disk images.

%files
%doc LICENSE
%{_bindir}/*
%{python3_sitelib}/diskimage_builder*
%{_datadir}/%{name}/elements

%changelog
