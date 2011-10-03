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

import urllib
import urllib2
import xml.etree.cElementTree as ETree
import zipfile
import cStringIO
import os

class TVDB(object):
    """
    The main interface to thetvdb.com.

    This object provides many methods for retrieving information from
    thetvdb.com using their developer's API.
    """
    def __init__(self):
        # Define how we connect to thetvdb.com
        self.tvdb_apikey = "2A5FFFB6E15B508A"
        self.tvdb_mirror_url = "http://www.thetvdb.com"
        self.tvdb_api_url = self.tvdb_mirror_url + "/api"
        self.tvdb_apikey_url = self.tvdb_api_url + "/" + self.tvdb_apikey
        self.tvdb_banner_url = self.tvdb_mirror_url  + "/banners"
        self.lang = "en"
        self.temp_dir = "temp"
        if os.path.isdir(self.temp_dir):
            pass
        elif os.path.exists(self.temp_dir):
            os.remove(self.temp_dir)
            os.mkdir(self.temp_dir)
        else:
            os.mkdir(self.temp_dir)

    class Series(object):
        """Class to hold info about a series"""
        def __init__(self, node):
            self.seriesid = node.findtext("id")
            self.actors = [actor.strip() for actor in \
             node.findtext("Actors").split("|") if actor]
            self.airs_day = node.findtext("Airs_DayOfWeek")
            self.airs_time = node.findtext("Airs_Time")
            self.content_rating = node.findtext("ContentRating")
            self.first_aired = node.findtext("FirstAired")
            self.genre = [genre.strip() for genre in \
             node.findtext("Genre").split("|") if genre]
            self.language = node.findtext("Language")
            self.network = node.findtext("Network")
            self.overview = node.findtext("Overview")
            self.rating = node.findtext("Rating")
