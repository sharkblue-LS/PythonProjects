# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the feature permission bar widget.
"""

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from E5Gui.E5AnimatedWidget import E5AnimatedWidget

import UI.PixmapCache


class FeaturePermissionBar(E5AnimatedWidget):
    """
    Class implementing the feature permission bar widget.
    """
    DefaultHeight = 30
    
    def __init__(self, page, origin, feature, manager):
        """
        Constructor
        
        @param page reference to the web page
        @type QWebView
        @param origin security origin requesting the feature
        @type QUrl
        @param feature requested feature
        @type QWebPage.Feature
        @param manager reference to the feature permissions manager
        @type FeaturePermissionManager
        """
        super(FeaturePermissionBar, self).__init__(parent=page.view())
        
        self.__origin = QUrl(origin)
        self.__feature = feature
        self.__page = page
        self.__manager = manager
        
        self.__permissionFeatureTexts = {
            QWebEnginePage.Feature.Geolocation:
                self.tr("{0} wants to use your position."),
            QWebEnginePage.Feature.MediaAudioCapture:
                self.tr("{0} wants to use your microphone."),
            QWebEnginePage.Feature.MediaVideoCapture:
                self.tr("{0} wants to use your camera."),
            QWebEnginePage.Feature.MediaAudioVideoCapture:
                self.tr("{0} wants to use your microphone and camera."),
            QWebEnginePage.Feature.MouseLock:
                self.tr("{0} wants to lock your mouse."),
        }
        try:
            # these are defined as of Qt 5.10.0/PyQt 5.10.0
            self.__permissionFeatureTexts.update({
                QWebEnginePage.Feature.DesktopVideoCapture:
                    self.tr("{0} wants to capture video of your screen."),
                QWebEnginePage.Feature.DesktopAudioVideoCapture:
                    self.tr("{0} wants to capture audio and video of your"
                            " screen."),
            })
        except AttributeError:
            pass
        try:
            # this was re-added in Qt 5.13.0
            self.__permissionFeatureTexts[
                QWebEnginePage.Feature.Notifications] = self.tr(
                "{0} wants to use desktop notifications.")
        except AttributeError:
            pass
        
        self.__permissionFeatureIconNames = {
            QWebEnginePage.Feature.Geolocation: "geolocation",
            QWebEnginePage.Feature.MediaAudioCapture: "audiocapture",
            QWebEnginePage.Feature.MediaVideoCapture: "camera",
            QWebEnginePage.Feature.MediaAudioVideoCapture: "audio-video",
            QWebEnginePage.Feature.MouseLock: "mouse",
        }
        try:
            # these are defined as of Qt 5.10.0/PyQt 5.10.0
            self.__permissionFeatureIconNames.update({
                QWebEnginePage.Feature.DesktopVideoCapture:
                    "desktopVideoCapture",
                QWebEnginePage.Feature.DesktopAudioVideoCapture:
                    "desktopAudioVideoCapture",
            })
        except AttributeError:
            pass
        try:
            # this was re-added in Qt 5.13.0
            self.__permissionFeatureIconNames[
                QWebEnginePage.Feature.Notifications] = "notification"
        except AttributeError:
            pass
        
        self.setAutoFillBackground(True)
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.setContentsMargins(9, 0, 0, 0)
        self.__iconLabel = QLabel(self)
        self.__layout.addWidget(self.__iconLabel)
        self.__messageLabel = QLabel(self)
        self.__layout.addWidget(self.__messageLabel)
        self.__layout.addStretch()
        self.__rememberButton = QPushButton(self.tr("Remember"), self)
        self.__rememberButton.setCheckable(True)
        self.__allowButton = QPushButton(self.tr("Allow"), self)
        self.__denyButton = QPushButton(self.tr("Deny"), self)
        self.__discardButton = QPushButton(UI.PixmapCache.getIcon("close"),
                                           "", self)
        self.__allowButton.clicked.connect(self.__permissionGranted)
        self.__denyButton.clicked.connect(self.__permissionDenied)
        self.__discardButton.clicked.connect(self.__permissionUnknown)
        self.__layout.addWidget(self.__rememberButton)
        self.__layout.addWidget(self.__allowButton)
        self.__layout.addWidget(self.__denyButton)
        self.__layout.addWidget(self.__discardButton)
        
        try:
            self.__iconLabel.setPixmap(UI.PixmapCache.getPixmap(
                self.__permissionFeatureIconNames[self.__feature]))
        except KeyError:
            pass
        
        try:
            self.__messageLabel.setText(
                self.__permissionFeatureTexts[self.__feature].format(
                    self.__origin.host()))
        except KeyError:
            self.__messageLabel.setText(
                self.tr("{0} wants to use an unknown feature.").format(
                    self.__origin.host()))
        
        self.__page.loadStarted.connect(self.hide)
        
        self.resize(self.__page.view().width(), self.height())
        self.startAnimation()
    
    @pyqtSlot()
    def hide(self):
        """
        Public slot to hide the animated widget.
        """
        self.__page.loadStarted.disconnect(self.hide)
        super(FeaturePermissionBar, self).hide()
    
    def __permissionDenied(self):
        """
        Private slot handling the user pressing the deny button.
        """
        if self.__page is None or self.__manager is None:
            return
        
        self.__page.setFeaturePermission(
            self.__origin, self.__feature,
            QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)
        
        if self.__rememberButton.isChecked():
            self.__manager.rememberFeaturePermission(
                self.__page.url().host(), self.__feature,
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser)
        
        self.hide()
    
    def __permissionGranted(self):
        """
        Private slot handling the user pressing the allow button.
        """
        if self.__page is None or self.__manager is None:
            return
        
        self.__page.setFeaturePermission(
            self.__origin, self.__feature,
            QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
        
        if self.__rememberButton.isChecked():
            self.__manager.rememberFeaturePermission(
                self.__page.url().host(), self.__feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
        
        self.hide()
    
    def __permissionUnknown(self):
        """
        Private slot handling the user closing the dialog without.
        """
        if self.__page is None or self.__manager is None:
            return
        
        self.__page.setFeaturePermission(
            self.__origin, self.__feature,
            QWebEnginePage.PermissionPolicy.PermissionUnknown)
        
        self.hide()
