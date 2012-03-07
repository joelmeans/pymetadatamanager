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

import logging
from PyQt4 import QtXml
from show_utils import Series, Episode, Actor, Banner

class NfoReader(object):
    def __init__(self):
        self.logger = logging.getLogger('pymetadatamanager.nfo_reader')

    def __del__(self):
        pass

    def readNfo(self, filepath):
        try:
            data = open(filepath, 'r')
            self.logger.info("Reading file %s" % (filepath,))
        except IOError:
            self.logger.error("No file %s found" % (filepath,))
            return 0
        dom = QtXml.QDomDocument()
        dom.setContent(data.read())
        data.close()
        return dom

    def get_series(self, nfo_path):
        """Get series info from the nfo file"""
        dom = self.readNfo(nfo_path)
        node = dom.firstChildElement("tvshow")
        series = Series()
        series.set(node, '', 'nfo')
        return series

    def get_episode(self, nfo_path):
        """Get episode info from the nfo file"""
        dom = self.readNfo(nfo_path)
        node = dom.firstChildElement("episodedetails")
        episode = Episode()
        episode.set(node, '', 'nfo')
        return episode

    def get_actors(self, nfo_path):
        """Get actor info from the nfo file"""
        dom = self.readNfo(nfo_path)
        root = dom.firstChildElement("tvshow")
        series_id = int(root.firstChildElement("id").text())
        actors = []
        elem_actor = root.firstChildElement("actor")
        while not elem_actor.isNull():
            actor = Actor()
            actor.set(elem_actor, series_id, '', 'nfo')
            if not actor in actors:
                actors.append(actor)
            elem_actor = elem_actor.nextSiblingElement("actor")
        return actors

    def get_banners(self, nfo_path):
        """Get banner info from the nfo file"""
        dom = self.readNfo(nfo_path)
        root = dom.firstChildElement("tvshow")
        series_id = int(root.firstChildElement("id").text())
        elem_fanart = root.firstChildElement("fanart")
        tvdb_banner_url = str(elem_fanart.attribute("url"))
        banners = []
        elem_banner = root.firstChildElement("thumb")
        while not elem_banner.isNull():
            banner = Banner()
            banner.set(elem_banner, series_id, tvdb_banner_url, 'nfo')
            if not banner in banners:
                banners.append(banner)
            elem_banner = elem_banner.nextSiblingElement("thumb")
        elem_fanart_banner = elem_fanart.firstChildElement("thumb")
        while not elem_fanart_banner.isNull():
            banner = Banner()
            banner.set(elem_fanart_banner, series_id, tvdb_banner_url, 'nfo')
            if not banner in banners:
                banners.append(banner)
            elem_fanart_banner = elem_fanart_banner.nextSiblingElement("thumb")
        return banners
