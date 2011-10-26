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
__date__ ="$Jan 15, 2010 3:59:23 PM$"

import os.path
from PyQt4 import QtGui, QtCore
from main_window_ui import Ui_MainWindow
from tvshowdb import TVShowDB
from tvdb import TVDB
from scanner import Scanner
from models import ShowListModel,\
                   AbstractShowModel,\
                   AbstractSeasonEpisodeModel,\
                   AbstractBannerModel,\
                   EmptyTableModel,\
                   AbstractBannerWideModel
from configuration import Config
from configuration_dialog import ConfigDialog

#Get configuration information
config = Config()

#Connect to the database
dbTV = TVShowDB(config.tvshowdb)
dbTV.init_db()

#Setup the connection to thetvdb.com
TVDB = TVDB()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """Initializes the Main Window"""
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #Create a dom representing the shows in the database
        shows = dbTV.make_shows_list()
        #Turn that into a model
        model = ShowListModel(shows)
        #Set that as the model for the listView
        self.ui.listView_shows.setModel(model)

        #Create a progress dialog for downloading images
        self.progress = QtGui.QProgressDialog()
        self.progress.setCancelButtonText(QtCore.QString())
        self.progress.setMinimum(0)
        self.progress.setGeometry(500, 500, 50, 100)
        self.progress.setMinimumDuration(500)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Information")

        #Create a dialog window
        self.input_dialog = QtGui.QInputDialog()
        self.input_dialog.setGeometry(1000, 1000, 50, 100)
        self.input_dialog.setWindowTitle("Multiple Matches")

        # Connect sockets to slots
        self.ui.listView_shows.clicked.connect(self.list_view_clicked)
        self.ui.columnView_season_episode.clicked.connect(self.column_view_clicked)
#        self.ui.combo_actors.currentIndexChanged.connect(self.set_actor_thumb)
#        self.ui.tabWidget_series_artwork.currentChanged.connect(self.set_series_artwork)
#        self.ui.tabWidget_season_artwork.currentChanged.connect(self.set_season_artwork)
#        self.ui.line_series_name.textEdited.connect(self.set_series_name_updated)
#        self.ui.text_series_overview.textChanged.connect(self.set_series_overview_updated)
#        self.ui.line_network.textEdited.connect(self.set_series_network_updated)
#        self.ui.line_airtime.textEdited.connect(self.set_series_airtime_updated)
#        self.ui.line_runtime.textEdited.connect(self.set_series_runtime_updated)
#        self.ui.line_status.textEdited.connect(self.set_series_status_updated)
#        self.ui.pushButton_save_series_changes.pressed.connect(self.update_series)
#        self.ui.pushButton_revert_series_changes.pressed.connect(self.revert_series)
#
#        self.ui.line_episode_name.textEdited.connect(self.set_episode_name_updated)
#        self.ui.text_episode_plot.textChanged.connect(self.set_episode_plot_updated)
#        self.ui.line_airdate.textEdited.connect(self.set_episode_airdate_updated)
##        self.ui.line_tvdb_id.textEdited.connect(self.set_episode_tvdb_id_updated)
#        self.ui.line_tvdb_rating.textEdited.connect(self.set_episode_tvdb_rating_updated)
#        self.ui.pushButton_save_episode_changes.pressed.connect(self.update_episode)
#        self.ui.pushButton_revert_episode_changes.pressed.connect(self.revert_episode)
#        
        self.ui.actionScan_Files.triggered.connect(self.scan_files)
        self.ui.actionEdit_Preferences.triggered.connect(self.edit_preferences)
        self.ui.actionClear_Cache.triggered.connect(self.clear_cache)
