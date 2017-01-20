#!/usr/bin/env python
# coding=utf-8

# lachesis automates the segmentation of a transcript into closed captions
#
# Copyright (C) 2016-2017, Alberto Pettarin (www.albertopettarin.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Set the lachesis package up.
"""

from setuptools import setup

from setupmeta import PKG_AUTHOR
from setupmeta import PKG_AUTHOR_EMAIL
from setupmeta import PKG_CLASSIFIERS
from setupmeta import PKG_EXTRAS_REQUIRE
from setupmeta import PKG_INSTALL_REQUIRES
from setupmeta import PKG_KEYWORDS
from setupmeta import PKG_LICENSE
from setupmeta import PKG_LONG_DESCRIPTION
from setupmeta import PKG_NAME
from setupmeta import PKG_PACKAGES
from setupmeta import PKG_PACKAGE_DATA
from setupmeta import PKG_SCRIPTS
from setupmeta import PKG_SHORT_DESCRIPTION
from setupmeta import PKG_URL
from setupmeta import PKG_VERSION

__author__ = "Alberto Pettarin"
__email__ = "info@readbeyond.it"
__copyright__ = "Copyright 2016-2017, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "GNU AGPL 3"
__status__ = "Pre-Alpha"
__version__ = "0.0.2"


##############################################################################
#
# actual setup
#
##############################################################################

# scripts to be installed globally
# on Linux and Mac OS X, use the file without extension
# on Windows, use the file with .py extension
#if IS_WINDOWS:
#    PKG_SCRIPTS = [s + ".py" for s in PKG_SCRIPTS]

# now we are ready to call setup()
setup(
    name=PKG_NAME,
    version=PKG_VERSION,
    packages=PKG_PACKAGES,
    package_data=PKG_PACKAGE_DATA,
    description=PKG_SHORT_DESCRIPTION,
    long_description=PKG_LONG_DESCRIPTION,
    author=PKG_AUTHOR,
    author_email=PKG_AUTHOR_EMAIL,
    url=PKG_URL,
    license=PKG_LICENSE,
    keywords=PKG_KEYWORDS,
    classifiers=PKG_CLASSIFIERS,
    install_requires=PKG_INSTALL_REQUIRES,
    extras_require=PKG_EXTRAS_REQUIRE,
    scripts=PKG_SCRIPTS,
)
