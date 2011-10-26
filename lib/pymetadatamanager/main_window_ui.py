# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Wed Oct 26 09:26:32 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1143, 1174)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_tv = QtGui.QWidget()
        self.tab_tv.setObjectName(_fromUtf8("tab_tv"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tab_tv)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.listView_shows = QtGui.QListView(self.tab_tv)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_shows.sizePolicy().hasHeightForWidth())
        self.listView_shows.setSizePolicy(sizePolicy)
        self.listView_shows.setMinimumSize(QtCore.QSize(300, 0))
        self.listView_shows.setMaximumSize(QtCore.QSize(300, 16777215))
        self.listView_shows.setObjectName(_fromUtf8("listView_shows"))
        self.horizontalLayout.addWidget(self.listView_shows)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget_2 = QtGui.QTabWidget(self.tab_tv)
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab_series_info = QtGui.QWidget()
        self.tab_series_info.setObjectName(_fromUtf8("tab_series_info"))
        self.tabWidget_2.addTab(self.tab_series_info, _fromUtf8(""))
        self.tab_series_artwork = QtGui.QWidget()
        self.tab_series_artwork.setObjectName(_fromUtf8("tab_series_artwork"))
        self.tabWidget_2.addTab(self.tab_series_artwork, _fromUtf8(""))
        self.tab_season_artwork = QtGui.QWidget()
        self.tab_season_artwork.setObjectName(_fromUtf8("tab_season_artwork"))
        self.tabWidget_2.addTab(self.tab_season_artwork, _fromUtf8(""))
        self.tab_episode_info = QtGui.QWidget()
        self.tab_episode_info.setObjectName(_fromUtf8("tab_episode_info"))
        self.tabWidget_2.addTab(self.tab_episode_info, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget_2)
        self.columnView_season_episode = QtGui.QColumnView(self.tab_tv)
        self.columnView_season_episode.setMaximumSize(QtCore.QSize(16777215, 400))
        self.columnView_season_episode.setObjectName(_fromUtf8("columnView_season_episode"))
        self.verticalLayout.addWidget(self.columnView_season_episode)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_tv, _fromUtf8(""))
        self.tab_movies = QtGui.QWidget()
        self.tab_movies.setObjectName(_fromUtf8("tab_movies"))
        self.tabWidget.addTab(self.tab_movies, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1143, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionScan_Files = QtGui.QAction(MainWindow)
        self.actionScan_Files.setObjectName(_fromUtf8("actionScan_Files"))
        self.actionEdit_Preferences = QtGui.QAction(MainWindow)
        self.actionEdit_Preferences.setObjectName(_fromUtf8("actionEdit_Preferences"))
        self.actionClear_Cache = QtGui.QAction(MainWindow)
        self.actionClear_Cache.setObjectName(_fromUtf8("actionClear_Cache"))
        self.menuTools.addAction(self.actionScan_Files)
        self.menuTools.addAction(self.actionEdit_Preferences)
        self.menuTools.addAction(self.actionClear_Cache)
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_series_info), QtGui.QApplication.translate("MainWindow", "Series Info", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_series_artwork), QtGui.QApplication.translate("MainWindow", "Series Artwork", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_season_artwork), QtGui.QApplication.translate("MainWindow", "Season Artwork", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_episode_info), QtGui.QApplication.translate("MainWindow", "Episode Info", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tv), QtGui.QApplication.translate("MainWindow", "TV Shows", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_movies), QtGui.QApplication.translate("MainWindow", "Movies", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionScan_Files.setText(QtGui.QApplication.translate("MainWindow", "Scan Files", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_Preferences.setText(QtGui.QApplication.translate("MainWindow", "Edit Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear_Cache.setText(QtGui.QApplication.translate("MainWindow", "Clear Cache", None, QtGui.QApplication.UnicodeUTF8))

