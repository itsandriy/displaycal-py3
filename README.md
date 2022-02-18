# DisplayCAL (a.k.a DispCalGUI) Python 3 update project

This is a project intended to modernize the DisplayCAL code for use with Python 3. It was started as it appears that the
DisplayCAL author is not interested in or motivated to do so (Python 3 support has been a known issue with DisplayCAL
for more than two years now).

![image](https://user-images.githubusercontent.com/1786804/152724907-fdea50c1-8b69-454e-8634-93880c16aeff.png)


Status Update
=============

Under Python 3.9.7 here is a list of things that is working:

What is working
---------------

- The UI is starting with some annoying error messages (issue #9).
- Calibration + Profiling is working.

What is not working (yet)
-------------------------

- Installing the profile at the end of the profiling session. There are tons of ``bytes/str/unicode`` related bugs.
  Hopefully I'm solving them fairly quickly, albeit one by one.

How to install
--------------

Currently, there is no RPM, DEB, APP or MSI packages. To test the code you can either run it directly from the source
or install it as a ``sdist`` package:

```shell
git clone https://github.com/eoyilmaz/displaycal-py3
cd ./displaycal-py3/
python setup.py install --install-data $HOME/.local/
```

This should install the code as an ``sdist``. To run the UI:

```shell
displaycal
```

You may need browse to the ``bin`` folder of you ``python`` interpreter. I used a ``virtualenv`` through ``PyCharm`` to
develop and test the code.

Have fun!

Road Map
--------

Some ideas on where to focus on future development:

- Try to move the UI to Qt. This is a big ticket. The motivation behind that is that I'm much more experienced with Qt.
  In fact, I have zero experience with ``wxPython``.
- Make the code fully compliant with PEP8 with the modification of hard wrapping the code at 120 characters instead of
  80 characters. This also means a lot of class and method/function names will be changed.
- Create unit tests with ``Pytest`` and reach to 100% code coverage. The ``3.8.9.3`` version of DisplayCAL is around
  120k lines of Python code (other languages are not included) and there are no tests (or the repository I adapted
  doesn't contain any tests). This is a nightmare and super hard to maintain.
- Maybe I'm not experienced enough, and I'm wrong on saying this, but I don't see the motivation behind having a
  C-Extension for EDID, XRandr etc. stuff. It should be possible to cover all the functionality of this extension and
  stay purely in Python. It is super hard to debug (for me at least) and super hard to maintain (again, for me).
- Replace the ``wexpect.py`` with the latest release of ``Pexpect``. I'm not very familiar with this module, and there
  is no comment in the code on why we have a ``wexpect.py`` instead of using the PyPI version of ``Pexpect``.
- Replace the ``DisplayCAL.ordereddict.OrderedDict`` with the real thing.
- Replace ``os.path`` with ``pathlib``.
- Replace 
- Organize the module structure, move UI related stuff in to ``ui`` module etc., move non-source files into their own
  folders.
- Remove all the hackery that includes ``exec()``. I know, there should be a reason for them to exist, but this
  generally is considered as ``hacking``.