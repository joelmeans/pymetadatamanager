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
