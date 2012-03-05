############################################################################
#    Copyright (C) 2009 by Joel Means,,,                                   #
#    means.joel@gmail.com                                                  #
#                                                                          #
#    This program is free software; you can redistribute it and/or modify  #
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

import string
import urllib
import urllib2
import zipfile
import cStringIO
import os
import re
import logging
from PyQt4 import QtXml
from configuration import Config

dvdorder = True

class TVDB(object):
    """
    The main interface to thetvdb.com.

    This object provides many methods for retrieving information from
    thetvdb.com using their developer's API.
    """
    def __init__(self):
        self.logger = logging.getLogger('pymetadatamanager.tvdb')
        # Define how we connect to thetvdb.com
        self.tvdb_apikey = "2A5FFFB6E15B508A"
        self.tvdb_mirror_url = "http://www.thetvdb.com"
        self.tvdb_api_url = self.tvdb_mirror_url + "/api"
        self.tvdb_apikey_url = self.tvdb_api_url + "/" + self.tvdb_apikey
        self.tvdb_banner_url = self.tvdb_mirror_url  + "/banners"
        self.lang = "en"
        config = Config()
        self.cache_dir = os.path.join(config.config_dir, "cache")
        if os.path.exists(self.cache_dir):
            if not os.path.isdir(self.cache_dir):
                os.remove(self.cache_dir)
                os.mkdir(self.cache_dir)
        else:
            os.mkdir(self.cache_dir)

    class Series(object):
        """Class to hold info about a series"""
        def __init__(self, node, url):
            self.episodeguide = url
            self.seriesid = int(node.firstChildElement("id").text())
            self.actors = [actor.strip() for actor in \
              unicode(node.firstChildElement("Actors").text(), \
                      "latin-1").split("|") if actor]
            self.airs_day = str(\
              node.firstChildElement("Airs_DayOfWeek").text())
            self.airs_time = str(node.firstChildElement("Airs_Time").text())
            self.content_rating = str(\
              node.firstChildElement("ContentRating").text())
            self.first_aired = str(node.firstChildElement("FirstAired").text())
            self.genre = [genre.strip() for genre in \
              str(node.firstChildElement("Genre").text()).split("|") if genre]
            self.language = str(node.firstChildElement("Language").text())
            self.network = str(node.firstChildElement("Network").text())
            self.overview = unicode(node.firstChildElement("Overview").text(), \
                                    "latin-1")
            self.rating = str(node.firstChildElement("Rating").text())
            self.runtime = str(node.firstChildElement("Runtime").text())
            if self.runtime == '':
                self.runtime = '0'
            self.name = str(node.firstChildElement("SeriesName").text())
            self.status = str(node.firstChildElement("Status").text())
            self.banner = str(node.firstChildElement("banner").text())
            self.fanart = str(node.firstChildElement("fanart").text())
            self.poster = str(node.firstChildElement("poster").text())
            self.last_updated = str(\
              node.firstChildElement("lastupdated").text())

    class Episode(object):
        """Class to hold info about an episode"""
        def __init__(self, node, tvdb_banner_url):
            self.episodeid = int(node.firstChildElement("id").text())
            self.directors = [director.strip() for director in \
              unicode(node.firstChildElement("Director").text(), \
                      "latin-1").split("|") if director]
            self.episode_name = unicode(\
              node.firstChildElement("EpisodeName").text(), "latin-1")
            dvd_ep = node.firstChildElement("DVD_episodenumber").text()
            if not dvd_ep == '' and dvdorder:
                self.episode_number = int(\
                  node.firstChildElement("DVD_episodenumber").text().split('.')[0])
            else:
                self.episode_number = int(\
                  node.firstChildElement("EpisodeNumber").text())
            self.first_aired = str(node.firstChildElement("FirstAired").text())
            self.guest_stars = [guest.strip() for guest in \
              unicode(node.firstChildElement("GuestStars").text(), \
                      "latin-1").split("|") if guest]
            self.language = str(node.firstChildElement("Language").text())
            self.overview = unicode(\
              node.firstChildElement("Overview").text(), "latin-1")
            self.production_code = \
              str(node.firstChildElement("ProductionCode").text())
            self.rating = str(node.firstChildElement("Rating").text())
            self.season_number = int(\
              node.firstChildElement("SeasonNumber").text())
            self.writers = [writer.strip() for writer in \
              unicode(node.firstChildElement("Writer").text(), \
                      "latin-1").split("|") if writer]
            thumb_path = str(node.firstChildElement("filename").text())
            if not thumb_path == "":
                self.thumb = "%s/%s" % (tvdb_banner_url, thumb_path)
            else:
                self.thumb = ""
            self.last_updated = node.firstChildElement("lastupdated").text()

    class Actor(object):
        """Class to hold actor info"""
        def __init__(self, node, seriesid, tvdb_banner_url):
            self.seriesid = seriesid
            self.actorid = unicode(node.firstChildElement("id").text(), \
                                   "latin-1")
            thumbnail = str(node.firstChildElement("Image").text())
            if not thumbnail == "":
                self.thumb = "%s/%s" % (tvdb_banner_url, thumbnail)
            else:
                self.thumb = "none"
            self.name = unicode(node.firstChildElement("Name").text(), \
                                "latin-1")
            self.role = unicode(node.firstChildElement("Role").text(), \
                                "latin-1")

    class Banner(object):
        """Class to hold banner info"""
        def __init__(self, node, seriesid, tvdb_banner_url):
            self.seriesid = seriesid
            self.id = int(node.firstChildElement("id").text())
            self.path = str(node.firstChildElement("BannerPath").text())
            self.type = str(node.firstChildElement("BannerType").text())
            self.type2 = str(node.firstChildElement("BannerType2").text())
            self.colors = str(node.firstChildElement("Colors").text())
            self.season = str(node.firstChildElement("Season").text())
            self.thumb = str(node.firstChildElement("ThumbnailPath").text())
            self.url = tvdb_banner_url

    def get_server_time(self):
        """Gets the current server time.  Needed for updates"""
        updates_args = urllib.urlencode({"type": "none"}, doseq = True)
        tvdb_time_url = "%s/Updates.php?%s" % (self.tvdb_api_url, updates_args)
        try:
            server_time = urllib2.urlopen(tvdb_time_url)
        except urllib2.HTTPError, e:
            return None
        dom = QtXml.QDomDocument()
        dom.setContent(server_time.read())
        item = dom.firstChildElement("Items")
        time_element = item.firstChildElement("Time")
        return time_element.text()

    def get_series_update_list(self, last_time):
        """Gets a list of updated series since last_time"""
        updates_args = urllib.urlencode({"type": "all", "time": last_time}, \
         doseq = True)
        tvdb_update_url = "%s/Updates.php?%s" % (self.tvdb_api_url, \
         updates_args)
        try:
            updates = urllib2.urlopen(tvdb_update_url)
        except urllib2.HTTPError, e:
            return None
        series_list = []
        if updates:
            try:
                dom = QtXml.QDomDocument()
                dom.setContent(updates.read())
                items = dom.firstChildElement("Items")
                series_element = items.firstChildElement("Series")
                while not series_element.isNull():
                    series_list.append(str(series_element.text()))
                    series_element = \
                                   series_element.nextSiblingElement("Series")
            except SyntaxError:
                pass
        return series_list

    def get_episode_update_list(self, last_time):
        """Gets list of updated episodes since last_time"""
        updates_args = urllib.urlencode({"type": "all", "time": last_time}, \
         doseq = True)
        tvdb_update_url = "%s/Updates.php?%s" % (self.tvdb_api_url, \
         updates_args)
        try:
            updates = urllib2.urlopen(tvdb_update_url)
        except urllib2.HTTPError, e:
           return None
        episode_list = []
        if updates:
            try:
                dom = QtXml.QDomDocument()
                dom.setContent(updates.read())
                items = dom.firstChildElement("Items")
                episode_element = items.firstChildElement("Episode")
                while not episode_element.isNull():
                    episode_list.append(str(episode_element.text()))
                    episode_element = \
                                  episode_element.nextSiblingElement("Episode")
            except SyntaxError:
                pass
        return episode_list

    def find_series(self, series_name):
        """Finds matches for name "series_name" from thetvdb.com

        This function queries thetvdb.com for "series_name".  If an
        exact match is found in the results, the seriesid for that 
        series is returned.  If an exact match is not found, a list
        of possible matches is presented and the user is asked to 
        input the ID of the correct show."""
        series_args = urllib.urlencode({"seriesname": series_name}, \
         doseq=True)
        series_search_url = "%s/GetSeries.php?%s" % (self.tvdb_api_url, \
         series_args)
        try:
           matches = urllib2.urlopen(series_search_url)
        except urllib2.HTTPError, e:
           return None
        match_list = []
        seriesid = 0
        if matches:
            try:
                dom = QtXml.QDomDocument()
                dom.setContent(matches.read())
                data = dom.firstChildElement("Data")
                series_node = data.firstChildElement("Series")
                while not series_node.isNull():
                    match_id = str(\
                          series_node.firstChildElement("seriesid").text())
                    match_name = str(\
                          series_node.firstChildElement("SeriesName").text())
                    match_list.append((match_id, match_name))
                    series_node = series_node.nextSiblingElement("Series")
            except SyntaxError:
                self.logger.info("No possible matches found for %s." % (series_name))
        return match_list 

    def get_series_all_by_id(self, series_id):
        """Grabs the information for series with id "series_id" """
        xml_file_in_zip = "%s.xml" % (self.lang,)
        series_info_url = "%s/series/%s/all/%s.zip" % \
          (self.tvdb_apikey_url, series_id, self.lang)
        try:
            series_info_remote = urllib2.urlopen(series_info_url)
        except urllib2.HTTPError, e:
            return None
        series_info_memory = cStringIO.StringIO(series_info_remote.read()) 
        series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
        try:
            dom = QtXml.QDomDocument()
            dom.setContent(series_info_zip.read(xml_file_in_zip))
            data = dom.firstChildElement("Data") 
            series_node = data.firstChildElement("Series")
            series_info = self.Series(series_node, series_info_url)
        except SyntaxError:
            self.logger.error("Syntax error in file from %s." % (series_info_url))
        return series_info

    def get_episodes_by_series_id(self, series_id):
        """Parse the <lang>.xml file for episode information"""
        xml_file_in_zip = "%s.xml" % (self.lang,)
        series_info_url = "%s/series/%s/all/%s.zip" % \
          (self.tvdb_apikey_url, series_id, self.lang)
        try:
            series_info_remote = urllib2.urlopen(series_info_url)
        except:
            return None
        series_info_memory = cStringIO.StringIO(series_info_remote.read())
        series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
        #Parse it up and put the info into a list of Episode objects
        dom = QtXml.QDomDocument()
        dom.setContent(series_info_zip.read(xml_file_in_zip))
        data = dom.firstChildElement("Data")
        episode_info = []
        episode_node = data.firstChildElement("Episode")
        while not episode_node.isNull():
            episode_info.append(\
              self.Episode(episode_node, self.tvdb_banner_url))
            episode_node = episode_node.nextSiblingElement("Episode")
        return episode_info

    def get_actors_by_id(self, series_id):
        """Gets information about the actors in a given series"""
        series_info_url = "%s/series/%s/all/en.zip" % \
          (self.tvdb_apikey_url, series_id)
        try:
            series_info_remote = urllib2.urlopen(series_info_url)
        except urllib2.HTTPError, e:
            return None
        series_info_memory = cStringIO.StringIO(series_info_remote.read())
        series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
        #Parse it up and put the info into a list of Actor objects
        dom = QtXml.QDomDocument()
        dom.setContent(series_info_zip.read("actors.xml"))
        actor_info_list = []
        actors = dom.firstChildElement("Actors")
        actor_node = actors.firstChildElement("Actor")
        while not actor_node.isNull():
            actor_info_list.append(self.Actor(actor_node, \
                series_id, self.tvdb_banner_url))
            actor_node = actor_node.nextSiblingElement("Actor") 
        return actor_info_list

    def get_banners_by_id(self, series_id):
        """Gets information about banners for a given series"""
        series_info_url = "%s/series/%s/all/en.zip" % \
          (self.tvdb_apikey_url, series_id)
        try:
            series_info_remote = urllib2.urlopen(series_info_url)
        except urllib2.HTTPError, e:
            return None
        series_info_memory = cStringIO.StringIO(series_info_remote.read())
        series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
        #Parse it up and put the info into a list of Banner objects
        dom = QtXml.QDomDocument()
        dom.setContent(series_info_zip.read("banners.xml"))
        banner_info_list = []
        banners = dom.firstChildElement("Banners")
        banner_node = banners.firstChildElement("Banner")
        while not banner_node.isNull():
            banner_info_list.append(self.Banner(banner_node, series_id, \
              self.tvdb_banner_url))
            banner_node = banner_node.nextSiblingElement("Banner")
        return banner_info_list

    def get_series_by_id(self, series_id):
        """Parse the <lang>.xml file for series information"""
        series_info_url = "%s/series/%s/%s.xml" % \
            (self.tvdb_apikey_url, series_id, self.lang)
        series_info_zip_url = "%s/series/%s/all/en.zip" % \
          (self.tvdb_apikey_url, series_id)
        try:
            series_info = urllib2.urlopen(series_info_url)
        except urllib2.HTTPError, e:
            return None
        dom = QtXml.QDomDocument()
        dom.setContent(series_info.read())
        data = dom.firstChildElement("Data")
        series_node = data.firstChildElement("Series")
        series_info = self.Series(series_node, series_info_zip_url)
        return series_info

    def get_episode_by_id(self, episode_id):
        """Parse the <lang>.xml file for episode information"""
        episode_info_url = "%s/episodes/%s/%s.xml" % \
            (self.tvdb_apikey_url, episode_id, self.lang)
        try:
            episode_info = urllib2.urlopen(episode_info_url)
        except urllib2.HTTPError, e:
            return None
        dom = QtXml.QDomDocument()
        dom.setContent(episode_info.read())
        data = dom.firstChildElement("Data")
        episode_node = data.firstChildElement("Episode")
        episode_info = self.Episode(episode_node, self.tvdb_banner_url)
        return episode_info

    def get_episode_by_season_episode(self, series_id, season, episode):
        """Parse the <lang>.xml file for episode information"""
        episode_info_url = "%s/series/%s/default/%s/%s/%s.xml" % \
            (self.tvdb_apikey_url, series_id, season.lstrip('0'), \
               episode.lstrip('0'), self.lang)
        try:
            episode_info = urllib2.urlopen(episode_info_url)
        except urllib2.HTTPError, e:
            return None
        dom = QtXml.QDomDocument()
        dom.setContent(episode_info.read())
        data = dom.firstChildElement("Data")
        episode_node = data.firstChildElement("Episode")
        episode_info = self.Episode(episode_node, self.tvdb_banner_url)
        return episode_info

    def retrieve_banner(self, url):
        """Retrieves a banner from <url> and saves it as <filename>"""
        if url is not None:
            if not str(url) == '':
                banner_name = url.split("/")[-1]
                banner_type = url.split("/")[-2]
                banner_cache = url.split("/")[-4]
                if banner_type == "original":
                    if banner_cache == "_cache":
                        banner_type = "fanart-cache"
                    else:
                        banner_type = "fanart-original"
                filedir = os.path.join(self.cache_dir, banner_type)
                filename = os.path.join(filedir, banner_name)
                if not os.path.isdir(filedir):
                    os.mkdir(filedir)
                if not os.path.isfile(filename):
                    urllib.urlretrieve(url, filename)
            else:
                filename = None
        else:
            filename = None
        return filename

    def massage_episode_name(self, episode_name):
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        episode_name = episode_name.lower()
        episode_name = " ".join(episode_name.split('/'))
        episode_name = regex.sub('', episode_name)
        # This one is especially for Austin City Limits
        episode_name = re.sub('followed by', ' ', episode_name)
        episode_name = re.sub('and', ' ', episode_name)
        episode_name = " ".join(episode_name.split())
        return episode_name

    def get_ssxee_by_seriesname_episodename(self, series_name, episode_name):
        """Lookup and return season and episode number from episode name."""
        episode_name_in = self.massage_episode_name(episode_name)
        match_list = self.find_series(series_name)
        series_id = 0
        if len(match_list) == 0:
            series_id = raw_input("Please input the ID for the correct series:")
        elif len(match_list) == 1:
            self.logger.info("Found match for '%s'." % (series_name))
            series_id = match_list[0][0]
        else:
            for i in range(0,len(match_list)):
                if match_list[i][1] == series_name:
                    self.logger.info("Found match for '%s'." % (series_name))
                    series_id = match_list[i][0]
        if not series_id:
            self.logger.info("Cannot find series %s." % (series_name))
            return 0
        episodes = self.get_episodes_by_series_id(series_id)
        for episode in episodes:
            episode_name_to_match = self.massage_episode_name(episode.episode_name)
            self.logger.debug("'%s' == '%s'" % (episode_name_to_match, episode_name_in))
            if episode_name_to_match == episode_name_in:
                season_num = episode.season_number
                episode_num = episode.episode_number
                return (season_num, episode_num)
            else:
                season_num = 00
                episode_num = 00
        return (season_num, episode_num)
