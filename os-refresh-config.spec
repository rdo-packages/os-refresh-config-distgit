
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           os-refresh-config
Version:        11.0.1
Release:        1%{?dist}
Summary:        Refresh system configuration

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git

Requires:       dib-utils

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-psutil

%description
Tool to refresh openstack config changes to service.

%prep

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
* Mon Jun 14 2021 RDO <dev@lists.rdoproject.org> 11.0.1-1
- Update to 11.0.1

* Thu Mar 11 2021 RDO <dev@lists.rdoproject.org> 11.0.0-1
- Update to 11.0.0