#        self.ui.tableView_series_banners.clicked.connect(self.series_banner_selected)
#        self.ui.tableView_series_banners_wide.clicked.connect(self.series_banner_wide_selected)
#        self.ui.tableView_series_fanart.clicked.connect(self.series_fanart_selected)
#        self.ui.tableView_season_banners.clicked.connect(self.season_banner_selected)
#        self.ui.tableView_season_banners_wide.clicked.connect(self.season_banner_wide_selected)

        #Initialize some variables
        self.series_name_updated = 0
        self.series_overview_updated = 0
        self.series_network_updated = 0
        self.series_airtime_updated = 0
        self.series_runtime_updated = 0
        self.series_status_updated = 0
        self.episode_name_updated = 0
        self.episode_plot_updated = 0
        self.episode_airdate_updated = 0
        self.episode_tvdb_id_updated = 0
        self.episode_tvdb_rating_updated = 0

        #Create some empty lists for later
        self.series_banners_url = []
        self.series_banners_wide_url = []
        self.series_fanart_banners_url = []
        self.season_banners_url = []
        self.season_banners_wide_url = []

        #Initialize the configuration dialog
        self.config_dialog = ConfigDialog()

    def list_view_clicked(self, index):
        """Determines what was clicked in the column view tree"""
        #other functions need to know where we are in the tree
        self.index = index
        #Find the series we are working with
        show_name = index.data().toString()
        dom = dbTV.make_seasons_episodes_dom(show_name)
        model = AbstractSeasonEpisodeModel(dom)
        self.ui.columnView_season_episode.setModel(model)

    def column_view_clicked(self, index):
        """Determines what was clicked in the column view tree"""
        #other functions need to know where we are in the tree
        self.index = index
        #Find the series we are working with
        this_node_data = index.data().toString()
        parent = index.parent()
        parent_data = parent.data().toString()

        if parent_data == "":    #we are at the season level
            self.season_number = int(this_node_data)
#            self.clear_episode_info()
#            self.get_season_artwork_list()
        else:                           #we are at the episode level
            self.season_number = int(parent_data)
            self.episode_number = int(str(this_node_data.split("-")[0]).rstrip())
#            self.set_episode_info()
#            self.ui.pushButton_save_episode_changes.setEnabled(0)
#            self.ui.pushButton_revert_episode_changes.setEnabled(0)

