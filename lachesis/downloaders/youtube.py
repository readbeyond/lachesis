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
import io
import re
import os
import youtube_dl
from lxml import etree

from lachesis.downloaders.errors import NotDownloadedError
from lachesis.elements import Document
from lachesis.elements import EndOfLineToken
from lachesis.elements import RawCCLineSpan
from lachesis.elements import RawCCListSpan
from lachesis.elements import RawCCSpan
from lachesis.exacttiming import TimeInterval
from lachesis.exacttiming import TimeValue
import lachesis.globalfunctions as gf


class YDLogger(object):
    """
    TBW
    """
    def debug(self, msg):
        # print(u"[DEBU] %s" % msg)
        pass

    def warning(self, msg):
        # print(u"[WARN] %s" % msg)
        pass

    def error(self, msg):
        # print(u"[ERRO] %s" % msg)
        pass


class YouTubeDownloader(object):

    CODE = u"youtube"

    OPTION_AUTO = u"auto"

    @classmethod
    def can_download(cls, url):
        """
        Determine if this class can download the given ``url``.
        """
        if url is None:
            return False
        return (
            (u"youtube.com" in url) or
            (u"youtu.be" in url) or
            (len(url) == 11)
        )

    @classmethod
    def download(cls, url, language, options):
        """
        Download CCs from the given ``url`` for the given ``language``,
        and return a raw string with the result.
        """
        auto = options.get(cls.OPTION_AUTO, False)
        handler, tmp = gf.tmp_file()
        if os.path.exists(tmp):
            os.remove(tmp)
        tmp = gf.to_unicode_string(tmp)
        out = u"%s.%s.ttml" % (tmp, language)
        ydl_options = {
            "outtmpl": tmp,
            "subtitlesformat": u"ttml",
            "subtitleslangs": [language],
            "writesubtitles": not auto,
            "writeautomaticsub": auto,
            "skip_download": True,
            "logger": YDLogger(),
        }
        try:
            with youtube_dl.YoutubeDL(ydl_options) as ydl:
                ydl.download([url])
        except Exception as e:
            raise NotDownloadedError
        if not os.path.exists(out):
            raise NotDownloadedError
        with io.open(out, "r", encoding="utf-8") as out_file:
            data = out_file.read()
        gf.delete_file(handler, tmp)
        gf.delete_file(None, out)
        return data

    @classmethod
    def parse(cls, raw_data, language=None):
        """
        Parse the given ``raw_data`` string,
        and return a Document object.
        """
        # constants
        PLACEHOLDER_BR = u" ||| "
        PLACEHOLDER_NO_TEXT = u"()"
        PATTERN_SPAN_OPEN = re.compile(r"<span[^>]*>")
        PATTERN_SPAN_CLOSE = re.compile(r"</span>")
        PATTERN_BR = re.compile(r"<br[ ]*/>")
        PATTERN_SPACES = re.compile(r"\s+")
        TTML_NS = "{http://www.w3.org/ns/ttml}"
        TTML_TT = "%stt" % TTML_NS
        TTML_P = "%sp" % TTML_NS
        TTML_BEGIN = "begin"
        TTML_END = "end"
        XML_NS = "{http://www.w3.org/XML/1998/namespace}"
        XML_LANG = "%slang" % XML_NS

        # remove spans
        s = raw_data
        s = re.sub(PATTERN_SPAN_OPEN, u"", s)
        s = re.sub(PATTERN_SPAN_CLOSE, u"", s)
        # replace br with placeholder
        s = re.sub(PATTERN_BR, PLACEHOLDER_BR, s)
        # remove duplicated spaces
        s = re.sub(PATTERN_SPACES, u" ", s).strip()

        # encode to utf-8 as required by lxml
        if gf.is_unicode(s):
            s = s.encode("utf-8")

        # create tree
        root = etree.fromstring(s)

        # parse language
        xml_lang = language
        for elem in root.iter(TTML_TT):
            try:
                xml_lang = gf.to_unicode_string(elem.get(XML_LANG))
                break
            except:
                pass

        raw_ccl = RawCCListSpan()

        # parse fragments
        for elem in root.iter(TTML_P):
            begin = gf.time_from_hhmmssmmm(elem.get(TTML_BEGIN).strip())
            end = gf.time_from_hhmmssmmm(elem.get(TTML_END).strip())
            text = elem.text
            # text missing
            if text is None:
                text = u""
            # strip leading/trailing spaces
            text = text.strip()
            # if no text is available, replace it with ()
            if text == u"":
                text = PLACEHOLDER_NO_TEXT
            # split lines if the <br/> is present
            lines = [l.strip() for l in text.split(PLACEHOLDER_BR)]
            # make sure we return unicode strings
            lines = [gf.to_unicode_string(l) for l in lines if len(l) > 0]
            lines = [u"%s %s" % (l, EndOfLineToken.RAW) for l in lines]
            # append span objects
            raw_ccl.append(RawCCSpan(
                elements=[RawCCLineSpan(raw=l) for l in lines],
                time_interval=TimeInterval(TimeValue(begin), TimeValue(end)),
            ))

        # create new Document object
        doc = Document(raw=raw_ccl, language=xml_lang)

        return doc
