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

from lachesis.elements import Span
from lachesis.elements import Token
from lachesis.language import Language
from lachesis.nlpwrappers.base import BaseWrapper


class NLTKWrapper(BaseWrapper):
    """
    TBW
    """

    CODE = u"nltk"

    LANGUAGE_TO_NLTK_FILE = {
        Language.CZECH: u"czech",
        Language.DANISH: u"danish",
        Language.DUTCH: u"dutch",
        Language.ENGLISH: u"english",
        Language.ESTONIAN: u"estonian",
        Language.FINNISH: u"finnish",
        Language.FRENCH: u"french",
        Language.GERMAN: u"german",
        Language.GREEK: u"greek",
        Language.ITALIAN: u"italian",
        Language.NORWEGIAN: u"norwegian",
        Language.POLISH: u"polish",
        Language.PORTUGUESE: u"portuguese",
        Language.SLOVENIAN: u"slovene",
        Language.SPANISH: u"spanish",
        Language.SWEDISH: u"swedish",
        Language.TURKISH: u"turkish",
    }

    LANGUAGES = LANGUAGE_TO_NLTK_FILE.keys()

    def __init__(self, language):
        super(NLTKWrapper, self).__init__(language)
        self.nltk_language = self.LANGUAGE_TO_NLTK_FILE[self.language]
        import nltk
        self.tokenizer = nltk.data.load("tokenizers/punkt/%s.pickle" % self.nltk_language)
        from nltk.tokenize import sent_tokenize
        from nltk.tokenize import word_tokenize
        from nltk import pos_tag
        self.sent_tokenize = sent_tokenize
        self.word_tokenize = word_tokenize
        self.pos_tag = pos_tag

    def _analyze(self, document):
        sentences = []
        lib_sentences = self.sent_tokenize(document.raw_flat_string, language=self.nltk_language)
        for lib_sentence in lib_sentences:
            sentence_tokens = []
            lib_tokens = self.word_tokenize(lib_sentence, language=self.nltk_language)
            tagged_tokens = self.pos_tag(lib_tokens, tagset="universal")
            for lib_token in tagged_tokens:
                raw, upos_tag = lib_token
                token = Token(raw=raw, upos_tag=self.UPOSTAG_MAP[upos_tag])
                sentence_tokens.append(token)
            sentences.append((lib_sentence, sentence_tokens))
        return sentences
