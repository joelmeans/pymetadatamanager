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

class Config(object):
    """
    Provides configuration information for pymetadatamanager
    """
    def __init__(self):
        self.home_dir = os.environ['HOME']
        self.config_dir = self.get_config_dir()
        self.video_dirs = ['/var/media/videos/TV/Alias']
        self.tvshowdb = os.path.join(self.config_dir, 'TV.db')

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
            config = os.poth.join('Library', 'Application Support', \
                                  'PyMetadataManager')
        elif platform == 'win32':
            config = os.poth.join('AppData', 'Local')
        config_dir = os.path.join(self.home_dir, config)
        if os.path.exists(config_dir):
            if not os.path.isdir(config_dir):
                os.path.remove(config_dir)
                os.mkdir(config_dir)
        else:
            os.mkdir(config_dir)

        return config_dir
