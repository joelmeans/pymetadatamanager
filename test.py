#! /usr/bin/env python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jmeans"
__date__ ="$Feb 10, 2010 3:15:02 PM$"

import mediainfo
from PyQt4 import QtXml

MI = mediainfo.MediaInfo()
dom = MI.make_info_dom('30_Rock_01x01.dvdrip.mkv')
root = dom.documentElement()
elem_file = root.firstChildElement('File')
elem_track = elem_file.firstChildElement('track')
while not elem_track.isNull():
    print elem_track.attribute('type')
    elem_track = elem_track.nextSiblingElement('track')
