# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the MicroPython REPL widget.
"""

import re
import time
import os
import functools

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QPoint, QEvent
from PyQt5.QtGui import QColor, QKeySequence, QTextCursor, QBrush, QClipboard
from PyQt5.QtWidgets import (
    QWidget, QMenu, QApplication, QHBoxLayout, QSpacerItem, QSizePolicy,
    QTextEdit, QToolButton, QDialog
)

from E5Gui.E5ZoomWidget import E5ZoomWidget
from E5Gui import E5MessageBox, E5FileDialog
from E5Gui.E5Application import e5App
from E5Gui.E5ProcessDialog import E5ProcessDialog
from E5Gui.E5OverrideCursor import E5OverrideCursor, E5OverridenCursor

from .Ui_MicroPythonWidget import Ui_MicroPythonWidget

from . import MicroPythonDevices
from . import UF2FlashDialog
try:
    from .MicroPythonGraphWidget import MicroPythonGraphWidget
    HAS_QTCHART = True
except ImportError:
    HAS_QTCHART = False
from .MicroPythonFileManagerWidget import MicroPythonFileManagerWidget
try:
    from .MicroPythonCommandsInterface import MicroPythonCommandsInterface
    HAS_QTSERIALPORT = True
except ImportError:
    HAS_QTSERIALPORT = False

import Globals
import UI.PixmapCache
import Preferences
import Utilities

from UI.Info import BugAddress

# ANSI Colors (see https://en.wikipedia.org/wiki/ANSI_escape_code)
AnsiColorSchemes = {
    "Windows 7": {
        0: QBrush(QColor(0, 0, 0)),
        1: QBrush(QColor(128, 0, 0)),
        2: QBrush(QColor(0, 128, 0)),
        3: QBrush(QColor(128, 128, 0)),
        4: QBrush(QColor(0, 0, 128)),
        5: QBrush(QColor(128, 0, 128)),
        6: QBrush(QColor(0, 128, 128)),
        7: QBrush(QColor(192, 192, 192)),
        10: QBrush(QColor(128, 128, 128)),
        11: QBrush(QColor(255, 0, 0)),
        12: QBrush(QColor(0, 255, 0)),
        13: QBrush(QColor(255, 255, 0)),
        14: QBrush(QColor(0, 0, 255)),
        15: QBrush(QColor(255, 0, 255)),
        16: QBrush(QColor(0, 255, 255)),
        17: QBrush(QColor(255, 255, 255)),
    },
    "Windows 10": {
        0: QBrush(QColor(12, 12, 12)),
        1: QBrush(QColor(197, 15, 31)),
        2: QBrush(QColor(19, 161, 14)),
        3: QBrush(QColor(193, 156, 0)),
        4: QBrush(QColor(0, 55, 218)),
        5: QBrush(QColor(136, 23, 152)),
        6: QBrush(QColor(58, 150, 221)),
        7: QBrush(QColor(204, 204, 204)),
        10: QBrush(QColor(118, 118, 118)),
        11: QBrush(QColor(231, 72, 86)),
        12: QBrush(QColor(22, 198, 12)),
        13: QBrush(QColor(249, 241, 165)),
        14: QBrush(QColor(59, 12, 255)),
        15: QBrush(QColor(180, 0, 158)),
        16: QBrush(QColor(97, 214, 214)),
        17: QBrush(QColor(242, 242, 242)),
    },
    "PuTTY": {
        0: QBrush(QColor(0, 0, 0)),
        1: QBrush(QColor(187, 0, 0)),
        2: QBrush(QColor(0, 187, 0)),
        3: QBrush(QColor(187, 187, 0)),
        4: QBrush(QColor(0, 0, 187)),
        5: QBrush(QColor(187, 0, 187)),
        6: QBrush(QColor(0, 187, 187)),
        7: QBrush(QColor(187, 187, 187)),
        10: QBrush(QColor(85, 85, 85)),
        11: QBrush(QColor(255, 85, 85)),
        12: QBrush(QColor(85, 255, 85)),
        13: QBrush(QColor(255, 255, 85)),
        14: QBrush(QColor(85, 85, 255)),
        15: QBrush(QColor(255, 85, 255)),
        16: QBrush(QColor(85, 255, 255)),
        17: QBrush(QColor(255, 255, 255)),
    },
    "xterm": {
        0: QBrush(QColor(0, 0, 0)),
        1: QBrush(QColor(205, 0, 0)),
        2: QBrush(QColor(0, 205, 0)),
        3: QBrush(QColor(205, 205, 0)),
        4: QBrush(QColor(0, 0, 238)),
        5: QBrush(QColor(205, 0, 205)),
        6: QBrush(QColor(0, 205, 205)),
        7: QBrush(QColor(229, 229, 229)),
        10: QBrush(QColor(127, 127, 127)),
        11: QBrush(QColor(255, 0, 0)),
        12: QBrush(QColor(0, 255, 0)),
        13: QBrush(QColor(255, 255, 0)),
        14: QBrush(QColor(0, 0, 255)),
        15: QBrush(QColor(255, 0, 255)),
        16: QBrush(QColor(0, 255, 255)),
        17: QBrush(QColor(255, 255, 255)),
    },
    "Ubuntu": {
        0: QBrush(QColor(1, 1, 1)),
        1: QBrush(QColor(222, 56, 43)),
        2: QBrush(QColor(57, 181, 74)),
        3: QBrush(QColor(255, 199, 6)),
        4: QBrush(QColor(0, 11, 184)),
        5: QBrush(QColor(118, 38, 113)),
        6: QBrush(QColor(44, 181, 233)),
        7: QBrush(QColor(204, 204, 204)),
        10: QBrush(QColor(128, 128, 128)),
        11: QBrush(QColor(255, 0, 0)),
        12: QBrush(QColor(0, 255, 0)),
        13: QBrush(QColor(255, 255, 0)),
        14: QBrush(QColor(0, 0, 255)),
        15: QBrush(QColor(255, 0, 255)),
        16: QBrush(QColor(0, 255, 255)),
        17: QBrush(QColor(255, 255, 255)),
    },
    "Ubuntu (dark)": {
        0: QBrush(QColor(96, 96, 96)),
        1: QBrush(QColor(235, 58, 45)),
        2: QBrush(QColor(57, 181, 74)),
        3: QBrush(QColor(255, 199, 29)),
        4: QBrush(QColor(25, 56, 230)),
        5: QBrush(QColor(200, 64, 193)),
        6: QBrush(QColor(48, 200, 255)),
        7: QBrush(QColor(204, 204, 204)),
        10: QBrush(QColor(128, 128, 128)),
        11: QBrush(QColor(255, 0, 0)),
        12: QBrush(QColor(0, 255, 0)),
        13: QBrush(QColor(255, 255, 0)),
        14: QBrush(QColor(0, 0, 255)),
        15: QBrush(QColor(255, 0, 255)),
        16: QBrush(QColor(0, 255, 255)),
        17: QBrush(QColor(255, 255, 255)),
    },
    "Breeze (dark)": {
        0: QBrush(QColor(35, 38, 39)),
        1: QBrush(QColor(237, 21, 21)),
        2: QBrush(QColor(17, 209, 22)),
        3: QBrush(QColor(246, 116, 0)),
        4: QBrush(QColor(29, 153, 243)),
        5: QBrush(QColor(155, 89, 182)),
        6: QBrush(QColor(26, 188, 156)),
        7: QBrush(QColor(252, 252, 252)),
        10: QBrush(QColor(127, 140, 141)),
        11: QBrush(QColor(192, 57, 43)),
        12: QBrush(QColor(28, 220, 154)),
        13: QBrush(QColor(253, 188, 75)),
        14: QBrush(QColor(61, 174, 233)),
        15: QBrush(QColor(142, 68, 173)),
        16: QBrush(QColor(22, 160, 133)),
        17: QBrush(QColor(255, 255, 255)),
    },
}


class MicroPythonWidget(QWidget, Ui_MicroPythonWidget):
    """
    Class implementing the MicroPython REPL widget.
    
    @signal dataReceived(data) emitted to send data received via the serial
        connection for further processing
    """
    ZoomMin = -10
    ZoomMax = 20
    
    DeviceTypeRole = Qt.ItemDataRole.UserRole
    DeviceBoardRole = Qt.ItemDataRole.UserRole + 1
    DevicePortRole = Qt.ItemDataRole.UserRole + 2
    DeviceVidRole = Qt.ItemDataRole.UserRole + 3
    DevicePidRole = Qt.ItemDataRole.UserRole + 4
    
    dataReceived = pyqtSignal(bytes)
    
    ManualMarker = "<manual>"
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MicroPythonWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.__ui = parent
        
        self.__superMenu = QMenu(self)
        self.__superMenu.aboutToShow.connect(self.__aboutToShowSuperMenu)
        
        self.menuButton.setObjectName(
            "micropython_supermenu_button")
        self.menuButton.setIcon(UI.PixmapCache.getIcon("superMenu"))
        self.menuButton.setToolTip(self.tr("MicroPython Menu"))
        self.menuButton.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup)
        self.menuButton.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.menuButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.menuButton.setAutoRaise(True)
        self.menuButton.setShowMenuInside(True)
        self.menuButton.setMenu(self.__superMenu)
        
        self.deviceIconLabel.setPixmap(MicroPythonDevices.getDeviceIcon(
            "", False))
        
        self.openButton.setIcon(UI.PixmapCache.getIcon("open"))
        self.saveButton.setIcon(UI.PixmapCache.getIcon("fileSaveAs"))
        
        self.checkButton.setIcon(UI.PixmapCache.getIcon("question"))
        self.runButton.setIcon(UI.PixmapCache.getIcon("start"))
        self.replButton.setIcon(UI.PixmapCache.getIcon("terminal"))
        self.filesButton.setIcon(UI.PixmapCache.getIcon("filemanager"))
        self.chartButton.setIcon(UI.PixmapCache.getIcon("chart"))
        self.connectButton.setIcon(UI.PixmapCache.getIcon("linkConnect"))
        
        self.__zoomLayout = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                 QSizePolicy.Policy.Minimum)
        self.__zoomLayout.addSpacerItem(spacerItem)
        
        self.__zoom0 = self.replEdit.fontPointSize()
        self.__zoomWidget = E5ZoomWidget(
            UI.PixmapCache.getPixmap("zoomOut"),
            UI.PixmapCache.getPixmap("zoomIn"),
            UI.PixmapCache.getPixmap("zoomReset"), self)
        self.__zoomLayout.addWidget(self.__zoomWidget)
        self.layout().insertLayout(
            self.layout().count() - 1,
            self.__zoomLayout)
        self.__zoomWidget.setMinimum(self.ZoomMin)
        self.__zoomWidget.setMaximum(self.ZoomMax)
        self.__zoomWidget.valueChanged.connect(self.__doZoom)
        self.__currentZoom = 0
        
        self.__fileManagerWidget = None
        self.__chartWidget = None
        
        self.__unknownPorts = []
        self.__lastPort = None
        self.__lastDeviceType = None
        
        if HAS_QTSERIALPORT:
            self.__interface = MicroPythonCommandsInterface(self)
        else:
            self.__interface = None
        self.__device = None
        self.__connected = False
        self.__setConnected(False)
        
        if not HAS_QTSERIALPORT:
            self.replEdit.setHtml(self.tr(
                "<h3>The QtSerialPort package is not available.<br/>"
                "MicroPython support is deactivated.</h3>"))
            self.setEnabled(False)
            return
        
        self.__vt100Re = re.compile(
            r'(?P<count>\d*)(?P<color>(?:;?\d*)*)(?P<action>[ABCDKm])')
        
        self.__populateDeviceTypeComboBox()
        
        self.replEdit.installEventFilter(self)
        # Hack to intercept middle button paste
        self.__origReplEditMouseReleaseEvent = self.replEdit.mouseReleaseEvent
        self.replEdit.mouseReleaseEvent = self.__replEditMouseReleaseEvent
        
        self.replEdit.customContextMenuRequested.connect(
            self.__showContextMenu)
        self.__ui.preferencesChanged.connect(self.__handlePreferencesChanged)
        self.__ui.preferencesChanged.connect(
            self.__interface.handlePreferencesChanged)
        
        self.__handlePreferencesChanged()
        
        charFormat = self.replEdit.currentCharFormat()
        self.DefaultForeground = charFormat.foreground()
        self.DefaultBackground = charFormat.background()
    
    def __populateDeviceTypeComboBox(self):
        """
        Private method to populate the device type selector.
        """
        currentDevice = self.deviceTypeComboBox.currentText()
        
        self.deviceTypeComboBox.clear()
        self.deviceInfoLabel.clear()
        
        self.deviceTypeComboBox.addItem("", "")
        devices, unknownDevices, unknownPorts = (
            MicroPythonDevices.getFoundDevices()
        )
        if devices:
            supportedMessage = self.tr(
                "%n supported device(s) detected.", "", len(devices))
            
            for index, (boardType, boardName, description, portName,
                        vid, pid) in enumerate(sorted(devices), 1):
                self.deviceTypeComboBox.addItem(
                    self.tr("{0} - {1} ({2})",
                            "board name, description, port name")
                    .format(boardName, description, portName)
                )
                self.deviceTypeComboBox.setItemData(
                    index, boardType, self.DeviceTypeRole)
                self.deviceTypeComboBox.setItemData(
                    index, boardName, self.DeviceBoardRole)
                self.deviceTypeComboBox.setItemData(
                    index, portName, self.DevicePortRole)
                self.deviceTypeComboBox.setItemData(
                    index, vid, self.DeviceVidRole)
                self.deviceTypeComboBox.setItemData(
                    index, pid, self.DevicePidRole)
            
        else:
            supportedMessage = self.tr("No supported devices detected.")
        
        self.__unknownPorts = unknownPorts
        if self.__unknownPorts:
            unknownMessage = self.tr(
                "\n%n unknown device(s) for manual selection.", "",
                len(self.__unknownPorts))
            if self.deviceTypeComboBox.count():
                self.deviceTypeComboBox.insertSeparator(
                    self.deviceTypeComboBox.count())
            self.deviceTypeComboBox.addItem(self.tr("Manual Selection"))
            self.deviceTypeComboBox.setItemData(
                self.deviceTypeComboBox.count() - 1,
                self.ManualMarker, self.DeviceTypeRole)
        else:
            unknownMessage = ""
        
        self.deviceInfoLabel.setText(supportedMessage + unknownMessage)
        
        index = self.deviceTypeComboBox.findText(currentDevice,
                                                 Qt.MatchFlag.MatchExactly)
        if index == -1:
            # entry is no longer present
            index = 0
            if self.__connected:
                # we are still connected, so disconnect
                self.on_connectButton_clicked()
        
        self.on_deviceTypeComboBox_activated(index)
        self.deviceTypeComboBox.setCurrentIndex(index)
        
        if unknownDevices:
            ignoredUnknown = {
                tuple(d)
                for d in Preferences.getMicroPython("IgnoredUnknownDevices")
            }
            uf2Devices = {(*x[2], x[1])
                          for x in UF2FlashDialog.getFoundDevices()}
            newUnknownDevices = (
                set(unknownDevices) - ignoredUnknown - uf2Devices
            )
            if newUnknownDevices:
                button = E5MessageBox.information(
                    self,
                    self.tr("Unknown MicroPython Device"),
                    self.tr(
                        '<p>Detected these unknown serial devices</p>'
                        '<ul>'
                        '<li>{0}</li>'
                        '</ul>'
                        '<p>Please report them together with the board name'
                        ' and a short description to <a href="mailto:{1}">'
                        ' the eric bug reporting address</a> if it is a'
                        ' MicroPython board.</p>'
                    ).format("</li><li>".join([
                        self.tr("{0} (0x{1:04x}/0x{2:04x})",
                                "description, VId, PId").format(
                            desc, vid, pid)
                        for vid, pid, desc in newUnknownDevices]),
                        BugAddress),
                    E5MessageBox.StandardButtons(
                        E5MessageBox.Ignore |
                        E5MessageBox.Ok
                    )
                )
                if button == E5MessageBox.Ignore:
                    ignoredUnknown = list(ignoredUnknown | newUnknownDevices)
                    Preferences.setMicroPython("IgnoredUnknownDevices",
                                               ignoredUnknown)
                else:
                    yes = E5MessageBox.yesNo(
                        self,
                        self.tr("Unknown MicroPython Device"),
                        self.tr("""Would you like to add them to the list of"""
                                """ manually configured devices?"""),
                        yesDefault=True)
                    if yes:
                        self.__addUnknownDevices(list(newUnknownDevices))
    
    def __handlePreferencesChanged(self):
        """
        Private slot to handle a change in preferences.
        """
        self.__colorScheme = Preferences.getMicroPython("ColorScheme")
        
        self.__font = Preferences.getEditorOtherFonts("MonospacedFont")
        self.replEdit.setFontFamily(self.__font.family())
        self.replEdit.setFontPointSize(self.__font.pointSize())
        
        if Preferences.getMicroPython("ReplLineWrap"):
            self.replEdit.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        else:
            self.replEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        
        if self.__chartWidget is not None:
            self.__chartWidget.preferencesChanged()
    
    def commandsInterface(self):
        """
        Public method to get a reference to the commands interface object.
        
        @return reference to the commands interface object
        @rtype MicroPythonCommandsInterface
        """
        return self.__interface
    
    def isMicrobit(self):
        """
        Public method to check, if the connected/selected device is a
        BBC micro:bit or Calliope mini.
        
        @return flag indicating a micro:bit device
        rtype bool
        """
        if self.__device and (
            "micro:bit" in self.__device.deviceName() or
            "Calliope" in self.__device.deviceName()
        ):
            return True
        
        return False
    
    @pyqtSlot(int)
    def on_deviceTypeComboBox_activated(self, index):
        """
        Private slot handling the selection of a device type.
        
        @param index index of the selected device
        @type int
        """
        deviceType = self.deviceTypeComboBox.itemData(
            index, self.DeviceTypeRole)
        if deviceType == self.ManualMarker:
            self.connectButton.setEnabled(bool(self.__unknownPorts))
        else:
            self.deviceIconLabel.setPixmap(MicroPythonDevices.getDeviceIcon(
                deviceType, False))
            
            vid = self.deviceTypeComboBox.itemData(
                index, self.DeviceVidRole)
            pid = self.deviceTypeComboBox.itemData(
                index, self.DevicePidRole)
            
            self.__device = MicroPythonDevices.getDevice(deviceType, self,
                                                         vid, pid)
            self.__device.setButtons()
            
            self.connectButton.setEnabled(bool(deviceType))
    
    @pyqtSlot()
    def on_checkButton_clicked(self):
        """
        Private slot to check for connected devices.
        """
        self.__populateDeviceTypeComboBox()
    
    def setActionButtons(self, **kwargs):
        """
        Public method to set the enabled state of the various action buttons.
        
        @keyparam kwargs keyword arguments containg the enabled states (keys
            are 'run', 'repl', 'files', 'chart', 'open', 'save'
        @type dict
        """
        if "open" in kwargs:
            self.openButton.setEnabled(kwargs["open"])
        if "save" in kwargs:
            self.saveButton.setEnabled(kwargs["save"])
        if "run" in kwargs:
            self.runButton.setEnabled(kwargs["run"])
        if "repl" in kwargs:
            self.replButton.setEnabled(kwargs["repl"])
        if "files" in kwargs:
            self.filesButton.setEnabled(kwargs["files"])
        if "chart" in kwargs:
            self.chartButton.setEnabled(kwargs["chart"] and HAS_QTCHART)
    
    @pyqtSlot(QPoint)
    def __showContextMenu(self, pos):
        """
        Private slot to show the REPL context menu.
        
        @param pos position to show the menu at
        @type QPoint
        """
        if Globals.isMacPlatform():
            copyKeys = QKeySequence(Qt.Modifier.CTRL + Qt.Key.Key_C)
            pasteKeys = QKeySequence(Qt.Modifier.CTRL + Qt.Key.Key_V)
        else:
            copyKeys = QKeySequence(
                Qt.Modifier.CTRL + Qt.Modifier.SHIFT + Qt.Key.Key_C)
            pasteKeys = QKeySequence(
                Qt.Modifier.CTRL + Qt.Modifier.SHIFT + Qt.Key.Key_V)
        menu = QMenu(self)
        menu.addAction(self.tr("Clear"), self.__clear)
        menu.addSeparator()
        menu.addAction(self.tr("Copy"), self.replEdit.copy, copyKeys)
        menu.addAction(self.tr("Paste"), self.__paste, pasteKeys)
        menu.addSeparator()
        menu.exec(self.replEdit.mapToGlobal(pos))
    
    def __setConnected(self, connected):
        """
        Private method to set the connection status LED.
        
        @param connected connection state
        @type bool
        """
        self.__connected = connected
        
        self.deviceConnectedLed.setOn(connected)
        if self.__fileManagerWidget:
            self.__fileManagerWidget.deviceConnectedLed.setOn(connected)
        
        self.deviceTypeComboBox.setEnabled(not connected)
        
        if connected:
            self.connectButton.setIcon(
                UI.PixmapCache.getIcon("linkDisconnect"))
            self.connectButton.setToolTip(self.tr(
                "Press to disconnect the current device"))
        else:
            self.connectButton.setIcon(
                UI.PixmapCache.getIcon("linkConnect"))
            self.connectButton.setToolTip(self.tr(
                "Press to connect the selected device"))
    
    def isConnected(self):
        """
        Public method to get the connection state.
        
        @return connection state
        @rtype bool
        """
        return self.__connected
    
    def __showNoDeviceMessage(self):
        """
        Private method to show a message dialog indicating a missing device.
        """
        E5MessageBox.critical(
            self,
            self.tr("No device attached"),
            self.tr("""Please ensure the device is plugged into your"""
                    """ computer and selected.\n\nIt must have a version"""
                    """ of MicroPython (or CircuitPython) flashed onto"""
                    """ it before anything will work.\n\nFinally press"""
                    """ the device's reset button and wait a few seconds"""
                    """ before trying again."""))
    
    @pyqtSlot(bool)
    def on_replButton_clicked(self, checked):
        """
        Private slot to connect to enable or disable the REPL widget.
       
        If the selected device is not connected yet, this will be done now.
        
        @param checked state of the button
        @type bool
        """
        if not self.__device:
            self.__showNoDeviceMessage()
            return
        
        if checked:
            ok, reason = self.__device.canStartRepl()
            if not ok:
                E5MessageBox.warning(
                    self,
                    self.tr("Start REPL"),
                    self.tr("""<p>The REPL cannot be started.</p><p>Reason:"""
                            """ {0}</p>""").format(reason))
                return
            
            self.replEdit.clear()
            self.__interface.dataReceived.connect(self.__processData)
            
            if not self.__interface.isConnected():
                self.__connectToDevice()
                if self.__device.forceInterrupt():
                    # send a Ctrl-B (exit raw mode)
                    self.__interface.write(b'\x02')
                    # send Ctrl-C (keyboard interrupt)
                    self.__interface.write(b'\x03')
            
            self.__device.setRepl(True)
            self.replEdit.setFocus(Qt.FocusReason.OtherFocusReason)
        else:
            self.__interface.dataReceived.disconnect(self.__processData)
            if (not self.chartButton.isChecked() and
                    not self.filesButton.isChecked()):
                self.__disconnectFromDevice()
            self.__device.setRepl(False)
        self.replButton.setChecked(checked)
    
    @pyqtSlot()
    def on_connectButton_clicked(self):
        """
        Private slot to connect to the selected device or disconnect from the
        currently connected device.
        """
        if self.__connected:
            with E5OverrideCursor():
                self.__disconnectFromDevice()
            
            if self.replButton.isChecked():
                self.on_replButton_clicked(False)
            if self.filesButton.isChecked():
                self.on_filesButton_clicked(False)
            if self.chartButton.isChecked():
                self.on_chartButton_clicked(False)
        else:
            with E5OverrideCursor():
                self.__connectToDevice()
    
    @pyqtSlot()
    def __clear(self):
        """
        Private slot to clear the REPL pane.
        """
        self.replEdit.clear()
        self.__interface.isConnected() and self.__interface.write(b"\r")
    
    @pyqtSlot()
    def __paste(self, mode=QClipboard.Mode.Clipboard):
        """
        Private slot to perform a paste operation.
        
        @param mode paste mode (defaults to QClipboard.Mode.Clipboard)
        @type QClipboard.Mode (optional)
        """
        # add support for paste by mouse middle button
        clipboard = QApplication.clipboard()
        if clipboard:
            pasteText = clipboard.text(mode=mode)
            if pasteText:
                pasteText = pasteText.replace('\n\r', '\r')
                pasteText = pasteText.replace('\n', '\r')
                self.__interface.isConnected() and self.__interface.write(
                    pasteText.encode("utf-8"))
    
    def eventFilter(self, obj, evt):
        """
        Public method to process events for the REPL pane.
        
        @param obj reference to the object the event was meant for
        @type QObject
        @param evt reference to the event object
        @type QEvent
        @return flag to indicate that the event was handled
        @rtype bool
        """
        if obj is self.replEdit and evt.type() == QEvent.Type.KeyPress:
            # handle the key press event on behalve of the REPL pane
            key = evt.key()
            msg = bytes(evt.text(), 'utf8')
            if key == Qt.Key.Key_Backspace:
                msg = b'\b'
            elif key == Qt.Key.Key_Delete:
                msg = b'\x1B[\x33\x7E'
            elif key == Qt.Key.Key_Up:
                msg = b'\x1B[A'
            elif key == Qt.Key.Key_Down:
                msg = b'\x1B[B'
            elif key == Qt.Key.Key_Right:
                msg = b'\x1B[C'
            elif key == Qt.Key.Key_Left:
                msg = b'\x1B[D'
            elif key == Qt.Key.Key_Home:
                msg = b'\x1B[H'
            elif key == Qt.Key.Key_End:
                msg = b'\x1B[F'
            elif ((Globals.isMacPlatform() and
                   evt.modifiers() == Qt.KeyboardModifier.MetaModifier) or
                  (not Globals.isMacPlatform() and
                   evt.modifiers() == Qt.KeyboardModifier.ControlModifier)):
                if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
                    # devices treat an input of \x01 as Ctrl+A, etc.
                    msg = bytes([1 + key - Qt.Key.Key_A])
            elif (
                evt.modifiers() == (
                    Qt.KeyboardModifier.ControlModifier |
                    Qt.KeyboardModifier.ShiftModifier) or
                (Globals.isMacPlatform() and
                 evt.modifiers() == Qt.KeyboardModifier.ControlModifier)
            ):
                if key == Qt.Key.Key_C:
                    self.replEdit.copy()
                    msg = b''
                elif key == Qt.Key.Key_V:
                    self.__paste()
                    msg = b''
            elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                tc = self.replEdit.textCursor()
                tc.movePosition(QTextCursor.MoveOperation.EndOfLine)
                self.replEdit.setTextCursor(tc)
            self.__interface.isConnected() and self.__interface.write(msg)
            return True
        else:
            # standard event processing
            return super(MicroPythonWidget, self).eventFilter(obj, evt)
    
    def __replEditMouseReleaseEvent(self, evt):
        """
        Private method handling mouse release events for the replEdit widget.
        
        Note: this is a hack because QTextEdit does not allow filtering of
        QEvent.Type.MouseButtonRelease. To make middle button paste work, we
        had to intercept the protected event method (some kind of
        reimplementing it).
        
        @param evt reference to the event object
        @type QMouseEvent
        """
        if evt.button() == Qt.MouseButton.MiddleButton:
            self.__paste(mode=QClipboard.Mode.Selection)
            msg = b''
            if self.__interface.isConnected():
                self.__interface.write(msg)
            evt.accept()
        else:
            self.__origReplEditMouseReleaseEvent(evt)
    
    def __processData(self, data):
        """
        Private slot to process bytes received from the device.
        
        @param data bytes received from the device
        @type bytes
        """
        tc = self.replEdit.textCursor()
        # the text cursor must be on the last line
        while tc.movePosition(QTextCursor.MoveOperation.Down):
            pass
        
        # set the font
        charFormat = tc.charFormat()
        charFormat.setFontFamily(self.__font.family())
        charFormat.setFontPointSize(self.__font.pointSize())
        tc.setCharFormat(charFormat)
        
        index = 0
        while index < len(data):
            if data[index] == 8:        # \b
                tc.movePosition(QTextCursor.MoveOperation.Left)
                self.replEdit.setTextCursor(tc)
            elif data[index] in (4, 13):     # EOT, \r
                pass
            elif (len(data) > index + 1 and
                  data[index] == 27 and
                  data[index + 1] == 91):
                # VT100 cursor command detected: <Esc>[
                index += 2      # move index to after the [
                match = self.__vt100Re.search(data[index:].decode("utf-8"))
                if match:
                    # move to last position in control sequence
                    # ++ will be done at end of loop
                    index += match.end() - 1
                    
                    action = match.group("action")
                    if action in "ABCD":
                        if match.group("count") == "":
                            count = 1
                        else:
                            count = int(match.group("count"))
                        
                        if action == "A":       # up
                            tc.movePosition(QTextCursor.MoveOperation.Up,
                                            n=count)
                            self.replEdit.setTextCursor(tc)
                        elif action == "B":     # down
                            tc.movePosition(QTextCursor.MoveOperation.Down,
                                            n=count)
                            self.replEdit.setTextCursor(tc)
                        elif action == "C":     # right
                            tc.movePosition(QTextCursor.MoveOperation.Right,
                                            n=count)
                            self.replEdit.setTextCursor(tc)
                        elif action == "D":     # left
                            tc.movePosition(QTextCursor.MoveOperation.Left,
                                            n=count)
                            self.replEdit.setTextCursor(tc)
                    elif action == "K":     # delete things
                        if match.group("count") in ("", "0"):
                            # delete to end of line
                            tc.movePosition(
                                QTextCursor.MoveOperation.EndOfLine,
                                mode=QTextCursor.MoveMode.KeepAnchor)
                            tc.removeSelectedText()
                            self.replEdit.setTextCursor(tc)
                        elif match.group("count") == "1":
                            # delete to beinning of line
                            tc.movePosition(
                                QTextCursor.MoveOperation.StartOfLine,
                                mode=QTextCursor.MoveMode.KeepAnchor)
                            tc.removeSelectedText()
                            self.replEdit.setTextCursor(tc)
                        elif match.group("count") == "2":
                            # delete whole line
                            tc.movePosition(
                                QTextCursor.MoveOperation.EndOfLine)
                            tc.movePosition(
                                QTextCursor.MoveOperation.StartOfLine,
                                mode=QTextCursor.MoveMode.KeepAnchor)
                            tc.removeSelectedText()
                            self.replEdit.setTextCursor(tc)
                    elif action == "m":
                        self.__setCharFormat(match.group(0)[:-1].split(";"),
                                             tc)
            else:
                tc.deleteChar()
                self.replEdit.setTextCursor(tc)
                self.replEdit.insertPlainText(chr(data[index]))
            
            index += 1
        
        self.replEdit.ensureCursorVisible()
    
    def __setCharFormat(self, formatCodes, textCursor):
        """
        Private method setting the current text format of the REPL pane based
        on the passed ANSI codes.
        
        Following codes are used:
        <ul>
        <li>0: Reset</li>
        <li>1: Bold font (weight 75)</li>
        <li>2: Light font (weight 25)</li>
        <li>3: Italic font</li>
        <li>4: Underlined font</li>
        <li>9: Strikeout font</li>
        <li>21: Bold off (weight 50)</li>
        <li>22: Light off (weight 50)</li>
        <li>23: Italic off</li>
        <li>24: Underline off</li>
        <li>29: Strikeout off</li>
        <li>30: foreground Black</li>
        <li>31: foreground Dark Red</li>
        <li>32: foreground Dark Green</li>
        <li>33: foreground Dark Yellow</li>
        <li>34: foreground Dark Blue</li>
        <li>35: foreground Dark Magenta</li>
        <li>36: foreground Dark Cyan</li>
        <li>37: foreground Light Gray</li>
        <li>39: reset foreground to default</li>
        <li>40: background Black</li>
        <li>41: background Dark Red</li>
        <li>42: background Dark Green</li>
        <li>43: background Dark Yellow</li>
        <li>44: background Dark Blue</li>
        <li>45: background Dark Magenta</li>
        <li>46: background Dark Cyan</li>
        <li>47: background Light Gray</li>
        <li>49: reset background to default</li>
        <li>53: Overlined font</li>
        <li>55: Overline off</li>
        <li>90: bright foreground Dark Gray</li>
        <li>91: bright foreground Red</li>
        <li>92: bright foreground Green</li>
        <li>93: bright foreground Yellow</li>
        <li>94: bright foreground Blue</li>
        <li>95: bright foreground Magenta</li>
        <li>96: bright foreground Cyan</li>
        <li>97: bright foreground White</li>
        <li>100: bright background Dark Gray</li>
        <li>101: bright background Red</li>
        <li>102: bright background Green</li>
        <li>103: bright background Yellow</li>
        <li>104: bright background Blue</li>
        <li>105: bright background Magenta</li>
        <li>106: bright background Cyan</li>
        <li>107: bright background White</li>
        </ul>
        
        @param formatCodes list of format codes
        @type list of str
        @param textCursor reference to the text cursor
        @type QTextCursor
        """
        if not formatCodes:
            # empty format codes list is treated as a reset
            formatCodes = ["0"]
        
        charFormat = textCursor.charFormat()
        for formatCode in formatCodes:
            try:
                formatCode = int(formatCode)
            except ValueError:
                # ignore non digit values
                continue
            
            if formatCode == 0:
                charFormat.setFontWeight(50)
                charFormat.setFontItalic(False)
                charFormat.setFontUnderline(False)
                charFormat.setFontStrikeOut(False)
                charFormat.setFontOverline(False)
                charFormat.setForeground(self.DefaultForeground)
                charFormat.setBackground(self.DefaultBackground)
            elif formatCode == 1:
                charFormat.setFontWeight(75)
            elif formatCode == 2:
                charFormat.setFontWeight(25)
            elif formatCode == 3:
                charFormat.setFontItalic(True)
            elif formatCode == 4:
                charFormat.setFontUnderline(True)
            elif formatCode == 9:
                charFormat.setFontStrikeOut(True)
            elif formatCode in (21, 22):
                charFormat.setFontWeight(50)
            elif formatCode == 23:
                charFormat.setFontItalic(False)
            elif formatCode == 24:
                charFormat.setFontUnderline(False)
            elif formatCode == 29:
                charFormat.setFontStrikeOut(False)
            elif formatCode == 53:
                charFormat.setFontOverline(True)
            elif formatCode == 55:
                charFormat.setFontOverline(False)
            elif formatCode in (30, 31, 32, 33, 34, 35, 36, 37):
                charFormat.setForeground(
                    AnsiColorSchemes[self.__colorScheme][formatCode - 30])
            elif formatCode in (40, 41, 42, 43, 44, 45, 46, 47):
                charFormat.setBackground(
                    AnsiColorSchemes[self.__colorScheme][formatCode - 40])
            elif formatCode in (90, 91, 92, 93, 94, 95, 96, 97):
                charFormat.setForeground(
                    AnsiColorSchemes[self.__colorScheme][formatCode - 80])
            elif formatCode in (100, 101, 102, 103, 104, 105, 106, 107):
                charFormat.setBackground(
                    AnsiColorSchemes[self.__colorScheme][formatCode - 90])
            elif formatCode == 39:
                charFormat.setForeground(self.DefaultForeground)
            elif formatCode == 49:
                charFormat.setBackground(self.DefaultBackground)
        
        textCursor.setCharFormat(charFormat)
    
    def __doZoom(self, value):
        """
        Private slot to zoom the REPL pane.
        
        @param value zoom value
        @type int
        """
        if value < self.__currentZoom:
            self.replEdit.zoomOut(self.__currentZoom - value)
        elif value > self.__currentZoom:
            self.replEdit.zoomIn(value - self.__currentZoom)
        self.__currentZoom = value
    
    def getCurrentPort(self):
        """
        Public method to determine the port path of the selected device.
        
        @return path of the port of the selected device
        @rtype str
        """
        portName = self.deviceTypeComboBox.currentData(self.DevicePortRole)
        if portName:
            if Globals.isWindowsPlatform():
                # return it unchanged
                return portName
            else:
                # return with device path prepended
                return "/dev/{0}".format(portName)
        else:
            return ""
    
    def getCurrentBoard(self):
        """
        Public method to get the board name of the selected device.
        
        @return board name of the selected device
        @rtype str
        """
        boardName = self.deviceTypeComboBox.currentData(self.DeviceBoardRole)
        return boardName
    
    def getDeviceWorkspace(self):
        """
        Public method to get the workspace directory of the device.
        
        @return workspace directory of the device
        @rtype str
        """
        if self.__device:
            return self.__device.getWorkspace()
        else:
            return ""
    
    def __connectToDevice(self):
        """
        Private method to connect to the selected device.
        """
        port = self.getCurrentPort()
        if not port:
            from .ConnectionSelectionDialog import ConnectionSelectionDialog
            with E5OverridenCursor():
                dlg = ConnectionSelectionDialog(
                    self.__unknownPorts, self.__lastPort, self.__lastDeviceType
                )
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    vid, pid, port, deviceType = dlg.getData()
                    
                    self.deviceIconLabel.setPixmap(
                        MicroPythonDevices.getDeviceIcon(deviceType, False))
                    self.__device = MicroPythonDevices.getDevice(
                        deviceType, self, vid, pid)
                    self.__device.setButtons()
                    
                    self.__lastPort = port
                    self.__lastDeviceType = deviceType
                else:
                    return
        
        if self.__interface.connectToDevice(port):
            self.__setConnected(True)
            
            if (Preferences.getMicroPython("SyncTimeAfterConnect") and
                    self.__device.hasTimeCommands()):
                self.__synchronizeTime(quiet=True)
        else:
            with E5OverridenCursor():
                E5MessageBox.warning(
                    self,
                    self.tr("Serial Device Connect"),
                    self.tr("""<p>Cannot connect to device at serial"""
                            """ port <b>{0}</b>.</p>""").format(port))
    
    def __disconnectFromDevice(self):
        """
        Private method to disconnect from the device.
        """
        self.__interface.disconnectFromDevice()
        self.__setConnected(False)
    
    @pyqtSlot()
    def on_runButton_clicked(self):
        """
        Private slot to execute the script of the active editor on the
        selected device.
        
        If the REPL is not active yet, it will be activated, which might cause
        an unconnected device to be connected.
        """
        if not self.__device:
            self.__showNoDeviceMessage()
            return
        
        aw = e5App().getObject("ViewManager").activeWindow()
        if aw is None:
            E5MessageBox.critical(
                self,
                self.tr("Run Script"),
                self.tr("""There is no editor open. Abort..."""))
            return
        
        script = aw.text()
        if not script:
            E5MessageBox.critical(
                self,
                self.tr("Run Script"),
                self.tr("""The current editor does not contain a script."""
                        """ Abort..."""))
            return
        
        ok, reason = self.__device.canRunScript()
        if not ok:
            E5MessageBox.warning(
                self,
                self.tr("Run Script"),
                self.tr("""<p>Cannot run script.</p><p>Reason:"""
                        """ {0}</p>""").format(reason))
            return
        
        if not self.replButton.isChecked():
            # activate on the REPL
            self.on_replButton_clicked(True)
        if self.replButton.isChecked():
            self.__device.runScript(script)
    
    @pyqtSlot()
    def on_openButton_clicked(self):
        """
        Private slot to open a file of the connected device.
        """
        if not self.__device:
            self.__showNoDeviceMessage()
            return
        
        workspace = self.getDeviceWorkspace()
        if workspace:
            fileName = E5FileDialog.getOpenFileName(
                self,
                self.tr("Open Python File"),
                workspace,
                self.tr("Python3 Files (*.py);;All Files (*)"))
            if fileName:
                e5App().getObject("ViewManager").openSourceFile(fileName)
    
    @pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Private slot to save the current editor to the connected device.
        """
        if not self.__device:
            self.__showNoDeviceMessage()
            return
        
        aw = e5App().getObject("ViewManager").activeWindow()
        if aw:
            workspace = self.getDeviceWorkspace()
            if workspace:
                aw.saveFileAs(workspace)
    
    @pyqtSlot(bool)
    def on_chartButton_clicked(self, checked):
        """
        Private slot to open a chart view to plot data received from the
        connected device.
       
        If the selected device is not connected yet, this will be done now.
        
        @param checked state of the button
        @type bool
        """
        if not HAS_QTCHART:
            # QtChart not available => fail silently
            return
        
        if not self.__device:
            self.__showNoDeviceMessage()
            return
        
        if checked:
            ok, reason = self.__device.canStartPlotter()
            if not ok:
                E5MessageBox.warning(
                    self,
                    self.tr("Start Chart"),
                    self.tr("""<p>The Chart cannot be started.</p><p>Reason:"""
                            """ {0}</p>""").format(reason))
                return
            
            self.__chartWidget = MicroPythonGraphWidget(self)
            self.__interface.dataReceived.connect(
                self.__chartWidget.processData)
            self.__chartWidget.dataFlood.connect(
                self.handleDataFlood)
            
            self.__ui.addSideWidget(self.__ui.BottomSide, self.__chartWidget,
                                    UI.PixmapCache.getIcon("chart"),
                                    self.tr("µPy Chart"))
            self.__ui.showSideWidget(self.__chartWidget)
            
            if not self.__interface.isConnected():
                self.__connectToDevice()
                if self.__device.forceInterrupt():
                    # send a Ctrl-B (exit raw mode)
                    self.__interface.write(b'\x02')
                    # send Ctrl-C (keyboard interrupt)
                    self.__interface.write(b'\x03')
            
            self.__device.setPlotter(True)
        else:
            if self.__chartWidget.isDirty():
                res = E5MessageBox.okToClearData(
                    self,
                    self.tr("Unsaved Chart Data"),
                    self.tr("""The chart contains unsaved data."""),
                    self.__chartWidget.saveData)
                if not res:
                    # abort
                    return
            
            self.__interface.dataReceived.disconnect(
                self.__chartWidget.processData)
            self.__chartWidget.dataFlood.disconnect(
                self.handleDataFlood)
            
            if (not self.replButton.isChecked() and
                    not self.filesButton.isChecked()):
                self.__disconnectFromDevice()
            
            self.__device.setPlotter(False)
            self.__ui.removeSideWidget(self.__chartWidget)
            
            self.__chartWidget.deleteLater()
            self.__chartWidget = None
        
        self.chartButton.setChecked(checked)
    
    @pyqtSlot()
    def handleDataFlood(self):
        """
        Public slot handling a data flood from the device.
        """
        self.on_connectButton_clicked()
        self.__device.handleDataFlood()
    
    @pyqtSlot(bool)
    def on_filesButton_clicked(self, checked):
        """
        Private slot to open a file manager window to the connected device.
       
        If the selected device is not connected yet, this will be done now.
        
        @param checked state of the button
        @type bool
        """
        if not self.__device:
            self.__showNoDeviceMessage()
            return
        
        if checked:
            ok, reason = self.__device.canStartFileManager()
            if not ok:
                E5MessageBox.warning(
                    self,
                    self.tr("Start File Manager"),
                    self.tr("""<p>The File Manager cannot be started.</p>"""
                            """<p>Reason: {0}</p>""").format(reason))
                return
            
            with E5OverrideCursor():
                if not self.__interface.isConnected():
                    self.__connectToDevice()
                if self.__connected:
                    self.__fileManagerWidget = MicroPythonFileManagerWidget(
                        self.__interface,
                        self.__device.supportsLocalFileAccess(),
                        self)
                    
                    self.__ui.addSideWidget(
                        self.__ui.BottomSide,
                        self.__fileManagerWidget,
                        UI.PixmapCache.getIcon("filemanager"),
                        self.tr("µPy Files")
                    )
                    self.__ui.showSideWidget(self.__fileManagerWidget)

                    self.__device.setFileManager(True)
                    
                    self.__fileManagerWidget.start()
        else:
            self.__fileManagerWidget.stop()
            
            if (not self.replButton.isChecked() and
                    not self.chartButton.isChecked()):
                self.__disconnectFromDevice()
            
            self.__device.setFileManager(False)
            self.__ui.removeSideWidget(self.__fileManagerWidget)
            
            self.__fileManagerWidget.deleteLater()
            self.__fileManagerWidget = None
        
        self.filesButton.setChecked(checked)
    
    ##################################################################
    ## Super Menu related methods below
    ##################################################################
    
    def __aboutToShowSuperMenu(self):
        """
        Private slot to populate the Super Menu before showing it.
        """
        self.__superMenu.clear()
        
        # prepare the download menu
        if self.__device:
            menuEntries = self.__device.getDownloadMenuEntries()
            if menuEntries:
                downloadMenu = QMenu(self.tr("Downloads"), self.__superMenu)
                for text, url in menuEntries:
                    if text == "<separator>":
                        downloadMenu.addSeparator()
                    else:
                        downloadMenu.addAction(
                            text,
                            functools.partial(self.__downloadFromUrl, url)
                        )
            else:
                downloadMenu = None
        
        # populate the super menu
        if self.__device:
            hasTime = self.__device.hasTimeCommands()
        else:
            hasTime = False
        
        act = self.__superMenu.addAction(
            self.tr("Show Version"), self.__showDeviceVersion)
        act.setEnabled(self.__connected)
        act = self.__superMenu.addAction(
            self.tr("Show Implementation"), self.__showImplementation)
        act.setEnabled(self.__connected)
        self.__superMenu.addSeparator()
        if hasTime:
            act = self.__superMenu.addAction(
                self.tr("Synchronize Time"), self.__synchronizeTime)
            act.setEnabled(self.__connected)
            act = self.__superMenu.addAction(
                self.tr("Show Device Time"), self.__showDeviceTime)
            act.setEnabled(self.__connected)
        self.__superMenu.addAction(
            self.tr("Show Local Time"), self.__showLocalTime)
        if hasTime:
            act = self.__superMenu.addAction(
                self.tr("Show Time"), self.__showLocalAndDeviceTime)
            act.setEnabled(self.__connected)
        self.__superMenu.addSeparator()
        if not Globals.isWindowsPlatform():
            available = self.__mpyCrossAvailable()
            act = self.__superMenu.addAction(
                self.tr("Compile Python File"), self.__compileFile2Mpy)
            act.setEnabled(available)
            act = self.__superMenu.addAction(
                self.tr("Compile Current Editor"), self.__compileEditor2Mpy)
            aw = e5App().getObject("ViewManager").activeWindow()
            act.setEnabled(available and bool(aw))
            self.__superMenu.addSeparator()
        if self.__device:
            self.__device.addDeviceMenuEntries(self.__superMenu)
            self.__superMenu.addSeparator()
            if downloadMenu is None:
                # generic download action
                act = self.__superMenu.addAction(
                    self.tr("Download Firmware"), self.__downloadFirmware)
                act.setEnabled(self.__device.hasFirmwareUrl())
            else:
                # download sub-menu
                self.__superMenu.addMenu(downloadMenu)
            self.__superMenu.addSeparator()
            act = self.__superMenu.addAction(
                self.tr("Show Documentation"), self.__showDocumentation)
            act.setEnabled(self.__device.hasDocumentationUrl())
            self.__superMenu.addSeparator()
        if not self.__device.hasFlashMenuEntry():
            self.__superMenu.addAction(self.tr("Flash UF2 Device"),
                                       self.__flashUF2)
            self.__superMenu.addSeparator()
        self.__superMenu.addAction(self.tr("Manage Unknown Devices"),
                                   self.__manageUnknownDevices)
        self.__superMenu.addAction(self.tr("Ignored Serial Devices"),
                                   self.__manageIgnored)
        self.__superMenu.addSeparator()
        self.__superMenu.addAction(self.tr("Configure"), self.__configure)
    
    @pyqtSlot()
    def __showDeviceVersion(self):
        """
        Private slot to show some version info about MicroPython of the device.
        """
        try:
            versionInfo = self.__interface.version()
            if versionInfo:
                msg = self.tr(
                    "<h3>Device Version Information</h3>"
                )
                msg += "<table>"
                for key, value in versionInfo.items():
                    msg += "<tr><td><b>{0}</b></td><td>{1}</td></tr>".format(
                        key.capitalize(), value)
                msg += "</table>"
            else:
                msg = self.tr("No version information available.")
            
            E5MessageBox.information(
                self,
                self.tr("Device Version Information"),
                msg)
        except Exception as exc:
            self.__showError("version()", str(exc))
    
    @pyqtSlot()
    def __showImplementation(self):
        """
        Private slot to show some implementation related information.
        """
        try:
            impInfo = self.__interface.getImplementation()
            if impInfo["name"] == "micropython":
                name = "MicroPython"
            elif impInfo["name"] == "circuitpython":
                name = "CircuitPython"
            elif impInfo["name"] == "unknown":
                name = self.tr("unknown")
            else:
                name = impInfo["name"]
            if impInfo["version"] == "unknown":
                version = self.tr("unknown")
            else:
                version = impInfo["version"]
            
            E5MessageBox.information(
                self,
                self.tr("Device Implementation Information"),
                self.tr(
                    "<h3>Device Implementation Information</h3>"
                    "<p>This device contains <b>{0} {1}</b>.</p>"
                ).format(name, version)
            )
        except Exception as exc:
            self.__showError("getImplementation()", str(exc))
    
    @pyqtSlot()
    def __synchronizeTime(self, quiet=False):
        """
        Private slot to set the time of the connected device to the local
        computer's time.
        
        @param quiet flag indicating to not show a message
        @type bool
        """
        if self.__device and self.__device.hasTimeCommands():
            try:
                self.__interface.syncTime(self.__device.getDeviceType())
                
                if not quiet:
                    with E5OverridenCursor():
                        E5MessageBox.information(
                            self,
                            self.tr("Synchronize Time"),
                            self.tr("<p>The time of the connected device was"
                                    " synchronized with the local time.</p>") +
                            self.__getDeviceTime()
                        )
            except Exception as exc:
                self.__showError("syncTime()", str(exc))
    
    def __getDeviceTime(self):
        """
        Private method to get a string containing the date and time of the
        connected device.
        
        @return date and time of the connected device
        @rtype str
        """
        if self.__device and self.__device.hasTimeCommands():
            try:
                dateTimeString = self.__interface.getTime()
                try:
                    date, time = dateTimeString.strip().split(None, 1)
                    return self.tr(
                        "<h3>Device Date and Time</h3>"
                        "<table>"
                        "<tr><td><b>Date</b></td><td>{0}</td></tr>"
                        "<tr><td><b>Time</b></td><td>{1}</td></tr>"
                        "</table>"
                    ).format(date, time)
                except ValueError:
                    return self.tr(
                        "<h3>Device Date and Time</h3>"
                        "<p>{0}</p>"
                    ).format(dateTimeString.strip())
            except Exception as exc:
                self.__showError("getTime()", str(exc))
                return ""
        else:
            return ""
    
    @pyqtSlot()
    def __showDeviceTime(self):
        """
        Private slot to show the date and time of the connected device.
        """
        msg = self.__getDeviceTime()
        if msg:
            E5MessageBox.information(
                self,
                self.tr("Device Date and Time"),
                msg)
    
    @pyqtSlot()
    def __showLocalTime(self):
        """
        Private slot to show the local date and time.
        """
        localdatetime = time.localtime()
        localdate = time.strftime('%Y-%m-%d', localdatetime)
        localtime = time.strftime('%H:%M:%S', localdatetime)
        E5MessageBox.information(
            self,
            self.tr("Local Date and Time"),
            self.tr("<h3>Local Date and Time</h3>"
                    "<table>"
                    "<tr><td><b>Date</b></td><td>{0}</td></tr>"
                    "<tr><td><b>Time</b></td><td>{1}</td></tr>"
                    "</table>"
                    ).format(localdate, localtime)
        )
    
    @pyqtSlot()
    def __showLocalAndDeviceTime(self):
        """
        Private slot to show the local and device time side-by-side.
        """
        localdatetime = time.localtime()
        localdate = time.strftime('%Y-%m-%d', localdatetime)
        localtime = time.strftime('%H:%M:%S', localdatetime)
        
        try:
            deviceDateTimeString = self.__interface.getTime()
            try:
                devicedate, devicetime = (
                    deviceDateTimeString.strip().split(None, 1)
                )
                E5MessageBox.information(
                    self,
                    self.tr("Date and Time"),
                    self.tr("<table>"
                            "<tr><th></th><th>Local Date and Time</th>"
                            "<th>Device Date and Time</th></tr>"
                            "<tr><td><b>Date</b></td>"
                            "<td align='center'>{0}</td>"
                            "<td align='center'>{2}</td></tr>"
                            "<tr><td><b>Time</b></td>"
                            "<td align='center'>{1}</td>"
                            "<td align='center'>{3}</td></tr>"
                            "</table>"
                            ).format(localdate, localtime,
                                     devicedate, devicetime)
                )
            except ValueError:
                E5MessageBox.information(
                    self,
                    self.tr("Date and Time"),
                    self.tr("<table>"
                            "<tr><th>Local Date and Time</th>"
                            "<th>Device Date and Time</th></tr>"
                            "<tr><td align='center'>{0} {1}</td>"
                            "<td align='center'>{2}</td></tr>"
                            "</table>"
                            ).format(localdate, localtime,
                                     deviceDateTimeString.strip())
                )
        except Exception as exc:
            self.__showError("getTime()", str(exc))
    
    def __showError(self, method, error):
        """
        Private method to show some error message.
        
        @param method name of the method the error occured in
        @type str
        @param error error message
        @type str
        """
        with E5OverridenCursor():
            E5MessageBox.warning(
                self,
                self.tr("Error handling device"),
                self.tr("<p>There was an error communicating with the"
                        " connected device.</p><p>Method: {0}</p>"
                        "<p>Message: {1}</p>")
                .format(method, error))
    
    def __mpyCrossAvailable(self):
        """
        Private method to check the availability of mpy-cross.
        
        @return flag indicating the availability of mpy-cross
        @rtype bool
        """
        available = False
        program = Preferences.getMicroPython("MpyCrossCompiler")
        if not program:
            program = "mpy-cross"
            if Utilities.isinpath(program):
                available = True
        else:
            if Utilities.isExecutable(program):
                available = True
        
        return available
    
    def __crossCompile(self, pythonFile="", title=""):
        """
        Private method to cross compile a Python file to a .mpy file.
        
        @param pythonFile name of the Python file to be compiled
        @type str
        @param title title for the various dialogs
        @type str
        """
        program = Preferences.getMicroPython("MpyCrossCompiler")
        if not program:
            program = "mpy-cross"
            if not Utilities.isinpath(program):
                E5MessageBox.critical(
                    self,
                    title,
                    self.tr("""The MicroPython cross compiler"""
                            """ <b>mpy-cross</b> cannot be found. Ensure it"""
                            """ is in the search path or configure it on"""
                            """ the MicroPython configuration page."""))
                return
        
        if not pythonFile:
            defaultDirectory = ""
            aw = e5App().getObject("ViewManager").activeWindow()
            if aw:
                fn = aw.getFileName()
                if fn:
                    defaultDirectory = os.path.dirname(fn)
            if not defaultDirectory:
                defaultDirectory = (
                    Preferences.getMicroPython("MpyWorkspace") or
                    Preferences.getMultiProject("Workspace") or
                    os.path.expanduser("~")
                )
            pythonFile = E5FileDialog.getOpenFileName(
                self,
                title,
                defaultDirectory,
                self.tr("Python Files (*.py);;All Files (*)"))
            if not pythonFile:
                # user cancelled
                return
        
        if not os.path.exists(pythonFile):
            E5MessageBox.critical(
                self,
                title,
                self.tr("""The Python file <b>{0}</b> does not exist."""
                        """ Aborting...""").format(pythonFile))
            return
        
        compileArgs = [
            pythonFile,
        ]
        dlg = E5ProcessDialog(self.tr("'mpy-cross' Output"), title)
        res = dlg.startProcess(program, compileArgs)
        if res:
            dlg.exec()
    
    @pyqtSlot()
    def __compileFile2Mpy(self):
        """
        Private slot to cross compile a Python file (*.py) to a .mpy file.
        """
        self.__crossCompile(title=self.tr("Compile Python File"))
    
    @pyqtSlot()
    def __compileEditor2Mpy(self):
        """
        Private slot to cross compile the current editor to a .mpy file.
        """
        aw = e5App().getObject("ViewManager").activeWindow()
        if not aw.checkDirty():
            # editor still has unsaved changes, abort...
            return
        if not aw.isPyFile():
            # no Python file
            E5MessageBox.critical(
                self,
                self.tr("Compile Current Editor"),
                self.tr("""The current editor does not contain a Python"""
                        """ file. Aborting..."""))
            return
        
        self.__crossCompile(
            pythonFile=aw.getFileName(),
            title=self.tr("Compile Current Editor")
        )
    
    @pyqtSlot()
    def __showDocumentation(self):
        """
        Private slot to open the documentation URL for the selected device.
        """
        if self.__device is None or not self.__device.hasDocumentationUrl():
            # abort silently
            return
        
        url = self.__device.getDocumentationUrl()
        e5App().getObject("UserInterface").launchHelpViewer(url)
    
    @pyqtSlot()
    def __downloadFirmware(self):
        """
        Private slot to open the firmware download page.
        """
        if self.__device is None or not self.__device.hasFirmwareUrl():
            # abort silently
            return
        
        self.__device.downloadFirmware()
    
    def __downloadFromUrl(self, url):
        """
        Private method to open a web browser for the given URL.
        
        @param url URL to be opened
        @type str
        """
        if self.__device is None:
            # abort silently
            return
        
        if url:
            e5App().getObject("UserInterface").launchHelpViewer(url)
    
    @pyqtSlot()
    def __manageIgnored(self):
        """
        Private slot to manage the list of ignored serial devices.
        """
        from .IgnoredDevicesDialog import IgnoredDevicesDialog
        
        dlg = IgnoredDevicesDialog(
            Preferences.getMicroPython("IgnoredUnknownDevices"),
            self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            ignoredDevices = dlg.getDevices()
            Preferences.setMicroPython("IgnoredUnknownDevices",
                                       ignoredDevices)
    
    @pyqtSlot()
    def __configure(self):
        """
        Private slot to open the MicroPython configuration page.
        """
        e5App().getObject("UserInterface").showPreferences("microPythonPage")
    
    @pyqtSlot()
    def __manageUnknownDevices(self):
        """
        Private slot to manage manually added boards (i.e. those not in the
        list of supported boards).
        """
        from .UnknownDevicesDialog import UnknownDevicesDialog
        dlg = UnknownDevicesDialog()
        dlg.exec()
    
    def __addUnknownDevices(self, devices):
        """
        Private method to add devices to the list of manually added boards.
        
        @param devices list of not ignored but unknown devices
        @type list of tuple of (int, int, str)
        """
        from .AddEditDevicesDialog import AddEditDevicesDialog
        
        if len(devices) > 1:
            from E5Gui.E5ListSelectionDialog import E5ListSelectionDialog
            sdlg = E5ListSelectionDialog(
                [d[2] for d in devices],
                title=self.tr("Add Unknown Devices"),
                message=self.tr("Select the devices to be added:"),
                checkBoxSelection=True
            )
            if sdlg.exec() == QDialog.DialogCode.Accepted:
                selectedDevices = sdlg.getSelection()
        else:
            selectedDevices = devices[0][2]
        
        if selectedDevices:
            manualDevices = Preferences.getMicroPython("ManualDevices")
            for vid, pid, description in devices:
                if description in selectedDevices:
                    dlg = AddEditDevicesDialog(vid, pid, description)
                    if dlg.exec() == QDialog.DialogCode.Accepted:
                        manualDevices.append(dlg.getDeviceDict())
            Preferences.setMicroPython("ManualDevices", manualDevices)
            
            # rescan the ports
            self.__populateDeviceTypeComboBox()
    
    @pyqtSlot()
    def __flashUF2(self):
        """
        Private slot to flash MicroPython/CircuitPython to a device
        support the UF2 bootloader.
        """
        dlg = UF2FlashDialog.UF2FlashDialog()
        dlg.exec()
