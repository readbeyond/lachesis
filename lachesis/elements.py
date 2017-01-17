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
import attr
import os

import lachesis.globalfunctions as gf


class Text(object):
    """
    TBW

    A Text is basically a list of sentences.
    Everything is a Unicode string
    (``unicode`` in PY2, ``str`` in PY3)
    internally.

    Parameter ``obj`` can be:

    * a ``string`` (to be segmented into sentences);
    * a ``list`` of ``string`` (each being a sentence);
    * a ``file`` or ``io.TextIOWrapper`` object
      or a path to an existing file (text will be read from it)
    """
    def __init__(self, obj, encoding="utf-8", is_segmented=False):
        # raw_string is the text as a single Unicode string
        self.raw_string = None
        # raw_sentence_strings is the text as a list of Unicode strings,
        # one per sentence
        self.raw_sentence_strings = None
        # sentence_objects is a list of (parsed) Sentence objects
        self.sentence_objects = []
        if gf.is_list_of_unicode(obj):
            # store list of sentence strings
            self.raw_sentence_strings = obj
        elif gf.is_file(obj):
            # read contents from the given file object
            self.read_from_file_obj(obj, is_segmented)
        elif gf.is_unicode(obj):
            if os.path.exists(obj):
                # open file, read contents, and close it
                self.read_from_file_path(obj, encoding, is_segmented)
            else:
                # store string
                self.raw_string = obj
        else:
            raise TypeError(u"Unknown type for paramenter 'obj'")

    @property
    def sentences(self):
        """
        TBW

        The list of parsed Sentence objects
        """
        return self.sentence_objects

    @property
    def is_string(self):
        """
        TBW

        Return ``True`` if this Text has been created
        from a single Unicode string, or ``False``
        if it has been created from a list of sentences.
        """
        return self.raw_string is not None

    @property
    def as_string(self):
        """
        TBW

        The text as a single Unicode string.
        """
        if self.is_string:
            return self.raw_string
        return u" ".join(self.raw_sentence_strings)

    @property
    def as_sentences(self):
        """
        TBW

        The text, as a list of sentence strings.
        """
        if not self.is_string:
            return self.raw_sentence_strings
        if len(self.sentences) > 0:
            return [s.raw_string for s in self.sentences]
        raise ValueError(u"This Text object was given as a single Unicode string but it has not been parsed yet.")

    def read_from_file_obj(self, file_obj, is_segmented=False):
        """
        TBW

        Read text from the given file object.
        """
        if not gf.is_file(file_obj):
            raise TypeError(u"The given 'file_obj' parameter is not a file")
        if is_segmented:
            self.raw_sentence_strings = [l.decode(encoding).strip() for l in file_obj.readlines()]
        else:
            self.raw_string = file_obj.read().decode(encoding)

    def read_from_file_path(self, file_path, encoding, is_segmented):
        """
        TBW

        Read text from the given file path.
        """
        if not is_unicode(file_path):
            raise TypeError(u"The given 'file_path' parameter is not a Unicode string")
        if not os.path.exists(file_path):
            raise IOError(u"The given path does not exist")
        with io.open(file_path, "r", encoding=encoding) as f:
            if is_segmented:
                self.raw_sentence_strings = [l.strip() for l in f.readlines()]
            else:
                self.raw_string = f.read()

    def clear(self):
        """
        TBW
        """
        self.sentence_objects = []

    def append_sentence(self, sentence):
        """
        TBW
        """
        self.sentence_objects.append(sentence)

    def merge(self):
        """
        TBW

        Merge all sentences in this Text into a single Sentence,
        and store it.
        """
        raw_string = u" ".join([s.raw_string for s in self.sentences])
        merged = Sentence(raw_string=raw_string)
        for sentence in self.sentences:
            for token in sentence.tokens:
                merged.append_token(token)
        self.sentence_objects = [merged]


@attr.s
class Sentence(object):
    """
    A Sentence is basically a list of Tokens.
    """
    raw_string = attr.ib()
    tokens = attr.ib(default=attr.Factory(list), repr=False)

    @property
    def tagged_string(self):
        """
        TBW
        """
        return u" ".join([t.tagged_string for t in self.tokens])

    def __str__(self):
        return self.raw_string

    def append_token(self, token):
        """
        TBW
        """
        self.tokens.append(token)


@attr.s
class Token(object):
    """
    A Token is a part of speech.
    """
    raw_string = attr.ib()
    upostag = attr.ib(default=None)
    chunktag = attr.ib(default=None, repr=False)
    pnptag = attr.ib(default=None, repr=False)
    lemma = attr.ib(default=None, repr=False)

    def __str__(self):
        return self.raw_string

    @property
    def tagged_string(self):
        """
        TBW
        """
        return u"%s/%s" % (self.raw_string, self.upostag)


@attr.s
class ClosedCaptionList(object):
    """
    A ClosedCaptionList represents a list of ClosedCaption objects.
    """

    language = attr.ib(default=None)
    cc_objects = attr.ib(default=attr.Factory(list), repr=False)

    def __len__(self):
        return len(self.cc_objects)

    def __str__(self):
        return u"\n".join([str(cc) for cc in self.cc_objects])

    def append_cc(self, cc):
        """
        TBW
        """
        self.cc_objects.append(cc)


@attr.s
class ClosedCaption(object):
    """
    A ClosedCaption represents a closed caption,
    that is, a time interval and a list of lines.
    """

    REGULAR = 0
    HEAD = 1
    TAIL = 2
    NONSPEECH = 3
    OTHER = 4

    kind = attr.ib()
    interval = attr.ib(default=None)
    lines = attr.ib(default=attr.Factory(list), repr=False)

    @property
    def has_time(self):
        """
        TBW
        """
        return self.interval is not None

    def __str__(self):
        return u" | ".join(self.lines)
