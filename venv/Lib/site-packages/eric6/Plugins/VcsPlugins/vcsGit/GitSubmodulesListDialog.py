# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to list the defined submodules.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QHeaderView

from .Ui_GitSubmodulesListDialog import Ui_GitSubmodulesListDialog


class GitSubmodulesListDialog(QDialog, Ui_GitSubmodulesListDialog):
    """
    Class implementing a dialog to list the defined submodules.
    """
    def __init__(self, submodules, parent=None):
        """
        Constructor
        
        @param submodules list of submodule data to be shown
        @type list of dictionaries with submodule name, path, URL and branch
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GitSubmodulesListDialog, self).__init__(parent)
        self.setupUi(self)
        
        for submodule in submodules:
            QTreeWidgetItem(self.submodulesList, [
                submodule["name"],
                submodule["path"],
                submodule["url"],
                submodule["branch"]
            ])
        self.submodulesList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.submodulesList.header().setStretchLastSection(True)
        
        self.submodulesList.setSortingEnabled(True)
        self.submodulesList.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.submodulesList.setSortingEnabled(False)
