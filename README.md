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

Currently, there is no RPM, DEB, APP or MSI packages. To test the code you can install from the source:

```shell
git clone https://github.com/eoyilmaz/displaycal-py3
cd ./displaycal-py3/
python setup.py install --install-data $HOME/.local/
```

This should install the code as an ``sdist``. To run the UI:

```shell
displaycal
```

You may need browse to the ``bin`` folder of you ``python`` interpreter. I used a ``virtualenv`` to develop and test the
code.

Have fun!