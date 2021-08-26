# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter data for the Mercurial import command.
"""

from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_HgImportDialog import Ui_HgImportDialog


class HgImportDialog(QDialog, Ui_HgImportDialog):
    """
    Class implementing a dialog to enter data for the Mercurial import command.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the VCS object
        @type Hg
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HgImportDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.patchFilePicker.setMode(E5PathPickerModes.OpenFileMode)
        self.patchFilePicker.setFilters(self.tr(
            "Patch Files (*.diff *.patch);;All Files (*)"))
        
        self.secretCheckBox.setEnabled(vcs.version >= (5, 3, 0))
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        self.__initDateTime = QDateTime.currentDateTime()
        self.dateEdit.setDateTime(self.__initDateTime)
    
    def __updateOK(self):
        """
        Private slot to update the OK button.
        """
        enabled = True
        if self.patchFilePicker.text() == "":
            enabled = False
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)
    
    @pyqtSlot(str)
    def on_patchFilePicker_textChanged(self, txt):
        """
        Private slot to react on changes of the patch file edit.
        
        @param txt contents of the line edit (string)
        """
        self.__updateOK()
    
    def getParameters(self):
        """
        Public method to retrieve the import data.
        
        @return tuple naming the patch file, a flag indicating to not commit,
            a commit message, a commit date, a commit user, a flag indicating
            to commit with the secret phase, a strip count and a flag
            indicating to enforce the import
        @rtype tuple of (str, bool, str, str, str, bool, int, bool)
        """
        if self.dateEdit.dateTime() != self.__initDateTime:
            date = self.dateEdit.dateTime().toString("yyyy-MM-dd hh:mm")
        else:
            date = ""
        
        return (self.patchFilePicker.text(), self.noCommitCheckBox.isChecked(),
                self.messageEdit.toPlainText(), date, self.userEdit.text(),
                self.secretCheckBox.isChecked(), self.stripSpinBox.value(),
                self.forceCheckBox.isChecked())
