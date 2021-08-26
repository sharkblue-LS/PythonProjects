# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the synchronization status wizard page.
"""

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWizardPage

from . import SyncGlobals

from .Ui_SyncCheckPage import Ui_SyncCheckPage

import Preferences
import UI.PixmapCache


class SyncCheckPage(QWizardPage, Ui_SyncCheckPage):
    """
    Class implementing the synchronization status wizard page.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(SyncCheckPage, self).__init__(parent)
        self.setupUi(self)
    
    def initializePage(self):
        """
        Public method to initialize the page.
        """
        self.syncErrorLabel.hide()
        
        forceUpload = self.field("ReencryptData")
        
        from WebBrowser.WebBrowserWindow import WebBrowserWindow
        syncMgr = WebBrowserWindow.syncManager()
        syncMgr.syncError.connect(self.__syncError)
        syncMgr.syncStatus.connect(self.__updateMessages)
        syncMgr.syncFinished.connect(self.__updateLabels)
        
        if Preferences.getWebBrowser("SyncType") == SyncGlobals.SyncTypeFtp:
            self.handlerLabel.setText(self.tr("FTP"))
            self.infoLabel.setText(self.tr("Host:"))
            self.infoDataLabel.setText(
                Preferences.getWebBrowser("SyncFtpServer"))
        elif (
            Preferences.getWebBrowser("SyncType") ==
                SyncGlobals.SyncTypeDirectory
        ):
            self.handlerLabel.setText(self.tr("Shared Directory"))
            self.infoLabel.setText(self.tr("Directory:"))
            self.infoDataLabel.setText(
                Preferences.getWebBrowser("SyncDirectoryPath"))
        else:
            self.handlerLabel.setText(self.tr("No Synchronization"))
            self.hostLabel.setText("")
        
        self.bookmarkMsgLabel.setText("")
        self.historyMsgLabel.setText("")
        self.passwordsMsgLabel.setText("")
        self.userAgentsMsgLabel.setText("")
        self.speedDialMsgLabel.setText("")
        
        if not syncMgr.syncEnabled():
            self.bookmarkLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
            self.historyLabel.setPixmap(UI.PixmapCache.getPixmap("syncNo"))
            self.passwordsLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
            self.userAgentsLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
            self.speedDialLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
            return
        
        # bookmarks
        if Preferences.getWebBrowser("SyncBookmarks"):
            self.__makeAnimatedLabel("loadingAnimation", self.bookmarkLabel)
        else:
            self.bookmarkLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
        
        # history
        if Preferences.getWebBrowser("SyncHistory"):
            self.__makeAnimatedLabel("loadingAnimation", self.historyLabel)
        else:
            self.historyLabel.setPixmap(UI.PixmapCache.getPixmap("syncNo"))
        
        # Passwords
        if Preferences.getWebBrowser("SyncPasswords"):
            self.__makeAnimatedLabel("loadingAnimation", self.passwordsLabel)
        else:
            self.passwordsLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
        
        # user agent settings
        if Preferences.getWebBrowser("SyncUserAgents"):
            self.__makeAnimatedLabel("loadingAnimation", self.userAgentsLabel)
        else:
            self.userAgentsLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
        
        # speed dial settings
        if Preferences.getWebBrowser("SyncSpeedDial"):
            self.__makeAnimatedLabel("loadingAnimation", self.speedDialLabel)
        else:
            self.speedDialLabel.setPixmap(
                UI.PixmapCache.getPixmap("syncNo"))
        
        QTimer.singleShot(
            0, lambda: syncMgr.loadSettings(forceUpload=forceUpload))
    
    def __makeAnimatedLabel(self, fileName, label):
        """
        Private slot to create an animated label.
        
        @param fileName name of the file containing the animation
        @type str
        @param label reference to the label to be animated
        @type E5AnimatedLabel
        """
        label.setInterval(40)
        label.setAnimationFile(fileName)
        label.start()
    
    def __updateMessages(self, type_, msg):
        """
        Private slot to update the synchronization status info.
        
        @param type_ type of synchronization data (string)
        @param msg synchronization message (string)
        """
        if type_ == "bookmarks":
            self.bookmarkMsgLabel.setText(msg)
        elif type_ == "history":
            self.historyMsgLabel.setText(msg)
        elif type_ == "passwords":
            self.passwordsMsgLabel.setText(msg)
        elif type_ == "useragents":
            self.userAgentsMsgLabel.setText(msg)
        elif type_ == "speeddial":
            self.speedDialMsgLabel.setText(msg)
    
    def __updateLabels(self, type_, status, download):
        """
        Private slot to handle a finished synchronization event.
        
        @param type_ type of the synchronization event (string one
            of "bookmarks", "history", "passwords", "useragents" or
            "speeddial")
        @param status flag indicating success (boolean)
        @param download flag indicating a download of a file (boolean)
        """
        if type_ == "bookmarks":
            if status:
                self.bookmarkLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncCompleted"))
            else:
                self.bookmarkLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncFailed"))
        elif type_ == "history":
            if status:
                self.historyLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncCompleted"))
            else:
                self.historyLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncFailed"))
        elif type_ == "passwords":
            if status:
                self.passwordsLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncCompleted"))
            else:
                self.passwordsLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncFailed"))
        elif type_ == "useragents":
            if status:
                self.userAgentsLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncCompleted"))
            else:
                self.userAgentsLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncFailed"))
        elif type_ == "speeddial":
            if status:
                self.speedDialLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncCompleted"))
            else:
                self.speedDialLabel.setPixmap(
                    UI.PixmapCache.getPixmap("syncFailed"))
    
    def __syncError(self, message):
        """
        Private slot to handle general synchronization issues.
        
        @param message error message (string)
        """
        self.syncErrorLabel.show()
        self.syncErrorLabel.setText(self.tr(
            '<font color="#FF0000"><b>Error:</b> {0}</font>').format(message))
