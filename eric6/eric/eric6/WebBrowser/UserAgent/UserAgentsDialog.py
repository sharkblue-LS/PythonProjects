# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show all saved user agent settings.
"""

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QDialog

from WebBrowser.WebBrowserWindow import WebBrowserWindow

from .UserAgentModel import UserAgentModel

from .Ui_UserAgentsDialog import Ui_UserAgentsDialog


class UserAgentsDialog(QDialog, Ui_UserAgentsDialog):
    """
    Class implementing a dialog to show all saved user agent settings.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(UserAgentsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.removeButton.clicked.connect(
            self.userAgentsTable.removeSelected)
        self.removeAllButton.clicked.connect(
            self.userAgentsTable.removeAll)
        
        self.userAgentsTable.verticalHeader().hide()
        self.__userAgentModel = UserAgentModel(
            WebBrowserWindow.userAgentsManager(), self)
        self.__proxyModel = QSortFilterProxyModel(self)
        self.__proxyModel.setSourceModel(self.__userAgentModel)
        self.searchEdit.textChanged.connect(
            self.__proxyModel.setFilterFixedString)
        self.userAgentsTable.setModel(self.__proxyModel)
        
        fm = QFontMetrics(QFont())
        height = fm.height() + fm.height() // 3
        self.userAgentsTable.verticalHeader().setDefaultSectionSize(height)
        self.userAgentsTable.verticalHeader().setMinimumSectionSize(-1)
        
        self.userAgentsTable.resizeColumnsToContents()
        self.userAgentsTable.horizontalHeader().setStretchLastSection(True)
