# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a copy operation.
"""

import os.path

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_SvnCopyDialog import Ui_SvnCopyDialog


class SvnCopyDialog(QDialog, Ui_SvnCopyDialog):
    """
    Class implementing a dialog to enter the data for a copy or rename
    operation.
    """
    def __init__(self, source, parent=None, move=False, force=False):
        """
        Constructor
        
        @param source name of the source file/directory (string)
        @param parent parent widget (QWidget)
        @param move flag indicating a move operation (boolean)
        @param force flag indicating a forced operation (boolean)
        """
        super(SvnCopyDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.source = source
        if os.path.isdir(self.source):
            self.targetPicker.setMode(E5PathPickerModes.DirectoryMode)
        else:
            self.targetPicker.setMode(E5PathPickerModes.SaveFileMode)
        
        if move:
            self.setWindowTitle(self.tr('Subversion Move'))
        else:
            self.forceCheckBox.setEnabled(False)
        self.forceCheckBox.setChecked(force)
        
        self.sourceEdit.setText(source)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
        
    def getData(self):
        """
        Public method to retrieve the copy data.
        
        @return the target name (string) and a flag indicating
            the operation should be enforced (boolean)
        """
        target = self.targetPicker.text()
        if not os.path.isabs(target):
            sourceDir = os.path.dirname(self.sourceEdit.text())
            target = os.path.join(sourceDir, target)
        return (target, self.forceCheckBox.isChecked())
    
    @pyqtSlot(str)
    def on_targetPicker_textChanged(self, txt):
        """
        Private slot to handle changes of the target.
        
        @param txt contents of the target edit (string)
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            os.path.isabs(txt) or os.path.dirname(txt) == "")
