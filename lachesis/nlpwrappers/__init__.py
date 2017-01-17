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
**lachesis.nlpwrappers** is a collection of wrappers
around different NLP packages.
"""

from lachesis.nlpwrappers.base import BaseWrapper
from lachesis.nlpwrappers.nlpengine import NLPEngine
from lachesis.nlpwrappers.nltk import NLTKWrapper
from lachesis.nlpwrappers.pattern import PatternWrapper
from lachesis.nlpwrappers.udpipe import UDPipeWrapper
