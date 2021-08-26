# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a widget to show some site information.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtWidgets import (
    QMenu, QGridLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy, QPushButton,
    QSpacerItem
)

import UI.PixmapCache

from WebBrowser.WebBrowserWindow import WebBrowserWindow


class SiteInfoWidget(QMenu):
    """
    Class implementing a widget to show SSL certificate infos.
    """
    def __init__(self, browser, parent=None):
        """
        Constructor
        
        @param browser reference to the browser view
        @type WebBrowserView
        @param parent reference to the parent object
        @type QWidget
        """
        super(SiteInfoWidget, self).__init__(parent)
        
        self.__browser = browser
        url = browser.url()
        
        self.setMinimumWidth(400)
        
        layout = QGridLayout(self)
        rows = 0
        
        titleLabel = QLabel(self)
        titleLabel.setText(self.tr("<b>Site {0}</b>").format(url.host()))
        layout.addWidget(titleLabel, rows, 0, 1, -1,
                         Qt.AlignmentFlag.AlignCenter)
        rows += 1
        
        line = QFrame(self)
        line.setLineWidth(1)
        line.setFrameStyle(QFrame.Shape.HLine | QFrame.Shadow.Sunken)
        layout.addWidget(line, rows, 0, 1, -1)
        rows += 1
        
        secureIcon = QLabel()
        layout.addWidget(secureIcon, rows, 0, Qt.AlignmentFlag.AlignCenter)
        secureLabel = QLabel()
        secureLabel.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Preferred)
        layout.addWidget(secureLabel, rows, 1)
        if url.scheme() in ["https"]:
            if WebBrowserWindow.networkManager().isInsecureHost(url.host()):
                secureLabel.setText(
                    self.tr("Your connection to this site "
                            "<b>may not be secure</b>."))
                secureIcon.setPixmap(
                    UI.PixmapCache.getPixmap("securityMedium"))
            else:
                secureLabel.setText(
                    self.tr("Your connection to this site is <b>secure</b>."))
                secureIcon.setPixmap(
                    UI.PixmapCache.getPixmap("securityHigh"))
        else:
            secureLabel.setText(
                self.tr("Your connection to this site is <b>not secure</b>."))
            secureIcon.setPixmap(
                UI.PixmapCache.getPixmap("securityLow"))
        rows += 1
        
        visits = WebBrowserWindow.historyManager().siteVisitsCount(
            url.scheme(), url.host())
        historyIcon = QLabel()
        layout.addWidget(historyIcon, rows, 0, Qt.AlignmentFlag.AlignCenter)
        historyLabel = QLabel()
        historyLabel.setSizePolicy(QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Preferred)
        layout.addWidget(historyLabel, rows, 1)
        if visits > 3:
            historyLabel.setText(
                self.tr("This is your <b>{0}.</b> visit of this site.")
                .format(visits))
            historyIcon.setPixmap(
                UI.PixmapCache.getPixmap("flagGreen"))
        elif visits == 0:
            historyLabel.setText(
                self.tr("You have <b>never</b> visited this site before.")
                .format(visits))
            historyIcon.setPixmap(
                UI.PixmapCache.getPixmap("flagBlack"))
        else:
            historyIcon.setPixmap(
                UI.PixmapCache.getPixmap("flagYellow"))
            if visits == 1:
                visitStr = self.tr("first")
            elif visits == 2:
                visitStr = self.tr("second")
            else:
                visitStr = self.tr("third")
            historyLabel.setText(
                self.tr("This is your <b>{0}</b> visit of this site.")
                .format(visitStr))
        rows += 1
        
        line = QFrame(self)
        line.setLineWidth(1)
        line.setFrameStyle(QFrame.Shape.HLine | QFrame.Shadow.Sunken)
        layout.addWidget(line, rows, 0, 1, -1)
        rows += 1
        
        page = self.__browser.page()
        scheme = page.registerProtocolHandlerRequestScheme()
        registeredUrl = (
            WebBrowserWindow.protocolHandlerManager().protocolHandler(scheme)
        )
        if (
            bool(scheme) and
            registeredUrl != page.registerProtocolHandlerRequestUrl()
        ):
            horizontalLayout = QHBoxLayout()
            protocolHandlerLabel = QLabel(
                self.tr("Register as <b>{0}</b> links handler.")
                .format(scheme), self)
            protocolHandlerLabel.setSizePolicy(QSizePolicy.Policy.Expanding,
                                               QSizePolicy.Policy.Preferred)
            
            horizontalLayout.addWidget(protocolHandlerLabel)
            protocolHandlerButton = QPushButton(self.tr("Register"), self)
            horizontalLayout.addWidget(protocolHandlerButton)
            protocolHandlerButton.clicked.connect(
                self.__registerProtocolHandler)
            layout.addLayout(horizontalLayout, rows, 0, 1, -1)
            rows += 1
            
            protocolHandlerLine = QFrame(self)
            protocolHandlerLine.setLineWidth(1)
            protocolHandlerLine.setFrameStyle(
                QFrame.Shape.HLine | QFrame.Shadow.Sunken)
            layout.addWidget(protocolHandlerLine, rows, 0, 1, -1)
            rows += 1
        
        horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(spacerItem)
        moreButton = QPushButton(self.tr("More..."), self)
        horizontalLayout.addWidget(moreButton)
        moreButton.clicked.connect(self.__showSiteInfo)
        layout.addLayout(horizontalLayout, rows, 0, 1, -1)
    
    def showAt(self, pos):
        """
        Public method to show the widget.
        
        @param pos position to show at
        @type QPoint
        """
        self.adjustSize()
        xpos = pos.x() - self.width() // 2
        if xpos < 0:
            xpos = 10
        p = QPoint(xpos, pos.y() + 10)
        self.move(p)
        self.show()
    
    def accept(self):
        """
        Public method to accept the widget.
        """
        self.close()
    
    @pyqtSlot()
    def __showSiteInfo(self):
        """
        Private slot to show the site info dialog.
        """
        from .SiteInfoDialog import SiteInfoDialog
        siteinfoDialog = SiteInfoDialog(
            self.__browser, self.__browser.mainWindow())
        siteinfoDialog.show()
    
    @pyqtSlot()
    def __registerProtocolHandler(self):
        """
        Private slot to register a protocol handler.
        """
        self.close()
        page = self.__browser.page()
        WebBrowserWindow.protocolHandlerManager().addProtocolHandler(
            page.registerProtocolHandlerRequestScheme(),
            page.registerProtocolHandlerRequestUrl())
