# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for CircuitPython boards.
"""

import shutil
import os

from PyQt5.QtCore import pyqtSlot

from E5Gui import E5MessageBox, E5FileDialog

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

import Utilities
import Preferences


class CircuitPythonDevice(MicroPythonDevice):
    """
    Class implementing the device for CircuitPython boards.
    """
    DeviceVolumeName = "CIRCUITPY"
    
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
        super(CircuitPythonDevice, self).__init__(
            microPythonWidget, deviceType, parent)
        
        self.__workspace = self.__findWorkspace()
        
        self.__nonUF2devices = {
            "teensy": self.__flashTeensy,
        }
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(CircuitPythonDevice, self).setButtons()
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
        return self.tr("CircuitPython")
    
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
        # Attempts to find the paths on the filesystem that represents the
        # plugged in CIRCUITPY boards.
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
                    self.tr("Python files for CircuitPython can be edited in"
                            " place, if the device volume is locally"
                            " available. Such a volume was not found. In"
                            " place editing will not be available."
                            )
                )
            
            return super(CircuitPythonDevice, self).getWorkspace()
    
    def addDeviceMenuEntries(self, menu):
        """
        Public method to add device specific entries to the given menu.
        
        @param menu reference to the context menu
        @type QMenu
        """
        connected = self.microPython.isConnected()
        
        act = menu.addAction(self.tr("Flash CircuitPython Firmware"),
                             self.__flashCircuitPython)
        act.setEnabled(not connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Install Library Files"),
                             self.__installLibraryFiles)
        act.setEnabled(self.__deviceVolumeMounted())
    
    def hasFlashMenuEntry(self):
        """
        Public method to check, if the device has its own flash menu entry.
        
        @return flag indicating a specific flash menu entry
        @rtype bool
        """
        return True
    
    @pyqtSlot()
    def __flashCircuitPython(self):
        """
        Private slot to flash a CircuitPython firmware to the device.
        """
        lBoardName = self.microPython.getCurrentBoard().lower()
        if lBoardName:
            for name in self.__nonUF2devices:
                if name in lBoardName:
                    self.__nonUF2devices[name]()
                    break
            else:
                from .UF2FlashDialog import UF2FlashDialog
                dlg = UF2FlashDialog(boardType="circuitpython")
                dlg.exec()
    
    def __flashTeensy(self):
        """
        Private method to show a message box because Teens does not support
        the UF2 bootloader yet.
        """
        E5MessageBox.information(
            self.microPython,
            self.tr("Flash CircuitPython Firmware"),
            self.tr("""<p>Teensy 4.0 and Teensy 4.1 do not support the UF2"""
                    """ bootloader. Please use the 'Teensy Loader'"""
                    """ application to flash CircuitPython. Make sure you"""
                    """ downloaded the CircuitPython .hex file.</p>"""
                    """<p>See <a href="{0}">the PJRC Teensy web site</a>"""
                    """ for details.</p>""")
            .format("https://www.pjrc.com/teensy/loader.html"))
    
    @pyqtSlot()
    def __installLibraryFiles(self):
        """
        Private slot to install Python files into the onboard library.
        """
        if not self.__deviceVolumeMounted():
            E5MessageBox.critical(
                self.microPython,
                self.tr("Install Library Files"),
                self.tr("""The device volume "<b>{0}</b>" is not available."""
                        """ Ensure it is mounted properly and try again."""))
            return
        
        target = os.path.join(self.getWorkspace(), "lib")
        # ensure that the library directory exists on the device
        if not os.path.isdir(target):
            os.makedirs(target)
        
        libraryFiles = E5FileDialog.getOpenFileNames(
            self.microPython,
            self.tr("Install Library Files"),
            os.path.expanduser("~"),
            self.tr("Compiled Python Files (*.mpy);;"
                    "Python Files (*.py);;"
                    "All Files (*)"))
        
        for libraryFile in libraryFiles:
            if os.path.exists(libraryFile):
                shutil.copy2(libraryFile, target)
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        return Preferences.getMicroPython("CircuitPythonDocuUrl")
    
    def getDownloadMenuEntries(self):
        """
        Public method to retrieve the entries for the downloads menu.
        
        @return list of tuples with menu text and URL to be opened for each
            entry
        @rtype list of tuple of (str, str)
        """
        return [
            (self.tr("CircuitPython Firmware"),
             Preferences.getMicroPython("CircuitPythonFirmwareUrl")),
            (self.tr("CircuitPython Libraries"),
             Preferences.getMicroPython("CircuitPythonLibrariesUrl"))
        ]
