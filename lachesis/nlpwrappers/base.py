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

from lachesis.elements import Sentence
from lachesis.elements import Text
from lachesis.elements import Token
from lachesis.upostags import UniversalPOSTags
import lachesis.globalfunctions as gf


class BaseWrapper(object):
    """
    TBW

    A wrapper for an NLP library.
    """

    LANGUAGES = []
    """ The languages supported by this NLP library """

    UPOSTAG_MAP = UniversalPOSTags.UPOSTAG_MAP_V1_TO_V2
    """ Maps the POS tags returned by this NLP library to Universal POS Tags (v2) """

    def __init__(self, language):
        if language not in self.LANGUAGES:
            raise ValueError(u"This NLP library does not support the '%s' language" % language)
        self.language = language

    def analyze(self, text):
        """
        TBW

        Analyze the given text, splitting it into sentences
        and tagging the tokens (words) with Universal POS tags.
        Some NLP libraries (e.g., ``pattern``)
        also performs chunking at this stage.

        The information output (sentences, token tags, etc.)
        will be stored inside the given ``text`` object.
        """
        text.clear()
        if text.is_string:
            self._analyze(text)
        else:
            for sentence_string in text.as_sentences:
                sentence_text_object = Text(sentence_string)
                self._analyze(sentence_text_object)
                sentence_text_object.merge()
                text.append_sentence(sentence_text_object.sentences[0])
        return text

    def _analyze(self, text):
        """
        TBW

        This is the actual function running
        the tokenizer and tagger over given Text object.
        """
        raise NotImplementedError(u"This method should be implemented in the subclasses.")

    @classmethod
    def _fix_sentence_raw_strings(cls, text):
        """
        TBW

        Fix the raw string of each sentence in the given text,
        to match the actual text string.
        This method will remove e.g. spaces before or after punctuation
        introduced by the NLP parser.
        """
        last_idx = 0
        current_idx = 0
        text_string = text.as_string
        for sentence in text.sentences:
            acc = u""
            for token in sentence.tokens:
                token_string = token.raw_string
                current_idx = text_string.find(token_string, last_idx) + len(token_string)
                acc += text_string[last_idx:current_idx]
                last_idx = current_idx
            sentence.raw_string = acc.strip()
