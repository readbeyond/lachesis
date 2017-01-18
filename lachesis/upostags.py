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

From http://universaldependencies.org/u/pos/
"""


class UniversalPOSTags(object):
    """
    TBW
    """

    # TODO better versioning of the tags?

    ADJ = u"ADJ"        # v1, v2
    ADP = u"ADP"        # v1, v2
    ADV = u"ADV"        # v1, v2
    AUX = u"AUX"        # v2
    CCONJ = u"CCONJ"    # v2, specifier of CONJ
    CONJ = u"CONJ"      # v1
    DET = u"DET"        # v1, v2
    INTJ = u"INTJ"      # v2
    NOUN = u"NOUN"      # v1, v2
    NUM = u"NUM"        # v1, v2
    PART = u"PART"      # v2
    PART_1 = u"PRT"     # v1, "PART" in v2
    PRON = u"PRON"      # v1, v2
    PROPN = u"PROPN"    # v2
    PUNCT = u"PUNCT"    # v2
    PUNCT_1 = u"."      # v1, "PUNCT" in v2
    SCONJ = u"SCONJ"    # v2, specifier of CONJ
    SYM = u"SYM"        # v2
    VERB = u"VERB"      # v1, v2
    X = u"X"            # v1, v2

    HUMAN_READABLE_NAMES = {
        ADJ: "adjective",
        ADP: "adposition",
        ADV: "adverb",
        AUX: "auxiliary",
        CCONJ: "coordinating conjunction",
        CONJ: "conjunction",
        DET: "determiner",
        INTJ: "interjection",
        NOUN: "noun",
        NUM: "numeral",
        PART: "particle",
        PART_1: "particle",
        PRON: "pronoun",
        PROPN: "proper noun",
        PUNCT: "punctuation",
        PUNCT_1: "punctuation",
        SCONJ: "subordinating conjunction",
        SYM: "symbol",
        VERB: "verb",
        X: "other",
    }

    UPOSTAG_MAP_V1_TO_V2 = {
        ADJ: ADJ,
        ADP: ADP,
        ADV: ADV,
        AUX: AUX,
        CCONJ: CCONJ,
        CONJ: CCONJ,
        DET: DET,
        INTJ: INTJ,
        NOUN: NOUN,
        NUM: NUM,
        PART: PART,
        PART_1: PART,
        PRON: PRON,
        PROPN: PROPN,
        PUNCT: PUNCT,
        PUNCT_1: PUNCT,
        SCONJ: SCONJ,
        SYM: SYM,
        VERB: VERB,
        X: X,
    }