#            self.runtime = [runtime for runtime in node.findtext("Runtime") if runtime]
            self.runtime = node.findtext("Runtime")
            if self.runtime == '':
                self.runtime = '0'
            self.name = node.findtext("SeriesName")
            self.status = node.findtext("Status")
            self.banner = node.findtext("banner")
            self.fanart = node.findtext("fanart")
            self.poster = node.findtext("poster")
            self.last_updated = node.findtext("lastupdated")

    class Episode(object):
        """Class to hold info about an episode"""
        def __init__(self, node, tvdb_banner_url):
        #def __init__(self, node, seriesid):
            self.episodeid = node.findtext("id")
            self.directors = [director.strip() for director in \
             node.findtext("Director").split("|") if director]
            self.episode_name = node.findtext("EpisodeName")
            self.episode_number = node.findtext("EpisodeNumber")
            self.first_aired = node.findtext("FirstAired")
            self.guest_stars = [guest.strip() for guest in \
             node.findtext("GuestStars").split("|") if guest]
            self.language = node.findtext("Language")
            self.overview = node.findtext("Overview")
            self.production_code = node.findtext("ProductionCode")
            self.rating = node.findtext("Rating")
            self.season_number = node.findtext("SeasonNumber")
            self.writers = [writer.strip() for writer in \
             node.findtext("Writer").split("|") if writer]
            if node.findtext("filename"):
                self.thumb = "%s/%s" % (tvdb_banner_url, \
                 node.findtext("filename"))
            else:
                self.thumb = ""
            self.last_updated = node.findtext("lastupdated")

    class Actor(object):
        """Class to hold actor info"""
        def __init__(self, node, seriesid, tvdb_banner_url):
            self.seriesid = seriesid
            self.actorid = node.findtext("id")
            thumbnail = node.findtext("Image")
            if not thumbnail == "":
                self.thumb = "%s/%s" % (tvdb_banner_url, thumbnail)
            else:
                self.thumb = "none"
            self.name = node.findtext("Name")
            self.role = node.findtext("Role")

    class Banner(object):
        """Class to hold banner info"""
        def __init__(self, node, seriesid, tvdb_banner_url):
            self.seriesid = seriesid
            self.id = node.findtext("id")
            self.path = node.findtext("BannerPath")
            self.type = node.findtext("BannerType")
            self.type2 = node.findtext("BannerType2")
            self.colors = node.findtext("Colors")
            self.season = node.findtext("Season")
            self.thumb = node.findtext("ThumbnailPath")
            self.url = tvdb_banner_url

    def get_server_time(self):
        """Gets the current server time.  Needed for updates"""
        updates_args = urllib.urlencode({"type": "none"}, doseq = True)
        tvdb_time_url = "%s/Updates.php?%s" % (self.tvdb_api_url, updates_args)
        server_time = urllib.urlopen(tvdb_time_url)
        tree = ETree.parse(server_time)
        time = tree.findtext("Time")
        return time

    def get_series_update_list(self, last_time):
        """Gets a list of updated series since last_time"""
        updates_args = urllib.urlencode({"type": "all", "time": last_time}, \
         doseq = True)
        tvdb_update_url = "%s/Updates.php?%s" % (self.tvdb_api_url, \
         updates_args)
        updates = urllib.urlopen(tvdb_update_url)
        series_list = []
        if updates:
            try:
                tree = ETree.parse(updates)
                series_element_list = tree.findall("Series")
                series_list = [series.text for series in series_element_list]
            except SyntaxError:
                pass
        return series_list

    def get_episode_update_list(self, last_time):
        """Gets list of updated episodes since last_time"""
        updates_args = urllib.urlencode({"type": "all", "time": last_time}, \
         doseq = True)
        tvdb_update_url = "%s/Updates.php?%s" % (self.tvdb_api_url, \
         updates_args)
        updates = urllib.urlopen(tvdb_update_url)
        episode_list = []
        if updates:
            try:
                tree = ETree.parse(updates)
                episode_element_list = tree.findall("Episode")
                episode_list = [episode.text for episode in \
                 episode_element_list]
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
        matches = urllib.urlopen(series_search_url)
        match_list = []
        seriesid = 0
        if matches:
            try:
                tree = ETree.parse(matches)
                match_list = [(series.findtext("seriesid"), \
                 series.findtext("SeriesName")) for series in \
                 tree.getiterator("Series")]
            except SyntaxError:
                print "No possible matches found for %s." % (series_name)
        return match_list 

    def get_series_all_by_id(self, series_id):
        """Grabs the information for series with id "series_id" """
        series_file_name = "%s/%s-%s.xml" % (self.temp_dir, self.lang, \
         series_id)
        actors_file_name = "%s/actors-%s.xml" % (self.temp_dir, series_id)
        banners_file_name = "%s/banners-%s.xml" % (self.temp_dir, series_id)
        xml_file_in_zip = "%s.xml" % (self.lang,)
        #See if we already have the info for this series
        if os.path.isfile(series_file_name):
            pass
        else:
            series_info_url = "%s/series/%s/all/%s.zip" % \
             (self.tvdb_apikey_url, series_id, self.lang)
            series_info_remote = urllib.urlopen(series_info_url)
            series_info_memory = cStringIO.StringIO(series_info_remote.read()) 
            series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
            #Now we can read the file and write the necessary xml to a temp file
            #This could be done with a ZipFile.extract() in 2.6, but not 2.5
            series_file = open(series_file_name, 'w')
            series_file.write(series_info_zip.read(xml_file_in_zip))
            series_file.close()
            #Write the actors file out
            actors_file = open(actors_file_name, 'w')
            actors_file.write(series_info_zip.read('actors.xml'))
            actors_file.close()
            #Write the banners file out
            banners_file = open(banners_file_name, 'w')
            banners_file.write(series_info_zip.read('banners.xml'))
            banners_file.close()
            series_info_zip.close()
        #Now read in the info from the file
        try:
            tree = ETree.parse(series_file_name)
            series_node = tree.find("Series")
            series_info = self.Series(series_node)
        except SyntaxError:
            print "Error"
        return series_info

    def get_episodes_by_series_id(self, series_id):
        """Parse the <lang>.xml file for episode information"""
        xml_file = "%s/%s-%s.xml" % (self.temp_dir, self.lang, series_id)
        xml_file_in_zip = "%s.xml" % (self.lang,)
        #See if we already have the file (from get_series_by_id)
        if os.path.isfile(xml_file):
            pass
        #If not, get it
        else:
            series_info_url = "%s/series/%s/all/%s.zip" % \
             (self.tvdb_apikey_url, series_id, self.lang)
            series_info_remote = urllib.urlopen(series_info_url)
            series_info_memory = cStringIO.StringIO(series_info_remote.read())
            series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
            series_file = open(xml_file, 'w')
            series_file.write(series_info_zip.read(xml_file_in_zip))
            series_file.close()
        #Parse it up and put the info into a list of Episode objects
        tree = ETree.parse(xml_file)
        episode_node = tree.findall("Episode")
        episode_info = []
        for episode in episode_node:
            episode_info.append(self.Episode(episode, self.tvdb_banner_url))
        return episode_info

    def get_actors_by_id(self, series_id):
        """Gets information about the actors in a given series"""
        xml_file = "%s/actors-%s.xml" % (self.temp_dir, series_id)
        #See if we already have the file (from get_series_by_id)
        if os.path.isfile(xml_file):
            pass
        #If not, get it
        else:
            series_info_url = "%s/series/%s/all/en.zip" % \
             (self.tvdb_apikey_url, series_id)
            series_info_remote = urllib.urlopen(series_info_url)
            series_info_memory = cStringIO.StringIO(series_info_remote.read())
            series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
            actors_file = open(xml_file, 'w')
            actors_file.write(series_info_zip.read('actors.xml'))
            actors_file.close()
        #Parse it up and put the info into a list of Actor objects
        tree = ETree.parse(xml_file)
        actor_node = tree.findall("Actor")
        actor_info_list = []
        for actor in actor_node:
            actor_info_list.append(self.Actor(actor, \
                series_id, self.tvdb_banner_url))
        return actor_info_list

    def get_banners_by_id(self, series_id):
        """Gets information about banners for a given series"""
        xml_file = "%s/banners-%s.xml" % (self.temp_dir, series_id)
        #See if we already have the file (from get_series_by_id)
        if os.path.isfile(xml_file):
            pass
        #If not, get it
        else:
            series_info_url = "%s/series/%s/all/en.zip" % \
             (self.tvdb_apikey_url, series_id)
            series_info_remote = urllib.urlopen(series_info_url)
            series_info_memory = cStringIO.StringIO(series_info_remote.read())
            series_info_zip = zipfile.ZipFile(series_info_memory, 'r')
            actors_file = open(xml_file, 'w')
            actors_file.write(series_info_zip.read('banners.xml'))
            actors_file.close()
        #Parse it up and put the info into a list of Banner objects
        tree = ETree.parse(xml_file)
        banner_node = tree.findall("Banner")
        banner_info_list = []
        for banner in banner_node:
            banner_info_list.append(self.Banner(banner, series_id, \
             self.tvdb_banner_url))
        return banner_info_list

    def get_series_by_id(self, series_id):
        """Parse the <lang>.xml file for episode information"""
        series_info_url = "%s/series/%s/%s.xml" % \
            (self.tvdb_apikey_url, series_id, self.lang)
        series_info = urllib.urlopen(series_info_url)
        tree = ETree.parse(series_info)
        series_node = tree.find("Series")
        series_info = self.Series(series_node)
        return series_info

    def get_episode_by_id(self, episode_id):
        """Parse the <lang>.xml file for episode information"""
        episode_info_url = "%s/episodes/%s/%s.xml" % \
            (self.tvdb_apikey_url, episode_id, self.lang)
        episode_info = urllib.urlopen(episode_info_url)
        tree = ETree.parse(episode_info)
        episode_node = tree.find("Episode")
        episode_info = self.Episode(episode_node, self.tvdb_banner_url)
        return episode_info

    def get_episode_by_season_episode(self, series_id, season, episode):
        """Parse the <lang>.xml file for episode information"""
        episode_info_url = "%s/series/%s/default/%s/%s/%s.xml" % \
            (self.tvdb_apikey_url, series_id, season, episode, self.lang)
        try:
            ep_info = urllib2.urlopen(episode_info_url)
        except urllib2.HTTPError, e:
            return None
        episode_info = urllib.urlretrieve(episode_info_url)
        tree = ETree.parse(episode_info[0])
        episode_node = tree.find("Episode")
        episode_info = self.Episode(episode_node, self.tvdb_banner_url)
        return episode_info

    def retrieve_banner(self, url):
        """Retrieves a banner from <url> and saves it as <filename>"""
        if not str(url) == 'none':
            banner_name = url.split("/")[-1]
            banner_type = url.split("/")[-2]
            if banner_type == "original":
                banner_type = "fanart-original"
            filedir = "%s/%s" % (self.temp_dir, banner_type)
            filename = "%s/%s" % (filedir, banner_name)
            if not os.path.isdir(filedir):
                os.mkdir(filedir)
            if not os.path.isfile(filename):
                urllib.urlretrieve(url, filename)
            return filename
        else:
            return Null
