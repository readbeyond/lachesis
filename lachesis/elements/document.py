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
import re

from lachesis.elements.span import RawSentenceSpan
from lachesis.elements.span import RawTextSpan
from lachesis.elements.span import Span
from lachesis.elements.token import EndOfLineToken
from lachesis.elements.token import EndOfSentenceToken
from lachesis.language import Language
import lachesis.globalfunctions as gf


class Document(object):
    """
    A Document is an abstract representation of closed captions,
    with or without time intervals or identifiers attached.

    Each Document offers two views of the string data:
    a ``text_view`` and a ``ccs_view``.

    A Document can be created by passing
    one of the following types
    to the ``raw`` parameter:

    * a unicode string;
    * a list of strings;
    * a ``Span`` object.

    Internally, every string is a Unicode string
    (``unicode`` in PY2, ``str`` in PY3),
    and every timing interval is a ``TimeInterval``.

    The document might have an associated language,
    represented by a ``LanguageObject`` object.
    """

    def __init__(self, raw=None, language=None):
        self.raw = self._set_raw(raw)
        self.language = Language.from_code(language)
        self.tokens = []
        self.text_view = None
        self.ccs_view = None

    def _set_raw(self, raw):
        """
        Assign the correct Span object, depending on the type of ``raw``.
        """
        if raw is None:
            return raw
        if isinstance(raw, Span):
            return raw
        if gf.is_unicode(raw):
            return RawTextSpan(raw=raw)
        if gf.is_list_of_unicode(raw):
            return RawTextSpan(
                elements=[RawSentenceSpan(raw=s) for s in raw]
            )
        raise TypeError(u"Parameter raw must be a unicode string or a list of unicode strings or a Span object. Found: '%s'" % type(raw))

    def clear(self):
        """
        Remove all information about tokens and views.
        """
        self.tokens = []
        self.text_view = None
        self.ccs_view = None

    def __str__(self):
        if self.text_view is not None:
            return self.text_view.string(flat=True, clean=True)
        if self.ccs_view is not None:
            return self.ccs_view.string()
        if self.has_raw:
            return self.raw_flat_clean_string
        return None

    @property
    def raw_string(self):
        if self.has_raw:
            return self.raw.string(eol=u"", eos=u"")
        return None

    @property
    def raw_flat_clean_string(self):
        if self.has_raw:
            s = self.raw.string(raw=True, flat=True, clean=True)
            s = re.sub(u"\n", u" ", s)
            s = re.sub(r" [ ]*", u" ", s)
            return s
        return None

    @property
    def has_raw(self):
        """
        Return ``True`` if this object has been created from a raw object.
        """
        return self.raw is not None

    @property
    def sentences(self):
        if self.text_view is None:
            return []
        return self.text_view.elements

    @property
    def ccs(self):
        if self.ccs_view is None:
            return []
        return self.ccs_view.elements
