############################################################################
#    Copyright (C) 2011 by Joel Means,,,                                   #
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

__author__="jmeans"
__date__ ="$Oct 13, 2011 12:46:59 PM$"

import os
import sys
import logging
from PyQt4 import QtXml

class Config(object):
    """
    Provides configuration information for pymetadatamanager
    """
    def __init__(self):
        self.logger = logging.getLogger('pymetadatamanager.configuration')
        self.home_dir = os.path.expanduser('~')
        self.config_dir = self.get_config_dir()
        self.config_file = os.path.join(self.config_dir, 'config.xml')
        self.log_file = os.path.join(self.config_dir, 'pymetadatamanager.log')
        self.tvshowdb = os.path.join(self.config_dir, 'TV.db')
        self.tv_dirs = []
        self.movie_dirs = []
        self.mediainfo_path = ""
        self.prefer_local = 0 
        if not os.path.isfile(self.config_file):
            self.set_default_dirs()
        else:
            self.read_config_file()

    def __del__(self):
        try:
            pass
        except AttributeError:
            pass

    def get_config_dir(self): 
        platform = sys.platform
        if platform == 'linux2' or platform == 'linux':
            config = '.pymetadatamanager'
        elif platform == 'darwin':
            config = os.path.join('Library', 'Application Support', \
                                  'PyMetadataManager')
        elif platform == 'win32':
            config = os.path.join('AppData', 'Local', 'PyMetadataManager')
        config_dir = os.path.join(self.home_dir, config)
        if os.path.exists(config_dir):
            if not os.path.isdir(config_dir):
                os.path.remove(config_dir)
                os.mkdir(config_dir)
        else:
            os.mkdir(config_dir)

        return config_dir

    def set_default_dirs(self):
        platform = sys.platform
        if platform == 'linux2' or platform == 'linux':
            self.tv_dirs.append(os.path.join(self.home_dir, \
                                'Videos', 'TV'))
            self.movie_dirs.append(os.path.join(self.home_dir, \
                                   'Videos', 'Movies'))
        elif platform == 'darwin':
            self.tv_dirs.append(os.path.join(self.home_dir, \
                                'Movies', 'TV'))
            self.movie_dirs.append(os.path.join(self.home_dir, \
                                   'Movies', 'Movies'))
        elif platform == 'win32':
            self.tv_dirs.append(os.path.join(self.home_dir, \
                                'My Videos', 'TV'))
            self.movie_dirs.append(os.path.join(self.home_dir, \
                                   'My Videos', 'Movies'))

    def write_config_file(self):
        self.logger.info("Writing new config file")
        dom = QtXml.QDomDocument()
        xml_header_pi = dom.createProcessingInstruction('xml', 'version="1.0"')
        dom.appendChild(xml_header_pi)
        root = dom.createElement("configuration")
        dom.appendChild(root)
        for dir in self.tv_dirs:
            tv_dir = dom.createElement("video_dir")
            tv_dir.setAttribute("type", "TV")
            tv_dir_text = dom.createTextNode(dir)
            tv_dir.appendChild(tv_dir_text)
            root.appendChild(tv_dir)
        for dir in self.movie_dirs:
            movie_dir = dom.createElement("video_dir")
            movie_dir.setAttribute("type", "Movies")
            movie_dir_text = dom.createTextNode(dir)
            movie_dir.appendChild(movie_dir_text)
            root.appendChild(movie_dir)
        mediainfo_path = dom.createElement("mediainfo")
        mediainfo_path_text = dom.createTextNode(self.mediainfo_path)
        mediainfo_path.appendChild(mediainfo_path_text)
        root.appendChild(mediainfo_path)
        prefer_local = dom.createElement("prefer_local")
        prefer_local_text = dom.createTextNode(str(self.prefer_local))
        prefer_local.appendChild(prefer_local_text)
        root.appendChild(prefer_local)
        config = open(self.config_file, 'w')
        config.write(dom.toString(4))
        config.close()

    def read_config_file(self):
        self.logger.debug("Reading config file")
        config_file = os.path.join(self.config_dir, 'config.xml')
        dom = QtXml.QDomDocument()
        data = open(config_file, 'r')
        dom.setContent(data.read())
        data.close()
        config = dom.firstChildElement("configuration")
        video_dir = config.firstChildElement("video_dir")
        while not video_dir.isNull():
            if video_dir.attribute('type') == "TV":
                self.tv_dirs.append(str(video_dir.text()))
            elif video_dir.attribute('type') == "Movies":
                self.movie_dirs.append(str(video_dir.text()))
            video_dir = video_dir.nextSiblingElement("video_dir")
        mediainfo_path = config.firstChildElement("mediainfo")
        if not mediainfo_path.isNull():
            self.mediainfo_path = str(mediainfo_path.text())
        prefer_local = config.firstChildElement("prefer_local")
        if not prefer_local.isNull():
            self.prefer_local = int(prefer_local.text())
