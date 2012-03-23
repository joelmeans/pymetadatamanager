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

import re
import logging
from PyQt4 import QtCore, QtXml

dvdorder = True

class Series(object):
    """Class to hold info about a series"""
    def __init__(self):
        pass

    def __del__(self):
        pass

    def set(self, node, url, source):
        if source == 'tvdb':
            self.episodeguide = url
            self.seriesid = int(node.firstChildElement("id").text())
            actors = unicode(node.firstChildElement("Actors").text(), \
              "latin-1")
            if re.search('\|', actors):
                self.actors = [actor.strip() for actor in actors.split('|') \
                  if actor]
            elif re.search(',', actors):
                self.actors = [actor.strip() for actor in actors.split(',') \
                  if actor]
            else:
                self.actors = [actors.strip()]
            self.airs_day = str(\
              node.firstChildElement("Airs_DayOfWeek").text())
            self.airs_time = str(node.firstChildElement("Airs_Time").text())
            self.content_rating = str(\
              node.firstChildElement("ContentRating").text())
            self.first_aired = str(node.firstChildElement("FirstAired").text())
            genres = str(node.firstChildElement("Genre").text())
            if re.search('\|', genres):
                self.genre = [genre.strip() for genre in \
                  genres.split('|') if genre]
            elif re.search(',', genres):
                self.genre = [genre.strip() for genre in \
                  genres.split(',') if genre]
            else:
                self.genre = [genres.strip()]
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
        elif source == 'nfo':
            self.episodeguide = str(\
              node.firstChildElement("episodeguide").text())
            self.seriesid = int(node.firstChildElement("id").text())
            self.airs_day = str(node.firstChildElement("airsday").text())
            self.airs_time = str(node.firstChildElement("airstime").text())
            self.content_rating = ""
            self.first_aired = str(node.firstChildElement("premiered").text())
            self.language = ""
            self.network = str(node.firstChildElement("network").text())
            self.overview = unicode(node.firstChildElement("plot").text(), \
                                    "latin-1")
            self.rating = str(node.firstChildElement("rating").text())
            self.runtime = str(node.firstChildElement("runtime").text())
            self.name = str(node.firstChildElement("title").text())
            self.status = str(node.firstChildElement("status").text())
            self.banner = ""
            self.fanart = ""
            self.poster = ""
            self.last_updated = ""
            self.actors = []
            elem_actor = node.firstChildElement("actor")
            while not elem_actor.isNull():
                elem_actor_name = elem_actor.firstChildElement("name")
                actor_name = unicode(elem_actor_name.text(), "latin-1")
                if not actor_name in self.actors:
                    self.actors.append(actor_name)
                elem_actor = elem_actor.nextSiblingElement("actor")
            self.genre = []
            elem_genre = node.firstChildElement("genre")
            while not elem_genre.isNull():
                genre = str(elem_genre.text())
                if not genre in self.genre:
                    self.genre.append(genre)
                elem_genre = elem_genre.nextSiblingElement("genre")

class Episode(object):
    """Class to hold info about an episode"""
    def __init__(self):
        pass

    def __del__(self):
        pass
    
    def set(self, node, tvdb_banner_url, source):
        if source == 'tvdb':
            self.episodeid = int(node.firstChildElement("id").text())
            directors = unicode(node.firstChildElement("Director").text(), \
              "latin-1")
            if re.search('\|', directors):
                self.directors = [director.strip() for director in \
                  directors.split('|') if director]
            elif re.search(',', directors):
                self.directors = [director.strip() for director in \
                  directors.split(',') if director]
            else:
                self.directors = [directors.strip()]
            self.episode_name = unicode(\
              node.firstChildElement("EpisodeName").text(), "latin-1")
            dvd_ep = node.firstChildElement("DVD_episodenumber").text()
            if not dvd_ep == '' and dvdorder:
                self.episode_number = int(\
                  node.firstChildElement(\
                  "DVD_episodenumber").text().split('.')[0])
            else:
                self.episode_number = int(\
                  node.firstChildElement("EpisodeNumber").text())
            self.first_aired = str(node.firstChildElement("FirstAired").text())
            guests = unicode(node.firstChildElement("GuestStars").text(), \
              "latin-1")
            if re.search('\|', guests):
                self.guest_stars = [guest.strip() for guest in \
                    guests.split('|') if guest]
            elif re.search(',', guests):
                self.guest_stars = [guest.strip() for guest in \
                    guests.split(',') if guest]
            else:
                self.guest_stars = [guests.strip()]
            self.language = str(node.firstChildElement("Language").text())
            self.overview = unicode(\
              node.firstChildElement("Overview").text(), "latin-1")
            self.production_code = \
              str(node.firstChildElement("ProductionCode").text())
            self.rating = str(node.firstChildElement("Rating").text())
            self.season_number = int(\
              node.firstChildElement("SeasonNumber").text())
            writers = unicode(node.firstChildElement("Writer").text(), \
              "latin-1")
            if re.search('\|', writers):
                self.writers = [writer.strip() for writer in \
                  writers.split('|') if writer]
            elif re.search(',', writers):
                self.writers = [writer.strip() for writer in \
                  writers.split(',') if writer]
            else:
                self.writers = [writers.strip()]
            thumb_path = str(node.firstChildElement("filename").text())
            if not thumb_path == "":
                self.thumb = "%s/%s" % (tvdb_banner_url, thumb_path)
            else:
                self.thumb = ""
            self.last_updated = node.firstChildElement("lastupdated").text()
        elif source == 'nfo':
            self.episodeid = int(node.firstChildElement("id").text())
            directors = unicode(node.firstChildElement("director").text(), \
              "latin-1")
            if re.search('\|', directors):
                self.directors = [director.strip() for director in \
                  directors.split('|') if director]
            elif re.search(',', directors):
                self.directors = [director.strip() for director in \
                  directors.split(',') if director]
            else:
                self.directors = [directors.strip()]
            self.episode_name = unicode(\
              node.firstChildElement("title").text(), "latin-1")
            self.episode_number = int(node.firstChildElement("episode").text())
            self.first_aired = str(node.firstChildElement("aired").text())
            self.guest_stars = []
            self.language = ""
            self.overview = unicode(node.firstChildElement("plot").text(), \
                                    "latin-1")
            self.production_code = str(node.firstChildElement("code").text())
            self.rating = str(node.firstChildElement("rating").text())
            self.season_number = int(node.firstChildElement("season").text())
            writers = unicode(node.firstChildElement("credits").text(), \
              "latin-1")
            if re.search('\|', writers):
                self.writers = [writer.strip() for writer in \
                  writers.split('|') if writer]
            elif re.search(',', writers):
                self.writers = [writer.strip() for writer in \
                  writers.split(',') if writer]
            else:
                self.writers = [writers.strip()]
            self.thumb = str(node.firstChildElement("thumb").text())
            self.last_updated = ""

