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
import logging
import logging.handlers
from PyQt4 import QtGui, QtCore, QtXml
from main_window_ui import Ui_MainWindow
from tvshowdb import TVShowDB
from tvdb import TVDB
from scanner import Scanner
from models import ShowListModel,\
                   SeasonListModel,\
                   ShowModel,\
                   SeasonEpisodeModel,\
                   BannerModel,\
                   EmptyTableModel,\
                   EmptyListModel,\
                   BannerWideModel
from configuration import Config
from configuration_dialog import ConfigDialog
from banner_dialog import BannerDialog
from nfo_reader import NfoReader
from show_utils import dom_from_series, dom_from_episode

#Get configuration information
config = Config()

#Set up the logging
logger = logging.getLogger('pymetadatamanager')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.TimedRotatingFileHandler(config.log_file, \
                                               when='midnight',\
                                               backupCount=2)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(name)-38s\n \
  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

#Connect to the database
dbTV = TVShowDB(config.tvshowdb)
dbTV.init_db()

#Setup the connection to thetvdb.com
TVDB = TVDB()

#Create an nfo_reader
nfo_reader = NfoReader()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """Initializes the Main Window"""
        self.logger = logging.getLogger('pymetadatamanager.main_window')
        self.logger.info('Creating the main window.')
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #Create a dom representing the shows in the database
        self.shows = dbTV.make_shows_list()
        #Turn that into a model
        model = ShowListModel(self.shows)
        #Set that as the model for the listView
        self.ui.listView_shows.setModel(model)

        #Set the initial tabs to be shown
        self.ui.tabWidget_main.setCurrentIndex(0)
        self.ui.tabWidget_tv_info.setCurrentIndex(0)

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

        #Set up the thread for saving files
        self.save_files = SaveFiles()

        # Connect sockets to slots
        self.ui.listView_shows.clicked.connect(self.list_view_clicked)
        self.ui.columnView_season_episode.clicked.connect(\
          self.column_view_clicked)
