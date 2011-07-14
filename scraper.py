#!/usr/bin/env python
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

from pymetadatamanager.file_parser import FileParser
from pymetadatamanager.tvdb import TVDB
from pymetadatamanager.tvshowdb import TVShowDB

dbTV = TVShowDB('TV.db')
dbTV.init_db()

TVDB = TVDB()
FP = FileParser()

#Get the current time from thetvdb.com for updates
new_time = TVDB.get_server_time()
#Now update and clean the db
dbTV.update_db()
dbTV.clean_db_files()

#Ask for the path to search and get a list of files within that path
file_path = raw_input("File Path to Add to DB: ")
file_list = FP.parse_files_by_path(file_path)

#Create a list of series names based on the filenames grokked above
series_list = []
for file in file_list:
    dir = file[0]
    filename = file[1]
    series_name = file[2]
    if not dbTV.check_db_for_file(dir, filename):
        if not series_list.count(series_name):
            series_list.append(series_name)

#Process each series we have found
for series_name in series_list:
    #If the series is already in the DB, we don't need to hit thetvdb.com
    series_id = dbTV.check_db_for_series_name(series_name)
    if series_id:
        pass
    #If not, get the info for the series
    else:
        series_id = TVDB.find_series(series_name)

        series = TVDB.get_series_all_by_id(series_id)
        episodes = TVDB.get_episodes_by_series_id(series_id)
        actors = TVDB.get_actors_by_id(series_id)
        banners = TVDB.get_banners_by_id(series_id)

        dbTV.write_series_to_db(series)
        dbTV.write_episodes_to_db(episodes, series_id)
        dbTV.write_actors_to_db(actors)
        dbTV.write_banners_to_db(banners)

    #Create a list of files from this series
    series_file_list = []
    for file in file_list:
        if file[2] == series_name:
            if dbTV.check_db_for_file(file[1], file[0]):
                pass
            else:
                series_file_list.append(file)
    #Add any new files to the DB
    if len(series_file_list):
        dbTV.write_files_to_db(series_file_list, series_id)

#Finally, write the new update time to the DB
dbTV.set_update_time(new_time)


#tvshow = dbTV.make_series_etree(series_id)
#outfile = open("test.xhtml", "w")
#ET.ElementTree(tvshow).write(outfile, "UTF-8")

#outfile.close()
