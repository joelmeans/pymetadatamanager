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
__date__ ="$Jan 19, 2010 12:02:05 PM$"

import logging
from PyQt4 import QtCore

module_logger = logging.getLogger('pymetadatamanager.models')

class ShowNode(object):
    """A node for information about a show"""
    def __init__(self, name, parent=None):
        self.logger = logging.getLogger('pymetadatamanager.models.ShowNode')
        self.name = QtCore.QString(name)
        self.parent = parent
        self.children = []
        self.setParent(parent)

    def setParent(self, parent):
        if parent != None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
        if len(self.children) > row:
            return self.children[row]
        return None

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def removeChild(self, row):
        value = self.children[row]
        self.children.remove(value)
        return True

    def __len__(self):
        return len(self.children)

class SeasonNode(object):
    """A node for information about a season"""
    def __init__(self, season_num, parent=None):
        self.logger = logging.getLogger('pymetadatamanager.models.SeasonNode')
        if str(season_num) == '0':
            self.name = QtCore.QString("Specials")
        else:
            self.name = QtCore.QString(season_num)
        self.parent = parent
        self.children = []
        self.setParent(parent)

    def setParent(self, parent):
        if parent != None:
            self.parent = parent
            self.parent.appendChild(self)
        else:
            self.parent = None

    def appendChild(self, child):
        self.children.append(child)

    def childAtRow(self, row):
        if len(self.children) > row:
            return self.children[row]
        return None

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item == child:
                return i
        return -1

    def removeChild(self, row):
        value = self.children[row]
        self.children.remove(value)
        return True

    def __len__(self):
        return len(self.children)

class ShowListModel(QtCore.QAbstractListModel): 
    def __init__(self, list, parent=None): 
        """Create a list model from the input list"""
        super(ShowListModel, self).__init__(parent) 
        self.logger = logging.getLogger('pymetadatamanager.models.ShowListModel')
        self.listdata = list
 
    def rowCount(self, parent): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.listdata[index.row()])
        else: 
            return QtCore.QVariant()

class SeasonListModel(QtCore.QAbstractListModel): 
    def __init__(self, list, parent=None): 
        """Create a list model from the input list"""
        super(SeasonListModel, self).__init__(parent) 
        self.logger = logging.getLogger('pymetadatamanager.models.SeasonListModel')
        self.listdata = list
 
    def rowCount(self, parent): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant("%s - %s" % (self.listdata[index.row()][0], \
                                                self.listdata[index.row()][1]))
        else: 
            return QtCore.QVariant()

class SeasonEpisodeModel(QtCore.QAbstractItemModel):
    """Create a model of shows from a DomDocument containing show information"""
    def __init__(self, document, parent=None):
        super(SeasonEpisodeModel, self).__init__(parent)
        self.logger = logging.getLogger('pymetadatamanager.models.SeasonEpisodeModel')
        self.treeView = parent
        self.headers = ['Season','Episode']
        self.columns = 3
        self.domDocument = document
        self.rootItem = ShowNode('season', None)
      # Create items
        root = self.domDocument.firstChildElement('show')
        season_elem = root.firstChildElement('season')
        while not season_elem.isNull():
            seasonItem = SeasonNode(season_elem.attribute('number'), \
                                  self.rootItem)
            episode_elem = season_elem.firstChildElement('episode')
            while not episode_elem.isNull():
                episodeItem = \
                 ShowNode("%s - %s" % (episode_elem.attribute('number'), \
                                       episode_elem.text()), seasonItem)
                episode_elem = episode_elem.nextSiblingElement('episode')
            season_elem = season_elem.nextSiblingElement('season')

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def data(self, index, role):
        if role == QtCore.Qt.DecorationRole:
            return QtCore.QVariant()
        if role == QtCore.Qt.TextAlignmentRole:
            return \
              QtCore.QVariant(int(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft))
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        node = self.nodeFromIndex(index)
        if index.column() == 0:
            try:
                return QtCore.QVariant(node.name)
            except AttributeError:
                return QtCore.QVariant()
        else:
            return QtCore.QVariant()

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, child):
        if not child.isValid():
            return QtCore.QModelIndex()

        node = self.nodeFromIndex(child)
        if node is None:
            return QtCore.QModelIndex()

        parent = node.parent
        if parent is None:
            return QtCore.QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QtCore.QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != - 1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.rootItem

