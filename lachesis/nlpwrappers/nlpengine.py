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

from lachesis.nlpwrappers.nltk import NLTKWrapper
from lachesis.nlpwrappers.pattern import PatternWrapper
from lachesis.nlpwrappers.udpipe import UDPipeWrapper
import lachesis.globalfunctions as gf


class NLPEngine(object):
    """
    TBW
    """

    KNOWN_WRAPPERS = [
        PatternWrapper,
        NLTKWrapper,
        UDPipeWrapper,
    ]

    CODE_TO_CLASS = {
        NLTKWrapper.CODE: NLTKWrapper,
        PatternWrapper.CODE: PatternWrapper,
        UDPipeWrapper.CODE: UDPipeWrapper,
    }

    def __init__(self, preload=[]):
        self.cache = {}
        for (l, w) in preload:
            self.load_wrapper(l, w, cache=True)

    def load_wrapper(self, language, wrapper, cache=False):
        """
        Return an instance of the NLP wrapper with code ``wrapper``
        for the given language ``language``.
        If ``cache`` is ``True``, the instance will be cached
        for subsequent use.
        """
        if (language, wrapper) in self.cache:
            return self.cache[(language, wrapper)]
        if not wrapper in self.CODE_TO_CLASS:
            raise ValueError(u"Unknown NLP wrapper code '%s'" % wrapper)
        wrapper_instance = self.CODE_TO_CLASS[wrapper](language)
        if cache:
            self.cache[(language, wrapper)] = wrapper_instance
        return wrapper_instance

    def analyze(self, text, wrapper=None, cache=False):
        """
        Analyze the given text object ``text``.

        If a ``wrapper`` code is specified, it will be loaded
        (from cache, if present).

        If ``cache`` is ``True``, the NLP wrapper will be cached
        for subsequent use.
        """
        wrapper_instance = None
        lang = text.language
        if wrapper is None:
            for (l, w) in self.cache.keys():
                if l == lang:
                    wrapper_instance = self.cache[(l, w)]
                    break
            if wrapper_instance is None:
                for code in [x.CODE for x in self.KNOWN_WRAPPERS]:
                    try:
                        wrapper_instance = self.load_wrapper(lang, code, cache=cache)
                        break
                    except Exception as e:
                        pass
        else:
            wrapper_instance = self.load_wrapper(lang, wrapper, cache=cache)
        if wrapper_instance is None:
            raise ValueError(u"Unable to locate a suitable NLP wrapper for language '%s'" % lang)
        #print(u"Using " + wrapper_instance.CODE)
        wrapper_instance.analyze(text)
