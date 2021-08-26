# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the feature permission dialog.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QDialog, QTreeWidgetItem, QTreeWidget, QAbstractItemView
)
from PyQt5.QtWebEngineWidgets import QWebEnginePage

import UI.PixmapCache

from .Ui_FeaturePermissionsDialog import Ui_FeaturePermissionsDialog


class FeaturePermissionsDialog(QDialog, Ui_FeaturePermissionsDialog):
    """
    Class implementing the feature permission dialog.
    """
    def __init__(self, featurePermissions, parent=None):
        """
        Constructor
        
        @param featurePermissions dictionary with remembered feature
            permissions
        @type dict of dict of list
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FeaturePermissionsDialog, self).__init__(parent)
        self.setupUi(self)
        
        # add the various lists
        
        if hasattr(QWebEnginePage, "Notifications"):
            # this was re-added in Qt 5.13.0
            self.notifList = QTreeWidget()
            self.notifList.setAlternatingRowColors(True)
            self.notifList.setSelectionMode(
                QAbstractItemView.SelectionMode.ExtendedSelection)
            self.notifList.setRootIsDecorated(False)
            self.notifList.setItemsExpandable(False)
            self.notifList.setAllColumnsShowFocus(True)
            self.notifList.setObjectName("notifList")
            self.notifList.setSortingEnabled(True)
            self.notifList.headerItem().setText(0, self.tr("Host"))
            self.notifList.headerItem().setText(1, self.tr("Permission"))
            self.tabWidget.addTab(
                self.notifList,
                UI.PixmapCache.getIcon("notification"),
                self.tr("Notifications"))
        
        self.geoList = QTreeWidget()
        self.geoList.setAlternatingRowColors(True)
        self.geoList.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.geoList.setRootIsDecorated(False)
        self.geoList.setItemsExpandable(False)
        self.geoList.setAllColumnsShowFocus(True)
        self.geoList.setObjectName("geoList")
        self.geoList.setSortingEnabled(True)
        self.geoList.headerItem().setText(0, self.tr("Host"))
        self.geoList.headerItem().setText(1, self.tr("Permission"))
        self.tabWidget.addTab(
            self.geoList,
            UI.PixmapCache.getIcon("geolocation"),
            self.tr("Geolocation"))
        
        self.micList = QTreeWidget()
        self.micList.setAlternatingRowColors(True)
        self.micList.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.micList.setRootIsDecorated(False)
        self.micList.setItemsExpandable(False)
        self.micList.setAllColumnsShowFocus(True)
        self.micList.setObjectName("micList")
        self.micList.setSortingEnabled(True)
        self.micList.headerItem().setText(0, self.tr("Host"))
        self.micList.headerItem().setText(1, self.tr("Permission"))
        self.tabWidget.addTab(
            self.micList,
            UI.PixmapCache.getIcon("audiocapture"),
            self.tr("Microphone"))
        
        self.camList = QTreeWidget()
        self.camList.setAlternatingRowColors(True)
        self.camList.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.camList.setRootIsDecorated(False)
        self.camList.setItemsExpandable(False)
        self.camList.setAllColumnsShowFocus(True)
        self.camList.setObjectName("camList")
        self.camList.setSortingEnabled(True)
        self.camList.headerItem().setText(0, self.tr("Host"))
        self.camList.headerItem().setText(1, self.tr("Permission"))
        self.tabWidget.addTab(
            self.camList,
            UI.PixmapCache.getIcon("camera"),
            self.tr("Camera"))
        
        self.micCamList = QTreeWidget()
        self.micCamList.setAlternatingRowColors(True)
        self.micCamList.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.micCamList.setRootIsDecorated(False)
        self.micCamList.setItemsExpandable(False)
        self.micCamList.setAllColumnsShowFocus(True)
        self.micCamList.setObjectName("micCamList")
        self.micCamList.setSortingEnabled(True)
        self.micCamList.headerItem().setText(0, self.tr("Host"))
        self.micCamList.headerItem().setText(1, self.tr("Permission"))
        self.tabWidget.addTab(
            self.micCamList,
            UI.PixmapCache.getIcon("audio-video"),
            self.tr("Microphone && Camera"))
        
        self.mouseLockList = QTreeWidget()
        self.mouseLockList.setAlternatingRowColors(True)
        self.mouseLockList.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection)
        self.mouseLockList.setRootIsDecorated(False)
        self.mouseLockList.setItemsExpandable(False)
        self.mouseLockList.setAllColumnsShowFocus(True)
        self.mouseLockList.setObjectName("mouseLockList")
        self.mouseLockList.setSortingEnabled(True)
        self.mouseLockList.headerItem().setText(0, self.tr("Host"))
        self.mouseLockList.headerItem().setText(1, self.tr("Permission"))
        self.tabWidget.addTab(
            self.mouseLockList,
            UI.PixmapCache.getIcon("mouse"),
            self.tr("Mouse Lock"))
        
        if hasattr(QWebEnginePage, "DesktopVideoCapture"):
            # these are shown as of Qt 5.10.0/PyQt 5.10.0
            self.deskVidList = QTreeWidget()
            self.deskVidList.setAlternatingRowColors(True)
            self.deskVidList.setSelectionMode(
                QAbstractItemView.SelectionMode.ExtendedSelection)
            self.deskVidList.setRootIsDecorated(False)
            self.deskVidList.setItemsExpandable(False)
            self.deskVidList.setAllColumnsShowFocus(True)
            self.deskVidList.setObjectName("deskVidList")
            self.deskVidList.setSortingEnabled(True)
            self.deskVidList.headerItem().setText(0, self.tr("Host"))
            self.deskVidList.headerItem().setText(1, self.tr("Permission"))
            self.tabWidget.addTab(
                self.deskVidList,
                UI.PixmapCache.getIcon("desktopVideoCapture"),
                self.tr("Desktop Video"))
            
            self.deskAudVidList = QTreeWidget()
            self.deskAudVidList.setAlternatingRowColors(True)
            self.deskAudVidList.setSelectionMode(
                QAbstractItemView.SelectionMode.ExtendedSelection)
            self.deskAudVidList.setRootIsDecorated(False)
            self.deskAudVidList.setItemsExpandable(False)
            self.deskAudVidList.setAllColumnsShowFocus(True)
            self.deskAudVidList.setObjectName("deskAudVidList")
            self.deskAudVidList.setSortingEnabled(True)
            self.deskAudVidList.headerItem().setText(0, self.tr("Host"))
            self.deskAudVidList.headerItem().setText(1, self.tr("Permission"))
            self.tabWidget.addTab(
                self.deskAudVidList,
                UI.PixmapCache.getIcon("desktopAudioVideoCapture"),
                self.tr("Desktop Audio && Video"))
        
        if hasattr(QWebEnginePage, "Notifications"):
            self.setTabOrder(self.tabWidget, self.notifList)
            self.setTabOrder(self.notifList, self.geoList)
        else:
            self.setTabOrder(self.tabWidget, self.geoList)
        self.setTabOrder(self.geoList, self.micList)
        self.setTabOrder(self.micList, self.camList)
        self.setTabOrder(self.camList, self.micCamList)
        self.setTabOrder(self.micCamList, self.mouseLockList)
        if hasattr(QWebEnginePage, "DesktopVideoCapture"):
            self.setTabOrder(self.mouseLockList, self.deskVidList)
            self.setTabOrder(self.deskVidList, self.deskAudVidList)
            self.setTabOrder(self.deskAudVidList, self.removeButton)
        else:
            self.setTabOrder(self.mouseLockList, self.removeButton)
        self.setTabOrder(self.removeButton, self.removeAllButton)
        
        self.__permissionStrings = {
            QWebEnginePage.PermissionPolicy.PermissionGrantedByUser:
                self.tr("Allow"),
            QWebEnginePage.PermissionPolicy.PermissionDeniedByUser:
                self.tr("Deny"),
        }
        
        self.__permissionsLists = {
            QWebEnginePage.Feature.Geolocation: self.geoList,
            QWebEnginePage.Feature.MediaAudioCapture: self.micList,
            QWebEnginePage.Feature.MediaVideoCapture: self.camList,
            QWebEnginePage.Feature.MediaAudioVideoCapture: self.micCamList,
            QWebEnginePage.Feature.MouseLock: self.mouseLockList,
        }
        if hasattr(QWebEnginePage, "DesktopVideoCapture"):
            self.__permissionsLists.update({
                QWebEnginePage.Feature.DesktopVideoCapture:
                    self.deskVidList,
                QWebEnginePage.Feature.DesktopAudioVideoCapture:
                    self.deskAudVidList,
            })
        if hasattr(QWebEnginePage, "Notifications"):
            self.__permissionsLists[QWebEnginePage.Feature.Notifications] = (
                self.notifList
            )
        
        for feature, permissionsList in self.__permissionsLists.items():
            for permission in featurePermissions[feature]:
                for host in featurePermissions[feature][permission]:
                    itm = QTreeWidgetItem(
                        permissionsList,
                        [host, self.__permissionStrings[permission]])
                    itm.setData(0, Qt.ItemDataRole.UserRole, permission)
        
        self.__previousCurrent = -1
        self.tabWidget.currentChanged.connect(self.__currentTabChanged)
        self.tabWidget.setCurrentIndex(0)
    
    @pyqtSlot(int)
    def __currentTabChanged(self, index):
        """
        Private slot handling changes of the selected tab.
        
        @param index index of the current tab
        @type int
        """
        if self.__previousCurrent >= 0:
            previousList = self.tabWidget.widget(self.__previousCurrent)
            previousList.itemSelectionChanged.disconnect(
                self.__itemSelectionChanged)
        
        self.__updateButtons()
        
        currentList = self.tabWidget.currentWidget()
        currentList.itemSelectionChanged.connect(self.__itemSelectionChanged)
        self.__previousCurrent = index
    
    def __updateButtons(self):
        """
        Private method to update the buttons.
        """
        currentList = self.tabWidget.currentWidget()
        self.removeAllButton.setEnabled(
            currentList.topLevelItemCount() > 0)
        self.removeButton.setEnabled(
            len(currentList.selectedItems()) > 0)
    
    @pyqtSlot()
    def __itemSelectionChanged(self):
        """
        Private slot handling changes in the current list of selected items.
        """
        self.__updateButtons()
    
    @pyqtSlot()
    def on_removeButton_clicked(self):
        """
        Private slot to remove selected entries.
        """
        currentList = self.tabWidget.currentWidget()
        for itm in currentList.selectedItems():
            row = currentList.indexOfTopLevelItem(itm)
            itm = currentList.takeTopLevelItem(row)
            del itm
        self.__updateButtons()
    
    @pyqtSlot()
    def on_removeAllButton_clicked(self):
        """
        Private slot to remove all entries.
        """
        currentList = self.tabWidget.currentWidget()
        while currentList.topLevelItemCount() > 0:
            itm = currentList.takeTopLevelItem(0)      # __IGNORE_WARNING__
            del itm
        self.__updateGeoButtons()
    
    def getData(self):
        """
        Public method to retrieve the dialog contents.
        
        @return new feature permission settings
        @rtype dict of dict of list
        """
        featurePermissions = {}
        for feature, permissionsList in self.__permissionsLists.items():
            featurePermissions[feature] = {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            }
            for row in range(permissionsList.topLevelItemCount()):
                itm = permissionsList.topLevelItem(row)
                host = itm.text(0)
                permission = itm.data(0, Qt.ItemDataRole.UserRole)
                featurePermissions[feature][permission].append(host)
        
        return featurePermissions
