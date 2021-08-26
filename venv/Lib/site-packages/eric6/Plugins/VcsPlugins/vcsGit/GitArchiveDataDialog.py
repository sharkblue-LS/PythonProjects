# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for the creation of an archive.
"""

import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui import E5FileDialog

from .Ui_GitArchiveDataDialog import Ui_GitArchiveDataDialog

import UI.PixmapCache
import Utilities


class GitArchiveDataDialog(QDialog, Ui_GitArchiveDataDialog):
    """
    Class implementing a dialog to enter the data for the creation of an
    archive.
    """
    def __init__(self, tagsList, branchesList, formatsList, parent=None):
        """
        Constructor
        
        @param tagsList list of tags (list of strings)
        @param branchesList list of branches (list of strings)
        @param formatsList list of archive formats (list of strings)
        @param parent reference to the parent widget (QWidget)
        """
        super(GitArchiveDataDialog, self).__init__(parent)
        self.setupUi(self)
       
        self.fileButton.setIcon(UI.PixmapCache.getIcon("open"))
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        self.tagCombo.addItems(sorted(tagsList))
        self.branchCombo.addItems(["master"] + sorted(branchesList))
        self.formatComboBox.addItems(sorted(formatsList))
        self.formatComboBox.setCurrentIndex(
            self.formatComboBox.findText("zip"))
        
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
        
        enabled &= bool(self.fileEdit.text())
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)
    
    @pyqtSlot(str)
    def on_fileEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the file edit.
        
        @param txt text of the edit (string)
        """
        self.__updateOK()
    
    @pyqtSlot()
    def on_fileButton_clicked(self):
        """
        Private slot to select a file via a file selection dialog.
        """
        fileName = E5FileDialog.getSaveFileName(
            self,
            self.tr("Select Archive File"),
            Utilities.fromNativeSeparators(self.fileEdit.text()),
            "")
            
        if fileName:
            root, ext = os.path.splitext(fileName)
            if not ext:
                ext = "." + self.formatComboBox.currentText()
            fileName = root + ext
            self.fileEdit.setText(Utilities.toNativeSeparators(fileName))
    
    @pyqtSlot(bool)
    def on_revButton_toggled(self, checked):
        """
        Private slot to handle changes of the rev select button.
        
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
    
    @pyqtSlot(bool)
    def on_tagButton_toggled(self, checked):
        """
        Private slot to handle changes of the Tag select button.
        
        @param checked state of the button (boolean)
        """
        self.__updateOK()
    
    @pyqtSlot(str)
    def on_tagCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the Tag combo.
        
        @param txt text of the combo (string)
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
    def on_branchCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the Branch combo.
        
        @param txt text of the combo (string)
        """
        self.__updateOK()
    
    def getData(self):
        """
        Public method to retrieve the entered data.
        
        @return tuple of selected revision (string), archive format (string),
            archive file (string) and prefix (string)
        """
        if self.revButton.isChecked():
            rev = self.revEdit.text()
        elif self.tagButton.isChecked():
            rev = self.tagCombo.currentText()
        elif self.branchButton.isChecked():
            rev = self.branchCombo.currentText()
        else:
            rev = "HEAD"
        
        return (rev, self.formatComboBox.currentText(),
                Utilities.toNativeSeparators(self.fileEdit.text()),
                self.prefixEdit.text()
                )
