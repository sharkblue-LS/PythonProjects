# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to manage the QtHelp documentation database.
"""

import sqlite3

from PyQt5.QtCore import pyqtSlot, Qt, QItemSelectionModel
from PyQt5.QtWidgets import (
    QDialog, QTreeWidgetItem, QListWidgetItem, QInputDialog, QLineEdit
)
from PyQt5.QtHelp import QHelpEngineCore

from E5Gui import E5MessageBox, E5FileDialog
from E5Gui.E5Application import e5App

from .Ui_QtHelpDocumentationDialog import Ui_QtHelpDocumentationDialog


class QtHelpDocumentationDialog(QDialog, Ui_QtHelpDocumentationDialog):
    """
    Class implementing a dialog to manage the QtHelp documentation database.
    """
    def __init__(self, engine, parent):
        """
        Constructor
        
        @param engine reference to the help engine (QHelpEngine)
        @param parent reference to the parent widget (QWidget)
        """
        super(QtHelpDocumentationDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__engine = engine
        self.__mw = parent
        
        self.__initDocumentsTab()
        self.__initFiltersTab()
        
        self.tabWidget.setCurrentIndex(0)
    
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        """
        Private slot handling a change of the current tab.
        
        @param index index of the current tab
        @type int
        """
        if (
            index != 1 and
            (self.__hasChangedFilters() or self.__removedAttributes)
        ):
            yes = E5MessageBox.yesNo(
                self,
                self.tr("Unsaved Filter Changes"),
                self.tr("""The page contains unsaved changes. Shall they be"""
                        """ saved?"""),
                yesDefault=True)
            if yes:
                self.on_applyFilterChangesButton_clicked()
    
    ##################################################################
    ## Documentations Tab
    ##################################################################
    
    def __initDocumentsTab(self):
        """
        Private method to initialize the documents tab.
        """
        self.documentsList.clear()
        self.removeDocumentsButton.setEnabled(False)
        
        docs = self.__engine.registeredDocumentations()
        self.documentsList.addItems(docs)

        self.__registeredDocs = []
        self.__unregisteredDocs = []
        self.__tabsToClose = []

        try:
            self.__pluginHelpDocuments = (
                e5App().getObject("PluginManager").getPluginQtHelpFiles()
            )
        except KeyError:
            from PluginManager.PluginManager import PluginManager
            pluginManager = PluginManager(self, doLoadPlugins=False)
            pluginManager.loadDocumentationSetPlugins()
            pluginManager.activatePlugins()
            self.__pluginHelpDocuments = pluginManager.getPluginQtHelpFiles()
        self.addPluginButton.setEnabled(bool(self.__pluginHelpDocuments))
    
    @pyqtSlot()
    def on_documentsList_itemSelectionChanged(self):
        """
        Private slot handling a change of the documents selection.
        """
        self.removeDocumentsButton.setEnabled(
            len(self.documentsList.selectedItems()) != 0)
    
    @pyqtSlot()
    def on_addDocumentsButton_clicked(self):
        """
        Private slot to add QtHelp documents to the help database.
        """
        fileNames = E5FileDialog.getOpenFileNames(
            self,
            self.tr("Add Documentation"),
            "",
            self.tr("Qt Compressed Help Files (*.qch)"))
        if not fileNames:
            return
        
        self.__registerDocumentations(fileNames)
    
    @pyqtSlot()
    def on_addPluginButton_clicked(self):
        """
        Private slot to add QtHelp documents provided by plug-ins to
        the help database.
        """
        from .QtHelpDocumentationSelectionDialog import (
            QtHelpDocumentationSelectionDialog
        )
        dlg = QtHelpDocumentationSelectionDialog(
            self.__pluginHelpDocuments,
            QtHelpDocumentationSelectionDialog.AddMode,
            self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            documents = dlg.getData()
            if not documents:
                return
            
            self.__registerDocumentations(documents)
    
    @pyqtSlot()
    def on_managePluginButton_clicked(self):
        """
        Private slot to manage the QtHelp documents provided by plug-ins.
        """
        from .QtHelpDocumentationSelectionDialog import (
            QtHelpDocumentationSelectionDialog
        )
        dlg = QtHelpDocumentationSelectionDialog(
            self.__pluginHelpDocuments,
            QtHelpDocumentationSelectionDialog.ManageMode,
            self)
        dlg.exec()
    
    def __registerDocumentations(self, fileNames):
        """
        Private method to register a given list of documentations.
        
        @param fileNames list of documentation files to be registered
        @type list of str
        """
        for fileName in fileNames:
            ns = QHelpEngineCore.namespaceName(fileName)
            if not ns:
                E5MessageBox.warning(
                    self,
                    self.tr("Add Documentation"),
                    self.tr(
                        """The file <b>{0}</b> is not a valid"""
                        """ Qt Help File.""").format(fileName)
                )
                continue
            
            if len(self.documentsList.findItems(
                ns, Qt.MatchFlag.MatchFixedString
            )):
                E5MessageBox.warning(
                    self,
                    self.tr("Add Documentation"),
                    self.tr(
                        """The namespace <b>{0}</b> is already registered.""")
                    .format(ns)
                )
                continue
            
            self.__engine.registerDocumentation(fileName)
            self.documentsList.addItem(ns)
            self.__registeredDocs.append(ns)
            if ns in self.__unregisteredDocs:
                self.__unregisteredDocs.remove(ns)
        
        self.__initFiltersTab()

    @pyqtSlot()
    def on_removeDocumentsButton_clicked(self):
        """
        Private slot to remove a document from the help database.
        """
        res = E5MessageBox.yesNo(
            self,
            self.tr("Remove Documentation"),
            self.tr(
                """Do you really want to remove the selected documentation """
                """sets from the database?"""))
        if not res:
            return
        
        openedDocs = self.__mw.getSourceFileList()
        
        items = self.documentsList.selectedItems()
        for item in items:
            ns = item.text()
            if ns in list(openedDocs.values()):
                res = E5MessageBox.yesNo(
                    self,
                    self.tr("Remove Documentation"),
                    self.tr(
                        """Some documents currently opened reference the """
                        """documentation you are attempting to remove. """
                        """Removing the documentation will close those """
                        """documents. Remove anyway?"""),
                    icon=E5MessageBox.Warning)
                if not res:
                    return
            self.__unregisteredDocs.append(ns)
            for docId in openedDocs:
                if openedDocs[docId] == ns and docId not in self.__tabsToClose:
                    self.__tabsToClose.append(docId)
            itm = self.documentsList.takeItem(self.documentsList.row(item))
            del itm
            
            self.__engine.unregisterDocumentation(ns)
        
        if self.documentsList.count():
            self.documentsList.setCurrentRow(
                0, QItemSelectionModel.SelectionFlag.ClearAndSelect)
    
    def hasDocumentationChanges(self):
        """
        Public slot to test the dialog for changes of configured QtHelp
        documents.
        
        @return flag indicating presence of changes
        @rtype bool
        """
        return (
            len(self.__registeredDocs) > 0 or
            len(self.__unregisteredDocs) > 0
        )
    
    def getTabsToClose(self):
        """
        Public method to get the list of tabs to close.
        
        @return list of tab ids to be closed
        @rtype list of int
        """
        return self.__tabsToClose
    
    ##################################################################
    ## Filters Tab
    ##################################################################
    
    def __initFiltersTab(self):
        """
        Private method to initialize the filters tab.
        """
        self.removeFiltersButton.setEnabled(False)
        self.removeAttributesButton.setEnabled(False)
        
        # save the current and selected filters
        currentFilter = self.filtersList.currentItem()
        if currentFilter:
            currentFilterText = currentFilter.text()
        else:
            currentFilterText = ""
        selectedFiltersText = [
            itm.text() for itm in self.filtersList.selectedItems()]
        
        # save the selected attributes
        selectedAttributesText = [
            itm.text(0) for itm in self.attributesList.selectedItems()]
        
        self.filtersList.clear()
        self.attributesList.clear()
        
        helpEngineCore = QHelpEngineCore(self.__engine.collectionFile())
        
        self.__removedFilters = []
        self.__filterMap = {}
        self.__filterMapBackup = {}
        self.__removedAttributes = []
        
        for customFilter in helpEngineCore.customFilters():
            atts = helpEngineCore.filterAttributes(customFilter)
            self.__filterMapBackup[customFilter] = atts
            if customFilter not in self.__filterMap:
                self.__filterMap[customFilter] = atts
        
        self.filtersList.addItems(sorted(self.__filterMap.keys()))
        for attr in helpEngineCore.filterAttributes():
            QTreeWidgetItem(self.attributesList, [attr])
        self.attributesList.sortItems(0, Qt.SortOrder.AscendingOrder)
        
        if selectedFiltersText or currentFilterText or selectedAttributesText:
            # restore the selected filters
            for txt in selectedFiltersText:
                items = self.filtersList.findItems(
                    txt, Qt.MatchFlag.MatchExactly)
                for itm in items:
                    itm.setSelected(True)
            # restore the current filter
            if currentFilterText:
                items = self.filtersList.findItems(currentFilterText,
                                                   Qt.MatchFlag.MatchExactly)
                if items:
                    self.filtersList.setCurrentItem(
                        items[0], QItemSelectionModel.SelectionFlag.NoUpdate)
            # restore the selected attributes
            for txt in selectedAttributesText:
                items = self.attributesList.findItems(
                    txt, Qt.MatchFlag.MatchExactly, 0)
                for itm in items:
                    itm.setSelected(True)
        elif self.__filterMap:
            self.filtersList.setCurrentRow(0)
    
    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_filtersList_currentItemChanged(self, current, previous):
        """
        Private slot to update the attributes depending on the current filter.
        
        @param current reference to the current item (QListWidgetitem)
        @param previous reference to the previous current item
            (QListWidgetItem)
        """
        checkedList = []
        if current is not None:
            checkedList = self.__filterMap[current.text()]
        for index in range(0, self.attributesList.topLevelItemCount()):
            itm = self.attributesList.topLevelItem(index)
            if itm.text(0) in checkedList:
                itm.setCheckState(0, Qt.CheckState.Checked)
            else:
                itm.setCheckState(0, Qt.CheckState.Unchecked)
    
    @pyqtSlot()
    def on_filtersList_itemSelectionChanged(self):
        """
        Private slot handling a change of selected filters.
        """
        self.removeFiltersButton.setEnabled(
            len(self.filtersList.selectedItems()) > 0)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_attributesList_itemChanged(self, item, column):
        """
        Private slot to handle a change of an attribute.
        
        @param item reference to the changed item (QTreeWidgetItem)
        @param column column containing the change (integer)
        """
        if self.filtersList.currentItem() is None:
            return
        
        customFilter = self.filtersList.currentItem().text()
        if customFilter not in self.__filterMap:
            return
        
        newAtts = []
        for index in range(0, self.attributesList.topLevelItemCount()):
            itm = self.attributesList.topLevelItem(index)
            if itm.checkState(0) == Qt.CheckState.Checked:
                newAtts.append(itm.text(0))
        self.__filterMap[customFilter] = newAtts
    
    @pyqtSlot()
    def on_attributesList_itemSelectionChanged(self):
        """
        Private slot handling the selection of attributes.
        """
        self.removeAttributesButton.setEnabled(
            len(self.attributesList.selectedItems()) != 0)
    
    @pyqtSlot()
    def on_addFilterButton_clicked(self):
        """
        Private slot to add a new filter.
        """
        customFilter, ok = QInputDialog.getText(
            None,
            self.tr("Add Filter"),
            self.tr("Filter name:"),
            QLineEdit.EchoMode.Normal)
        if not customFilter:
            return
        
        if customFilter not in self.__filterMap:
            self.__filterMap[customFilter] = []
            self.filtersList.addItem(customFilter)
        
        itm = self.filtersList.findItems(
            customFilter, Qt.MatchFlag.MatchCaseSensitive)[0]
        self.filtersList.setCurrentItem(itm)
    
    @pyqtSlot()
    def on_removeFiltersButton_clicked(self):
        """
        Private slot to remove the selected filters.
        """
        ok = E5MessageBox.yesNo(
            self,
            self.tr("Remove Filters"),
            self.tr(
                """Do you really want to remove the selected filters """
                """from the database?"""))
        if not ok:
            return
        
        items = self.filtersList.selectedItems()
        for item in items:
            itm = self.filtersList.takeItem(self.filtersList.row(item))
            if itm is None:
                continue
            
            del self.__filterMap[itm.text()]
            self.__removedFilters.append(itm.text())
            del itm
        
        if self.filtersList.count():
            self.filtersList.setCurrentRow(
                0, QItemSelectionModel.SelectionFlag.ClearAndSelect)
    
    @pyqtSlot()
    def on_removeAttributesButton_clicked(self):
        """
        Private slot to remove the selected filter attributes.
        """
        ok = E5MessageBox.yesNo(
            self,
            self.tr("Remove Attributes"),
            self.tr(
                """Do you really want to remove the selected attributes """
                """from the database?"""))
        if not ok:
            return
        
        items = self.attributesList.selectedItems()
        for item in items:
            itm = self.attributesList.takeTopLevelItem(
                self.attributesList.indexOfTopLevelItem(item))
            if itm is None:
                continue
            
            attr = itm.text(0)
            self.__removedAttributes.append(attr)
            for customFilter in self.__filterMap:
                if attr in self.__filterMap[customFilter]:
                    self.__filterMap[customFilter].remove(attr)
            
            del itm
    
    @pyqtSlot()
    def on_unusedAttributesButton_clicked(self):
        """
        Private slot to select all unused attributes.
        """
        # step 1: determine all used attributes
        attributes = set()
        for customFilter in self.__filterMap:
            attributes |= set(self.__filterMap[customFilter])
        
        # step 2: select all unused attribute items
        self.attributesList.clearSelection()
        for row in range(self.attributesList.topLevelItemCount()):
            itm = self.attributesList.topLevelItem(row)
            if itm.text(0) not in attributes:
                itm.setSelected(True)
    
    def __removeAttributes(self):
        """
        Private method to remove attributes from the Qt Help database.
        """
        try:
            self.__db = sqlite3.connect(self.__engine.collectionFile())
        except sqlite3.DatabaseError:
            pass        # ignore database errors
        
        for attr in self.__removedAttributes:
            self.__db.execute(
                "DELETE FROM FilterAttributeTable WHERE Name = '{0}'"  # secok
                .format(attr))
        self.__db.commit()
        self.__db.close()
    
    @pyqtSlot()
    def on_applyFilterChangesButton_clicked(self):
        """
        Private slot to apply the filter changes.
        """
        if self.__hasChangedFilters():
            for customFilter in self.__removedFilters:
                self.__engine.removeCustomFilter(customFilter)
            for customFilter in self.__filterMap:
                self.__engine.addCustomFilter(
                    customFilter, self.__filterMap[customFilter])
        
        if self.__removedAttributes:
            self.__removeAttributes()
        
        self.__initFiltersTab()
    
    def __hasChangedFilters(self):
        """
        Private method to determine, if there are filter changes.
        
        @return flag indicating the presence of filter changes
        @rtype bool
        """
        filtersChanged = False
        if len(self.__filterMapBackup) != len(self.__filterMap):
            filtersChanged = True
        else:
            for customFilter in self.__filterMapBackup:
                if customFilter not in self.__filterMap:
                    filtersChanged = True
                else:
                    oldFilterAtts = self.__filterMapBackup[customFilter]
                    newFilterAtts = self.__filterMap[customFilter]
                    if len(oldFilterAtts) != len(newFilterAtts):
                        filtersChanged = True
                    else:
                        for attr in oldFilterAtts:
                            if attr not in newFilterAtts:
                                filtersChanged = True
                                break

                if filtersChanged:
                    break
        
        return filtersChanged
    
    @pyqtSlot()
    def on_resetFilterChangesButton_clicked(self):
        """
        Private slot to forget the filter changes and reset the tab.
        """
        self.__initFiltersTab()
