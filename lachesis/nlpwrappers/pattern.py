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
from lachesis.nlpwrappers.upostags import UniversalPOSTags


class PatternWrapper(BaseWrapper):
    """
    TBW
    """

    CODE = u"pattern"

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
        u"NN-LOC": UniversalPOSTags.NOUN,
        u"NN-ORG": UniversalPOSTags.NOUN,
        u"NN-PERS": UniversalPOSTags.NOUN,
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
        if self.language == Language.ENGLISH:
            from pattern.en import parse as func_parse
            from pattern.en import split as func_split
        elif self.language == Language.ITALIAN:
            from pattern.it import parse as func_parse
            from pattern.it import split as func_split
        elif self.language == Language.SPANISH:
            from pattern.es import parse as func_parse
            from pattern.es import split as func_split
        elif self.language == Language.FRENCH:
            from pattern.fr import parse as func_parse
            from pattern.fr import split as func_split
        elif self.language == Language.GERMAN:
            from pattern.de import parse as func_parse
            from pattern.de import split as func_split
        elif self.language == Language.DUTCH:
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

    def _analyze(self, document):
        sentences = []
        tagged_string = self.func_parse(
            document.raw_flat_string,
            tokenize=True,
            tags=True,
            chunks=False,
            relations=False,
            lemmata=False,
            tagset="universal"
        )
        for lib_sentence in self.func_split(tagged_string):
            sentence_tokens = []
            for lib_token in lib_sentence:
                #
                # NOTE: if chunks=True use:
                # raw, upos_tag, chunk_tag, pnp_tag = lib_token.tags
                # token = Token(
                #     raw=raw,
                #     upos_tag=self.UPOSTAG_MAP[upos_tag],
                #     chunk_tag=chunk_tag,
                #     pnp_tag=pnp_tag
                # )
                #
                raw, upos_tag = lib_token.tags
                # NOTE: pattern replaces "/" with "&slash;"
                #       so we need to convert it back
                raw = raw.replace(u"&slash;", u"/")
                token = Token(raw=raw, upos_tag=self.UPOSTAG_MAP[upos_tag])
                sentence_tokens.append(token)
            sentences.append((lib_sentence.string, sentence_tokens))
        return sentences
