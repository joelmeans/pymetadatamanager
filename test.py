#! /usr/bin/env python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jmeans"
__date__ ="$Feb 10, 2010 3:15:02 PM$"

from PyQt4 import QtXml
from pymetadatamanager.tvdb_qt import TVDB
from pymetadatamanager.tvdb_et import TVDB as TVDB_ET
TVDB_ET = TVDB_ET()

TVDB = TVDB()
time = TVDB.get_server_time()
old_time = int(time) - 10000
updates = TVDB.get_series_update_list(old_time)

series = TVDB.find_series("Alias")
print series

series_et = TVDB_ET.find_series("Alias")
print series_et
