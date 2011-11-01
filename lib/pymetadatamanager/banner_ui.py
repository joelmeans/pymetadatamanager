# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'banner.ui'
#
# Created: Tue Nov  1 13:26:19 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_BannerDialog(object):
    def setupUi(self, BannerDialog):
        BannerDialog.setObjectName("BannerDialog")
        BannerDialog.resize(1000, 1000)
        self.verticalLayout = QtGui.QVBoxLayout(BannerDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtGui.QTableView(BannerDialog)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.buttonBox = QtGui.QDialogButtonBox(BannerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(BannerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), BannerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), BannerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(BannerDialog)

    def retranslateUi(self, BannerDialog):
        BannerDialog.setWindowTitle(QtGui.QApplication.translate("BannerDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

