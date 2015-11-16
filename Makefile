 #
# Makefile - build wrapper for python modules on RHEL 6
#
#	git clone RHEL 6 SRPM building tools from
#	https://github.com/nkadel/pythonrepo

# Base directory for yum repository
REPOBASEDIR="`/bin/pwd`"
# Base subdirectories for RPM deployment
REPOBASESUBDIRS+=$(REPOBASEDIR)/pythonrepo/5/SRPMS
REPOBASESUBDIRS+=$(REPOBASEDIR)/pythonrepo/5/x86_64
REPOBASESUBDIRS+=$(REPOBASEDIR)/pythonrepo/6/SRPMS
REPOBASESUBDIRS+=$(REPOBASEDIR)/pythonrepo/6/x86_64
REPOBASESUBDIRS+=$(REPOBASEDIR)/pythonrepo/7/SRPMS
REPOBASESUBDIRS+=$(REPOBASEDIR)/pythonrepo/7/x86_64

# These build with normal mock "epel-*" setups
EPELPKGS+=

# Require customized pythonrepo local repository for dependencies
# Required for RHEL 5, provided as python-setuptools on other releases
PYTHONPKGS+=python26-setuptools-srpm
# Builds as "python26-awscli under RHEL 5
PYTHONPKGS+=python-awscli-srpm

# Populate pythonrepo with packages that require pythonrepo
all:: /usr/bin/createrepo
all:: tarballs
all:: epel-install python-install

install:: epel-install python-install

epel-install:: $(EPELOKGS)

# Ensure availability of createrepo
/usr/bin/createrepo:

# Ensure working configs for python
python-install:: pythonrepo-5-x86_64.cfg
python-install:: pythonrepo-6-x86_64.cfg
python-install:: pythonrepo-7-x86_64.cfg
python-install:: $(PYTHONPKGS)

pythonrepo-6-x86_64.cfg:: pythonrepo-6-x86_64.cfg.in
	sed "s|@@@REPOBASEDIR@@@|$(REPOBASEDIR)|g" $? > $@

pythonrepo-6-x86_64.cfg:: FORCE
	@cmp -s $@ /etc/mock/$@ || \
		(echo Warning: /etc/mock/$@ does not match $@, exiting; exit 1)

pythonrepo-7-x86_64.cfg:: pythonrepo-7-x86_64.cfg.in
	sed "s|@@@REPOBASEDIR@@@|$(REPOBASEDIR)|g" $? > $@

pythonrepo-7-x86_64.cfg:: FORCE
	@cmp -s $@ /etc/mock/$@ || \
		(echo Warning: /etc/mock/$@ does not match $@, exiting; exit 1)

# Do the "5" packages last
pythonrepo-5-x86_64.cfg:: pythonrepo-5-x86_64.cfg.in
	sed "s|@@@REPOBASEDIR@@@|$(REPOBASEDIR)|g" $? > $@

pythonrepo-5-x86_64.cfg:: FORCE
	@cmp -s $@ /etc/mock/$@ || \
		(echo Warning: /etc/mock/$@ does not match $@, exiting; exit 1)

# Used for make build with local components
pythonrepo.repo:: pythonrepo.repo.in
	sed "s|@@@REPOBASEDIR@@@|$(REPOBASEDIR)|g" $? > $@

pythonrepo.repo:: FORCE
	@cmp -s $@ /etc/yum.repos.d/$@ || \
		(echo Warning: /etc/yum.repos.d/$@ does not match $@, exiting; exit 1)

epel:: $(EPELPKGS)

# Ensure presence, and repositories, for basedirs
$(REPOBASESUBDIRS)::
	mkdir -p $@
	createrepo -q --update $@

epel-install:: $(REPOBASESUBDIRS)

epel-install:: FORCE
	@for name in $(EPELPKGS); do \
		(cd $$name && $(MAKE) all install) || exit 1; \
	done

python:: $(PYTHONPKGS)

python-install:: FORCE
	@for name in $(PYTHONPKGS); do \
		(cd $$name && $(MAKE) all install) || exit 1; \
	done

# Dependencies
python26-awscli-srpm:: python26-setuptools-srpm

# Download tarballs as needed from pypi.org
$(EPELPKGS) $(PYTHONPKGS):: $(TARBALLS)
$(EPELPKGS) $(PYTHONPKGS):: $(REPOS)

TARBALLS+=python-awscli-srpm/awscli-1.9.7.tar.gz
TARBALLS+=python26-awscli-srpm/awscli-1.9.7.tar.gz
TARBALLS+=python26-setuptools-srpm/setuptools-0.7.4.tar.gz
tarballs:: $(TARBALLS)

# Ensure that local tarballs match or are downloaded from master
# pypi.python.org repository
python26-setuptools-srpm/setuptools-0.7.4.tar.gz::
	wget --quiet --mirror --no-host-directories --cut-dirs=4 --directory-prefix=`dirname $@` \
		https://pypi.python.org/packages/source/s/setuptools/`basename $@`

python26-awscli-srpm/awscli-1.9.7.tar.gz::
	wget --quiet --mirror --no-host-directories --cut-dirs=4 --directory-prefix=`dirname $@` \
		https://pypi.python.org/packages/source/a/awscli/`basename $@`

python-awscli-srpm/awscli-1.9.7.tar.gz::
	wget --quiet --mirror --no-host-directories --cut-dirs=4 --directory-prefix=`dirname $@` \
		https://pypi.python.org/packages/source/a/awscli/`basename $@`

# Git clone operations, not normally required
# Targets may change


# Build EPEL compatible softwaer in place
$(EPELPKGS):: FORCE
	(cd $@ && $(MAKE) $(MLAGS)) || exit 1

$(PYTHONPKGS):: pythonrepo-5-x86_64.cfg
$(PYTHONPKGS):: pythonrepo-6-x86_64.cfg
$(PYTHONPKGS):: pythonrepo-7-x86_64.cfg

$(PYTHONPKGS):: FORCE
	(cd $@ && $(MAKE) $(MLAGS)) || exit 1

# Needed for local compilation, only use for dev environments
build:: pythonrepo.repo

build clean realclean distclean:: FORCE
	@for name in $(EPELPKGS) $(PYTHONPKGS); do \
	     (cd $$name && $(MAKE) $(MFLAGS) $@); \
	done

realclean distclean:: clean

clean::
	find . -name \*~ -exec rm -f {} \;

# Use this only to build completely from scratch
# Leave the rest of pythonrepo alone.
maintainer-clean:: clean
	@echo Clearing local yum repository
	find pythonrepo -type f ! -type l -exec rm -f {} \; -print

# Leave a safe repodata subdirectory
maintainer-clean:: FORCE

safe-clean:: maintainer-clean FORCE
	@echo Populate pythonrepo with empty, safe repodata
	find pythonrepo -noleaf -type d -name repodata | while read name; do \
		createrepo -q $$name/..; \
	done

# This is only for upstream repository publication.
# Modify for local use as needed, but do try to keep passwords and SSH
# keys out of the git repository fo this software.
RSYNCTARGET=rsync://localhost/pythonrepo
RSYNCOPTS=-a -v --ignore-owner --ignore-group --ignore-existing
RSYNCSAFEOPTS=-a -v --ignore-owner --ignore-group
publish:: all
publish:: FORCE
	@echo Publishing RPMs to $(RSYNCTARGET)
	rsync $(RSYNCSAFEOPTS) --exclude=repodata $(RSYNCTARGET)/

publish:: FORCE
	@echo Publishing repodata to $(RSYNCTARGET)
	find repodata/ -type d -name repodata | while read name; do \
	     rsync $(RSYNCOPTS) $$name/ $(RSYNCTARGET)/$$name/; \
	done

FORCE::

