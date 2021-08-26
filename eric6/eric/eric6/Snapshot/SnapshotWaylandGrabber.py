# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a grabber object for non-Wayland desktops.
"""

import os
import uuid

from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QApplication

try:
    from PyQt5.QtDBus import QDBusInterface, QDBusMessage
    DBusAvailable = True
except ImportError:
    DBusAvailable = False

from E5Gui import E5MessageBox

from .SnapshotModes import SnapshotModes

import Globals


class SnapshotWaylandGrabber(QObject):
    """
    Class implementing a grabber object for non-Wayland desktops.
    
    @signal grabbed(QPixmap) emitted after the grab operation is finished
    """
    grabbed = pyqtSignal(QPixmap)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object
        @type QObject
        """
        super(SnapshotWaylandGrabber, self).__init__(parent)
        
        from .SnapshotTimer import SnapshotTimer
        self.__grabTimer = SnapshotTimer()
        self.__grabTimer.timeout.connect(self.__performGrab)
    
    def supportedModes(self):
        """
        Public method to get the supported screenshot modes.
        
        @return tuple of supported screenshot modes
        @rtype tuple of SnapshotModes
        """
        if DBusAvailable and Globals.isKdeDesktop():
            return (
                SnapshotModes.Fullscreen,
                SnapshotModes.SelectedScreen,
                SnapshotModes.SelectedWindow,
            )
        elif DBusAvailable and Globals.isGnomeDesktop():
            return (
                SnapshotModes.Fullscreen,
                SnapshotModes.SelectedScreen,
                SnapshotModes.SelectedWindow,
                SnapshotModes.Rectangle,
            )
        else:
            return ()
    
    def grab(self, mode, delay=0, captureCursor=False,
             captureDecorations=False):
        """
        Public method to perform a grab operation potentially after a delay.
        
        @param mode screenshot mode
        @type ScreenshotModes
        @param delay delay in seconds
        @type int
        @param captureCursor flag indicating to include the mouse cursor
        @type bool
        @param captureDecorations flag indicating to include the window
            decorations (only used for mode SnapshotModes.SelectedWindow)
        @type bool
        """
        if not DBusAvailable:
            # just to play it safe
            self.grabbed.emit(QPixmap())
            return
        
        self.__mode = mode
        self.__captureCursor = captureCursor
        self.__captureDecorations = captureDecorations
        if delay:
            self.__grabTimer.start(delay)
        else:
            QTimer.singleShot(200, self.__performGrab)
    
    def __performGrab(self):
        """
        Private method to perform the grab operations.
        
        @exception RuntimeError raised to indicate an unsupported grab mode
        """
        if self.__mode == SnapshotModes.Fullscreen:
            self.__grabFullscreen()
        elif self.__mode == SnapshotModes.SelectedScreen:
            self.__grabSelectedScreen()
        elif self.__mode == SnapshotModes.SelectedWindow:
            self.__grabSelectedWindow()
        elif self.__mode == SnapshotModes.Rectangle:
            self.__grabRectangle()
        else:
            raise RuntimeError("unsupported grab mode given")
    
    def __grabFullscreen(self):
        """
        Private method to grab the complete desktop.
        """
        snapshot = QPixmap()
        
        if Globals.isKdeDesktop():
            interface = QDBusInterface(
                "org.kde.KWin",
                "/Screenshot",
                "org.kde.kwin.Screenshot"
            )
            reply = interface.call(
                "screenshotFullscreen",
                self.__captureCursor
            )
            if self.__checkReply(reply, 1):
                filename = reply.arguments()[0]
                if filename:
                    snapshot = QPixmap(filename)
                    try:
                        os.remove(filename)
                    except OSError:
                        # just ignore it
                        pass
        elif Globals.isGnomeDesktop():
            path = self.__temporaryFilename()
            interface = QDBusInterface(
                "org.gnome.Shell",
                "/org/gnome/Shell/Screenshot",
                "org.gnome.Shell.Screenshot"
            )
            reply = interface.call(
                "Screenshot",
                self.__captureCursor,
                False,
                path
            )
            if self.__checkReply(reply, 2):
                filename = reply.arguments()[1]
                if filename:
                    snapshot = QPixmap(filename)
                    try:
                        os.remove(filename)
                    except OSError:
                        # just ignore it
                        pass
        
        self.grabbed.emit(snapshot)
    
    def __grabSelectedScreen(self):
        """
        Private method to grab a selected screen.
        """
        snapshot = QPixmap()
        
        if Globals.isKdeDesktop():
            screen = QApplication.screenAt(QCursor.pos())
            try:
                screenId = QApplication.screens().index(screen)
            except ValueError:
                # default to screen 0
                screenId = 0
            
            # Step 2: grab the screen
            interface = QDBusInterface(
                "org.kde.KWin",
                "/Screenshot",
                "org.kde.kwin.Screenshot"
            )
            reply = interface.call(
                "screenshotScreen",
                screenId,
                self.__captureCursor
            )
            if self.__checkReply(reply, 1):
                filename = reply.arguments()[0]
                if filename:
                    snapshot = QPixmap(filename)
                    try:
                        os.remove(filename)
                    except OSError:
                        # just ignore it
                        pass
        elif Globals.isGnomeDesktop():
            # Step 1: grab entire desktop
            path = self.__temporaryFilename()
            interface = QDBusInterface(
                "org.gnome.Shell",
                "/org/gnome/Shell/Screenshot",
                "org.gnome.Shell.Screenshot"
            )
            reply = interface.call(
                "ScreenshotWindow",
                self.__captureDecorations,
                self.__captureCursor,
                False,
                path
            )
            if self.__checkReply(reply, 2):
                filename = reply.arguments()[1]
                if filename:
                    snapshot = QPixmap(filename)
                    try:
                        os.remove(filename)
                    except OSError:
                        # just ignore it
                        pass
                    
                    # Step 2: extract the area of the screen containing
                    #         the cursor
                    if not snapshot.isNull():
                        screen = QApplication.screenAt(QCursor.pos())
                        geom = screen.geometry()
                        snapshot = snapshot.copy(geom)
        
        self.grabbed.emit(snapshot)
    
    def __grabSelectedWindow(self):
        """
        Private method to grab a selected window.
        """
        snapshot = QPixmap()
        
        if Globals.isKdeDesktop():
            mask = 0
            if self.__captureDecorations:
                mask |= 1
            if self.__captureCursor:
                mask |= 2
            interface = QDBusInterface(
                "org.kde.KWin",
                "/Screenshot",
                "org.kde.kwin.Screenshot"
            )
            reply = interface.call(
                "interactive",
                mask
            )
            if self.__checkReply(reply, 1):
                filename = reply.arguments()[0]
                if filename:
                    snapshot = QPixmap(filename)
                    try:
                        os.remove(filename)
                    except OSError:
                        # just ignore it
                        pass
        elif Globals.isGnomeDesktop():
            path = self.__temporaryFilename()
            interface = QDBusInterface(
                "org.gnome.Shell",
                "/org/gnome/Shell/Screenshot",
                "org.gnome.Shell.Screenshot"
            )
            reply = interface.call(
                "ScreenshotWindow",
                self.__captureDecorations,
                self.__captureCursor,
                False,
                path
            )
            if self.__checkReply(reply, 2):
                filename = reply.arguments()[1]
                if filename:
                    snapshot = QPixmap(filename)
                    try:
                        os.remove(filename)
                    except OSError:
                        # just ignore it
                        pass
        
        self.grabbed.emit(snapshot)
    
    def __grabRectangle(self):
        """
        Private method to grab a rectangular desktop area.
        """
        snapshot = QPixmap()
        
        if Globals.isGnomeDesktop():
            # Step 1: let the user select the area
            interface = QDBusInterface(
                "org.gnome.Shell",
                "/org/gnome/Shell/Screenshot",
                "org.gnome.Shell.Screenshot"
            )
            reply = interface.call("SelectArea")
            if self.__checkReply(reply, 4):
                x, y, width, height = reply.arguments()[:4]
                
                # Step 2: grab the selected area
                path = self.__temporaryFilename()
                reply = interface.call(
                    "ScreenshotArea",
                    x, y, width, height,
                    False,
                    path
                )
                if self.__checkReply(reply, 2):
                    filename = reply.arguments()[1]
                    if filename:
                        snapshot = QPixmap(filename)
                        try:
                            os.remove(filename)
                        except OSError:
                            # just ignore it
                            pass
        
        self.grabbed.emit(snapshot)
    
    def __checkReply(self, reply, argumentsCount):
        """
        Private method to check, if a reply is valid.
        
        @param reply reference to the reply message
        @type QDBusMessage
        @param argumentsCount number of expected arguments
        @type int
        @return flag indicating validity
        @rtype bool
        """
        if reply.type() == QDBusMessage.MessageType.ReplyMessage:
            if len(reply.arguments()) == argumentsCount:
                return True
            
            E5MessageBox.warning(
                None,
                self.tr("Screenshot Error"),
                self.tr("<p>Received an unexpected number of reply arguments."
                        " Expected {0} but got {1}</p>").format(
                    argumentsCount,
                    len(reply.arguments()),
                ))
        
        elif reply.type() == QDBusMessage.MessageType.ErrorMessage:
            E5MessageBox.warning(
                None,
                self.tr("Screenshot Error"),
                self.tr("<p>Received error <b>{0}</b> from DBus while"
                        " performing screenshot.</p><p>{1}</p>").format(
                    reply.errorName(),
                    reply.errorMessage(),
                ))
        
        elif reply.type() == QDBusMessage.MessageType.InvalidMessage:
            E5MessageBox.warning(
                None,
                self.tr("Screenshot Error"),
                self.tr("Received an invalid reply."))
        
        else:
            E5MessageBox.warning(
                None,
                self.tr("Screenshot Error"),
                self.tr("Received an unexpected reply."))
        
        return False
    
    def __temporaryFilename(self):
        """
        Private method to generate a temporary filename.
        
        @return path name for a unique, temporary file
        @rtype str
        """
        return "/tmp/eric-snap-{0}.png".format(uuid.uuid4().hex)   # secok
