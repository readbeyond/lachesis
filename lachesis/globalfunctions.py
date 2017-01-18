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
import re
import sys
import tempfile

from lachesis.exacttiming import TimeValue


# RUNTIME CONSTANTS

# timing regex patterns
HHMMSS_MMM_PATTERN = re.compile(r"([0-9]*):([0-9]*):([0-9]*)\.([0-9]*)")
HHMMSS_MMM_PATTERN_COMMA = re.compile(r"([0-9]*):([0-9]*):([0-9]*),([0-9]*)")

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


def to_unicode_string(obj):
    """
    Convert the given (string) object to the correct "unicode" string type:
    ``unicode`` on Python 2 and ``str`` on Python 3.

    :param variant obj: the object to convert
    :rtype: str
    """
    if is_unicode(obj):
        return obj
    return obj.decode("utf-8")


def time_from_hhmmssmmm(string, decimal_separator="."):
    """
    Parse the given ``HH:MM:SS.mmm`` string and return a time value.

    :param string string: the string to be parsed
    :param string decimal_separator: the decimal separator to be used
    :rtype: :class:`~lachesis.exacttiming.TimeValue`
    """
    if decimal_separator == ",":
        pattern = HHMMSS_MMM_PATTERN_COMMA
    else:
        pattern = HHMMSS_MMM_PATTERN
    v_length = TimeValue("0.000")
    try:
        match = pattern.search(string)
        if match is not None:
            v_h = int(match.group(1))
            v_m = int(match.group(2))
            v_s = int(match.group(3))
            v_f = TimeValue("0." + match.group(4))
            v_length = v_h * 3600 + v_m * 60 + v_s + v_f
    except:
        pass
    return v_length


def tmp_file(suffix=u"", root=None):
    """
    Return a (handler, path) tuple
    for a temporary file with given suffix created by ``tempfile``.

    :param string suffix: the suffix (e.g., the extension) of the file
    :param string root: path to the root temporary directory;
                        if ``None``, the default temporary directory
                        will be used instead
    :rtype: tuple
    """
    return tempfile.mkstemp(suffix=suffix, dir=root)


def close_file_handler(handler):
    """
    Safely close the given file handler.

    :param object handler: the file handler (as returned by tempfile)
    """
    if handler is not None:
        try:
            os.close(handler)
        except:
            pass


def delete_file(handler, path):
    """
    Safely delete file.

    :param object handler: the file handler (as returned by tempfile)
    :param string path: the file path
    """
    close_file_handler(handler)
    if path is not None:
        try:
            os.remove(path)
        except:
            pass
