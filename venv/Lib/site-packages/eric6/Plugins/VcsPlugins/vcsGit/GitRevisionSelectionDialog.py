# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select a revision.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_GitRevisionSelectionDialog import Ui_GitRevisionSelectionDialog


class GitRevisionSelectionDialog(QDialog, Ui_GitRevisionSelectionDialog):
    """
    Class implementing a dialog to select a revision.
    """
    def __init__(self, tagsList, branchesList, trackingBranchesList=None,
                 noneLabel="", showBranches=True, showHead=True, parent=None):
        """
        Constructor
        
        @param tagsList list of tags (list of strings)
        @param branchesList list of branches (list of strings)
        @param trackingBranchesList list of remote branches (list of strings)
        @param noneLabel label text for "no revision selected" (string)
        @param showBranches flag indicating to show the branch selection
            (boolean)
        @param showHead flag indicating to show the head selection (boolean)
        @param parent parent widget (QWidget)
        """
        super(GitRevisionSelectionDialog, self).__init__(parent)
        self.setupUi(self)
       
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        self.tagCombo.addItems(sorted(tagsList))
        self.branchCombo.addItems(["master"] + sorted(branchesList))
        
        self.tipButton.setVisible(showHead)
        self.branchButton.setVisible(showBranches)
        self.branchCombo.setVisible(showBranches)
        
        if noneLabel:
            self.noneButton.setText(noneLabel)
        
        if trackingBranchesList is not None:
            self.remoteBranchCombo.addItems(sorted(trackingBranchesList))
        else:
            self.remoteBranchButton.setVisible(False)
            self.remoteBranchCombo.setVisible(False)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateOK(self):
        """
        Private slot to update the OK button.
        """
        enabled = True
        if self.revButton.isChecked():
            enabled = self.revEdit.text() != ""
        elif self.tagButton.isChecked():
            enabled = self.tagCombo.currentText() != ""
        elif self.branchButton.isChecked():
            enabled = self.branchCombo.currentText() != ""
        elif self.remoteBranchButton.isChecked():
            enabled = self.remoteBranchCombo.currentText() != ""
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)
    
    @pyqtSlot(bool)
    def on_revButton_toggled(self, checked):
        """
        Private slot to handle changes of the rev select button.
        
        @param checked state of the button (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(bool)
    def on_tagButton_toggled(self, checked):
        """
        Private slot to handle changes of the Tag select button.
        
        @param checked state of the button (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(bool)
    def on_branchButton_toggled(self, checked):
        """
        Private slot to handle changes of the Branch select button.
        
        @param checked state of the button (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(bool)
    def on_remoteBranchButton_toggled(self, checked):
        """
        Private slot to handle changes of the Remote Branch select button.
        
        @param checked state of the button (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_revEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the rev edit.
        
        @param txt text of the edit (string)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_tagCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the Tag combo.
        
        @param txt text of the combo (string)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_branchCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the Branch combo.
        
        @param txt text of the combo (string)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_remoteBranchCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the Remote Branch combo.
        
        @param txt text of the combo (string)
        """
        self.__updateOK()
    
    def getRevision(self):
        """
        Public method to retrieve the selected revision.
        
        @return selected revision (string)
        """
        if self.revButton.isChecked():
            rev = self.revEdit.text()
        elif self.tagButton.isChecked():
            rev = self.tagCombo.currentText()
        elif self.branchButton.isChecked():
            rev = self.branchCombo.currentText()
        elif self.remoteBranchButton.isChecked():
            rev = self.remoteBranchCombo.currentText()
        elif self.tipButton.isChecked():
            rev = "HEAD"
        else:
            rev = ""
        
        return rev
