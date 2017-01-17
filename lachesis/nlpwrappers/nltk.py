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

    def _analyze(self, text):
        sentences = self.sent_tokenize(text.as_string, language=self.nltk_language)
        for sentence in sentences:
            my_sentence = Sentence(raw_string=sentence)
            tokens = self.word_tokenize(sentence, language=self.nltk_language)
            tagged_tokens = self.pos_tag(tokens, tagset="universal")
            for rs, pos in tagged_tokens:
                my_token = Token(
                    raw_string=rs,
                    upostag=self.UPOSTAG_MAP[pos],
                )
                my_sentence.append_token(my_token)
            text.append_sentence(my_sentence)
        self._fix_sentence_raw_strings(text)
