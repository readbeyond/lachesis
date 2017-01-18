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

from lachesis.elements import ClosedCaption as CC
from lachesis.elements import Sentence
from lachesis.elements import Token
from lachesis.language import Language
from lachesis.splitters.base import BaseSplitter


class GreedySplitter(BaseSplitter):
    """
    TBW
    """

    CODE = u"greedy"

    LANGUAGES = Language.ALL_LANGUAGES

    TOKENIZER_NLP_TOKENS = 0
    TOKENIZER_WHITESPACE = 1

    def __init__(
        self,
        language,
        max_chars_per_line=BaseSplitter.MAX_CHARS_PER_LINE,
        max_num_lines=BaseSplitter.MAX_NUM_LINES,
        tokenizer=TOKENIZER_NLP_TOKENS
    ):
        super(GreedySplitter, self).__init__(language, max_chars_per_line, max_num_lines)
        self.tokenizer = tokenizer

    def _tokenize(self, sentence):
        if self.tokenizer == self.TOKENIZER_NLP_TOKENS:
            return [t.augmented_string for t in sentence.tokens]
        if self.tokenizer == self.TOKENIZER_WHITESPACE:
            # TODO is there a better way of doing this?
            l = [s + " " for s in sentence.raw_string.split(u" ")]
            l[-1] = l[-1].strip()
            return l
        raise ValueError(u"Unknown tokenizer '%s'" % str(self.tokenizer))

    def _is_other(self, sentence):
        raw = sentence.raw_string
        if (
            (len(raw) >= 2) and
            (len(raw) < self.max_chars_per_line) and
            (
                ((raw[0] == u"(") and (raw[-1] == u")")) or
                ((raw[0] == u"[") and (raw[-1] == u"]")) or
                ((raw[0] == u"{") and (raw[-1] == u"}"))
            )
        ):
            return True
        return False


    def _split_sentence(self, sentence):
        # check for e.g. "(applause)" or similar "OTHER" fragments
        if self._is_other(sentence):
            return [CC(kind=CC.OTHER, lines=[sentence.raw_string])]

        # otherwise, process it
        ccs = []
        lines = []
        current_line = u""
        tokens = self._tokenize(sentence)
        for token in tokens:
            if len(current_line) + len(token) > self.max_chars_per_line:
                # "close" current line
                lines.append(current_line)
                if len(lines) == self.max_num_lines:
                    # "close" current cc
                    ccs.append(CC(kind=CC.REGULAR, lines=lines))
                    lines = []
                # create a new line
                current_line = token
            else:
                # append to current line
                current_line += token
        # append last line and close cc
        lines.append(current_line)
        ccs.append(CC(kind=CC.REGULAR, lines=lines))
        return ccs
