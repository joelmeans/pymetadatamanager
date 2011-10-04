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
from file_parser import FileParser
from tvdb import TVDB
from tvshowdb import TVShowDB

class scraper(object):
    """
    Methods for scraping files into the database.
    """

    def __init__(self):
        self.dbTV = TVShowDB('TV.db')
      	self.dbTV.init_db()
        self.TVDB = TVDB()
        self.FP = FileParser()
        self.new_time = TVDB.get_server_time()
        self.dbTV.update_db()
        self.dbTV.clean_db_files()
        self.series_list = []

    def __del__(self):
        dbTV.set_update_time(self.new_time)

    def get_files(self, path):
        self.file_list = self.FP.parse_files_by_path(path)

    def get_series_list(self):
        for file in self.file_list:
            dir = file[0]
            filename = file[1]
            series_name = file[2]
            if not self.dbTV.check_db_for_file(dir, filename):
                if not self.series_list.count(series_name):
                    self.series_list.append(series_name)

    def find_series_ids(self):
        for series_name in self.series_list:
            series_id = self.dbTV.check_db_for_series(series_name)
            if not series_id:
                match_list = self.TVDB.find_series(series_name)
                if len(match_list) == 0:
                    print "No matches found on thetvdb.com for %s." % (series_name)
                    series_id = raw_input("Please input the ID for the correct series:")
                elif len(match_list) == 1:
                    print "Found match for %s." % (series_name)
                    series_id = match_list[0][0]
                else:
                    print "Possible matches for %s:" % (series_name)
                    for i in range(0,len(match_list)):
                        print "[%d] %s (%s)" % (i, match_list[i][1], match_list[i][0])
                    selection = raw_input("Please select the number of the correct match: ")
                    selection = int(selection)
                    series_id = match_list[selection][0]

                series = self.TVDB.get_series_all_by_id(series_id)
                episodes = self.TVDB.get_episodes_by_series_id(series_id)
                actors = self.TVDB.get_actors_by_id(series_id)
                banners = self.TVDB.get_banners_by_id(series_id)

                self.dbTV.write_series_to_db(series)
                self.dbTV.write_episodes_to_db(episodes, series_id)
                self.dbTV.write_actors_to_db(actors)
                self.dbTV.write_banners_to_db(banners)

        #Create a list of files from this series
        series_file_list = []
        for file in file_list:
        if file[2] == series_name:
            if not self.dbTV.check_db_for_file(file[1], file[0]):
                series_file_list.append(file)
        #Add any new files to the DB
        if len(series_file_list):
            self.dbTV.write_files_to_db(series_file_list, series_id)
