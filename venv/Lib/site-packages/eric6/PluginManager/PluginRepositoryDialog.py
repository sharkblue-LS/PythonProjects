# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog showing the available plugins.
"""

import sys
import os
import zipfile
import glob
import re

from PyQt5.QtCore import (
    pyqtSignal, pyqtSlot, Qt, QFile, QIODevice, QUrl, QProcess, QPoint,
    QCoreApplication
)
from PyQt5.QtWidgets import (
    QWidget, QDialogButtonBox, QAbstractButton, QTreeWidgetItem, QDialog,
    QVBoxLayout, QMenu
)
from PyQt5.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)

from .Ui_PluginRepositoryDialog import Ui_PluginRepositoryDialog

from E5Gui import E5MessageBox
from E5Gui.E5MainWindow import E5MainWindow
from E5Gui.E5Application import e5App

from E5Network.E5NetworkProxyFactory import proxyAuthenticationRequired
try:
    from E5Network.E5SslErrorHandler import E5SslErrorHandler
    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

import Globals
import Utilities
import Preferences

import UI.PixmapCache

from eric6config import getConfig


class PluginRepositoryWidget(QWidget, Ui_PluginRepositoryDialog):
    """
    Class implementing a dialog showing the available plugins.
    
    @signal closeAndInstall() emitted when the Close & Install button is
        pressed
    """
    closeAndInstall = pyqtSignal()
    
    DescrRole = Qt.ItemDataRole.UserRole
    UrlRole = Qt.ItemDataRole.UserRole + 1
    FilenameRole = Qt.ItemDataRole.UserRole + 2
    AuthorRole = Qt.ItemDataRole.UserRole + 3

    PluginStatusUpToDate = 0
    PluginStatusNew = 1
    PluginStatusLocalUpdate = 2
    PluginStatusRemoteUpdate = 3
    PluginStatusError = 4
    
    def __init__(self, pluginManager, parent=None):
        """
        Constructor
        
        @param pluginManager reference to the plugin manager object
        @type PluginManager
        @param parent parent of this dialog
        @type QWidget
        """
        super(PluginRepositoryWidget, self).__init__(parent)
        self.setupUi(self)
        
        if pluginManager is None:
            # started as external plug-in repository dialog
            from .PluginManager import PluginManager
            self.__pluginManager = PluginManager()
            self.__external = True
        else:
            self.__pluginManager = pluginManager
            self.__external = False
        
        self.__updateButton = self.buttonBox.addButton(
            self.tr("Update"), QDialogButtonBox.ButtonRole.ActionRole)
        self.__downloadButton = self.buttonBox.addButton(
            self.tr("Download"), QDialogButtonBox.ButtonRole.ActionRole)
        self.__downloadButton.setEnabled(False)
        self.__downloadInstallButton = self.buttonBox.addButton(
            self.tr("Download && Install"),
            QDialogButtonBox.ButtonRole.ActionRole)
        self.__downloadInstallButton.setEnabled(False)
        self.__downloadCancelButton = self.buttonBox.addButton(
            self.tr("Cancel"), QDialogButtonBox.ButtonRole.ActionRole)
        self.__downloadCancelButton.setEnabled(False)
        self.__installButton = self.buttonBox.addButton(
            self.tr("Close && Install"),
            QDialogButtonBox.ButtonRole.ActionRole)
        self.__installButton.setEnabled(False)
        self.__closeButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close)
        self.__closeButton.setEnabled(True)
        
        self.repositoryUrlEdit.setText(
            Preferences.getUI("PluginRepositoryUrl6"))
        
        self.repositoryList.headerItem().setText(
            self.repositoryList.columnCount(), "")
        self.repositoryList.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder)
        
        self.__pluginContextMenu = QMenu(self)
        self.__hideAct = self.__pluginContextMenu.addAction(
            self.tr("Hide"), self.__hidePlugin)
        self.__hideSelectedAct = self.__pluginContextMenu.addAction(
            self.tr("Hide Selected"), self.__hideSelectedPlugins)
        self.__pluginContextMenu.addSeparator()
        self.__showAllAct = self.__pluginContextMenu.addAction(
            self.tr("Show All"), self.__showAllPlugins)
        self.__pluginContextMenu.addSeparator()
        self.__pluginContextMenu.addAction(
            self.tr("Cleanup Downloads"), self.__cleanupDownloads)
        
        self.pluginRepositoryFile = os.path.join(Utilities.getConfigDir(),
                                                 "PluginRepository")
        
        # attributes for the network objects
        self.__networkManager = QNetworkAccessManager(self)
        self.__networkManager.proxyAuthenticationRequired.connect(
            proxyAuthenticationRequired)
        if SSL_AVAILABLE:
            self.__sslErrorHandler = E5SslErrorHandler(self)
            self.__networkManager.sslErrors.connect(self.__sslErrors)
        self.__replies = []
        
        self.__pluginsToDownload = []
        self.__pluginsDownloaded = []
        self.__isDownloadInstall = False
        self.__allDownloadedOk = False
        
        self.__hiddenPlugins = Preferences.getPluginManager("HiddenPlugins")
        
        self.__populateList()
    
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Private slot to handle the click of a button of the button box.
        
        @param button reference to the button pressed (QAbstractButton)
        """
        if button == self.__updateButton:
            self.__updateList()
        elif button == self.__downloadButton:
            self.__isDownloadInstall = False
            self.__downloadPlugins()
        elif button == self.__downloadInstallButton:
            self.__isDownloadInstall = True
            self.__allDownloadedOk = True
            self.__downloadPlugins()
        elif button == self.__downloadCancelButton:
            self.__downloadCancel()
        elif button == self.__installButton:
            self.__closeAndInstall()
    
    def __formatDescription(self, lines):
        """
        Private method to format the description.
        
        @param lines lines of the description (list of strings)
        @return formatted description (string)
        """
        # remove empty line at start and end
        newlines = lines[:]
        if len(newlines) and newlines[0] == '':
            del newlines[0]
        if len(newlines) and newlines[-1] == '':
            del newlines[-1]
        
        # replace empty lines by newline character
        index = 0
        while index < len(newlines):
            if newlines[index] == '':
                newlines[index] = '\n'
            index += 1
        
        # join lines by a blank
        return ' '.join(newlines)
    
    def __changeScheme(self, url, newScheme=""):
        """
        Private method to change the scheme of the given URL.
        
        @param url URL to be modified
        @type str
        @param newScheme scheme to be set for the given URL
        @return modified URL
        @rtype str
        """
        if not newScheme:
            newScheme = self.repositoryUrlEdit.text().split("//", 1)[0]
        
        return newScheme + "//" + url.split("//", 1)[1]
    
    @pyqtSlot(QPoint)
    def on_repositoryList_customContextMenuRequested(self, pos):
        """
        Private slot to show the context menu.
        
        @param pos position to show the menu (QPoint)
        """
        self.__hideAct.setEnabled(
            self.repositoryList.currentItem() is not None and
            len(self.__selectedItems()) == 1)
        self.__hideSelectedAct.setEnabled(
            len(self.__selectedItems()) > 1)
        self.__showAllAct.setEnabled(bool(self.__hasHiddenPlugins()))
        self.__pluginContextMenu.popup(self.repositoryList.mapToGlobal(pos))
    
    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem)
    def on_repositoryList_currentItemChanged(self, current, previous):
        """
        Private slot to handle the change of the current item.
        
        @param current reference to the new current item (QTreeWidgetItem)
        @param previous reference to the old current item (QTreeWidgetItem)
        """
        if self.__repositoryMissing or current is None:
            return
        
        url = current.data(0, PluginRepositoryWidget.UrlRole)
        if url is None:
            url = ""
        else:
            url = self.__changeScheme(url)
        self.urlEdit.setText(url)
        self.descriptionEdit.setPlainText(
            current.data(0, PluginRepositoryWidget.DescrRole) and
            self.__formatDescription(
                current.data(0, PluginRepositoryWidget.DescrRole)) or "")
        self.authorEdit.setText(
            current.data(0, PluginRepositoryWidget.AuthorRole) or "")
    
    def __selectedItems(self):
        """
        Private method to get all selected items without the toplevel ones.
        
        @return list of selected items (list)
        """
        ql = self.repositoryList.selectedItems()
        for index in range(self.repositoryList.topLevelItemCount()):
            ti = self.repositoryList.topLevelItem(index)
            if ti in ql:
                ql.remove(ti)
        return ql
    
    @pyqtSlot()
    def on_repositoryList_itemSelectionChanged(self):
        """
        Private slot to handle a change of the selection.
        """
        enable = bool(self.__selectedItems())
        self.__downloadButton.setEnabled(enable)
        self.__downloadInstallButton.setEnabled(enable)
        self.__installButton.setEnabled(enable)
    
    def __updateList(self):
        """
        Private slot to download a new list and display the contents.
        """
        url = self.repositoryUrlEdit.text()
        self.__downloadFile(url,
                            self.pluginRepositoryFile,
                            self.__downloadRepositoryFileDone)
    
    def __downloadRepositoryFileDone(self, status, filename):
        """
        Private method called after the repository file was downloaded.
        
        @param status flaging indicating a successful download (boolean)
        @param filename full path of the downloaded file (string)
        """
        self.__populateList()
    
    def __downloadPluginDone(self, status, filename):
        """
        Private method called, when the download of a plugin is finished.
        
        @param status flag indicating a successful download (boolean)
        @param filename full path of the downloaded file (string)
        """
        if status:
            self.__pluginsDownloaded.append(filename)
        if self.__isDownloadInstall:
            self.__allDownloadedOk &= status
        
        self.__pluginsToDownload.pop(0)
        if len(self.__pluginsToDownload):
            self.__downloadPlugin()
        else:
            self.__downloadPluginsDone()
    
    def __downloadPlugin(self):
        """
        Private method to download the next plugin.
        """
        self.__downloadFile(self.__pluginsToDownload[0][0],
                            self.__pluginsToDownload[0][1],
                            self.__downloadPluginDone)
    
    def __downloadPlugins(self):
        """
        Private slot to download the selected plugins.
        """
        self.__pluginsDownloaded = []
        self.__pluginsToDownload = []
        self.__downloadButton.setEnabled(False)
        self.__downloadInstallButton.setEnabled(False)
        self.__installButton.setEnabled(False)
        
        newScheme = self.repositoryUrlEdit.text().split("//", 1)[0]
        for itm in self.repositoryList.selectedItems():
            if itm not in [self.__stableItem, self.__unstableItem,
                           self.__unknownItem, self.__obsoleteItem]:
                url = self.__changeScheme(
                    itm.data(0, PluginRepositoryWidget.UrlRole),
                    newScheme)
                filename = os.path.join(
                    Preferences.getPluginManager("DownloadPath"),
                    itm.data(0, PluginRepositoryWidget.FilenameRole))
                self.__pluginsToDownload.append((url, filename))
        self.__downloadPlugin()
    
    def __downloadPluginsDone(self):
        """
        Private method called, when the download of the plugins is finished.
        """
        self.__downloadButton.setEnabled(len(self.__selectedItems()))
        self.__downloadInstallButton.setEnabled(len(self.__selectedItems()))
        self.__installButton.setEnabled(len(self.__selectedItems()))
        if not self.__external:
            ui = e5App().getObject("UserInterface")
        else:
            ui = None
        if ui is not None:
            ui.showNotification(
                UI.PixmapCache.getPixmap("plugin48"),
                self.tr("Download Plugin Files"),
                self.tr("""The requested plugins were downloaded."""))
        
        if self.__isDownloadInstall:
            self.closeAndInstall.emit()
        else:
            if ui is None:
                E5MessageBox.information(
                    self,
                    self.tr("Download Plugin Files"),
                    self.tr("""The requested plugins were downloaded."""))
            
            self.downloadProgress.setValue(0)
            
            # repopulate the list to update the refresh icons
            self.__populateList()
    
    def __resortRepositoryList(self):
        """
        Private method to resort the tree.
        """
        self.repositoryList.sortItems(
            self.repositoryList.sortColumn(),
            self.repositoryList.header().sortIndicatorOrder())
    
    def __populateList(self):
        """
        Private method to populate the list of available plugins.
        """
        self.repositoryList.clear()
        self.__stableItem = None
        self.__unstableItem = None
        self.__unknownItem = None
        self.__obsoleteItem = None
        
        self.__newItems = 0
        self.__updateLocalItems = 0
        self.__updateRemoteItems = 0
        
        self.downloadProgress.setValue(0)
        
        if os.path.exists(self.pluginRepositoryFile):
            self.__repositoryMissing = False
            f = QFile(self.pluginRepositoryFile)
            if f.open(QIODevice.OpenModeFlag.ReadOnly):
                from E5XML.PluginRepositoryReader import PluginRepositoryReader
                reader = PluginRepositoryReader(f, self.addEntry)
                reader.readXML()
                self.repositoryList.resizeColumnToContents(0)
                self.repositoryList.resizeColumnToContents(1)
                self.repositoryList.resizeColumnToContents(2)
                self.__resortRepositoryList()
                url = Preferences.getUI("PluginRepositoryUrl6")
                if url != self.repositoryUrlEdit.text():
                    self.repositoryUrlEdit.setText(url)
                    E5MessageBox.warning(
                        self,
                        self.tr("Plugins Repository URL Changed"),
                        self.tr(
                            """The URL of the Plugins Repository has"""
                            """ changed. Select the "Update" button to get"""
                            """ the new repository file."""))
            else:
                E5MessageBox.critical(
                    self,
                    self.tr("Read plugins repository file"),
                    self.tr("<p>The plugins repository file <b>{0}</b> "
                            "could not be read. Select Update</p>")
                    .format(self.pluginRepositoryFile))
        else:
            self.__repositoryMissing = True
            QTreeWidgetItem(
                self.repositoryList,
                ["", self.tr(
                    "No plugin repository file available.\nSelect Update.")
                 ])
            self.repositoryList.resizeColumnToContents(1)
        
        self.newLabel.setText(self.tr("New: <b>{0}</b>")
                              .format(self.__newItems))
        self.updateLocalLabel.setText(self.tr("Local Updates: <b>{0}</b>")
                                      .format(self.__updateLocalItems))
        self.updateRemoteLabel.setText(self.tr("Remote Updates: <b>{0}</b>")
                                       .format(self.__updateRemoteItems))
    
    def __downloadFile(self, url, filename, doneMethod=None):
        """
        Private slot to download the given file.
        
        @param url URL for the download (string)
        @param filename local name of the file (string)
        @param doneMethod method to be called when done
        """
        self.__updateButton.setEnabled(False)
        self.__downloadButton.setEnabled(False)
        self.__downloadInstallButton.setEnabled(False)
        self.__closeButton.setEnabled(False)
        self.__downloadCancelButton.setEnabled(True)
        
        self.statusLabel.setText(url)
        
        request = QNetworkRequest(QUrl(url))
        request.setAttribute(
            QNetworkRequest.Attribute.CacheLoadControlAttribute,
            QNetworkRequest.CacheLoadControl.AlwaysNetwork)
        reply = self.__networkManager.get(request)
        reply.finished.connect(
            lambda: self.__downloadFileDone(reply, filename, doneMethod))
        reply.downloadProgress.connect(self.__downloadProgress)
        self.__replies.append(reply)
    
    def __downloadFileDone(self, reply, fileName, doneMethod):
        """
        Private method called, after the file has been downloaded
        from the Internet.
        
        @param reply reference to the reply object of the download
        @type QNetworkReply
        @param fileName local name of the file
        @type str
        @param doneMethod method to be called when done
        @type func
        """
        self.__updateButton.setEnabled(True)
        self.__closeButton.setEnabled(True)
        self.__downloadCancelButton.setEnabled(False)
        
        ok = True
        if reply in self.__replies:
            self.__replies.remove(reply)
        if reply.error() != QNetworkReply.NetworkError.NoError:
            ok = False
            if (
                reply.error() !=
                QNetworkReply.NetworkError.OperationCanceledError
            ):
                E5MessageBox.warning(
                    self,
                    self.tr("Error downloading file"),
                    self.tr(
                        """<p>Could not download the requested file"""
                        """ from {0}.</p><p>Error: {1}</p>"""
                    ).format(reply.url().toString(), reply.errorString())
                )
            self.downloadProgress.setValue(0)
            if self.repositoryList.topLevelItemCount():
                if self.repositoryList.currentItem() is None:
                    self.repositoryList.setCurrentItem(
                        self.repositoryList.topLevelItem(0))
                else:
                    self.__downloadButton.setEnabled(
                        len(self.__selectedItems()))
                    self.__downloadInstallButton.setEnabled(
                        len(self.__selectedItems()))
            reply.deleteLater()
            return
        
        downloadIODevice = QFile(fileName + ".tmp")
        downloadIODevice.open(QIODevice.OpenModeFlag.WriteOnly)
        # read data in chunks
        chunkSize = 64 * 1024 * 1024
        while True:
            data = reply.read(chunkSize)
            if data is None or len(data) == 0:
                break
            downloadIODevice.write(data)
        downloadIODevice.close()
        if QFile.exists(fileName):
            QFile.remove(fileName)
        downloadIODevice.rename(fileName)
        reply.deleteLater()
        
        if doneMethod is not None:
            doneMethod(ok, fileName)
    
    def __downloadCancel(self, reply=None):
        """
        Private slot to cancel the current download.
        
        @param reply reference to the network reply
        @type QNetworkReply
        """
        if reply is None:
            if self.__replies:
                reply = self.__replies[0]
        self.__pluginsToDownload = []
        if reply is not None:
            reply.abort()
    
    def __downloadProgress(self, done, total):
        """
        Private slot to show the download progress.
        
        @param done number of bytes downloaded so far (integer)
        @param total total bytes to be downloaded (integer)
        """
        if total:
            self.downloadProgress.setMaximum(total)
            self.downloadProgress.setValue(done)
    
    def addEntry(self, name, short, description, url, author, version,
                 filename, status):
        """
        Public method to add an entry to the list.
        
        @param name data for the name field (string)
        @param short data for the short field (string)
        @param description data for the description field (list of strings)
        @param url data for the url field (string)
        @param author data for the author field (string)
        @param version data for the version field (string)
        @param filename data for the filename field (string)
        @param status status of the plugin (string [stable, unstable, unknown])
        """
        pluginName = filename.rsplit("-", 1)[0]
        if pluginName in self.__hiddenPlugins:
            return
        
        if status == "stable":
            if self.__stableItem is None:
                self.__stableItem = QTreeWidgetItem(
                    self.repositoryList, [self.tr("Stable")])
                self.__stableItem.setExpanded(True)
            parent = self.__stableItem
        elif status == "unstable":
            if self.__unstableItem is None:
                self.__unstableItem = QTreeWidgetItem(
                    self.repositoryList, [self.tr("Unstable")])
                self.__unstableItem.setExpanded(True)
            parent = self.__unstableItem
        elif status == "obsolete":
            if self.__obsoleteItem is None:
                self.__obsoleteItem = QTreeWidgetItem(
                    self.repositoryList, [self.tr("Obsolete")])
                self.__obsoleteItem.setExpanded(True)
            parent = self.__obsoleteItem
        else:
            if self.__unknownItem is None:
                self.__unknownItem = QTreeWidgetItem(
                    self.repositoryList, [self.tr("Unknown")])
                self.__unknownItem.setExpanded(True)
            parent = self.__unknownItem
        itm = QTreeWidgetItem(parent, [name, version, short])
        
        itm.setData(0, PluginRepositoryWidget.UrlRole, url)
        itm.setData(0, PluginRepositoryWidget.FilenameRole, filename)
        itm.setData(0, PluginRepositoryWidget.AuthorRole, author)
        itm.setData(0, PluginRepositoryWidget.DescrRole, description)
        
        updateStatus = self.__updateStatus(filename, version)
        if updateStatus == PluginRepositoryWidget.PluginStatusUpToDate:
            itm.setIcon(1, UI.PixmapCache.getIcon("empty"))
            itm.setToolTip(1, self.tr("up-to-date"))
        elif updateStatus == PluginRepositoryWidget.PluginStatusNew:
            itm.setIcon(1, UI.PixmapCache.getIcon("download"))
            itm.setToolTip(1, self.tr("new download available"))
            self.__newItems += 1
        elif updateStatus == PluginRepositoryWidget.PluginStatusLocalUpdate:
            itm.setIcon(1, UI.PixmapCache.getIcon("updateLocal"))
            itm.setToolTip(1, self.tr("update installable"))
            self.__updateLocalItems += 1
        elif updateStatus == PluginRepositoryWidget.PluginStatusRemoteUpdate:
            itm.setIcon(1, UI.PixmapCache.getIcon("updateRemote"))
            itm.setToolTip(1, self.tr("updated download available"))
            self.__updateRemoteItems += 1
        elif updateStatus == PluginRepositoryWidget.PluginStatusError:
            itm.setIcon(1, UI.PixmapCache.getIcon("warning"))
            itm.setToolTip(1, self.tr("error determining status"))
    
    def __updateStatus(self, filename, version):
        """
        Private method to check the given archive update status.
        
        @param filename data for the filename field (string)
        @param version data for the version field (string)
        @return plug-in update status (integer, one of PluginStatusNew,
            PluginStatusUpToDate, PluginStatusLocalUpdate,
            PluginStatusRemoteUpdate)
        """
        archive = os.path.join(Preferences.getPluginManager("DownloadPath"),
                               filename)
        
        # check, if it is an update (i.e. we already have archives
        # with the same pattern)
        archivesPattern = archive.rsplit('-', 1)[0] + "-*.zip"
        if len(glob.glob(archivesPattern)) == 0:
            # Check against installed/loaded plug-ins
            pluginName = filename.rsplit('-', 1)[0]
            pluginDetails = self.__pluginManager.getPluginDetails(pluginName)
            if (
                pluginDetails is None or
                pluginDetails["moduleName"] != pluginName
            ):
                return PluginRepositoryWidget.PluginStatusNew
            if pluginDetails["error"]:
                return PluginRepositoryWidget.PluginStatusError
            pluginVersionTuple = Globals.versionToTuple(
                pluginDetails["version"])[:3]
            versionTuple = Globals.versionToTuple(version)[:3]
            if pluginVersionTuple < versionTuple:
                return PluginRepositoryWidget.PluginStatusRemoteUpdate
            else:
                return PluginRepositoryWidget.PluginStatusUpToDate
        
        # check, if the archive exists
        if not os.path.exists(archive):
            return PluginRepositoryWidget.PluginStatusRemoteUpdate
        
        # check, if the archive is a valid zip file
        if not zipfile.is_zipfile(archive):
            return PluginRepositoryWidget.PluginStatusRemoteUpdate
        
        zipFile = zipfile.ZipFile(archive, "r")
        try:
            aversion = zipFile.read("VERSION").decode("utf-8")
        except KeyError:
            aversion = ""
        zipFile.close()
        
        if aversion == version:
            # Check against installed/loaded plug-ins
            pluginName = filename.rsplit('-', 1)[0]
            pluginDetails = self.__pluginManager.getPluginDetails(pluginName)
            if pluginDetails is None:
                return PluginRepositoryWidget.PluginStatusLocalUpdate
            if (
                Globals.versionToTuple(pluginDetails["version"])[:3] <
                Globals.versionToTuple(version)[:3]
            ):
                return PluginRepositoryWidget.PluginStatusLocalUpdate
            else:
                return PluginRepositoryWidget.PluginStatusUpToDate
        else:
            return PluginRepositoryWidget.PluginStatusRemoteUpdate
    
    def __sslErrors(self, reply, errors):
        """
        Private slot to handle SSL errors.
        
        @param reply reference to the reply object (QNetworkReply)
        @param errors list of SSL errors (list of QSslError)
        """
        ignored = self.__sslErrorHandler.sslErrorsReply(reply, errors)[0]
        if ignored == E5SslErrorHandler.NotIgnored:
            self.__downloadCancel(reply)
    
    def getDownloadedPlugins(self):
        """
        Public method to get the list of recently downloaded plugin files.
        
        @return list of plugin filenames (list of strings)
        """
        return self.__pluginsDownloaded
    
    @pyqtSlot(bool)
    def on_repositoryUrlEditButton_toggled(self, checked):
        """
        Private slot to set the read only status of the repository URL line
        edit.
        
        @param checked state of the push button (boolean)
        """
        self.repositoryUrlEdit.setReadOnly(not checked)
    
    def __closeAndInstall(self):
        """
        Private method to close the dialog and invoke the install dialog.
        """
        if not self.__pluginsDownloaded and self.__selectedItems():
            for itm in self.__selectedItems():
                filename = os.path.join(
                    Preferences.getPluginManager("DownloadPath"),
                    itm.data(0, PluginRepositoryWidget.FilenameRole))
                self.__pluginsDownloaded.append(filename)
        self.closeAndInstall.emit()
    
    def __hidePlugin(self):
        """
        Private slot to hide the current plug-in.
        """
        itm = self.__selectedItems()[0]
        pluginName = (itm.data(0, PluginRepositoryWidget.FilenameRole)
                      .rsplit("-", 1)[0])
        self.__updateHiddenPluginsList([pluginName])
    
    def __hideSelectedPlugins(self):
        """
        Private slot to hide all selected plug-ins.
        """
        hideList = []
        for itm in self.__selectedItems():
            pluginName = (itm.data(0, PluginRepositoryWidget.FilenameRole)
                          .rsplit("-", 1)[0])
            hideList.append(pluginName)
        self.__updateHiddenPluginsList(hideList)
    
    def __showAllPlugins(self):
        """
        Private slot to show all plug-ins.
        """
        self.__hiddenPlugins = []
        self.__updateHiddenPluginsList([])
    
    def __hasHiddenPlugins(self):
        """
        Private method to check, if there are any hidden plug-ins.
        
        @return flag indicating the presence of hidden plug-ins (boolean)
        """
        return bool(self.__hiddenPlugins)
    
    def __updateHiddenPluginsList(self, hideList):
        """
        Private method to store the list of hidden plug-ins to the settings.
        
        @param hideList list of plug-ins to add to the list of hidden ones
            (list of string)
        """
        if hideList:
            self.__hiddenPlugins.extend(
                [p for p in hideList if p not in self.__hiddenPlugins])
        Preferences.setPluginManager("HiddenPlugins", self.__hiddenPlugins)
        self.__populateList()
    
    def __cleanupDownloads(self):
        """
        Private slot to cleanup the plug-in downloads area.
        """
        PluginRepositoryDownloadCleanup()


