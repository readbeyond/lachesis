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
from lachesis.nlpwrappers.base import BaseWrapper


class UDPipeWrapper(BaseWrapper):
    """
    TBW
    """

    CODE = u"udpipe"

    MODEL_FILES_DIRECTORY_PATH = os.path.expanduser("~/udpipe_data")

    LANGUAGE_TO_MODEL_FILE = {
        Language.ITALIAN: u"italian-ud-1.2-160523.udpipe",
        u"ancient-greek-proiel": u"ancient-greek-proiel-ud-1.2-160523.udpipe",
        Language.GREEK_ANCIENT: u"ancient-greek-ud-1.2-160523.udpipe",
        Language.ARABIC: u"arabic-ud-1.2-160523.udpipe",
        Language.BASQUE: u"basque-ud-1.2-160523.udpipe",
        Language.BULGARIAN: u"bulgarian-ud-1.2-160523.udpipe",
        Language.CROATIAN: u"croatian-ud-1.2-160523.udpipe",
        Language.CZECH: u"czech-ud-1.2-160523.udpipe",
        Language.DANISH: u"danish-ud-1.2-160523.udpipe",
        Language.DUTCH: u"dutch-ud-1.2-160523.udpipe",
        Language.ENGLISH: u"english-ud-1.2-160523.udpipe",
        Language.ESTONIAN: u"estonian-ud-1.2-160523.udpipe",
        u"finnish-ftb": u"finnish-ftb-ud-1.2-160523.udpipe",
        Language.FINNISH: u"finnish-ud-1.2-160523.udpipe",
        Language.FRENCH: u"french-ud-1.2-160523.udpipe",
        Language.GERMAN: u"german-ud-1.2-160523.udpipe",
        Language.GOTHIC: u"gothic-ud-1.2-160523.udpipe",
        Language.GREEK: u"greek-ud-1.2-160523.udpipe",
        Language.HEBREW: u"hebrew-ud-1.2-160523.udpipe",
        Language.HINDI: u"hindi-ud-1.2-160523.udpipe",
        Language.HUNGARIAN: u"hungarian-ud-1.2-160523.udpipe",
        Language.INDONESIAN: u"indonesian-ud-1.2-160523.udpipe",
        Language.IRISH: u"irish-ud-1.2-160523.udpipe",
        Language.ITALIAN: u"italian-ud-1.2-160523.udpipe",
        u"latin-itt": u"latin-itt-ud-1.2-160523.udpipe",
        u"latin-proiel": u"latin-proiel-ud-1.2-160523.udpipe",
        Language.LATIN: u"latin-ud-1.2-160523.udpipe",
        Language.NORWEGIAN: u"norwegian-ud-1.2-160523.udpipe",
        Language.OLD_CHURCH_SLAVONIC: u"old-church-slavonic-ud-1.2-160523.udpipe",
        Language.PERSIAN: u"persian-ud-1.2-160523.udpipe",
        Language.POLISH: u"polish-ud-1.2-160523.udpipe",
        Language.PORTUGUESE: u"portuguese-ud-1.2-160523.udpipe",
        Language.ROMANIAN: u"romanian-ud-1.2-160523.udpipe",
        Language.SLOVENIAN: u"slovenian-ud-1.2-160523.udpipe",
        Language.SPANISH: u"spanish-ud-1.2-160523.udpipe",
        Language.SWEDISH: u"swedish-ud-1.2-160523.udpipe",
        Language.TAMIL: u"tamil-ud-1.2-160523.udpipe",
    }

    LANGUAGES = LANGUAGE_TO_MODEL_FILE.keys()

    def __init__(self, language, model_file_path=None):
        super(UDPipeWrapper, self).__init__(language)
        import ufal.udpipe
        if model_file_path is None:
            model_file_path = os.path.join(
                self.MODEL_FILES_DIRECTORY_PATH,
                self.LANGUAGE_TO_MODEL_FILE[self.language]
            )
        self.model = ufal.udpipe.Model.load(model_file_path)
        if not self.model:
            raise ValueError(u"Unable to load model from file path '%s'. Please specify a valid path with the 'model_file_path' parameter." % model_file_path)

    def _analyze(self, document):
        sentences = []
        import ufal.udpipe
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer.")
        tokenizer.setText(document.raw_flat_string)
        error = ufal.udpipe.ProcessingError()
        lib_sentences = []
        lib_sentence = ufal.udpipe.Sentence()
        while tokenizer.nextSentence(lib_sentence, error):
            lib_sentences.append(lib_sentence)
            lib_sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)
        for lib_sentence in lib_sentences:
            sentence_tokens = []
            self.model.tag(lib_sentence, self.model.DEFAULT)
            self.model.parse(lib_sentence, self.model.DEFAULT)
            lib_useful_tokens = [w for w in lib_sentence.words if w.form != u"<root>"]
            raw_string = u" ".join([w.form for w in lib_useful_tokens])
            for lib_token in lib_useful_tokens:
                if lib_token.form != u"<root>":
                    token = Token(
                        raw=lib_token.form,
                        upos_tag=self.UPOSTAG_MAP[lib_token.upostag],
                        lemma=lib_token.lemma
                    )
                    sentence_tokens.append(token)
            sentences.append((raw_string, sentence_tokens))
        return sentences
