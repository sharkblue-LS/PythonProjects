# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select from a list.
"""

from PyQt5.QtWidgets import QDialog

from .Ui_GitListDialog import Ui_GitListDialog


class GitListDialog(QDialog, Ui_GitListDialog):
    """
    Class implementing a dialog to select from a list.
    """
    def __init__(self, selections, parent=None):
        """
        Constructor
        
        @param selections list of entries to select from (list of string)
        @param parent reference to the parent widget (QWidget)
        """
        super(GitListDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.selectionList.addItems(selections)
    
    def getSelection(self):
        """
        Public method to return the selected entries.
        
        @return list of selected entries (list of string)
        """
        selection = []
        for itm in self.selectionList.selectedItems():
            selection.append(itm.text())
        
        return selection
