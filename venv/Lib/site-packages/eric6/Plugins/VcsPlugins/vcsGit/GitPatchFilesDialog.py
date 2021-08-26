# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select a list of patch files.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui import E5FileDialog

from .Ui_GitPatchFilesDialog import Ui_GitPatchFilesDialog

import UI.PixmapCache
import Utilities


class GitPatchFilesDialog(QDialog, Ui_GitPatchFilesDialog):
    """
    Class implementing a dialog to select a list of patch files.
    """
    def __init__(self, rootDir, patchCheckData, parent=None):
        """
        Constructor
        
        @param rootDir root of the directory tree (string)
        @param patchCheckData tuple of data as returned by the
            getData() method
        @param parent reference to the parent widget (QWidget)
        """
        super(GitPatchFilesDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__rootDir = rootDir
        if patchCheckData is not None:
            self.patchFilesList.addItems(patchCheckData[0])
            self.stripSpinBox.setValue(patchCheckData[1])
            self.eofCheckBox.setChecked(patchCheckData[2])
            self.lineCountsCheckBox.setChecked(patchCheckData[3])
        
        self.addButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.deleteButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.upButton.setIcon(UI.PixmapCache.getIcon("1uparrow"))
        self.downButton.setIcon(UI.PixmapCache.getIcon("1downarrow"))
        
        self.__okButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok)
        self.__okButton.setEnabled(len(self.__getPatchFilesList()) > 0)
    
        self.deleteButton.setEnabled(False)
        self.upButton.setEnabled(False)
        self.downButton.setEnabled(False)
    
    @pyqtSlot()
    def on_patchFilesList_itemSelectionChanged(self):
        """
        Private slot to enable button states depending on selection.
        """
        selectedItems = self.patchFilesList.selectedItems()
        count = len(selectedItems)
        isFirst = (
            count == 1 and
            self.patchFilesList.row(selectedItems[0]) == 0
        )
        isLast = (
            count == 1 and
            self.patchFilesList.row(selectedItems[0]) ==
            self.patchFilesList.count() - 1
        )
        self.deleteButton.setEnabled(count > 0)
        self.upButton.setEnabled(count == 1 and not isFirst)
        self.downButton.setEnabled(count == 1 and not isLast)
    
    @pyqtSlot()
    def on_addButton_clicked(self):
        """
        Private slot to add patch files to the list.
        """
        patchFiles = E5FileDialog.getOpenFileNames(
            self,
            self.tr("Patch Files"),
            self.__rootDir,
            self.tr("Patch Files (*.diff *.patch);;All Files (*)"))
        if patchFiles:
            currentPatchFiles = self.__getPatchFilesList()
            for patchFile in patchFiles:
                patchFile = Utilities.toNativeSeparators(patchFile)
                if patchFile not in currentPatchFiles:
                    self.patchFilesList.addItem(patchFile)
        
        self.__okButton.setEnabled(len(self.__getPatchFilesList()) > 0)
        self.on_patchFilesList_itemSelectionChanged()
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        """
        Private slot to delete the selected patch files.
        """
        for itm in self.patchFilesList.selectedItems():
            row = self.patchFilesList.row(itm)
            self.patchFilesList.takeItem(row)
            del itm
        
        self.__okButton.setEnabled(len(self.__getPatchFilesList()) > 0)
        self.on_patchFilesList_itemSelectionChanged()
    
    @pyqtSlot()
    def on_upButton_clicked(self):
        """
        Private slot to move an entry up in the list.
        """
        row = self.patchFilesList.row(self.patchFilesList.selectedItems()[0])
        itm = self.patchFilesList.takeItem(row)
        self.patchFilesList.insertItem(row - 1, itm)
        itm.setSelected(True)
    
    @pyqtSlot()
    def on_downButton_clicked(self):
        """
        Private slot to move an entry down in the list.
        """
        row = self.patchFilesList.row(self.patchFilesList.selectedItems()[0])
        itm = self.patchFilesList.takeItem(row)
        self.patchFilesList.insertItem(row + 1, itm)
        itm.setSelected(True)
    
    def __getPatchFilesList(self):
        """
        Private method to get the list of patch files.
        
        @return list of patch files (list of string)
        """
        patchFiles = []
        for row in range(self.patchFilesList.count()):
            itm = self.patchFilesList.item(row)
            patchFiles.append(itm.text())
        
        return patchFiles
    
    def getData(self):
        """
        Public slot to get the entered data.
        
        @return tuple of list of patch files, strip count, flag indicating
            that the patch has inaccurate end-of-file marker and a flag
            indicating to not trust the line count information
            (list of string, integer, boolean, boolean)
        """
        return (self.__getPatchFilesList(), self.stripSpinBox.value(),
                self.eofCheckBox.isChecked(),
                self.lineCountsCheckBox.isChecked())
