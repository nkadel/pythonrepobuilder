%if 0%{?fedora} > 12
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-jmespath
Version:        0.5.0
#Release:        2%{?dist}
Release:        0.2%{?dist}
Summary:        JSON Matching Expressions
Group:          System Environment/Libraries

License:        ASL 2.0
URL:            https://github.com/boto/jmespath
Source0:        https://pypi.python.org/packages/source/j/jmespath/jmespath-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %with python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

This package contains the library for Python 2.


%package -n python3-jmespath
Summary:        JSON Matching Expressions
Group:          System Environment/Libraries

%description -n python3-jmespath
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

This package contains the library for Python 3.


%prep
%setup -q -n jmespath-%{version}

%if %with python3
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' |xargs sed -i 's|^#!.*python|#!%{__python3}|'
%endif

find -name '*.py' |xargs sed -i 's|^#!.*python|#!%{__python2}|'


%build
%if %with python3
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%{__python2} setup.py build


%install
%if %with python3
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/{,python3-}jp
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

 
%check
%if %with python3
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%{__python2} setup.py test


%files
%{python2_sitelib}/*
%{_bindir}/jp
%doc README.rst
%doc LICENSE.txt


%if %with python3
%files -n python3-jmespath
%{python3_sitelib}/*
%{_bindir}/python3-jp
%doc README.rst
%doc LICENSE.txt
%endif


%changelog
* Sun Apr  3 2016 Nico Kadel-Garcia <nkadel@skyhookwireless.com> - 0.5.0-0.2
- Backport to RHEL 7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.5.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-1
- Initial packaging