class Actor(object):
    """Class to hold actor info"""
    def __init__(self):
        pass

    def __del__(self):
        pass

    def set(self, node, series_id, tvdb_banner_url, source):
        if source == 'tvdb':
            self.seriesid = series_id
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
        elif source == 'nfo':
            self.seriesid = series_id
            self.actorid = ""
            self.thumb = str(node.firstChildElement("thumb").text())
            self.name = unicode(node.firstChildElement("name").text(), \
                                "latin-1")
            self.role = unicode(node.firstChildElement("role").text(), \
                                "latin-1")

class Banner(object):
    """Class to hold banner info"""
    def __init__(self):
        pass

    def __del__(self):
        pass

    def set(self, node, series_id, tvdb_banner_url, source):
        if source == 'tvdb':
            self.seriesid = series_id
            self.id = int(node.firstChildElement("id").text())
            self.path = str(node.firstChildElement("BannerPath").text())
            self.type = str(node.firstChildElement("BannerType").text())
            self.type2 = str(node.firstChildElement("BannerType2").text())
            self.colors = str(node.firstChildElement("Colors").text())
            self.season = str(node.firstChildElement("Season").text())
            self.thumb = str(node.firstChildElement("ThumbnailPath").text())
            self.url = str(tvdb_banner_url)
        elif source == 'nfo':
            self.seriesid = series_id
            self.url = str(tvdb_banner_url)
            self.id = 0
            self.path = str(node.text()).lstrip(self.url)
            if not node.attribute("type").isNull():
                self.type = str(node.attribute("type"))
            else:
                self.type = ""
            if not node.attribute("dim").isNull():
                self.type2 = str(node.attribute("dim"))
            else:
                self.type2 = ""
            if not node.attribute("colors").isNull():
                self.colors = str(node.attribute("colors"))
            else:
                self.colors = ""
            if not node.attribute("season").isNull():
                self.season = str(node.attribute("season"))
            else:
                self.season = ""
            if not node.attribute("preview").isNull():
                self.thumb = str(node.attribute("preview"))
            else:
                self.thumb = ""

