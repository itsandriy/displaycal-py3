#!/usr/bin/env python3

import calendar
import codecs
import glob
import os
import re
import shutil
import subprocess
import sys
import time
from configparser import RawConfigParser
from distutils.util import get_platform
from hashlib import md5, sha1
from textwrap import fill
from time import gmtime, strftime

if sys.platform == "win32":
    import msilib

sys.path.insert(0, "DisplayCAL")

pypath = os.path.abspath(__file__)
pydir = os.path.dirname(pypath)


def create_appdmg(zeroinstall=False):
    if zeroinstall:
        dmgname = name + "-0install"
        srcdir = "0install"
    else:
        dmgname = name + "-" + version
        srcdir = f"py2app.{get_platform()}-py{sys.version[:3]}"

    retcode = subprocess.call(["hdiutil", "create", os.path.join(pydir, "dist", dmgname + ".dmg"),
                               "-volname", dmgname, "-srcfolder",
                               os.path.join(pydir, "dist", srcdir, dmgname)])

    if retcode != 0:
        sys.exit(retcode)


def format_changelog(changelog, format="appstream"):
    if format.lower() in ("appstream", "rpm"):
        from xml.etree import ElementTree as ET

        # Remove changelog entries of prev versions
        changelog = re.sub(r'(?s:\s*<p id="changelog-.*$)', "", changelog)
        # AppStream: Do not assume the format is HTML. Only paragraph (p),
        # ordered list (ol) and unordered list (ul) are supported at this time.
        # + list items (li)
        allowed_tags = ["p", "ol", "ul", "li"]

        if format == "rpm":
            allowed_tags.append("a")

        changelog = re.sub(r"\s*<dt(?:\s+[^>]*)?>.+?</dt>\n?", "", changelog)
        changelog = re.sub(r"<(h4|p)(?:\s+[^>]*)?>(.+?)</\1>", r"<p>\2</p>", changelog)
        # Remove everything between <!--more-->..<!--/more-->
        changelog = re.sub(r"(?s:<!--more-->.+?<!--/more-->)", "", changelog)
        # Remove all except allowed tags
        tags = re.findall(r'<[^/][^>]+>', changelog)

        for tag in tags:
            tagname = tag.strip('<>').split()[0]

            if tagname not in allowed_tags:
                changelog = changelog.replace(tag, "")
                changelog = changelog.replace("</" + tagname + ">", "")

        # Remove macOS and Windows specific items
        changelog = re.sub(r"(?is:<li>[^,:<]*(?:Mac ?OS ?X?|Windows)([^,:<]*):.*?</li>)", "", changelog)
        # Remove text "Linux" in item before colon (":")
        changelog = re.sub(r"(<li>[^,:<]*)\s+Linux([^,:<]*):", r"\1\2", changelog)

        if format.lower() == "appstream":
            # Conform to appstream-util validate-strict rules
            def truncate(matches, maxlen):
                return "%s%s%s" % (matches.group(1),
                                   # appstream-util validate counts bytes, not characters
                                   matches.group(2).encode("UTF-8")[:maxlen - 3].rstrip().decode("UTF-8", "ignore") +
                                   "...", matches.group(3))

            # - <p> maximum is 600 chars
            changelog = re.sub(r"(<p>)\s*([^<]{601,}?)\s*(</p>)", lambda matches: truncate(matches, 600), changelog)
            # - <li> cannot end in '.'
            changelog = re.sub(r"([^.])\.\s*</li>", r"\1</li>", changelog)
            # - <li> maximum is 100 chars
            changelog = re.sub(r"(<li>)\s*([^<]{101,}?)\s*(<(?:ol|ul|/li)>)", lambda matches: truncate(matches, 100),
                            changelog)

        # Nice formatting
        changelog = re.sub(r"(?m:^\s+)", r"\t" * 4, changelog)  # Multi-line
        changelog = re.sub(r"(<li)", r"\t\1", changelog)
        changelog = re.sub(r"\s*\n\s*\n", "\n", changelog)
        # Remove line breaks
        changelog = re.sub(r"\s*\n+\s*", " ", changelog)

        # Parse into ETree
        tree = ET.fromstring(f"<root>{changelog.encode('UTF-8')}</root>")
    else:
        raise ValueError(f"Changelog format not supported: {format!r}")

    if format.lower() == "rpm":
        changelog = ""

        for lvl1 in tree:
            if lvl1.tag in ("ol", "ul"):
                for lvl2 in lvl1:
                    if lvl2.tag == "li":
                        changelog = f"{changelog}  * {lvl2.text.lstrip()}"
                        links = []
                        link_cnt = 1

                        for lvl3 in lvl2:
                            if lvl3.tag in ("ol", "ul"):
                                if not changelog.endswith("\n"):
                                    changelog = f"{changelog}\n"

                                for lvl4 in lvl3:
                                    if lvl4.tag == "li":
                                        changelog += f"    {lvl4.text.lstrip()}"

                                        for lvl5 in lvl4:
                                            if lvl5.tag == "a":
                                                # Collect links
                                                links.append(lvl5.attrib["href"])
                                                changelog = f"{changelog}{lvl5.text.strip()}[{link_cnt}]{lvl5.tail}"
                                                link_cnt += 1

                                        if not changelog.endswith("\n"):
                                            changelog = f"{changelog}\n"
                            elif lvl3.tag == "a":
                                # Collect links
                                links.append(lvl3.attrib["href"])
                                changelog = f"{changelog}{lvl3.text.strip()}[{link_cnt}]{lvl3.tail}"
                                link_cnt += 1

                        if not changelog.endswith("\n"):
                            changelog = f"{changelog}\n"

                        for n, link in enumerate(links, 1):
                            changelog = f"{changelog}    [{n}] {link}\n"

        # Wrap each line to 67 chars
        changelog = changelog.splitlines()

        for i, line in enumerate(changelog):
            block = fill(line.rstrip(), 67, subsequent_indent='    ')
            changelog[i] = block

        changelog = "\n".join(changelog)
    else:
        # Nice formatting
        from xml.sax.saxutils import escape
        changelog = ""
        nump = 0
        maxp = 3

        for lvl1 in tree:
            if lvl1.tag in {"p", "ol", "ul"}:
                text = lvl1.text.strip()

                if lvl1.tag == "p":
                    if nump == maxp:
                        continue

                    nump += 1

                changelog = f"{changelog}\t\t\t\t<{lvl1.tag}>\n"

                if text:
                    changelog = f"{changelog}\t\t\t\t\t{escape(text)}\n"

                for lvl2 in lvl1:
                    if lvl2.tag == "li":
                        changelog = f"{changelog}\t\t\t\t\t<li>\n\t\t\t\t\t\t{escape(lvl2.text.strip())}\n"

                        for lvl3 in lvl2:
                            if lvl3.tag in {"p", "ol", "ul"}:
                                text = lvl3.text.strip()

                                if lvl3.tag == "p":
                                    if nump == maxp:
                                        continue

                                    nump += 1

                                changelog = f"{changelog}\t\t\t\t\t\t<{lvl3.tag}>\n"

                                if text:
                                    changelog = f"{changelog}\t\t\t\t\t\t\t{escape(text)}\n"

                                for lvl4 in lvl3:
                                    if lvl4.tag == "li":
                                        changelog = f"{changelog}\t\t\t\t\t\t\t<li>{escape(lvl4.text.strip())}</li>\n"

                                changelog = f"{changelog}\t\t\t\t\t\t</{lvl3.tag}>\n"

                        changelog = f"{changelog}\t\t\t\t\t</li>\n"

                changelog = f"{changelog}\t\t\t\t</{lvl1.tag}>\n"

        changelog = changelog.rstrip()

    return changelog


