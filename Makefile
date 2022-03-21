NUM_CPUS = $(shell nproc ||  grep -c '^processor' /proc/cpuinfo)
SETUP_PY_FLAGS = --use-distutils

all: build FORCE

build: FORCE
	python setup.py build -j$(NUM_CPUS) $(SETUP_PY_FLAGS)

clean: FORCE
	-rm -rf build

dist:
	util/sdist.sh

distclean: clean FORCE
	-rm -f INSTALLED_FILES
	-rm -f setuptools-*.egg
	-rm -f use-distutils

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

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:
