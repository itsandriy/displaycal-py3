NUM_CPUS = $(shell nproc ||  grep -c '^processor' /proc/cpuinfo)
SETUP_PY_FLAGS = --use-distutils
VERSION := $(shell cat VERSION_BASE)
VERSION_FILE=$(CURDIR)/VERSION_BASE

all: build FORCE

build: FORCE
	python setup.py build -j$(NUM_CPUS) $(SETUP_PY_FLAGS)

clean: FORCE
	-rm -rf build
	-rm -rf .pytest_cache

dist:
	util/sdist.sh

distclean: clean FORCE
	-rm -f INSTALLED_FILES
	-rm -f setuptools-*.egg
	-rm -f use-distutils
	-rm -rf dist

clean-all: distclean
	-rm MANIFEST.in
	-rm VERSION
	-rm -Rf DisplayCAL.egg-info
	-rm DisplayCAL/__version__.py

html:
	./setup.py readme

install: build FORCE
	python setup.py install $(SETUP_PY_FLAGS)

requirements: requirements.txt requirements-dev.txt
	pip install wheel pip --upgrade
	MAKEFLAGS="-j$(NUM_CPUS)" pip install  -r requirements.txt
	MAKEFLAGS="-j$(NUM_CPUS)" pip install  -r requirements-dev.txt

uninstall:
	./setup.py uninstall $(SETUP_PY_FLAGS)

new-release:
	git add $(VERSION_FILE)
	git commit -m "Version $(VERSION)"
	git push
	git checkout main
	git merge develop
	git tag $(VERSION)
	git push origin main --tags
	python -m build
# 	twine check dist/DisplayCAL-*.whl
	twine check dist/DisplayCAL-*.tar.gz
# 	twine upload dist/DisplayCAL-*.whl
	twine upload dist/DisplayCAL-*.tar.gz

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:
