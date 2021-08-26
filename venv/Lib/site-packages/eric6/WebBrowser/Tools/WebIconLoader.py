# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing an object to load web site icons.
"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtNetwork import QNetworkRequest, QSslConfiguration

try:
    from PyQt5.QtNetwork import QSslConfiguration     # __IGNORE_WARNING__
    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

import WebBrowser.WebBrowserWindow


class WebIconLoader(QObject):
    """
    Class implementing a loader for web site icons.
    
    @signal iconLoaded(icon) emitted when the icon has been loaded
    @signal sslConfiguration(config) emitted to pass the SSL data
    @signal clearSslConfiguration() emitted to clear stored SSL data
    """
    iconLoaded = pyqtSignal(QIcon)
    if SSL_AVAILABLE:
        sslConfiguration = pyqtSignal(QSslConfiguration)
        clearSslConfiguration = pyqtSignal()
    
    def __init__(self, url, parent=None):
        """
        Constructor
        
        @param url URL to fetch the icon from
        @type QUrl
        @param parent reference to the parent object
        @type QObject
        """
        super(WebIconLoader, self).__init__(parent)
        
        networkManager = (
            WebBrowser.WebBrowserWindow.WebBrowserWindow.networkManager()
        )
        self.__reply = networkManager.get(QNetworkRequest(url))
        self.__reply.finished.connect(self.__finished)
    
    @pyqtSlot()
    def __finished(self):
        """
        Private slot handling the downloaded icon.
        """
        # ignore any errors and emit an empty icon in this case
        data = self.__reply.readAll()
        icon = QIcon(QPixmap.fromImage(QImage.fromData(data)))
        self.iconLoaded.emit(icon)
        
        if SSL_AVAILABLE:
            if self.__reply.url().scheme().lower() == "https":
                sslConfiguration = self.__reply.sslConfiguration()
                self.sslConfiguration.emit(sslConfiguration)
            else:
                self.clearSslConfiguration.emit()
        
        self.__reply.deleteLater()
        self.__reply = None
