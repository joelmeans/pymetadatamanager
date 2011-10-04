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
#                                                                          #
# Sorry for all of the commenting.  This was originally generated using    #
# Qt4 Designer and pyuic4.  I needed to do some things I couldn't figure   #
# out using Designer, so I had to go through and figure out what was going #
# on here.  So, I commented every little thing as I went.                  #
#                                                                          #
############################################################################

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    """This class defines the main window layout"""
    def setupUi(self, MainWindow):
        """Sets up the main window"""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1154, 934)

        #Create the central widget (the primary one for the MainWindow)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Now, the main tab widget (tabs for TV and Movies)
        self.tabWidget_main = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_main.setGeometry(QtCore.QRect(10, 0, 1131, 891))
        self.tabWidget_main.setObjectName("tabWidget_main")

        #The TV tab
        self.tab_tv = QtGui.QWidget()
        self.tab_tv.setObjectName("tab_tv")

        #A column view for the tree of shows
        self.columnView_show_tree = QtGui.QColumnView(self.tab_tv)
        self.columnView_show_tree.setGeometry(QtCore.QRect(0, 0, 1121, 331))
        self.columnView_show_tree.setAlternatingRowColors(True)
        self.columnView_show_tree.setObjectName("columnView_show_tree")

        #A tab widget for TV info
        self.tabWidget_tv_info = QtGui.QTabWidget(self.tab_tv)
        self.tabWidget_tv_info.setGeometry(QtCore.QRect(0, 350, 1121, 511))
        self.tabWidget_tv_info.setObjectName("tabWidget_tv_info")

        #The series info tab
        self.tab_series_info = QtGui.QWidget()
        self.tab_series_info.setObjectName("tab_series_info")

        #A layout widget for the left side series info
        self.layoutWidget = QtGui.QWidget(self.tab_series_info)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 531, 471))
        self.layoutWidget.setObjectName("layoutWidget")

        #A form layout within the layout widget for the series info
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout.setObjectName("formLayout")

        #Now all of the labels and line or text edit boxes
        self.label_series_name = QtGui.QLabel(self.layoutWidget)
        self.label_series_name.setObjectName("label_series_name")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_series_name)

        self.line_series_name = QtGui.QLineEdit(self.layoutWidget)
        self.line_series_name.setObjectName("line_series_name")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.line_series_name)

        self.label_series_overview = QtGui.QLabel(self.layoutWidget)
        self.label_series_overview.setObjectName("label_series_overview")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_series_overview)

        self.text_series_overview = QtGui.QTextEdit(self.layoutWidget)
        self.text_series_overview.setObjectName("text_series_overview")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.text_series_overview)

        self.label_network = QtGui.QLabel(self.layoutWidget)
        self.label_network.setObjectName("label_network")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_network)

        self.line_network = QtGui.QLineEdit(self.layoutWidget)
        self.line_network.setObjectName("line_network")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.line_network)

        self.label_airtime = QtGui.QLabel(self.layoutWidget)
        self.label_airtime.setObjectName("label_airtime")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_airtime)

        self.line_airtime = QtGui.QLineEdit(self.layoutWidget)
        self.line_airtime.setObjectName("line_airtime")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.line_airtime)

        self.label_runtime = QtGui.QLabel(self.layoutWidget)
        self.label_runtime.setObjectName("label_runtime")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_runtime)

        self.line_runtime = QtGui.QLineEdit(self.layoutWidget)
        self.line_runtime.setObjectName("line_runtime")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.line_runtime)

        self.label_status = QtGui.QLabel(self.layoutWidget)
        self.label_status.setObjectName("label_status")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_status)

        self.line_status = QtGui.QLineEdit(self.layoutWidget)
        self.line_status.setObjectName("line_status")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.line_status)

        #A layout widget for the right column of the series info
        self.layoutWidget1 = QtGui.QWidget(self.tab_series_info)
        self.layoutWidget1.setGeometry(QtCore.QRect(550, 0, 561, 471))
        self.layoutWidget1.setObjectName("layoutWidget1")

        #A form layout within the layout widget for the series info
        self.formLayout1 = QtGui.QFormLayout(self.layoutWidget1)
        self.formLayout1.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.formLayout1.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout1.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout1.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout1.setObjectName("formLayout1")

        #All of the labels and edit boxes for the rest of the series info
        self.label_actors = QtGui.QLabel(self.layoutWidget1)
        self.label_actors.setObjectName("label_actors")
        self.formLayout1.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_actors)

        self.combo_actors = QtGui.QComboBox(self.layoutWidget1)
        self.combo_actors.setObjectName("combo_actors")
        self.formLayout1.setWidget(0, QtGui.QFormLayout.FieldRole, self.combo_actors)

        self.label_actor_thumb = QtGui.QLabel(self.layoutWidget1)
        self.label_actor_thumb.setObjectName("label_actor_thumb")
        self.formLayout1.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_actor_thumb)

        self.pushButton_save_series_changes = QtGui.QPushButton(self.layoutWidget1)
        self.pushButton_save_series_changes.setObjectName("pushButton_save_series_changes")
        self.formLayout1.setWidget(4, QtGui.QFormLayout.FieldRole, self.pushButton_save_series_changes)
        self.pushButton_save_series_changes.setEnabled(0)

        self.pushButton_revert_series_changes = QtGui.QPushButton(self.layoutWidget1)
        self.pushButton_revert_series_changes.setObjectName("pushButton_revert_series_changes")
        self.formLayout1.setWidget(5, QtGui.QFormLayout.FieldRole, self.pushButton_revert_series_changes)
        self.pushButton_revert_series_changes.setEnabled(0)

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout1.setItem(1, QtGui.QFormLayout.FieldRole, spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout1.setItem(3, QtGui.QFormLayout.FieldRole, spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout1.setItem(2, QtGui.QFormLayout.LabelRole, spacerItem2)

        #Now add the tv series info tab to the tv info tab widget
        self.tabWidget_tv_info.addTab(self.tab_series_info, "")

        #Create the series artwork tab
        self.tab_series_artwork = QtGui.QWidget()
        self.tab_series_artwork.setObjectName("tab_series_artwork")

        #Make the series artwork tab widget (to hold tabs for posters, wide banners and fanart)
        self.tabWidget_series_artwork = QtGui.QTabWidget(self.tab_series_artwork)
        self.tabWidget_series_artwork.setGeometry(QtCore.QRect(0, 0, 1121, 481))
        self.tabWidget_series_artwork.setObjectName("tabWidget_series_artwork")

        #Add the tab for series posters (banners)
        self.tab_series_banners = QtGui.QWidget()
        self.tab_series_banners.setObjectName("tab_series_banners")

        #A table view for the series posters on the tab
        self.tableView_series_banners = QtGui.QTableView(self.tab_series_banners)
        self.tableView_series_banners.setGeometry(QtCore.QRect(0, 0, 1111, 451))
        self.tableView_series_banners.setObjectName("tableView_series_banners")

        #Add the tab to the tab widget
        self.tabWidget_series_artwork.addTab(self.tab_series_banners, "")

        #Add the tab for series wide banners
        self.tab_series_banners_wide = QtGui.QWidget()
        self.tab_series_banners_wide.setObjectName("tab_series_banners_wide")

        #A table view for the series wide banners
        self.tableView_series_banners_wide = QtGui.QTableView(self.tab_series_banners_wide)
        self.tableView_series_banners_wide.setGeometry(QtCore.QRect(0, 0, 1111, 451))
        self.tableView_series_banners_wide.setObjectName("tableView_series_banners_wide")

        #Add the tab to the tab widget
        self.tabWidget_series_artwork.addTab(self.tab_series_banners_wide, "")

        #Add the tab for fanart
        self.tab_series_fanart = QtGui.QWidget()
        self.tab_series_fanart.setObjectName("tab_series_fanart")

        #A table view for the fanart
        self.tableView_series_fanart = QtGui.QTableView(self.tab_series_fanart)
        self.tableView_series_fanart.setGeometry(QtCore.QRect(0, 0, 1111, 451))
        self.tableView_series_fanart.setObjectName("tableView_series_fanart")

        #Add the tab to the tab widget
        self.tabWidget_series_artwork.addTab(self.tab_series_fanart, "")

        #Add the series artwork tab to the tv info tab widget
        self.tabWidget_tv_info.addTab(self.tab_series_artwork, "")

        #Add the season artwork tab
        self.tab_season_artwork = QtGui.QWidget()
        self.tab_season_artwork.setObjectName("tab_season_artwork")

        #Add a tab widget for season artwork (to hold posters and wide banners)
        self.tabWidget_season_artwork = QtGui.QTabWidget(self.tab_season_artwork)
        self.tabWidget_season_artwork.setGeometry(QtCore.QRect(0, 0, 1111, 481))
        self.tabWidget_season_artwork.setObjectName("tabWidget_season_artwork")

        #Add the season posters (banners) tab
        self.tab_season_banners = QtGui.QWidget()
        self.tab_season_banners.setObjectName("tab_season_banners")

        #A table view for the season posters
        self.tableView_season_banners = QtGui.QTableView(self.tab_season_banners)
        self.tableView_season_banners.setGeometry(QtCore.QRect(0, 0, 1101, 451))
        self.tableView_season_banners.setObjectName("tableView_season_banners")

        #Add the season posters tab to the tab widget
        self.tabWidget_season_artwork.addTab(self.tab_season_banners, "")

        #Add a season wide banners tab
        self.tab_season_banners_wide = QtGui.QWidget()
        self.tab_season_banners_wide.setObjectName("tab_season_banners_wide")

        #A table view for the season wide banners
        self.tableView_season_banners_wide = QtGui.QTableView(self.tab_season_banners_wide)
        self.tableView_season_banners_wide.setGeometry(QtCore.QRect(0, 0, 1101, 451))
        self.tableView_season_banners_wide.setObjectName("tableView_season_banners_wide")

        #Add the season wide banners tab to the tab widget
        self.tabWidget_season_artwork.addTab(self.tab_season_banners_wide, "")

        #Add the season artwork tab to the tv info tab widget
        self.tabWidget_tv_info.addTab(self.tab_season_artwork, "")

        #Add a tab for episode info
        self.tab_episode_info = QtGui.QWidget()
        self.tab_episode_info.setObjectName("tab_episode_info")

        #A layout widget to line up the episode info nicely
        self.layoutWidget2 = QtGui.QWidget(self.tab_episode_info)
        self.layoutWidget2.setGeometry(QtCore.QRect(3, 0, 541, 461))
        self.layoutWidget2.setObjectName("layoutWidget2")

        #A form layout for the info on the left
        self.formLayout2 = QtGui.QFormLayout(self.layoutWidget2)
        self.formLayout2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.formLayout2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout2.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout2.setObjectName("formLayout2")

        #The labels and edit boxes for the episode info on the left
        self.label_episode_name = QtGui.QLabel(self.layoutWidget2)
        self.label_episode_name.setObjectName("label_episode_name")
        self.formLayout2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_episode_name)

        self.line_episode_name = QtGui.QLineEdit(self.layoutWidget2)
        self.line_episode_name.setObjectName("line_episode_name")
        self.formLayout2.setWidget(0, QtGui.QFormLayout.FieldRole, self.line_episode_name)

        self.label_episode_plot = QtGui.QLabel(self.layoutWidget2)
        self.label_episode_plot.setObjectName("label_episode_plot")
        self.formLayout2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_episode_plot)

        self.text_episode_plot = QtGui.QPlainTextEdit(self.layoutWidget2)
        self.text_episode_plot.setObjectName("text_episode_plot")
        self.formLayout2.setWidget(1, QtGui.QFormLayout.FieldRole, self.text_episode_plot)

        self.line_airdate = QtGui.QLineEdit(self.layoutWidget2)
        self.line_airdate.setObjectName("line_airdate")
        self.formLayout2.setWidget(2, QtGui.QFormLayout.FieldRole, self.line_airdate)

        self.label_airdate = QtGui.QLabel(self.layoutWidget2)
        self.label_airdate.setObjectName("label_airdate")
        self.formLayout2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_airdate)

        self.line_tvdb_id = QtGui.QLineEdit(self.layoutWidget2)
        self.line_tvdb_id.setObjectName("line_tvdb_id")
        self.formLayout2.setWidget(3, QtGui.QFormLayout.FieldRole, self.line_tvdb_id)

        self.label_tvdb_id = QtGui.QLabel(self.layoutWidget2)
        self.label_tvdb_id.setObjectName("label_tvdb_id")
        self.formLayout2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_tvdb_id)

        self.label_tvdb_rating = QtGui.QLabel(self.layoutWidget2)
        self.label_tvdb_rating.setObjectName("label_tvdb_rating")
        self.formLayout2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_tvdb_rating)

        self.line_tvdb_rating = QtGui.QLineEdit(self.layoutWidget2)
        self.line_tvdb_rating.setObjectName("line_tvdb_rating")
        self.formLayout2.setWidget(4, QtGui.QFormLayout.FieldRole, self.line_tvdb_rating)

        #A layout widget for the right side info
        self.layoutWidget3 = QtGui.QWidget(self.tab_episode_info)
        self.layoutWidget3.setGeometry(QtCore.QRect(550, 0, 561, 461))
        self.layoutWidget3.setObjectName("layoutWidget3")

        #A form layout for the info on the right
        self.formLayout3 = QtGui.QFormLayout(self.layoutWidget3)
        self.formLayout3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.formLayout3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout3.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout3.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayout3.setObjectName("formLayout3")

        #Labels and edit boxes for the info on the right
        self.label_director = QtGui.QLabel(self.layoutWidget3)
        self.label_director.setObjectName("label_director")
        self.formLayout3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_director)

        self.combo_directors = QtGui.QComboBox(self.layoutWidget3)
        self.combo_directors.setObjectName("combo_directors")
        self.formLayout3.setWidget(1, QtGui.QFormLayout.FieldRole, self.combo_directors)

        self.label_writers = QtGui.QLabel(self.layoutWidget3)
        self.label_writers.setObjectName("label_writers")
        self.formLayout3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_writers)

        self.combo_writers = QtGui.QComboBox(self.layoutWidget3)
        self.combo_writers.setObjectName("combo_writers")
        self.formLayout3.setWidget(2, QtGui.QFormLayout.FieldRole, self.combo_writers)

        self.label_guests = QtGui.QLabel(self.layoutWidget3)
        self.label_guests.setObjectName("label_guests")
        self.formLayout3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_guests)

        self.combo_guests = QtGui.QComboBox(self.layoutWidget3)
        self.combo_guests.setObjectName("combo_guests")
        self.formLayout3.setWidget(3, QtGui.QFormLayout.FieldRole, self.combo_guests)

        self.pushButton_save_episode_changes = QtGui.QPushButton(self.layoutWidget3)
        self.pushButton_save_episode_changes.setObjectName("pushButton_save_episode_changes")
        self.formLayout3.setWidget(7, QtGui.QFormLayout.FieldRole, self.pushButton_save_episode_changes)
        self.pushButton_save_episode_changes.setEnabled(0)

        self.pushButton_revert_episode_changes = QtGui.QPushButton(self.layoutWidget3)
        self.pushButton_revert_episode_changes.setObjectName("pushButton_revert_episode_changes")
        self.formLayout3.setWidget(8, QtGui.QFormLayout.FieldRole, self.pushButton_revert_episode_changes)
        self.pushButton_revert_episode_changes.setEnabled(0)

        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout3.setItem(4, QtGui.QFormLayout.FieldRole, spacerItem3)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout3.setItem(5, QtGui.QFormLayout.LabelRole, spacerItem4)
        self.label_episode_thumb = QtGui.QLabel(self.layoutWidget3)
        self.label_episode_thumb.setObjectName("label_episode_thumb")
        self.formLayout3.setWidget(5, QtGui.QFormLayout.FieldRole, self.label_episode_thumb)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout3.setItem(6, QtGui.QFormLayout.FieldRole, spacerItem5)

        #Add the episode info tab to the tv info tab widget
        self.tabWidget_tv_info.addTab(self.tab_episode_info, "")

        #Add the tv info tab to the main tab widget
        self.tabWidget_main.addTab(self.tab_tv, "")

        #Create the tab for movie info
        self.tab_movies = QtGui.QWidget()
        self.tab_movies.setObjectName("tab_movies")
        self.tabWidget_main.addTab(self.tab_movies, "")

        #A bunch of grid layouts to make it all look good, even with resizing
        mainGrid = QtGui.QGridLayout()
        mainGrid.setSpacing(1)
        mainGrid.addWidget(self.tabWidget_main, 0, 0)
        self.centralwidget.setLayout(mainGrid)
        tvGrid = QtGui.QGridLayout()
        tvGrid.setSpacing(1)
        tvGrid.addWidget(self.columnView_show_tree, 0, 0)
        tvGrid.addWidget(self.tabWidget_tv_info, 1, 0)
        self.tab_tv.setLayout(tvGrid)
        seriesInfoGrid = QtGui.QGridLayout()
        seriesInfoGrid.setSpacing(1)
        seriesInfoGrid.addWidget(self.layoutWidget, 0, 0)
        seriesInfoGrid.addWidget(self.layoutWidget1, 0, 1)
        self.tab_series_info.setLayout(seriesInfoGrid)
        seriesArtworkGrid = QtGui.QGridLayout()
        seriesArtworkGrid.setSpacing(1)
        seriesArtworkGrid.addWidget(self.tabWidget_series_artwork, 0, 0)
        self.tab_series_artwork.setLayout(seriesArtworkGrid)
        seriesBannersGrid = QtGui.QGridLayout()
        seriesBannersGrid.setSpacing(1)
        seriesBannersGrid.addWidget(self.tableView_series_banners, 0, 0)
        self.tab_series_banners.setLayout(seriesBannersGrid)
        seriesBannersWideGrid = QtGui.QGridLayout()
        seriesBannersWideGrid.setSpacing(1)
        seriesBannersWideGrid.addWidget(self.tableView_series_banners_wide, 0, 0)
        self.tab_series_banners_wide.setLayout(seriesBannersWideGrid)
        seriesFanartGrid = QtGui.QGridLayout()
        seriesFanartGrid.setSpacing(1)
        seriesFanartGrid.addWidget(self.tableView_series_fanart, 0, 0)
        self.tab_series_fanart.setLayout(seriesFanartGrid)
        seasonArtworkGrid = QtGui.QGridLayout()
        seasonArtworkGrid.setSpacing(1)
        seasonArtworkGrid.addWidget(self.tabWidget_season_artwork, 0, 0)
        self.tab_season_artwork.setLayout(seasonArtworkGrid)
        seasonBannersGrid = QtGui.QGridLayout()
        seasonBannersGrid.setSpacing(1)
        seasonBannersGrid.addWidget(self.tableView_season_banners, 0, 0)
        self.tab_season_banners.setLayout(seasonBannersGrid)
        seasonBannersWideGrid = QtGui.QGridLayout()
        seasonBannersWideGrid.setSpacing(1)
        seasonBannersWideGrid.addWidget(self.tableView_season_banners_wide, 0, 0)
        self.tab_season_banners_wide.setLayout(seasonBannersWideGrid)
        episodeInfoGrid = QtGui.QGridLayout()
        episodeInfoGrid.setSpacing(1)
        episodeInfoGrid.addWidget(self.layoutWidget2, 0, 0)
        episodeInfoGrid.addWidget(self.layoutWidget3, 0, 1)
        self.tab_episode_info.setLayout(episodeInfoGrid)

        #Set the content of the main window
        MainWindow.setCentralWidget(self.centralwidget)

        #Create and populate the menu bar for the main window
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 22))
        self.menubar.setObjectName("menubar")
        self.menuTVDB_Scraper = QtGui.QMenu(self.menubar)
        self.menuTVDB_Scraper.setObjectName("menuTVDB_Scraper")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuTVDB_Scraper.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)

        #Set where to start when the program opens
        self.tabWidget_main.setCurrentIndex(0)
        self.tabWidget_tv_info.setCurrentIndex(0)
        self.tabWidget_series_artwork.setCurrentIndex(0)
        self.tabWidget_season_artwork.setCurrentIndex(0)

        #Connect the slots so it all works
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Sets the text for everything with localization"""
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_series_name.setText(QtGui.QApplication.translate("MainWindow", "Series Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_series_overview.setText(QtGui.QApplication.translate("MainWindow", "Overview", None, QtGui.QApplication.UnicodeUTF8))
        self.label_network.setText(QtGui.QApplication.translate("MainWindow", "Network", None, QtGui.QApplication.UnicodeUTF8))
        self.label_airtime.setText(QtGui.QApplication.translate("MainWindow", "Airtime", None, QtGui.QApplication.UnicodeUTF8))
        self.label_runtime.setText(QtGui.QApplication.translate("MainWindow", "Runtime", None, QtGui.QApplication.UnicodeUTF8))
        self.label_status.setText(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.label_actors.setText(QtGui.QApplication.translate("MainWindow", "Actors", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_save_series_changes.setText(QtGui.QApplication.translate("MainWindow", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_revert_series_changes.setText(QtGui.QApplication.translate("MainWindow", "Revert Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tv_info.setTabText(self.tabWidget_tv_info.indexOf(self.tab_series_info), QtGui.QApplication.translate("MainWindow", "Series Info", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_series_artwork.setTabText(self.tabWidget_series_artwork.indexOf(self.tab_series_banners), QtGui.QApplication.translate("MainWindow", "Posters", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_series_artwork.setTabText(self.tabWidget_series_artwork.indexOf(self.tab_series_banners_wide), QtGui.QApplication.translate("MainWindow", "Wide Banners", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_series_artwork.setTabText(self.tabWidget_series_artwork.indexOf(self.tab_series_fanart), QtGui.QApplication.translate("MainWindow", "Fanart", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tv_info.setTabText(self.tabWidget_tv_info.indexOf(self.tab_series_artwork), QtGui.QApplication.translate("MainWindow", "Series Artwork", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_season_artwork.setTabText(self.tabWidget_season_artwork.indexOf(self.tab_season_banners), QtGui.QApplication.translate("MainWindow", "Posters", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_season_artwork.setTabText(self.tabWidget_season_artwork.indexOf(self.tab_season_banners_wide), QtGui.QApplication.translate("MainWindow", "Wide Banners", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tv_info.setTabText(self.tabWidget_tv_info.indexOf(self.tab_season_artwork), QtGui.QApplication.translate("MainWindow", "Season Artwork", None, QtGui.QApplication.UnicodeUTF8))
        self.label_episode_name.setText(QtGui.QApplication.translate("MainWindow", "Episode Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_episode_plot.setText(QtGui.QApplication.translate("MainWindow", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_airdate.setText(QtGui.QApplication.translate("MainWindow", "Original Airdate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_tvdb_id.setText(QtGui.QApplication.translate("MainWindow", "thetvdb.com ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_tvdb_rating.setText(QtGui.QApplication.translate("MainWindow", "thetvdb.com Rating", None, QtGui.QApplication.UnicodeUTF8))
        self.label_director.setText(QtGui.QApplication.translate("MainWindow", "Director(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_writers.setText(QtGui.QApplication.translate("MainWindow", "Writer(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_guests.setText(QtGui.QApplication.translate("MainWindow", "Guest Stars", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_save_episode_changes.setText(QtGui.QApplication.translate("MainWindow", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_revert_episode_changes.setText(QtGui.QApplication.translate("MainWindow", "Revert Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_tv_info.setTabText(self.tabWidget_tv_info.indexOf(self.tab_episode_info), QtGui.QApplication.translate("MainWindow", "Episode Info", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_tv), QtGui.QApplication.translate("MainWindow", "TV Shows", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_movies), QtGui.QApplication.translate("MainWindow", "Movies", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTVDB_Scraper.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))

