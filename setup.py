#! /usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import ez_setup
import hashlib
import time, random
import re
try:
    from urllib2 import quote
    from urllib2 import urlopen
    from urllib2 import HTTPError
except ImportError:
    from urllib.parse import quote
    from urllib.request import urlopen
    from urllib.error import HTTPError

HERE = os.path.abspath(os.path.split(os.path.realpath(__file__))[0])

TRACKINSTALL=True
if "--donottrackinstall" in sys.argv:
    TRACKINSTALL=False
    sys.argv.remove("--donottrackinstall")

try:
    from setuptools import setup, find_packages
except ImportError:
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

# Generates a unique id for ete installation. If this is an upgrade,
# use the previous id. ETEID is only used to get basic statistics
# about number of users/installations. The id generated is just a
# random unique text string. This installation script does not collect
# any personal information about you or your system.
try:
    # Avoids importing a previously generated id
    _wd = os.getcwd()
    try:
        sys.path.remove(_wd)
    except ValueError:
        _fix_path = False
    else:
        _fix_path = True

    # Is there is a previous ETE installation? If so, use the same id
    from ete3 import __installid__ as ETEID

    if _fix_path:
        sys.path.insert(0, _wd)
except Exception:
    ETEID = hashlib.md5(str(time.time()+random.random()).encode('utf-8')).hexdigest()

PYTHON_DEPENDENCIES = [
    ["numpy", "Numpy is required for the ArrayTable and ClusterTree classes.", 0],
    ["PyQt4", "PyQt4 is required for tree visualization and image rendering.", 0],
    ["lxml", "lxml is required from Nexml and Phyloxml support.", 0]
]

CLASSIFIERS= [
    "Development Status :: 6 - Mature",
    "Environment :: Console",
    "Environment :: X11 Applications :: Qt",
    "Intended Audience :: Developers",
    "Intended Audience :: Other Audience",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ]

def can_import(mname):
    'Test if a module can be imported '
    if mname == "PyQt4":
        try:
            __import__("PyQt4.QtCore")
            __import__("PyQt4.QtGui")
        except ImportError:
            return False
        else:
            return True
    else:
        try:
            __import__(mname)
        except ImportError:
            return False
        else:
            return True

print("\nInstalling ETE (A python Environment for Tree Exploration).\n")
print()

try:
    ETE_VERSION = open(os.path.join(HERE, "VERSION")).readline().strip()
except IOError:
    ETE_VERSION = 'unknown'

MOD_NAME = "ete3"

LONG_DESCRIPTION="""
The Environment for Tree Exploration (ETE) is a Python programming
toolkit that assists in the automated manipulation, analysis and
visualization of phylogenetic trees (although clustering trees or any
other tree-like data structure could be used).

ETE is currently developed as a tool for researchers working in
phylogenetics and genomics. If you use ETE for a published work,
please cite:

::

  Jaime Huerta-Cepas, Joaquin Dopazo and Toni Gabaldon. ETE: a python
  Environment for Tree Exploration. BMC Bioinformatics 2010, 11:24.


Visit http://etetoolkit.org for more info.
"""

open("%s/version.py" %MOD_NAME, 'w').write("#autogenerated by setup.py\n__version__='%s'\n__installid__='%s'\n" %(ETE_VERSION, ETEID))

try:
    _s = setup(
        include_package_data = True,

        name = MOD_NAME,
        version = ETE_VERSION,
        packages = find_packages(),

        entry_points = {"console_scripts":
                        ["ete = %s.tools.ete:main" %MOD_NAME]},
        requires = ["six"],

        # Project uses reStructuredText, so ensure that the docutils get
        # installed or upgraded on the target machine
        install_requires = [
            ],
        package_data = {

        },
        data_files = [("%s/tools" %MOD_NAME, ["%s/tools/phylobuild.cfg" %MOD_NAME])],

        # metadata for upload to PyPI
        author = "Jaime Huerta-Cepas",
        author_email = "jhcepas@gmail.com",
        maintainer = "Jaime Huerta-Cepas",
        maintainer_email = "jhcepas@gmail.com",
        platforms = "OS Independent",
        license = "GPLv3",
        description = "A Python Environment for (phylogenetic) Tree Exploration",
        long_description = LONG_DESCRIPTION,
        classifiers = CLASSIFIERS,
        provides = [MOD_NAME],
        keywords = "Tree handling, manipulation, analysis and visualization",
        url = "http://etetoolkit.org",
#        download_url = "http://etetoolkit.org/static/releases/ete3/",
    )

except:
    print("\033[91m - Errors found! - \033[0m")
    raise

else:

    print("\033[92m - Done! - \033[0m")
    missing = False
    for mname, msg, ex in PYTHON_DEPENDENCIES:
        if not can_import(mname):
            print(" Warning:\033[93m Optional library [%s] could not be found \033[0m" %mname)
            print("  ",msg)
            missing=True

    notwanted = set(["-h", "--help", "-n", "--dry-run"])
    seen = set(_s.script_args)
    wanted = set(["install", "bdist", "bdist_egg"])
    if TRACKINSTALL and (wanted & seen) and not (notwanted & seen):
        try:
            welcome = quote("New alien in earth!")
            urlopen("http://etetoolkit.org/static/et_phone_home.php?ID=%s&VERSION=%s&MSG=%s"
                            %(ETEID, ETE_VERSION, welcome))
        except Exception:
            pass