class PluginRepositoryDialog(QDialog):
    """
    Class for the dialog variant.
    """
    def __init__(self, pluginManager, parent=None):
        """
        Constructor
        
        @param pluginManager reference to the plugin manager object
        @type PluginManager
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PluginRepositoryDialog, self).__init__(parent)
        self.setSizeGripEnabled(True)
        
        self.__layout = QVBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)
        
        self.cw = PluginRepositoryWidget(pluginManager, self)
        size = self.cw.size()
        self.__layout.addWidget(self.cw)
        self.resize(size)
        self.setWindowTitle(self.cw.windowTitle())
        
        self.cw.buttonBox.accepted.connect(self.accept)
        self.cw.buttonBox.rejected.connect(self.reject)
        self.cw.closeAndInstall.connect(self.__closeAndInstall)
        
    def __closeAndInstall(self):
        """
        Private slot to handle the closeAndInstall signal.
        """
        self.done(QDialog.DialogCode.Accepted + 1)
    
    def getDownloadedPlugins(self):
        """
        Public method to get the list of recently downloaded plugin files.
        
        @return list of plugin filenames (list of strings)
        """
        return self.cw.getDownloadedPlugins()


class PluginRepositoryWindow(E5MainWindow):
    """
    Main window class for the standalone dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(PluginRepositoryWindow, self).__init__(parent)
        self.cw = PluginRepositoryWidget(None, self)
        size = self.cw.size()
        self.setCentralWidget(self.cw)
        self.resize(size)
        self.setWindowTitle(self.cw.windowTitle())
        
        self.setStyle(Preferences.getUI("Style"),
                      Preferences.getUI("StyleSheet"))
        
        self.cw.buttonBox.accepted.connect(self.close)
        self.cw.buttonBox.rejected.connect(self.close)
        self.cw.closeAndInstall.connect(self.__startPluginInstall)
    
    def __startPluginInstall(self):
        """
        Private slot to start the eric plugin installation dialog.
        """
        proc = QProcess()
        applPath = os.path.join(getConfig("ericDir"), "eric6_plugininstall.py")
        
        args = []
        args.append(applPath)
        args += self.cw.getDownloadedPlugins()
        
        if (
            not os.path.isfile(applPath) or
            not proc.startDetached(sys.executable, args)
        ):
            E5MessageBox.critical(
                self,
                self.tr('Process Generation Error'),
                self.tr(
                    '<p>Could not start the process.<br>'
                    'Ensure that it is available as <b>{0}</b>.</p>'
                ).format(applPath),
                self.tr('OK'))
        
        self.close()


