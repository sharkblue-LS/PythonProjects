# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a copy or rename operation.
"""

import os.path

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui.E5Completers import E5FileCompleter, E5DirCompleter
from E5Gui import E5FileDialog

from .Ui_GitCopyDialog import Ui_GitCopyDialog

import Utilities
import UI.PixmapCache


class GitCopyDialog(QDialog, Ui_GitCopyDialog):
    """
    Class implementing a dialog to enter the data for a copy or rename
    operation.
    """
    def __init__(self, source, parent=None, move=False):
        """
        Constructor
        
        @param source name of the source file/directory (string)
        @param parent parent widget (QWidget)
        @param move flag indicating a move operation (boolean)
        """
        super(GitCopyDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.dirButton.setIcon(UI.PixmapCache.getIcon("open"))
       
        self.source = source
        if os.path.isdir(self.source):
            self.targetCompleter = E5DirCompleter(self.targetEdit)
        else:
            self.targetCompleter = E5FileCompleter(self.targetEdit)
        
        if move:
            self.setWindowTitle(self.tr('Git Move'))
        else:
            self.forceCheckBox.setEnabled(False)
        
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
        target = self.targetEdit.text()
        if not os.path.isabs(target):
            sourceDir = os.path.dirname(self.sourceEdit.text())
            target = os.path.join(sourceDir, target)
        return (
            Utilities.toNativeSeparators(target),
            self.forceCheckBox.isChecked()
        )
    
    @pyqtSlot()
    def on_dirButton_clicked(self):
        """
        Private slot to handle the button press for selecting the target via a
        selection dialog.
        """
        if os.path.isdir(self.source):
            target = E5FileDialog.getExistingDirectory(
                self,
                self.tr("Select target"),
                self.targetEdit.text(),
                E5FileDialog.Options(E5FileDialog.ShowDirsOnly))
        else:
            target = E5FileDialog.getSaveFileName(
                self,
                self.tr("Select target"),
                self.targetEdit.text(),
                "",
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
        
        if target:
            self.targetEdit.setText(Utilities.toNativeSeparators(target))
    
    @pyqtSlot(str)
    def on_targetEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the target.
        
        @param txt contents of the target edit (string)
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            os.path.isabs(txt) or os.path.dirname(txt) == "")
