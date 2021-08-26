# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select the data for pushing a branch.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_GitBranchPushDialog import Ui_GitBranchPushDialog


class GitBranchPushDialog(QDialog, Ui_GitBranchPushDialog):
    """
    Class implementing a dialog to select the data for pushing a branch.
    """
    def __init__(self, branches, remotes, delete=False, parent=None):
        """
        Constructor
        
        @param branches list of branch names (list of string)
        @param remotes list of remote names (list of string)
        @param delete flag indicating a delete branch action (boolean)
        @param parent reference to the parent widget (QWidget)
        """
        super(GitBranchPushDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__okButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok)
        
        self.__allBranches = self.tr("<all branches>")
        
        if "origin" in remotes:
            self.remoteComboBox.addItem("origin")
            remotes.remove("origin")
        self.remoteComboBox.addItems(sorted(remotes))
        
        if delete:
            self.branchComboBox.addItem("")
        else:
            self.branchComboBox.addItem(self.__allBranches)
        if "master" in branches:
            if not delete:
                self.branchComboBox.addItem("master")
            branches.remove("master")
        self.branchComboBox.addItems(sorted(branches))
        
        if delete:
            self.__okButton.setEnabled(False)
            self.branchComboBox.setEditable(True)
    
    @pyqtSlot(str)
    def on_branchComboBox_editTextChanged(self, txt):
        """
        Private slot to handle a change of the branch name.
        
        @param txt branch name (string)
        """
        self.__okButton.setEnabled(bool(txt))
    
    def getData(self):
        """
        Public method to get the selected data.
        
        @return tuple of selected branch name, remote name and a flag
            indicating all branches (tuple of two strings and a boolean)
        """
        return (self.branchComboBox.currentText(),
                self.remoteComboBox.currentText(),
                self.branchComboBox.currentText() == self.__allBranches)