#        self.ui.combo_actors.currentIndexChanged.connect(self.set_actor_thumb)
        self.ui.lineEdit_series_name.textEdited.connect(\
          self.set_series_name_updated)
        self.ui.plainTextEdit_overview.textChanged.connect(\
          self.set_series_overview_updated)
        self.ui.lineEdit_network.textEdited.connect(\
          self.set_series_network_updated)
        self.ui.lineEdit_airtime.textEdited.connect(\
          self.set_series_airtime_updated)
        self.ui.lineEdit_runtime.textEdited.connect(\
          self.set_series_runtime_updated)
        self.ui.lineEdit_status.textEdited.connect(\
          self.set_series_status_updated)
        self.ui.pushButton_save_series_changes.pressed.connect(\
          self.update_series)
        self.ui.pushButton_revert_series_changes.pressed.connect(\
          self.revert_series)
        self.ui.pushButton_load_local_series_nfo.pressed.connect(\
          self.load_series_nfo)
        self.ui.pushButton_update_series_from_tvdb.pressed.connect(\
          self.update_series_from_tvdb)
        self.ui.line_episode_name.textEdited.connect(\
          self.set_episode_name_updated)
        self.ui.text_episode_plot.textChanged.connect(\
          self.set_episode_plot_updated)
        self.ui.line_airdate.textEdited.connect(\
          self.set_episode_airdate_updated)
        self.ui.line_tvdb_rating.textEdited.connect(\
          self.set_episode_tvdb_rating_updated)
        self.ui.pushButton_save_episode_changes.pressed.connect(\
          self.update_episode)
        self.ui.pushButton_revert_episode_changes.pressed.connect(\
          self.revert_episode)
        self.ui.pushButton_load_local_episode_nfo.pressed.connect(\
          self.load_episode_nfo)
        self.ui.pushButton_update_episode_from_tvdb.pressed.connect(\
          self.update_episode_from_tvdb)
        self.ui.pushButton_new_series_poster.pressed.connect(\
          self.select_series_poster)
        self.ui.pushButton_new_series_wide_banner.pressed.connect(\
          self.select_series_wide_banner)
        self.ui.pushButton_new_season_poster.pressed.connect(\
          self.select_season_poster)
        self.ui.pushButton_new_season_wide.pressed.connect(\
          self.select_season_wide_banner)
        self.ui.pushButton_new_series_fanart.pressed.connect(\
          self.select_series_fanart)
        self.ui.actionScan_Files.triggered.connect(\
          self.scan_files)
        self.ui.actionEdit_Preferences.triggered.connect(\
          self.edit_preferences)
        self.ui.actionClear_Cache.triggered.connect(\
          self.clear_cache)
        self.ui.actionSave_all.triggered.connect(\
          self.save_all)
        self.ui.actionSave_series_artwork.triggered.connect(\
          self.save_series_artwork)
        self.ui.actionSave_series_nfo.triggered.connect(\
          self.save_series_nfo)
        self.ui.actionSave_series_both.triggered.connect(\
          self.save_series_both)
        self.ui.actionSave_episode_artwork.triggered.connect(\
          self.save_episode_artwork)
        self.ui.actionSave_episode_nfo.triggered.connect(\
          self.save_episode_nfo)
        self.ui.actionSave_episode_both.triggered.connect(\
          self.save_episode_both)
        self.save_files.started.connect(self.started_status)
        self.save_files.finished.connect(self.finished_status)
        self.save_files.terminated.connect(self.terminated_status)
        self.connect(self.save_files, \
                     QtCore.SIGNAL("updateStatus(QString)"), \
                     self.update_status)
        self.connect(self.save_files, \
                     QtCore.SIGNAL("updateProgress(int)"), \
                     self.update_progress)
        self.connect(self.save_files, \
                     QtCore.SIGNAL("setupProgress(int)"), \
                     self.setup_progress)

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
        self.episode_tvdb_rating_updated = 0

        #Create some empty lists for later
        self.series_banners_url = []
        self.series_banners_wide_url = []
        self.series_fanart_banners_url = []
        self.season_banners_url = []
        self.season_banners_wide_url = []

        #Initialize the configuration dialog
        self.config_dialog = ConfigDialog()
        self.config_dialog.accepted.connect(self.read_config)
        
        self.ui.pushButton_save_series_changes.setEnabled(0)
        self.ui.pushButton_revert_series_changes.setEnabled(0)
        self.ui.pushButton_save_episode_changes.setEnabled(0)
        self.ui.pushButton_revert_episode_changes.setEnabled(0)
        self.ui.pushButton_new_series_poster.setEnabled(0)
        self.ui.pushButton_new_series_wide_banner.setEnabled(0)
        self.ui.pushButton_new_season_poster.setEnabled(0)
        self.ui.pushButton_new_season_wide.setEnabled(0)
        self.ui.pushButton_load_local_series_nfo.setEnabled(0)
        self.ui.pushButton_load_local_episode_nfo.setEnabled(0)
        self.ui.pushButton_update_series_from_tvdb.setEnabled(0)
        self.ui.pushButton_update_episode_from_tvdb.setEnabled(0)

        #Put a progress bar on the status bar
        self.pb = QtGui.QProgressBar()
        self.statusBar().addPermanentWidget(self.pb)

    def list_view_clicked(self, index):
        """Determines what was clicked in the column view tree"""
        #other functions need to know where we are in the tree
        self.index = index
        #Find the series we are working with
        self.series_name = index.data().toString()
        self.clear_season_info()
        self.clear_episode_info()
        self.set_column_view()
        self.set_series_info(0)
        self.ui.pushButton_save_series_changes.setEnabled(0)
        self.ui.pushButton_revert_series_changes.setEnabled(0)
        self.ui.pushButton_new_series_poster.setEnabled(1)
        self.ui.pushButton_new_series_wide_banner.setEnabled(1)
        self.ui.pushButton_new_season_poster.setEnabled(0)
        self.ui.pushButton_new_season_wide.setEnabled(0)

    def column_view_clicked(self, index):
        """Determines what was clicked in the column view tree"""
        #other functions need to know where we are in the tree
        self.index = index
        #Find the series we are working with
        this_node_data = index.data().toString()
        parent = index.parent()
        parent_data = parent.data().toString()

        if parent_data == "":    #we are at the season level
            season_number = this_node_data
            if str(season_number) == 'Specials':
                self.season_number = 0 
            else:
                self.season_number = int(season_number)
            self.clear_episode_info()
            self.set_season_info()
            self.ui.pushButton_new_season_poster.setEnabled(1)
            self.ui.pushButton_new_season_wide.setEnabled(1)
        else:                           #we are at the episode level
            season_number = parent_data
            if str(season_number) == 'Specials':
                self.season_number = 0 
            else:
                self.season_number = int(season_number)
            self.episode_number = \
              int(str(this_node_data.split("-")[0]).rstrip())
            self.set_season_info()
            self.set_episode_info()
            self.ui.pushButton_save_episode_changes.setEnabled(0)
            self.ui.pushButton_revert_episode_changes.setEnabled(0)

    def set_series_name_updated(self, text):
        self.series_name_updated = 1
        self.new_series_name = str(text)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def set_series_overview_updated(self):
        self.series_overview_updated = 1
        self.new_series_overview = \
          unicode(self.ui.plainTextEdit_overview.toPlainText(), "latin-1")
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def set_series_network_updated(self, text):
        self.series_network_updated = 1
        self.new_series_network = str(text)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def set_series_airtime_updated(self, text):
        self.series_airtime_updated = 1
        self.new_series_airtime = str(text)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def set_series_runtime_updated(self, text):
        self.series_runtime_updated = 1
        self.new_series_runtime = str(text)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def set_series_status_updated(self, text):
        self.series_status_updated = 1
        self.new_series_status = str(text)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def update_series(self):
        series_id = dbTV.get_series_id(self.series_name)
        if self.series_name_updated == 1:
            dbTV.update_series_field('name', self.new_series_name, series_id)
            self.series_name=self.new_series_name
        if self.series_overview_updated == 1:
            dbTV.update_series_field('overview', \
                                     self.new_series_overview, series_id)
        if self.series_network_updated == 1:
            pass
        if self.series_airtime_updated == 1:
            new_series_airs_time = self.new_series_airtime.split(' at ')[1]
            new_series_airs_day = self.new_series_airtime.split(' at ')[0]
            dbTV.update_series_field('airs_time', \
                                     new_series_airs_time, series_id)
            dbTV.update_series_field('airs_day', \
                                     new_series_airs_day, series_id)
        if self.series_runtime_updated == 1:
            dbTV.update_series_field('runtime', \
                                     self.new_series_runtime, series_id)
        if self.series_status_updated == 1:
            dbTV.update_series_field('status', \
                                     self.new_series_status, series_id)
        self.ui.pushButton_save_series_changes.setEnabled(0)
        self.ui.pushButton_revert_series_changes.setEnabled(0)

    def revert_series(self):
        self.set_series_info(0)
        self.ui.pushButton_save_series_changes.setEnabled(0)
        self.ui.pushButton_revert_series_changes.setEnabled(0)

    def load_series_nfo(self):
        series_id = dbTV.get_series_id(self.series_name)
        series_nfo = dbTV.get_series_nfo_filename(series_id)
        series_doc = nfo_reader.readNfo(series_nfo)
        self.set_series_info_from_dom(series_doc, 0)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def update_series_from_tvdb(self):
        series_id = dbTV.get_series_id(self.series_name)
        series = TVDB.get_series_info(series_id)
        dom = dom_from_series(series)
        self.set_series_info_from_dom(dom, 0)
        self.ui.pushButton_save_series_changes.setEnabled(1)
        self.ui.pushButton_revert_series_changes.setEnabled(1)

    def set_episode_name_updated(self, text):
        self.episode_name_updated = 1
        self.new_episode_name = str(text)
        self.ui.pushButton_save_episode_changes.setEnabled(1)
        self.ui.pushButton_revert_episode_changes.setEnabled(1)

    def set_episode_plot_updated(self):
        self.episode_plot_updated = 1
        self.new_episode_plot = \
          str(self.ui.text_episode_plot.toPlainText().toUtf8())
        self.ui.pushButton_save_episode_changes.setEnabled(1)
        self.ui.pushButton_revert_episode_changes.setEnabled(1)

    def set_episode_airdate_updated(self, text):
        self.episode_airdate_updated = 1
        self.new_episode_airdate = str(text)
        self.ui.pushButton_save_episode_changes.setEnabled(1)
        self.ui.pushButton_revert_episode_changes.setEnabled(1)

    def set_episode_tvdb_rating_updated(self, text):
        self.episode_tvdb_rating_updated = 1
        self.new_episode_tvdb_rating = str(text)
        self.ui.pushButton_save_episode_changes.setEnabled(1)
        self.ui.pushButton_revert_episode_changes.setEnabled(1)

    def update_episode(self):
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)
        if self.episode_name_updated == 1:
            dbTV.update_episode_field('name', \
                                      self.new_episode_name, episode_id)
        if self.episode_plot_updated == 1:
            dbTV.update_episode_field('overview', \
                                      self.new_episode_plot, episode_id)
        if self.episode_airdate_updated == 1:
            dbTV.update_episode_field('first_aired', \
                                      self.new_episode_airdate, episode_id)
        if self.episode_tvdb_rating_updated == 1:
            dbTV.update_episode_field('rating', \
                                      self.new_episode_tvdb_rating, episode_id)
        self.ui.pushButton_save_episode_changes.setEnabled(0)
        self.ui.pushButton_revert_episode_changes.setEnabled(0)

    def revert_episode(self):
        self.set_episode_info()
        self.ui.pushButton_save_episode_changes.setEnabled(0)
        self.ui.pushButton_revert_episode_changes.setEnabled(0)

    def load_episode_nfo(self):
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)
        episode_nfo = dbTV.get_episode_nfo_filename(episode_id)
        dom = nfo_reader.readNfo(episode_nfo)
        if dom is not None:
            self.set_episode_info_from_dom(dom)
            self.ui.pushButton_save_episode_changes.setEnabled(1)
            self.ui.pushButton_revert_episode_changes.setEnabled(1)

    def update_episode_from_tvdb(self):
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)
        episode = TVDB.get_episode_info(episode_id)
        dom = dom_from_episode(episode)
        self.set_episode_info_from_dom(dom)
        self.ui.pushButton_save_episode_changes.setEnabled(1)
        self.ui.pushButton_revert_episode_changes.setEnabled(1)

    def set_column_view(self):
        dom = dbTV.make_seasons_episodes_dom(self.series_name)
        model = SeasonEpisodeModel(dom)
        self.ui.columnView_season_episode.setModel(model)
        self.ui.columnView_season_episode.setColumnWidths([300,550,50])

    def set_season_info(self):
        """Sets the info for the current season in the display window"""
        series_id = dbTV.get_series_id(self.series_name)
        season_list = dbTV.make_episodes_list(series_id, self.season_number)
        model = SeasonListModel(season_list)
        self.ui.listView_season_episode_full.setModel(model)
        self.selected_season_poster = dbTV.get_selected_banner_url(\
          series_id, 'season', self.season_number)
        if not self.selected_season_poster == "":
            filename = TVDB.retrieve_banner(self.selected_season_poster)
            season_poster_pixmap = QtGui.QPixmap(filename).scaled(300, 450,\
                                                  QtCore.Qt.KeepAspectRatio)
            self.ui.label_season_poster.setPixmap(season_poster_pixmap)
        else:
            self.ui.label_season_poster.clear()
            self.ui.label_season_poster.setText("No season poster selected")
        self.selected_season_banner_wide = dbTV.get_selected_banner_url(\
          series_id, 'seasonwide', self.season_number)
        if not self.selected_season_banner_wide == "":
            filename = TVDB.retrieve_banner(self.selected_season_banner_wide)
            season_banner_wide_pixmap = \
              QtGui.QPixmap(filename).scaledToHeight(140)
            self.ui.label_season_banner_wide.setPixmap(\
              season_banner_wide_pixmap)
        else:   
            self.ui.label_season_banner_wide.clear()
            self.ui.label_season_banner_wide.setText(\
              "No season wide banner selected")

    def set_series_info(self, tab_index):
        #Get the series id from the database
        series_id = dbTV.get_series_id(self.series_name)

        #Create a QDomDocument containing the series details
        series_doc = dbTV.make_series_dom(series_id)
        self.set_series_info_from_dom(series_doc, tab_index)        
        self.ui.pushButton_load_local_series_nfo.setEnabled(1)
        self.ui.pushButton_update_series_from_tvdb.setEnabled(1)

    def set_series_info_from_dom(self, series_doc, tab_index):
        """Sets the info for the current series in the display window"""
        series_root = series_doc.firstChildElement('tvshow')
        #Extract the details and fill in the display
        elem_series_name = series_root.firstChildElement('title')
        series_name = elem_series_name.text()
        self.ui.lineEdit_series_name.setText(series_name)

        elem_series_plot = series_root.firstChildElement('plot')
        series_plot = QtCore.QString(elem_series_plot.text())
        self.ui.plainTextEdit_overview.setPlainText(series_plot)

        series_actors = []
        self.ui.combo_actors.clear()
        elem_series_actor = series_root.firstChildElement('actor')
        while not elem_series_actor.isNull():
            elem_series_actor_name = \
              elem_series_actor.firstChildElement('name')
            series_actor_name = elem_series_actor_name.text()
            if not series_actor_name in series_actors:
                series_actors.append(series_actor_name)
            elem_series_actor = elem_series_actor.nextSiblingElement('actor')

        series_actors.sort()
        for series_actor in series_actors:
            self.ui.combo_actors.addItem(series_actor)

        elem_series_network = series_root.firstChildElement('network')
        series_network = elem_series_network.text()
        self.ui.lineEdit_network.setText(series_network)

        elem_series_airs_day = series_root.firstChildElement('airsday')
        series_airs_day = elem_series_airs_day.text()
        elem_series_airs_time = series_root.firstChildElement('airstime')
        series_airs_time = elem_series_airs_time.text()
        if not series_airs_day == '':
            series_airtime = series_airs_day + " at " + series_airs_time
        else:
            series_airtime = ''
        self.ui.lineEdit_airtime.setText(series_airtime)

        elem_series_runtime = series_root.firstChildElement('runtime')
        series_runtime = elem_series_runtime.text()
        self.ui.lineEdit_runtime.setText(series_runtime)

        elem_series_status = series_root.firstChildElement('status')
        series_status = elem_series_status.text()
        self.ui.lineEdit_status.setText(series_status)

        series_id = dbTV.get_series_id(self.series_name)
        self.ui.lineEdit_tvdb_series_id.setText(str(series_id))        

        self.selected_series_poster = \
          dbTV.get_selected_banner_url(series_id, 'poster', '')
        if not self.selected_series_poster == "":
            filename = TVDB.retrieve_banner(self.selected_series_poster)
            series_poster_pixmap = QtGui.QPixmap(filename).scaledToHeight(450)
            self.ui.label_series_banner.setPixmap(series_poster_pixmap)
        else:
            self.ui.label_series_banner.clear()
            self.ui.label_series_banner.setText("No series poster selected")

        self.selected_series_wide_banner = \
          dbTV.get_selected_banner_url(series_id, 'series', '')
        if not self.selected_series_wide_banner == "":
            filename = TVDB.retrieve_banner(self.selected_series_wide_banner)
            series_wide_pixmap = QtGui.QPixmap(filename).scaledToHeight(140)
            self.ui.label_banner_wide.setPixmap(series_wide_pixmap)
        else:
            self.ui.label_banner_wide.clear()
            self.ui.label_banner_wide.setText("No series wide banner selected")

        self.selected_series_fanart = \
          dbTV.get_selected_banner_url(series_id, 'fanart', '')
        if not self.selected_series_fanart == "":
            filename = TVDB.retrieve_banner(self.selected_series_fanart)
            series_fanart_pixmap = QtGui.QPixmap(filename).scaledToHeight(480)
            self.ui.label_series_fanart.setPixmap(series_fanart_pixmap)
        else:
            self.ui.label_series_fanart.clear()
            self.ui.label_series_fanart.setText("No fanart selected")

        self.ui.tabWidget_tv_info.setCurrentIndex(tab_index)

    def set_episode_info(self):
        """Sets the info for the show in the display window"""
        #Get the episode_id from the database
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)

        #Create a QDomDocument containing the episode details
        episode_doc = dbTV.make_episode_dom(episode_id)
        self.set_episode_info_from_dom(episode_doc)
        self.ui.pushButton_load_local_episode_nfo.setEnabled(1)
        self.ui.pushButton_update_episode_from_tvdb.setEnabled(1)

    def set_episode_info_from_dom(self, dom):
        """Sets the info for the show in the display window"""
        episode_root = dom.firstChildElement('episodedetails')

        #Extract the details and fill in the display
        elem_episode_title = episode_root.firstChildElement('title')
        episode_title = elem_episode_title.text()
        self.ui.line_episode_name.setText(episode_title)

        elem_episode_plot = episode_root.firstChildElement('plot')
        episode_plot = QtCore.QString(elem_episode_plot.text())
        self.ui.text_episode_plot.setPlainText(episode_plot)

        elem_episode_thumb = episode_root.firstChildElement('thumb')
        if not elem_episode_thumb.isNull():
            episode_thumb = elem_episode_thumb.text()
        else:
            episode_thumb = "none"
        #Set the preview image
        image_file = TVDB.retrieve_banner(str(episode_thumb))
        if image_file is not None:
            image = QtGui.QPixmap(image_file)
            self.ui.label_episode_thumb.setPixmap(image)

        elem_episode_airdate = episode_root.firstChildElement('aired')
        episode_airdate = elem_episode_airdate.text()
        self.ui.line_airdate.setText(episode_airdate)

        elem_episode_id = episode_root.firstChildElement('id')
        episode_id = elem_episode_id.text()
        self.ui.line_tvdb_id.setText(episode_id)

        elem_episode_rating = episode_root.firstChildElement('rating')
        episode_rating = elem_episode_rating.text()
        self.ui.line_tvdb_rating.setText(episode_rating)

        elem_episode_directors = episode_root.firstChildElement('director')
        episode_directors = elem_episode_directors.text().split("|")
        self.ui.combo_directors.clear()
        i = 0
        while i < episode_directors.count():
            self.ui.combo_directors.addItem(episode_directors.takeAt(i))
            i = i + 1

        elem_episode_writers = episode_root.firstChildElement('credits')
        episode_writers = elem_episode_writers.text().split("|")
        self.ui.combo_writers.clear()
        i = 0
        while i < episode_writers.count():
            self.ui.combo_writers.addItem(episode_writers.takeAt(i))
            i = i + 1

        episode_actors = []
        elem_episode_actor = episode_root.firstChildElement('actor')
        self.ui.combo_guests.clear()
        while not elem_episode_actor.isNull():
            elem_episode_actor_name = \
              elem_episode_actor.firstChildElement('name')
            episode_actor_name = elem_episode_actor_name.text()
            episode_actors.append(episode_actor_name)
            elem_episode_actor = elem_episode_actor.nextSiblingElement('actor')

        episode_actors = set(episode_actors)
        for episode_actor in episode_actors:
            if self.ui.combo_actors.findText(episode_actor) < 0:
                self.ui.combo_guests.addItem(episode_actor)

        self.ui.tabWidget_tv_info.setCurrentIndex(3)

    def clear_episode_info(self):
        """Clears the episode info from the display window"""
        self.ui.line_episode_name.clear()
        self.ui.text_episode_plot.clear()
        self.ui.line_airdate.clear()
        self.ui.line_tvdb_id.clear()
        self.ui.line_tvdb_rating.clear()
        self.ui.combo_directors.clear()
        self.ui.combo_writers.clear()
        self.ui.combo_guests.clear()
        self.ui.label_episode_thumb.clear()
        
    def clear_season_info(self):
        model = EmptyListModel()
        self.ui.listView_season_episode_full.setModel(model)
        self.ui.label_season_poster.clear()
        self.ui.label_season_banner_wide.clear()

    def select_series_poster(self):
        banner_dialog = BannerDialog(self.series_name, "series_posters", 0)
        accepted = banner_dialog.exec_()
        if accepted:
            self.set_series_info(0)
        self.ui.pushButton_new_series_poster.setDown(False)

    def select_series_wide_banner(self):
        banner_dialog = BannerDialog(self.series_name, "series_wide", 0)
        accepted = banner_dialog.exec_()
        if accepted:
            self.set_series_info(0)
        self.ui.pushButton_new_series_wide_banner.setDown(False)

    def select_series_fanart(self):
        banner_dialog = BannerDialog(self.series_name, "series_fanart", 0)
        accepted = banner_dialog.exec_()
        if accepted:
            self.set_series_info(1)
        self.ui.pushButton_new_series_fanart.setDown(False)

    def select_season_poster(self):
        banner_dialog = BannerDialog(self.series_name, \
                                     "season_posters", \
                                      self.season_number)
        accepted = banner_dialog.exec_()
        if accepted:
            self.set_season_info()
        self.ui.pushButton_new_season_poster.setDown(False)

    def select_season_wide_banner(self):
        banner_dialog = BannerDialog(self.series_name, \
                                     "season_wide", \
                                     self.season_number)
        accepted = banner_dialog.exec_()
        if accepted:
            self.set_season_info()
        self.ui.pushButton_new_season_wide.setDown(False)

    def scan_files(self):
        for video_dir in config.tv_dirs:
            self.progress.setLabelText("Scanning Files from %s into DB..." \
                                       %  (video_dir))
            self.logger.info("Scanning files")
            scanner = Scanner(video_dir)
            scanner.set_series_list()
            self.progress.setMaximum(len(scanner.series_list))
            self.progress.setValue(0)
            for series_name in scanner.series_list:
                self.progress.setValue(scanner.series_list.index(series_name))
                match_list = scanner.get_series_id_list(series_name)
                if len(match_list) == 0:
                    self.logger.info("No matches found on thetvdb.com for '%s'." % (series_name))
                    series_id = raw_input("Please input the ID for the correct series:")
                elif len(match_list) == 1:
                    self.logger.info("Found match for '%s'." % (series_name))
                    series_id = match_list[0][0]
                else:
                    match = False
                    list = ''
                    for i in range(0,len(match_list)):
                        if match_list[i][1] == series_name:
                            self.logger.info("Found match for '%s'." % (series_name))
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
                            self.logger.info("That is not an option.")
                if config.prefer_local:
                    self.logger.info("Adding info from local nfo files")
                    scanner.add_series_to_db_by_nfo(series_name)
                else:
                    self.logger.info("Adding info from thetvdb.com")
                    scanner.add_series_to_db_by_id(series_id)
                scanner.add_files_to_db(series_id, series_name)
            dbTV.clean_unlinked_files()
            dbTV.remove_shows_with_no_files()
            scanner.__del__()
            self.progress.setValue(len(scanner.series_list))

        self.logger.info("Finished Scanning")
        #Create a dom representing the shows in the database
        shows = dbTV.make_shows_list()
        #Turn that into a model
        model = ShowListModel(shows)
        #Set that as the model for the listView
        self.ui.listView_shows.setModel(model)

    def edit_preferences(self):
        self.config_dialog.show()

    def read_config(self):
        config.read_config_file()

    def clear_cache(self):
        top = os.path.join(config.config_dir, "cache")
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def save_all(self):
        self.save_files.save_all(self.shows)

    def save_series_artwork(self):
        series_id = dbTV.get_series_id(self.series_name)
        self.save_files.save_series_artwork(series_id)

    def save_series_nfo(self):
        series_id = dbTV.get_series_id(self.series_name)
        self.save_files.save_series_nfos(series_id)

    def save_series_both(self):
        series_id = dbTV.get_series_id(self.series_name)
        self.save_files.save_series_both(series_id)

    def save_episode_artwork(self):
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)
        dbTV.write_episode_thumb(episode_id)

    def save_episode_nfo(self):
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)
        dbTV.write_episode_nfo(episode_id)

    def save_episode_both(self):
        episode_id = dbTV.get_episode_id(self.series_name, \
                                         self.season_number, \
                                         self.episode_number)
        dbTV.write_episode_nfo(episode_id)
        dbTV.write_episode_thumb(episode_id)

    def started_status(self):
        self.statusBar().showMessage("Saving files.")
        self.pb.show()

    def finished_status(self):
        self.pb.hide()
        self.statusBar().showMessage("File saving finished.")

    def terminated_status(self):
        self.pb.hide()
        self.statusBar().showMessage("File saving terminated.")

    def update_status(self, show):
        self.statusBar().showMessage("Saving info and artwork for %s" % (show,))

    def update_progress(self, progress):
        self.pb.setValue(progress)

    def setup_progress(self, max):
        self.pb.setRange(0, max)

