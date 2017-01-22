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


class Token(object):
    """
    A Token is a word or punctuation in a Document.
    """

    def __init__(
        self,
        raw,
        upos_tag=None,
        chunk_tag=None,
        pnp_tag=None,
        lemma=None,
        trailing_whitespace=False,
        end_of_sentence=False
    ):
        self.raw = raw
        self.upos_tag = upos_tag
        self.chunk_tag = chunk_tag
        self.pnp_tag = pnp_tag
        self.lemma = lemma
        self.trailing_whitespace = trailing_whitespace
        self.end_of_sentence = end_of_sentence

    def __str__(self):
        return self.tagged_string

    @property
    def augmented_string(self):
        """
        Return a string representation of the token,
        including a trailing whitespace
        (if the corresponding flag is set).
        """
        if self.trailing_whitespace:
            return self.raw + u" "
        return self.raw

    @property
    def string(self):
        """
        Return a string representation of the token.
        It currently returns the augmented string.
        """
        return self.augmented_string

    @property
    def tagged_string(self):
        """
        Return a tagged representation of the token,
        in the form ``STRING/UPOS/C``, where:

        * STRING is the token string,
        * UPOS is the Universal POS of the token,
        * C is "+" if the token has a trailing whitespace, "-" if it does not,
          or "=" if the token is the last token of a sentence
        """
        ws = u"-"
        if self.trailing_whitespace:
            ws = u"+"
        if self.end_of_sentence:
            ws = u"="
        return u"%s/%s/%s " % (self.raw, self.upos_tag, ws)


class LineToken(Token):

    def __init__(self):
        self.raw = u" |||"
        self.upos_tag = u"ZZZ"
        self.chunk_tag = None
        self.pnp_tag = None
        self.lemma = None
        self.trailing_whitespace = True
        self.end_of_sentence = False
