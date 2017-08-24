%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:           os-refresh-config
Version:        7.0.0
Release:        1%{?dist}
Summary:        Refresh system configuration

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  git

Requires:       dib-utils
Requires:       python-psutil

%description
Tool to refresh openstack config changes to service.

%prep

%autosetup -n %{name}-%{upstream_version} -S git

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/pre-configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/migration.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/post-configure.d

# remove tests
rm -fr %{buildroot}%{python_sitelib}/os_refresh_config/tests

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-refresh-config
%{python_sitelib}/os_refresh_config*
%{_libexecdir}/%{name}

%changelog
* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 7.0.0-1
- Update to 7.0.0

