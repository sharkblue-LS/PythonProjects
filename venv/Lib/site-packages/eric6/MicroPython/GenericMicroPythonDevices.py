# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for generic MicroPython devices
(i.e. those devices not specifically supported yet).
"""

import os

from E5Gui import E5MessageBox

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

import Preferences
import Utilities


class GenericMicroPythonDevice(MicroPythonDevice):
    """
    Class implementing the device interface for generic MicroPython boards.
    """
    def __init__(self, microPythonWidget, deviceType, vid, pid, parent=None):
        """
        Constructor
        
        @param microPythonWidget reference to the main MicroPython widget
        @type MicroPythonWidget
        @param deviceType device type assigned to this device interface
        @type str
        @param vid vendor ID
        @type int
        @param pid product ID
        @type int
        @param parent reference to the parent object
        @type QObject
        """
        super(GenericMicroPythonDevice, self).__init__(
            microPythonWidget, deviceType, parent)
        
        self.__directAccess = False
        self.__deviceVolumeName = ""
        self.__workspace = ""
        self.__deviceName = ""
        
        for deviceData in Preferences.getMicroPython("ManualDevices"):
            if (
                deviceData["vid"] == vid and
                deviceData["pid"] == pid
            ):
                self.__deviceVolumeName = deviceData["data_volume"]
                self.__directAccess = bool(deviceData["data_volume"])
                self.__deviceName = deviceData["description"]
                
                if self.__directAccess:
                    self.__workspace = self.__findWorkspace()
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(GenericMicroPythonDevice, self).setButtons()
        self.microPython.setActionButtons(
            run=True, repl=True, files=True, chart=HAS_QTCHART)
        
        if self.__directAccess and self.__deviceVolumeMounted():
            self.microPython.setActionButtons(open=True, save=True)
    
    def deviceName(self):
        """
        Public method to get the name of the device.
        
        @return name of the device
        @rtype str
        """
        return self.__deviceName
    
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
        
        return (
            self.__directAccess and
            self.__deviceVolumeName in self.getWorkspace(silent=True)
        )
    
    def getWorkspace(self, silent=False):
        """
        Public method to get the workspace directory.
        
        @param silent flag indicating silent operations
        @type bool
        @return workspace directory used for saving files
        @rtype str
        """
        if self.__directAccess:
            if self.__workspace:
                # return cached entry
                return self.__workspace
            else:
                self.__workspace = self.__findWorkspace(silent=silent)
                return self.__workspace
        else:
            return super(GenericMicroPythonDevice, self).getWorkspace()
    
    def __findWorkspace(self, silent=False):
        """
        Private method to find the workspace directory.
        
        @param silent flag indicating silent operations
        @type bool
        @return workspace directory used for saving files
        @rtype str
        """
        # Attempts to find the path on the filesystem that represents the
        # plugged in board.
        deviceDirectories = Utilities.findVolume(self.__deviceVolumeName,
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
                    self.tr("Python files for this generic board can be"
                            " edited in place, if the device volume is locally"
                            " available. A volume named '{0}' was not found."
                            " In place editing will not be available."
                            ).format(self.__deviceVolumeName)
                )
            
            return super(GenericMicroPythonDevice, self).getWorkspace()