def replace_placeholders(tmpl_path, out_path, lastmod_time=0, iterable=None):
    global longdesc

    with codecs.open(tmpl_path, "r", "UTF-8") as tmpl:
        tmpl_data = tmpl.read()

    if os.path.basename(tmpl_path).startswith("debian"):
        longdesc_backup = longdesc
        longdesc = "\n".join([" " + (line if line.strip() else ".") for line in longdesc.splitlines()])

    appdatadesc = "\n\t\t\t" + longdesc.replace("\n", "\n\t\t\t").replace(".\n", ".\n\t\t</p>\n\t\t<p>\n") + "\n\t\t"
    mapping = {
        # e.g. Tue Jul 06 2010
        "DATE": strftime("%a %b %d %Y", gmtime(lastmod_time or os.stat(tmpl_path).st_mtime)),
        # e.g. Wed Jul 07 15:25:00 UTC 2010
        "DATETIME": strftime("%a %b %d %H:%M:%S UTC %Y", gmtime(lastmod_time or os.stat(tmpl_path).st_mtime)),
        "DEBPACKAGE": name.lower(),
        # e.g. Wed, 07 Jul 2010 15:25:00 +0100
        "DEBDATETIME": strftime("%a, %d %b %Y %H:%M:%S ",
                                gmtime(lastmod_time or os.stat(tmpl_path).st_mtime)) + "+0000",
        "DOMAIN": domain.lower(),
        "REVERSEDOMAIN": ".".join(reversed(domain.split("."))),
        "ISODATE": strftime("%Y-%m-%d", gmtime(lastmod_time or os.stat(tmpl_path).st_mtime)),
        "ISODATETIME": strftime("%Y-%m-%dT%H:%M:%S", gmtime(lastmod_time or os.stat(tmpl_path).st_mtime)) + "+0000",
        "ISOTIME": strftime("%H:%M", gmtime(lastmod_time or os.stat(tmpl_path).st_mtime)),
        "TIMESTAMP": str(int(lastmod_time)),
        "SUMMARY": description,
        "DESC": longdesc,
        "APPDATADESC": f'<p>{appdatadesc}</p>\n\t\t<p xml:lang="en">{appdatadesc}</p>',
        "APPNAME": name,
        "APPNAME_HTML": name_html,
        "APPNAME_LOWER": name.lower(),
        "APPSTREAM_ID": appstream_id,
        "AUTHOR": author,
        "AUTHOR_EMAIL": author_email.replace("@", "_at_"),
        "MAINTAINER": author,
        "MAINTAINER_EMAIL": author_email.replace("@", "_at_"),
        "MAINTAINER_EMAIL_SHA1": sha1(author_email.encode('utf-8')).hexdigest(),
        "PACKAGE": name,
        "PY_MAXVERSION": ".".join(str(n) for n in py_maxversion),
        "PY_MINVERSION": ".".join(str(n) for n in py_minversion),
        "VERSION": version,
        "VERSION_SHORT": re.sub(r"(?:\.0){1,2}$", "", version),
        "URL": f"https://{domain.lower()}/",
        # For share counts...
        "HTTPURL": f"http://{domain.lower()}/",
        "WX_MINVERSION": ".".join(str(n) for n in wx_minversion),
        "YEAR": strftime("%Y", gmtime(lastmod_time or os.stat(tmpl_path).st_mtime))
    }
    mapping.update(iterable or {})

    for key, val in mapping.items():
        tmpl_data = tmpl_data.replace(f"${{{key}}}", val)

    tmpl_data = tmpl_data.replace(f"{mapping['YEAR']}-{mapping['YEAR']}", mapping["YEAR"])

    if os.path.basename(tmpl_path).startswith("debian"):
        longdesc = longdesc_backup

    if os.path.isfile(out_path):
        with codecs.open(out_path, "r", "UTF-8") as out:
            data = out.read()

        if data == tmpl_data:
            return
    elif not os.path.isdir(os.path.dirname(out_path)):
        os.makedirs(os.path.dirname(out_path))

    with codecs.open(out_path, "w", "UTF-8") as out:
        out.write(tmpl_data)


