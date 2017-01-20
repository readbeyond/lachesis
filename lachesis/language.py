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

import lachesis.globalfunctions as gf

# NOTE: consider using langcodes once available as unified PY2+PY2 package


class LanguageObject(object):
    """
    TBW
    """

    def __init__(self, name, codes):
        self.name = name
        self.codes = codes

    def __eq__(self, other):
        if isinstance(other, LanguageObject):
            return self.name == other.name
        if gf.is_unicode(other):
            other = other.lower()
            return (other in self.codes) or (other == self.name.lower())
        return False

    def __neq__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Language(object):
    """
    TBW
    """

    ARABIC = LanguageObject(u"Arabic", (u"ara", u"ar"))
    BASQUE = LanguageObject(u"Basque", (u"baq", u"eus", u"eu"))
    BULGARIAN = LanguageObject(u"Bulgarian", (u"bul", u"bg"))
    CROATIAN = LanguageObject(u"Croatian", (u"hrv", u"hr"))
    CZECH = LanguageObject(u"Czech", (u"cze", u"cse", u"cs"))
    DANISH = LanguageObject(u"Danish", (u"dan", u"da"))
    DUTCH = LanguageObject(u"Dutch", (u"dut", u"nld", u"nl"))
    ENGLISH = LanguageObject(u"English", (u"eng", u"en"))
    ESTONIAN = LanguageObject(u"Estonian", (u"est", u"et"))
    FINNISH = LanguageObject(u"Finnish", (u"fin", u"fi"))
    FRENCH = LanguageObject(u"French", (u"fre", u"fra", u"fr"))
    GERMAN = LanguageObject(u"German", (u"ger", u"deu", u"de"))
    GOTHIC = LanguageObject(u"Gothic", (u"got",))
    GREEK = LanguageObject(u"Greek", (u"gre", u"ell", u"el"))
    GREEK_ANCIENT = LanguageObject(u"Ancient Greek", (u"grc",))
    HEBREW = LanguageObject(u"Hebrew", (u"heb", u"he"))
    HINDI = LanguageObject(u"Hindi", (u"hin", u"hi"))
    HUNGARIAN = LanguageObject(u"Hungarian", (u"hun", u"hu"))
    INDONESIAN = LanguageObject(u"Indonesian", (u"ind", u"id"))
    IRISH = LanguageObject(u"Irish", (u"gle", u"ga"))
    ITALIAN = LanguageObject(u"Italian", (u"ita", u"it"))
    LATIN = LanguageObject(u"Latin", (u"lat", u"la"))
    NORWEGIAN = LanguageObject(u"Norwegian", (u"nor", u"no"))
    OLD_CHURCH_SLAVONIC = LanguageObject(u"Old Church Slavonic", (u"chu", u"cu"))
    PERSIAN = LanguageObject(u"Persian", (u"per", u"fas", u"fa"))
    POLISH = LanguageObject(u"Polish", (u"pol", u"po"))
    PORTUGUESE = LanguageObject(u"Portuguese", (u"por", u"pt"))
    ROMANIAN = LanguageObject(u"Romanian", (u"rum", u"ron", u"ro"))
    SLOVENIAN = LanguageObject(u"Slovenian", (u"slv", u"sl"))
    SPANISH = LanguageObject(u"Spanish", (u"spa", u"es"))
    SWEDISH = LanguageObject(u"Swedish", (u"swe", u"sv"))
    TAMIL = LanguageObject(u"Tamil", (u"tam", u"ta"))
    TURKISH = LanguageObject(u"Turkish", (u"tur", u"tr"))

    ALL_LANGUAGES = [
        ARABIC,
        BASQUE,
        BULGARIAN,
        CROATIAN,
        CZECH,
        DANISH,
        DUTCH,
        ENGLISH,
        ESTONIAN,
        FINNISH,
        FRENCH,
        GERMAN,
        GOTHIC,
        GREEK,
        GREEK_ANCIENT,
        HEBREW,
        HINDI,
        HUNGARIAN,
        INDONESIAN,
        IRISH,
        ITALIAN,
        LATIN,
        NORWEGIAN,
        OLD_CHURCH_SLAVONIC,
        PERSIAN,
        POLISH,
        PORTUGUESE,
        ROMANIAN,
        SLOVENIAN,
        SPANISH,
        SWEDISH,
        TAMIL,
        TURKISH,
    ]

    @classmethod
    def from_code(cls, code):
        if isinstance(code, LanguageObject) and code in cls.ALL_LANGUAGES:
            return code
        for language in cls.ALL_LANGUAGES:
            if language == code:
                return language
        return None
