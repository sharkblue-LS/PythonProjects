# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter some IDL compiler options.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QInputDialog

from .Ui_IdlCompilerOptionsDialog import Ui_IdlCompilerOptionsDialog

import UI.PixmapCache

from E5Gui import E5PathPickerDialog
from E5Gui.E5PathPicker import E5PathPickerModes

from .IdlCompilerDefineNameDialog import IdlCompilerDefineNameDialog


class IdlCompilerOptionsDialog(QDialog, Ui_IdlCompilerOptionsDialog):
    """
    Class implementing a dialog to enter some IDL compiler options.
    """
    def __init__(self, includeDirectories, definedNames, undefinedNames,
                 project=None, parent=None):
        """
        Constructor
        
        @param includeDirectories list of include directories
        @type list of str
        @param definedNames list of defined variables with name and value
            separated by '='
        @type list of str
        @param undefinedNames list of undefined names
        @type list of str
        @param project reference to the project object
        @type Project
        @param parent reference to the parent widget
        @type QWidget
        """
        super(IdlCompilerOptionsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__project = project
        
        self.idAddButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.idDeleteButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.idEditButton.setIcon(UI.PixmapCache.getIcon("edit"))
        
        self.dnAddButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.dnDeleteButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.dnEditButton.setIcon(UI.PixmapCache.getIcon("edit"))
        
        self.unAddButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.unDeleteButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.unEditButton.setIcon(UI.PixmapCache.getIcon("edit"))
        
        self.__populateIncludeDirectoriesList(includeDirectories)
        self.__populateDefineNamesList(definedNames)
        self.unList.addItems(undefinedNames)
        
        self.__updateIncludeDirectoryButtons()
        self.__updateDefineNameButtons()
        self.__updateUndefineNameButtons()
    
    #######################################################################
    ## Methods implementing the 'Include Directory' option
    #######################################################################
    
    def __updateIncludeDirectoryButtons(self):
        """
        Private method to set the state of the 'Include Directory' buttons.
        """
        enable = len(self.idList.selectedItems())
        self.idDeleteButton.setEnabled(enable)
        self.idEditButton.setEnabled(enable)
    
    def __populateIncludeDirectoriesList(self, includeDirectories):
        """
        Private method to populate the 'Include Directories' list.
        
        @param includeDirectories list of include directories
        @type list of str
        """
        for directory in includeDirectories:
            if self.__project:
                path = self.__project.getRelativeUniversalPath(directory)
                if not path:
                    # it is the project directory
                    path = "."
                self.idList.addItem(path)
            else:
                self.idList.addItem(directory)
    
    def __generateIncludeDirectoriesList(self):
        """
        Private method to prepare the list of 'Include Directories'.
        
        @return list of 'Include Directories'
        @rtype list of str
        """
        return [
            self.idList.item(row).text()
            for row in range(self.idList.count())
        ]
    
    def __includeDirectoriesContain(self, directory):
        """
        Private method to test, if the currently defined 'Include Directories'
        contain a given one.
        
        @param directory directory name to be tested
        @type str
        @return flag indicating that the given directory is already included
        @rtype bool
        """
        return len(self.idList.findItems(
            directory, Qt.MatchFlag.MatchExactly)) > 0
    
    @pyqtSlot()
    def on_idList_itemSelectionChanged(self):
        """
        Private slot handling the selection of an 'Include Directory' entry.
        """
        self.__updateIncludeDirectoryButtons()
    
    @pyqtSlot()
    def on_idAddButton_clicked(self):
        """
        Private slot to add an 'Include Directory'.
        """
        if self.__project:
            defaultDirectory = self.__project.getProjectPath()
        else:
            defaultDirectory = ""
        path, ok = E5PathPickerDialog.getPath(
            self,
            self.tr("Include Directory"),
            self.tr("Select Include Directory"),
            E5PathPickerModes.DirectoryShowFilesMode,
            defaultDirectory=defaultDirectory
        )
        if ok and path:
            if self.__project:
                path = self.__project.getRelativeUniversalPath(path)
                if not path:
                    path = "."
            if not self.__includeDirectoriesContain(path):
                self.idList.addItem(path)
    
    @pyqtSlot()
    def on_idDeleteButton_clicked(self):
        """
        Private slot to delete the selected 'Include Directory' entry.
        """
        itm = self.idList.selectedItems()[0]
        row = self.idList.row(itm)
        self.idList.takeItem(row)
        del itm
    
    @pyqtSlot()
    def on_idEditButton_clicked(self):
        """
        Private slot to edit the selected 'Include Directory' entry.
        """
        itm = self.idList.selectedItems()[0]
        if self.__project:
            path = self.__project.getAbsoluteUniversalPath(itm.text())
            defaultDirectory = self.__project.getProjectPath()
        else:
            path = itm.text()
            defaultDirectory = ""
        path, ok = E5PathPickerDialog.getPath(
            self,
            self.tr("Include Directory"),
            self.tr("Select Include Directory"),
            E5PathPickerModes.DirectoryShowFilesMode,
            path=path,
            defaultDirectory=defaultDirectory
        )
        if ok and path:
            if self.__project:
                path = self.__project.getRelativeUniversalPath(path)
                if not path:
                    path = "."
            if self.__includeDirectoriesContain(path) and itm.text() != path:
                # the entry exists already, delete the edited one
                row = self.idList.row(itm)
                self.idList.takeItem(row)
                del itm
            else:
                itm.setText(path)
    
    #######################################################################
    ## Methods implementing the 'Define Name' option
    #######################################################################
    
    def __updateDefineNameButtons(self):
        """
        Private method to set the state of the 'Define Name' buttons.
        """
        enable = len(self.dnList.selectedItems())
        self.dnDeleteButton.setEnabled(enable)
        self.dnEditButton.setEnabled(enable)
    
    def __populateDefineNamesList(self, definedNames):
        """
        Private method to populate the list of defined names.
        
        @param definedNames list of defined variables with name and value
            separated by '='
        @type list of str
        """
        for definedName in definedNames:
            if definedName:
                nameValueList = definedName.split("=")
                name = nameValueList[0].strip()
                if len(nameValueList) > 1:
                    value = nameValueList[1].strip()
                else:
                    value = ""
                QTreeWidgetItem(self.dnList, [name, value])
        
        self.dnList.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    def __generateDefinedNamesList(self):
        """
        Private method to prepare the list of 'Defined Names'.
        
        @return list of 'Defined Names'
        @rtype list of str
        """
        definedNames = []
        for row in range(self.dnList.topLevelItemCount()):
            itm = self.dnList.topLevelItem(row)
            name = itm.text(0).strip()
            value = itm.text(1).strip()
            if value:
                definedNames.append("{0}={1}".format(name, value))
            else:
                definedNames.append(name)
        
        return definedNames
    
    def __definedNamesContain(self, name):
        """
        Private method to test, if the currently defined 'Defined Names'
        contain a given one.
        
        @param name variable name to be tested
        @type str
        @return flag indicating that the given name is already included
        @rtype bool
        """
        return len(self.dnList.findItems(
            name, Qt.MatchFlag.MatchExactly, 0)) > 0
    
    @pyqtSlot()
    def on_dnList_itemSelectionChanged(self):
        """
        Private slot handling the selection of a 'Define Name' entry.
        """
        self.__updateDefineNameButtons()
    
    @pyqtSlot()
    def on_dnAddButton_clicked(self):
        """
        Private slot to add a 'Define Name' entry.
        """
        dlg = IdlCompilerDefineNameDialog(parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, value = dlg.getData()
            if not self.__definedNamesContain(name):
                QTreeWidgetItem(self.dnList, [name, value])
        
        self.dnList.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    @pyqtSlot()
    def on_dnDeleteButton_clicked(self):
        """
        Private slot to delete the selected 'Define Name' entry.
        """
        itm = self.dnList.selectedItems()[0]
        index = self.dnList.indexOfTopLevelItem(itm)
        self.dnList.takeTopLevelItem(index)
        del itm
    
    @pyqtSlot()
    def on_dnEditButton_clicked(self):
        """
        Private slot to edit the selected 'Define Name' entry.
        """
        itm = self.dnList.selectedItems()[0]
        
        dlg = IdlCompilerDefineNameDialog(
            name=itm.text(0), value=itm.text(1), parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, value = dlg.getData()
            if self.__definedNamesContain(name) and itm.text(0) != name:
                # the entry exists already, delete the edited one
                index = self.dnList.indexOfTopLevelItem(itm)
                self.dnList.takeTopLevelItem(index)
                del itm
                
                # change the named one
                itm = self.dnList.findItems(
                    name, Qt.MatchFlag.MatchExactly, 0)[0]
                itm.setText(1, value)
            else:
                itm.setText(0, name)
                itm.setText(1, value)
        
        self.dnList.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    #######################################################################
    ## Methods implementing the 'Undefine Name' option
    #######################################################################
    
    def __updateUndefineNameButtons(self):
        """
        Private method to set the state of the 'Undefine Name' buttons.
        """
        enable = len(self.unList.selectedItems())
        self.unDeleteButton.setEnabled(enable)
        self.unEditButton.setEnabled(enable)
    
    def __generateUndefinedNamesList(self):
        """
        Private method to prepare the list of 'Undefined Names'.
        
        @return list of 'Undefined Names'
        @rtype list of str
        """
        return [
            self.unList.item(row).text()
            for row in range(self.unList.count())
        ]
    
    def __undefinedNamesContain(self, name):
        """
        Private method to test, if the currently defined 'Undefined Names'
        contain a given one.
        
        @param name variable name to be tested
        @type str
        @return flag indicating that the given name is already included
        @rtype bool
        """
        return len(self.unList.findItems(name, Qt.MatchFlag.MatchExactly)) > 0
    
    @pyqtSlot()
    def on_unList_itemSelectionChanged(self):
        """
        Private slot handling the selection of a 'Undefine Name' entry.
        """
        self.__updateUndefineNameButtons()
    
    @pyqtSlot()
    def on_unAddButton_clicked(self):
        """
        Private slot to add a 'Undefine Name' entry.
        """
        name, ok = QInputDialog.getText(
            self,
            self.tr("Undefine Name"),
            self.tr("Enter a variable name to be undefined:")
        )
        name = name.strip()
        if ok and name and not self.__undefinedNamesContain(name):
            self.unList.addItem(name)
    
    @pyqtSlot()
    def on_unDeleteButton_clicked(self):
        """
        Private slot to delete the selected 'Undefine Name' entry.
        """
        itm = self.unList.selectedItems()[0]
        row = self.unList.row(itm)
        self.unList.takeItem(row)
        del itm
    
    @pyqtSlot()
    def on_unEditButton_clicked(self):
        """
        Private slot to edit the selected 'Undefine Name' entry.
        """
        itm = self.unList.selectedItems()[0]
        name, ok = QInputDialog.getText(
            self,
            self.tr("Undefine Name"),
            self.tr("Enter a variable name to be undefined:"),
            text=itm.text()
        )
        name = name.strip()
        if ok and name:
            if self.__undefinedNamesContain(name) and itm.text() != name:
                # the entry exists already, delete the edited one
                row = self.unList.row(itm)
                self.unList.takeItem(row)
                del itm
            else:
                itm.setText(name)
    
    #######################################################################
    ## Methods implementing the result preparation
    #######################################################################
    
    def getData(self):
        """
        Public method to return the data entered by the user.
        
        @return tuple containing the list of include directories, list of
            defined names and list of undefined names
        @rtype tuple of (list of str, list of str, list of str)
        """
        return (
            self.__generateIncludeDirectoriesList(),
            self.__generateDefinedNamesList(),
            self.__generateUndefinedNamesList(),
        )
