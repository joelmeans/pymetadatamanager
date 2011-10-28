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

__author__="jlmeans"
__date__ ="$Oct 20, 2011 4:59:23 PM$"

from PyQt4 import QtGui, QtCore
from banner_ui import Ui_BannerDialog
from tvshowdb import TVShowDB
from tvdb import TVDB
from configuration import Config
from models import AbstractBannerModel, AbstractBannerWideModel

config = Config()
TVDB = TVDB()
dbTV = TVShowDB(config.tvshowdb)
dbTV.init_db()

class BannerDialog(QtGui.QDialog):
    def __init__(self, series_name, banner_type, parent=None):
        """Initializes the Dialog"""
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_BannerDialog()
        self.ui.setupUi(self)
        self.series_name = series_name
        self.banner_url = ''

        #Create a progress dialog for downloading images
        self.progress = QtGui.QProgressDialog()
        self.progress.setCancelButtonText(QtCore.QString())
        self.progress.setMinimum(0)
        self.progress.setGeometry(500, 500, 50, 100)
        self.progress.setMinimumDuration(500)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Information")

        level = banner_type.split("_")[0]
        if level == "series":
            self.get_series_artwork_list()
        elif level == "season":
            self.get_season_artwork_list()
        self.set_artwork(banner_type)

        self.ui.tableView.clicked.connect(self.banner_selected)

    def get_series_artwork_list(self):
        """Creates lists of thumbnail urls for a series"""
        #Get the series id and the episode id from the database
        series_id = dbTV.get_series_id(self.series_name)
        #Create a QDomDocument containing the series details
        series_doc = dbTV.make_series_dom(series_id)
        series_root = series_doc.firstChildElement('tvshow')
        #These are the lists we will populate from the series info
        season_banners_url = []
        self.series_banners_url = []
        self.series_banners_wide_url = []
        self.series_fanart_banners_url = []
        elem_series_banner = series_root.firstChildElement('thumb')
        while not elem_series_banner.isNull():
            try:
                elem_series_banner_type = \
                 elem_series_banner.attribute('type')
                if elem_series_banner_type == 'season':
                    season_banners_url.append( \
                     elem_series_banner.text())
            except:
                pass
            if not season_banners_url.count(elem_series_banner.text()):
                if str(elem_series_banner.text()).find("graphical") > -1:
                    self.series_banners_wide_url.append(\
                     elem_series_banner.text())
                elif str(elem_series_banner.text()).find("text") > -1:
                    self.series_banners_wide_url.append( \
                     elem_series_banner.text())
                elif str(elem_series_banner.text()).find("blank") > -1:
                    self.series_banners_wide_url.append( \
                     elem_series_banner.text())
                else:
                    self.series_banners_url.append( \
                     elem_series_banner.text())
            elem_series_banner = \
             elem_series_banner.nextSiblingElement('thumb')

        elem_series_fanart = series_root.firstChildElement('fanart')
        url_base = elem_series_fanart.attribute('url')
        elem_series_fanart_banner = \
         elem_series_fanart.firstChildElement('thumb')
        while not elem_series_fanart_banner.isNull():
            url = "%s/%s" % (url_base, \
             elem_series_fanart_banner.attribute('preview'))
            self.series_fanart_banners_url.append(url)
            elem_series_fanart_banner = \
             elem_series_fanart_banner.nextSiblingElement('thumb')

    def get_season_artwork_list(self):
        """Creates lists of thumbnail urls for a season"""
        #Get the series id and the episode id from the database
        series_id = dbTV.get_series_id(self.series_name)
        #Create a QDomDocument containing the series details
        series_doc = dbTV.make_series_dom(series_id)
        series_root = series_doc.firstChildElement('tvshow')
        #These are the lists we will populate from the season info
        self.season_banners_url = []
        self.season_banners_wide_url = []
        elem_series_banner = series_root.firstChildElement('thumb')
        while not elem_series_banner.isNull():
            try:
                elem_series_banner_type = \
                 elem_series_banner.attribute('type')
                if elem_series_banner_type == 'season':
                    season = elem_series_banner.attribute('season')
                    if int(season) == self.season_number:
                        if str(elem_series_banner.text()).find( \
                         "seasonswide") > -1:
                            self.season_banners_wide_url.append( \
                             elem_series_banner.text())
                        else:
                            self.season_banners_url.append( \
                             elem_series_banner.text())
            except:
                pass
            elem_series_banner = \
             elem_series_banner.nextSiblingElement('thumb')

    def set_artwork(self, type):
        """Set the artwork for the given tab"""
        if type == 'series_posters':
            self.set_series_banners()
        elif type == 'series_wide':
            self.set_series_banners_wide()
        elif type == 'series_fanart':
            self.set_series_fanart()
        elif type == 'season_posters':
            self.set_season_banners()
        elif type == 'season_wide':
            self.set_season_banners_wide()

    def set_series_banners(self):
        """Downloads the posters for a series and displays them"""
        #Series Banners Tab
        series_banners = []
        self.progress.setLabelText("Downloading Series Posters...")
        self.progress.setMaximum(len(self.series_banners_url))
        for banner_url in self.series_banners_url:
            self.progress.setValue(self.series_banners_url.index(banner_url))
            filename = TVDB.retrieve_banner(str(banner_url).replace( \
             'banners/', 'banners/_cache/'))
            banner_pixmap = QtGui.QPixmap(filename)
            series_banners.append((banner_pixmap, banner_url))
        banner_model_series = AbstractBannerModel(series_banners)
        self.ui.tableView.setModel(banner_model_series)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.resizeRowsToContents()
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.horizontalHeader().hide()
        self.progress.setValue(len(self.series_banners_url))

    def set_series_banners_wide(self):
        """Downloads the wide series banners and displays them"""
        #Series Banners Wide Tab
        series_banners_wide = []
        self.progress.setLabelText("Downloading Series Wide Banners...")
        self.progress.setMaximum(len(self.series_banners_wide_url))
        for banner_url in self.series_banners_wide_url:
            self.progress.setValue( \
             self.series_banners_wide_url.index(banner_url))
            filename = TVDB.retrieve_banner(str(banner_url))
            banner_pixmap = QtGui.QPixmap(filename)
            series_banners_wide.append((banner_pixmap, banner_url))
        banner_model_series_wide = AbstractBannerWideModel(series_banners_wide)
        self.ui.tableView.setModel(banner_model_series_wide)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.resizeRowsToContents()
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.horizontalHeader().hide()
        self.progress.setValue(len(self.series_banners_wide_url))

    def set_series_fanart(self):
        """Downloads the series fanart and displays it"""
        #Fanart
        series_fanart_banners = []
        self.progress.setLabelText("Downloading Series Fanart...")
        self.progress.setMaximum(len(self.series_fanart_banners_url))
        for banner_url in self.series_fanart_banners_url:
            self.progress.setValue( \
             self.series_fanart_banners_url.index(banner_url))
            filename = TVDB.retrieve_banner(str(banner_url))
            banner_pixmap = QtGui.QPixmap(filename)
            series_fanart_banners.append((banner_pixmap, banner_url))
        banner_model_series_fanart = AbstractBannerModel(series_fanart_banners)
        self.ui.tableView.setModel(banner_model_series_fanart)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.resizeRowsToContents()
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.horizontalHeader().hide()
        self.progress.setValue(len(self.series_fanart_banners_url))

    def set_season_banners(self):
        """Downloads the posters for a season and displays them"""
        #Season Posters Tab
        season_banners = []
        self.progress.setLabelText("Downloading Season Posters...")
        self.progress.setMaximum(len(self.season_banners_url))
        for banner_url in self.season_banners_url:
            self.progress.setValue(self.season_banners_url.index(banner_url))
            filename = TVDB.retrieve_banner(str(banner_url).replace( \
             'banners/', 'banners/_cache/'))
            banner_pixmap = QtGui.QPixmap(filename)
            season_banners.append((banner_pixmap, banner_url))
        banner_model_season = AbstractBannerModel(season_banners)
        self.ui.tableView.setModel(banner_model_season)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.resizeRowsToContents()
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.horizontalHeader().hide()
        self.progress.setValue(len(self.season_banners_url))

    def set_season_banners_wide(self):
        """Downloads the wide banners for a season and displays them"""
        #Season Wide Banners Tab
        season_banners_wide = []
        self.progress.setLabelText("Downloading Season Wide Banners...")
        self.progress.setMaximum(len(self.season_banners_wide_url))
        for banner_url in self.season_banners_wide_url:
            self.progress.setValue( \
             self.season_banners_wide_url.index(banner_url))
            filename = TVDB.retrieve_banner(str(banner_url))
            banner_pixmap = QtGui.QPixmap(filename)
            season_banners_wide.append((banner_pixmap, banner_url))
        banner_model_season_wide = AbstractBannerWideModel(season_banners_wide)
        self.ui.tableView.setModel(banner_model_season_wide)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.resizeRowsToContents()
        self.ui.tableView.verticalHeader().hide()
        self.ui.tableView.horizontalHeader().hide()
        self.progress.setValue(len(self.season_banners_wide_url))

    def banner_selected(self, index):
        self.banner_url = str(self.ui.tableView.model().data(index, QtCore.Qt.UserRole))

    def accept(self):
        if not self.banner_url == '':
            dbTV.link_selected_banner_show(self.series_name, self.banner_url)
        QtGui.QDialog.accept(self)
