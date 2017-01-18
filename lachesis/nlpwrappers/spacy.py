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

from lachesis.elements import Sentence
from lachesis.elements import Token
from lachesis.language import Language
from lachesis.nlpwrappers.base import BaseWrapper


class SpacyWrapper(BaseWrapper):
    """
    TBW
    """

    CODE = u"spacy"

    MODEL_FILES_DIRECTORY_PATH = os.path.expanduser("~/spacy_data")

    LANGUAGE_TO_SPACY_CODE = {
        Language.ENGLISH: u"en",
        # Language.GERMAN: u"de",
    }

    LANGUAGES = LANGUAGE_TO_SPACY_CODE.keys()

    def __init__(self, language, model_file_path=None):
        super(SpacyWrapper, self).__init__(language)
        import spacy
        if model_file_path is None:
            model_file_path = self.MODEL_FILES_DIRECTORY_PATH
        try:
            self.nlp = spacy.load(self.LANGUAGE_TO_SPACY_CODE[self.language], path=model_file_path)
        except RuntimeError:
            raise ValueError(u"Unable to load model from file path '%s'. Please specify a valid path with the 'model_file_path' parameter." % model_file_path)

    def _analyze(self, text):
        doc = self.nlp(text.as_string)
        for sentence in doc.sents:
            my_sentence = Sentence(raw_string=sentence.text)
            for word in sentence:
                my_token = Token(
                    raw_string=word.text,
                    upostag=word.pos_,
                    chunktag=None,
                    pnptag=None
                )
                my_sentence.append_token(my_token)
            text.append_sentence(my_sentence)
        self._fix_sentence_raw_strings(text)
