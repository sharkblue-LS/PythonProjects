# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a window for showing the QtHelp index.
"""

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextBrowser, QApplication, QMenu
)


class HelpSearchWidget(QWidget):
    """
    Class implementing a window for showing the QtHelp index.
    
    @signal escapePressed() emitted when the ESC key was pressed
    @signal openUrl(QUrl, str) emitted to open a search result entry in the
        current tab
    @signal newTab(QUrl, str) emitted to open a search result entry in a
        new tab
    @signal newBackgroundTab(QUrl, str) emitted to open a search result entry
        in a new background tab
    @signal newWindow(QUrl, str) emitted to open a search result entry in a
        new window
    """
    escapePressed = pyqtSignal()
    openUrl = pyqtSignal(QUrl)
    newTab = pyqtSignal(QUrl)
    newBackgroundTab = pyqtSignal(QUrl)
    newWindow = pyqtSignal(QUrl)
    
    def __init__(self, engine, parent=None):
        """
        Constructor
        
        @param engine reference to the help search engine (QHelpSearchEngine)
        @param parent reference to the parent widget (QWidget)
        """
        super(HelpSearchWidget, self).__init__(parent)
        
        self.__engine = engine
        
        self.__layout = QVBoxLayout(self)
        
        self.__result = self.__engine.resultWidget()
        self.__query = self.__engine.queryWidget()
        
        self.__layout.addWidget(self.__query)
        self.__layout.addWidget(self.__result)
        
        self.setFocusProxy(self.__query)
        
        self.__query.search.connect(self.__search)
        self.__result.requestShowLink.connect(self.__linkActivated)
        
        self.__engine.searchingStarted.connect(self.__searchingStarted)
        self.__engine.searchingFinished.connect(self.__searchingFinished)
        
        self.__browser = self.__result.findChildren(QTextBrowser)[0]
    
    def __search(self):
        """
        Private slot to perform a search of the database.
        """
        query = self.__query.query()
        self.__engine.search(query)
    
    def __searchingStarted(self):
        """
        Private slot to handle the start of a search.
        """
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
    
    def __searchingFinished(self, hits):
        """
        Private slot to handle the end of the search.
        
        @param hits number of hits (integer) (unused)
        """
        QApplication.restoreOverrideCursor()
    
    @pyqtSlot(QUrl)
    def __linkActivated(self, url):
        """
        Private slot handling the activation of an entry.
        
        @param url URL of the activated entry
        @type QUrl
        """
        if not url.isEmpty() and url.isValid():
            buttons = QApplication.mouseButtons()
            modifiers = QApplication.keyboardModifiers()
            
            if buttons & Qt.MouseButton.MidButton:
                self.newTab.emit(url)
            else:
                if (
                    modifiers & (
                        Qt.KeyboardModifier.ControlModifier |
                        Qt.KeyboardModifier.ShiftModifier
                    ) == (
                        Qt.KeyboardModifier.ControlModifier |
                        Qt.KeyboardModifier.ShiftModifier
                    )
                ):
                    self.newBackgroundTab.emit(url)
                elif modifiers & Qt.KeyboardModifier.ControlModifier:
                    self.newTab.emit(url)
                elif modifiers & Qt.KeyboardModifier.ShiftModifier:
                    self.newWindow.emit(url)
                else:
                    self.openUrl.emit(url)
    
    def keyPressEvent(self, evt):
        """
        Protected method handling key press events.
        
        @param evt reference to the key press event (QKeyEvent)
        """
        if evt.key() == Qt.Key.Key_Escape:
            self.escapePressed.emit()
        else:
            evt.ignore()
    
    def contextMenuEvent(self, evt):
        """
        Protected method handling context menu events.
        
        @param evt reference to the context menu event (QContextMenuEvent)
        """
        point = evt.globalPos()
        
        if self.__browser:
            point = self.__browser.mapFromGlobal(point)
            if not self.__browser.rect().contains(point, True):
                return
            link = QUrl(self.__browser.anchorAt(point))
        else:
            point = self.__result.mapFromGlobal(point)
            link = self.__result.linkAt(point)
        
        if link.isEmpty() or not link.isValid():
            return
        
        menu = QMenu()
        curTab = menu.addAction(self.tr("Open Link"))
        newTab = menu.addAction(self.tr("Open Link in New Tab"))
        newBackgroundTab = menu.addAction(
            self.tr("Open Link in Background Tab"))
        newWindow = menu.addAction(self.tr("Open Link in New Window"))
        menu.move(evt.globalPos())
        act = menu.exec()
        if act == curTab:
            self.openUrl.emit(link)
        elif act == newTab:
            self.newTab.emit(link)
        elif act == newBackgroundTab:
            self.newBackgroundTab.emit(link)
        elif act == newWindow:
            self.newWindow.emit(link)
