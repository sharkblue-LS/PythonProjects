# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the label to show the web site icon.
"""

from PyQt5.QtCore import Qt, QPoint, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QLabel, QApplication


class FavIconLabel(QLabel):
    """
    Class implementing the label to show the web site icon.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(FavIconLabel, self).__init__(parent)
        
        self.__browser = None
        self.__dragStartPos = QPoint()
        
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setMinimumSize(16, 16)
        self.resize(16, 16)
        
        self.__browserIconChanged()
    
    def __browserIconChanged(self):
        """
        Private slot to set the icon.
        """
        if self.__browser:
            self.setPixmap(
                self.__browser.icon().pixmap(16, 16))
    
    def __clearIcon(self):
        """
        Private slot to clear the icon.
        """
        self.setPixmap(QPixmap())
    
    def setBrowser(self, browser):
        """
        Public method to set the browser connection.
        
        @param browser reference to the browser widegt (HelpBrowser)
        """
        self.__browser = browser
        self.__browser.loadFinished.connect(self.__browserIconChanged)
        self.__browser.faviconChanged.connect(self.__browserIconChanged)
        self.__browser.loadStarted.connect(self.__clearIcon)
    
    def mousePressEvent(self, evt):
        """
        Protected method to handle mouse press events.
        
        @param evt reference to the mouse event (QMouseEvent)
        """
        if evt.button() == Qt.MouseButton.LeftButton:
            self.__dragStartPos = evt.pos()
        super(FavIconLabel, self).mousePressEvent(evt)
    
    def mouseReleaseEvent(self, evt):
        """
        Protected method to handle mouse release events.
        
        @param evt reference to the mouse event (QMouseEvent)
        """
        if evt.button() == Qt.MouseButton.LeftButton:
            self.__showPopup(evt.globalPos())
        super(FavIconLabel, self).mouseReleaseEvent(evt)
    
    def mouseMoveEvent(self, evt):
        """
        Protected method to handle mouse move events.
        
        @param evt reference to the mouse event (QMouseEvent)
        """
        if (
            evt.button() == Qt.MouseButton.LeftButton and
            ((evt.pos() - self.__dragStartPos).manhattanLength() >
                QApplication.startDragDistance()) and
            self.__browser is not None
        ):
            drag = QDrag(self)
            mimeData = QMimeData()
            title = self.__browser.title()
            if title == "":
                title = str(self.__browser.url().toEncoded(), encoding="utf-8")
            mimeData.setText(title)
            mimeData.setUrls([self.__browser.url()])
            p = self.pixmap()
            if p:
                drag.setPixmap(p)
            drag.setMimeData(mimeData)
            drag.exec()
    
    def __showPopup(self, pos):
        """
        Private method to show the site info popup.
        
        @param pos position the popup should be shown at
        @type QPoint
        """
        if self.__browser is None:
            return
        
        url = self.__browser.url()
        if url.isValid() and url.scheme() not in [
                "eric", "about", "data", "chrome"]:
            from ..SiteInfo.SiteInfoWidget import SiteInfoWidget
            info = SiteInfoWidget(self.__browser, self)
            info.showAt(pos)
