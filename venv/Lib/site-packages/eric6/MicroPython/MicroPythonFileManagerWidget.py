# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a file manager for MicroPython devices.
"""

import os
import shutil

from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtWidgets import (
    QWidget, QTreeWidgetItem, QHeaderView, QMenu, QInputDialog, QLineEdit,
    QDialog
)

from E5Gui import E5MessageBox, E5PathPickerDialog
from E5Gui.E5PathPicker import E5PathPickerModes
from E5Gui.E5FileSaveConfirmDialog import confirmOverwrite
from E5Gui.E5Application import e5App

from .Ui_MicroPythonFileManagerWidget import Ui_MicroPythonFileManagerWidget

from .MicroPythonFileManager import MicroPythonFileManager
from .MicroPythonFileSystemUtilities import (
    mtime2string, mode2string, decoratedName, listdirStat
)

from UI.DeleteFilesConfirmationDialog import DeleteFilesConfirmationDialog

import UI.PixmapCache
import Preferences
import Utilities
import Globals


class MicroPythonFileManagerWidget(QWidget, Ui_MicroPythonFileManagerWidget):
    """
    Class implementing a file manager for MicroPython devices.
    """
    def __init__(self, commandsInterface, deviceWithLocalAccess, parent=None):
        """
        Constructor
        
        @param commandsInterface reference to the commands interface object
        @type MicroPythonCommandsInterface
        @param deviceWithLocalAccess flag indicating the device supports file
            access via a local directory
        @type bool
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MicroPythonFileManagerWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.__repl = parent
        self.__deviceWithLocalAccess = deviceWithLocalAccess
        
        self.syncButton.setIcon(UI.PixmapCache.getIcon("2rightarrow"))
        self.putButton.setIcon(UI.PixmapCache.getIcon("1rightarrow"))
        self.putAsButton.setIcon(UI.PixmapCache.getIcon("putAs"))
        self.getButton.setIcon(UI.PixmapCache.getIcon("1leftarrow"))
        self.getAsButton.setIcon(UI.PixmapCache.getIcon("getAs"))
        self.localUpButton.setIcon(UI.PixmapCache.getIcon("1uparrow"))
        self.localHomeButton.setIcon(UI.PixmapCache.getIcon("home"))
        self.localReloadButton.setIcon(UI.PixmapCache.getIcon("reload"))
        self.deviceUpButton.setIcon(UI.PixmapCache.getIcon("1uparrow"))
        self.deviceHomeButton.setIcon(UI.PixmapCache.getIcon("home"))
        self.deviceReloadButton.setIcon(UI.PixmapCache.getIcon("reload"))
        
        self.deviceUpButton.setEnabled(not self.__repl.isMicrobit())
        self.deviceHomeButton.setEnabled(not self.__repl.isMicrobit())
        
        self.putButton.setEnabled(False)
        self.putAsButton.setEnabled(False)
        self.getButton.setEnabled(False)
        self.getAsButton.setEnabled(False)
        
        self.localFileTreeWidget.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder)
        self.deviceFileTreeWidget.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder)
        
        self.__progressInfoDialog = None
        self.__fileManager = MicroPythonFileManager(commandsInterface, self)
        
        self.__fileManager.longListFiles.connect(self.__handleLongListFiles)
        self.__fileManager.currentDir.connect(self.__handleCurrentDir)
        self.__fileManager.currentDirChanged.connect(self.__handleCurrentDir)
        self.__fileManager.putFileDone.connect(self.__newDeviceList)
        self.__fileManager.getFileDone.connect(self.__handleGetDone)
        self.__fileManager.rsyncDone.connect(self.__handleRsyncDone)
        self.__fileManager.rsyncProgressMessage.connect(
            self.__handleRsyncProgressMessage)
        self.__fileManager.removeDirectoryDone.connect(self.__newDeviceList)
        self.__fileManager.createDirectoryDone.connect(self.__newDeviceList)
        self.__fileManager.deleteFileDone.connect(self.__newDeviceList)
        self.__fileManager.fsinfoDone.connect(self.__fsInfoResultReceived)
        
        self.__fileManager.error.connect(self.__handleError)
        
        self.localFileTreeWidget.customContextMenuRequested.connect(
            self.__showLocalContextMenu)
        self.deviceFileTreeWidget.customContextMenuRequested.connect(
            self.__showDeviceContextMenu)
        
        self.__localMenu = QMenu(self)
        self.__localMenu.addAction(self.tr("Change Directory"),
                                   self.__changeLocalDirectory)
        self.__localMenu.addAction(
            self.tr("Create Directory"), self.__createLocalDirectory)
        self.__localDelDirTreeAct = self.__localMenu.addAction(
            self.tr("Delete Directory Tree"), self.__deleteLocalDirectoryTree)
        self.__localMenu.addSeparator()
        self.__localDelFileAct = self.__localMenu.addAction(
            self.tr("Delete File"), self.__deleteLocalFile)
        self.__localMenu.addSeparator()
        act = self.__localMenu.addAction(self.tr("Show Hidden Files"))
        act.setCheckable(True)
        act.setChecked(Preferences.getMicroPython("ShowHiddenLocal"))
        act.triggered[bool].connect(self.__localHiddenChanged)
        
        self.__deviceMenu = QMenu(self)
        if not self.__repl.isMicrobit():
            self.__deviceMenu.addAction(
                self.tr("Change Directory"), self.__changeDeviceDirectory)
            self.__deviceMenu.addAction(
                self.tr("Create Directory"), self.__createDeviceDirectory)
            if not self.__deviceWithLocalAccess:
                self.__devDelDirAct = self.__deviceMenu.addAction(
                    self.tr("Delete Directory"), self.__deleteDeviceDirectory)
            self.__devDelDirTreeAct = self.__deviceMenu.addAction(
                self.tr("Delete Directory Tree"),
                self.__deleteDeviceDirectoryTree)
            self.__deviceMenu.addSeparator()
        self.__devDelFileAct = self.__deviceMenu.addAction(
            self.tr("Delete File"), self.__deleteDeviceFile)
        self.__deviceMenu.addSeparator()
        act = self.__deviceMenu.addAction(self.tr("Show Hidden Files"))
        act.setCheckable(True)
        act.setChecked(Preferences.getMicroPython("ShowHiddenDevice"))
        act.triggered[bool].connect(self.__deviceHiddenChanged)
        if not parent.isMicrobit():
            self.__deviceMenu.addSeparator()
            self.__deviceMenu.addAction(
                self.tr("Show Filesystem Info"), self.__showFileSystemInfo)
    
    def start(self):
        """
        Public method to start the widget.
        """
        dirname = ""
        vm = e5App().getObject("ViewManager")
        aw = vm.activeWindow()
        if aw:
            dirname = os.path.dirname(aw.getFileName())
        if not dirname:
            dirname = (
                Preferences.getMicroPython("MpyWorkspace") or
                Preferences.getMultiProject("Workspace") or
                os.path.expanduser("~")
            )
        self.__listLocalFiles(dirname)
        
        if self.__deviceWithLocalAccess:
            dirname = self.__repl.getDeviceWorkspace()
            if dirname:
                self.__listLocalFiles(dirname, True)
                return
        
        # list files via device script
        self.__fileManager.pwd()
    
    def stop(self):
        """
        Public method to stop the widget.
        """
        pass
    
    @pyqtSlot(str, str)
    def __handleError(self, method, error):
        """
        Private slot to handle errors.
        
        @param method name of the method the error occured in
        @type str
        @param error error message
        @type str
        """
        E5MessageBox.warning(
            self,
            self.tr("Error handling device"),
            self.tr("<p>There was an error communicating with the connected"
                    " device.</p><p>Method: {0}</p><p>Message: {1}</p>")
            .format(method, error))
    
    @pyqtSlot(str)
    def __handleCurrentDir(self, dirname):
        """
        Private slot to handle a change of the current directory of the device.
        
        @param dirname name of the current directory
        @type str
        """
        self.deviceCwd.setText(dirname)
        self.__newDeviceList()
    
    @pyqtSlot(tuple)
    def __handleLongListFiles(self, filesList):
        """
        Private slot to receive a long directory listing.
        
        @param filesList tuple containing tuples with name, mode, size and time
            for each directory entry
        @type tuple of (str, str, str, str)
        """
        self.deviceFileTreeWidget.clear()
        for name, mode, size, dateTime in filesList:
            itm = QTreeWidgetItem(self.deviceFileTreeWidget,
                                  [name, mode, size, dateTime])
            itm.setTextAlignment(1, Qt.AlignmentFlag.AlignHCenter)
            itm.setTextAlignment(2, Qt.AlignmentFlag.AlignRight)
        self.deviceFileTreeWidget.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
    
    def __listLocalFiles(self, dirname="", localDevice=False):
        """
        Private method to populate the local files list.
        
        @param dirname name of the local directory to be listed
        @type str
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if not dirname:
            dirname = os.getcwd()
        if dirname.endswith(os.sep):
            dirname = dirname[:-1]
        if localDevice:
            self.deviceCwd.setText(dirname)
            showHidden = Preferences.getMicroPython("ShowHiddenDevice")
        else:
            self.localCwd.setText(dirname)
            showHidden = Preferences.getMicroPython("ShowHiddenLocal")
        
        filesStatList = listdirStat(dirname, showHidden=showHidden)
        filesList = [(
            decoratedName(f, s[0], os.path.isdir(os.path.join(dirname, f))),
            mode2string(s[0]),
            str(s[6]),
            mtime2string(s[8])) for f, s in filesStatList]
        if localDevice:
            fileTreeWidget = self.deviceFileTreeWidget
        else:
            fileTreeWidget = self.localFileTreeWidget
        fileTreeWidget.clear()
        for item in filesList:
            itm = QTreeWidgetItem(fileTreeWidget, item)
            itm.setTextAlignment(1, Qt.AlignmentFlag.AlignHCenter)
            itm.setTextAlignment(2, Qt.AlignmentFlag.AlignRight)
        fileTreeWidget.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_localFileTreeWidget_itemActivated(self, item, column):
        """
        Private slot to handle the activation of a local item.
        
        If the item is a directory, the list will be re-populated for this
        directory.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column column of the activation
        @type int
        """
        name = os.path.join(self.localCwd.text(), item.text(0))
        if name.endswith("/"):
            # directory names end with a '/'
            self.__listLocalFiles(name[:-1])
        elif Utilities.MimeTypes.isTextFile(name):
            e5App().getObject("ViewManager").getEditor(name)
    
    @pyqtSlot()
    def on_localFileTreeWidget_itemSelectionChanged(self):
        """
        Private slot handling a change of selection in the local pane.
        """
        enable = bool(len(self.localFileTreeWidget.selectedItems()))
        if enable:
            enable &= not (
                self.localFileTreeWidget.selectedItems()[0].text(0)
                .endswith("/"))
        self.putButton.setEnabled(enable)
        self.putAsButton.setEnabled(enable)
    
    @pyqtSlot()
    def on_localUpButton_clicked(self):
        """
        Private slot to go up one directory level.
        """
        cwd = self.localCwd.text()
        dirname = os.path.dirname(cwd)
        self.__listLocalFiles(dirname)
    
    @pyqtSlot()
    def on_localHomeButton_clicked(self):
        """
        Private slot to change directory to the configured workspace.
        """
        dirname = (
            Preferences.getMicroPython("MpyWorkspace") or
            Preferences.getMultiProject("Workspace") or
            os.path.expanduser("~")
        )
        self.__listLocalFiles(dirname)
    
    @pyqtSlot()
    def on_localReloadButton_clicked(self):
        """
        Private slot to reload the local list.
        """
        dirname = self.localCwd.text()
        self.__listLocalFiles(dirname)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_deviceFileTreeWidget_itemActivated(self, item, column):
        """
        Private slot to handle the activation of a device item.
        
        If the item is a directory, the current working directory is changed
        and the list will be re-populated for this directory.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column column of the activation
        @type int
        """
        if self.__deviceWithLocalAccess:
            name = os.path.join(self.deviceCwd.text(), item.text(0))
            if name.endswith("/"):
                # directory names end with a '/'
                self.__listLocalFiles(name[:-1], True)
            elif Utilities.MimeTypes.isTextFile(name):
                e5App().getObject("ViewManager").getEditor(name)
        else:
            cwd = self.deviceCwd.text()
            if cwd.endswith("/"):
                name = cwd + item.text(0)
            else:
                name = "{0}/{1}".format(cwd, item.text(0))
            if name.endswith("/"):
                # directory names end with a '/'
                self.__fileManager.cd(name[:-1])
    
    @pyqtSlot()
    def on_deviceFileTreeWidget_itemSelectionChanged(self):
        """
        Private slot handling a change of selection in the local pane.
        """
        enable = bool(len(self.deviceFileTreeWidget.selectedItems()))
        if enable:
            enable &= not (
                self.deviceFileTreeWidget.selectedItems()[0].text(0)
                .endswith("/"))
        self.getButton.setEnabled(enable)
        self.getAsButton.setEnabled(enable)
    
    @pyqtSlot()
    def on_deviceUpButton_clicked(self):
        """
        Private slot to go up one directory level on the device.
        """
        cwd = self.deviceCwd.text()
        dirname = os.path.dirname(cwd)
        if self.__deviceWithLocalAccess:
            self.__listLocalFiles(dirname, True)
        else:
            self.__fileManager.cd(dirname)
    
    @pyqtSlot()
    def on_deviceHomeButton_clicked(self):
        """
        Private slot to move to the device home directory.
        """
        if self.__deviceWithLocalAccess:
            dirname = self.__repl.getDeviceWorkspace()
            if dirname:
                self.__listLocalFiles(dirname, True)
                return
        
        # list files via device script
        self.__fileManager.cd("/")
    
    @pyqtSlot()
    def on_deviceReloadButton_clicked(self):
        """
        Private slot to reload the device list.
        """
        dirname = self.deviceCwd.text()
        if self.__deviceWithLocalAccess:
            self.__listLocalFiles(dirname, True)
        else:
            if dirname:
                self.__newDeviceList()
            else:
                self.__fileManager.pwd()
    
    def __isFileInList(self, filename, treeWidget):
        """
        Private method to check, if a file name is contained in a tree widget.
        
        @param filename name of the file to check
        @type str
        @param treeWidget reference to the tree widget to be checked against
        @return flag indicating that the file name is present
        @rtype bool
        """
        itemCount = treeWidget.topLevelItemCount()
        if itemCount:
            for row in range(itemCount):
                if treeWidget.topLevelItem(row).text(0) == filename:
                    return True
        
        return False
    
    @pyqtSlot()
    def on_putButton_clicked(self, putAs=False):
        """
        Private slot to copy the selected file to the connected device.
        
        @param putAs flag indicating to give it a new name
        @type bool
        """
        selectedItems = self.localFileTreeWidget.selectedItems()
        if selectedItems:
            filename = selectedItems[0].text(0).strip()
            if not filename.endswith("/"):
                # it is really a file
                if putAs:
                    deviceFilename, ok = QInputDialog.getText(
                        self,
                        self.tr("Put File As"),
                        self.tr("Enter a new name for the file"),
                        QLineEdit.EchoMode.Normal,
                        filename)
                    if not ok or not filename:
                        return
                else:
                    deviceFilename = filename
                
                if self.__isFileInList(deviceFilename,
                                       self.deviceFileTreeWidget):
                    # ask for overwrite permission
                    action, resultFilename = confirmOverwrite(
                        deviceFilename, self.tr("Copy File to Device"),
                        self.tr("The given file exists already"
                                " (Enter file name only)."),
                        False, self)
                    if action == "cancel":
                        return
                    elif action == "rename":
                        deviceFilename = os.path.basename(resultFilename)
                
                if self.__deviceWithLocalAccess:
                    shutil.copy2(
                        os.path.join(self.localCwd.text(), filename),
                        os.path.join(self.deviceCwd.text(), deviceFilename)
                    )
                    self.__listLocalFiles(self.deviceCwd.text(),
                                          localDevice=True)
                else:
                    deviceCwd = self.deviceCwd.text()
                    if deviceCwd:
                        if deviceCwd != "/":
                            deviceFilename = deviceCwd + "/" + deviceFilename
                        else:
                            deviceFilename = "/" + deviceFilename
                    self.__fileManager.put(
                        os.path.join(self.localCwd.text(), filename),
                        deviceFilename
                    )
    
    @pyqtSlot()
    def on_putAsButton_clicked(self):
        """
        Private slot to copy the selected file to the connected device
        with a different name.
        """
        self.on_putButton_clicked(putAs=True)
    
    @pyqtSlot()
    def on_getButton_clicked(self, getAs=False):
        """
        Private slot to copy the selected file from the connected device.
        
        @param getAs flag indicating to give it a new name
        @type bool
        """
        selectedItems = self.deviceFileTreeWidget.selectedItems()
        if selectedItems:
            filename = selectedItems[0].text(0).strip()
            if not filename.endswith("/"):
                # it is really a file
                if getAs:
                    localFilename, ok = QInputDialog.getText(
                        self,
                        self.tr("Get File As"),
                        self.tr("Enter a new name for the file"),
                        QLineEdit.EchoMode.Normal,
                        filename)
                    if not ok or not filename:
                        return
                else:
                    localFilename = filename
                
                if self.__isFileInList(localFilename,
                                       self.localFileTreeWidget):
                    # ask for overwrite permission
                    action, resultFilename = confirmOverwrite(
                        localFilename, self.tr("Copy File from Device"),
                        self.tr("The given file exists already."),
                        True, self)
                    if action == "cancel":
                        return
                    elif action == "rename":
                        localFilename = resultFilename
                
                if self.__deviceWithLocalAccess:
                    shutil.copy2(
                        os.path.join(self.deviceCwd.text(), filename),
                        os.path.join(self.localCwd.text(), localFilename)
                    )
                    self.__listLocalFiles(self.localCwd.text())
                else:
                    deviceCwd = self.deviceCwd.text()
                    if deviceCwd:
                        filename = deviceCwd + "/" + filename
                    self.__fileManager.get(
                        filename,
                        os.path.join(self.localCwd.text(), localFilename)
                    )
    
    @pyqtSlot()
    def on_getAsButton_clicked(self):
        """
        Private slot to copy the selected file from the connected device
        with a different name.
        """
        self.on_getButton_clicked(getAs=True)
    
    @pyqtSlot(str, str)
    def __handleGetDone(self, deviceFile, localFile):
        """
        Private slot handling a successful copy of a file from the device.
        
        @param deviceFile name of the file on the device
        @type str
        @param localFile name of the local file
        @type str
        """
        self.__listLocalFiles(self.localCwd.text())
    
    @pyqtSlot()
    def on_syncButton_clicked(self):
        """
        Private slot to synchronize the local directory to the device.
        """
        self.__fileManager.rsync(
            self.localCwd.text(),
            self.deviceCwd.text(),
            mirror=True,
            localDevice=self.__deviceWithLocalAccess,
        )
    
    @pyqtSlot(str, str)
    def __handleRsyncDone(self, localDir, deviceDir):
        """
        Private method to handle the completion of the rsync operation.
        
        @param localDir name of the local directory
        @type str
        @param deviceDir name of the device directory
        @type str
        """
        # simulate button presses to reload the two lists
        self.on_localReloadButton_clicked()
        self.on_deviceReloadButton_clicked()
    
    @pyqtSlot(str)
    def __handleRsyncProgressMessage(self, message):
        """
        Private slot handling progress messages sent by the file manager.
        
        @param message message to be shown
        @type str
        """
        if self.__progressInfoDialog is None:
            from .MicroPythonProgressInfoDialog import (
                MicroPythonProgressInfoDialog
            )
            self.__progressInfoDialog = MicroPythonProgressInfoDialog(self)
            self.__progressInfoDialog.finished.connect(
                self.__progressInfoDialogFinished)
        self.__progressInfoDialog.show()
        self.__progressInfoDialog.addMessage(message)
    
    @pyqtSlot()
    def __progressInfoDialogFinished(self):
        """
        Private slot handling the closing of the progress info dialog.
        """
        self.__progressInfoDialog.deleteLater()
        self.__progressInfoDialog = None
    
    @pyqtSlot()
    def __newDeviceList(self):
        """
        Private slot to initiate a new long list of the device directory.
        """
        self.__fileManager.lls(
            self.deviceCwd.text(),
            showHidden=Preferences.getMicroPython("ShowHiddenDevice")
        )
    
    ##################################################################
    ## Context menu methods for the local files below
    ##################################################################
    
    @pyqtSlot(QPoint)
    def __showLocalContextMenu(self, pos):
        """
        Private slot to show the REPL context menu.
        
        @param pos position to show the menu at
        @type QPoint
        """
        hasSelection = bool(len(self.localFileTreeWidget.selectedItems()))
        if hasSelection:
            name = self.localFileTreeWidget.selectedItems()[0].text(0)
            isDir = name.endswith("/")
            isFile = not isDir
        else:
            isDir = False
            isFile = False
        self.__localDelDirTreeAct.setEnabled(isDir)
        self.__localDelFileAct.setEnabled(isFile)
        
        self.__localMenu.exec(self.localFileTreeWidget.mapToGlobal(pos))
    
    @pyqtSlot()
    def __changeLocalDirectory(self, localDevice=False):
        """
        Private slot to change the local directory.
        
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if localDevice:
            cwdWidget = self.deviceCwd
        else:
            cwdWidget = self.localCwd
        
        dirPath, ok = E5PathPickerDialog.getPath(
            self,
            self.tr("Change Directory"),
            self.tr("Select Directory"),
            E5PathPickerModes.DirectoryShowFilesMode,
            path=cwdWidget.text(),
            defaultDirectory=cwdWidget.text(),
        )
        if ok and dirPath:
            if not os.path.isabs(dirPath):
                dirPath = os.path.join(cwdWidget.text(), dirPath)
            cwdWidget.setText(dirPath)
            self.__listLocalFiles(dirPath, localDevice=localDevice)
    
    @pyqtSlot()
    def __createLocalDirectory(self, localDevice=False):
        """
        Private slot to create a local directory.
        
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if localDevice:
            cwdWidget = self.deviceCwd
        else:
            cwdWidget = self.localCwd
        
        dirPath, ok = QInputDialog.getText(
            self,
            self.tr("Create Directory"),
            self.tr("Enter directory name:"),
            QLineEdit.EchoMode.Normal)
        if ok and dirPath:
            dirPath = os.path.join(cwdWidget.text(), dirPath)
            try:
                os.mkdir(dirPath)
                self.__listLocalFiles(cwdWidget.text(),
                                      localDevice=localDevice)
            except OSError as exc:
                E5MessageBox.critical(
                    self,
                    self.tr("Create Directory"),
                    self.tr("""<p>The directory <b>{0}</b> could not be"""
                            """ created.</p><p>Reason: {1}</p>""").format(
                        dirPath, str(exc))
                )
    
    @pyqtSlot()
    def __deleteLocalDirectoryTree(self, localDevice=False):
        """
        Private slot to delete a local directory tree.
        
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if localDevice:
            cwdWidget = self.deviceCwd
            fileTreeWidget = self.deviceFileTreeWidget
        else:
            cwdWidget = self.localCwd
            fileTreeWidget = self.localFileTreeWidget
        
        if bool(len(fileTreeWidget.selectedItems())):
            name = fileTreeWidget.selectedItems()[0].text(0)
            dirname = os.path.join(cwdWidget.text(), name[:-1])
            dlg = DeleteFilesConfirmationDialog(
                self,
                self.tr("Delete Directory Tree"),
                self.tr(
                    "Do you really want to delete this directory tree?"),
                [dirname])
            if dlg.exec() == QDialog.DialogCode.Accepted:
                try:
                    shutil.rmtree(dirname)
                    self.__listLocalFiles(cwdWidget.text(),
                                          localDevice=localDevice)
                except Exception as exc:
                    E5MessageBox.critical(
                        self,
                        self.tr("Delete Directory Tree"),
                        self.tr("""<p>The directory <b>{0}</b> could not be"""
                                """ deleted.</p><p>Reason: {1}</p>""").format(
                            dirname, str(exc))
                    )
    
    @pyqtSlot()
    def __deleteLocalFile(self, localDevice=False):
        """
        Private slot to delete a local file.
        
        @param localDevice flag indicating device access via local file system
        @type bool
        """
        if localDevice:
            cwdWidget = self.deviceCwd
            fileTreeWidget = self.deviceFileTreeWidget
        else:
            cwdWidget = self.localCwd
            fileTreeWidget = self.localFileTreeWidget
        
        if bool(len(fileTreeWidget.selectedItems())):
            name = fileTreeWidget.selectedItems()[0].text(0)
            filename = os.path.join(cwdWidget.text(), name)
            dlg = DeleteFilesConfirmationDialog(
                self,
                self.tr("Delete File"),
                self.tr(
                    "Do you really want to delete this file?"),
                [filename])
            if dlg.exec() == QDialog.DialogCode.Accepted:
                try:
                    os.remove(filename)
                    self.__listLocalFiles(cwdWidget.text(),
                                          localDevice=localDevice)
                except OSError as exc:
                    E5MessageBox.critical(
                        self,
                        self.tr("Delete File"),
                        self.tr("""<p>The file <b>{0}</b> could not be"""
                                """ deleted.</p><p>Reason: {1}</p>""").format(
                            filename, str(exc))
                    )
    
    @pyqtSlot(bool)
    def __localHiddenChanged(self, checked):
        """
        Private slot handling a change of the local show hidden menu entry.
        
        @param checked new check state of the action
        @type bool
        """
        Preferences.setMicroPython("ShowHiddenLocal", checked)
        self.on_localReloadButton_clicked()
    
    ##################################################################
    ## Context menu methods for the device files below
    ##################################################################
    
    @pyqtSlot(QPoint)
    def __showDeviceContextMenu(self, pos):
        """
        Private slot to show the REPL context menu.
        
        @param pos position to show the menu at
        @type QPoint
        """
        hasSelection = bool(len(self.deviceFileTreeWidget.selectedItems()))
        if hasSelection:
            name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
            isDir = name.endswith("/")
            isFile = not isDir
        else:
            isDir = False
            isFile = False
        if not self.__repl.isMicrobit():
            if not self.__deviceWithLocalAccess:
                self.__devDelDirAct.setEnabled(isDir)
            self.__devDelDirTreeAct.setEnabled(isDir)
        self.__devDelFileAct.setEnabled(isFile)
        
        self.__deviceMenu.exec(self.deviceFileTreeWidget.mapToGlobal(pos))
    
    @pyqtSlot()
    def __changeDeviceDirectory(self):
        """
        Private slot to change the current directory of the device.
        
        Note: This triggers a re-population of the device list for the new
        current directory.
        """
        if self.__deviceWithLocalAccess:
            self.__changeLocalDirectory(True)
        else:
            dirPath, ok = QInputDialog.getText(
                self,
                self.tr("Change Directory"),
                self.tr("Enter the directory path on the device:"),
                QLineEdit.EchoMode.Normal,
                self.deviceCwd.text())
            if ok and dirPath:
                if not dirPath.startswith("/"):
                    dirPath = self.deviceCwd.text() + "/" + dirPath
                self.__fileManager.cd(dirPath)
    
    @pyqtSlot()
    def __createDeviceDirectory(self):
        """
        Private slot to create a directory on the device.
        """
        if self.__deviceWithLocalAccess:
            self.__createLocalDirectory(True)
        else:
            dirPath, ok = QInputDialog.getText(
                self,
                self.tr("Create Directory"),
                self.tr("Enter directory name:"),
                QLineEdit.EchoMode.Normal)
            if ok and dirPath:
                self.__fileManager.mkdir(dirPath)
    
    @pyqtSlot()
    def __deleteDeviceDirectory(self):
        """
        Private slot to delete an empty directory on the device.
        """
        if self.__deviceWithLocalAccess:
            self.__deleteLocalDirectoryTree(True)
        else:
            if bool(len(self.deviceFileTreeWidget.selectedItems())):
                name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
                cwd = self.deviceCwd.text()
                if cwd:
                    if cwd != "/":
                        dirname = cwd + "/" + name[:-1]
                    else:
                        dirname = "/" + name[:-1]
                else:
                    dirname = name[:-1]
                dlg = DeleteFilesConfirmationDialog(
                    self,
                    self.tr("Delete Directory"),
                    self.tr(
                        "Do you really want to delete this directory?"),
                    [dirname])
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self.__fileManager.rmdir(dirname)
    
    @pyqtSlot()
    def __deleteDeviceDirectoryTree(self):
        """
        Private slot to delete a directory and all its subdirectories
        recursively.
        """
        if self.__deviceWithLocalAccess:
            self.__deleteLocalDirectoryTree(True)
        else:
            if bool(len(self.deviceFileTreeWidget.selectedItems())):
                name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
                cwd = self.deviceCwd.text()
                if cwd:
                    if cwd != "/":
                        dirname = cwd + "/" + name[:-1]
                    else:
                        dirname = "/" + name[:-1]
                else:
                    dirname = name[:-1]
                dlg = DeleteFilesConfirmationDialog(
                    self,
                    self.tr("Delete Directory Tree"),
                    self.tr(
                        "Do you really want to delete this directory tree?"),
                    [dirname])
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self.__fileManager.rmdir(dirname, recursive=True)
    
    @pyqtSlot()
    def __deleteDeviceFile(self):
        """
        Private slot to delete a file.
        """
        if self.__deviceWithLocalAccess:
            self.__deleteLocalFile(True)
        else:
            if bool(len(self.deviceFileTreeWidget.selectedItems())):
                name = self.deviceFileTreeWidget.selectedItems()[0].text(0)
                dirname = self.deviceCwd.text()
                if dirname:
                    if dirname != "/":
                        filename = dirname + "/" + name
                    else:
                        filename = "/" + name
                else:
                    filename = name
                dlg = DeleteFilesConfirmationDialog(
                    self,
                    self.tr("Delete File"),
                    self.tr(
                        "Do you really want to delete this file?"),
                    [filename])
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    self.__fileManager.delete(filename)
    
    @pyqtSlot(bool)
    def __deviceHiddenChanged(self, checked):
        """
        Private slot handling a change of the device show hidden menu entry.
        
        @param checked new check state of the action
        @type bool
        """
        Preferences.setMicroPython("ShowHiddenDevice", checked)
        self.on_deviceReloadButton_clicked()
    
    @pyqtSlot()
    def __showFileSystemInfo(self):
        """
        Private slot to show some file system information.
        """
        self.__fileManager.fileSystemInfo()
    
    @pyqtSlot(tuple)
    def __fsInfoResultReceived(self, fsinfo):
        """
        Private slot to show the file system information of the device.
        
        @param fsinfo tuple of tuples containing the file system name, the
            total size, the used size and the free size
        @type tuple of tuples of (str, int, int, int)
        """
        msg = self.tr("<h3>Filesystem Information</h3>")
        for name, totalSize, usedSize, freeSize in fsinfo:
            msg += self.tr(
                "<h4>{0}</h4"
                "<table>"
                "<tr><td>Total Size: </td><td align='right'>{1}</td></tr>"
                "<tr><td>Used Size: </td><td align='right'>{2}</td></tr>"
                "<tr><td>Free Size: </td><td align='right'>{3}</td></tr>"
                "</table>"
            ).format(name,
                     Globals.dataString(totalSize),
                     Globals.dataString(usedSize),
                     Globals.dataString(freeSize),
                     )
        E5MessageBox.information(
            self,
            self.tr("Filesystem Information"),
            msg)
