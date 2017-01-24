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
from lachesis.splitters.base import BaseSplitter


class GreedySplitter(BaseSplitter):
    """
    TBW
    """

    CODE = u"greedy"

    LANGUAGES = Language.ALL_LANGUAGES

    def _split_sentence(self, sentence_span):
        # check for e.g. "(applause)" or similar OTHER fragments
        if self._is_cc_other(sentence_span):
            line = Span(elements=sentence_span.elements)
            cc = Span(elements=[line])
            return [cc]

        # otherwise, process it
        ccs = []
        line_spans = []
        current_line_span = Span()
        for g_tokens, g_len in self._group_tokens(sentence_span.elements):
            c_len = len(current_line_span.string(raw=True))
            if c_len + g_len > self.max_chars_per_line:
                # close current line and open a new one
                line_spans.append(current_line_span)
                if len(line_spans) == self.max_num_lines:
                    # close current cc and open a new one
                    ccs.append(Span(elements=line_spans))
                    line_spans = []
                # create a new line
                current_line_span = Span()
            # append to current line
            current_line_span.extend(g_tokens)
        # append last line and close cc
        line_spans.append(current_line_span)
        ccs.append(Span(elements=line_spans))
        return ccs
