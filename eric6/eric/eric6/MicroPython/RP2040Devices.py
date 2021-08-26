# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for RP2040 based boards
(e.g. Raspberry Pi Pico).
"""

from PyQt5.QtCore import pyqtSlot

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

import Preferences


class RP2040Device(MicroPythonDevice):
    """
    Class implementing the device for RP2040 based boards.
    """
    def __init__(self, microPythonWidget, deviceType, parent=None):
        """
        Constructor
        
        @param microPythonWidget reference to the main MicroPython widget
        @type MicroPythonWidget
        @param deviceType device type assigned to this device interface
        @type str
        @param parent reference to the parent object
        @type QObject
        """
        super(RP2040Device, self).__init__(
            microPythonWidget, deviceType, parent)
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(RP2040Device, self).setButtons()
        self.microPython.setActionButtons(
            run=True, repl=True, files=True, chart=HAS_QTCHART)
    
    def forceInterrupt(self):
        """
        Public method to determine the need for an interrupt when opening the
        serial connection.
        
        @return flag indicating an interrupt is needed
        @rtype bool
        """
        return False
    
    def deviceName(self):
        """
        Public method to get the name of the device.
        
        @return name of the device
        @rtype str
        """
        return self.tr("RP2040")
    
    def canStartRepl(self):
        """
        Public method to determine, if a REPL can be started.
        
        @return tuple containing a flag indicating it is safe to start a REPL
            and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def canStartPlotter(self):
        """
        Public method to determine, if a Plotter can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def canRunScript(self):
        """
        Public method to determine, if a script can be executed.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def runScript(self, script):
        """
        Public method to run the given Python script.
        
        @param script script to be executed
        @type str
        """
        pythonScript = script.split("\n")
        self.sendCommands(pythonScript)
    
    def canStartFileManager(self):
        """
        Public method to determine, if a File Manager can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            File Manager and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return True, ""
    
    def addDeviceMenuEntries(self, menu):
        """
        Public method to add device specific entries to the given menu.
        
        @param menu reference to the context menu
        @type QMenu
        """
        connected = self.microPython.isConnected()
        
        act = menu.addAction(self.tr("Activate Bootloader"),
                             self.__activateBootloader)
        act.setEnabled(connected)
        act = menu.addAction(self.tr("Flash Firmware"), self.__flashPython)
        act.setEnabled(not connected)
    
    def hasFlashMenuEntry(self):
        """
        Public method to check, if the device has its own flash menu entry.
        
        @return flag indicating a specific flash menu entry
        @rtype bool
        """
        return True
    
    @pyqtSlot()
    def __flashPython(self):
        """
        Private slot to flash a MicroPython firmware to the device.
        """
        from .UF2FlashDialog import UF2FlashDialog
        dlg = UF2FlashDialog(boardType="rp2040")
        dlg.exec()
    
    def __activateBootloader(self):
        """
        Private method to switch the board into 'bootloader' mode.
        """
        if self.microPython.isConnected():
            self.microPython.commandsInterface().execute([
                "import machine",
                "machine.bootloader()",
            ])
            # simulate pressing the disconnect button
            self.microPython.on_connectButton_clicked()
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        return Preferences.getMicroPython("MicroPythonDocuUrl")
    
    def getDownloadMenuEntries(self):
        """
        Public method to retrieve the entries for the downloads menu.
        
        @return list of tuples with menu text and URL to be opened for each
            entry
        @rtype list of tuple of (str, str)
        """
        return [
            (self.tr("MicroPython Firmware"),
             Preferences.getMicroPython("MicroPythonFirmwareUrl")),
            ("<separator>", ""),
            (self.tr("CircuitPython Firmware"),
             Preferences.getMicroPython("CircuitPythonFirmwareUrl")),
            (self.tr("CircuitPython Libraries"),
             Preferences.getMicroPython("CircuitPythonLibrariesUrl"))
        ]
