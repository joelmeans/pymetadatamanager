# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created: Tue Oct 25 09:25:11 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName(_fromUtf8("ConfigDialog"))
        ConfigDialog.resize(554, 240)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigDialog)
        self.buttonBox.setGeometry(QtCore.QRect(200, 190, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_3 = QtGui.QLabel(ConfigDialog)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 379, 82))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.widget = QtGui.QWidget(ConfigDialog)
        self.widget.setGeometry(QtCore.QRect(10, 70, 531, 102))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit_tv_dirs = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_tv_dirs.sizePolicy().hasHeightForWidth())
        self.lineEdit_tv_dirs.setSizePolicy(sizePolicy)
        self.lineEdit_tv_dirs.setObjectName(_fromUtf8("lineEdit_tv_dirs"))
        self.verticalLayout.addWidget(self.lineEdit_tv_dirs)
        self.lineEdit_movie_dirs = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_movie_dirs.sizePolicy().hasHeightForWidth())
        self.lineEdit_movie_dirs.setSizePolicy(sizePolicy)
        self.lineEdit_movie_dirs.setObjectName(_fromUtf8("lineEdit_movie_dirs"))
        self.verticalLayout.addWidget(self.lineEdit_movie_dirs)
        self.lineEdit_mediainfo_path = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_mediainfo_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_mediainfo_path.setSizePolicy(sizePolicy)
        self.lineEdit_mediainfo_path.setObjectName(_fromUtf8("lineEdit_mediainfo_path"))
        self.verticalLayout.addWidget(self.lineEdit_mediainfo_path)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.pushButton_tv_browse = QtGui.QPushButton(self.widget)
        self.pushButton_tv_browse.setObjectName(_fromUtf8("pushButton_tv_browse"))
        self.verticalLayout_3.addWidget(self.pushButton_tv_browse)
        self.pushButton_movie_browse = QtGui.QPushButton(self.widget)
        self.pushButton_movie_browse.setObjectName(_fromUtf8("pushButton_movie_browse"))
        self.verticalLayout_3.addWidget(self.pushButton_movie_browse)
        self.pushButton_mediainfo_browse = QtGui.QPushButton(self.widget)
        self.pushButton_mediainfo_browse.setObjectName(_fromUtf8("pushButton_mediainfo_browse"))
        self.verticalLayout_3.addWidget(self.pushButton_mediainfo_browse)
        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(ConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QtGui.QApplication.translate("ConfigDialog", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ConfigDialog", "Enter comma-separated lists of video direcories:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConfigDialog", "TV Directories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConfigDialog", "Movie Directories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ConfigDialog", "MediaInfo Path", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_tv_browse.setText(QtGui.QApplication.translate("ConfigDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_movie_browse.setText(QtGui.QApplication.translate("ConfigDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_mediainfo_browse.setText(QtGui.QApplication.translate("ConfigDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))

