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
TBW
"""

from __future__ import absolute_import
from __future__ import print_function

from lachesis.language import Language
import lachesis.globalfunctions as gf


class Span(object):
    """
    A Span corresponds to an arbitrary sublist of Tokens of a Document.
    Its elements might be Token objects or other (nested) Span objects.
    """

    JOINER = u""
    FLAT_JOINER = u""

    def __init__(self, raw=None, elements=None):
        self.raw = raw
        self.elements = [] if elements is None else elements

    def append(self, obj):
        self.elements.append(obj)

    def extend(self, lst):
        self.elements.extend(lst)

    def __str__(self):
        return self.string

    def _helper_string(self, delimiter, raw=False, flat=False, tagged=False):
        if raw:
            if self.raw is not None:
                return self.raw
            if flat:
                return delimiter.join([e.raw_flat_string for e in self.elements])
            return delimiter.join([e.raw_string for e in self.elements])
        else:
            if tagged:
                return delimiter.join([e.tagged_string for e in self.elements])
            return delimiter.join([e.string for e in self.elements])

    @property
    def string(self):
        return self._helper_string(self.JOINER, raw=False, tagged=False)

    @property
    def tagged_string(self):
        return self._helper_string(self.JOINER, raw=False, tagged=True)

    @property
    def raw_string(self):
        return self._helper_string(self.JOINER, raw=True, flat=False)

    @property
    def raw_flat_string(self):
        return self._helper_string(self.FLAT_JOINER, raw=True, flat=True)


class RawTextSpan(Span):
    JOINER = u"\n"
    FLAT_JOINER = u" "


class RawSentenceSpan(Span):
    JOINER = u" "
    FLAT_JOINER = u" "


class RawCCListSpan(Span):
    JOINER = u"\n\n"
    FLAT_JOINER = u" "


class RawCCSpan(Span):
    JOINER = u"\n"
    FLAT_JOINER = u" "

    def __init__(self, raw=None, elements=[], time_interval=None):
        super(RawCCSpan, self).__init__(raw=raw, elements=elements)
        self.time_interval = time_interval


class RawCCLineSpan(Span):
    pass
