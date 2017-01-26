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
import os

from lachesis.elements import Span
from lachesis.elements import Token
from lachesis.language import Language
from lachesis.ml import CRFPredictor
from lachesis.ml import CRFTrainer
from lachesis.splitters.base import BaseSplitter


class CRFSplitter(BaseSplitter):
    """
    TBW
    """

    CODE = u"crf"

    CHECK_LANGUAGE = False

    MODEL_FILES_DIRECTORY_PATH = os.path.join(
        os.path.expanduser("~/"),
        "lachesis_data",
        "crf_data"
    )

    LANGUAGE_TO_MODEL_FILE = {
        Language.ENGLISH: [(u"eng.42.5.pattern.crfsuite", 42, 5, u"pattern")],
        Language.ITALIAN: [(u"ita.42.5.pattern.crfsuite", 42, 5, u"pattern")],
    }

    LANGUAGES = LANGUAGE_TO_MODEL_FILE.keys()

    def __init__(self, language, max_chars_per_line=BaseSplitter.MAX_CHARS_PER_LINE, max_num_lines=BaseSplitter.MAX_NUM_LINES, model_file_path=None):
        super(CRFSplitter, self).__init__(language, max_chars_per_line, max_num_lines)
        self.model_file_path = model_file_path
        if self.model_file_path is None:
            # first, check the language
            self._check_language()
            # then, find the path of the model file
            # best matching the splitter parameters
            # TODO currently serving only the first model
            mfp = ((self.LANGUAGE_TO_MODEL_FILE[self.language])[0])[0]
            self.model_file_path = os.path.join(self.MODEL_FILES_DIRECTORY_PATH, mfp)
        if not os.path.isfile(self.model_file_path):
            raise ValueError(u"Unable to load CRF model '%s'. Please download the file in that path, or provide your own path with the model_file_path parameter." % self.model_file_path)

    def _split_sentence(self, sentence_span):

        def _select_best_split(candidates):
            #
            # each candidate tuple is: (begin_idx, end_idx, labels, probability)
            #
            # first, sort by the label of the last token
            # to put the candidates with LABEL_LAST first
            candidates = sorted(candidates, key=lambda x: (1 if x[2][-1] == CRFTrainer.LABEL_LAST else 0), reverse=True)
            # then, sort by probability and end index
            # to put most probable and most long candidates first
            candidates = sorted(candidates, key=lambda x: (x[3], x[1]), reverse=True)
            # print(u"Sorted: %s" % str(candidates))
            return candidates[0]

        # check for e.g. "(applause)" or similar OTHER fragments
        if self._is_cc_other(sentence_span):
            line = Span(elements=sentence_span.elements)
            cc = Span(elements=[line])
            return [cc]

        # otherwise, process it
        tokens = [t for t in sentence_span.elements if t.is_regular]
        clean_sentence_span = Span(elements=tokens)

        # if the tokens fit into a single line,
        # create a CC with one line and return it
        if len(clean_sentence_span.string()) <= self.max_chars_per_line:
            return [Span(elements=[clean_sentence_span])]

        # we actually need to create more than one line
        # load the CRF model
        predictor = CRFPredictor(self.model_file_path)
        n = len(tokens)
        ccs = []
        line_spans = []
        current_line_span = Span()
        candidates = []
        current_line_start_idx = 0
        idx = 0
        while idx < n:
            # checking if the current sublist of tokens fits in one line
            current_line_span = Span(elements=tokens[current_line_start_idx:idx+1])
            aug_s = current_line_span.string().strip()
            if len(aug_s) <= self.max_chars_per_line:
                # yes, label the current sublist of tokens
                p_labels, p_probability = predictor.predict(current_line_span)
                candidate = (current_line_start_idx, idx + 1, p_labels, p_probability)
                # print(u"  New candidate: %s" % str(candidate))
                candidates.append(candidate)
            else:
                # no, the current sublist would be too long
                # select best split among the candidates seen so far
                chosen = _select_best_split(candidates)
                # print(u"Chosen candidate: %s" % str(chosen))
                chosen_line = Span(elements=tokens[chosen[0]:chosen[1]])
                line_spans.append(chosen_line)
                if len(line_spans) >= self.max_num_lines:
                    # we fill the cc, add it
                    ccs.append(Span(elements=line_spans))
                    line_spans = []
                # reset
                candidates = []
                current_line_span = Span()
                current_line_start_idx = chosen[1]
                idx = chosen[1]
            idx += 1

        if current_line_start_idx < n:
            # we need to add the end of the sentence
            line_spans.append(Span(elements=tokens[current_line_start_idx:]))
            ccs.append(Span(elements=line_spans))

        return ccs
