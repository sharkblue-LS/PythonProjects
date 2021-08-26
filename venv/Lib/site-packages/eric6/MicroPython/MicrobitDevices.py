# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the device interface class for BBC micro:bit and
Calliope mini boards.
"""

import os
import shutil

from PyQt5.QtCore import pyqtSlot, QStandardPaths
from PyQt5.QtWidgets import QInputDialog, QLineEdit

from .MicroPythonDevices import MicroPythonDevice
from .MicroPythonWidget import HAS_QTCHART

from E5Gui import E5MessageBox, E5FileDialog
from E5Gui.E5Application import e5App

import Utilities
import Preferences


class MicrobitDevice(MicroPythonDevice):
    """
    Class implementing the device for BBC micro:bit and Calliope mini boards.
    """
    def __init__(self, microPythonWidget, deviceType, parent=None):
        """
        Constructor
        
        @param microPythonWidget reference to the main MicroPython widget
        @type MicroPythonWidget
        @param deviceType type of the device
        @type str
        @param parent reference to the parent object
        @type QObject
        """
        super(MicrobitDevice, self).__init__(
            microPythonWidget, deviceType, parent)
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        super(MicrobitDevice, self).setButtons()
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
        if self.getDeviceType() == "bbc_microbit":
            # BBC micro:bit
            return self.tr("BBC micro:bit")
        else:
            # Calliope mini
            return self.tr("Calliope mini")
    
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
    
    def hasTimeCommands(self):
        """
        Public method to check, if the device supports time commands.
        
        The default returns True.
        
        @return flag indicating support for time commands
        @rtype bool
        """
        return False
    
    def addDeviceMenuEntries(self, menu):
        """
        Public method to add device specific entries to the given menu.
        
        @param menu reference to the context menu
        @type QMenu
        """
        connected = self.microPython.isConnected()
        
        act = menu.addAction(self.tr("Flash MicroPython"),
                             self.__flashMicroPython)
        act.setEnabled(not connected)
        act = menu.addAction(self.tr("Flash Firmware"),
                             lambda: self.__flashMicroPython(firmware=True))
        act.setEnabled(not connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Save Script"), self.__saveScriptToDevice)
        act.setToolTip(self.tr(
            "Save the current script to the selected device"))
        act.setEnabled(connected)
        act = menu.addAction(self.tr("Save Script as 'main.py'"),
                             self.__saveMain)
        act.setToolTip(self.tr(
            "Save the current script as 'main.py' on the connected device"))
        act.setEnabled(connected)
        menu.addSeparator()
        act = menu.addAction(self.tr("Reset {0}").format(self.deviceName()),
                             self.__resetDevice)
        act.setEnabled(connected)
    
    def hasFlashMenuEntry(self):
        """
        Public method to check, if the device has its own flash menu entry.
        
        @return flag indicating a specific flash menu entry
        @rtype bool
        """
        return True
    
    @pyqtSlot()
    def __flashMicroPython(self, firmware=False):
        """
        Private slot to flash MicroPython or the DAPLink firmware to the
        device.
        
        @param firmware flag indicating to flash the DAPLink firmware
        @type bool
        """
        # Attempts to find the path on the file system that represents the
        # plugged in micro:bit board. To flash the DAPLink firmware, it must be
        # in maintenance mode, for MicroPython in standard mode.
        if self.getDeviceType() == "bbc_microbit":
            # BBC micro:bit
            if firmware:
                deviceDirectories = Utilities.findVolume("MAINTENANCE",
                                                         findAll=True)
            else:
                deviceDirectories = Utilities.findVolume("MICROBIT",
                                                         findAll=True)
        else:
            # Calliope mini
            if firmware:
                deviceDirectories = Utilities.findVolume("MAINTENANCE",
                                                         findAll=True)
            else:
                deviceDirectories = Utilities.findVolume("MINI",
                                                         findAll=True)
        if len(deviceDirectories) == 0:
            if self.getDeviceType() == "bbc_microbit":
                # BBC micro:bit is not ready or not mounted
                if firmware:
                    E5MessageBox.critical(
                        self.microPython,
                        self.tr("Flash MicroPython/Firmware"),
                        self.tr(
                            '<p>The BBC micro:bit is not ready for flashing'
                            ' the DAPLink firmware. Follow these'
                            ' instructions. </p>'
                            '<ul>'
                            '<li>unplug USB cable and any batteries</li>'
                            '<li>keep RESET button pressed an plug USB cable'
                            ' back in</li>'
                            '<li>a drive called MAINTENANCE should be'
                            ' available</li>'
                            '</ul>'
                            '<p>See the '
                            '<a href="https://microbit.org/guide/firmware/">'
                            'micro:bit web site</a> for details.</p>'
                        )
                    )
                else:
                    E5MessageBox.critical(
                        self.microPython,
                        self.tr("Flash MicroPython/Firmware"),
                        self.tr(
                            '<p>The BBC micro:bit is not ready for flashing'
                            ' the MicroPython firmware. Please make sure,'
                            ' that a drive called MICROBIT is available.'
                            '</p>'
                        )
                    )
            else:
                # Calliope mini is not ready or not mounted
                if firmware:
                    E5MessageBox.critical(
                        self.microPython,
                        self.tr("Flash MicroPython/Firmware"),
                        self.tr(
                            '<p>The "Calliope mini" is not ready for flashing'
                            ' the DAPLink firmware. Follow these'
                            ' instructions. </p>'
                            '<ul>'
                            '<li>unplug USB cable and any batteries</li>'
                            '<li>keep RESET button pressed an plug USB cable'
                            ' back in</li>'
                            '<li>a drive called MAINTENANCE should be'
                            ' available</li>'
                            '</ul>'
                        )
                    )
                else:
                    E5MessageBox.critical(
                        self.microPython,
                        self.tr("Flash MicroPython/Firmware"),
                        self.tr(
                            '<p>The "Calliope mini" is not ready for flashing'
                            ' the MicroPython firmware. Please make sure,'
                            ' that a drive called MINI is available.'
                            '</p>'
                        )
                    )
        elif len(deviceDirectories) == 1:
            downloadsPath = QStandardPaths.standardLocations(
                QStandardPaths.StandardLocation.DownloadLocation)[0]
            firmware = E5FileDialog.getOpenFileName(
                self.microPython,
                self.tr("Flash MicroPython/Firmware"),
                downloadsPath,
                self.tr("MicroPython/Firmware Files (*.hex *.bin);;"
                        "All Files (*)"))
            if firmware and os.path.exists(firmware):
                shutil.copy2(firmware, deviceDirectories[0])
        else:
            E5MessageBox.warning(
                self,
                self.tr("Flash MicroPython/Firmware"),
                self.tr("There are multiple devices ready for flashing."
                        " Please make sure, that only one device is prepared.")
            )
    
    @pyqtSlot()
    def __saveMain(self):
        """
        Private slot to copy the current script as 'main.py' onto the
        connected device.
        """
        self.__saveScriptToDevice("main.py")
    
    @pyqtSlot()
    def __saveScriptToDevice(self, scriptName=""):
        """
        Private method to save the current script onto the connected
        device.
        
        @param scriptName name of the file on the device
        @type str
        """
        aw = e5App().getObject("ViewManager").activeWindow()
        if not aw:
            return
        
        if scriptName:
            title = self.tr("Save Script as '{0}'").format(scriptName)
        else:
            title = self.tr("Save Script")
        
        if not (aw.isPyFile() or aw.isMicroPythonFile()):
            yes = E5MessageBox.yesNo(
                self.microPython,
                title,
                self.tr("""The current editor does not contain a Python"""
                        """ script. Write it anyway?"""))
            if not yes:
                return
        
        script = aw.text().strip()
        if not script:
            E5MessageBox.warning(
                self.microPython,
                title,
                self.tr("""The script is empty. Aborting."""))
            return
        
        if not scriptName:
            scriptName = os.path.basename(aw.getFileName())
            scriptName, ok = QInputDialog.getText(
                self.microPython,
                title,
                self.tr("Enter a file name on the device:"),
                QLineEdit.EchoMode.Normal,
                scriptName)
            if not ok or not bool(scriptName):
                return
            
            title = self.tr("Save Script as '{0}'").format(scriptName)
        
        commands = [
            "fd = open('{0}', 'wb')".format(scriptName),
            "f = fd.write",
        ]
        for line in script.splitlines():
            commands.append("f(" + repr(line + "\n") + ")")
        commands.append("fd.close()")
        out, err = self.microPython.commandsInterface().execute(commands)
        if err:
            E5MessageBox.critical(
                self.microPython,
                title,
                self.tr("""<p>The script could not be saved to the"""
                        """ device.</p><p>Reason: {0}</p>""")
                .format(err.decode("utf-8")))
        
        # reset the device
        self.__resetDevice()
    
    @pyqtSlot()
    def __resetDevice(self):
        """
        Private slot to reset the connected device.
        """
        if self.getDeviceType() == "bbc_microbit":
            # BBC micro:bit
            self.microPython.commandsInterface().execute([
                "import microbit",
                "microbit.reset()",
            ])
        else:
            # Calliope mini
            self.microPython.commandsInterface().execute([
                "import calliope_mini",
                "calliope_mini.reset()",
            ])
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        if self.getDeviceType() == "bbc_microbit":
            # BBC micro:bit
            return Preferences.getMicroPython("MicrobitDocuUrl")
        else:
            # Calliope mini
            return Preferences.getMicroPython("CalliopeDocuUrl")
    
    def getDownloadMenuEntries(self):
        """
        Public method to retrieve the entries for the downloads menu.
        
        @return list of tuples with menu text and URL to be opened for each
            entry
        @rtype list of tuple of (str, str)
        """
        if self.getDeviceType() == "bbc_microbit":
            return [
                (self.tr("MicroPython Firmware for BBC micro:bit V1"),
                 Preferences.getMicroPython("MicrobitMicroPythonUrl")),
                (self.tr("MicroPython Firmware for BBC micro:bit V2"),
                 Preferences.getMicroPython("MicrobitV2MicroPythonUrl")),
                (self.tr("DAPLink Firmware"),
                 Preferences.getMicroPython("MicrobitFirmwareUrl"))
            ]
        else:
            return [
                (self.tr("MicroPython Firmware"),
                 Preferences.getMicroPython("CalliopeMicroPythonUrl")),
                (self.tr("DAPLink Firmware"),
                 Preferences.getMicroPython("CalliopeDAPLinkUrl"))
            ]
