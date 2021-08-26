# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter options for a submodule update command.
"""

from PyQt5.QtWidgets import QDialog

from .Ui_GitSubmodulesUpdateOptionsDialog import (
    Ui_GitSubmodulesUpdateOptionsDialog
)


class GitSubmodulesUpdateOptionsDialog(QDialog,
                                       Ui_GitSubmodulesUpdateOptionsDialog):
    """
    Class implementing a dialog to enter options for a submodule update
    command.
    """
    def __init__(self, submodulePaths, parent=None):
        """
        Constructor
        
        @param submodulePaths list of submodule paths
        @type list of str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GitSubmodulesUpdateOptionsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.submodulesList.addItems(sorted(submodulePaths))
    
    def getData(self):
        """
        Public method to get the entered data.
        
        @return tuple containing the update procedure, a flag indicating an
            init, a flag indicating an update with remote, a flag indicating
            not to fetch the remote, a flag indicating an enforced operation
            and a list of selected submodules.
        @rtype tuple of (int, bool, bool, bool, bool, list of str)
        """
        submodulePaths = []
        for itm in self.submodulesList.selectedItems():
            submodulePaths.append(itm.text())
        
        if self.checkoutButton.isChecked():
            procedure = "--checkout"
        elif self.rebaseButton.isChecked():
            procedure = "--rebase"
        else:
            procedure = "--merge"
        
        if self.remoteCheckBox.isChecked():
            nofetch = self.nofetchCheckBox.isChecked()
        else:
            nofetch = False
        
        return (
            procedure,
            self.initCheckBox.isChecked(),
            self.remoteCheckBox.isChecked(),
            nofetch,
            self.forceCheckBox.isChecked(),
            submodulePaths,
        )
