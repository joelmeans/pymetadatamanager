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
import urllib
import logging
from sqlite3 import dbapi2 as sqlite
from tvdb import TVDB
from PyQt4 import QtCore
from PyQt4 import QtXml
from mediainfo import MediaInfo

class TVShowDB(object):
    """
    A class for interacting with a local sqlite database.

    This class creates and interacts with a local sqlite database containing
    information about TV episodes which are being catalogued.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.dbTV = sqlite.connect(self.db_name, check_same_thread = False)
        self.sqlTV = self.dbTV.cursor()
        self.new_version = 5
        self.tvdb = TVDB()
        self.MediaInfo = MediaInfo()
        self.logger = logging.getLogger('pymetadatamanager.tvshowdb')
        self.logger.info('Creating connection to tv show database')

    def __del__(self):
        self.sqlTV.close()
        self.dbTV.close()

    def init_db(self):
        """Initialize the database for use"""
        self.logger.info('Initializing the database (%s)' % (self.db_name))
        # find out if a previous version of the database exists
        current_version = 0
        self.sqlTV.execute("SELECT * FROM sqlite_master WHERE type = \
         'table' AND name = 'version'")
        if len(self.sqlTV.fetchall()):
            self.sqlTV.execute('SELECT idVersion FROM version')
            for x in self.sqlTV.fetchall():
                current_version = x[0]
        else:
            current_version = 0
        # if no db existed previously, create it
        if current_version < 1:
            self.sqlTV.execute( 'CREATE TABLE version (idVersion INTEGER, \
             lastUpdate INTEGER)')
            self.sqlTV.execute('INSERT INTO version (idVersion) VALUES (?)', \
             (self.new_version, ))
            self.sqlTV.execute('CREATE TABLE files (id INTEGER PRIMARY KEY, \
             filename VARCHAR(50), filepath VARCHAR(100))')
            self.sqlTV.execute('CREATE TABLE shows (id INTEGER PRIMARY KEY, \
             seriesid INTEGER, name VARCHAR(50), overview VARCHAR(500), \
             content_rating VARCHAR(10), runtime INTEGER, status VARCHAR(15), \
             language VARCHAR(5), first_aired VARCHAR(15), \
             airs_day VARCHAR(15), airs_time VARCHAR(10), \
             rating VARCHAR(5))')
            self.sqlTV.execute('CREATE TABLE episodes (id INTEGER PRIMARY KEY, \
             episodeid INTEGER, name VARCHAR(50), overview VARCHAR(500), \
             season_number INTEGER, episode_number INTEGER, \
             language VARCHAR(5), prod_code VARCHAR(10), rating VARCHAR(15), \
             first_aired VARCHAR(15), thumb VARCHAR(100))')
            self.sqlTV.execute('CREATE TABLE actors (id INTEGER PRIMARY KEY, \
             name VARCHAR(50), thumb VARCHAR(100))')
            self.sqlTV.execute('CREATE TABLE networks (id INTEGER PRIMARY KEY, \
             name VARCHAR(50))')
            self.sqlTV.execute('CREATE TABLE genres (id INTEGER PRIMARY KEY, \
             name VARCHAR(50))')
            self.sqlTV.execute('CREATE TABLE directors \
             (id INTEGER PRIMARY KEY, name VARCHAR(50))')
            self.sqlTV.execute('CREATE TABLE writers (id INTEGER PRIMARY KEY, \
             name VARCHAR(50))')
            self.sqlTV.execute('CREATE TABLE episodelinkshow \
             (idEpisode INTEGER, idShow INTEGER)')
            self.sqlTV.execute('CREATE TABLE actorlinkshow \
             (idActor INTEGER, idShow INTEGER, role VARCHAR(50))')
            self.sqlTV.execute('CREATE TABLE networklinkshow \
             (idNetwork INTEGER, idShow INTEGER)')
            self.sqlTV.execute('CREATE TABLE genrelinkshow (idGenre INTEGER, \
             idShow INTEGER)')
            self.sqlTV.execute('CREATE TABLE directorlinkepisode (idDirector \
             INTEGER, idEpisode INTEGER)')
            #For guest stars, they are put in the actor table,
            #  but linked to episodes
            self.sqlTV.execute('CREATE TABLE actorlinkepisode \
             (idActor INTEGER, idEpisode INTEGER, role VARCHAR(50))')
            self.sqlTV.execute('CREATE TABLE writerlinkepisode \
             (idWriter INTEGER, idEpisode INTEGER)')
            self.sqlTV.execute('CREATE TABLE filelinkepisode \
             (idFile INTEGER, idEpisode INTEGER)')
            self.sqlTV.execute('CREATE TABLE banners (id INTEGER PRIMARY KEY, \
             idBanner INTEGER, path VARCHAR(100), type VARCHAR(50), \
             type2 VARCHAR(50), colors VARCHAR(100), \
             thumbnailPath VARCHAR(100), season INT, url VARCHAR(100))')
            self.sqlTV.execute('CREATE TABLE bannerlinkshow \
             (idBanner INTEGER, idShow INTEGER)')
        if current_version < 2:
            self.sqlTV.execute('CREATE TABLE modified_episodes \
             (idEpisode INTEGER)')
            self.sqlTV.execute('CREATE TABLE modified_shows \
             (idShow INTEGER)')
        if current_version < 3:
            self.sqlTV.execute('CREATE TABLE video_formats \
             (id INTEGER PRIMARY KEY, codec VARCHAR(20), aspect FLOAT, \
             width INTEGER, height INTEGER)')
            self.sqlTV.execute('CREATE TABLE audio_formats \
             (id INTEGER PRIMARY KEY, codec VARCHAR(20), \
             language VARCHAR(30), channels INTEGER)')
            self.sqlTV.execute('CREATE TABLE subtitle_formats \
             (id INTEGER PRIMARY KEY, language VARCHAR(20))')
            self.sqlTV.execute('CREATE TABLE videolinkfile \
             (idVideoFormat INTEGER, idFile INTEGER)')
            self.sqlTV.execute('CREATE TABLE audiolinkfile \
             (idAudioFormat INTEGER, idFile INTEGER)')
            self.sqlTV.execute('CREATE TABLE sublinkfile \
             (idSubtitleFormat INTEGER, idFile INTEGER)')
        if current_version < 4:
            self.sqlTV.execute('CREATE TABLE selectedbannerlinkshow \
             (idBanner INTEGER, idShow INTEGER, type VARCHAR(50), season INTEGER)')
        if current_version < 5:
            self.sqlTV.execute('ALTER TABLE shows ADD COLUMN \
             episodeguide VARCHAR(200)')
        if not current_version == 1:
            self.sqlTV.execute('UPDATE version SET idVersion=(?)', \
             (self.new_version, ))
        self.dbTV.commit()

    def set_update_time(self, time):
        """Sets the time of the last update in the db"""
        self.sqlTV.execute('UPDATE version SET lastUpdate=(?)', (int(time), ))
        self.dbTV.commit()

    def get_update_time(self):
        """Gets the time of the last update from the db"""
        self.sqlTV.execute('SELECT lastUpdate FROM version')
        time_list = self.sqlTV.fetchall()
        if len(time_list):
            for x in time_list[0]: time = x
        else:
            time = 0
        return time

    def write_episodes_to_db(self, episodes, series_id):
        """Writes info for episodes to the database"""
        for episode in episodes:
            #Check to see if the episode is already in the db
            self.sqlTV.execute('SELECT * FROM episodes WHERE episodeid=(?)', \
             (episode.episodeid, ))
            if len(self.sqlTV.fetchall()):
                self.logger.info("Season %s episode %s is already in the DB" % (episode.season_number, episode.episode_number))
                pass
            else:
                self.logger.info("Adding season %s episode %s to the DB" % (episode.season_number, episode.episode_number))
                self.sqlTV.execute('INSERT INTO episodes ("episodeid", "name", \
                 "overview", "season_number", "episode_number", "language", \
                 "prod_code", "rating", "first_aired", "thumb") VALUES \
                 (?,?,?,?,?,?,?,?,?,?)', \
                 (episode.episodeid, \
                  episode.episode_name, \
                  episode.overview, \
                  episode.season_number, \
                  episode.episode_number, \
                  episode.language, \
                  episode.production_code, \
                  episode.rating, \
                  episode.first_aired, \
                  episode.thumb))
                #Link the episode to the series
                self.sqlTV.execute('SELECT id FROM episodes WHERE \
                 episodeid=(?)', (episode.episodeid, ))
                id_episode_list = self.sqlTV.fetchall()
                self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
                 (series_id, ))
                id_show_list = self.sqlTV.fetchall()
                for x in id_episode_list[0]: id_episode = x
                for y in id_show_list[0]: id_show = y
                #Make sure the link doesn't already exist
                self.sqlTV.execute('SELECT * FROM episodelinkshow WHERE \
                 idEpisode=(?) AND idShow=(?)', (id_episode, id_show))
                if len(self.sqlTV.fetchall()):
                    pass
                else:
                    self.sqlTV.execute('INSERT INTO episodelinkshow \
                     ("idEpisode", "idShow") VALUES (?,?)', \
                     (id_episode, id_show))
            #Add in the actors appearing in single episodes as guests
            for guest in episode.guest_stars:
                #See if the actor is already in the db
                self.sqlTV.execute('SELECT * FROM actors WHERE name=(?)', \
                 (guest, ))
                if len(self.sqlTV.fetchall()):
                    pass
                else:
                    self.sqlTV.execute('INSERT INTO actors ("name", "thumb") \
                     VALUES (?, ?)', (guest, "none"))
                #Link the actor to the episode
                self.sqlTV.execute('SELECT id FROM actors WHERE name=(?)', \
                 (guest, ))
                id_guest_list = self.sqlTV.fetchall()
                self.sqlTV.execute('SELECT id FROM episodes WHERE \
                 episodeid=(?)', (episode.episodeid, ))
                id_episode_list = self.sqlTV.fetchall()
                for x in id_guest_list[0]: id_guest = x
                for y in id_episode_list[0]: id_episode = y
                self.sqlTV.execute('INSERT INTO actorlinkepisode ("idActor", \
                 "idEpisode") VALUES (?, ?)', (id_guest, id_episode))
            #Add in the directors
            for director in episode.directors:
                #See if the director is already in the db
                self.sqlTV.execute('SELECT * FROM directors WHERE name=(?)', \
                 (director, ))
                if len (self.sqlTV.fetchall()):
                    pass
                else:
                    self.sqlTV.execute('INSERT INTO directors ("name") \
                     VALUES (?)', (director, ))
                #Link the director to the episode
                self.sqlTV.execute('SELECT id FROM directors WHERE name=(?)', \
                 (director, ))
                id_director_list = self.sqlTV.fetchall()
                self.sqlTV.execute('SELECT id FROM episodes WHERE \
                 episodeid=(?)', (episode.episodeid, ))
                id_episode_list = self.sqlTV.fetchall()
                for x in id_director_list[0]: id_director = x
                for y in id_episode_list[0]: id_episode = y
                self.sqlTV.execute('INSERT INTO directorlinkepisode \
                 ("idDirector", "idEpisode") VALUES (?, ?)', \
                 (id_director, id_episode))
            #Add in the writers
            for writer in episode.writers:
                #See if the writer is already in the db
                self.sqlTV.execute('SELECT * FROM writers WHERE name=(?)', \
                 (writer, ))
                if len (self.sqlTV.fetchall()):
                    pass
                else:
                    self.sqlTV.execute('INSERT INTO writers ("name") \
                     VALUES (?)', (writer, ))
                #Link the writer to the episode
                self.sqlTV.execute('SELECT id FROM writers WHERE name=(?)', \
                 (writer, ))
                id_writer_list = self.sqlTV.fetchall()
                self.sqlTV.execute('SELECT id FROM episodes WHERE \
                 episodeid=(?)', (episode.episodeid, ))
                id_episode_list = self.sqlTV.fetchall()
                for x in id_writer_list[0]: id_writer = x
                for y in id_episode_list[0]: id_episode = y
                self.sqlTV.execute('INSERT INTO writerlinkepisode \
                 ("idWriter", "idEpisode") VALUES (?, ?)', \
                 (id_writer, id_episode))
        self.dbTV.commit()

    def write_actors_to_db(self, actors):
        """Writes actor info to the database"""
        for actor in actors:
            #See if the actor is already in the db
            self.sqlTV.execute('SELECT * FROM actors WHERE name=(?)', \
             (actor.name, ))
            found_list = self.sqlTV.fetchall()
            #If so, see if the thumbnail link exists and add it if not
            if len(found_list):
                found = found_list[0]
                if not found[2]:
                    self.sqlTV.execute('UPDATE actors SET thumb=(?) \
                     WHERE id=(?)', (actor.thumb, found[0]))
                elif found[2] == "none":
                    self.sqlTV.execute('UPDATE actors SET thumb=(?) \
                     WHERE id=(?)', (actor.thumb, found[0]))
            #If not, add the actor to the db
            else:
                self.sqlTV.execute('INSERT INTO actors ("name", "thumb") \
                 VALUES (?,?)', (actor.name, actor.thumb))
            #Link the actor to the series
            self.sqlTV.execute('SELECT id FROM actors WHERE name=(?)', \
             (actor.name, ))
            id_actor_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
             (actor.seriesid, ))
            id_show_list = self.sqlTV.fetchall()
            for x in id_actor_list[0]: id_actor = x
            for y in id_show_list[0]: id_show = y
            #Make sure the link isn't already there
            self.sqlTV.execute('SELECT * FROM actorlinkshow WHERE idActor=(?) \
             and idShow=(?)', (id_actor, id_show))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO actorlinkshow \
                 ("idActor", "idShow", "role") VALUES (?,?,?)', \
                 (id_actor, id_show, actor.role))
        self.dbTV.commit()

    def write_banners_to_db(self, banners):
        """Writes info about series banners to the database"""
        for banner in banners:
#            self.logger.debug("banner.path = %s" % (banner.path,))
            #See if the banner is already in the db
            self.sqlTV.execute('SELECT * FROM banners WHERE path=(?)', \
             (banner.path, ))
            found_list = self.sqlTV.fetchall()
            if len(found_list):
#                self.logger.debug("alread found in database")
                pass
            else:
                self.sqlTV.execute('INSERT INTO banners \
                 ("idBanner", "path", "type", "type2", "colors", \
                 "thumbnailPath", "season", "url") VALUES (?,?,?,?,?,?,?,?)', \
                 (banner.id, banner.path, banner.type, banner.type2, \
                 banner.colors, banner.thumb, banner.season, banner.url))
            self.dbTV.commit()
            #Link the banner to the series
            self.sqlTV.execute('SELECT id FROM banners WHERE path=(?)', \
             (banner.path, ))
            id_banner_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
             (banner.seriesid, ))
            id_show_list = self.sqlTV.fetchall()
            for x in id_banner_list[0]: id_banner = x
            for y in id_show_list[0]: id_show = y
            #Make sure the link isn't already there
            self.sqlTV.execute('SELECT * FROM bannerlinkshow WHERE \
             idBanner=(?) and idShow=(?)', (id_banner, id_show))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO bannerlinkshow \
                 ("idBanner", "idShow") VALUES (?,?)', (id_banner, id_show, ))
        self.dbTV.commit()

    def write_series_to_db(self, series):
        """Writes info for a series to the database"""
        #Check to see if the series is already in the db
        self.sqlTV.execute('SELECT * FROM shows WHERE seriesid=(?)', \
         (series.seriesid, ))
        if len(self.sqlTV.fetchall()):
            pass
        #If not, then write the info
        else:
            self.sqlTV.execute('INSERT INTO shows \
             ("seriesid", "name", "overview", "content_rating", "runtime", \
             "status", "language", "first_aired", "airs_day", "airs_time", \
             "rating", "episodeguide") VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', \
             (series.seriesid, \
              series.name, \
              series.overview, \
              series.content_rating, \
              series.runtime, \
              series.status, \
              series.language, \
              series.first_aired, \
              series.airs_day, \
              series.airs_time, \
              series.rating, \
              series.episodeguide))
            #Add the genres if they aren't already there and link them up
            for genre in series.genre:
                self.sqlTV.execute('SELECT * FROM genres WHERE name=(?)', \
                 (genre, ))
                if len (self.sqlTV.fetchall()):
                    pass
                else:
                    self.sqlTV.execute('INSERT INTO genres ("name") \
                     VALUES (?)', (genre, ))
                self.sqlTV.execute('SELECT id FROM genres WHERE name=(?)', \
                 (genre, ))
                id_genre_list = self.sqlTV.fetchall()
                self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
                 (series.seriesid, ))
                id_show_list = self.sqlTV.fetchall()
                for x in id_genre_list[0]: id_genre = x
                for y in id_show_list[0]: id_show = y
                self.sqlTV.execute('INSERT INTO genrelinkshow \
                 ("idGenre", "idShow") VALUES (?, ?)', (id_genre, id_show))
            #Add the network if it isn't already there and link it up
            self.sqlTV.execute('SELECT * FROM networks WHERE name=(?)', \
             (series.network, ))
            if not len (self.sqlTV.fetchall()):
                self.sqlTV.execute('INSERT INTO networks ("name") VALUES (?)', \
                 (series.network, ))
            self.sqlTV.execute('SELECT id FROM networks WHERE name=(?)', \
             (series.network, ))
            id_network_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
             (series.seriesid, ))
            id_show_list = self.sqlTV.fetchall()
            for x in id_network_list[0]: id_network = x
            for y in id_show_list[0]: id_show = y
            self.sqlTV.execute('INSERT INTO networklinkshow \
             ("idNetwork", "idShow") VALUES (?, ?)', (id_network, id_show))
        self.dbTV.commit()

    def write_files_to_db(self, file_list, series_id):
        """Writes info about files to the database"""
        #Parse out the tuple for each file
        for file in file_list:
            file_path = file[0]
            file_name = file[1]
            file_season = file[3]
            file_episode = file[4]
            #See if the file is already in the db
            self.sqlTV.execute('SELECT * FROM files WHERE filename=(?)', \
                               (file_name, ))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO files ("filename", \
                 "filepath") VALUES (?,?)', (file_name, file_path))
            #Link the file to the appropriate episode
            self.sqlTV.execute('SELECT id FROM files WHERE filename=(?)', \
                               (file_name, ))
            id_file_list = self.sqlTV.fetchall()
            for x in id_file_list[0]: id_file = x
            self.sqlTV.execute('SELECT episodes.id FROM episodes JOIN \
             episodelinkshow ON episodelinkshow.idEpisode=episodes.id JOIN \
             shows ON episodelinkshow.idShow=shows.id WHERE shows.seriesid=(?) \
             AND episodes.season_number=(?) AND episodes.episode_number=(?)', \
             (series_id, file_season, file_episode))
            id_episode_list = self.sqlTV.fetchall()
            if not len(id_episode_list):
                episodes = [self.tvdb.get_episode_by_season_episode(\
                 series_id, file_season.lstrip('0'), file_episode.lstrip('0'))]
                if episodes[0] is not None:
                    self.write_episodes_to_db(episodes, series_id)
                    self.logger.info(\
                      "Adding Series %s, season %s, episode %s to database" \
                      % (series_id, file_season, file_episode))
                else:
                    self.logger.info("Series %s, season %s, episode %s not found on thetvdb.com" % (series_id, file_season, file_episode))
                self.sqlTV.execute('SELECT episodes.id FROM episodes \
                 JOIN episodelinkshow ON episodelinkshow.idEpisode=episodes.id \
                 JOIN shows ON episodelinkshow.idShow=shows.id \
                 WHERE shows.seriesid=(?) AND episodes.season_number=(?) \
                 AND episodes.episode_number=(?)', \
                 (series_id, file_season, file_episode))
                id_episode_list = self.sqlTV.fetchall()
            if not len(id_episode_list) < 1:
                for y in id_episode_list[0]:
                    id_episode = y
            else:
                id_episode = 00000
            self.sqlTV.execute('SELECT * FROM filelinkepisode WHERE \
             idFile=(?) and idEpisode=(?)', (id_file, id_episode))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                if not id_episode == 0:
                    self.sqlTV.execute(\
                      'INSERT INTO filelinkepisode ("idFile", "idEpisode") \
                      VALUES (?, ?)', (id_file, id_episode))
            #See if we know the video info for the file already
            self.sqlTV.execute('SELECT * FROM videolinkfile WHERE \
             idFile=(?)', (id_file,))
            if not len(self.sqlTV.fetchall()):
                #Get the meta info for the file
                formats = []
                file_fullpath = file_path + "/" + file_name
                dom = self.MediaInfo.make_info_dom(file_fullpath)
                root = dom.documentElement()
                elem_file = root.firstChildElement('File')
                elem_track = elem_file.firstChildElement('track')
                while not elem_track.isNull():
                    if elem_track.attribute('type') == 'Video':
                        elem_video = elem_track
                        elem_codec = elem_video.firstChildElement('Codec_ID')
                        if elem_codec.isNull():
                            codec = "unknown"
                        else:
                            codec = str(elem_codec.text()).lower().split('/')[-1]
                            if codec == "avc": codec = "h264"
                        elem_width = elem_video.firstChildElement('Width')
                        if elem_width.isNull():
                            width = 0
                        else:
                            width = str(elem_width.text()).strip(' pixels')
                            width = re.sub("\s+", "", width)
                        elem_height = elem_video.firstChildElement('Height')
                        if elem_height.isNull():
                            height = 0
                        else:
                            height = str(elem_height.text()).strip(' pixels')
                            height = re.sub("\s+", "", height)
                        elem_aspect = \
                         elem_video.firstChildElement('Display_aspect_ratio')
                        if elem_aspect.isNull():
                            aspect = 0
                        else:
                            aspect_sep = str(elem_aspect.text()).split(':')
                            if len(aspect_sep) < 2:
                                aspect = 0
                            else:
                                if aspect_sep[1] > 0:
                                    aspect = \
                                     float(aspect_sep[0]) / float(aspect_sep[1])
                                else:
                                    aspect = 0
                        formats.append((codec, aspect, int(width), int(height)))
                    elem_track = elem_track.nextSiblingElement('track')
                for format in formats:
                    self.sqlTV.execute('SELECT id FROM video_formats WHERE \
                     codec=(?) AND aspect=(?) AND width=(?) AND height=(?)', \
                     format)
                    id_format_list = self.sqlTV.fetchall()
                    if not len(id_format_list):
                        self.sqlTV.execute('INSERT INTO video_formats \
                         ("codec", "aspect", "width", "height") \
                         VALUES (?,?,?,?)', format)
                        self.sqlTV.execute('SELECT id FROM video_formats WHERE \
                         codec=(?) AND aspect=(?) AND width=(?) \
                         AND height=(?)', format)
                        id_format_list = self.sqlTV.fetchall()
                        for y in id_format_list[0]: id_format = int(y)
                    else:
                        for y in id_format_list[0]: id_format = int(y)
                    self.sqlTV.execute('INSERT INTO videolinkfile \
                     ("idVideoFormat", "idFile") VALUES (?, ?)', \
                     (id_format, id_file))
            self.dbTV.commit()

    def check_db_for_series_name(self, series_name):
        """See if a series with a given series_name exists in the database"""
        seriesname = '%s%s%s' % ("%", series_name, "%")
        self.sqlTV.execute("SELECT seriesid FROM shows WHERE name LIKE (?)", \
                            (seriesname,))
        series_id_list = self.sqlTV.fetchall()
        if len(series_id_list):
            for x in series_id_list[0]: series_id = x
        else:
            series_id = 0
        return series_id

    def check_db_for_file(self, file_path, file_name):
        """See if a given file exists in the database"""
        self.sqlTV.execute('SELECT id FROM files WHERE filename=(?) AND \
         filepath=(?)', (file_name, file_path))
        if len(self.sqlTV.fetchall()):
            found = 1
        else:
            found = 0
        return found

    def check_db_for_series(self, series_id):
        """See if a given series exists in the database"""
        self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        if len(self.sqlTV.fetchall()):
            found = 1
        else:
            found = 0
        return found

    def check_db_for_episode(self, episode_id):
        """See if a given episode exists in the database"""
        self.sqlTV.execute('SELECT id FROM episodes WHERE episodeid=(?)', \
         (episode_id, ))
        if len(self.sqlTV.fetchall()):
            found = 1
        else:
            found = 0
        return found

    def get_episode_id(self, seriesname, season, episode):
        """Returns the episodeid for a given seriesname, season and episode"""
        series_id = self.check_db_for_series_name(seriesname)
        self.sqlTV.execute('SELECT episodes.episodeid FROM episodelinkshow \
         JOIN episodes ON episodelinkshow.idEpisode=episodes.id JOIN shows \
         ON episodelinkshow.idShow=shows.id WHERE episodes.episode_number=(?) \
         AND episodes.season_number=(?) AND shows.seriesid=(?)', \
         (str(episode), str(season), str(series_id)))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: episode_id = x
        return episode_id

    def get_series_id(self, seriesname):
        """Returns the seriesid for a given series"""
        series_id = self.check_db_for_series_name(seriesname)
        return series_id

    def get_actor_thumb(self, actorname):
        """Returns the url of the thumbnail for a given actor"""
        self.sqlTV.execute('SELECT thumb FROM actors WHERE name=(?)', \
         (unicode(actorname, "latin-1"), ))
        value_db = self.sqlTV.fetchall()
        if len(value_db):
             for x in value_db[0]: thumburl = x
        else:
            thumburl = None 
        return thumburl
        
    def get_series_name(self, series_id):
        """Returns the series name for a given series_id"""
        self.sqlTV.execute('SELECT name FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        if len(value_db):
            for x in value_db[0]: series_name = x[1]
        else:
            series_name = None
        return series_name

    def db_query(self, sql):
        """Perform any query on the db.  Used for testing purposes only"""
        self.sqlTV.execute(sql)
        result = self.sqlTV.fetchall()
        return result

    def make_shows_dom(self):
        """Creates a QDomDocument for the shows in the database"""
        dom = QtXml.QDomDocument()
        root = dom.createElement("shows")
        dom.appendChild(root)
        self.sqlTV.execute('SELECT shows.name, episodes.season_number, \
         episodes.episode_number FROM filelinkepisode JOIN episodes \
         ON filelinkepisode.idEpisode=episodes.id JOIN episodelinkshow \
         ON episodelinkshow.idEpisode=episodes.id JOIN shows \
         ON shows.id=episodelinkshow.idShow')
        episodes = self.sqlTV.fetchall()
        episodes.sort()
        series_done = []
        season_done = []
        for episode in episodes:
            series = episode[0]
            season = episode[1]
            number = episode[2]
            if series_done.count(series):
                pass
            else:
                elem_series = dom.createElement("series")
                elem_series.setAttribute("name", series)
                root.appendChild(elem_series)
                series_done.append(series)
            if season_done.count((series, season)):
                pass
            else:
                elem_season = dom.createElement("season")
                elem_season.setAttribute("number", season)
                elem_series.appendChild(elem_season)
                season_done.append((series, season))
            elem_episode = dom.createElement("episode")
            text_episode = dom.createTextNode(str(number))
            elem_episode.appendChild(text_episode)
            elem_season.appendChild(elem_episode)
        return dom

    def make_seasons_episodes_dom(self, show):
        """Creates a QDomDocument for the shows in the database"""
        dom = QtXml.QDomDocument()
        root = dom.createElement("show")
        dom.appendChild(root)
        showname = "%s%s%s" % ("%", show, "%")
        self.sqlTV.execute('SELECT episodes.season_number, \
         episodes.episode_number, episodes.name \
         FROM filelinkepisode JOIN episodes \
         ON filelinkepisode.idEpisode=episodes.id JOIN episodelinkshow \
         ON episodelinkshow.idEpisode=episodes.id JOIN shows \
         ON shows.id=episodelinkshow.idShow WHERE shows.name LIKE (?)', \
         (showname,))
        episodes = self.sqlTV.fetchall()
        episodes.sort()
        season_done = []
        for episode in episodes:
            season = episode[0]
            number = episode[1]
            name = episode[2]
            if season_done.count(season):
                pass
            else:
                elem_season = dom.createElement("season")
                elem_season.setAttribute("number", season)
                root.appendChild(elem_season)
                season_done.append(season)
            elem_episode = dom.createElement("episode")
            elem_episode.setAttribute("number", number)
            text_episode = dom.createTextNode(name)
            elem_episode.appendChild(text_episode)
            elem_season.appendChild(elem_episode)
        return dom

    def make_episode_dom(self, episode_id):
        """Get info for an episode from the db and put in into a QDomDocument"""
        #separator for lists with multiple items (writers, directors, etc)
        sep = "|"

        dom = QtXml.QDomDocument()
        root = dom.createElement("episodedetails")
        dom.appendChild(root)

        elem_title = dom.createElement("title")
        self.sqlTV.execute("SELECT name FROM episodes WHERE episodeid=(?)", \
         (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_title = dom.createTextNode(x)
        elem_title.appendChild(text_title)
        root.appendChild(elem_title)

        elem_rating = dom.createElement("rating")
        self.sqlTV.execute('SELECT rating FROM episodes WHERE episodeid=(?)', \
         (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_rating = dom.createTextNode(x)
        elem_rating.appendChild(text_rating)
        root.appendChild(elem_rating)

        elem_year = dom.createElement("year") #0
        text_year = dom.createTextNode('0')
        elem_year.appendChild(text_year)
        root.appendChild(elem_year)

        elem_top250 = dom.createElement("top250") #0
        text_top250 = dom.createTextNode('0')
        elem_top250.appendChild(text_top250)
        root.appendChild(elem_top250)

        elem_season = dom.createElement("season")
        self.sqlTV.execute('SELECT season_number FROM episodes WHERE \
         episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]:
            text_season = dom.createTextNode(str(x))
        elem_season.appendChild(text_season)
        root.appendChild(elem_season)

        elem_episode = dom.createElement("episode")
        self.sqlTV.execute('SELECT episode_number FROM episodes WHERE \
         episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]:
            text_episode = dom.createTextNode(str(x))
        elem_episode.appendChild(text_episode)
        root.appendChild(elem_episode)

        elem_displayseason = dom.createElement("displayseason") #-1
        text_displayseason = dom.createTextNode('-1')
        elem_displayseason.appendChild(text_displayseason)
        root.appendChild(elem_displayseason)

        elem_displayepisode = dom.createElement("displayepisode") #-1
        text_displayepisode = dom.createTextNode('-1')
        elem_displayepisode.appendChild(text_displayepisode)
        root.appendChild(elem_displayepisode)

        elem_plot = dom.createElement("plot")
        self.sqlTV.execute('SELECT overview FROM episodes WHERE \
         episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]:
            text_plot = dom.createTextNode(x)
        elem_plot.appendChild(text_plot)
        root.appendChild(elem_plot)

        elem_thumb = dom.createElement("thumb")
        self.sqlTV.execute('SELECT thumb FROM episodes WHERE \
         episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]:
            text_thumb = dom.createTextNode(x)
        elem_thumb.appendChild(text_thumb)
        root.appendChild(elem_thumb)

        elem_playcount = dom.createElement("playcount")
        text_playcount = dom.createTextNode('0')
        elem_playcount.appendChild(text_playcount)
        root.appendChild(elem_playcount)

        elem_episodeid = dom.createElement("id")
        text_episodeid = dom.createTextNode(str(episode_id))
        elem_episodeid.appendChild(text_episodeid)
        root.appendChild(elem_episodeid)

        elem_credits = dom.createElement("credits") #Writers
        self.sqlTV.execute('SELECT writers.name FROM writerlinkepisode \
         JOIN episodes ON episodes.id=writerlinkepisode.idEpisode \
         JOIN writers ON writers.id=writerlinkepisode.idWriter \
         WHERE episodes.episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        writers_list = []
        for x in value_db: writers_list.append(x[0])
        credits = sep.join(writers_list)
        text_credits = dom.createTextNode(credits)
        elem_credits.appendChild(text_credits)
        root.appendChild(elem_credits)

        elem_director = dom.createElement("director")
        self.sqlTV.execute('SELECT directors.name FROM directorlinkepisode \
         JOIN episodes ON episodes.id=directorlinkepisode.idEpisode \
         JOIN directors ON directors.id=directorlinkepisode.idDirector \
         WHERE episodes.episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        directors_list = []
        for x in value_db: directors_list.append(x[0])
        director = sep.join(directors_list)
        text_director = dom.createTextNode(director)
        elem_director.appendChild(text_director)
        root.appendChild(elem_director)

        elem_code = dom.createElement("code")
        self.sqlTV.execute('SELECT prod_code FROM episodes \
         WHERE episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_code = dom.createTextNode(str(x))
        elem_code.appendChild(text_code)
        root.appendChild(elem_code)

        elem_aired = dom.createElement("aired")
        self.sqlTV.execute('SELECT first_aired FROM episodes \
         WHERE episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]:
            text_aired = dom.createTextNode(x)
        elem_aired.appendChild(text_aired)
        root.appendChild(elem_aired)

        #Get the seriesid to find the actors associated with the series
        self.sqlTV.execute('SELECT shows.seriesid FROM episodes \
         JOIN episodelinkshow ON episodes.id=episodelinkshow.idEpisode \
         JOIN shows ON shows.id=episodelinkshow.idShow \
         WHERE episodes.episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: series_id = x

        #Get all actors associated with the series itself
        self.sqlTV.execute('SELECT actors.name, actorlinkshow.role, \
         actors.thumb FROM actorlinkshow JOIN shows \
         ON shows.id=actorlinkshow.idShow JOIN actors \
         ON actors.id=actorlinkshow.idActor \
         WHERE shows.seriesid=(?)', (series_id, ))
        value_db = self.sqlTV.fetchall()
        actors_list = []
        for x in value_db: actors_list.append(x)

        #Then get the actors associated with this episode only
        self.sqlTV.execute('SELECT actors.name, actorlinkepisode.role, \
         actors.thumb FROM actorlinkepisode JOIN episodes \
         ON episodes.id=actorlinkepisode.idEpisode JOIN actors \
         ON actors.id=actorlinkepisode.idActor \
         WHERE episodes.episodeid=(?)', (episode_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db: actors_list.append(x)

        for x in actors_list:
            elem_actor = dom.createElement("actor")
            elem_actor_name = dom.createElement("name")
            elem_actor_role = dom.createElement("role")
            elem_actor_thumb = dom.createElement("thumb")
            text_actor_name = dom.createTextNode(QtCore.QString(x[0]))
            if x[1] == None:
                text_actor_role = dom.createTextNode("")
            else:
                text_actor_role = dom.createTextNode(QtCore.QString(x[1]))
            if x[2] == None:
                text_actor_thumb = dom.createTextNode("")
            else:
                text_actor_thumb = dom.createTextNode(QtCore.QString(x[2]))
            elem_actor_name.appendChild(text_actor_name)
            elem_actor_role.appendChild(text_actor_role)
            elem_actor_thumb.appendChild(text_actor_thumb)
            elem_actor.appendChild(elem_actor_name)
            elem_actor.appendChild(elem_actor_role)
            elem_actor.appendChild(elem_actor_thumb)
            root.appendChild(elem_actor)

        return dom

    def make_series_dom(self, series_id):
        """Get info for a series from the db and put in into an ElementTree"""
        #separator for lists with multiple items (genres, etc)
        sep = "|"

        dom = QtXml.QDomDocument()
        root = dom.createElement("tvshow")
        dom.appendChild(root)

        elem_title = dom.createElement("title")
        self.sqlTV.execute('SELECT name FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_title = dom.createTextNode(x)
        elem_title.appendChild(text_title)
        root.appendChild(elem_title)

        elem_rating = dom.createElement("rating")
        self.sqlTV.execute('SELECT rating FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_rating = dom.createTextNode(x)
        elem_rating.appendChild(text_rating)
        root.appendChild(elem_rating)

        elem_year = dom.createElement("year") #empty for TV
        text_year = dom.createTextNode("0")
        elem_year.appendChild(text_year)
        root.appendChild(elem_year)

        elem_top250 = dom.createElement("top250") #empty for TV
        text_top250 = dom.createTextNode("0")
        elem_top250.appendChild(text_top250)
        root.appendChild(elem_top250)

        elem_season = dom.createElement("season") #-1 for TV
        text_season = dom.createTextNode("-1")
        elem_season.appendChild(text_season)
        root.appendChild(elem_season)

        elem_episode = dom.createElement("episode")
        self.sqlTV.execute('SELECT files.id, count(0) FROM filelinkepisode \
         JOIN files ON filelinkepisode.idFile=files.id JOIN episodelinkshow \
         ON episodelinkshow.idEpisode=filelinkepisode.idEpisode JOIN shows \
         ON shows.id=episodelinkshow.idShow \
         WHERE shows.seriesid=(?)', (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_episode = dom.createTextNode(str(x))
        elem_episode.appendChild(text_episode)
        root.appendChild(elem_episode)

        elem_displayseason = dom.createElement("displayseason")
        text_displayseason = dom.createTextNode("-1")
        elem_displayseason.appendChild(text_displayseason)
        root.appendChild(elem_displayseason)

        elem_votes = dom.createElement("votes")
        text_votes = dom.createTextNode("0")
        elem_votes.appendChild(text_votes)
        root.appendChild(elem_votes)

        elem_plot = dom.createElement("plot")
        self.sqlTV.execute('SELECT overview FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_plot = dom.createTextNode(x)
        elem_plot.appendChild(text_plot)
        root.appendChild(elem_plot)

        elem_runtime = dom.createElement("runtime")
        self.sqlTV.execute('SELECT runtime FROM shows WHERE seriesid=(?)', \
         (series_id,))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_runtime = dom.createTextNode(str(x))
        elem_runtime.appendChild(text_runtime)
        root.appendChild(elem_runtime)

        elem_network = dom.createElement("network")
        self.sqlTV.execute('SELECT networks.name FROM networklinkshow \
         JOIN networks ON networklinkshow.idNetwork=networks.id \
         JOIN shows on networklinkshow.idShow=shows.id \
         WHERE shows.seriesid=(?)', (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_network = dom.createTextNode(x)
        elem_network.appendChild(text_network)
        root.appendChild(elem_network)

        elem_airs_day = dom.createElement("airsday")
        self.sqlTV.execute('SELECT airs_day FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_airs_day = dom.createTextNode(x)
        elem_airs_day.appendChild(text_airs_day)
        root.appendChild(elem_airs_day)

        elem_airs_time = dom.createElement("airstime")
        self.sqlTV.execute('SELECT airs_time FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_airs_time = dom.createTextNode(x)
        elem_airs_time.appendChild(text_airs_time)
        root.appendChild(elem_airs_time)

        self.sqlTV.execute('SELECT banners.path, banners.type, banners.type2, \
         banners.colors, banners.thumbnailPath, banners.season, banners.url \
         FROM bannerlinkshow JOIN shows ON shows.id=bannerlinkshow.idShow \
         JOIN banners ON banners.id=bannerlinkshow.idBanner \
         WHERE shows.seriesid=(?)', (series_id,))
        value_db = self.sqlTV.fetchall()
        banners_list = []
        for x in value_db: banners_list.append(x)
        elem_fanart = dom.createElement("fanart")
        elem_fanart.setAttribute("url", "%s/" % (banners_list[0][6],))
        for y in banners_list:
            if y[1] == "fanart":
                elem_thumb = dom.createElement("thumb")
                elem_thumb.setAttribute("dim", y[2])
                elem_thumb.setAttribute("colors", y[3])
                elem_thumb.setAttribute("preview", y[4])
                text_thumb = dom.createTextNode(y[0])
                elem_thumb.appendChild(text_thumb)
                elem_fanart.appendChild(elem_thumb)
            elif y[1] == "season":
                elem_thumb = dom.createElement("thumb")
                elem_thumb.setAttribute("type", y[1])
                elem_thumb.setAttribute("season", str(y[5]))
                text_thumb = dom.createTextNode("%s/%s" % (y[6], y[0]))
                elem_thumb.appendChild(text_thumb)
                root.appendChild(elem_thumb)
            else:
                elem_thumb = dom.createElement("thumb")
                text_thumb = dom.createTextNode("%s/%s" % (y[6], y[0]))
                elem_thumb.appendChild(text_thumb)
                root.appendChild(elem_thumb)
        root.appendChild(elem_fanart)

        elem_episodeguide = dom.createElement("episodeguide")
        self.sqlTV.execute('SELECT episodeguide FROM shows WHERE seriesid=(?)', \
         (series_id, ))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]:
            if x is not None:
                text_episodeguide = dom.createTextNode(x)
                elem_episodeguide.appendChild(text_episodeguide)
                root.appendChild(elem_episodeguide)

        elem_seriesid = dom.createElement("id")
        text_seriesid = dom.createTextNode(str(series_id))
        elem_seriesid.appendChild(text_seriesid)
        root.appendChild(elem_seriesid)

        elem_genre = dom.createElement("genre")
        self.sqlTV.execute('SELECT genres.name FROM genrelinkshow JOIN shows \
         ON shows.id=genrelinkshow.idShow JOIN genres \
         ON genres.id=genrelinkshow.idGenre \
         WHERE shows.seriesid=(?)', (series_id,))
        value_db = self.sqlTV.fetchall()
        genres_list = []
        for x in value_db: genres_list.append(x[0])
        genres = sep.join(genres_list)
        text_genres = dom.createTextNode(genres)
        elem_genre.appendChild(text_genres)
        root.appendChild(elem_genre)

        elem_premiered = dom.createElement("premiered")
        self.sqlTV.execute('SELECT first_aired FROM shows WHERE seriesid=(?)', \
         (series_id,))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_premiered = dom.createTextNode(x)
        elem_premiered.appendChild(text_premiered)
        root.appendChild(elem_premiered)

        elem_status = dom.createElement("status")
        self.sqlTV.execute('SELECT status FROM shows WHERE seriesid=(?)', \
         (series_id,))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: text_status = dom.createTextNode(x)
        elem_status.appendChild(text_status)
        root.appendChild(elem_status)

        self.sqlTV.execute('SELECT actors.name, actorlinkshow.role, \
         actors.thumb FROM actorlinkshow JOIN shows \
         ON shows.id=actorlinkshow.idShow JOIN actors \
         ON actors.id=actorlinkshow.idActor WHERE shows.seriesid=(?)', \
         (series_id,))
        value_db = self.sqlTV.fetchall()
        actors_list = []
        for x in value_db: actors_list.append(x)
        for y in actors_list:
            elem_actor = dom.createElement("actor")
            elem_actor_name = dom.createElement("name")
            elem_actor_role = dom.createElement("role")
            elem_actor_thumb = dom.createElement("thumb")
            text_actor_name = dom.createTextNode(QtCore.QString(y[0]))
            if x[1] == None:
                text_actor_role = dom.createTextNode("")
            else:
                text_actor_role = dom.createTextNode(QtCore.QString(y[1]))
            if x[2] == None:
                text_actor_thumb = dom.createTextNode("")
            else:
                text_actor_thumb = dom.createTextNode(QtCore.QString(y[2]))
            elem_actor_name.appendChild(text_actor_name)
            elem_actor_role.appendChild(text_actor_role)
            elem_actor_thumb.appendChild(text_actor_thumb)
            elem_actor.appendChild(elem_actor_name)
            elem_actor.appendChild(elem_actor_role)
            elem_actor.appendChild(elem_actor_thumb)
            root.appendChild(elem_actor)

        return dom

    def make_episodes_list(self, series_id, season_number):
        """Get a list of all episodes in a give season"""
        self.sqlTV.execute("SELECT episodes.episode_number, episodes.name \
         FROM shows JOIN episodelinkshow ON episodelinkshow.idShow=shows.id \
         JOIN episodes ON episodelinkshow.idEpisode=episodes.id WHERE \
         shows.seriesid=(?) AND episodes.season_number=(?)", \
         (series_id, season_number))
        reply = self.sqlTV.fetchall()
        return reply

    def make_shows_list(self):
        """Creates a list of shows in the database"""
        show_list = []
        self.sqlTV.execute('SELECT name FROM shows')
        shows = self.sqlTV.fetchall()
        for show in shows:
            show_list.append(show[0])
        show_list.sort()
        return show_list

    def update_series_to_db(self, series):
        """Updates info for a series in the database"""
        self.sqlTV.execute('UPDATE shows SET name=?, overview=?, \
         content_rating=?, runtime=?, status=?, language=?, first_aired=?, \
         airs_day=?, airs_time=?, rating=? WHERE seriesid=?', \
         (series.name, series.overview, series.content_rating, \
         int(series.runtime), series.status, series.language, \
         series.first_aired, series.airs_day, series.airs_time, \
         series.rating, int(series.seriesid)))
        for genre in series.genre:
            self.sqlTV.execute('SELECT * FROM genres WHERE name=(?)', (genre, ))
            if len (self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO genres ("name") VALUES (?)', \
                 (genre, ))
            self.sqlTV.execute('SELECT id FROM genres WHERE name=(?)', \
             (genre, ))
            id_genre_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
             (series.seriesid, ))
            id_show_list = self.sqlTV.fetchall()
            for x in id_genre_list[0]: id_genre = x
            for y in id_show_list[0]: id_show = y
            self.sqlTV.execute('SELECT * FROM genrelinkshow WHERE idGenre=(?) \
             AND idShow=(?)', (id_genre, id_show))
            if len (self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO genrelinkshow \
                 ("idGenre", "idShow") VALUES (?, ?)', (id_genre, id_show))
        self.sqlTV.execute('SELECT * FROM networks WHERE name=(?)', \
         (series.network, ))
        if len (self.sqlTV.fetchall()):
            pass
        else:
            self.sqlTV.execute('INSERT INTO networks ("name") VALUES (?)', \
             (series.network, ))
        self.sqlTV.execute('SELECT id FROM networks WHERE name=(?)', \
         (series.network, ))
        id_network_list = self.sqlTV.fetchall()
        self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
         (series.seriesid, ))
        id_show_list = self.sqlTV.fetchall()
        for x in id_network_list[0]: id_network = x
        for y in id_show_list[0]: id_show = y
        self.sqlTV.execute('SELECT * FROM networklinkshow WHERE idNetwork=(?) \
         AND idShow=(?)', (id_network, id_show))
        if len (self.sqlTV.fetchall()):
            pass
        else:
            self.sqlTV.execute('INSERT INTO networklinkshow \
             ("idNetwork", "idShow") VALUES (?, ?)', (id_network, id_show))
        self.dbTV.commit()

    def update_episode_to_db(self, episode):
        """Updates info for a single episode in the database"""
        self.sqlTV.execute('UPDATE episodes SET name=?, overview=?, \
         season_number=?, episode_number=?, language=?, prod_code=?, \
         rating=?, first_aired=? WHERE episodeid=(?)', \
         (episode.episode_name, episode.overview, episode.season_number, \
         episode.episode_number, episode.language, episode.production_code, \
         episode.rating, episode.first_aired, episode.episodeid))
        for guest in episode.guest_stars:
            self.sqlTV.execute('SELECT * FROM actors WHERE name=(?)', (guest, ))
            if len (self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO actors ("name") VALUES (?)', \
                 (guest, ))
            self.sqlTV.execute('SELECT id FROM actors WHERE name=(?)', \
             (guest, ))
            id_guest_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM episodes WHERE episodeid=(?)', \
             (episode.episodeid, ))
            id_episode_list = self.sqlTV.fetchall()
            for x in id_guest_list[0]: id_guest = x
            for y in id_episode_list[0]: id_episode = y
            self.sqlTV.execute('SELECT * FROM actorlinkepisode WHERE \
             idActor=(?) AND idEpisode=(?)', (id_guest, id_episode))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO actorlinkepisode \
                 ("idActor", "idEpisode") VALUES (?, ?)', \
                 (id_guest, id_episode))
        for director in episode.directors:
            self.sqlTV.execute('SELECT * FROM directors WHERE name=(?)', \
             (director, ))
            if len (self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO directors ("name") \
                 VALUES (?)', (director, ))
            self.sqlTV.execute('SELECT id FROM directors WHERE name=(?)', \
             (director, ))
            id_director_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM episodes WHERE episodeid=(?)', \
             (episode.episodeid, ))
            id_episode_list = self.sqlTV.fetchall()
            for x in id_director_list[0]: id_director = x
            for y in id_episode_list[0]: id_episode = y
            self.sqlTV.execute('SELECT * FROM directorlinkepisode WHERE \
             idDirector=(?) AND idEpisode=(?)', (id_director, id_episode))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO directorlinkepisode \
                 ("idDirector", "idEpisode") VALUES (?, ?)', \
                 (id_director, id_episode))
        for writer in episode.writers:
            self.sqlTV.execute('SELECT * FROM writers WHERE name=(?)', \
             (writer, ))
            if len (self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO writers ("name") \
                 VALUES (?)', (writer, ))
            self.sqlTV.execute('SELECT id FROM writers WHERE name=(?)', \
             (writer, ))
            id_writer_list = self.sqlTV.fetchall()
            self.sqlTV.execute('SELECT id FROM episodes WHERE episodeid=(?)', \
             (episode.episodeid, ))
            id_episode_list = self.sqlTV.fetchall()
            for x in id_writer_list[0]: id_writer = x
            for y in id_episode_list[0]: id_episode = y
            self.sqlTV.execute('SELECT * FROM writerlinkepisode WHERE \
             idWriter=(?) AND idEpisode=(?)', (id_writer, id_episode))
            if len(self.sqlTV.fetchall()):
                pass
            else:
                self.sqlTV.execute('INSERT INTO writerlinkepisode \
                 ("idWriter", "idEpisode") VALUES (?, ?)', \
                 (id_writer, id_episode))
        self.dbTV.commit()

    def update_series_field(self, field, value, seriesid):
        sql = "UPDATE shows SET %s=(?) WHERE seriesid=(?)" % (field,)
        self.sqlTV.execute(sql, (value, seriesid))
        self.sqlTV.execute('SELECT id FROM shows WHERE seriesid=(?)', \
         (seriesid,))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: id = x
        self.sqlTV.execute('SELECT idShow FROM modified_shows WHERE \
         idShow=(?)', (id,))
        if not len(self.sqlTV.fetchall()):
            self.sqlTV.execute('INSERT INTO modified_shows ("idShow") \
             VALUES (?)', (id,))
        self.dbTV.commit()

    def update_episode_field(self, field, value, episodeid):
        sql = "UPDATE episodes SET %s=(?) WHERE episodeid=(?)" % (field,)
        self.sqlTV.execute(sql, (value, episodeid))
        self.sqlTV.execute('SELECT id FROM episodes WHERE episodeid=(?)', \
         (episodeid,))
        value_db = self.sqlTV.fetchall()
        for x in value_db[0]: id = x
        self.sqlTV.execute('SELECT idEpisode FROM modified_episodes WHERE \
         idEpisode=(?)', (id,))
        if not len(self.sqlTV.fetchall()):
            self.sqlTV.execute('INSERT INTO modified_episodes ("idEpisode") \
             VALUES (?)', (id,))
        self.dbTV.commit()

    def update_db(self):
        """Check the database against thetvdb.com for updates"""
        #Get the time of the last update for comparison (from the DB)
        last_update_time = self.get_update_time()

        #Update any episodes and series which have been changed
        #  since the last update
        self.logger.info("Getting Episode Update List")
        episode_update_list = \
         self.tvdb.get_episode_update_list(last_update_time)
        self.logger.info("Getting Series Update List")
        series_update_list = self.tvdb.get_series_update_list(last_update_time)
        for episode_id in episode_update_list:
            if self.check_db_for_episode(episode_id):
                self.logger.info("Updating info for episode %s" \
                                 % (episode_id,))
                episode = self.tvdb.get_episode_by_id(episode_id)
                self.update_episode_to_db(episode)
        for series_id in series_update_list:
           if self.check_db_for_series(series_id):
                self.logger.info("Updating info for series %s" % (series_id,))
                series = self.tvdb.get_series_by_id(series_id)
                episodes = self.tvdb.get_episodes_by_series_id(series_id)
                episode_list = []
                self.update_series_to_db(series)
                for episode in episodes:
                    episode_id = episode.episodeid
                    if not self.check_db_for_episode(episode_id):
                        self.logger.info("Adding info for episode %s" % (episode_id,))
                        episode_list.append(episode)
                if len(episode_list):
                    self.write_episodes_to_db(episode_list, series_id)

    def clean_db_files(self):
        """Cleans missing files out of the database"""
        self.logger.info("Checking for missing files.")
        self.sqlTV.execute('SELECT filepath, filename FROM files')
        files = self.sqlTV.fetchall()
        for file in files:
            fullpath = os.path.join(str(file[0]), str(file[1]))
            if not os.path.exists(fullpath):
                self.logger.info("Removing %s" % (str(file[1]),))
                self.sqlTV.execute('DELETE FROM files WHERE filename=(?)', \
                 (str(file[1]),))
        self.sqlTV.execute('SELECT idFile FROM filelinkepisode')
        linked_files = self.sqlTV.fetchall()
        for link in linked_files:
            self.sqlTV.execute('SELECT filename FROM files WHERE id=(?)', \
             (int(link[0]),))
            if not len(self.sqlTV.fetchall()):
                self.sqlTV.execute('DELETE FROM filelinkepisode \
                 WHERE idFile=(?)', (int(link[0]),))
        self.dbTV.commit()

    def link_selected_banner_show(self, show, url):
        """Links selected banner to specific show"""
        self.sqlTV.execute('SELECT DISTINCT url FROM banners')
        base_url_results = self.sqlTV.fetchall()
        base_urls = []
        for base_url in base_url_results:
            base_urls.append("%s/" % str(base_url[0]))
        for base_url in base_urls:
            url = url.replace(base_url, '')
        url = url.replace('/_cache/', '')
        search_url = "%s%s%s" % ("%", url, "%")
        self.sqlTV.execute( \
          'SELECT id, type, type2, season FROM banners WHERE path LIKE (?)', \
           (search_url,))
        banner_id, banner_type, banner_type2, banner_season = \
          self.sqlTV.fetchall()[0]
        if banner_type == 'season':
            banner_type = banner_type2
        search_name = "%s%s%s" % ("%", show, "%")
        self.sqlTV.execute('SELECT id FROM shows WHERE name LIKE (?)', \
                           (search_name,))
        show_id = self.sqlTV.fetchall()[0][0]
        self.sqlTV.execute('SELECT idBanner FROM selectedbannerlinkshow \
                            WHERE idShow LIKE (?) \
                            AND type LIKE (?) \
                            AND season LIKE (?)', \
                           (show_id, banner_type, banner_season))
        result = self.sqlTV.fetchall()
        for link in result:
            banner_id_del = link[0]
            self.sqlTV.execute('DELETE FROM selectedbannerlinkshow \
                                WHERE idBanner=(?)', (int(banner_id_del),))
        self.sqlTV.execute('INSERT INTO selectedbannerlinkshow ("idBanner", \
                 "idShow", "type", "season") VALUES (?, ?, ?, ?)', \
                 (banner_id, show_id, banner_type, banner_season))
        self.dbTV.commit()

    def get_selected_banner_url(self, series_id, type, season):
        self.sqlTV.execute('SELECT banners.url, banners.path \
          FROM selectedbannerlinkshow JOIN banners \
          ON selectedbannerlinkshow.idBanner=banners.id JOIN shows \
          ON selectedbannerlinkshow.idShow=shows.id \
          WHERE shows.seriesid=(?) AND selectedbannerlinkshow.type=(?) \
          AND selectedbannerlinkshow.season=(?)', (series_id, type, season))
        try:
            base_url, path = self.sqlTV.fetchall()[0]
            url = "%s/%s" % (base_url, path)
        except IndexError:
            url = ""
        return url

    def get_series_nfo_filename(self, series_id):
        self.sqlTV.execute('SELECT DISTINCT files.filepath FROM \
          filelinkepisode JOIN files ON filelinkepisode.idFile=files.id JOIN \
          episodelinkshow ON filelinkepisode.idEpisode=episodelinkshow.idEpisode \
          JOIN shows ON episodelinkshow.idShow=shows.id WHERE shows.seriesid=(?)', \
          (series_id,))
        filepaths = self.sqlTV.fetchall()
        paths = []
        for filepath in filepaths:
            path = re.sub('[S|s]eason[ |_][0-9]*', '', str(filepath[0]))
            if path not in paths:
                paths.append(path)
        path = paths[0]
        nfo_file = os.path.join(path, "tvshow.nfo")
        return nfo_file 

    def write_series_nfo(self, series_id):
        nfo_file = self.get_series_nfo_filename(series_id)
        dom = self.make_series_dom(series_id)
        self.logger.info("Saving %s" % (nfo_file,))
        nfo = open(nfo_file, "w")
        nfo.write(dom.toString(4))
        nfo.close()

    def write_series_posters(self, series_id):
        path = self.get_series_nfo_path(series_id)
        self.sqlTV.execute('SELECT banners.url, banners.path, \
          banners.type, banners.type2, banners.season \
          FROM selectedbannerlinkshow JOIN banners ON \
          selectedbannerlinkshow.idBanner=banners.id JOIN shows ON \
          selectedbannerlinkshow.idShow=shows.id WHERE shows.seriesid=(?)', \
          (series_id,))
        banners = self.sqlTV.fetchall()
        banner_urls = []
        for banner in banners:
            banner_urls.append(("%s/%s" % (str(banner[0]), str(banner[1])), \
                                str(banner[2]), str(banner[3]), str(banner[4])))
        for banner in banner_urls:
            if banner[1] == 'poster':
                outfile = "season-all.tbn"
            elif banner[1] == 'series':
                outfile = "folder.jpg"
            elif banner[1] == 'season':
                if banner[2] == 'season':
                    if str(banner[3]) == '0':
                        outfile = "season-specials.tbn"
                    else:
                        outfile = "%s%s.tbn" % ("season", str(banner[3]).zfill(2))
                elif banner[2] == 'seasonwide':
                    outfile = None
            elif banner[1] == 'fanart':
                outfile = "fanart.jpg"
            if outfile is not None:
                filename = os.path.join(path, outfile)
                self.logger.info("Saving %s" % (filename,))
                urllib.urlretrieve(banner[0], filename)

    def get_episode_nfo_filename(self, episode_id):
        self.sqlTV.execute("SELECT files.filename, files.filepath FROM \
          filelinkepisode JOIN files ON files.id=filelinkepisode.idFile \
          JOIN episodes ON filelinkepisode.idEpisode=episodes.id WHERE \
          episodes.episodeid=(?)", (episode_id,))
        try:
            filename, filepath = self.sqlTV.fetchall()[0]
            filename = os.path.splitext(filename)[0]
            nfo_file = os.path.join(filepath, "%s.nfo" % filename)
            return nfo_file
        except IndexError:
            self.logger.error("Error processing episode %s." % (episode_id,))
            return None

    def write_episode_nfo(self, episode_id):
        dom = self.make_episode_dom(episode_id)
        nfo_file = self.get_episode_nfo_filename(episode_id)
        if nfo_file is not None:
            self.logger.info("Saving %s" % (nfo_file,))
            nfo = open(nfo_file, "w")
            nfo.write(dom.toString(4))
            nfo.close()

    def write_all_episode_nfos(self, series_id):
        self.sqlTV.execute('SELECT episodes.episodeid FROM episodelinkshow \
          JOIN shows ON episodelinkshow.idShow=shows.id \
          JOIN episodes ON episodelinkshow.idEpisode=episodes.id \
          JOIN filelinkepisode ON episodes.id=filelinkepisode.idEpisode \
          WHERE shows.seriesid=(?)', (series_id,))
        episodes = self.sqlTV.fetchall()
        for episode in episodes:
            episode_id = episode[0]
            self.write_episode_nfo(episode_id)

    def write_episode_thumb(self, episode_id):
        self.sqlTV.execute("SELECT files.filename, files.filepath, episodes.thumb \
          FROM filelinkepisode JOIN files ON files.id=filelinkepisode.idFile \
          JOIN episodes ON filelinkepisode.idEpisode=episodes.id WHERE \
          episodes.episodeid=(?)", (episode_id,))
        try:
            filename, filepath, url = self.sqlTV.fetchall()[0]
            filename = os.path.splitext(filename)[0]
            dom = self.make_episode_dom(episode_id)
            thumb_file = os.path.join(filepath, "%s.tbn" % filename)
            if not url == '':
                self.logger.info("Saving %s" % (thumb_file,))
                urllib.urlretrieve(url, thumb_file)
        except (IndexError, IOError):
            self.logger.error("Error processing episode %s." % (episode_id,))

    def write_all_episode_thumbs(self, series_id):
        self.sqlTV.execute('SELECT episodes.episodeid FROM episodelinkshow \
          JOIN shows ON episodelinkshow.idShow=shows.id \
          JOIN episodes ON episodelinkshow.idEpisode=episodes.id \
          JOIN filelinkepisode ON episodes.id=filelinkepisode.idEpisode \
          WHERE shows.seriesid=(?)', (series_id,))
        episodes = self.sqlTV.fetchall()
        for episode in episodes:
            episode_id = episode[0]
            self.write_episode_thumb(episode_id)

    def get_all_episode_ids(self, series_id):
        episode_ids = []
        self.sqlTV.execute('SELECT episodes.episodeid FROM episodelinkshow \
          JOIN shows ON episodelinkshow.idShow=shows.id \
          JOIN episodes ON episodelinkshow.idEpisode=episodes.id \
          JOIN filelinkepisode ON episodes.id=filelinkepisode.idEpisode \
          WHERE shows.seriesid=(?)', (series_id,))
        episodes = self.sqlTV.fetchall()
        for episode in episodes:
            episode_ids.append(episode[0])
        return episode_ids