def setup():
    if sys.platform == "darwin":
        bdist_cmd = "py2app"
    elif sys.platform == "win32":
        bdist_cmd = "py2exe"
    else:
        bdist_cmd = "bdist_bbfreeze"

    if "bdist_standalone" in sys.argv[1:]:
        i = sys.argv.index("bdist_standalone")
        sys.argv = sys.argv[:i] + sys.argv[i + 1:]

        if bdist_cmd not in sys.argv[1:i]:
            sys.argv.insert(i, bdist_cmd)
    elif "bdist_bbfreeze" in sys.argv[1:]:
        bdist_cmd = "bdist_bbfreeze"
    elif "bdist_pyi" in sys.argv[1:]:
        bdist_cmd = "pyi"
    elif "py2app" in sys.argv[1:]:
        bdist_cmd = "py2app"
    elif "py2exe" in sys.argv[1:]:
        bdist_cmd = "py2exe"

    appdata = "appdata" in sys.argv[1:]
    arch = None
    bdist_appdmg = "bdist_appdmg" in sys.argv[1:]
    bdist_pkg = "bdist_pkg" in sys.argv[1:]
    bdist_deb = "bdist_deb" in sys.argv[1:]
    bdist_pyi = "bdist_pyi" in sys.argv[1:]
    buildservice = "buildservice" in sys.argv[1:]
    setup_cfg = None
    dry_run = "-n" in sys.argv[1:] or "--dry-run" in sys.argv[1:]
    help = False
    inno = "inno" in sys.argv[1:]
    onefile = "-F" in sys.argv[1:] or "--onefile" in sys.argv[1:]
    purge = "purge" in sys.argv[1:]
    purge_dist = "purge_dist" in sys.argv[1:]
    use_setuptools = "--use-setuptools" in sys.argv[1:]
    zeroinstall = "0install" in sys.argv[1:]
    stability = "testing"

    argv = list(sys.argv[1:])

    for i, arg in enumerate(reversed(argv)):
        n = len(sys.argv) - i - 1
        arg = arg.split("=")

        if len(arg) == 2:
            if arg[0] == "--force-arch":
                arch = arg[1]
            elif arg[0] in ("--cfg", "--stability"):
                if arg[0] == "--cfg":
                    setup_cfg = arg[1]
                else:
                    stability = arg[1]

                sys.argv = sys.argv[:n] + sys.argv[n + 1:]
        elif arg[0] == "-h" or arg[0].startswith("--help"):
            help = True

    lastmod_time = 0
    non_build_args = list(
        filter(
            lambda x: x in sys.argv[1:],
            ["bdist_appdmg", "clean", "purge", "purge_dist", "uninstall", "-h", "--help", "--help-commands", "--all",
             "--name", "--fullname", "--author", "--author-email", "--maintainer", "--maintainer-email", "--contact",
             "--contact-email", "--url", "--license", "--licence", "--description", "--long-description", "--platforms",
             "--classifiers", "--keywords", "--provides", "--requires", "--obsoletes", "--quiet", "-q", "register",
             "--list-classifiers", "upload", "--use-distutils", "--use-setuptools", "--verbose", "-v", "finalize_msi"]
        )
    )

    from DisplayCAL.util_os import which

    if os.path.isdir(os.path.join(pydir, ".git")) and (which("git") or which("git.exe")) and \
            (not sys.argv[1:] or (len(non_build_args) < len(sys.argv[1:]) and not help)):
        print("Trying to get git version information...")
        git_version = None

        try:
            p = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE, cwd=pydir)
        except Exception as exception:
            print("...failed:", exception)
        else:
            git_version = p.communicate()[0].strip().decode()
            version_base_filename = os.path.join(pydir, "VERSION_BASE")
            version_base = "0.0.0.0".split(".")

            if os.path.isfile(version_base_filename):
                with open(version_base_filename) as version_base_file:
                    version_base = version_base_file.read().strip().split(".")

        print("Trying to get git information...")
        lastmod = ""
        timestamp = None
        mtime = 0

        try:
            p = subprocess.Popen(["git", "log", "-1", "--format=%ct"], stdout=subprocess.PIPE, cwd=pydir)
        except Exception as exception:
            print("...failed:", exception)
        else:
            mtime = int(p.communicate()[0].strip().decode())
            timestamp = time.gmtime(mtime)

        if timestamp:
            lastmod = strftime("%Y-%m-%dT%H:%M:%S", timestamp) + str(round(mtime - int(mtime), 6))[1:] + "Z"

        if not dry_run:
            print("Generating __version__.py")

            with open(os.path.join(pydir, "DisplayCAL", "__version__.py"), "w") as versionpy:
                versionpy.write("# generated by setup.py\n\n")
                build_time = time.time()
                versionpy.write(
                    "BUILD_DATE = %r\n" % (strftime("%Y-%m-%dT%H:%M:%S", gmtime(build_time)) + "Z")
                )

                if lastmod:
                    versionpy.write(f"LASTMOD = {lastmod!r}\n")

                if git_version:
                    print("Version", ".".join(version_base))
                    versionpy.write("VERSION = (%s)\n" % ", ".join(version_base))
                    versionpy.write("VERSION_BASE = (%s)\n" % ", ".join(version_base))
                    versionpy.write("VERSION_STRING = %r\n" % ".".join(version_base))

                    with open(os.path.join(pydir, "VERSION"), "w") as versiontxt:
                        versiontxt.write(".".join(version_base))

    if not help and not dry_run:
        # Restore setup.cfg.backup if it exists
        if os.path.isfile(os.path.join(pydir, "setup.cfg.backup")) and \
                not os.path.isfile(os.path.join(pydir, "setup.cfg")):
            shutil.copy2(os.path.join(pydir, "setup.cfg.backup"), os.path.join(pydir, "setup.cfg"))

    if not sys.argv[1:]:
        return

    global name, name_html, author, author_email, description, longdesc
    global domain, py_maxversion, py_minversion
    global version, version_lin, version_mac
    global version_src, version_tuple, version_win
    global wx_minversion, appstream_id

    from DisplayCAL.meta import (name, author, lastmod, longdesc, domain, py_minversion,
                                 version, version_tuple, script2pywname, appstream_id,
                                 get_latest_changelog_entry)
    longdesc = fill(longdesc)

    if not lastmod_time:
        lastmod_time = calendar.timegm(time.strptime(lastmod, "%Y-%m-%dT%H:%M:%SZ"))

    msiversion = ".".join((str(version_tuple[0]),
                           str(version_tuple[1]),
                           str(version_tuple[2]) +
                           str(version_tuple[3])))

    if not dry_run and not help:
        if setup_cfg or ("bdist_msi" in sys.argv[1:] and use_setuptools):
            if not os.path.exists(os.path.join(pydir, "setup.cfg.backup")):
                shutil.copy2(os.path.join(pydir, "setup.cfg"), os.path.join(pydir, "setup.cfg.backup"))

        if "bdist_msi" in sys.argv[1:] and use_setuptools:
            # setuptools parses options globally even if they're not under the
            # section of the currently run command
            os.remove(os.path.join(pydir, "setup.cfg"))

        if setup_cfg:
            shutil.copy2(os.path.join(pydir, "misc", f"setup.{setup_cfg}.cfg"),
                         os.path.join(pydir, "setup.cfg"))

    if purge or purge_dist:
        # remove the "build", "DisplayCAL.egg-info" and
        # "pyinstaller/bincache*" directories and their contents recursively

        if dry_run:
            print("dry run - nothing will be removed")

        paths = []

        if purge:
            paths += glob.glob(os.path.join(pydir, "build")) + glob.glob(
                os.path.join(pydir, name + ".egg-info")) + glob.glob(
                os.path.join(pydir, "pyinstaller", "bincache*"))
            sys.argv.remove("purge")

        if purge_dist:
            paths += glob.glob(os.path.join(pydir, "dist"))
            sys.argv.remove("purge_dist")

        for path in paths:
            if os.path.exists(path):
                if dry_run:
                    print(path)
                    continue
                try:
                    shutil.rmtree(path)
                except Exception as exception:
                    print(exception)
                else:
                    print("removed", path)

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and dry_run):
            return

    if "readme" in sys.argv[1:]:
        if not dry_run:
            for tmpl_name in ["CHANGES", "README", "history"]:
                for suffix in ("", "-fr"):
                    if suffix:
                        if tmpl_name == "README":
                            tmpl_name += suffix
                        else:
                            continue

                    replace_placeholders(os.path.join(pydir, "misc",
                                                      tmpl_name + ".template.html"),
                                         os.path.join(pydir, tmpl_name + ".html"),
                                         lastmod_time,
                                         {"STABILITY": "Beta" if stability != "stable" else ""})
        sys.argv.remove("readme")

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and dry_run):
            return

    create_appdata = ((appdata or
                       "install" in sys.argv[1:]) and
                      not help and not dry_run)

    if (("sdist" in sys.argv[1:] or "install" in sys.argv[1:] or "bdist_deb" in sys.argv[1:]) and not help):
        buildservice = True

    if create_appdata or buildservice:
        with codecs.open(os.path.join(pydir, "CHANGES.html"), "r", "UTF-8") as readme:
            readme = readme.read()

        changelog = get_latest_changelog_entry(readme)

    if create_appdata:
        from DisplayCAL.setup import get_scripts
        from DisplayCAL import localization as lang

        scripts = get_scripts()
        provides = [f"<python2>{name}</python2>"]

        for script, desc in scripts:
            provides.append(f"<binary>{script}</binary>")

        provides = "\n\t\t".join(provides)
        lang.init()
        languages = []

        for code, tdict in sorted(lang.ldict.items()):
            if code == "en":
                continue

            untranslated = 0

            for key in tdict:
                if key.startswith("*") and key != "*":
                    untranslated += 1

            languages.append('<lang percentage="%i">%s</lang>' %
                             (round((1 - untranslated / (len(tdict) - 1.0)) * 100), code))

        languages = "\n\t\t".join(languages)
        tmpl_name = appstream_id + ".appdata.xml"
        replace_placeholders(os.path.join(pydir, "misc", tmpl_name),
                             os.path.join(pydir, "dist", tmpl_name),
                             lastmod_time,
                             {
                                 "APPDATAPROVIDES": provides,
                                 "LANGUAGES": languages,
                                 "CHANGELOG": format_changelog(changelog, "appstream")
                             })
    if appdata:
        sys.argv.remove("appdata")

    if buildservice and not dry_run:
        replace_placeholders(os.path.join(pydir, "misc", "debian.copyright"),
                             os.path.join(pydir, "dist", "copyright"), lastmod_time)

    if "buildservice" in sys.argv[1:]:
        sys.argv.remove("buildservice")

    if bdist_deb:
        bdist_args = ["bdist_rpm"]

        if not arch:
            arch = get_platform().split("-")[1]
            bdist_args += ["--force-arch=" + arch]

        i = sys.argv.index("bdist_deb")
        sys.argv = sys.argv[:i] + bdist_args + sys.argv[i + 1:]

    if bdist_pyi:
        i = sys.argv.index("bdist_pyi")
        sys.argv = sys.argv[:i] + sys.argv[i + 1:]

        if "build_ext" not in sys.argv[1:i]:
            sys.argv.insert(i, "build_ext")

        if "-F" in sys.argv[1:]:
            sys.argv.remove("-F")

        if "--onefile" in sys.argv[1:]:
            sys.argv.remove("--onefile")

    if inno and sys.platform == "win32":
        tmpl_types = ["pyi" if bdist_pyi else bdist_cmd]

        if zeroinstall:
            tmpl_types.extend(["0install", "0install-per-user"])

        for tmpl_type in tmpl_types:
            inno_template_path = os.path.join(pydir, "misc", f"{name}-Setup-{tmpl_type}.iss")
            inno_template = open(inno_template_path, "r")
            inno_script = inno_template.read() % {
                "AppCopyright": "© %s %s" % (strftime("%Y"), author),
                "AppName": name,
                "AppVerName": version,
                "AppPublisher": author,
                "AppPublisherURL": f"https://{domain}/",
                "AppSupportURL": f"https://{domain}/",
                "AppUpdatesURL": f"https://{domain}/",
                "VersionInfoVersion": ".".join(map(str, version_tuple)),
                "VersionInfoTextVersion": version,
                "AppVersion": version,
                "Platform": get_platform(),
                "PythonVersion": sys.version[:3],
                "URL": f"https://{domain.lower()}/",
                "HTTPURL": f"http://{domain.lower()}/",
            }
            inno_template.close()
            inno_path = os.path.join("dist",
                                     os.path.basename(inno_template_path).replace(
                                         bdist_cmd, "%s.%s-py%s" % (bdist_cmd, get_platform(), sys.version[:3])
                                     ))

            if not dry_run:
                if not os.path.exists("dist"):
                    os.makedirs("dist")

                inno_file = open(inno_path, "w")
                inno_file.write(inno_script.encode("MBCS", "replace"))
                inno_file.close()

        sys.argv.remove("inno")

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and dry_run):
            return

    if "finalize_msi" in sys.argv[1:]:
        db = msilib.OpenDatabase(rf"dist\{name}-{msiversion}.win32-py{sys.version[:3]}.msi", msilib.MSIDBOPEN_TRANSACT)
        view = db.OpenView("SELECT Value FROM Property WHERE Property = 'ProductCode'")
        view.Execute(None)
        record = view.Fetch()
        productcode = record.GetString(1)
        view.Close()
        msilib.add_data(db, "Directory", [("ProgramMenuFolder",  # Directory
                                           "TARGETDIR",  # Parent
                                           ".")])  # DefaultDir
        msilib.add_data(db, "Directory", [("MenuDir",  # Directory
                                           "ProgramMenuFolder",  # Parent
                                           name.upper()[:6] + "~1|" + name)])  # DefaultDir
        msilib.add_data(db, "Icon", [(name + ".ico",  # Name
                                      msilib.Binary(os.path.join(pydir, name,
                                                                 "theme", "icons",
                                                                 name + ".ico")))])  # Data
        msilib.add_data(db, "Icon", [("uninstall.ico",  # Name
                                      msilib.Binary(os.path.join(pydir, name,
                                                                 "theme", "icons",
                                                                 name + "-uninstall.ico")))])  # Data
        msilib.add_data(db, "RemoveFile", [("MenuDir",  # FileKey
                                            name,  # Component
                                            None,  # FileName
                                            "MenuDir",  # DirProperty
                                            2)])  # InstallMode
        msilib.add_data(db, "Registry", [("DisplayIcon",  # Registry
                                          -1,  # Root
                                          rf"Software\Microsoft\Windows\CurrentVersion\Uninstall\{productcode}",
                                          "DisplayIcon",  # Name
                                          r"[icons]%s.ico" % name,  # Value
                                          name)])  # Component
        msilib.add_data(db, "Shortcut", [(name,  # Shortcut
                                          "MenuDir",  # Directory
                                          name.upper()[:6] + "~1|" + name,  # Name
                                          name,  # Component
                                          r"[TARGETDIR]pythonw.exe",  # Target
                                          rf'"[TARGETDIR]Scripts\{name}"',  # Arguments
                                          None,  # Description
                                          None,  # Hotkey
                                          f"{name}.ico",  # Icon
                                          None,  # IconIndex
                                          None,  # ShowCmd
                                          name)])  # WkDir
        msilib.add_data(db, "Shortcut", [("CHANGES",  # Shortcut
                                          "MenuDir",  # Directory
                                          "CHANGES|CHANGES",  # Name
                                          name,  # Component
                                          rf"[{name}]CHANGES.html",  # Target
                                          None,  # Arguments
                                          None,  # Description
                                          None,  # Hotkey
                                          None,  # Icon
                                          None,  # IconIndex
                                          None,  # ShowCmd
                                          name)])  # WkDir
        msilib.add_data(db, "Shortcut", [("LICENSE",  # Shortcut
                                          "MenuDir",  # Directory
                                          "LICENSE|LICENSE",  # Name
                                          name,  # Component
                                          rf"[{name}]LICENSE.txt",  # Target
                                          None,  # Arguments
                                          None,  # Description
                                          None,  # Hotkey
                                          None,  # Icon
                                          None,  # IconIndex
                                          None,  # ShowCmd
                                          name)])  # WkDir
        msilib.add_data(db, "Shortcut", [("README",  # Shortcut
                                          "MenuDir",  # Directory
                                          "README|README",  # Name
                                          name,  # Component
                                          rf"[{name}]README.html",  # Target
                                          None,  # Arguments
                                          None,  # Description
                                          None,  # Hotkey
                                          None,  # Icon
                                          None,  # IconIndex
                                          None,  # ShowCmd
                                          name)])  # WkDir
        msilib.add_data(db, "Shortcut", [("Uninstall",  # Shortcut
                                          "MenuDir",  # Directory
                                          "UNINST|Uninstall",  # Name
                                          name,  # Component
                                          r"[SystemFolder]msiexec",  # Target
                                          r"/x" + productcode,  # Arguments
                                          None,  # Description
                                          None,  # Hotkey
                                          "uninstall.ico",  # Icon
                                          None,  # IconIndex
                                          None,  # ShowCmd
                                          "SystemFolder")])  # WkDir

        if not dry_run:
            db.Commit()

        sys.argv.remove("finalize_msi")

        if len(sys.argv) == 1 or (len(sys.argv) == 2 and dry_run):
            return

    if zeroinstall:
        sys.argv.remove("0install")

    if bdist_appdmg:
        sys.argv.remove("bdist_appdmg")

    if bdist_pkg:
        sys.argv.remove("bdist_pkg")

    if (not zeroinstall and not buildservice and not appdata and not bdist_appdmg and not bdist_pkg) or sys.argv[1:]:
        print(sys.argv[1:])
        from DisplayCAL.setup import setup
        setup()

    if dry_run or help:
        return

    if buildservice:
        # Create control files
        mapping = {
            "POST": open(os.path.join(pydir, "util", "rpm_postinstall.sh"), "r").read().strip(),
            "POSTUN": open(os.path.join(pydir, "util", "rpm_postuninstall.sh"), "r").read().strip(),
            "CHANGELOG": format_changelog(changelog, "rpm")
        }
        tgz = os.path.join(pydir, "dist", f"{name}-{version}.tar.gz")

        if os.path.isfile(tgz):
            with open(tgz, "rb") as tgzfile:
                mapping["MD5"] = md5(tgzfile.read()).hexdigest()

        for tmpl_name in ("PKGBUILD", "debian.changelog", "debian.control",
                          "debian.copyright",
                          "debian.rules", f"{name}.changes",
                          f"{name}.dsc", f"{name}.spec",
                          "appimage.yml",
                          os.path.join("0install", "PKGBUILD"),
                          os.path.join("0install", "debian.changelog"),
                          os.path.join("0install", "debian.control"),
                          os.path.join("0install", "debian.rules"),
                          os.path.join("0install", f"{name}.dsc"),
                          os.path.join("0install", f"{name}.spec")):
            tmpl_path = os.path.join(pydir, "misc", tmpl_name)
            replace_placeholders(tmpl_path,
                                 os.path.join(pydir, "dist", tmpl_name),
                                 lastmod_time, mapping)

    if bdist_deb:
        # Read setup.cfg
        cfg = RawConfigParser()
        cfg.read(os.path.join(pydir, "setup.cfg"))
        # Get dependencies
        dependencies = [val.strip().split(None, 1) for val in
                        cfg.get("bdist_rpm", "Requires").split(",")]

        # Get group
        if cfg.has_option("bdist_rpm", "group"):
            group = cfg.get("bdist_rpm", "group")
        else:
            group = None

        # Get maintainer
        if cfg.has_option("bdist_rpm", "maintainer"):
            maintainer = cfg.get("bdist_rpm", "maintainer")
        else:
            maintainer = None

        # Get packager
        if cfg.has_option("bdist_rpm", "packager"):
            packager = cfg.get("bdist_rpm", "packager")
        else:
            packager = None

        # Convert dependency format:
        # 'package >= version' to 'package (>= version)'
        for i in range(len(dependencies)):
            if len(dependencies[i]) > 1:
                dependencies[i][1] = f"({dependencies[i][1]})"

            dependencies[i] = " ".join(dependencies[i])

        release = 1  # TODO: parse setup.cfg
        rpm_filename = os.path.join(pydir, "dist", f"{name}-{version}-{release}.{arch}.rpm")

        if not dry_run:
            # remove target directory (and contents) if it already exists
            target_dir = os.path.join(pydir, "dist", f"{name}-{version}")

            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)

            if os.path.exists(f"{target_dir}.orig"):
                shutil.rmtree(f"{target_dir}.orig")

            # use alien to create deb dir from rpm package
            retcode = subprocess.call(
                ["alien", "-c", "-g", "-k", os.path.basename(rpm_filename)], cwd=os.path.join(pydir, "dist")
            )

            if retcode != 0:
                sys.exit(retcode)

            # update changelog
            shutil.copy2(os.path.join(pydir, "dist", "debian.changelog"),
                         os.path.join(pydir, "dist", f"{name}-{version}", "debian", "changelog"))
            # update rules
            shutil.copy2(os.path.join(pydir, "misc", "alien.rules"),
                         os.path.join(pydir, "dist", f"{name}-{version}", "debian", "rules"))
            # update control
            control_filename = os.path.join(pydir, "dist", f"{name}-{version}", "debian", "control")
            shutil.copy2(os.path.join(pydir, "dist", "debian.control"), control_filename)
            # # read control file from deb dir
            # control = open(control_filename, "r")
            # lines = [line.rstrip("\n") for line in control.readlines()]
            # control.close()
            # # update control with info from setup.cfg
            # for i in range(len(lines)):
            #     if lines[i].startswith("Depends:"):
            #         # add dependencies
            #         lines[i] += ", python"
            #         lines[i] += ", python" + sys.version[:3]
            #         lines[i] += ", " + ", ".join(dependencies)
            #     elif lines[i].startswith("Maintainer:") and (maintainer or packager):
            #         # set maintainer
            #         lines[i] = "Maintainer: " + (maintainer or packager)
            #     elif lines[i].startswith("Section:") and group:
            #         # set section
            #         lines[i] = "Section: " + group
            #     elif lines[i].startswith("Description:"):
            #         lines.pop()
            #         lines.pop()
            #         break
            # # write updated control file
            # control = open(control_filename, "w")
            # control.write("\n".join(lines))
            # control.close()
            # # run strip on shared libraries
            # sos = os.path.join(change_root(target_dir, get_python_lib(True)), name, "*.so")
            # for so in glob.glob(sos):
            #     retcode = call(["strip", "--strip-unneeded", so])

            # create deb package
            retcode = subprocess.call(["chmod", "+x", "./debian/rules"], cwd=target_dir)
            retcode = subprocess.call(["./debian/rules", "binary"], cwd=target_dir)

            if retcode:
                sys.exit(retcode)

    if setup_cfg or ("bdist_msi" in sys.argv[1:] and use_setuptools):
        shutil.copy2(os.path.join(pydir, "setup.cfg.backup"), os.path.join(pydir, "setup.cfg"))

    if bdist_pyi:
        # create an executable using pyinstaller
        retcode = subprocess.call([sys.executable, os.path.join(pydir, "pyinstaller", "pyinstaller.py"),
                                   "--workpath",
                                   os.path.join(pydir, "build", f"pyi.{get_platform()}-{sys.version[:3]}"),
                                   "--distpath",
                                   os.path.join(pydir, "dist", f"pyi.{get_platform()}-{sys.version[:3]}"),
                                   os.path.join(pydir, "misc", "%s.pyi.spec" % name)])

        if retcode != 0:
            sys.exit(retcode)

    if zeroinstall:
        from xml.dom import minidom
        # Create/update 0install feeds
        from DisplayCAL.setup import get_scripts
        scripts = sorted((script2pywname(script), desc) for script, desc in get_scripts())
        cmds = []

        for script, desc in scripts:
            cmdname = "run"

            if script != name:
                cmdname += "-" + script.replace(name + "-", "")

            cmds.append((cmdname, script, desc))
            # if script.endswith("-apply-profiles"):
            #     # Add forced calibration loading entry
            #     cmds.append((cmdname + "-force", script, desc))

        # Get archive digest
        extract = f"{name}-{version}"
        archive_name = f"{extract}.tar.gz"
        archive_path = os.path.join(pydir, "dist", archive_name)

        from DisplayCAL.util_os import fs_enc

        p = subprocess.Popen(
            ["0install", "digest", archive_path.encode(fs_enc), extract],
            stdout=subprocess.PIPE, cwd=pydir
        )
        stdout, stderr = p.communicate()
        print(stdout)
        hash_ = re.search(r"(sha\d+\w+[=_][0-9a-f]+)", stdout.strip().decode())

        if not hash_:
            raise SystemExit(p.wait())

        hash_ = hash_.groups()[0]

        for tmpl_name in ("7z.xml", "argyllcms.xml", f"{name}.xml",
                          f"{name}-linux.xml", f"{name}-mac.xml",
                          f"{name}-win32.xml", "numpy.xml", "SDL.xml",
                          "pyglet.xml", "pywin32.xml", "wmi.xml",
                          "wxpython.xml", "comtypes.xml", "enum34.xml",
                          "faulthandler.xml", "netifaces.xml", "protobuf.xml",
                          "pychromecast.xml", "requests.xml", "six.xml",
                          "zeroconf.xml"):
            dist_path = os.path.join(pydir, "dist", "0install", tmpl_name)
            create = not os.path.isfile(dist_path)

            if create:
                tmpl_path = os.path.join(pydir, "misc", "0install", tmpl_name)
                replace_placeholders(tmpl_path, dist_path, lastmod_time)

            if tmpl_name.startswith(name):
                with open(dist_path) as dist_file:
                    xml = dist_file.read()
                    domtree = minidom.parseString(xml)

                # Get interface
                interface = domtree.getElementsByTagName("interface")[0]
                # Get languages
                langs = [os.path.splitext(os.path.basename(lang))[0] for lang in
                         glob.glob(os.path.join(name, "lang", "*.json"))]
                # Get architecture groups
                groups = domtree.getElementsByTagName("group")

                if groups:
                    # Get main group
                    group0 = groups[0]
                    # Add languages
                    group0.setAttribute("langs", " ".join(langs))

                # Update groups
                for i, group in enumerate(groups[-1:]):
                    if create:
                        # Remove dummy implementations
                        for implementation in group.getElementsByTagName("implementation"):
                            if implementation.getAttribute("released") == "0000-00-00":
                                implementation.parentNode.removeChild(implementation)

                        # Add commands
                        runner = domtree.createElement("runner")

                        if group.getAttribute("arch").startswith("Windows-"):
                            runner.setAttribute("command", "run-win")

                        if group.getAttribute("arch").startswith("Linux"):
                            python = "http://repo.roscidus.com/python/python"
                        else:
                            python = f"http://{domain.lower()}/0install/python.xml"

                        runner.setAttribute("interface", python)
                        runner.setAttribute("version", f"{py_minversion}.{py_minversion}..!3.0")

                        for cmdname, script, desc in cmds:
                            # Add command to group
                            cmd = domtree.createElement("command")
                            cmd.setAttribute("name", cmdname)
                            cmd.setAttribute("path", f"{script}.pyw")
                            ##if cmdname.endswith("-apply-profiles"):
                            ### Autostart
                            ##arg = domtree.createElement("suggest-auto-start")
                            ##cmd.appendChild(arg)

                            if cmdname.endswith("-apply-profiles-force"):
                                # Forced calibration loading
                                arg = domtree.createElement("arg")
                                arg.appendChild(domtree.createTextNode("--force"))
                                cmd.appendChild(arg)

                            cmd.appendChild(runner.cloneNode(True))
                            group.appendChild(cmd)

                    # Add implementation if it does not exist yet, update otherwise
                    match = None

                    for implementation in group.getElementsByTagName("implementation"):
                        match = (implementation.getAttribute("version") == version and
                                 implementation.getAttribute("stability") == stability)

                        if match:
                            break

                    if not match:
                        implementation = domtree.createElement("implementation")
                        implementation.setAttribute("version", version)
                        implementation.setAttribute("released", strftime("%Y-%m-%d", gmtime(lastmod_time)))
                        implementation.setAttribute("stability", stability)
                        digest = domtree.createElement("manifest-digest")
                        implementation.appendChild(digest)
                        archive = domtree.createElement("archive")
                        implementation.appendChild(archive)
                    else:
                        digest = implementation.getElementsByTagName("manifest-digest")[0]

                        for attrname, value in digest.attributes.items():
                            # Remove existing hashes
                            digest.removeAttribute(attrname)

                        archive = implementation.getElementsByTagName("archive")[0]

                    implementation.setAttribute("id", hash_)
                    digest.setAttribute(*hash_.split("="))

                    # Update archive
                    if stability == "stable":
                        folder = ""
                    else:
                        folder = "&folder=snapshot"

                    archive.setAttribute("extract", extract)
                    archive.setAttribute("href",
                                         f"http://{domain.lower()}/download.php?version={version}&"
                                         f"suffix=.tar.gz{folder}")
                    archive.setAttribute("size", str(os.stat(archive_path).st_size))
                    archive.setAttribute("type", "application/x-compressed-tar")
                    group.appendChild(implementation)

                if create:
                    for cmdname, script, desc in cmds:
                        # Add entry-points to interface
                        if script == name + "-eeColor-to-madVR-converter" or script.endswith("-console"):
                            continue

                        entry_point = domtree.createElement("entry-point")
                        entry_point.setAttribute("command", cmdname)
                        binname = script

                        if cmdname.endswith("-force"):
                            binname += "-force"

                        entry_point.setAttribute("binary-name", binname)
                        cfg = RawConfigParser()
                        desktopbasename = f"{script}.desktop"

                        if cmdname.endswith("-apply-profiles"):
                            desktopbasename = "z-" + desktopbasename

                        cfg.read(os.path.join(pydir, "misc", desktopbasename))

                        for option, tagname in (("Name", "name"),
                                                ("GenericName", "summary"),
                                                ("Comment", "description")):
                            for lang in [None] + langs:
                                if lang:
                                    suffix = f"[{lang}]"
                                else:
                                    suffix = ""

                                option = f"{option}{suffix}"

                                if cfg.has_option("Desktop Entry", option):
                                    value = cfg.get("Desktop Entry", option)

                                    if value:
                                        tag = domtree.createElement(tagname)

                                        if not lang:
                                            lang = "en"

                                        tag.setAttribute("xml:lang", lang)
                                        tag.appendChild(domtree.createTextNode(value))
                                        entry_point.appendChild(tag)

                        for ext, mime_type in (("ico", "image/vnd.microsoft.icon"), ("png", "image/png")):
                            icon = domtree.createElement("icon")

                            if ext == "ico":
                                subdir = ""
                                filename = script
                            else:
                                subdir = "256x256/"
                                filename = script.lower()

                            icon.setAttribute("href", f"http://{domain.lower()}/theme/icons/{subdir}{filename}.{ext}")
                            icon.setAttribute("type", mime_type)
                            entry_point.appendChild(icon)

                        interface.appendChild(entry_point)

                # Update feed
                print("Updating 0install feed", dist_path)

                with open(dist_path, "wb") as dist_file:
                    xml = domtree.toprettyxml(encoding="utf-8")
                    xml = re.sub(r"\n\s+\n", "\n", xml)
                    xml = re.sub(r"\n\s*([^<]+)\n\s*", r"\1", xml)
                    dist_file.write(xml.encode())

                # Sign feed
                zeropublish = which("0publish") or which("0publish.exe")
                args = []

                if not zeropublish:
                    zeropublish = which("0install") or which("0install.exe")

                    if zeropublish:
                        args = ["run", "--command", "0publish", "--", "http://0install.de/feeds/ZeroInstall_Tools.xml"]

                if zeropublish:
                    passphrase_path = os.path.join(pydir, "gpg", "passphrase.txt")
                    print("Signing", dist_path)

                    if os.path.isfile(passphrase_path):
                        from DisplayCAL import wexpect
                        with open(passphrase_path) as passphrase_file:
                            passphrase = passphrase_file.read().strip()

                        p = wexpect.spawn(zeropublish.encode(fs_enc), args + ["-x", dist_path.encode(fs_enc)])
                        p.expect(":")
                        p.send(passphrase)
                        p.send("\n")

                        try:
                            p.expect(wexpect.EOF, timeout=3)
                        except:
                            p.terminate()
                    else:
                        subprocess.call([zeropublish] + args + ["-x", dist_path.encode(fs_enc)])
                else:
                    print("WARNING: 0publish not found, please sign the feed!")

        # Create 0install app bundles
        bundletemplate = os.path.join("0install", "template.app", "Contents")
        bundletemplatepath = os.path.join(pydir, bundletemplate)

        if os.path.isdir(bundletemplatepath):
            p = subprocess.Popen(["0install", "-V"], stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()
            zeroinstall_version = re.search(r" (\d(?:\.\d+)+)", stdout.decode())

            if zeroinstall_version:
                zeroinstall_version = zeroinstall_version.groups()[0]

            if zeroinstall_version < "2.8":
                zeroinstall_version = "2.8"

            feeduri = f"http://{domain.lower()}/0install/{name}.xml"
            dist_dir = os.path.join(pydir, "dist", "0install", name + "-0install")

            for script, desc in scripts + [("0install-launcher", "0install Launcher"),
                                           ("0install-cache-manager", "0install Cache Manager")]:
                if script.endswith("-apply-profiles"):
                    continue

                desc = re.sub(fr"^{name} ", "", desc).strip()

                if script == "0install-launcher":
                    bundlename = name
                else:
                    bundlename = desc

                bundledistpath = os.path.join(dist_dir, desc + ".app", "Contents")
                replace_placeholders(os.path.join(bundletemplatepath, "Info.plist"),
                                     os.path.join(bundledistpath, "Info.plist"), lastmod_time,
                                     {
                                         "NAME": bundlename,
                                         "EXECUTABLE": script,
                                         "ID": ".".join(reversed(domain.split("."))) + "." + script
                                     })

                if script.startswith(name):
                    run = "0launch%s -- %s" % (re.sub(r"^%s" % name, " --command=run", script), feeduri)
                else:
                    run = {"0install-launcher": "0launch --gui " + feeduri,
                           "0install-cache-manager": "0store manage"}.get(script)

                replace_placeholders(
                    os.path.join(bundletemplatepath, "MacOS", "template"),
                    os.path.join(bundledistpath, "MacOS", script),
                    lastmod_time,
                    {"EXEC": run, "ZEROINSTALL_VERSION": zeroinstall_version}
                )
                os.chmod(os.path.join(bundledistpath, "MacOS", script), 0o755)

                for binary in os.listdir(os.path.join(bundletemplatepath, "MacOS")):
                    if binary == "template":
                        continue

                    src = os.path.join(bundletemplatepath, "MacOS", binary)
                    dst = os.path.join(bundledistpath, "MacOS", binary)

                    if os.path.islink(src):
                        linkto = os.readlink(src)

                        if os.path.islink(dst) and os.readlink(dst) != linkto:
                            os.remove(dst)

                        if not os.path.islink(dst):
                            os.symlink(linkto, dst)
                    else:
                        shutil.copy2(src, dst)

                resdir = os.path.join(bundledistpath, "Resources")

                if not os.path.isdir(resdir):
                    os.mkdir(resdir)

                if script.startswith(name):
                    iconsrc = os.path.join(pydir, name, "theme", "icons", script + ".icns")
                else:
                    iconsrc = os.path.join(pydir, "0install", "ZeroInstall.icns")

                icondst = os.path.join(resdir, script + ".icns")

                if os.path.isfile(iconsrc) and not os.path.isfile(icondst):
                    shutil.copy2(iconsrc, icondst)

            # README as .webloc file (link to homepage)
            with codecs.open(os.path.join(dist_dir, "README.webloc"), "w", "UTF-8") as readme:
                readme.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>URL</key>
    <string>https://{domain.lower()}/</string>
</dict>
</plist>
""")
            # Copy LICENSE.txt
            shutil.copy2(os.path.join(pydir, "LICENSE.txt"), os.path.join(dist_dir, "LICENSE.txt"))

    if bdist_appdmg:
        create_appdmg(zeroinstall)

    if bdist_pkg:
        version_dir = os.path.join(pydir, "dist", version)
        replace_placeholders(
            os.path.join(pydir, "misc", name + ".pkgproj"),
            os.path.join(version_dir, name + "-" + version + ".pkgproj"),
            lastmod_time, {"PYDIR": pydir}
        )
        shutil.move(
            os.path.join(pydir, "dist", f"py2app.{get_platform()}-py{sys.version[:3]}", f"{name}-{version}"),
            version_dir
        )
        os.rename(
            os.path.join(version_dir, f"{name}-{version}"),
            os.path.join(version_dir, name)
        )

        if subprocess.call(["/usr/local/bin/packagesbuild", "-v",
                            os.path.join(version_dir, f"{name}-{version}.pkgproj")]) == 0:
            # Success
            os.rename(
                os.path.join(version_dir, f"{name}.pkg"),
                os.path.join(version_dir, f"{name}-{version}.pkg")
            )


if __name__ == "__main__":
    setup()
