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
from lachesis.upostags import UniversalPOSTags


class PatternWrapper(BaseWrapper):
    """
    TBW
    """

    LANGUAGES = [
        Language.DUTCH,
        Language.ENGLISH,
        Language.FRENCH,
        Language.GERMAN,
        Language.ITALIAN,
        Language.SPANISH,
    ]

    UPOSTAG_MAP = {
        u"NN": UniversalPOSTags.NOUN,
        u"VB": UniversalPOSTags.VERB,
        u"JJ": UniversalPOSTags.ADJ,
        u"RB": UniversalPOSTags.ADV,
        u"PR": UniversalPOSTags.PRON,
        u"DT": UniversalPOSTags.DET,
        u"PP": UniversalPOSTags.ADP,
        u"NO": UniversalPOSTags.NUM,
        u"CJ": UniversalPOSTags.CCONJ,
        u"UH": UniversalPOSTags.INTJ,
        u"PT": UniversalPOSTags.PART,
        u".": UniversalPOSTags.PUNCT,
        u"X": UniversalPOSTags.X,
    }

    def __init__(self, language):
        super(PatternWrapper, self).__init__(language)
        if language == Language.ENGLISH:
            from pattern.en import parse as func_parse
            from pattern.en import split as func_split
        elif language == Language.ITALIAN:
            from pattern.it import parse as func_parse
            from pattern.it import split as func_split
        elif language == Language.SPANISH:
            from pattern.es import parse as func_parse
            from pattern.es import split as func_split
        elif language == Language.FRENCH:
            from pattern.fr import parse as func_parse
            from pattern.fr import split as func_split
        elif language == Language.GERMAN:
            from pattern.de import parse as func_parse
            from pattern.de import split as func_split
        elif language == Language.DUTCH:
            from pattern.nl import parse as func_parse
            from pattern.nl import split as func_split
        else:
            raise ValueError(u"No pattern submodule for the given language '%s'." % language)
        self.func_parse = func_parse
        self.func_split = func_split

        #
        # From the docs:
        # http://www.clips.ua.ac.be/pages/pattern-en#parser
        #
        # The output of parse() is a subclass of unicode called TaggedString
        # whose TaggedString.split() method by default yields a list of sentences,
        # where each sentence is a list of tokens,
        # where each token is a list of the word + its tags.
        #
        # parse(string,
        #   tokenize = True,        # Split punctuation marks from words?
        #   tags = True,            # Parse part-of-speech tags? (NN, JJ, ...)
        #   chunks = True,          # Parse chunks? (NP, VP, PNP, ...)
        #   relations = False,      # Parse chunk relations? (-SBJ, -OBJ, ...)
        #   lemmata = False,        # Parse lemmata? (ate => eat)
        #   encoding = 'utf-8'      # Input string encoding.
        #   tagset = None)          # Penn Treebank II (default) or UNIVERSAL.
        #

    def _analyze(self, text):
        tagged_string = self.func_parse(
            text.as_string,
            tokenize=True,
            tags=True,
            chunks=True,
            relations=False,
            lemmata=False,
            tagset="universal"
        )
        for sentence in self.func_split(tagged_string):
            my_sentence = Sentence(raw_string=sentence.string)
            for token in sentence:
                raw_string, upostag, chunktag, pnptag = token.tags
                my_token = Token(
                    raw_string=raw_string,
                    upostag=self.UPOSTAG_MAP[upostag],
                    chunktag=chunktag,
                    pnptag=pnptag
                )
                my_sentence.append_token(my_token)
            text.append_sentence(my_sentence)
        self._fix_sentence_raw_strings(text)
