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
Global common functions.
"""

from __future__ import absolute_import
from __future__ import print_function
import io
import os
import sys


# RUNTIME CONSTANTS

# True if running from a frozen binary (e.g., compiled with pyinstaller)
FROZEN = getattr(sys, "frozen", False)

# True if running under Python 2
PY2 = (sys.version_info[0] == 2)


# COMMON FUNCTIONS

def is_file(obj):
    """
    Return ``True`` if the given object is a file object.

    :param variant obj: the object to test
    :rtype: bool
    """
    return isinstance(obj, file) or isinstance(obj, io.TextIOWrapper)


def is_unicode(obj):
    """
    Return ``True`` if the given object is a sequence of Unicode code points.

    :param variant object: the object to test
    :rtype: bool
    """
    if PY2:
        return isinstance(obj, unicode)
    return isinstance(obj, str)


def is_list_of_unicode(obj):
    """
    Return ``True`` if the given object is a list of Unicode strings.

    :param variant obj: the object to test
    :rtype: bool
    """
    if not isinstance(obj, list):
        return False
    return reduce(lambda x, y: x and y, [is_unicode(s) for s in obj])


def to_native_string(obj):
    """
    Convert the given (string) object to the correct "native" string type:
    ``str`` (bytes) on Python 2 and ``str`` (unicode) on Python 3.

    :param variant obj: the object to convert
    :rtype: str
    """
    if not is_unicode(obj):
        raise TypeError(u"The given 'obj' must be a unicode string.")
    if PY2:
        return obj.encode("utf-8")
    return obj