def dom_from_series(series):
    #separator for lists with multiple items (writers, directors, etc)
    sep = "|"
    dom = QtXml.QDomDocument()
    root = dom.createElement("tvshow")
    dom.appendChild(root)

    elem_title = dom.createElement("title")
    text_title = dom.createTextNode(series.name)
    elem_title.appendChild(text_title)
    root.appendChild(elem_title)

    elem_rating = dom.createElement("rating")
    text_rating = dom.createTextNode(series.rating)
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

    elem_displayseason = dom.createElement("displayseason")
    text_displayseason = dom.createTextNode("-1")
    elem_displayseason.appendChild(text_displayseason)
    root.appendChild(elem_displayseason)

    elem_votes = dom.createElement("votes")
    text_votes = dom.createTextNode("0")
    elem_votes.appendChild(text_votes)
    root.appendChild(elem_votes)

    elem_plot = dom.createElement("plot")
    text_plot = dom.createTextNode(series.overview)
    elem_plot.appendChild(text_plot)
    root.appendChild(elem_plot)

    elem_runtime = dom.createElement("runtime")
    text_runtime = dom.createTextNode(str(series.runtime))
    elem_runtime.appendChild(text_runtime)
    root.appendChild(elem_runtime)
    elem_network = dom.createElement("network")
    text_network = dom.createTextNode(series.network)
    elem_network.appendChild(text_network)
    root.appendChild(elem_network)

    elem_airs_day = dom.createElement("airsday")
    text_airs_day = dom.createTextNode(series.airs_day)
    elem_airs_day.appendChild(text_airs_day)
    root.appendChild(elem_airs_day)

    elem_airs_time = dom.createElement("airstime")
    text_airs_time = dom.createTextNode(series.airs_time)
    elem_airs_time.appendChild(text_airs_time)
    root.appendChild(elem_airs_time)

    elem_episodeguide = dom.createElement("episodeguide")
    text_episodeguide = dom.createTextNode(series.episodeguide)
    elem_episodeguide.appendChild(text_episodeguide)
    root.appendChild(elem_episodeguide)

    elem_seriesid = dom.createElement("id")
    text_seriesid = dom.createTextNode(str(series.seriesid))
    elem_seriesid.appendChild(text_seriesid)
    root.appendChild(elem_seriesid)

    elem_genre = dom.createElement("genre")
    genres = sep.join(series.genre)
    text_genres = dom.createTextNode(genres)
    elem_genre.appendChild(text_genres)
    root.appendChild(elem_genre)

    elem_premiered = dom.createElement("premiered")
    text_premiered = dom.createTextNode(series.first_aired)
    elem_premiered.appendChild(text_premiered)
    root.appendChild(elem_premiered)

    elem_status = dom.createElement("status")
    text_status = dom.createTextNode(series.status)
    elem_status.appendChild(text_status)
    root.appendChild(elem_status)

    for x in series.actors:
        elem_actor = dom.createElement("actor")
        elem_actor_name = dom.createElement("name")
        text_actor_name = dom.createTextNode(QtCore.QString(x))
        elem_actor_name.appendChild(text_actor_name)
        elem_actor.appendChild(elem_actor_name)
        root.appendChild(elem_actor)

    return dom

def dom_from_episode(episode):
    #separator for lists with multiple items (writers, directors, etc)
    sep = "|"

    dom = QtXml.QDomDocument()
    root = dom.createElement("episodedetails")
    dom.appendChild(root)

    elem_title = dom.createElement("title")
    text_title = dom.createTextNode(episode.episode_name)
    elem_title.appendChild(text_title)
    root.appendChild(elem_title)

    elem_rating = dom.createElement("rating")
    text_rating = dom.createTextNode(episode.rating)
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
    text_season = dom.createTextNode(str(episode.season_number))
    elem_season.appendChild(text_season)
    root.appendChild(elem_season)

    elem_episode = dom.createElement("episode")
    text_episode = dom.createTextNode(str(episode.episode_number))
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
    text_plot = dom.createTextNode(episode.overview)
    elem_plot.appendChild(text_plot)
    root.appendChild(elem_plot)
    elem_thumb = dom.createElement("thumb")
    text_thumb = dom.createTextNode(episode.thumb)
    elem_thumb.appendChild(text_thumb)
    root.appendChild(elem_thumb)

    elem_playcount = dom.createElement("playcount")
    text_playcount = dom.createTextNode('0')
    elem_playcount.appendChild(text_playcount)
    root.appendChild(elem_playcount)

    elem_episodeid = dom.createElement("id")
    text_episodeid = dom.createTextNode(str(episode.episodeid))
    elem_episodeid.appendChild(text_episodeid)
    root.appendChild(elem_episodeid)

    elem_credits = dom.createElement("credits") #Writers
    credits = sep.join(episode.writers)
    text_credits = dom.createTextNode(credits)
    elem_credits.appendChild(text_credits)
    root.appendChild(elem_credits)

    elem_director = dom.createElement("director")
    director = sep.join(episode.directors)
    text_director = dom.createTextNode(director)
    elem_director.appendChild(text_director)
    root.appendChild(elem_director)

    elem_code = dom.createElement("code")
    text_code = dom.createTextNode(str(episode.production_code))
    elem_code.appendChild(text_code)
    root.appendChild(elem_code)

    elem_aired = dom.createElement("aired")
    text_aired = dom.createTextNode(episode.first_aired)
    elem_aired.appendChild(text_aired)
    root.appendChild(elem_aired)

    for x in episode.guest_stars:
        elem_actor = dom.createElement("actor")
        elem_actor_name = dom.createElement("name")
        text_actor_name = dom.createTextNode(QtCore.QString(x))
        elem_actor_name.appendChild(text_actor_name)
        elem_actor.appendChild(elem_actor_name)
        root.appendChild(elem_actor)

    return dom
