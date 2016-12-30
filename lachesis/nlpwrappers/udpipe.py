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
from lachesis.nlpwrappers.base import BaseWrapper


class UDPipeWrapper(BaseWrapper):
    """
    TBW
    """

    # TODO change this to point to a directory inside the user $HOME
    MODEL_FILES_DIRECTORY_PATH = "/data/nlp/udpipe_models/"

    LANGUAGE_TO_MODEL_FILE = {
        u"eng": u"english-ud-1.2-160523.udpipe",
        u"ita": u"italian-ud-1.2-160523.udpipe",

        # TODO
        # ancient-greek-proiel-ud-1.2-160523.udpipe
        # ancient-greek-ud-1.2-160523.udpipe
        # arabic-ud-1.2-160523.udpipe
        # basque-ud-1.2-160523.udpipe
        # bulgarian-ud-1.2-160523.udpipe
        # croatian-ud-1.2-160523.udpipe
        # czech-ud-1.2-160523.udpipe
        # danish-ud-1.2-160523.udpipe
        # dutch-ud-1.2-160523.udpipe
        # english-ud-1.2-160523.udpipe
        # estonian-ud-1.2-160523.udpipe
        # finnish-ftb-ud-1.2-160523.udpipe
        # finnish-ud-1.2-160523.udpipe
        # french-ud-1.2-160523.udpipe
        # german-ud-1.2-160523.udpipe
        # gothic-ud-1.2-160523.udpipe
        # greek-ud-1.2-160523.udpipe
        # hebrew-ud-1.2-160523.udpipe
        # hindi-ud-1.2-160523.udpipe
        # hungarian-ud-1.2-160523.udpipe
        # indonesian-ud-1.2-160523.udpipe
        # irish-ud-1.2-160523.udpipe
        # italian-ud-1.2-160523.udpipe
        # latin-itt-ud-1.2-160523.udpipe
        # latin-proiel-ud-1.2-160523.udpipe
        # latin-ud-1.2-160523.udpipe
        # norwegian-ud-1.2-160523.udpipe
        # old-church-slavonic-ud-1.2-160523.udpipe
        # persian-ud-1.2-160523.udpipe
        # polish-ud-1.2-160523.udpipe
        # portuguese-ud-1.2-160523.udpipe
        # romanian-ud-1.2-160523.udpipe
        # slovenian-ud-1.2-160523.udpipe
        # spanish-ud-1.2-160523.udpipe
        # swedish-ud-1.2-160523.udpipe
        # tamil-ud-1.2-160523.udpipe
    }

    LANGUAGES = LANGUAGE_TO_MODEL_FILE.keys()

    def __init__(self, language, model_file_path=None):
        super(UDPipeWrapper, self).__init__(language)
        import ufal.udpipe
        if model_file_path is None:
            model_file_path = os.path.join(
                self.MODEL_FILES_DIRECTORY_PATH,
                self.LANGUAGE_TO_MODEL_FILE[language]
            )
        self.model = ufal.udpipe.Model.load(model_file_path)
        if not self.model:
            raise ValueError(u"Unable to load model from file path '%s'. Please specify a valid path with the 'model_file_path' parameter." % model_file_path)

    def _analyze(self, text):
        import ufal.udpipe
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer.")
        tokenizer.setText(text.as_string)
        error = ufal.udpipe.ProcessingError()
        sentences = []
        sentence = ufal.udpipe.Sentence()
        while tokenizer.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)
        for sentence in sentences:
            self.model.tag(sentence, self.model.DEFAULT)
            self.model.parse(sentence, self.model.DEFAULT)
            useful_tokens = [w for w in sentence.words if w.form != u"<root>"]
            raw_string = u" ".join([w.form for w in useful_tokens])
            my_sentence = Sentence(raw_string=raw_string)
            for token in useful_tokens:
                if token.form != u"<root>":
                    my_token = Token(
                        raw_string=token.form,
                        upostag=self.UPOSTAG_MAP[token.upostag],
                        lemma=token.lemma
                    )
                    my_sentence.append_token(my_token)
            text.append_sentence(my_sentence)
        self._fix_sentence_raw_strings(text)
