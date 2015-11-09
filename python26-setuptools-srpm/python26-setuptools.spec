%{!?__python2:        %define __python2 /usr/bin/python2.6}
%{!?python2_sitelib:  %define python2_sitelib  %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %define python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_version:  %define python2_version  %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}

%define __os_install_post %{__multiple_python_os_install_post}
%define __python_provides %{__multiple_python_provides}
%define __python_requires %{__multiple_python_requires}

%define modn   setuptools
%define modv   0.7.4


Summary:       Easily build and distribute Python packages
Name:          python26-%{modn}
Version:       %{modv}
Release:       0.1%{?dist}%{?pext}
License:       Python or ZPLv2.0
Group:         Development/Libraries
Source0:       https://pypi.python.org/packages/source/s/%{modn}/%{modn}-%{modv}.tar.gz
Patch0:        %{modn}-0.7.4-build.patch
URL:           https://pypi.python.org/pypi/%{modn}/
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:        Python Packaging Authority <distutils-sig@python.org>
Provides:      python(%{modn}) = %{modv}
Provides:      python(%{modn}.command) = %{modv}
Provides:      python(%{modn}.tests) = %{modv}
Provides:      python(_markerlib) = %{modv}
BuildRequires: python26-devel
BuildArch:     noarch


%description
Setuptools is a collection of enhancements to the Python distutils that
allows to more easily build and distribute Python packages, especially
ones that have dependencies on other packages.


%prep
%setup -q -n %{modn}-%{modv}
%patch0 -p1

# Cleanup
%{__rm} -f *.egg-info/*.orig


%build
%{__python2} -c 'execfile("setup.py")' build


%check
%{__python2} setup.py test


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_prefix}

%{__python2} -c 'execfile("setup.py")' install \
	--skip-build -O1 --root ${RPM_BUILD_ROOT}


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGES.* CONTRIBUTORS* DEVGUIDE* README*
%doc --parents docs/*.txt
%{_bindir}/easy_install
%{_bindir}/easy_install-%{python2_version}
%{python2_sitelib}/%{modn}
%{python2_sitelib}/_markerlib
%{python2_sitelib}/easy_install.py*
%{python2_sitelib}/pkg_resources.py*
%{python2_sitelib}/*.egg-info


%changelog
* Thu Nov 05 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 0.7.4-0.1
- Roll back release number to avoid upstream conflicts

* Wed Feb 04 2015 Peter Pramberger <peterpramb@member.fsf.org> - 0.7.4-1
- Initial build