class SaveFiles(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.db = TVShowDB(config.tvshowdb)

    def __del__(self):
        self.exiting = True
        self.wait()

    def save_all(self, shows):
        self.shows = shows
        self.which = 'all'
        self.start()

    def save_series_artwork(self, series_id):
        self.series_id = series_id
        self.which = 'series_artwork'
        self.start()

    def save_series_nfos(self, series_id):
        self.series_id = series_id
        self.which = 'series_nfos'
        self.start()

    def save_series_both(self, series_id):
        self.series_id = series_id
        self.which = 'series_both'
        self.start()

    def run(self):
        if self.which == 'all':
            for show in self.shows:
                self.emit(QtCore.SIGNAL("updateStatus(QString)"), \
                          QtCore.QString(show))
                series_id = self.db.get_series_id(show)
                self.db.write_series_nfo(series_id)
                self.db.write_series_posters(series_id)
                episode_ids = self.db.get_all_episode_ids(series_id)
                self.emit(QtCore.SIGNAL("setupProgress(int)"), \
                          len(episode_ids))
                for episode_id in episode_ids:
                    self.emit(QtCore.SIGNAL("updateProgress(int)"), \
                              episode_ids.index(episode_id))
                    self.db.write_episode_nfo(episode_id)
                    self.db.write_episode_thumb(episode_id)

        elif self.which == 'series_artwork': 
            show = self.db.get_series_name(self.series_id)
            if show is not None:
                self.emit(QtCore.SIGNAL("updateStatus(QString)"), \
                          QtCore.QString(show))
                self.db.write_series_posters(self.series_id)
                episode_ids = self.db.get_all_episode_ids(self.series_id)
                self.emit(QtCore.SIGNAL("setupProgress(int)"), \
                          len(episode_ids))
                for episode_id in episode_ids:
                    self.emit(QtCore.SIGNAL("updateProgress(int)"), \
                              episode_ids.index(episode_id))
                    self.db.write_episode_thumb(episode_id)

        elif self.which == 'series_nfos': 
            show = self.db.get_series_name(self.series_id)
            if show is not None:
                self.emit(QtCore.SIGNAL("updateStatus(QString)"), \
                          QtCore.QString(show))
                self.db.write_series_nfo(self.series_id)
                episode_ids = self.db.get_all_episode_ids(self.series_id)
                self.emit(QtCore.SIGNAL("setupProgress(int)"), \
                          len(episode_ids))
                for episode_id in episode_ids:
                    self.emit(QtCore.SIGNAL("updateProgress(int)"), \
                              episode_ids.index(episode_id))
                    self.db.write_episode_nfo(episode_id)

        elif self.which == 'series_both': 
            show = self.db.get_series_name(self.series_id)
            if show is not None:
                self.emit(QtCore.SIGNAL("updateStatus(QString)"), \
                          QtCore.QString(show))
                self.db.write_series_nfo(self.series_id)
                self.db.write_series_posters(self.series_id)
                episode_ids = self.db.get_all_episode_ids(self.series_id)
                self.emit(QtCore.SIGNAL("setupProgress(int)"), \
                          len(episode_ids))
                for episode_id in episode_ids:
                    self.emit(QtCore.SIGNAL("updateProgress(int)"), \
                              episode_ids.index(episode_id))
                    self.db.write_episode_nfo(episode_id)
                    self.db.write_episode_thumb(episode_id)
