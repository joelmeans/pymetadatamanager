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

import os.path
import logging
from configuration import Config
from configuration_ui import Ui_ConfigDialog
from PyQt4 import QtGui

class ConfigDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        """Initializes the Dialog"""
        self.logger = logging.getLogger('pymetadatamanager.configuration_dialog')
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)

        self.config = Config()
        self.ui.lineEdit_tv_dirs.setText(",".join(self.config.tv_dirs))
        self.ui.lineEdit_movie_dirs.setText(",".join(self.config.movie_dirs))
        self.ui.lineEdit_mediainfo_path.setText(self.config.mediainfo_path)
        self.ui.pushButton_tv_browse.clicked.connect(self.tv_browser)
        self.ui.pushButton_movie_browse.clicked.connect(self.movie_browser)
        self.ui.pushButton_mediainfo_browse.clicked.connect(self.mediainfo_browser)
        self.ui.buttonBox.accepted.connect(self.save_values)

    def tv_browser(self):
        old_filename = self.ui.lineEdit_tv_dirs.text()
        filename = QtGui.QFileDialog.getExistingDirectory(self, "TV Directory", \
                                                          old_filename)
        if not filename == '':
            self.ui.lineEdit_tv_dirs.setText(filename)
        else:
            self.ui.lineEdit_tv_dirs.setText(old_filename)

    def movie_browser(self):
        old_filename = self.ui.lineEdit_movie_dirs.text()
        filename = QtGui.QFileDialog.getExistingDirectory(self, "Movie Directory", \
                                                          old_filename)
        if not filename == '':
            self.ui.lineEdit_movie_dirs.setText(filename)
        else:
            self.ui.lineEdit_movie_dirs.setText(old_filename)

    def mediainfo_browser(self):
        old_path = self.ui.lineEdit_mediainfo_path.text()
        path = QtGui.QFileDialog.getOpenFileName(self, \
                                             "MediaInfo Path", \
                                             os.path.expanduser("~"))
        if not path == '':
            self.ui.lineEdit_mediainfo_path.setText(path)
        else:
            self.ui.lineEdit_mediainfo_path.setText(old_path)

    def save_values(self):
        del self.config.tv_dirs[:]
        for dir in str(self.ui.lineEdit_tv_dirs.text()).split(","):
            self.config.tv_dirs.append(dir)
        del self.config.movie_dirs[:]
        for dir in str(self.ui.lineEdit_movie_dirs.text()).split(","):
            self.config.movie_dirs.append(dir)
        self.config.mediainfo_path = self.ui.lineEdit_mediainfo_path.text()
        self.config.write_config_file()
        self.config.read_config_file()
