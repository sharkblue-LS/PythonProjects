# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for ESP32 and ESP8266 based
boards.
"""

import sys

from PyQt5.QtCore import pyqtSlot, QProcess
from PyQt5.QtWidgets import QDialog

from E5Gui import E5MessageBox
from E5Gui.E5ProcessDialog import E5ProcessDialog
from E5Gui.E5Application import e5App

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

import Preferences


class EspDevice(MicroPythonDevice):
    """
    Class implementing the device for ESP32 and ESP8266 based boards.
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
        super(EspDevice, self).__init__(microPythonWidget, deviceType, parent)
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(EspDevice, self).setButtons()
        self.microPython.setActionButtons(
            run=True, repl=True, files=True, chart=HAS_QTCHART)
    
    def forceInterrupt(self):
        """
        Public method to determine the need for an interrupt when opening the
        serial connection.
        
        @return flag indicating an interrupt is needed
        @rtype bool
        """
        return True
    
    def deviceName(self):
        """
        Public method to get the name of the device.
        
        @return name of the device
        @rtype str
        """
        return self.tr("ESP8266, ESP32")
    
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
        
        act = menu.addAction(self.tr("Erase Flash"),
                             self.__eraseFlash)
        act.setEnabled(not connected)
        act = menu.addAction(self.tr("Flash MicroPython Firmware"),
                             self.__flashMicroPython)
        act.setEnabled(not connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Flash Additional Firmware"),
                             self.__flashAddons)
        act.setEnabled(not connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Backup Firmware"),
                             self.__backupFlash)
        act.setEnabled(not connected)
        act = menu.addAction(self.tr("Restore Firmware"),
                             self.__restoreFlash)
        act.setEnabled(not connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Show Chip ID"),
                             self.__showChipID)
        act.setEnabled(not connected)
        act = menu.addAction(self.tr("Show Flash ID"),
                             self.__showFlashID)
        act.setEnabled(not connected)
        act = menu.addAction(self.tr("Show MAC Address"),
                             self.__showMACAddress)
        act.setEnabled(not connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Reset Device"), self.__resetDevice)
        menu.addSeparator()
        menu.addAction(self.tr("Install 'esptool.py'"), self.__installEspTool)
    
    def hasFlashMenuEntry(self):
        """
        Public method to check, if the device has its own flash menu entry.
        
        @return flag indicating a specific flash menu entry
        @rtype bool
        """
        return True
    
    @pyqtSlot()
    def __eraseFlash(self):
        """
        Private slot to erase the device flash memory.
        """
        ok = E5MessageBox.yesNo(
            self.microPython,
            self.tr("Erase Flash"),
            self.tr("""Shall the flash of the selected device really be"""
                    """ erased?"""))
        if ok:
            flashArgs = [
                "-u",
                "-m", "esptool",
                "--port", self.microPython.getCurrentPort(),
                "erase_flash",
            ]
            dlg = E5ProcessDialog(self.tr("'esptool erase_flash' Output"),
                                  self.tr("Erase Flash"),
                                  showProgress=True)
            res = dlg.startProcess(sys.executable, flashArgs)
            if res:
                dlg.exec()
    
    @pyqtSlot()
    def __flashMicroPython(self):
        """
        Private slot to flash a MicroPython firmware to the device.
        
        @exception ValueError raised to indicate an unsupported chip type
        """
        from .EspFirmwareSelectionDialog import EspFirmwareSelectionDialog
        dlg = EspFirmwareSelectionDialog()
        if dlg.exec() == QDialog.DialogCode.Accepted:
            chip, firmware, flashMode, _ = dlg.getData()
            if chip == "esp8266":
                flashAddress = "0x0000"
            elif chip == "esp32":
                flashAddress = "0x1000"
            else:
                raise ValueError(self.tr("Unsupported chip type '{0}'.")
                                 .format(chip))
            flashArgs = [
                "-u",
                "-m", "esptool",
                "--chip", chip,
                "--port", self.microPython.getCurrentPort(),
                "write_flash",
            ]
            if flashMode:
                flashArgs.extend([
                    "--flash_mode", flashMode
                ])
            flashArgs.extend([
                flashAddress,
                firmware,
            ])
            dlg = E5ProcessDialog(self.tr("'esptool write_flash' Output"),
                                  self.tr("Flash MicroPython Firmware"),
                                  showProgress=True)
            res = dlg.startProcess(sys.executable, flashArgs)
            if res:
                dlg.exec()
    
    @pyqtSlot()
    def __flashAddons(self):
        """
        Private slot to flash some additional firmware images.
        """
        from .EspFirmwareSelectionDialog import EspFirmwareSelectionDialog
        dlg = EspFirmwareSelectionDialog(addon=True)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            chip, firmware, flashMode, flashAddress = dlg.getData()
            flashArgs = [
                "-u",
                "-m", "esptool",
                "--chip", chip,
                "--port", self.microPython.getCurrentPort(),
                "write_flash",
            ]
            if flashMode:
                flashArgs.extend([
                    "--flash_mode", flashMode
                ])
            flashArgs.extend([
                flashAddress.lower(),
                firmware,
            ])
            dlg = E5ProcessDialog(self.tr("'esptool write_flash' Output"),
                                  self.tr("Flash Additional Firmware"),
                                  showProgress=True)
            res = dlg.startProcess(sys.executable, flashArgs)
            if res:
                dlg.exec()
    
    @pyqtSlot()
    def __backupFlash(self):
        """
        Private slot to backup the currently flashed firmware.
        """
        from .EspBackupRestoreFirmwareDialog import (
            EspBackupRestoreFirmwareDialog
        )
        dlg = EspBackupRestoreFirmwareDialog(backupMode=True)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            chip, flashSize, flashMode, firmware = dlg.getData()
            flashArgs = [
                "-u",
                "-m", "esptool",
                "--chip", chip,
                "--port", self.microPython.getCurrentPort(),
                "read_flash",
                "0x0", flashSize,
                firmware,
            ]
            dlg = E5ProcessDialog(self.tr("'esptool read_flash' Output"),
                                  self.tr("Backup Firmware"),
                                  showProgress=True)
            res = dlg.startProcess(sys.executable, flashArgs)
            if res:
                dlg.exec()
    
    @pyqtSlot()
    def __restoreFlash(self):
        """
        Private slot to restore a previously saved firmware.
        """
        from .EspBackupRestoreFirmwareDialog import (
            EspBackupRestoreFirmwareDialog
        )
        dlg = EspBackupRestoreFirmwareDialog(backupMode=False)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            chip, flashSize, flashMode, firmware = dlg.getData()
            flashArgs = [
                "-u",
                "-m", "esptool",
                "--chip", chip,
                "--port", self.microPython.getCurrentPort(),
                "write_flash",
                "--flash_mode", flashMode,
            ]
            if bool(flashSize):
                flashArgs.extend([
                    "--flash_size", flashSize,
                ])
            flashArgs.extend([
                "0x0",
                firmware,
            ])
            dlg = E5ProcessDialog(self.tr("'esptool write_flash' Output"),
                                  self.tr("Restore Firmware"),
                                  showProgress=True)
            res = dlg.startProcess(sys.executable, flashArgs)
            if res:
                dlg.exec()
    
    @pyqtSlot()
    def __showChipID(self):
        """
        Private slot to show the ID of the ESP chip.
        """
        args = [
            "-u",
            "-m", "esptool",
            "--port", self.microPython.getCurrentPort(),
            "chip_id"
        ]
        dlg = E5ProcessDialog(self.tr("'esptool chip_id' Output"),
                              self.tr("Show Chip ID"))
        res = dlg.startProcess(sys.executable, args)
        if res:
            dlg.exec()
    
    @pyqtSlot()
    def __showFlashID(self):
        """
        Private slot to show the ID of the ESP flash chip.
        """
        args = [
            "-u",
            "-m", "esptool",
            "--port", self.microPython.getCurrentPort(),
            "flash_id"
        ]
        dlg = E5ProcessDialog(self.tr("'esptool flash_id' Output"),
                              self.tr("Show Flash ID"))
        res = dlg.startProcess(sys.executable, args)
        if res:
            dlg.exec()
    
    @pyqtSlot()
    def __showMACAddress(self):
        """
        Private slot to show the MAC address of the ESP chip.
        """
        args = [
            "-u",
            "-m", "esptool",
            "--port", self.microPython.getCurrentPort(),
            "read_mac"
        ]
        dlg = E5ProcessDialog(self.tr("'esptool read_mac' Output"),
                              self.tr("Show MAC Address"))
        res = dlg.startProcess(sys.executable, args)
        if res:
            dlg.exec()
    
    @pyqtSlot()
    def __resetDevice(self):
        """
        Private slot to reset the connected device.
        """
        if self.microPython.isConnected():
            self.microPython.commandsInterface().execute([
                "import machine",
                "machine.reset()",
            ])
        else:
            # perform a reset via esptool using flash_id command ignoring
            # the output
            args = [
                "-u",
                "-m", "esptool",
                "--port", self.microPython.getCurrentPort(),
                "flash_id"
            ]
            proc = QProcess()
            proc.start(sys.executable, args)
            procStarted = proc.waitForStarted(10000)
            if procStarted:
                proc.waitForFinished(10000)
    
    @pyqtSlot()
    def __installEspTool(self):
        """
        Private slot to install the esptool package via pip.
        """
        pip = e5App().getObject("Pip")
        pip.installPackages(["esptool"], interpreter=sys.executable)
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        return Preferences.getMicroPython("MicroPythonDocuUrl")
    
    def getFirmwareUrl(self):
        """
        Public method to get the device firmware download URL.
        
        @return firmware download URL of the device
        @rtype str
        """
        return Preferences.getMicroPython("MicroPythonFirmwareUrl")