class ShowModel(QtCore.QAbstractItemModel):
    """Create a model of shows from a DomDocument containing show information"""
    def __init__(self, document, parent=None):
        super(ShowModel, self).__init__(parent)
        self.logger = logging.getLogger('pymetadatamanager.models.ShowModel')
        self.treeView = parent
        self.headers = ['Series', 'Season','Episode']
        self.columns = 4
        self.domDocument = document
        self.rootItem = ShowNode('root', None)
      # Create items
        show_elem = self.domDocument.firstChildElement('shows')
        series_elem = show_elem.firstChildElement('series')
        while not series_elem.isNull():
            seriesItem = ShowNode(series_elem.attribute('name'), self.rootItem)
            season_elem = series_elem.firstChildElement('season')
            while not season_elem.isNull():
                seasonItem = \
                 ShowNode(season_elem.attribute('number'), seriesItem)
                episode_elem = season_elem.firstChildElement('episode')
                while not episode_elem.isNull():
                    episodeItem = ShowNode(episode_elem.text(), seasonItem)
                    episode_elem = episode_elem.nextSiblingElement('episode')
                season_elem = season_elem.nextSiblingElement('season')
            series_elem = series_elem.nextSiblingElement('series')

    def insertRow(self, row, parent):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, (row + (count - 1)))
        self.endInsertRows()
        return True

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, row, count, parentIndex):
        self.beginRemoveRows(parentIndex, row, row)
        node = self.nodeFromIndex(parentIndex)
        node.removeChild(row)
        self.endRemoveRows()
        return True

    def index(self, row, column, parent):
        node = self.nodeFromIndex(parent)
        return self.createIndex(row, column, node.childAtRow(row))

    def data(self, index, role):
        if role == QtCore.Qt.DecorationRole:
            return QtCore.QVariant()
        if role == QtCore.Qt.TextAlignmentRole:
            return \
              QtCore.QVariant(int(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft))
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        node = self.nodeFromIndex(index)
        if index.column() == 0:
            try:
                return QtCore.QVariant(node.name)
            except AttributeError:
                return QtCore.QVariant()
        else:
            return QtCore.QVariant()

    def columnCount(self, parent):
        return self.columns

    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None:
            return 0
        return len(node)

    def parent(self, child):
        if not child.isValid():
            return QtCore.QModelIndex()

        node = self.nodeFromIndex(child)
        if node is None:
            return QtCore.QModelIndex()

        parent = node.parent
        if parent is None:
            return QtCore.QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QtCore.QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != - 1
        return self.createIndex(row, 0, parent)

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self.rootItem

class BannerModel(QtCore.QAbstractTableModel):
    """Create a table model of banners from a list of banner files"""
    def __init__(self, banners, parent=None):
        super(BannerModel, self).__init__(parent)
        self.logger = logging.getLogger('pymetadatamanager.models.BannerModel')
        banners_col_0 = []
        banners_col_1 = []
        banners_col_2 = []
        for banner in banners:
            if banners.index(banner) % 3 == 0:
                banners_col_0.append(banner)
            elif banners.index(banner) % 3 == 1:
                banners_col_1.append(banner)
            else:
                banners_col_2.append(banner)
        if not len(banners_col_0) == len(banners_col_1):
            banners_col_1.append('none')
        if not len(banners_col_0) == len(banners_col_2):
            banners_col_2.append('none')
        self.banners_table_list = [banners_col_0, banners_col_1, banners_col_2]
        self.list = self.transpose(self.banners_table_list)

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.UserRole:
            return self.list[index.row()][index.column()][1]
        elif role == QtCore.Qt.DecorationRole:
            return QtCore.QVariant(self.list[index.row()][index.column()][0])
        else:
            return QtCore.QVariant()

    def columnCount(self, parent):
        try:    
            return len(self.list[0])
        except IndexError:
            return 0

    def rowCount(self, parent):
        return len(self.list)

    def transpose(self, list):
        newlist = []
        for x in range(0, len(list[0])):
            newlist.append([list[0][x], list[1][x], list[2][x]])
        return newlist

class BannerWideModel(QtCore.QAbstractTableModel):
    """Create a table model of banners from a list of banner files"""
    def __init__(self, banners, parent=None):
        super(BannerWideModel, self).__init__(parent)
        self.logger = logging.getLogger('pymetadatamanager.models.BannerWideModel')
        self.list = banners

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.UserRole:
            return self.list[index.row()][1]
        elif role == QtCore.Qt.DecorationRole:
            return QtCore.QVariant(self.list[index.row()][0])
        else:
            return QtCore.QVariant()

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        return len(self.list)

class EmptyTableModel(QtCore.QAbstractTableModel):
    """Create an empty table model to clear a display"""
    def __init__(self, parent=None):
        super(EmptyTableModel, self).__init__(parent)
        self.logger = logging.getLogger('pymetadatamanager.models.EmptyTableModel')

    def data(self, index, role):
        return QtCore.QVariant()

    def columnCount(self, parent):
        return 0

    def rowCount(self, parent):
        return 0

class EmptyListModel(QtCore.QAbstractListModel):
    """Create an empty list model to clear a display"""
    def __init__(self, parent=None):
        super(EmptyListModel, self).__init__(parent)
        self.logger = logging.getLogger('pymetadatamanager.models.EmptyListModel')

    def data(self, index, role):
        return QtCore.QVariant()

    def rowCount(self, parent):
        return 0
