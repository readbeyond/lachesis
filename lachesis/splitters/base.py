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
from lachesis.language import Language


class BaseSplitter(object):
    """
    TBW

    A splitter, that is, a class that takes a Text object
    and splits it into a Span.
    """

    CODE = u"base"

    LANGUAGES = []
    """ The languages supported by this splitter """

    MAX_CHARS_PER_LINE = 42
    """ Maximum number of characters per CC line. Set to -1 to ignore. """

    MAX_NUM_LINES = 2
    """ Maximum number of CC lines. Set to -1 to ignore. """

    def __init__(self, language, max_chars_per_line=MAX_CHARS_PER_LINE, max_num_lines=MAX_NUM_LINES):
        self.max_chars_per_line = max_chars_per_line
        self.max_num_lines = max_num_lines
        lfc = Language.from_code(language)
        if (lfc is not None) and (lfc in self.LANGUAGES):
            self.language = lfc
            return
        if language in self.LANGUAGES:
            self.language = language
            return
        raise ValueError(u"This splitter does not support the '%s' language" % language)

    def _is_cc_other(self, sentence_span):
        """
        TBW

        Return ``True`` if the given sentence bears text that can be labeled
        as "other" (like "(applause)", "(music)", etc.);
        return ``False`` otherwise.
        Currently, this function just checks if the the sentence
        is on a single line and if it is "(...)", "[...]", or "{...}".
        """
        # TODO allow the user to specify her own "other" rules
        string = sentence_span.string(raw=True)
        if (
            (string is not None) and
            (len(string) >= 2) and
            (len(string) < self.max_chars_per_line) and
            (
                ((string[0] == u"(") and (string[-1] == u")")) or
                ((string[0] == u"[") and (string[-1] == u"]")) or
                ((string[0] == u"{") and (string[-1] == u"}"))
            )
        ):
            return True
        return False

    def _group_tokens(self, tokens):
        """
        Given a list of Token objects ``tokens``,
        return a list of list, each inner list being one or more tokens,
        such that only the last token of each group might not have a trailing whitespace.

        "For example let's say: Hello, World!" => [["For"], ["example"], ["let's"], ["say", ":"], ["Hello", ","], ["World", "!"]]
        """
        grouped_tokens = []
        current_group = []
        for token in [t for t in tokens if t.is_regular]:
            if token.trailing_whitespace:
                current_group.append(token)
                grouped_tokens.append(current_group)
                current_group = []
            else:
                current_group.append(token)
        if len(current_group) > 0:
            grouped_tokens.append(current_group)
        return [(l, sum([len(ll.raw) for ll in l])) for l in grouped_tokens]

    def _split_sentence(self, sentence_span):
        """
        TBW

        This is the actual function running
        the splitter over the given Sentence object.
        """
        raise NotImplementedError(u"This method should be implemented in a subclass.")

    def split(self, document):
        """
        TBW
        """
        ccs_view = Span()
        for sentence_span in document.sentences:
            ccs = self._split_sentence(sentence_span)
            ccs_view.extend(ccs)
        document.ccs_view = ccs_view
