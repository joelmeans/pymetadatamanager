############################################################################
#    Copyright (C) 2009 by Joel Means,,,                                   #
#    means.joel@gmail.com                                                  #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import os
import re
import logging

class FileParser(object):
    def __init__(self):
        self.logger = logging.getLogger('pymetadatamanager.file_parser')
        self.exts = ['mkv', 'avi', 'mpg', 'iso', 'm4v', 'mp4']
        self.se = re.compile('[Ss]*[0-9]{1,2}[\._x ]{1}[Ee]*[0-9-]{2,3}')
        self.file_list = []

    def parse_filename(self, arg, directory, files):
        """Parses a filename to extract show name, season, and episode"""
        for file in files:
            for ext in self.exts:
                if file.endswith(ext) and not file.startswith('.'):
                    season_ep = self.se.search(file)
                    if season_ep:
                        season_ep = season_ep.group(0)
                        #self.logger.debug("season_ep = %s" % (season_ep))
                        season, episode = re.findall('[0-9]{1,3}', season_ep)
                        show = file.split(season_ep)[0].rstrip(' _.')
                        show_name = re.sub('_', ' ', show)
                        filename = os.path.splitext(file)[0]
                        nfo_name = "%s.nfo" % (filename,)
                        nfo_fullpath = os.path.join(directory, nfo_name)
                        if os.path.isfile(nfo_fullpath):
                            nfo = nfo_fullpath
                        else:
                            nfo = ""
                        series_path = re.sub('[S|s]eason[ |_][0-9]*', '', \
                                             directory)
                        series_nfo = os.path.join(series_path, "tvshow.nfo")
                        if os.path.isfile(series_nfo):
                            nfo_s = series_nfo
                        else:
                            nfo_s = ""
                        show_tuple = (directory, file, show_name, \
                          season.zfill(2), episode, series_nfo, nfo)
                        self.file_list.append(show_tuple)

    def parse_files_by_path(self, filepath):
        """Parses a directory tree to find tv show files"""
        self.logger.debug("Parsing files from %s" % (filepath,))
        os.path.walk(filepath, self.parse_filename, None)
        return self.file_list
