# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for PyBoard boards.
"""

import os

from PyQt5.QtCore import pyqtSlot, QStandardPaths

from E5Gui import E5MessageBox, E5FileDialog
from E5Gui.E5Application import e5App
from E5Gui.E5ProcessDialog import E5ProcessDialog

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

import Utilities
import Preferences


class PyBoardDevice(MicroPythonDevice):
    """
    Class implementing the device for PyBoard boards.
    """
    DeviceVolumeName = "PYBFLASH"
    
    FlashInstructionsURL = (
        "https://github.com/micropython/micropython/wiki/"
        "Pyboard-Firmware-Update"
    )
    
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
        super(PyBoardDevice, self).__init__(microPythonWidget, deviceType,
                                            parent)
        
        self.__workspace = self.__findWorkspace()
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(PyBoardDevice, self).setButtons()
        self.microPython.setActionButtons(
            run=True, repl=True, files=True, chart=HAS_QTCHART)
        
        if self.__deviceVolumeMounted():
            self.microPython.setActionButtons(open=True, save=True)
    
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
        return self.tr("PyBoard")
    
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
    
    def supportsLocalFileAccess(self):
        """
        Public method to indicate file access via a local directory.
        
        @return flag indicating file access via local directory
        @rtype bool
        """
        return self.__deviceVolumeMounted()
    
    def __deviceVolumeMounted(self):
        """
        Private method to check, if the device volume is mounted.
        
        @return flag indicated a mounted device
        @rtype bool
        """
        if self.__workspace and not os.path.exists(self.__workspace):
            self.__workspace = ""       # reset
        
        return self.DeviceVolumeName in self.getWorkspace(silent=True)
    
    def getWorkspace(self, silent=False):
        """
        Public method to get the workspace directory.
        
        @param silent flag indicating silent operations
        @type bool
        @return workspace directory used for saving files
        @rtype str
        """
        if self.__workspace:
            # return cached entry
            return self.__workspace
        else:
            self.__workspace = self.__findWorkspace(silent=silent)
            return self.__workspace
    
    def __findWorkspace(self, silent=False):
        """
        Private method to find the workspace directory.
        
        @param silent flag indicating silent operations
        @type bool
        @return workspace directory used for saving files
        @rtype str
        """
        # Attempts to find the path on the filesystem that represents the
        # plugged in PyBoard board.
        deviceDirectories = Utilities.findVolume(self.DeviceVolumeName,
                                                 findAll=True)
        
        if deviceDirectories:
            if len(deviceDirectories) == 1:
                return deviceDirectories[0]
            else:
                return self.selectDeviceDirectory(deviceDirectories)
        else:
            # return the default workspace and give the user a warning (unless
            # silent mode is selected)
            if not silent:
                E5MessageBox.warning(
                    self.microPython,
                    self.tr("Workspace Directory"),
                    self.tr("Python files for PyBoard can be edited in"
                            " place, if the device volume is locally"
                            " available. Such a volume was not found. In"
                            " place editing will not be available."
                            )
                )
            
            return super(PyBoardDevice, self).getWorkspace()
    
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
        act = menu.addAction(self.tr("List DFU-capable Devices"),
                             self.__listDfuCapableDevices)
        act.setEnabled(not connected)
        act = menu.addAction(self.tr("Flash MicroPython Firmware"),
                             self.__flashMicroPython)
        act.setEnabled(not connected)
        menu.addSeparator()
        menu.addAction(self.tr("MicroPython Flash Instructions"),
                       self.__showFlashInstructions)
    
    def hasFlashMenuEntry(self):
        """
        Public method to check, if the device has its own flash menu entry.
        
        @return flag indicating a specific flash menu entry
        @rtype bool
        """
        return True
    
    @pyqtSlot()
    def __showFlashInstructions(self):
        """
        Private slot to open the URL containing instructions for installing
        MicroPython on the pyboard.
        """
        e5App().getObject("UserInterface").launchHelpViewer(
            PyBoardDevice.FlashInstructionsURL)
    
    def __dfuUtilAvailable(self):
        """
        Private method to check the availability of dfu-util.
        
        @return flag indicating the availability of dfu-util
        @rtype bool
        """
        available = False
        program = Preferences.getMicroPython("DfuUtilPath")
        if not program:
            program = "dfu-util"
            if Utilities.isinpath(program):
                available = True
        else:
            if Utilities.isExecutable(program):
                available = True
        
        if not available:
            E5MessageBox.critical(
                self.microPython,
                self.tr("dfu-util not available"),
                self.tr("""The dfu-util firmware flashing tool"""
                        """ <b>dfu-util</b> cannot be found or is not"""
                        """ executable. Ensure it is in the search path"""
                        """ or configure it on the MicroPython"""
                        """ configuration page.""")
            )
        
        return available
    
    def __showDfuEnableInstructions(self, flash=True):
        """
        Private method to show some instructions to enable the DFU mode.
        
        @param flash flag indicating to show a warning message for flashing
        @type bool
        @return flag indicating OK to continue or abort
        @rtype bool
        """
        msg = self.tr(
            "<h3>Enable DFU Mode</h3>"
            "<p>1. Disconnect everything from your board</p>"
            "<p>2. Disconnect your board</p>"
            "<p>3. Connect the DFU/BOOT0 pin with a 3.3V pin</p>"
            "<p>4. Re-connect your board</p>"
            "<hr />"
        )
        
        if flash:
            msg += self.tr(
                "<p><b>Warning:</b> Make sure that all other DFU capable"
                " devices except your PyBoard are disconnected."
                "<hr />"
            )
        
        msg += self.tr(
            "<p>Press <b>OK</b> to continue...</p>"
        )
        res = E5MessageBox.information(
            self.microPython,
            self.tr("Enable DFU mode"),
            msg,
            E5MessageBox.StandardButtons(
                E5MessageBox.Abort |
                E5MessageBox.Ok))
        
        return res == E5MessageBox.Ok
    
    def __showDfuDisableInstructions(self):
        """
        Private method to show some instructions to disable the DFU mode.
        """
        msg = self.tr(
            "<h3>Disable DFU Mode</h3>"
            "<p>1. Disconnect your board</p>"
            "<p>2. Remove the DFU jumper</p>"
            "<p>3. Re-connect your board</p>"
            "<hr />"
            "<p>Press <b>OK</b> to continue...</p>"
        )
        E5MessageBox.information(
            self.microPython,
            self.tr("Disable DFU mode"),
            msg
        )
    
    @pyqtSlot()
    def __listDfuCapableDevices(self):
        """
        Private slot to list all DFU-capable devices.
        """
        if self.__dfuUtilAvailable():
            ok2continue = self.__showDfuEnableInstructions(flash=False)
            if ok2continue:
                program = Preferences.getMicroPython("DfuUtilPath")
                if not program:
                    program = "dfu-util"
                
                args = [
                    "--list",
                ]
                dlg = E5ProcessDialog(
                    self.tr("'dfu-util' Output"),
                    self.tr("List DFU capable Devices")
                )
                res = dlg.startProcess(program, args)
                if res:
                    dlg.exec()
    
    @pyqtSlot()
    def __flashMicroPython(self):
        """
        Private slot to flash a MicroPython firmware.
        """
        if self.__dfuUtilAvailable():
            ok2continue = self.__showDfuEnableInstructions()
            if ok2continue:
                program = Preferences.getMicroPython("DfuUtilPath")
                if not program:
                    program = "dfu-util"
                
                downloadsPath = QStandardPaths.standardLocations(
                    QStandardPaths.StandardLocation.DownloadLocation)[0]
                firmware = E5FileDialog.getOpenFileName(
                    self.microPython,
                    self.tr("Flash MicroPython Firmware"),
                    downloadsPath,
                    self.tr(
                        "MicroPython Firmware Files (*.dfu);;All Files (*)")
                )
                if firmware and os.path.exists(firmware):
                    args = [
                        "--alt", "0",
                        "--download", firmware,
                    ]
                    dlg = E5ProcessDialog(
                        self.tr("'dfu-util' Output"),
                        self.tr("Flash MicroPython Firmware")
                    )
                    res = dlg.startProcess(program, args)
                    if res:
                        dlg.exec()
                        self.__showDfuDisableInstructions()
    
    @pyqtSlot()
    def __activateBootloader(self):
        """
        Private slot to activate the bootloader and disconnect.
        """
        if self.microPython.isConnected():
            self.microPython.commandsInterface().execute([
                "import pyb",
                "pyb.bootloader()",
            ])
            # simulate pressing the disconnect button
            self.microPython.on_connectButton_clicked()
