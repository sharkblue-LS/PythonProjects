# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a merge operation.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_HgMergeDialog import Ui_HgMergeDialog


class HgMergeDialog(QDialog, Ui_HgMergeDialog):
    """
    Class implementing a dialog to enter the data for a merge operation.
    """
    def __init__(self, tagsList, branchesList, bookmarksList=None,
                 parent=None):
        """
        Constructor
        
        @param tagsList list of tags (list of strings)
        @param branchesList list of branches (list of strings)
        @param bookmarksList list of bookmarks (list of strings)
        @param parent parent widget (QWidget)
        """
        super(HgMergeDialog, self).__init__(parent)
        self.setupUi(self)
       
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        self.tagCombo.addItems(sorted(tagsList))
        self.branchCombo.addItems(["default"] + sorted(branchesList))
        if bookmarksList is not None:
            self.bookmarkCombo.addItems(sorted(bookmarksList))
        else:
            self.bookmarkButton.setHidden(True)
            self.bookmarkCombo.setHidden(True)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateOK(self):
        """
        Private slot to update the OK button.
        """
        enabled = True
        if self.idButton.isChecked():
            enabled = self.idEdit.text() != ""
        elif self.tagButton.isChecked():
            enabled = self.tagCombo.currentText() != ""
        elif self.branchButton.isChecked():
            enabled = self.branchCombo.currentText() != ""
        elif self.bookmarkButton.isChecked():
            enabled = self.bookmarkCombo.currentText() != ""
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)
    
    @pyqtSlot(bool)
    def on_idButton_toggled(self, checked):
        """
        Private slot to handle changes of the ID select button.
        
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
    def on_bookmarkButton_toggled(self, checked):
        """
        Private slot to handle changes of the Bookmark select button.
        
        @param checked state of the button (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_idEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the ID edit.
        
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
    def on_bookmarkCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the Bookmark combo.
        
        @param txt text of the combo (string)
        """
        self.__updateOK()
    
    def getParameters(self):
        """
        Public method to retrieve the merge data.
        
        @return tuple naming the revision and a flag indicating a
            forced merge (string, boolean)
        """
        if self.numberButton.isChecked():
            rev = "rev({0})".format(self.numberSpinBox.value())
        elif self.idButton.isChecked():
            rev = "id({0})".format(self.idEdit.text())
        elif self.tagButton.isChecked():
            rev = self.tagCombo.currentText()
        elif self.branchButton.isChecked():
            rev = self.branchCombo.currentText()
        elif self.bookmarkButton.isChecked():
            rev = self.bookmarkCombo.currentText()
        else:
            rev = ""
        
        return rev, self.forceCheckBox.isChecked()
