# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a specialized error message dialog.
"""

from PyQt5.QtCore import (
    qInstallMessageHandler, QtDebugMsg, QtWarningMsg, QtCriticalMsg,
    QtFatalMsg, QThread, QMetaObject, Qt, Q_ARG, QSettings
)
from PyQt5.QtWidgets import QErrorMessage, QDialog

from E5Gui.E5Application import e5App

import Globals
import Utilities
import Preferences


_msgHandlerDialog = None
_origMsgHandler = None

_filterSettings = QSettings(
    QSettings.Format.IniFormat,
    QSettings.Scope.UserScope,
    Globals.settingsNameOrganization,
    "eric6messagefilters")
_defaultFilters = [
    "QFont::",
    "QCocoaMenu::removeMenuItem",
    "QCocoaMenu::insertNative",
    ",type id:",
    "Remote debugging server started successfully",
    "Uncaught SecurityError:",
    "Content Security Policy",
    "QXcbClipboard:",
    "QXcbConnection: XCB error",
    "libpng warning: iCCP:",
    "Uncaught ReferenceError: $ is not defined",
]


def filterMessage(message):
    """
    Module function to filter messages.
    
    @param message message to be checked
    @type str
    @return flag indicating that the message should be filtered out
    @rtype bool
    """
    for filterStr in Globals.toList(_filterSettings.value(
            "MessageFilters", [])) + _defaultFilters:
        if filterStr in message:
            return True
    
    return False


class E5ErrorMessage(QErrorMessage):
    """
    Class implementing a specialized error message dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5ErrorMessage, self).__init__(parent)
    
    def showMessage(self, message, msgType=""):
        """
        Public method to show a message.
        
        @param message error message to be shown
        @type str
        @param msgType type of the error message
        @type str
        """
        if not filterMessage(message):
            if msgType:
                super(E5ErrorMessage, self).showMessage(message, msgType)
            else:
                super(E5ErrorMessage, self).showMessage(message)
    
    def editMessageFilters(self):
        """
        Public method to edit the list of message filters.
        """
        from .E5ErrorMessageFilterDialog import E5ErrorMessageFilterDialog
        dlg = E5ErrorMessageFilterDialog(
            Globals.toList(_filterSettings.value(
                "MessageFilters", [])))
##            _defaultFilters)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            filters = dlg.getFilters()
            _filterSettings.setValue("MessageFilters", filters)


def messageHandler(msgType, context, message):
    """
    Module function handling messages.
    
    @param msgType type of the message
    @type  int, QtMsgType
    @param context context information
    @type QMessageLogContext
    @param message message to be shown
    @type bytes
    """
    if _msgHandlerDialog:
        if msgType < Preferences.getUI("MinimumMessageTypeSeverity"):
            # severity is lower than configured
            # just ignore the message
            return
        
        try:
            if msgType == QtDebugMsg:
                messageType = "Debug Message:"
            elif msgType == QtWarningMsg:
                messageType = "Warning:"
            elif msgType == QtCriticalMsg:
                messageType = "Critical:"
            elif msgType == QtFatalMsg:
                messageType = "Fatal Error:"
            if isinstance(message, bytes):
                message = Utilities.decodeBytes(message)
            if filterMessage(message):
                return
            message = (
                message.replace("\r\n", "<br/>")
                .replace("\n", "<br/>")
                .replace("\r", "<br/>")
            )
            if context.file is not None:
                msg = (
                    "<p><b>{0}</b></p><p>{1}</p><p>File: {2}</p>"
                    "<p>Line: {3}</p><p>Function: {4}</p>"
                ).format(messageType, Utilities.html_uencode(message),
                         context.file, context.line, context.function)
            else:
                msg = "<p><b>{0}</b></p><p>{1}</p>".format(
                    messageType, Utilities.html_uencode(message))
            if QThread.currentThread() == e5App().thread():
                _msgHandlerDialog.showMessage(msg)
            else:
                QMetaObject.invokeMethod(
                    _msgHandlerDialog,
                    "showMessage",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, msg))
            return
        except RuntimeError:
            pass
    elif _origMsgHandler:
        _origMsgHandler(msgType, message)
        return
    
    if msgType == QtDebugMsg:
        messageType = "Debug Message"
    elif msgType == QtWarningMsg:
        messageType = "Warning"
    elif msgType == QtCriticalMsg:
        messageType = "Critical"
    elif msgType == QtFatalMsg:
        messageType = "Fatal Error"
    if isinstance(message, bytes):
        message = message.decode()
    print("{0}: {1} in {2} at line {3} ({4})".format(
        messageType, message, context.file, context.line,
        context.function))


def qtHandler():
    """
    Module function to install an E5ErrorMessage dialog as the global
    message handler.
    
    @return reference to the message handler dialog
    @rtype E5ErrorMessage
    """
    global _msgHandlerDialog, _origMsgHandler
    
    if _msgHandlerDialog is None:
        # Install an E5ErrorMessage dialog as the global message handler.
        _msgHandlerDialog = E5ErrorMessage()
        _origMsgHandler = qInstallMessageHandler(messageHandler)
    
    return _msgHandlerDialog


def editMessageFilters():
    """
    Module function to edit the list of message filters.
    """
    if _msgHandlerDialog:
        _msgHandlerDialog.editMessageFilters()
    else:
        print("No message handler installed.")


def messageHandlerInstalled():
    """
    Module function to check, if a message handler was installed.
    
    @return flag indicating an installed message handler
    @rtype bool
    """
    return _msgHandlerDialog is not None

#
# eflag: noqa = M801
