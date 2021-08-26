# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to add RSS feeds.
"""

import functools

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel

from .Ui_FeedsDialog import Ui_FeedsDialog

import UI.PixmapCache
from UI.NotificationWidget import NotificationTypes


class FeedsDialog(QDialog, Ui_FeedsDialog):
    """
    Class implementing a dialog to add RSS feeds.
    """
    def __init__(self, availableFeeds, browser, parent=None):
        """
        Constructor
        
        @param availableFeeds list of available RSS feeds (list of tuple of
            two strings)
        @param browser reference to the browser widget (WebBrowserView)
        @param parent reference to the parent widget (QWidget)
        """
        super(FeedsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.iconLabel.setPixmap(UI.PixmapCache.getPixmap("rss48"))
        
        self.__browser = browser
        
        self.__availableFeeds = availableFeeds[:]
        for row in range(len(self.__availableFeeds)):
            feed = self.__availableFeeds[row]
            button = QPushButton(self)
            button.setText(self.tr("Add"))
            button.feed = feed
            label = QLabel(self)
            label.setText(feed[0])
            self.feedsLayout.addWidget(label, row, 0)
            self.feedsLayout.addWidget(button, row, 1)
            button.clicked.connect(
                functools.partial(self.__addFeed, button))
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __addFeed(self, button):
        """
        Private slot to add a RSS feed.
        
        @param button reference to the feed button
        @type QPushButton
        """
        urlString = button.feed[1]
        url = QUrl(urlString)
        if url.isRelative():
            url = self.__browser.url().resolved(url)
            urlString = url.toDisplayString(
                QUrl.ComponentFormattingOption.FullyDecoded)
        
        if not url.isValid():
            return
        
        if button.feed[0]:
            title = button.feed[0]
        else:
            title = self.__browser.url().host()
        
        from WebBrowser.WebBrowserWindow import WebBrowserWindow
        feedsManager = WebBrowserWindow.feedsManager()
        if feedsManager.addFeed(urlString, title, self.__browser.icon()):
            WebBrowserWindow.showNotification(
                UI.PixmapCache.getPixmap("rss48"),
                self.tr("Add RSS Feed"),
                self.tr("""The feed was added successfully."""))
        else:
            WebBrowserWindow.showNotification(
                UI.PixmapCache.getPixmap("rss48"),
                self.tr("Add RSS Feed"),
                self.tr("""The feed was already added before."""),
                kind=NotificationTypes.Warning,
                timeout=0)
        
        self.close()
