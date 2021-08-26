# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a merge operation.
"""

import re

from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_SvnMergeDialog import Ui_SvnMergeDialog


class SvnMergeDialog(QDialog, Ui_SvnMergeDialog):
    """
    Class implementing a dialog to enter the data for a merge operation.
    """
    def __init__(self, mergelist1, mergelist2, targetlist, force=False,
                 parent=None):
        """
        Constructor
        
        @param mergelist1 list of previously entered URLs/revisions
            (list of strings)
        @param mergelist2 list of previously entered URLs/revisions
            (list of strings)
        @param targetlist list of previously entered targets (list of strings)
        @param force flag indicating a forced merge (boolean)
        @param parent parent widget (QWidget)
        """
        super(SvnMergeDialog, self).__init__(parent)
        self.setupUi(self)
       
        self.forceCheckBox.setChecked(force)
        
        self.rx_url = re.compile('(?:file:|svn:|svn+ssh:|http:|https:)//.+')
        self.rx_rev = re.compile('\\d+')
        
        self.tag1Combo.clear()
        self.tag1Combo.addItems(mergelist1)
        self.tag2Combo.clear()
        self.tag2Combo.addItems(mergelist2)
        self.targetCombo.clear()
        self.targetCombo.addItems(targetlist)
        
        self.okButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok)
        self.okButton.setEnabled(False)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
        
    def __enableOkButton(self):
        """
        Private method used to enable/disable the OK-button.
        """
        self.okButton.setDisabled(
            self.tag1Combo.currentText() != "" or
            self.tag2Combo.currentText() != "" or
            not (
                (bool(self.rx_url.fullmatch(self.tag1Combo.currentText())) and
                 bool(self.rx_url.fullmatch(self.tag2Combo.currentText()))) or
                (bool(self.rx_rev.fullmatch(self.tag1Combo.currentText())) and
                 bool(self.rx_rev.fullmatch(self.tag2Combo.currentText())))
            )
        )
        
    def on_tag1Combo_editTextChanged(self, text):
        """
        Private slot to handle the tag1Combo editTextChanged signal.
        
        @param text text of the combo (string)
        """
        self.__enableOkButton()
        
    def on_tag2Combo_editTextChanged(self, text):
        """
        Private slot to handle the tag2Combo editTextChanged signal.
        
        @param text text of the combo (string)
        """
        self.__enableOkButton()
        
    def getParameters(self):
        """
        Public method to retrieve the merge data.
        
        @return tuple naming two tag names or two revisions, a target and
            a flag indicating a forced merge (string, string, string, boolean)
        """
        return (self.tag1Combo.currentText(),
                self.tag2Combo.currentText(),
                self.targetCombo.currentText(),
                self.forceCheckBox.isChecked())
