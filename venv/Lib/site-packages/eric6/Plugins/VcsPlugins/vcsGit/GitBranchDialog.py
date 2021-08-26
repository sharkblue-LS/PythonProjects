# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a branching operation.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_GitBranchDialog import Ui_GitBranchDialog


class GitBranchDialog(QDialog, Ui_GitBranchDialog):
    """
    Class implementing a dialog to enter the data for a branching operation.
    """
    CreateBranch = 1
    DeleteBranch = 2
    RenameBranch = 3
    CreateSwitchBranch = 4
    CreateTrackingBranch = 5
    SetTrackingBranch = 6
    UnsetTrackingBranch = 7
    
    def __init__(self, branchlist, revision=None, branchName=None,
                 branchOp=None, parent=None):
        """
        Constructor
        
        @param branchlist list of previously entered branches (list of strings)
        @param revision revision to set tag for (string)
        @param branchName name of the branch (string)
        @param branchOp desired branch operation (integer)
        @param parent parent widget (QWidget)
        """
        super(GitBranchDialog, self).__init__(parent)
        self.setupUi(self)
       
        self.okButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok)
        self.okButton.setEnabled(False)
        
        self.__remoteBranches = [b for b in branchlist
                                 if b.startswith("remotes/")]
        self.__lokalBranches = [b for b in branchlist
                                if not b.startswith("remotes/")]
        
        self.branchCombo.clear()
        self.branchCombo.addItem("")
        self.branchCombo.addItems(sorted(self.__lokalBranches))
        
        self.remoteBranchCombo.clear()
        self.remoteBranchCombo.addItems(sorted(self.__remoteBranches))
        
        if revision:
            self.revisionEdit.setText(revision)
        
        if branchName:
            index = self.branchCombo.findText(branchName)
            if index > -1:
                self.branchCombo.setCurrentIndex(index)
                # suggest the most relevant branch action
                self.deleteBranchButton.setChecked(True)
            else:
                self.branchCombo.setEditText(branchName)
                self.createBranchButton.setChecked(True)
        
        if branchOp:
            if branchOp == GitBranchDialog.CreateBranch:
                self.createBranchButton.setChecked(True)
            elif branchOp == GitBranchDialog.DeleteBranch:
                self.deleteBranchButton.setChecked(True)
            elif branchOp == GitBranchDialog.RenameBranch:
                self.moveBranchButton.setChecked(True)
            elif branchOp == GitBranchDialog.CreateSwitchBranch:
                self.createSwitchButton.setChecked(True)
            elif branchOp == GitBranchDialog.CreateTrackingBranch:
                self.createTrackingButton.setChecked(True)
            elif branchOp == GitBranchDialog.SetTrackingBranch:
                self.setTrackingButton.setChecked(True)
            elif branchOp == GitBranchDialog.UnsetTrackingBranch:
                self.unsetTrackingButton.setChecked(True)
            else:
                # Oops, fall back to a save default
                self.createBranchButton.setChecked(True)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateOK(self):
        """
        Private method used to enable/disable the OK-button.
        """
        if (
            self.setTrackingButton.isChecked() or
            self.unsetTrackingButton.isChecked()
        ):
            enable = True
        else:
            enable = self.branchCombo.currentText() != ""
            if self.moveBranchButton.isChecked():
                enable &= self.newBranchNameEdit.text() != ""
        
        self.okButton.setEnabled(enable)
    
    @pyqtSlot(bool)
    def on_createTrackingButton_toggled(self, checked):
        """
        Private slot to handle the selection of creating a tracking branch.
        
        @param checked state of the selection (boolean)
        """
        self.branchCombo.setEditable(not checked)
        self.branchCombo.clear()
        if checked:
            self.branchCombo.addItems(sorted(self.__remoteBranches))
        else:
            self.branchCombo.addItem("")
            self.branchCombo.addItems(sorted(self.__lokalBranches))
        self.__updateOK()
    
    @pyqtSlot(bool)
    def on_setTrackingButton_toggled(self, checked):
        """
        Private slot to handle the selection of setting a tracking branch.
        
        @param checked state of the selection (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(bool)
    def on_unsetTrackingButton_toggled(self, checked):
        """
        Private slot to handle the selection of unsetting a tracking branch.
        
        @param checked state of the selection (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_branchCombo_editTextChanged(self, text):
        """
        Private slot to handle a change of the branch.
        
        @param text branch name entered in the combo (string)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_newBranchNameEdit_textChanged(self, text):
        """
        Private slot to handle a change of the new branch.
        
        @param text new branch name entered (string)
        """
        self.__updateOK()
    
    def getParameters(self):
        """
        Public method to retrieve the branch data.
        
        @return tuple of an int, four strings and a boolean
            (branch operation, branch name, revision, new branch name,
            remote branch name, enforce operation)
        """
        branch = self.branchCombo.currentText().replace(" ", "_")
        
        if self.createBranchButton.isChecked():
            branchOp = GitBranchDialog.CreateBranch
        elif self.deleteBranchButton.isChecked():
            branchOp = GitBranchDialog.DeleteBranch
        elif self.moveBranchButton.isChecked():
            branchOp = GitBranchDialog.RenameBranch
        elif self.createSwitchButton.isChecked():
            branchOp = GitBranchDialog.CreateSwitchBranch
        elif self.createTrackingButton.isChecked():
            branchOp = GitBranchDialog.CreateTrackingBranch
        elif self.setTrackingButton.isChecked():
            branchOp = GitBranchDialog.SetTrackingBranch
        else:
            branchOp = GitBranchDialog.UnsetTrackingBranch
        
        return (branchOp, branch, self.revisionEdit.text(),
                self.newBranchNameEdit.text(),
                self.remoteBranchCombo.currentText(),
                self.forceCheckBox.isChecked())
