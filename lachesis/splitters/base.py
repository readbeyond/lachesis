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

from lachesis.elements import ClosedCaptionList
from lachesis.language import Language


class BaseSplitter(object):
    """
    TBW

    A splitter, that is, a class that takes a Text object
    and splits it into a ClosedCaptionList.
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

    def _is_cc_other(self, sentence):
        """
        TBW

        Return ``True`` if the given sentence bears text that can be labeled
        as "other" (like "(applause)", "(music)", etc.);
        return ``False`` otherwise.
        Currently, this function just checks if the the sentence
        is on a single line and if it is "(...)", "[...]", or "{...}".
        """
        # TODO allow the user to specify her own "other" rules
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
        """
        TBW

        This is the actual function running
        the splitter over the given Sentence object.
        """
        raise NotImplementedError(u"This method should be implemented in a subclass.")

    def split(self, text):
        """
        TBW
        """
        ccl = ClosedCaptionList(language=text.language)
        for ts in text.sentences:
            ccs = self._split_sentence(ts)
            ccl.extend_ccs(ccs)
        return ccl
