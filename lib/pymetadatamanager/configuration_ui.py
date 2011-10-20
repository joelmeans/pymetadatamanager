# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created: Thu Oct 20 16:45:10 2011
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
        ConfigDialog.resize(408, 277)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_3 = QtGui.QLabel(ConfigDialog)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 379, 82))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.widget = QtGui.QWidget(ConfigDialog)
        self.widget.setGeometry(QtCore.QRect(10, 69, 391, 91))
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
        self.lineEdit_movie_dirs = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_movie_dirs.sizePolicy().hasHeightForWidth())
        self.lineEdit_movie_dirs.setSizePolicy(sizePolicy)
        self.lineEdit_movie_dirs.setObjectName(_fromUtf8("lineEdit_movie_dirs"))
        self.verticalLayout.addWidget(self.lineEdit_movie_dirs)
        self.lineEdit_tv_dirs = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_tv_dirs.sizePolicy().hasHeightForWidth())
        self.lineEdit_tv_dirs.setSizePolicy(sizePolicy)
        self.lineEdit_tv_dirs.setObjectName(_fromUtf8("lineEdit_tv_dirs"))
        self.verticalLayout.addWidget(self.lineEdit_tv_dirs)
        self.lineEdit_mediainfo_location = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_mediainfo_location.sizePolicy().hasHeightForWidth())
        self.lineEdit_mediainfo_location.setSizePolicy(sizePolicy)
        self.lineEdit_mediainfo_location.setObjectName(_fromUtf8("lineEdit_mediainfo_location"))
        self.verticalLayout.addWidget(self.lineEdit_mediainfo_location)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        ConfigDialog.setWindowTitle(QtGui.QApplication.translate("ConfigDialog", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ConfigDialog", "Enter comma-separated lists of video direcories:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConfigDialog", "TV Directories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConfigDialog", "Movie Directories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ConfigDialog", "MediaInfo Location", None, QtGui.QApplication.UnicodeUTF8))

