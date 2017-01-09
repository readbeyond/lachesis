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
    OPTION_RETRIES = u"retries"

    RETRIES = 5

    YOUTUBE = YTD.CODE

    @classmethod
    def write_file(cls, path, data):
        """
        Write the given data to file
        """
        with io.open(path, "w", encoding="utf-8") as output_file:
            output_file.write(data)

    @classmethod
    def get_data(cls, url, language, options, parse=True, output_file_path=None):
        """
        Download the CC in raw form from a given URL ``url``,
        for a given language ``language``.

        Additional parameters can be passed in ``options``.

        If ``output_file_path`` is not ``None``, write raw data to file.

        If ``parse == False``, return a string containing the raw data.

        If ``parse == True``, return a list of tuples, one for each fragment.
        Each tuple is ``(begin_time, end_time, [line1, line2, ..., lineN])``.
        """
        retries = options.get(cls.OPTION_RETRIES, cls.RETRIES)
        downloader = options.get(cls.OPTION_DOWNLOADER)
        if YTD.can_download(url, downloader):
            download_function = YTD.get_data
            parse_function = YTD.parse_raw_data
        #
        # TODO add other downloaders here, for example:
        #
        # if VD.can_download(url, downloader):
        #     raw_data = VD.get_raw_data(url, language, options)
        #
        raw_data = None
        for i in range(retries):
            try:
                raw_data = download_function(url, language, options)
                break
            except:
                pass
        if raw_data is None:
            raise NotImplementedError(u"No known backend for '%s'" % url)
        if output_file_path is not None:
            cls.write_file(output_file_path, raw_data)
        if parse:
            data = parse_function(raw_data)
        else:
            data = raw_data
        return data
