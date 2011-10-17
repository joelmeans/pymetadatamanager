#! /usr/bin/env python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jmeans"
__date__ ="$Feb 10, 2010 3:15:02 PM$"

from PyQt4 import QtXml
from pymetadatamanager.tvdb import TVDB

TVDB = TVDB()
time = TVDB.get_server_time()
old_time = int(time) - 10000
updates = TVDB.get_series_update_list(old_time)

series = TVDB.find_series("Alias")
print series

ssxee = TVDB.get_ssxee_by_seriesname_episodename("Parenthood (2010)", "Nora")
print ssxee
