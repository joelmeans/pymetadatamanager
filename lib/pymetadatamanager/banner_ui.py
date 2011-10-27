# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'banner.ui'
#
# Created: Thu Oct 27 13:14:25 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_BannerDialog(object):
    def setupUi(self, BannerDialog):
        BannerDialog.setObjectName(_fromUtf8("BannerDialog"))
        BannerDialog.resize(1438, 1232)
        self.verticalLayout = QtGui.QVBoxLayout(BannerDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(BannerDialog)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.buttonBox = QtGui.QDialogButtonBox(BannerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(BannerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), BannerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), BannerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BannerDialog)

    def retranslateUi(self, BannerDialog):
        BannerDialog.setWindowTitle(QtGui.QApplication.translate("BannerDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

