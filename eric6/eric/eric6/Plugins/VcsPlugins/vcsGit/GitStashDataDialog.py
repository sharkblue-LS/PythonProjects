# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a stash operation.
"""

from PyQt5.QtWidgets import QDialog

from .Ui_GitStashDataDialog import Ui_GitStashDataDialog


class GitStashDataDialog(QDialog, Ui_GitStashDataDialog):
    """
    Class implementing a dialog to enter the data for a stash operation.
    """
    NoUntracked = 0
    UntrackedOnly = 1
    UntrackedAndIgnored = 2
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(GitStashDataDialog, self).__init__(parent)
        self.setupUi(self)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def getData(self):
        """
        Public method to get the user data.
        
        @return tuple containing the message (string), a flag indicating to
            keep changes in the staging area (boolean) and an indication to
            stash untracked and/or ignored files (integer)
        """
        if self.noneRadioButton.isChecked():
            untracked = self.NoUntracked
        elif self.untrackedRadioButton.isChecked():
            untracked = self.UntrackedOnly
        else:
            untracked = self.UntrackedAndIgnored
        
        return (self.messageEdit.text(), self.keepCheckBox.isChecked(),
                untracked)
