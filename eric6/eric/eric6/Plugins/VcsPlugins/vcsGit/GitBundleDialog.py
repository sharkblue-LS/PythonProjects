# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a bundle operation.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_GitBundleDialog import Ui_GitBundleDialog


class GitBundleDialog(QDialog, Ui_GitBundleDialog):
    """
    Class implementing a dialog to enter the data for a bundle operation.
    """
    def __init__(self, tagsList, branchesList, parent=None):
        """
        Constructor
        
        @param tagsList list of tags (list of strings)
        @param branchesList list of branches (list of strings)
        @param parent parent widget (QWidget)
        """
        super(GitBundleDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        self.tagCombo.addItems(sorted(tagsList))
        self.branchCombo.addItems(["master"] + sorted(branchesList))
    
    def __updateOK(self):
        """
        Private slot to update the OK button.
        """
        enabled = True
        if self.revisionsButton.isChecked():
            enabled = self.revisionsEdit.text() != ""
        elif self.tagButton.isChecked():
            enabled = self.tagCombo.currentText() != ""
        elif self.branchButton.isChecked():
            enabled = self.branchCombo.currentText() != ""
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)
    
    @pyqtSlot(bool)
    def on_revisionsButton_toggled(self, checked):
        """
        Private slot to handle changes of the revisions select button.
        
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
    
    @pyqtSlot(str)
    def on_revisionsEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the Revisions edit.
        
        @param txt text of the line edit (string)
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
    
    def getData(self):
        """
        Public method to retrieve the bundle data.
        
        @return list of revision expressions (list of strings)
        """
        if self.revisionsButton.isChecked():
            revs = self.revisionsEdit.text().strip().split()
        elif self.tagButton.isChecked():
            revs = [self.tagCombo.currentText()]
        elif self.branchButton.isChecked():
            revs = [self.branchCombo.currentText()]
        else:
            revs = []
        
        return revs
