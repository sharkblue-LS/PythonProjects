# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter data for the Mercurial Phase operation.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_HgPhaseDialog import Ui_HgPhaseDialog


class HgPhaseDialog(QDialog, Ui_HgPhaseDialog):
    """
    Class dimplementing a dialog to enter data for the Mercurial Phase
    operation.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(HgPhaseDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.phaseCombo.addItem("", "")
        self.phaseCombo.addItem(self.tr("Public"), "p")
        self.phaseCombo.addItem(self.tr("Draft"), "d")
        self.phaseCombo.addItem(self.tr("Secret"), "s")
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
    
    def __updateOk(self):
        """
        Private slot to update the state of the OK button.
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            self.revisionsEdit.toPlainText().strip() != "" and
            self.phaseCombo.currentText().strip() != "")
    
    @pyqtSlot()
    def on_revisionsEdit_textChanged(self):
        """
        Private slot to react upon changes of revisions.
        """
        self.__updateOk()
    
    @pyqtSlot(int)
    def on_phaseCombo_activated(self, index):
        """
        Private slot to react upon changes of the phase.
        
        @param index index of the selected entry
        @type int
        """
        self.__updateOk()
    
    def getData(self):
        """
        Public method to retrieve the entered data.
        
        @return tuple with list of revisions, phase and a flag indicating
            a forced operation (list of strings, string, boolean)
        """
        return (
            self.revisionsEdit.toPlainText().strip().splitlines(),
            self.phaseCombo.itemData(self.phaseCombo.currentIndex()),
            self.forceCheckBox.isChecked()
        )
