# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a model for search engines.
"""

import re

from PyQt5.QtCore import Qt, QUrl, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QPixmap, QIcon


class OpenSearchEngineModel(QAbstractTableModel):
    """
    Class implementing a model for search engines.
    """
    def __init__(self, manager, parent=None):
        """
        Constructor
        
        @param manager reference to the search engine manager
            (OpenSearchManager)
        @param parent reference to the parent object (QObject)
        """
        super(OpenSearchEngineModel, self).__init__(parent)
        
        self.__manager = manager
        manager.changed.connect(self.__enginesChanged)
        
        self.__headers = [
            self.tr("Name"),
            self.tr("Keywords"),
        ]
    
    def removeRows(self, row, count, parent=None):
        """
        Public method to remove entries from the model.
        
        @param row start row (integer)
        @param count number of rows to remove (integer)
        @param parent parent index (QModelIndex)
        @return flag indicating success (boolean)
        """
        if parent is None:
            parent = QModelIndex()
        
        if parent.isValid():
            return False
        
        if count <= 0:
            return False
        
        if self.rowCount() <= 1:
            return False
        
        lastRow = row + count - 1
        
        self.beginRemoveRows(parent, row, lastRow)
        
        nameList = self.__manager.allEnginesNames()
        for index in range(row, lastRow + 1):
            self.__manager.removeEngine(nameList[index])
        
        return True
    
    def rowCount(self, parent=None):
        """
        Public method to get the number of rows of the model.
        
        @param parent parent index (QModelIndex)
        @return number of rows (integer)
        """
        if parent is None:
            parent = QModelIndex()
        
        if parent.isValid():
            return 0
        else:
            return self.__manager.enginesCount()
    
    def columnCount(self, parent=None):
        """
        Public method to get the number of columns of the model.
        
        @param parent parent index (QModelIndex) (Unused)
        @return number of columns (integer)
        """
        return 2
    
    def flags(self, index):
        """
        Public method to get flags for a model cell.
        
        @param index index of the model cell (QModelIndex)
        @return flags (Qt.ItemFlags)
        """
        if index.column() == 1:
            return (
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEditable
            )
        else:
            return (
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsSelectable
            )
    
    def data(self, index, role):
        """
        Public method to get data from the model.
        
        @param index index to get data for (QModelIndex)
        @param role role of the data to retrieve (integer)
        @return requested data
        """
        if index.row() >= self.__manager.enginesCount() or index.row() < 0:
            return None
        
        engine = self.__manager.engine(
            self.__manager.allEnginesNames()[index.row()])
        
        if engine is None:
            return None
        
        if index.column() == 0:
            if role == Qt.ItemDataRole.DisplayRole:
                return engine.name()
                
            elif role == Qt.ItemDataRole.DecorationRole:
                image = engine.image()
                if image.isNull():
                    from WebBrowser.WebBrowserWindow import WebBrowserWindow
                    icon = WebBrowserWindow.icon(QUrl(engine.imageUrl()))
                else:
                    icon = QIcon(QPixmap.fromImage(image))
                return icon
                
            elif role == Qt.ItemDataRole.ToolTipRole:
                description = self.tr(
                    "<strong>Description:</strong> {0}"
                ).format(engine.description())
                if engine.providesSuggestions():
                    description += "<br/>"
                    description += self.tr(
                        "<strong>Provides contextual suggestions</strong>")
                
                return description
        elif index.column() == 1:
            if role in [Qt.ItemDataRole.EditRole, Qt.ItemDataRole.DisplayRole]:
                return ",".join(self.__manager.keywordsForEngine(engine))
            elif role == Qt.ItemDataRole.ToolTipRole:
                return self.tr(
                    "Comma-separated list of keywords that may"
                    " be entered in the location bar followed by search terms"
                    " to search with this engine")
        
        return None
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        """
        Public method to set the data of a model cell.
        
        @param index index of the model cell (QModelIndex)
        @param value value to be set
        @param role role of the data (integer)
        @return flag indicating success (boolean)
        """
        if not index.isValid() or index.column() != 1:
            return False
        
        if index.row() >= self.rowCount() or index.row() < 0:
            return False
        
        if role != Qt.ItemDataRole.EditRole:
            return False
        
        engineName = self.__manager.allEnginesNames()[index.row()]
        keywords = re.split("[ ,]+", value)
        self.__manager.setKeywordsForEngine(
            self.__manager.engine(engineName), keywords)
        
        return True
    
    def headerData(self, section, orientation,
                   role=Qt.ItemDataRole.DisplayRole):
        """
        Public method to get the header data.
        
        @param section section number (integer)
        @param orientation header orientation (Qt.Orientation)
        @param role data role (Qt.ItemDataRole)
        @return header data
        """
        if (
            orientation == Qt.Orientation.Horizontal and
            role == Qt.ItemDataRole.DisplayRole
        ):
            try:
                return self.__headers[section]
            except IndexError:
                pass
        
        return None
    
    def __enginesChanged(self):
        """
        Private slot handling a change of the registered engines.
        """
        self.beginResetModel()
        self.endResetModel()
