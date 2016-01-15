# Manage python 2.6 requirements for RHEL 5
%if ( 0%{?rhel} > 0 && 0%{?rhel} < 6 )
%define __python %{_bindir}/python2.6
%define setuptool python26-setuptools
%define name python26-awscli

# Added from python26-setuptools
%{!?python_sitelib:  %define python_sitelib  %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python_version:  %define python_version  %(%{__python} -c "import sys; sys.stdout.write(sys.version[:3])")}

%else
%define setuptool python-setuptools
%define name python-awscli
%endif

%global srcname awscli

Name: %{name}
Summary: Universal Command Line Environment for AWS.
Version: 1.9.20
Release: 0.1%{?dist}
# Actual download URL
Source0: https://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz
License: Apache License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Amazon Web Services <UNKNOWN>
Url: http://aws.amazon.com/cli/
# Deal with python 2.6 or greater requirements
%if 0%{?el5}
BuildRequires: python26
BuildRequires: python26-setuptools
%else
BuildRequires: %{__python}
BuildRequires: python-setuptools
%endif
# Not yet tested
#Requires: python-botocore == 0.3.20
#Requires: python-colorama >= 0.2.5
#Requires: python-colorama < 0.3.3
#Requires: python-docutils >= 0.10
#Requires: python-rsa >= 3.1.2
#Requires: python-rsa <= 3.3.0
# For Python 2.6
#Requires: python-argparse >= 1.1

%description
=======
aws-cli
=======

This package provides a unified command line interface to Amazon Web Services.

The aws-cli package works on Python versions:

* 2.6.5 and greater
* 2.7.x and greater
* 3.3.x and greater
* 3.4.x and greater

.. attention::
   We recommend that all customers regularly monitor the
   `Amazon Web Services Security Bulletins website`_ for any important security bulletins related to
   aws-cli.


%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/*
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}-%{version}-*.egg-info
%doc LICENSE.txt README.rst

%changelog
* Fri Jan 15 2016 Nico Kadel-Garcia <nkadel@gmail.com> - 1.9.20-0.1
- Updte to 1.9.20

* Mon Jan  4 2016 Nico Kadel-Garcia <nkadel@gmail.com> - 1.9.15-1
- Update to 1.9.15

* Mon Dec 14 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 1.9.12-1
- Update to 1.9.12

* Sat Dec  5 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 1.9.5-1
- Udpate to relase "1" for Fedora deployment
- Re-arrange if statements for RHEL 5

* Fri Nov 20 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 1.9.5-0.2
- Use build and clena steps consistent with EPEL modules

* Thu Nov  5 2015 Nico Kadel-Garcia <nkadel@gmail.com> - 1.9.5-0.1
- Initial SRPM packaging
- Add python26 and python26-setupdtools dependencies for RHEL 5