#    def set_series_name_updated(self, text):
#        self.series_name_updated = 1
#        self.new_series_name = str(text)
#        self.ui.pushButton_save_series_changes.setEnabled(1)
#        self.ui.pushButton_revert_series_changes.setEnabled(1)
#
#    def set_series_overview_updated(self):
#        self.series_overview_updated = 1
#        self.new_series_overview = \
#         unicode(self.ui.text_series_overview.toPlainText(), "latin-1")
#        self.ui.pushButton_save_series_changes.setEnabled(1)
#        self.ui.pushButton_revert_series_changes.setEnabled(1)
#
#    def set_series_network_updated(self, text):
#        self.series_network_updated = 1
#        self.new_series_network = str(text)
#        self.ui.pushButton_save_series_changes.setEnabled(1)
#        self.ui.pushButton_revert_series_changes.setEnabled(1)
#
#    def set_series_airtime_updated(self, text):
#        self.series_airtime_updated = 1
#        self.new_series_airtime = str(text)
#        self.ui.pushButton_save_series_changes.setEnabled(1)
#        self.ui.pushButton_revert_series_changes.setEnabled(1)
#
#    def set_series_runtime_updated(self, text):
#        self.series_runtime_updated = 1
#        self.new_series_runtime = str(text)
#        self.ui.pushButton_save_series_changes.setEnabled(1)
#        self.ui.pushButton_revert_series_changes.setEnabled(1)
#
#    def set_series_status_updated(self, text):
#        self.series_status_updated = 1
#        self.new_series_status = str(text)
#        self.ui.pushButton_save_series_changes.setEnabled(1)
#        self.ui.pushButton_revert_series_changes.setEnabled(1)
#
#    def update_series(self):
#        series_id = dbTV.get_series_id(self.series_name)
#        if self.series_name_updated == 1:
#            dbTV.update_series_field('name', self.new_series_name, series_id)
#            self.series_name=self.new_series_name
#        if self.series_overview_updated == 1:
#            dbTV.update_series_field('overview', self.new_series_overview, series_id)
#        if self.series_network_updated == 1:
#            pass
#        if self.series_airtime_updated == 1:
#            new_series_airs_time = self.new_series_airtime.split(' at ')[1]
#            new_series_airs_day = self.new_series_airtime.split(' at ')[0]
#            dbTV.update_series_field('airs_time', new_series_airs_time, series_id)
#            dbTV.update_series_field('airs_day', new_series_airs_day, series_id)
#        if self.series_runtime_updated == 1:
#            dbTV.update_series_field('runtime', self.new_series_runtime, series_id)
#        if self.series_status_updated == 1:
#            dbTV.update_series_field('status', self.new_series_status, series_id)
#        self.ui.pushButton_save_series_changes.setEnabled(0)
#        self.ui.pushButton_revert_series_changes.setEnabled(0)
#
#    def revert_series(self):
#        self.set_series_info()
#        self.ui.pushButton_save_series_changes.setEnabled(0)
#        self.ui.pushButton_revert_series_changes.setEnabled(0)
#
#    def set_episode_name_updated(self, text):
#        self.episode_name_updated = 1
#        self.new_episode_name = str(text)
#        self.ui.pushButton_save_episode_changes.setEnabled(1)
#        self.ui.pushButton_revert_episode_changes.setEnabled(1)
#
#    def set_episode_plot_updated(self):
#        self.episode_plot_updated = 1
#        self.new_episode_plot = \
#         str(self.ui.text_episode_plot.toPlainText().toUtf8())
#        self.ui.pushButton_save_episode_changes.setEnabled(1)
#        self.ui.pushButton_revert_episode_changes.setEnabled(1)
#
#    def set_episode_airdate_updated(self, text):
#        self.episode_airdate_updated = 1
#        self.new_episode_airdate = str(text)
#        self.ui.pushButton_save_episode_changes.setEnabled(1)
#        self.ui.pushButton_revert_episode_changes.setEnabled(1)
#
##    def set_episode_tvdb_id_updated(self, text):
##        self.episode_tvdb_id_updated = 1
##        self.new_episode_tvdb_id = str(text)
##        self.ui.pushButton_save_episode_changes.setEnabled(1)
##        self.ui.pushButton_revert_episode_changes.setEnabled(1)
#
#    def set_episode_tvdb_rating_updated(self, text):
#        self.episode_tvdb_rating_updated = 1
#        self.new_episode_tvdb_rating = str(text)
#        self.ui.pushButton_save_episode_changes.setEnabled(1)
#        self.ui.pushButton_revert_episode_changes.setEnabled(1)
#
#    def update_episode(self):
#        episode_id = dbTV.get_episode_id(self.series_name, self.season_number, \
#         self.episode_number)
#        if self.episode_name_updated == 1:
#            dbTV.update_episode_field('name', self.new_episode_name, episode_id)
#        if self.episode_plot_updated == 1:
#            dbTV.update_episode_field('overview', self.new_episode_plot, episode_id)
#        if self.episode_airdate_updated == 1:
#            dbTV.update_episode_field('first_aired', self.new_episode_airdate, episode_id)
##        if self.episode_tvdb_id_updated == 1:
##            dbTV.update_episode_field('episodeid', self.new_episode_tvdb_id, episode_id)
#        if self.episode_tvdb_rating_updated == 1:
#            dbTV.update_episode_field('rating', self.new_episode_tvdb_rating, episode_id)
#        self.ui.pushButton_save_episode_changes.setEnabled(0)
#        self.ui.pushButton_revert_episode_changes.setEnabled(0)
#
#    def revert_episode(self):
#        self.set_episode_info()
#        self.ui.pushButton_save_episode_changes.setEnabled(0)
#        self.ui.pushButton_revert_episode_changes.setEnabled(0)
#
#    def set_series_info(self):
#        """Sets the info for the current series in the display window"""
#        #Get the series id from the database
#        series_id = dbTV.get_series_id(self.series_name)
#
#        #Create a QDomDocument containing the series details
#        series_doc = dbTV.make_series_dom(series_id)
#        series_root = series_doc.firstChildElement('tvshow')
#
#        #Extract the details and fill in the display
#        elem_series_name = series_root.firstChildElement('title')
#        series_name = elem_series_name.text()
#        self.ui.line_series_name.setText(series_name)
#
#        elem_series_plot = series_root.firstChildElement('plot')
#        series_plot = QtCore.QString(elem_series_plot.text())
#        self.ui.text_series_overview.setPlainText(series_plot)
#
#        series_actors = []
#        self.ui.combo_actors.clear()
#        elem_series_actor = series_root.firstChildElement('actor')
#        while not elem_series_actor.isNull():
#            elem_series_actor_name = elem_series_actor.firstChildElement('name')
#            series_actor_name = elem_series_actor_name.text()
#            series_actors.append(series_actor_name)
#            elem_series_actor = elem_series_actor.nextSiblingElement('actor')
#
#        series_actors = set(series_actors)
#        for series_actor in series_actors:
#            self.ui.combo_actors.addItem(series_actor)
#
#        elem_series_network = series_root.firstChildElement('network')
#        series_network = elem_series_network.text()
#        self.ui.line_network.setText(series_network)
#
#        elem_series_airs_day = series_root.firstChildElement('airsday')
#        series_airs_day = elem_series_airs_day.text()
#        elem_series_airs_time = series_root.firstChildElement('airstime')
#        series_airs_time = elem_series_airs_time.text()
#        if not series_airs_day == '':
#            series_airtime = series_airs_day + " at " + series_airs_time
#        else:
#            series_airtime = ''
#        self.ui.line_airtime.setText(series_airtime)
#
#        elem_series_runtime = series_root.firstChildElement('runtime')
#        series_runtime = elem_series_runtime.text()
#        self.ui.line_runtime.setText(series_runtime)
#
#        elem_series_status = series_root.firstChildElement('status')
#        series_status = elem_series_status.text()
#        self.ui.line_status.setText(series_status)
#        self.ui.tabWidget_tv_info.setCurrentIndex(0)
#
#    def get_series_artwork_list(self):
#        """Creates lists of thumbnail urls for a series"""
#        #Get the series id and the episode id from the database
#        series_id = dbTV.get_series_id(self.series_name)
#        #Create a QDomDocument containing the series details
#        series_doc = dbTV.make_series_dom(series_id)
#        series_root = series_doc.firstChildElement('tvshow')
#        #These are the lists we will populate from the series info
#        season_banners_url = []
#	self.series_banners_url = []
#        self.series_banners_wide_url = []
#	self.series_fanart_banners_url = []
#        elem_series_banner = series_root.firstChildElement('thumb')
#        while not elem_series_banner.isNull():
#            try:
#                elem_series_banner_type = \
#                 elem_series_banner.attribute('type')
#                if elem_series_banner_type == 'season':
#                    season_banners_url.append( \
#                     elem_series_banner.text())
#            except:
#                pass
#            if not season_banners_url.count(elem_series_banner.text()):
#                if str(elem_series_banner.text()).find("graphical") > -1:
#                    self.series_banners_wide_url.append(\
#                     elem_series_banner.text())
#                elif str(elem_series_banner.text()).find("text") > -1:
#                    self.series_banners_wide_url.append( \
#                     elem_series_banner.text())
#                elif str(elem_series_banner.text()).find("blank") > -1:
#                    self.series_banners_wide_url.append( \
#                     elem_series_banner.text())
#                else:
#                    self.series_banners_url.append( \
#                     elem_series_banner.text())
#            elem_series_banner = \
#             elem_series_banner.nextSiblingElement('thumb')
#
#        elem_series_fanart = series_root.firstChildElement('fanart')
#        url_base = elem_series_fanart.attribute('url')
#        elem_series_fanart_banner = \
#         elem_series_fanart.firstChildElement('thumb')
#        while not elem_series_fanart_banner.isNull():
#            url = "%s/%s" % (url_base, \
#             elem_series_fanart_banner.attribute('preview'))
#            self.series_fanart_banners_url.append(url)
#            elem_series_fanart_banner = \
#             elem_series_fanart_banner.nextSiblingElement('thumb')
#        self.set_series_artwork(0)
#        self.ui.tabWidget_series_artwork.setCurrentIndex(0)
#
#    def get_season_artwork_list(self):
#        """Creates lists of thumbnail urls for a season"""
#        #Get the series id and the episode id from the database
#        series_id = dbTV.get_series_id(self.series_name)
#        #Create a QDomDocument containing the series details
#        series_doc = dbTV.make_series_dom(series_id)
#        series_root = series_doc.firstChildElement('tvshow')
#        #These are the lists we will populate from the season info
#        self.season_banners_url = []
#	self.season_banners_wide_url = []
#        elem_series_banner = series_root.firstChildElement('thumb')
#        while not elem_series_banner.isNull():
#            try:
#                elem_series_banner_type = \
#                 elem_series_banner.attribute('type')
#                if elem_series_banner_type == 'season':
#                    season = elem_series_banner.attribute('season')
#                    if int(season) == self.season_number:
#                        if str(elem_series_banner.text()).find( \
#                         "seasonswide") > -1:
#                            self.season_banners_wide_url.append( \
#                             elem_series_banner.text())
#                        else:
#                            self.season_banners_url.append( \
#                             elem_series_banner.text())
#            except:
#                pass
#            elem_series_banner = \
#             elem_series_banner.nextSiblingElement('thumb')
#        self.set_season_artwork(0)
#        self.ui.tabWidget_season_artwork.setCurrentIndex(0)
#
#    def set_series_artwork(self, tab_number):
#        """Set the artwork for the given tab"""
##        print "Setting Series Artwork on Tab %s" % (tab_number,)
#        if tab_number == 0:
#            self.set_series_banners()
#        elif tab_number == 1:
#            self.set_series_banners_wide()
#        elif tab_number == 2:
#            self.set_series_fanart()
#
#    def set_season_artwork(self, tab_number):
##        print "Setting Season Artwork on Tab %s" % (tab_number,)
#        """Set the artwork for a given tab"""
#        if tab_number == 0:
#            self.set_season_banners()
#        elif tab_number == 1:
#            self.set_season_banners_wide()
#
#    def set_series_banners(self):
#        """Downloads the posters for a series and displays them"""
#        #Series Banners Tab
#        series_banners = []
#        self.progress.setLabelText("Downloading Series Posters...")
#        self.progress.setMaximum(len(self.series_banners_url))
#        for banner_url in self.series_banners_url:
#            self.progress.setValue(self.series_banners_url.index(banner_url))
#            filename = TVDB.retrieve_banner(str(banner_url).replace( \
#             'banners/', 'banners/_cache/'))
#            banner_pixmap = QtGui.QPixmap(filename)
#            series_banners.append(banner_pixmap)
#        banner_model_series = AbstractBannerModel(series_banners)
#        self.ui.tableView_series_banners.setModel(banner_model_series)
#        self.ui.tableView_series_banners.resizeColumnsToContents()
#        self.ui.tableView_series_banners.resizeRowsToContents()
#        self.ui.tableView_series_banners.verticalHeader().hide()
#        self.ui.tableView_series_banners.horizontalHeader().hide()
#        self.progress.setValue(len(self.series_banners_url))
#
#    def set_series_banners_wide(self):
#        """Downloads the wide series banners and displays them"""
#        #Series Banners Wide Tab
#        series_banners_wide = []
#        self.progress.setLabelText("Downloading Series Wide Banners...")
#        self.progress.setMaximum(len(self.series_banners_wide_url))
#        for banner_url in self.series_banners_wide_url:
#            self.progress.setValue( \
#             self.series_banners_wide_url.index(banner_url))
#            filename = TVDB.retrieve_banner(str(banner_url))
#            banner_pixmap = QtGui.QPixmap(filename)
#            series_banners_wide.append(banner_pixmap)
#        banner_model_series_wide = AbstractBannerWideModel(series_banners_wide)
#        self.ui.tableView_series_banners_wide.setModel(banner_model_series_wide)
#        self.ui.tableView_series_banners_wide.resizeColumnsToContents()
#        self.ui.tableView_series_banners_wide.resizeRowsToContents()
#        self.ui.tableView_series_banners_wide.verticalHeader().hide()
#        self.ui.tableView_series_banners_wide.horizontalHeader().hide()
#        self.progress.setValue(len(self.series_banners_wide_url))
#
#    def set_series_fanart(self):
#        """Downloads the series fanart and displays it"""
#        #Fanart
#        series_fanart_banners = []
#        self.progress.setLabelText("Downloading Series Fanart...")
#        self.progress.setMaximum(len(self.series_fanart_banners_url))
#        for banner_url in self.series_fanart_banners_url:
#            self.progress.setValue( \
#             self.series_fanart_banners_url.index(banner_url))
#            filename = TVDB.retrieve_banner(str(banner_url))
#            banner_pixmap = QtGui.QPixmap(filename)
#            series_fanart_banners.append(banner_pixmap)
#        banner_model_series_fanart = AbstractBannerModel(series_fanart_banners)
#        self.ui.tableView_series_fanart.setModel(banner_model_series_fanart)
#        self.ui.tableView_series_fanart.resizeColumnsToContents()
#        self.ui.tableView_series_fanart.resizeRowsToContents()
#        self.ui.tableView_series_fanart.verticalHeader().hide()
#        self.ui.tableView_series_fanart.horizontalHeader().hide()
#        self.progress.setValue(len(self.series_fanart_banners_url))
#
#    def set_season_banners(self):
#        """Downloads the posters for a season and displays them"""
#        #Season Posters Tab
#        season_banners = []
#        self.progress.setLabelText("Downloading Season Posters...")
#        self.progress.setMaximum(len(self.season_banners_url))
#        for banner_url in self.season_banners_url:
#            self.progress.setValue(self.season_banners_url.index(banner_url))
#            filename = TVDB.retrieve_banner(str(banner_url).replace( \
#             'banners/', 'banners/_cache/'))
#            banner_pixmap = QtGui.QPixmap(filename)
#            season_banners.append(banner_pixmap)
#        banner_model_season = AbstractBannerModel(season_banners)
#        self.ui.tableView_season_banners.setModel(banner_model_season)
#        self.ui.tableView_season_banners.resizeColumnsToContents()
#        self.ui.tableView_season_banners.resizeRowsToContents()
#        self.ui.tableView_season_banners.verticalHeader().hide()
#        self.ui.tableView_season_banners.horizontalHeader().hide()
#        self.progress.setValue(len(self.season_banners_url))
#
#    def set_season_banners_wide(self):
#        """Downloads the wide banners for a season and displays them"""
#        #Season Wide Banners Tab
#        season_banners_wide = []
#        self.progress.setLabelText("Downloading Season Wide Banners...")
#        self.progress.setMaximum(len(self.season_banners_wide_url))
#        for banner_url in self.season_banners_wide_url:
#            self.progress.setValue( \
#             self.season_banners_wide_url.index(banner_url))
#            filename = TVDB.retrieve_banner(str(banner_url))
#            banner_pixmap = QtGui.QPixmap(filename)
#            season_banners_wide.append(banner_pixmap)
#        banner_model_season_wide = AbstractBannerWideModel(season_banners_wide)
#        self.ui.tableView_season_banners_wide.setModel(banner_model_season_wide)
#        self.ui.tableView_season_banners_wide.resizeColumnsToContents()
#        self.ui.tableView_season_banners_wide.resizeRowsToContents()
#        self.ui.tableView_season_banners_wide.verticalHeader().hide()
#        self.ui.tableView_season_banners_wide.horizontalHeader().hide()
#        self.progress.setValue(len(self.season_banners_wide_url))
#
#    def set_actor_thumb(self, index):
#        """Downloads and displays a thumbnail for the given actor"""
#        actor = self.ui.combo_actors.itemText(index)
#        url = dbTV.get_actor_thumb(actor)
#        if not url == "none":
#            filename = TVDB.retrieve_banner(url)
#            thumb = QtGui.QPixmap(filename)
#            self.ui.label_actor_thumb.setGeometry(0, 0, \
#             thumb.width(), thumb.height())
#            self.ui.label_actor_thumb.setPixmap(thumb)
#        else:
#            self.ui.label_actor_thumb.clear()
#            
#    def set_episode_info(self):
#        """Sets the info for the show in the display window"""
#        #Get the episode_id from the database
#        episode_id = dbTV.get_episode_id(self.series_name, self.season_number, \
#         self.episode_number)
#
#        #Create a QDomDocument containing the episode details
#        episode_doc = dbTV.make_episode_dom(episode_id)
#        episode_root = episode_doc.firstChildElement('episodedetails')
#
#        #Extract the details and fill in the display
#        elem_episode_title = episode_root.firstChildElement('title')
#        episode_title = elem_episode_title.text()
#        self.ui.line_episode_name.setText(episode_title)
#
#        elem_episode_plot = episode_root.firstChildElement('plot')
#        episode_plot = QtCore.QString(elem_episode_plot.text())
#        self.ui.text_episode_plot.setPlainText(episode_plot)
#
#        elem_episode_thumb = episode_root.firstChildElement('thumb')
#        if not elem_episode_thumb.isNull():
#            episode_thumb = elem_episode_thumb.text()
#        else:
#            episode_thumb = "none"
#        #Set the preview image
#        image_file = TVDB.retrieve_banner(str(episode_thumb))
#        image = QtGui.QPixmap(image_file)
#        self.ui.label_episode_thumb.setGeometry(0, 0, \
#         image.width(), image.height())
#        self.ui.label_episode_thumb.setPixmap(image)
#
#        elem_episode_airdate = episode_root.firstChildElement('aired')
#        episode_airdate = elem_episode_airdate.text()
#        self.ui.line_airdate.setText(episode_airdate)
#
#        elem_episode_id = episode_root.firstChildElement('id')
#        episode_id = elem_episode_id.text()
#        self.ui.line_tvdb_id.setText(episode_id)
#
#        elem_episode_rating = episode_root.firstChildElement('rating')
#        episode_rating = elem_episode_rating.text()
#        self.ui.line_tvdb_rating.setText(episode_rating)
#
#        elem_episode_directors = episode_root.firstChildElement('director')
#        episode_directors = elem_episode_directors.text().split("|")
#        self.ui.combo_directors.clear()
#        i = 0
#        while i < episode_directors.count():
#            self.ui.combo_directors.addItem(episode_directors.takeAt(i))
#            i = i + 1
#
#        elem_episode_writers = episode_root.firstChildElement('credits')
#        episode_writers = elem_episode_writers.text().split("|")
#        self.ui.combo_writers.clear()
#        i = 0
#        while i < episode_writers.count():
#            self.ui.combo_writers.addItem(episode_writers.takeAt(i))
#            i = i + 1
#
#        episode_actors = []
#        elem_episode_actor = episode_root.firstChildElement('actor')
#        self.ui.combo_guests.clear()
#        while not elem_episode_actor.isNull():
#            elem_episode_actor_name = \
#             elem_episode_actor.firstChildElement('name')
#            episode_actor_name = elem_episode_actor_name.text()
#            episode_actors.append(episode_actor_name)
#            elem_episode_actor = elem_episode_actor.nextSiblingElement('actor')
#
#        episode_actors = set(episode_actors)
#        for episode_actor in episode_actors:
#            if self.ui.combo_actors.findText(episode_actor) < 0:
#                self.ui.combo_guests.addItem(episode_actor)
#
#        self.ui.tabWidget_tv_info.setCurrentIndex(3)
#
#        episode_xml = episode_doc.toString(4)
#        outfile = "output_tests/%s_%sx%s.nfo" % (self.series_name, \
#         str(self.season_number).zfill(2), str(self.episode_number).zfill(2))
#        output = QtCore.QFile(outfile)
#        output.open(QtCore.QIODevice.WriteOnly)
#        output.writeData(episode_xml)
#        output.close()
#
#    def clear_episode_info(self):
#        """Clears the episode info from the display window"""
#        self.ui.line_episode_name.clear()
#        self.ui.text_episode_plot.clear()
#        self.ui.line_airdate.clear()
#        self.ui.line_tvdb_id.clear()
#        self.ui.line_tvdb_rating.clear()
#        self.ui.combo_directors.clear()
#        self.ui.combo_writers.clear()
#        self.ui.combo_guests.clear()
#        self.ui.label_episode_thumb.clear()
#
#    def clear_series_artwork(self):
#        """Clears the artwork displays"""
#        empty_model = EmptyTableModel()
#        self.ui.tableView_series_banners.setModel(empty_model)
#        self.ui.tableView_series_banners_wide.setModel(empty_model)
#        self.ui.tableView_series_fanart.setModel(empty_model)
#
#    def clear_season_artwork(self):
#        """Clears the artwork displays"""
#        empty_model = EmptyTableModel()
#        self.ui.tableView_season_banners.setModel(empty_model)
#        self.ui.tableView_season_banners_wide.setModel(empty_model)
#        
    def scan_files(self):
        for video_dir in config.tv_dirs:
            self.progress.setLabelText("Scanning Files from %s into DB..." \
                                       %  (video_dir))
            print "Scanning Files"
            scanner = Scanner(video_dir)
            scanner.set_series_list()
            self.progress.setMaximum(len(scanner.series_list))
            self.progress.setValue(0)
            for series_name in scanner.series_list:
                self.progress.setValue(scanner.series_list.index(series_name))
                match_list = scanner.get_series_id_list(series_name)
                if len(match_list) == 0:
                    print "No matches found on thetvdb.com for '%s'." % (series_name)
                    series_id = raw_input("Please input the ID for the correct series:")
                elif len(match_list) == 1:
                    print "Found match for '%s'." % (series_name)
                    series_id = match_list[0][0]
                else:
                    match = False
                    list = ''
                    for i in range(0,len(match_list)):
                        if match_list[i][1] == series_name:
                            print "Found match for '%s'." % (series_name)
                            series_id = match_list[i][0]
                            match = True
                        else:
                            list += "[%d] %s (%s)\n " % (i, match_list[i][1], \
                                                         match_list[i][0])
                    if not match:
                        selection = self.input_dialog.getInt(self, '', \
                                    "Select best match:\n %s" % (list), \
                                    0, 0, len(match_list) - 1)[0]
                        try:
                            series_id = match_list[selection][0]
                        except IndexError:
                            print "That is not an option."
                scanner.add_series_to_db(series_id)
                scanner.add_files_to_db(series_name, series_id)
            scanner.__del__()
            self.progress.setValue(len(scanner.series_list))

        print "Finished Scanning"
