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

from lachesis.elements import Document
from lachesis.elements import Span
from lachesis.language import Language
from lachesis.nlpwrappers.upostags import UniversalPOSTags
import lachesis.globalfunctions as gf


class BaseWrapper(object):
    """
    TBW

    A wrapper for an NLP library.
    """

    CODE = u"base"

    LANGUAGES = []
    """ The languages supported by this NLP library """

    UPOSTAG_MAP = UniversalPOSTags.UPOSTAG_MAP_V1_TO_V2
    """ Maps the POS tags returned by this NLP library to Universal POS Tags (v2) """

    def __init__(self, language):
        lfc = Language.from_code(language)
        if (lfc is not None) and (lfc in self.LANGUAGES):
            self.language = lfc
            return self
        if language in self.LANGUAGES:
            self.language = language
            return self
        raise ValueError(u"This NLP library does not support the '%s' language" % language)

    def analyze(self, document):
        """
        Analyze the given document, splitting it into sentences
        and tagging the tokens (words) with Universal POS tags.
        Some NLP libraries (e.g., ``pattern``)
        also performs chunking at this stage.

        The information output (sentences, token tags, etc.)
        will be stored inside the given ``document`` object.
        """
        if document.raw_flat_string is None:
            raise ValueError(u"The document has no text set.")
        if (document.language is not None) and (document.language != self.language):
            # TODO warning instead?
            raise ValueError(u"The document has been created with the '%s' language set while this NLP library has loaded the '%s' language." % (document.language, self.language))

        # remove any information from the document
        document.clear()

        # do the actual analysis
        document.text_view = Span(raw=document.raw_flat_string)
        sentences = self._analyze(document)
        for raw, tokens in sentences:
            sentence = Span(raw=raw)
            for token in tokens:
                document.tokens.append(token)
                sentence.append(token)
            sentence.elements[-1].end_of_sentence = True
            document.text_view.append(sentence)
        document._set_token_whitespace()

    def _analyze(self, document):
        """
        This is the actual function running
        the tokenizer and tagger over given Document object.
        """
        raise NotImplementedError(u"This method should be implemented in a subclass.")
