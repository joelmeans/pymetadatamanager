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

import logging
from file_parser import FileParser
from tvdb import TVDB
from tvshowdb import TVShowDB
from configuration import Config

class Scanner(object):
    """
    Methods for scanning files into the database.
    """

    def __init__(self, path):
        self.logger = logging.getLogger('pymetadatamanager.scanner')
        self.config = Config()
        self.dbTV = TVShowDB(self.config.tvshowdb)
      	self.dbTV.init_db()
        self.TVDB = TVDB()
        self.FP = FileParser()
        self.new_time = self.TVDB.get_server_time()
        self.dbTV.update_db()
        self.dbTV.clean_db_files()
        self.series_list = []
        self.set_file_list(path)

    def __del__(self):
        try:
            self.dbTV.set_update_time(self.new_time)
        except AttributeError:
            pass

    def set_file_list(self, path):
        self.file_list = self.FP.parse_files_by_path(path)

    def set_series_list(self):
        for file in self.file_list:
            dir = file[0]
            filename = file[1]
            series_name = file[2]
            if not self.dbTV.check_db_for_file(dir, filename):
                if not self.series_list.count(series_name):
                    self.series_list.append(series_name)

    def get_series_id_list(self, series_name):
        series_id = self.dbTV.check_db_for_series(series_name)
        if not series_id:
            match_list = self.TVDB.find_series(series_name)
        return match_list

    def add_series_to_db(self, series_id):
        series = self.TVDB.get_series_all_by_id(series_id)
        episodes = self.TVDB.get_episodes_by_series_id(series_id)
        actors = self.TVDB.get_actors_by_id(series_id)
        banners = self.TVDB.get_banners_by_id(series_id)
        series_name = self.dbTV.get_series_name(series_id)
        self.logger.info("Adding series %s to DB", (series_name,))

        if series is not None:
            self.dbTV.write_series_to_db(series)
        if episodes is not None:
            self.dbTV.write_episodes_to_db(episodes, series_id)
        if actors is not None:
            self.dbTV.write_actors_to_db(actors)
        if banners is not None:
            self.dbTV.write_banners_to_db(banners)

    def add_files_to_db(self, series_name, series_id):
        series_name = self.dbTV.get_series_name(series_id)
        #Create a list of files from this series
        series_file_list = []
        for file in self.file_list:
            if file[2] == series_name:
                if not self.dbTV.check_db_for_file(file[1], file[0]):
                    series_file_list.append(file)
        #Add any new files to the DB
        if len(series_file_list):
            self.logger.info("Adding files from %s to DB", (series_name,))
            self.dbTV.write_files_to_db(series_file_list, series_id)
