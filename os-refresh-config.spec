%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x4c29ff0e437f3351fd82bdf47c5a3bc787dc7035

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           os-refresh-config
Version:        13.0.1
Release:        1%{?dist}
Summary:        Refresh system configuration

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

BuildRequires:  git-core

Requires:       dib-utils

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-psutil

%description
Tool to refresh openstack config changes to service.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif

%autosetup -n %{name}-%{upstream_version} -S git

%build
%{py3_build}

%install
%{py3_install}
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/pre-configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/migration.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/post-configure.d

# remove tests
rm -fr %{buildroot}%{python3_sitelib}/os_refresh_config/tests

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-refresh-config
%{_libexecdir}/%{name}
%{python3_sitelib}/os_refresh_config*

%changelog
* Mon Apr 04 2022 RDO <dev@lists.rdoproject.org> 13.0.1-1
- Update to 13.0.1

