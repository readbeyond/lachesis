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

from lachesis.elements import Document
from lachesis.elements import EndOfSentenceToken
from lachesis.elements import EndOfLineToken
from lachesis.elements import Span
from lachesis.elements import Token
from lachesis.language import Language
from lachesis.nlpwrappers.upostags import UniversalPOSTags
import lachesis.globalfunctions as gf


class BaseWrapper(object):
    """
    TBW

    A wrapper for an NLP library.
    """

    CODE = u"base"

    LANGUAGES = []
    """ The languages supported by this NLP library """

    UPOSTAG_MAP = UniversalPOSTags.UPOSTAG_MAP_V1_TO_V2
    """ Maps the POS tags returned by this NLP library to Universal POS Tags (v2) """

    def __init__(self, language):
        lfc = Language.from_code(language)
        if (lfc is not None) and (lfc in self.LANGUAGES):
            self.language = lfc
            return self
        if language in self.LANGUAGES:
            self.language = language
            return self
        raise ValueError(u"This NLP library does not support the '%s' language" % language)

    def analyze(self, document):
        """
        Analyze the given document, splitting it into sentences
        and tagging the tokens (words) with Universal POS tags.
        Some NLP libraries (e.g., ``pattern``)
        also performs chunking at this stage.

        The information output (sentences, token tags, etc.)
        will be stored inside the given ``document`` object.
        """
        def _remove_unnecessary_eols(sentences):
            new_sentences = []
            new_tokens = []
            for sent in sentences:
                # remove an EndOfLineToken at the begin or end
                while (len(sent) > 0) and (isinstance(sent[0], EndOfLineToken)):
                    sent = sent[1:]
                while (len(sent) > 0) and (isinstance(sent[-1], EndOfLineToken)):
                    sent = sent[:-1]
                # return only if at least one token survived
                if len(sent) > 0:
                    new_sentences.append(sent)
                    new_tokens.extend(sent)
            return new_sentences, new_tokens

        def _set_trailing_whitespace_attributes(doc_string, tokens):
            n = len(doc_string)
            i = 0
            for t in tokens:
                if t.is_regular:
                    i = doc_string.find(t.raw, i) + len(t.raw)
                    t.trailing_whitespace = (i < n) and (doc_string[i] == u" ")

        doc_string = document.raw_flat_clean_string
        if (doc_string is None) or (len(doc_string) < 1):
            raise ValueError(u"The document has no text set.")
        if (document.language is not None) and (document.language != self.language):
            # TODO warning instead?
            raise ValueError(u"The document has been created with the '%s' language set while this NLP library has loaded the '%s' language." % (document.language, self.language))

        def _fix_across_sentence_splits(sentences):
            # move characters with no trailing whitespace
            # located at the begin of current sentence
            # back to previous sentence
            # e.g.:
            # She said 'hello world.' Then off she went.
            # becomes, after NLP:
            # ["She said 'hello world.", "' Then off she went."]
            # after this step:
            # ["She said 'hello world.'", "Then off she went."]
            # as expected
            for i in range(1, len(sentences)):
                prev_sent = sentences[i - 1]
                curr_sent = sentences[i]
                while (len(prev_sent) > 0) and (len(curr_sent) > 0) and (not prev_sent[-1].trailing_whitespace):
                    # print("MOVE: %s <= %s" % (prev_sent[-1], curr_sent[0]))
                    prev_sent.append(curr_sent[0])
                    curr_sent = curr_sent[1:]
                sentences[i - 1] = prev_sent
                sentences[i] = curr_sent
            return sentences

        # remove any information from the document
        document.clear()

        # do the actual analysis
        doc_string_with_eol = document.raw.string(flat=True)
        sentences = self._analyze(doc_string_with_eol)

        # remove unnecessary EndOfLineToken objects
        # and keep only non-empty sentences
        sentences, tokens = _remove_unnecessary_eols(sentences)

        # set trailing_whitespace attributes
        _set_trailing_whitespace_attributes(doc_string, tokens)

        # fix (punctuation) across sentence splits
        sentences = _fix_across_sentence_splits(sentences)

        # remove unnecessary EndOfLineToken objects
        # and keep only non-empty sentences
        #
        # NOTE: yes, running this twice is mandatory
        #
        sentences, tokens = _remove_unnecessary_eols(sentences)

        # append resulting non-empty sentences to document
        document.text_view = Span()
        for sent in sentences:
            # add end of sentence token
            token = EndOfSentenceToken()
            sent.append(token)
            # add all surviving tokens
            sentence = Span()
            document.tokens.extend(sent)
            sentence.extend(sent)
            document.text_view.append(sentence)

    def _analyze(self, doc_string):
        """
        This is the actual function running
        the tokenizer and tagger over given ``doc_string`` object.
        """
        raise NotImplementedError(u"This method should be implemented in a subclass.")

    def _create_token(self, raw, upos_tag, lemma=None):
        """
        Return a new token, either a EndOfLineToken or a regular token.
        """
        if raw == EndOfLineToken.RAW:
            return EndOfLineToken()
        return Token(raw=raw, upos_tag=self.UPOSTAG_MAP[upos_tag], lemma=lemma)
