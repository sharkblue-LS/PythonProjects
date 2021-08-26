# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the feature permission manager object.
"""

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage

import Globals
import Preferences


class FeaturePermissionManager(QObject):
    """
    Class implementing the feature permission manager object.
    """
    SettingsKeyFormat = "WebBrowser/FeaturePermissions/{0}"
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object
        @type QObject
        """
        super(FeaturePermissionManager, self).__init__(parent)
        
        self.__featurePermissions = {
            QWebEnginePage.Feature.Geolocation: {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            },
            QWebEnginePage.Feature.MediaAudioCapture: {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            },
            QWebEnginePage.Feature.MediaVideoCapture: {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            },
            QWebEnginePage.Feature.MediaAudioVideoCapture: {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            },
            QWebEnginePage.Feature.MouseLock: {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            },
        }
        try:
            # these are defined as of Qt 5.10.0/PyQt 5.10.0
            self.__featurePermissions.update({
                QWebEnginePage.Feature.DesktopVideoCapture: {
                    QWebEnginePage.PermissionPolicy.PermissionGrantedByUser:
                        [],
                    QWebEnginePage.PermissionPolicy.PermissionDeniedByUser:
                        [],
                },
                QWebEnginePage.Feature.DesktopAudioVideoCapture: {
                    QWebEnginePage.PermissionPolicy.PermissionGrantedByUser:
                        [],
                    QWebEnginePage.PermissionPolicy.PermissionDeniedByUser:
                        [],
                },
            })
        except AttributeError:
            pass
        try:
            # this was re-added in Qt 5.13.0
            self.__featurePermissions[QWebEnginePage.Feature.Notifications] = {
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser: [],
                QWebEnginePage.PermissionPolicy.PermissionDeniedByUser: [],
            }
        except AttributeError:
            pass
        
        self.__featurePermissionsKeys = {
            (QWebEnginePage.Feature.Geolocation,
             QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
            "GeolocationGranted",
            (QWebEnginePage.Feature.Geolocation,
             QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
            "GeolocationDenied",
            (QWebEnginePage.Feature.MediaAudioCapture,
             QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
            "MediaAudioCaptureGranted",
            (QWebEnginePage.Feature.MediaAudioCapture,
             QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
            "MediaAudioCaptureDenied",
            (QWebEnginePage.Feature.MediaVideoCapture,
             QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
            "MediaVideoCaptureGranted",
            (QWebEnginePage.Feature.MediaVideoCapture,
             QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
            "MediaVideoCaptureDenied",
            (QWebEnginePage.Feature.MediaAudioVideoCapture,
             QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
            "MediaAudioVideoCaptureGranted",
            (QWebEnginePage.Feature.MediaAudioVideoCapture,
             QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
            "MediaAudioVideoCaptureDenied",
            (QWebEnginePage.Feature.MouseLock,
             QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
            "MouseLockGranted",
            (QWebEnginePage.Feature.MouseLock,
             QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
            "MouseLockDenied",
        }
        try:
            # these are defined as of Qt 5.10.0/PyQt 5.10.0
            self.__featurePermissionsKeys.update({
                (QWebEnginePage.Feature.DesktopVideoCapture,
                 QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
                "DesktopVideoCaptureGranted",
                (QWebEnginePage.Feature.DesktopVideoCapture,
                 QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
                "DesktopVideoCaptureDenied",
                (QWebEnginePage.Feature.DesktopAudioVideoCapture,
                 QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
                "DesktopAudioVideoCaptureGranted",
                (QWebEnginePage.Feature.DesktopAudioVideoCapture,
                 QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
                "DesktopAudioVideoCaptureDenied",
            })
        except AttributeError:
            pass
        try:
            # this was re-added in Qt 5.13.0
            self.__featurePermissionsKeys.update({
                (QWebEnginePage.Feature.Notifications,
                 QWebEnginePage.PermissionPolicy.PermissionGrantedByUser):
                "NotificationsGranted",
                (QWebEnginePage.Feature.Notifications,
                 QWebEnginePage.PermissionPolicy.PermissionDeniedByUser):
                "NotificationsDenied",
            })
        except AttributeError:
            pass
        
        self.__loaded = False

    def requestFeaturePermission(self, page, origin, feature):
        """
        Public method to request a feature permission.
        
        @param page reference to the requesting web page
        @type QWebEnginePage
        @param origin security origin requesting the feature
        @type QUrl
        @param feature requested feature
        @type QWebEnginePage.Feature
        """
        if origin is None or origin.isEmpty():
            return
        
        if not self.__loaded:
            self.__loadSettings()
        
        host = origin.host()
        
        if feature in self.__featurePermissions:
            for permission in self.__featurePermissions[feature]:
                if host in self.__featurePermissions[feature][permission]:
                    page.setFeaturePermission(origin, feature, permission)
                    return
        
        from .FeaturePermissionBar import FeaturePermissionBar
        bar = FeaturePermissionBar(page, origin, feature, self)
        bar.show()
    
    def rememberFeaturePermission(self, host, feature, permission):
        """
        Public method to remember a user decision for a feature permission.
        
        @param host host name to remember the decision for
        @type str
        @param feature feature to be remembered
        @type QWebEnginePage.Feature
        @param permission feature permission to be remembered
        @type QWebEnginePage.PermissionPolicy
        """
        if feature in self.__featurePermissions:
            if host not in self.__featurePermissions[feature][permission]:
                self.__featurePermissions[feature][permission].append(host)
                self.__saveSettings()
    
    def __loadSettings(self):
        """
        Private method to load the remembered feature permissions.
        """
        if self.__loaded:
            # no reloading allowed
            return
        
        for (feature, permission), key in (
            self.__featurePermissionsKeys.items()
        ):
            self.__featurePermissions[feature][permission] = (
                Globals.toList(Preferences.Prefs.settings.value(
                    FeaturePermissionManager.SettingsKeyFormat.format(key),
                    []
                ))
            )
        
        self.__loaded = True
    
    def __saveSettings(self):
        """
        Private method to save the remembered feature permissions.
        """
        if not self.__loaded:
            return
        
        import WebBrowser.WebBrowserWindow
        if WebBrowser.WebBrowserWindow.WebBrowserWindow.isPrivate():
            return
        
        for (feature, permission), key in (
                self.__featurePermissionsKeys.items()
        ):
            Preferences.Prefs.settings.setValue(
                FeaturePermissionManager.SettingsKeyFormat.format(key),
                self.__featurePermissions[feature][permission])
    
    def showFeaturePermissionsDialog(self):
        """
        Public method to show a dialog to manage the remembered feature
        permissions.
        """
        if not self.__loaded:
            self.__loadSettings()
        
        from .FeaturePermissionsDialog import FeaturePermissionsDialog
        dlg = FeaturePermissionsDialog(self.__featurePermissions)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            newFeaturePermissions = dlg.getData()
            self.__featurePermissions = newFeaturePermissions
            self.__saveSettings()
