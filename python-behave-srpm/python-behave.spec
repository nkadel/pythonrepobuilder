%if 0%{?rhel} >= 6 || 0%{?fedora} >= 18
%bcond_without documentation
%bcond_without testsuite
%else
%bcond_with documentation
%bcond_with testsuite
%endif

%{?!__python2:%global __python2 %{__python}}
%{?!python2_sitelib:%global python2_sitelib %{python_sitelib}}
%global modname behave

Name:               python-%{modname}
Version:            1.2.5
Release:            3%{?dist}
Summary:            Tools for the behavior-driven development, Python style

License:            BSD
URL:                http://pypi.python.org/pypi/%{modname}
Source0:            http://pypi.python.org/packages/source/b/%{modname}/%{modname}-%{version}.tar.gz
# Pending pull request in the upstream repository
# https://github.com/behave/behave/pull/86
Patch0: HTML-Formatter.patch
Patch1: html_formatter_no_set_codecs.patch
BuildArch:          noarch

Requires:           python-setuptools
BuildRequires:      python-parse
BuildRequires:      python-setuptools
BuildRequires:      python2-devel
BuildRequires:      python-parse, python-parse_type
Requires:           python-parse, python-parse_type

%if %{with testsuite}
BuildRequires:      python-mock
BuildRequires:      python-nose
%endif

%{?el6:BuildRequires:      python-ordereddict}
%{?el6:Requires:    python-ordereddict}
%{?el6:BuildRequires:      python-argparse}
%{?el6:Requires:    python-argparse}
%{?el6:BuildRequires:    python-importlib}
%{?el6:Requires:    python-importlib}


%description
Behavior-driven development (or BDD) is an agile software development
technique that encourages collaboration between developers, QA and non-
technical or business participants in a software project.

*%{modname}* uses tests written in a natural language style, backed up by
Python code.


%if %{with documentation}
%package doc
Summary:            Documentation for %{name}

%{?!el6:BuildRequires:      python-sphinx}
%{?el6:BuildRequires:      python-sphinx10}
BuildRequires:      help2man
BuildRequires:      python-sphinxcontrib-cheeseshop

%description doc
Behavior-driven development (or BDD) is an agile software development
technique that encourages collaboration between developers, QA and non-
technical or business participants in a software project.

*%{modname}* uses tests written in a natural language style, backed up by
Python code.

This package contains documentation in reST and HTML formats and some
brief feature-examples.
%endif


%prep
%setup -q -n %{modname}-%{version}
%patch0 -p1 -b .HTMLformatter
%patch1 -p1 -b .html_no_codecs

# Remove bundled egg-info in case it exists
rm -rf %{modname}*.egg-info

%if %{with documentation}
# Copy reST-files into a seperate dir
mkdir -p reST
cp -a docs/*.rst reST

# Fix setting for python-sphinx10 on el6
%{?el6:sed -i -e 's!sphinx-build!sphinx-1.0-build!g' docs/Makefile}
%endif


%build
%{__python2} setup.py build

%if %{with documentation}
# Build the autodocs
make html -C docs

rm -rf build/docs/html/.buildinfo
mv build/docs/html .
%endif


%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}


%if %{with documentation}
# Generate a manpage. Doesn't work on el6.
PYTHONPATH=%{buildroot}%{python2_sitelib}/%{modname}*.egg-info \
%{?!el6:help2man --no-info --name="Run a number of feature tests with behave." \
    --output=%{modname}.1 --no-discard-stderr \
    %{buildroot}%{_bindir}/%{modname}}

# Install the manpage.
%{?!el6:install -d %{buildroot}%{_mandir}/man1}
%{?!el6:install -p -m 0644 %{modname}.1 %{buildroot}%{_mandir}/man1/}
%endif

# As of now (2013-10-22) behave supports python2 only
# see https://github.com/behave/behave/issues/119 for more
find %{buildroot}%{_bindir} -type f \
    | xargs sed -i '1s|^#!python|#!%{__python2}|'


%check
%if %{with testsuite}
nosetests -v
%endif


%files
%doc README.rst LICENSE
%{_bindir}/%{modname}
%if %{with documentation}
%{?!el6:%{_mandir}/man1/%{modname}.*}
%endif
%{python2_sitelib}/*

%if %{with documentation}
%files doc
%doc README.rst LICENSE html reST
%endif


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Matej Cepl <mcepl@redhat.com> - 1.2.5-2
- Add a patch for embeding video in HTML formatted report

* Wed Apr 29 2015 Matej Cepl <mcepl@redhat.com> - 1.2.5-1
- Upgrade to the latest release (fix #1214767)

* Fri Sep 12 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.4-4
- Add another patch to fix an Unicode error (thanks for vbenes for
  fixing my earlier proposal).

* Thu Jul 17 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.4-2
- Build documentation even on EPEL-7.

* Thu Jun 19 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.4-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.3-13
- Remove bundled compatibility libraries and add Requires
  (fix #1096220).

* Mon Apr 07 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.3-12
- Add python-setuptools dependency (fix #1084996)

* Wed Mar 19 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.3-11
- Another fix for RHBZ# 1067388 by Vadim Rutkovsky

* Wed Mar 12 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.3-10
- Fix Patch 1

* Wed Mar 12 2014 Matěj Cepl <mcepl@redhat.com> - 1.2.3-9
- Add two patches provided by Vadim Rutkovsky (fix #1058371 and
  #1067388)

* Tue Oct 29 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-8
- Add Vadim Rutkovsky’s HTML Formatter patch (fix #1024023)

* Wed Oct 23 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-7
- Make generating of docs conditional again.

* Wed Oct 23 2013 Björn Esser <bjoern.esser@gmail.com> - 1.2.3-6
- fixed all remaining issues as mentioned in rhbz# 987622 c# 16
- added needed conditionals for building on el6.

* Tue Oct 22 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-5
- Generate sphinx documentation

* Tue Oct 22 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-4
- Fix spelling to en_US (apparently reviewer doesn't understand proper
  English ;))
- Add specific python2 marcros
- Fix files in _bindir to refer to python2 explicitly.
- Run testsuite

* Mon Oct 21 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-3
- Update generation of manpage from --help output.

* Sun Jul 28 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-2
- Fix changelog
- Give up on Python3 module ATM
  (https://bugzilla.redhat.com/show_bug.cgi?id=987622#c2 and
  https://github.com/behave/behave/issues/119)
- noarch package doesn't need CFLAGS set

* Tue Jul 23 2013 Matěj Cepl <mcepl@redhat.com> - 1.2.3-1
- initial package for Fedora
