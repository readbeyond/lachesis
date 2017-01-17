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

# TODO from lachesis.downloaders.vimeo import VimeoDownloader as VD
from lachesis.downloaders.youtube import YouTubeDownloader as YTD
import lachesis.globalfunctions as gf


class Downloader(object):

    OPTION_DOWNLOADER = u"downloader"
    OPTION_OUTPUT_FILE_PATH = u"output_file_path"
    OPTION_RETRIES = u"retries"

    OUTPUT_FILE_PATH = None
    RETRIES = 5

    # TODO add other downloaders here
    DOWNLOADERS = {
        YTD.CODE: YTD,
        #VD.CODE: VD,
    }

    @classmethod
    def select_downloader(cls, url, options):
        """
        Return a known class that can download
        and parse the given ``url`` or ``None`` if not possible.
        """
        downloader_class = None
        downloader = options.get(cls.OPTION_DOWNLOADER)
        if downloader is None:
            # no explicit downloader: try determining it using can_download() functions
            for d_class in cls.DOWNLOADERS.values():
                if d_class.can_download(url):
                    downloader_class = d_class
                    break
        else:
            # explicit downloader requested
            downloader_class = cls.DOWNLOADERS.get(downloader, None)
        if downloader_class is None:
            raise NotImplementedError(u"No known backend for '%s'" % url)
        return downloader_class

    @classmethod
    def read_closed_captions(cls, input_file_path, options):
        """
        Extract CC from the given file ``input_file_path``,
        and return a ClosedCaptionList object.
        """
        def read_file(path):
            with io.open(path, "r", encoding="utf-8") as input_file:
                data = input_file.read()
            return data

        d_class = cls.select_downloader(None, options)
        raw_data = read_file(input_file_path)
        return d_class.parse(raw_data, language=None)

    @classmethod
    def download_closed_captions(cls, url, language, options):
        """
        Download the CC from a given URL ``url``,
        for a given language ``language``,
        parse them and return a ClosedCaptionList object.

        Additional parameters can be passed in ``options``:

            1. if ``output_file_path`` is specified and not ``None``,
               write raw data to file (default: do not write);
            2. if ``retries`` is specified , attempt that many downloads
               before raising an exception (default: 5).
        """
        def write_file(path, data):
            """
            Write the given data to file.
            """
            with io.open(path, "w", encoding="utf-8") as output_file:
                output_file.write(data)

        raw_data = None
        output_file_path = options.get(cls.OPTION_OUTPUT_FILE_PATH, cls.OUTPUT_FILE_PATH)
        retries = options.get(cls.OPTION_RETRIES, cls.RETRIES)

        d_class = cls.select_downloader(url, options)
        for i in range(retries):
            try:
                raw_data = d_class.download(url, language, options)
                break
            except:
                pass
        if raw_data is None:
            raise IOError(u"Unable to download CC data, please check your Internet connection.")
        if output_file_path is not None:
            write_file(output_file_path, raw_data)
        return d_class.parse(raw_data, language=language)
