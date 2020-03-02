# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           os-refresh-config
Version:        XXX
Release:        XXX
Summary:        Refresh system configuration

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git

Requires:       dib-utils

BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr

Requires:       python%{pyver}-psutil

%description
Tool to refresh openstack config changes to service.

%prep

%autosetup -n %{name}-%{upstream_version} -S git

%build
%{pyver_build}

%install
%{pyver_install}
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/pre-configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/migration.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/post-configure.d

# remove tests
rm -fr %{buildroot}%{pyver_sitelib}/os_refresh_config/tests

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-refresh-config
%{_libexecdir}/%{name}
%{pyver_sitelib}/os_refresh_config*

%changelog
