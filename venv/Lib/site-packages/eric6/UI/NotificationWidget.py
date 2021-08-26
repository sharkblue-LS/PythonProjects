# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a Notification widget.
"""

from enum import Enum

from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout

from .Ui_NotificationFrame import Ui_NotificationFrame

import Globals
import Preferences
import UI.PixmapCache


class NotificationTypes(Enum):
    """
    Class implementing the notification types.
    """
    Information = 0
    Warning = 1             # __IGNORE_WARNING_M131__
    Critical = 2
    Other = 99


class NotificationFrame(QFrame, Ui_NotificationFrame):
    """
    Class implementing a Notification widget.
    """
    NotificationStyleSheetTemplate = "color:{0};background-color:{1};"
    
    def __init__(self, icon, heading, text,
                 kind=NotificationTypes.Information, parent=None):
        """
        Constructor
        
        @param icon icon to be used
        @type QPixmap
        @param heading heading to be used
        @type str
        @param text text to be used
        @type str
        @param kind kind of notification to be shown
        @type NotificationTypes
        @param parent reference to the parent widget
        @type QWidget
        """
        super(NotificationFrame, self).__init__(parent)
        self.setupUi(self)
        
        self.layout().setAlignment(
            self.verticalLayout,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        
        self.setStyleSheet(NotificationFrame.getStyleSheet(kind))
        
        if icon is None:
            icon = NotificationFrame.getIcon(kind)
        self.icon.setPixmap(icon)
        
        self.heading.setText(heading)
        self.text.setText(text)
        
        self.show()
        self.adjustSize()
    
    @classmethod
    def getIcon(cls, kind):
        """
        Class method to get the icon for a specific notification kind.
        
        @param kind notification kind
        @type NotificationTypes
        @return icon for the notification kind
        @rtype QPixmap
        """
        if kind == NotificationTypes.Critical:
            return UI.PixmapCache.getPixmap("notificationCritical48")
        elif kind == NotificationTypes.Warning:
            return UI.PixmapCache.getPixmap("notificationWarning48")
        elif kind == NotificationTypes.Information:
            return UI.PixmapCache.getPixmap("notificationInformation48")
        else:
            return UI.PixmapCache.getPixmap("notification48")
    
    @classmethod
    def getStyleSheet(cls, kind):
        """
        Class method to get a style sheet for specific notification kind.
        
        @param kind notification kind
        @type NotificationTypes
        @return string containing the style sheet for the notification kind
        @rtype str
        """
        if kind == NotificationTypes.Critical:
            return NotificationFrame.NotificationStyleSheetTemplate.format(
                Preferences.getUI("NotificationCriticalForeground"),
                Preferences.getUI("NotificationCriticalBackground")
            )
        elif kind == NotificationTypes.Warning:
            return NotificationFrame.NotificationStyleSheetTemplate.format(
                Preferences.getUI("NotificationWarningForeground"),
                Preferences.getUI("NotificationWarningBackground")
            )
        else:
            return ""


class NotificationWidget(QWidget):
    """
    Class implementing a Notification list widget.
    """
    def __init__(self, parent=None, setPosition=False):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        @param setPosition flag indicating to set the display
            position interactively
        @type bool
        """
        super(NotificationWidget, self).__init__(parent)
        
        self.__layout = QVBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)
        
        self.__timeout = 5000
        self.__dragPosition = QPoint()
        self.__timers = {}
        self.__notifications = []
        
        self.__settingPosition = setPosition
        
        flags = (
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        if Globals.isWindowsPlatform():
            flags |= Qt.WindowType.ToolTip
        self.setWindowFlags(flags)
        
        if self.__settingPosition:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
    
    def showNotification(self, icon, heading, text,
                         kind=NotificationTypes.Information, timeout=0):
        """
        Public method to show a notification.
        
        @param icon icon to be used
        @type QPixmap
        @param heading heading to be used
        @type str
        @param text text to be used
        @type str
        @param kind kind of notification to be shown
        @type NotificationTypes
        @param timeout timeout in seconds after which the notification is
            to be removed (0 = do not remove until it is clicked on)
        @type int
        """
        notificationFrame = NotificationFrame(
            icon, heading, text, kind=kind, parent=self)
        self.__layout.addWidget(notificationFrame)
        self.__notifications.append(notificationFrame)
        
        self.show()
        
        self.__adjustSizeAndPosition()
        
        if timeout:
            timer = QTimer()
            self.__timers[id(notificationFrame)] = timer
            timer.setSingleShot(True)
            timer.timeout.connect(
                lambda: self.__removeNotification(notificationFrame)
            )
            timer.setInterval(timeout * 1000)
            timer.start()
    
    def __adjustSizeAndPosition(self):
        """
        Private slot to adjust the notification list widget size and position.
        """
        self.adjustSize()
        
        if not self.__settingPosition:
            pos = Preferences.getUI("NotificationPosition")
            try:
                screen = self.screen()
            except AttributeError:
                # < Qt 5.15
                from PyQt5.QtGui import QGuiApplication
                screen = QGuiApplication.screenAt(pos)
            screenGeom = screen.geometry()
            
            newX = pos.x()
            newY = pos.y()
            if newX < screenGeom.x():
                newX = screenGeom.x()
            if newY < screenGeom.y():
                newY = screenGeom.y()
            if newX + self.width() > screenGeom.width():
                newX = screenGeom.width() - self.width()
            if newY + self.height() > screenGeom.height():
                newY = screenGeom.height() - self.height()
            
            self.move(newX, newY)
    
    def __removeNotification(self, notification):
        """
        Private method to remove a notification from the list.
        
        @param notification reference to the notification to be removed
        @type NotificationFrame
        """
        notification.hide()
        
        # delete timer of an auto close notification
        key = id(notification)
        if key in self.__timers:
            self.__timers[key].stop()
            del self.__timers[key]
        
        # delete the notification
        index = self.__layout.indexOf(notification)
        self.__layout.takeAt(index)
        try:
            self.__notifications.remove(notification)
            notification.deleteLater()
        except ValueError:
            # it was already delete by other method; ignore
            pass
        
        if self.__layout.count():
            self.__adjustSizeAndPosition()
        else:
            self.hide()
    
    def mousePressEvent(self, evt):
        """
        Protected method to handle presses of a mouse button.
        
        @param evt reference to the mouse event (QMouseEvent)
        """
        if not self.__settingPosition:
            clickedLabel = self.childAt(evt.pos())
            if clickedLabel:
                clickedNotification = clickedLabel.parent()
                self.__removeNotification(clickedNotification)
            return
        
        if evt.button() == Qt.MouseButton.LeftButton:
            self.__dragPosition = (
                evt.globalPos() - self.frameGeometry().topLeft()
            )
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            evt.accept()
    
    def mouseReleaseEvent(self, evt):
        """
        Protected method to handle releases of a mouse button.
        
        @param evt reference to the mouse event (QMouseEvent)
        """
        if (
            self.__settingPosition and
            evt.button() == Qt.MouseButton.LeftButton
        ):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
    
    def mouseMoveEvent(self, evt):
        """
        Protected method to handle dragging the window.
        
        @param evt reference to the mouse event (QMouseEvent)
        """
        if evt.buttons() & Qt.MouseButton.LeftButton:
            self.move(evt.globalPos() - self.__dragPosition)
            evt.accept()
