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

__author__="jmeans"
__date__ ="$Feb 12, 2010 9:26:59 AM$"

import os
from subprocess import Popen
from PyQt4 import QtXml, QtCore

class MediaInfo(object):
    """
    Provides methods for getting well-formatted meta-info from video files

    The methods in this class will take an input file, call 'mediainfo' to
    get meta-info from that input file, and output either an html file
    (which is one native output from mediainfo) or an xml file, or return
    a QDomDocument for processing by other programs.
    """
    def __init__(self):
        self.temp_dir = "temp"
        if os.path.isdir(self.temp_dir):
            pass
        elif os.path.exists(self.temp_dir):
            os.rm(self.temp_dir)
            os.mkdir(self.temp_dir)
        else:
            os.mkdir(self.temp_dir)
        self.temp_file = self.temp_dir + "/info.xml"

    def __del__(self):
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except AttributeError:
	    pass
        
    def make_info_xml_native(self, infile, outfile="none"):
        """Calls 'mediainfo' to output an xml file with metadata for infile"""
        output = open(self.temp_file, 'w')
        info = Popen(["/usr/bin/mediainfo", "--Output=xml", infile], \
         stdout=output)
        info.wait()
        output.close()
        if not outfile == "none":
            os.system ("cp %s %s" % (self.temp_file, outfile))

    def make_info_dom(self, infile):
        """Creates a QDomDocument from the 'mediainfo' output on infile"""
        self.make_info_xml_native(infile)
        dom = QtXml.QDomDocument()

        infile = open(self.temp_file, 'r')
        data = infile.read()
        infile.close()
        dom.setContent(data)
        return dom

    def make_info_xml(self, infile, outfile):
        """Creates an xml file from the 'mediainfo' output on infile"""
        dom = self.make_info_dom(infile)
        xml = dom.toString(4)
        output = QtCore.QFile(outfile)
        output.open(QtCore.QIODevice.WriteOnly)
        output.writeData(xml)
        output.close()
