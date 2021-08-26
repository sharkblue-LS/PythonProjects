# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Watch expression model.
"""

import copy

from PyQt5.QtCore import pyqtSignal, Qt, QAbstractItemModel, QModelIndex


class WatchPointModel(QAbstractItemModel):
    """
    Class implementing a custom model for watch expressions.
    
    @signal dataAboutToBeChanged(QModelIndex, QModelIndex) emitted to indicate
        a change of the data
    """
    dataAboutToBeChanged = pyqtSignal(QModelIndex, QModelIndex)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QObject)
        """
        super(WatchPointModel, self).__init__(parent)
        
        self.watchpoints = []
        self.header = [
            self.tr("Condition"),
            self.tr("Special"),
            self.tr('Temporary'),
            self.tr('Enabled'),
            self.tr('Ignore Count'),
        ]
        self.alignments = [Qt.Alignment(Qt.AlignmentFlag.AlignLeft),
                           Qt.Alignment(Qt.AlignmentFlag.AlignLeft),
                           Qt.Alignment(Qt.AlignmentFlag.AlignHCenter),
                           Qt.Alignment(Qt.AlignmentFlag.AlignHCenter),
                           Qt.Alignment(Qt.AlignmentFlag.AlignRight),
                           ]
        
    def columnCount(self, parent=None):
        """
        Public method to get the current column count.
        
        @param parent index of the parent item (QModelIndex) (Unused)
        @return column count (integer)
        """
        return len(self.header)
    
    def rowCount(self, parent=None):
        """
        Public method to get the current row count.
        
        @param parent index of the parent item (QModelIndex)
        @return row count (integer)
        """
        # we do not have a tree, parent should always be invalid
        if parent is None or not parent.isValid():
            return len(self.watchpoints)
        else:
            return 0
    
    def data(self, index, role):
        """
        Public method to get the requested data.
        
        @param index index of the requested data (QModelIndex)
        @param role role of the requested data (Qt.ItemDataRole)
        @return the requested data
        """
        if not index.isValid():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() in [0, 1, 4]:
                return self.watchpoints[index.row()][index.column()]
        
        if role == Qt.ItemDataRole.CheckStateRole:
            if index.column() in [2, 3]:
                return self.watchpoints[index.row()][index.column()]
        
        if role == Qt.ItemDataRole.ToolTipRole:
            if index.column() in [0, 1]:
                return self.watchpoints[index.row()][index.column()]
        
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() < len(self.alignments):
                return self.alignments[index.column()]
        
        return None
    
    def flags(self, index):
        """
        Public method to get item flags.
        
        @param index index of the requested flags (QModelIndex)
        @return item flags for the given index (Qt.ItemFlags)
        """
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
    
    def headerData(self, section, orientation,
                   role=Qt.ItemDataRole.DisplayRole):
        """
        Public method to get header data.
        
        @param section section number of the requested header data (integer)
        @param orientation orientation of the header (Qt.Orientation)
        @param role role of the requested data (Qt.ItemDataRole)
        @return header data
        """
        if (
            orientation == Qt.Orientation.Horizontal and
            role == Qt.ItemDataRole.DisplayRole
        ):
            if section >= len(self.header):
                return ""
            else:
                return self.header[section]
        
        return None
    
    def index(self, row, column, parent=None):
        """
        Public method to create an index.
        
        @param row row number for the index (integer)
        @param column column number for the index (integer)
        @param parent index of the parent item (QModelIndex)
        @return requested index (QModelIndex)
        """
        if (
            (parent and parent.isValid()) or
            row < 0 or
            row >= len(self.watchpoints) or
            column < 0 or
            column >= len(self.header)
        ):
            return QModelIndex()
        
        return self.createIndex(row, column, self.watchpoints[row])

    def parent(self, index):
        """
        Public method to get the parent index.
        
        @param index index of item to get parent (QModelIndex)
        @return index of parent (QModelIndex)
        """
        return QModelIndex()
    
    def hasChildren(self, parent=None):
        """
        Public method to check for the presence of child items.
        
        @param parent index of parent item (QModelIndex)
        @return flag indicating the presence of child items (boolean)
        """
        if parent is None or not parent.isValid():
            return len(self.watchpoints) > 0
        else:
            return False
    
    ###########################################################################
    
    def addWatchPoint(self, cond, special, properties):
        """
        Public method to add a new watch expression to the list.
        
        @param cond expression of the watch expression
        @type str
        @param special special condition of the watch expression
        @type str
        @param properties properties of the watch expression
            (tuple of temporary flag, enabled flag, ignore count)
        @type tuple of (bool, bool, int)
        """
        wp = [cond, special] + list(properties)
        cnt = len(self.watchpoints)
        self.beginInsertRows(QModelIndex(), cnt, cnt)
        self.watchpoints.append(wp)
        self.endInsertRows()
    
    def addWatchPoints(self, watchpoints):
        """
        Public method to add multiple watch expressions to the list.
        
        @param watchpoints list of watch expressions with expression, special
            condition, temporary flag, enabled flag and ignore count each
        @type list of (str, str, bool, bool, int)
        """
        cnt = len(self.watchpoints)
        self.beginInsertRows(QModelIndex(), cnt, cnt + len(watchpoints) - 1)
        self.watchpoints += watchpoints
        self.endInsertRows()
    
    def setWatchPointByIndex(self, index, cond, special, properties):
        """
        Public method to set the values of a watch expression given by index.
        
        @param index index of the watch expression (QModelIndex)
        @param cond expression of the watch expression (string)
        @param special special condition of the watch expression (string)
        @param properties properties of the watch expression
            (tuple of temporary flag (bool), enabled flag (bool),
            ignore count (integer))
        """
        if index.isValid():
            row = index.row()
            index1 = self.createIndex(row, 0, self.watchpoints[row])
            index2 = self.createIndex(
                row, len(self.watchpoints[row]), self.watchpoints[row])
            self.dataAboutToBeChanged.emit(index1, index2)
            self.watchpoints[row] = [cond, special] + list(properties)
            self.dataChanged.emit(index1, index2)

    def setWatchPointEnabledByIndex(self, index, enabled):
        """
        Public method to set the enabled state of a watch expression given by
        index.
        
        @param index index of the watch expression (QModelIndex)
        @param enabled flag giving the enabled state (boolean)
        """
        if index.isValid():
            row = index.row()
            col = 3
            index1 = self.createIndex(row, col, self.watchpoints[row])
            self.dataAboutToBeChanged.emit(index1, index1)
            self.watchpoints[row][col] = enabled
            self.dataChanged.emit(index1, index1)
    
    def deleteWatchPointByIndex(self, index):
        """
        Public method to set the values of a watch expression given by index.
        
        @param index index of the watch expression (QModelIndex)
        """
        if index.isValid():
            row = index.row()
            self.beginRemoveRows(QModelIndex(), row, row)
            del self.watchpoints[row]
            self.endRemoveRows()

    def deleteWatchPoints(self, idxList):
        """
        Public method to delete a list of watch expressions given by their
        indexes.
        
        @param idxList list of watch expression indexes (list of QModelIndex)
        """
        rows = []
        for index in idxList:
            if index.isValid():
                rows.append(index.row())
        rows.sort(reverse=True)
        for row in rows:
            if row < len(self.breakpoints):
                self.beginRemoveRows(QModelIndex(), row, row)
                del self.watchpoints[row]
                self.endRemoveRows()

    def deleteAll(self):
        """
        Public method to delete all watch expressions.
        """
        if self.watchpoints:
            self.beginRemoveRows(QModelIndex(), 0, len(self.watchpoints) - 1)
            self.watchpoints = []
            self.endRemoveRows()

    def getWatchPointByIndex(self, index):
        """
        Public method to get the values of a watch expression given by index.
        
        @param index index of the watch expression (QModelIndex)
        @return watch expression (list of six values (expression,
            special condition, temporary flag, enabled flag, ignore count))
        @rtype tuple of (str, str, bool, bool, int)
        """
        if index.isValid():
            return self.watchpoints[index.row()][:]  # return a copy
        else:
            return []
    
    def getAllWatchpoints(self):
        """
        Public method to get the list of watchpoints.
        
        @return list of watchpoints
        @rtype list of list of [str, str, bool, bool, int]
        """
        return copy.deepcopy(self.watchpoints)
    
    def getWatchPointIndex(self, cond, special=""):
        """
        Public method to get the index of a watch expression given by
        expression.
        
        @param cond expression of the watch expression (string)
        @param special special condition of the watch expression (string)
        @return index (QModelIndex)
        """
        for row in range(len(self.watchpoints)):
            wp = self.watchpoints[row]
            if wp[0] == cond:
                if special and wp[1] != special:
                    continue
                return self.createIndex(row, 0, self.watchpoints[row])
        
        return QModelIndex()