def PluginRepositoryDownloadCleanup(quiet=False):
    """
    Module function to clean up the plug-in downloads area.
    
    @param quiet flag indicating quiet operations
    @type bool
    """
    pluginsRegister = []    # list of plug-ins contained in the repository
    
    def registerPlugin(name, short, description, url, author, version,
                       filename, status):
        """
        Method to register a plug-in's data.
        
        @param name data for the name field (string)
        @param short data for the short field (string)
        @param description data for the description field (list of strings)
        @param url data for the url field (string)
        @param author data for the author field (string)
        @param version data for the version field (string)
        @param filename data for the filename field (string)
        @param status status of the plugin (string [stable, unstable, unknown])
        """
        pluginName = os.path.splitext(url.rsplit("/", 1)[1])[0]
        if pluginName not in pluginsRegister:
            pluginsRegister.append(pluginName)
    
    downloadPath = Preferences.getPluginManager("DownloadPath")
    downloads = {}  # plug-in name as key, file name as value
    
    # step 1: extract plug-ins and downloaded files
    for pluginFile in os.listdir(downloadPath):
        if not os.path.isfile(os.path.join(downloadPath, pluginFile)):
            continue
        
        try:
            pluginName, pluginVersion = (
                pluginFile.replace(".zip", "").rsplit("-", 1)
            )
            pluginVersionList = re.split("[._-]", pluginVersion)
            for index in range(len(pluginVersionList)):
                try:
                    pluginVersionList[index] = int(pluginVersionList[index])
                except ValueError:
                    # use default of 0
                    pluginVersionList[index] = 0
        except ValueError:
            # rsplit() returned just one entry, i.e. file name doesn't contain
            # version info separated by '-'
            # => assume version 0.0.0
            pluginName = pluginFile.replace(".zip", "")
            pluginVersionList = [0, 0, 0]
        
        if pluginName not in downloads:
            downloads[pluginName] = []
        downloads[pluginName].append((pluginFile, tuple(pluginVersionList)))
    
    # step 2: delete old entries
    hiddenPlugins = Preferences.getPluginManager("HiddenPlugins")
    for pluginName in downloads:
        downloads[pluginName].sort(key=lambda x: x[1])
    
        if (
            pluginName in hiddenPlugins and
            not Preferences.getPluginManager("KeepHidden")
        ):
            removeFiles = [f[0] for f in downloads[pluginName]]
        else:
            removeFiles = [f[0] for f in downloads[pluginName][
                :-Preferences.getPluginManager("KeepGenerations")]]
        for removeFile in removeFiles:
            try:
                os.remove(os.path.join(downloadPath, removeFile))
            except OSError as err:
                if not quiet:
                    E5MessageBox.critical(
                        None,
                        QCoreApplication.translate(
                            "PluginRepositoryWidget",
                            "Cleanup of Plugin Downloads"),
                        QCoreApplication.translate(
                            "PluginRepositoryWidget",
                            """<p>The plugin download <b>{0}</b> could"""
                            """ not be deleted.</p><p>Reason: {1}</p>""")
                        .format(removeFile, str(err)))
    
    # step 3: delete entries of obsolete plug-ins
    pluginRepositoryFile = os.path.join(Utilities.getConfigDir(),
                                        "PluginRepository")
    if os.path.exists(pluginRepositoryFile):
        f = QFile(pluginRepositoryFile)
        if f.open(QIODevice.OpenModeFlag.ReadOnly):
            from E5XML.PluginRepositoryReader import PluginRepositoryReader
            reader = PluginRepositoryReader(f, registerPlugin)
            reader.readXML()
            
            for pluginName in downloads:
                if pluginName not in pluginsRegister:
                    removeFiles = [f[0] for f in downloads[pluginName]]
                    for removeFile in removeFiles:
                        try:
                            os.remove(os.path.join(downloadPath, removeFile))
                        except OSError as err:
                            if not quiet:
                                E5MessageBox.critical(
                                    None,
                                    QCoreApplication.translate(
                                        "PluginRepositoryWidget",
                                        "Cleanup of Plugin Downloads"),
                                    QCoreApplication.translate(
                                        "PluginRepositoryWidget",
                                        "<p>The plugin download <b>{0}</b>"
                                        " could not be deleted.</p>"
                                        "<p>Reason: {1}</p>""")
                                    .format(removeFile, str(err)))
