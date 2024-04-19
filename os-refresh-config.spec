# Building commit snap so we can not check gpg signature
%global sources_gpg 0
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate sphinx openstackdocstheme

%{!?upstream_version: %global upstream_version %{commit}}
%global commit 4b510162e573dbde407bc362b9cdfae74397d322
%global shortcommit %(c=%{commit}; echo ${c:0:7})
# DO NOT REMOVE ALPHATAG
%global alphatag .%{shortcommit}git

%{?dlrn: %global tarsources %{name}-%{upstream_version}}
%{!?dlrn: %global tarsources %{name}}

Name:           os-refresh-config
Version:        13.2.1
Release:        0.1%{?alphatag}%{?dist}
Summary:        Refresh system configuration

License:        Apache-2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://opendev.org/openstack/%{name}/archive/%{upstream_version}.tar.gz#/%{name}-%{shortcommit}.tar.gz
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description
Tool to refresh openstack config changes to service.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif

%autosetup -n %{tarsources} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/pre-configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/configure.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/migration.d
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}/post-configure.d

%check
%tox -e %{default_toxenv}

%files
%doc README.rst
%doc LICENSE
%{_bindir}/os-refresh-config
%{_bindir}/dib-run-parts
%{_libexecdir}/%{name}
%{python3_sitelib}/os_refresh_config*
%exclude %{python3_sitelib}/os_refresh_config/tests

%changelog
* Fri Apr 19 2024 Alfredo Moralejo <amoralej@redhat.com> 13.2.1-0.1.4b510162git
- Rebuild of pre 13.2.1 release (4b510162e573dbde407bc362b9cdfae74397d322)
