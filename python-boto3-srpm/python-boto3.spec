#
# spec file for package python-boto3
#
# Copyright (c) 2015 Nico Kadel-Garcia.
#

%global srcname boto3

Name:           python-%{srcname}
Version:        1.2.2
Release:        0.1%{?dist}
Url:            https://github.com/boto/%{srcname}
Summary:        The AWS SDK for Python
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         https://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel
#Suggests:       python-futures == 2.2.0
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires: python(abi)

%description
===============================
Boto 3 - The AWS SDK for Python
===============================

|Build Status| |Docs| |Version|

Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for
Python, which allows Python developers to write software that makes use
of services like Amazon S3 and Amazon EC2. You can find the latest, most
up to date, documentation at `Read the Docs`_, including a list of
services that are supported.


.. _boto: https://docs.pythonboto.org/
.. _`Read the Docs`: https://boto3.readthedocs.org/en/latest/
.. |Build Status| image:: http://img.shields.io/travis/boto/boto3/develop.svg?style=flat
    :target: https://travis-ci.org/boto/boto3
    :alt: Build Status
.. |Docs| image:: https://readthedocs.org/projects/boto3/badge/?version=latest&style=flat
    :target: https://boto3.readthedocs.org/en/latest/
    :alt: Read the docs
.. |Downloads| image:: http://img.shields.io/pypi/dm/boto3.svg?style=flat
    :target: https://pypi.python.org/pypi/boto3/
    :alt: Downloads
.. |Version| image:: http://img.shields.io/pypi/v/boto3.svg?style=flat
    :target: https://pypi.python.org/pypi/boto3/
    :alt: Version
.. |License| image:: http://img.shields.io/pypi/l/boto3.svg?style=flat
    :target: https://github.com/boto/boto3/blob/develop/LICENSE
    :alt: License

Quick Start
-----------
First, install the library and set a default region:

.. code-block:: sh

    $ pip install boto3

Next, set up credentials (in e.g. ``~/.aws/credentials``):

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_KEY
    aws_secret_access_key = YOUR_SECRET

Then, set up a default region (in e.g. ``~/.aws/config``):

.. code-block:: ini

    [default]
    region=us-east-1

Then, from a Python interpreter:

.. code-block:: python

    >>> import boto3
    >>> s3 = boto3.resource('s3')
    >>> for bucket in s3.buckets.all():
            print(bucket.name)

Development
-----------

Getting Started
~~~~~~~~~~~~~~~
Assuming that you have Python and ``virtualenv`` installed, set up your
environment and install the required dependencies like this instead of
the ``pip install boto3`` defined above:

.. code-block:: sh

    $ git clone https://github.com/boto/boto3.git
    $ cd boto3
    $ virtualenv venv
    ...
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    $ pip install -e .

Running Tests
~~~~~~~~~~~~~
You can run tests in all supported Python versions using ``tox``. By default,
it will run all of the unit tests, but you can also specify your own
``nosetests`` options. Note that this requires that you have all supported
versions of Python installed, otherwise you must pass ``-e`` or run the
``nosetests`` command directly:

.. code-block:: sh

    $ tox
    $ tox tests/unit/test_session.py
    $ tox -e py26,py33 tests/integration

You can also run individual tests with your default Python version:

.. code-block:: sh

    $ nosetests tests/unit

Generating Documentation
~~~~~~~~~~~~~~~~~~~~~~~~
Sphinx is used for documentation. You can generate HTML locally with the
following:

.. code-block:: sh

    $ pip install -r requirements-docs.txt
    $ cd docs
    $ make html

%prep
%setup -q -n %{srcname}-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst LICENSE
%{python_sitelib}/%{srcname}
%{python_sitelib}/%{srcname}-%{version}-*.egg-info

%changelog
* Wed Dec 16 2016 Nico Kadel-Garcia <nkadel@gmail.com> - 1.2.2-0.1
- Create initial .spec file with py2pack