#        #Create a dom representing the shows in the database
#        doc = dbTV.make_shows_dom()
#        #Turn that into a model
#        model = AbstractShowModel(doc)
#        #Set that as the model for the columnView
#        self.ui.columnView_show_tree.setModel(model)
#        self.ui.columnView_show_tree.setColumnWidths([300,150,150,500])
#        self.clear_season_artwork()
#        self.clear_episode_info()
#        self.clear_series_artwork()
#
    def edit_preferences(self):
        self.config_dialog.show()

    def clear_cache(self):
        top = os.path.join(config.config_dir, "cache")
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

#    def series_banner_selected(self, index):
#        self.series_banner = self.ui.tableView_series_banners.model().data(index, QtCore.Qt.DecorationRole).toPyObject()
#
#    def series_banner_wide_selected(self, index):
#        self.series_banner_wide = self.ui.tableView_series_banners_wide.model().data(index, QtCore.Qt.DecorationRole).toPyObject()
#
#    def series_fanart_selected(self, index):
#        self.series_fanart = self.ui.tableView_series_fanart.model().data(index, QtCore.Qt.DecorationRole).toPyObject()
#
#    def season_banner_selected(self, index):
#        self.season_banner = self.ui.tableView_season_banners.model().data(index, QtCore.Qt.DecorationRole).toPyObject()
#
#    def season_banner_wide_selected(self, index):
#        self.season_banner_wide = self.ui.tableView_season_banners_wide.model().data(index, QtCore.Qt.DecorationRole).toPyObject()

