%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 28
%global with_python3 1
%endif

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

%if 0%{?with_python3} == 0
# begin python2 requirements
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pbr

Requires:       python2-psutil
# end python2 requirements
%else
# begin python3 requirements
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr

Requires:       python3-psutil
# end python3 requirements
%endif

%description
Tool to refresh openstack config changes to service.

%prep

%autosetup -n %{name}-%{upstream_version} -S git

%build
%if 0%{?with_python3} == 0
%{py2_build}
%else
%{py3_build}
%endif

%install
%if 0%{?with_python3} == 0
%{py2_install}
%else
%{py3_install}
%endif
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
