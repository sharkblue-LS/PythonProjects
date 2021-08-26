# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to manage the list of defined virtual
environments.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QHeaderView

from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_VirtualenvManagerDialog import Ui_VirtualenvManagerDialog

import Utilities


class VirtualenvManagerDialog(QDialog, Ui_VirtualenvManagerDialog):
    """
    Class implementing a dialog to manage the list of defined virtual
    environments.
    """
    IsGlobalRole = Qt.ItemDataRole.UserRole + 1
    IsCondaRole = Qt.ItemDataRole.UserRole + 2
    IsRemoteRole = Qt.ItemDataRole.UserRole + 3
    ExecPathRole = Qt.ItemDataRole.UserRole + 4
    
    def __init__(self, manager, parent=None):
        """
        Constructor
        
        @param manager reference to the virtual environment manager
        @type VirtualenvManager
        @param parent reference to the parent widget
        @type QWidget
        """
        super(VirtualenvManagerDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__manager = manager
        
        baseDir = self.__manager.getVirtualEnvironmentsBaseDir()
        if not baseDir:
            baseDir = Utilities.getHomeDir()
        
        self.envBaseDirectoryPicker.setMode(E5PathPickerModes.DirectoryMode)
        self.envBaseDirectoryPicker.setWindowTitle(
            self.tr("Virtualenv Base Directory"))
        self.envBaseDirectoryPicker.setText(baseDir)
        
        self.__populateVenvList()
        self.__updateButtons()
        
        self.venvList.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
    
    def __updateButtons(self):
        """
        Private method to update the enabled state of the various buttons.
        """
        selectedItemsCount = len(self.venvList.selectedItems())
        topLevelItemCount = self.venvList.topLevelItemCount()
        
        deletableSelectedItemCount = 0
        for itm in self.venvList.selectedItems():
            if (
                itm.text(0) != "<default>" and
                bool(itm.text(1)) and
                not itm.data(0, VirtualenvManagerDialog.IsGlobalRole) and
                not itm.data(0, VirtualenvManagerDialog.IsRemoteRole)
            ):
                deletableSelectedItemCount += 1
        
        deletableItemCount = 0
        for index in range(topLevelItemCount):
            itm = self.venvList.topLevelItem(index)
            if (
                itm.text(0) != "<default>" and
                bool(itm.text(1)) and
                not itm.data(0, VirtualenvManagerDialog.IsRemoteRole)
            ):
                deletableItemCount += 1
        
        canBeRemoved = (
            selectedItemsCount == 1 and
            self.venvList.selectedItems()[0].text(0) != "<default>"
        )
        canAllBeRemoved = (
            topLevelItemCount == 1 and
            self.venvList.topLevelItem(0).text(0) != "<default>"
        )
        
        self.editButton.setEnabled(selectedItemsCount == 1)
        
        self.removeButton.setEnabled(selectedItemsCount > 1 or canBeRemoved)
        self.removeAllButton.setEnabled(
            topLevelItemCount > 1 or canAllBeRemoved)
        
        self.deleteButton.setEnabled(deletableSelectedItemCount)
        self.deleteAllButton.setEnabled(deletableItemCount)
    
    @pyqtSlot()
    def on_addButton_clicked(self):
        """
        Private slot to add a new entry.
        """
        from .VirtualenvAddEditDialog import VirtualenvAddEditDialog
        dlg = VirtualenvAddEditDialog(
            self.__manager,
            baseDir=self.envBaseDirectoryPicker.text()
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (venvName, venvDirectory, venvInterpreter, isGlobal, isConda,
             isRemote, execPath) = dlg.getData()
            
            self.__manager.addVirtualEnv(
                venvName, venvDirectory, venvInterpreter, isGlobal, isConda,
                isRemote, execPath)
    
    @pyqtSlot()
    def on_newButton_clicked(self):
        """
        Private slot to create a new virtual environment.
        """
        self.__manager.createVirtualEnv(
            baseDir=self.envBaseDirectoryPicker.text())
    
    @pyqtSlot()
    def on_editButton_clicked(self):
        """
        Private slot to edit the selected entry.
        """
        selectedItem = self.venvList.selectedItems()[0]
        oldVenvName = selectedItem.text(0)
        
        from .VirtualenvAddEditDialog import VirtualenvAddEditDialog
        dlg = VirtualenvAddEditDialog(
            self.__manager, selectedItem.text(0),
            selectedItem.text(1), selectedItem.text(2),
            selectedItem.data(0, VirtualenvManagerDialog.IsGlobalRole),
            selectedItem.data(0, VirtualenvManagerDialog.IsCondaRole),
            selectedItem.data(0, VirtualenvManagerDialog.IsRemoteRole),
            selectedItem.data(0, VirtualenvManagerDialog.ExecPathRole),
            baseDir=self.envBaseDirectoryPicker.text()
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (venvName, venvDirectory, venvInterpreter, isGlobal, isConda,
             isRemote, execPath) = dlg.getData()
            if venvName != oldVenvName:
                self.__manager.renameVirtualEnv(
                    oldVenvName, venvName, venvDirectory, venvInterpreter,
                    isGlobal, isConda, isRemote, execPath)
            else:
                self.__manager.setVirtualEnv(
                    venvName, venvDirectory, venvInterpreter, isGlobal,
                    isConda, isRemote, execPath)
    
    @pyqtSlot()
    def on_removeButton_clicked(self):
        """
        Private slot to remove all selected entries from the list but keep
        their directories.
        """
        selectedVenvs = []
        for itm in self.venvList.selectedItems():
            selectedVenvs.append(itm.text(0))
        
        if selectedVenvs:
            self.__manager.removeVirtualEnvs(selectedVenvs)
    
    @pyqtSlot()
    def on_removeAllButton_clicked(self):
        """
        Private slot to remove all entries from the list but keep their
        directories.
        """
        venvNames = []
        for index in range(self.venvList.topLevelItemCount()):
            itm = self.venvList.topLevelItem(index)
            venvNames.append(itm.text(0))
        
        if venvNames:
            self.__manager.removeVirtualEnvs(venvNames)
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        """
        Private slot to delete all selected entries from the list and disk.
        """
        selectedVenvs = []
        for itm in self.venvList.selectedItems():
            selectedVenvs.append(itm.text(0))
        
        if selectedVenvs:
            self.__manager.deleteVirtualEnvs(selectedVenvs)
    
    @pyqtSlot()
    def on_deleteAllButton_clicked(self):
        """
        Private slot to delete all entries from the list and disk.
        """
        venvNames = []
        for index in range(self.venvList.topLevelItemCount()):
            itm = self.venvList.topLevelItem(index)
            venvNames.append(itm.text(0))
        
        if venvNames:
            self.__manager.deleteVirtualEnvs(venvNames)
    
    @pyqtSlot()
    def on_venvList_itemSelectionChanged(self):
        """
        Private slot handling a change of the selected items.
        """
        self.__updateButtons()
    
    @pyqtSlot()
    def refresh(self):
        """
        Public slot to refresh the list of shown items.
        """
        # 1. remember selected entries
        selectedVenvs = []
        for itm in self.venvList.selectedItems():
            selectedVenvs.append(itm.text(0))
        
        # 2. clear the list
        self.venvList.clear()
        
        # 3. re-populate the list
        self.__populateVenvList()
        
        # 4. re-establish selection
        for venvName in selectedVenvs:
            itms = self.venvList.findItems(
                venvName, Qt.MatchFlag.MatchExactly, 0)
            if itms:
                itms[0].setSelected(True)
    
    def __populateVenvList(self):
        """
        Private method to populate the list of virtual environments.
        """
        environments = self.__manager.getEnvironmentEntries()
        for venvName in environments:
            itm = QTreeWidgetItem(self.venvList, [
                venvName,
                environments[venvName]["path"],
                environments[venvName]["interpreter"],
            ])
            itm.setData(0, VirtualenvManagerDialog.IsGlobalRole,
                        environments[venvName]["is_global"])
            itm.setData(0, VirtualenvManagerDialog.IsCondaRole,
                        environments[venvName]["is_conda"])
            itm.setData(0, VirtualenvManagerDialog.IsRemoteRole,
                        environments[venvName]["is_remote"])
            itm.setData(0, VirtualenvManagerDialog.ExecPathRole,
                        environments[venvName]["exec_path"])
            
            # show remote environments with underlined font
            if environments[venvName]["is_remote"]:
                font = itm.font(0)
                font.setUnderline(True)
                for column in range(itm.columnCount()):
                    itm.setFont(column, font)
            else:
                # local environments
                
                # show global environments with bold font
                if environments[venvName]["is_global"]:
                    font = itm.font(0)
                    font.setBold(True)
                    for column in range(itm.columnCount()):
                        itm.setFont(column, font)
                
                # show Anaconda environments with italic font
                if environments[venvName]["is_conda"]:
                    font = itm.font(0)
                    font.setItalic(True)
                    for column in range(itm.columnCount()):
                        itm.setFont(column, font)
        
        self.__resizeSections()
    
    def __resizeSections(self):
        """
        Private method to resize the sections of the environment list to their
        contents.
        """
        self.venvList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.venvList.header().setStretchLastSection(True)
    
    def closeEvent(self, evt):
        """
        Protected method to handle the close event.
        
        @param evt reference to the close event
        @type QCloseEvent
        """
        baseDir = self.envBaseDirectoryPicker.text()
        self.__manager.setVirtualEnvironmentsBaseDir(baseDir)
        
        evt.accept()
