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

class FileParser(object):
    def __init__(self):
        self.exts = ['mkv', 'avi', 'mpg', 'iso', 'm4v', 'mp4']
        self.file_list = []

    def parse_filename(self, arg, directory, files):
        """Parses a filename to extract show name, season, and episode"""
        for file in files:
            for ext in self.exts:
                if file.endswith(ext):
                    ssxeee = re.search('[0-9]{2}x[0-9]{3}', file)
                    ssxee = re.search('[0-9]{2}x[0-9]{2}', file)
                    if ssxeee:
                        season_ep = ssxeee.group(0)
                        season = season_ep.split('x')[0]
                        episode = season_ep.split('x')[1]
                        show = file.split(season_ep)[0].rstrip().rstrip('_')
                        show_name = re.sub('_', ' ', show)
                        show_tuple = (directory, file, show_name, season, \
                          episode)
                        self.file_list.append(show_tuple)
                    elif ssxee:
                        season_ep = ssxee.group(0)
                        season = season_ep.split('x')[0]
                        episode = season_ep.split('x')[1]
                        show = file.split(season_ep)[0].rstrip().rstrip('_')
                        show_name = re.sub('_', ' ', show)
                        show_tuple = (directory, file, show_name, season, \
                          episode)
                        self.file_list.append(show_tuple)

    def parse_files_by_path(self, filepath):
        """Parses a directory tree to find tv show files"""
        os.path.walk(filepath, self.parse_filename, None)
        return self.file_list
