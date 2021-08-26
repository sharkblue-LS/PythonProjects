# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the MicroPython configuration page.
"""

from E5Gui.E5PathPicker import E5PathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_MicroPythonPage import Ui_MicroPythonPage

import Preferences
import Utilities

from MicroPython.MicroPythonWidget import AnsiColorSchemes


class MicroPythonPage(ConfigurationPageBase, Ui_MicroPythonPage):
    """
    Class implementing the MicroPython configuration page.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MicroPythonPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("MicroPythonPage")
        
        self.workspacePicker.setMode(E5PathPickerModes.DirectoryMode)
        
        self.colorSchemeComboBox.addItems(sorted(AnsiColorSchemes.keys()))
        
        # populate the chart theme combobox
        try:
            from PyQt5.QtChart import QChart
            
            self.chartThemeComboBox.addItem(
                self.tr("Automatic"), -1)
            self.chartThemeComboBox.addItem(
                self.tr("Light"),
                QChart.ChartTheme.ChartThemeLight)
            self.chartThemeComboBox.addItem(
                self.tr("Dark"),
                QChart.ChartTheme.ChartThemeDark)
            self.chartThemeComboBox.addItem(
                self.tr("Blue Cerulean"),
                QChart.ChartTheme.ChartThemeBlueCerulean)
            self.chartThemeComboBox.addItem(
                self.tr("Brown Sand"),
                QChart.ChartTheme.ChartThemeBrownSand)
            self.chartThemeComboBox.addItem(
                self.tr("Blue NCS"),
                QChart.ChartTheme.ChartThemeBlueNcs)
            self.chartThemeComboBox.addItem(
                self.tr("High Contrast"),
                QChart.ChartTheme.ChartThemeHighContrast)
            self.chartThemeComboBox.addItem(
                self.tr("Blue Icy"),
                QChart.ChartTheme.ChartThemeBlueIcy)
            self.chartThemeComboBox.addItem(
                self.tr("Qt"),
                QChart.ChartTheme.ChartThemeQt)
        except ImportError:
            self.chartThemeComboBox.setEnabled(False)
        
        self.mpyCrossPicker.setMode(E5PathPickerModes.OpenFileMode)
        self.mpyCrossPicker.setFilters(self.tr("All Files (*)"))
        
        self.dfuUtilPathPicker.setMode(E5PathPickerModes.OpenFileMode)
        self.dfuUtilPathPicker.setFilters(self.tr("All Files (*)"))
        
        # set initial values
        # workspace
        self.workspacePicker.setText(
            Utilities.toNativeSeparators(
                Preferences.getMicroPython("MpyWorkspace") or
                Utilities.getHomeDir()))
        
        # serial link parameters
        self.timeoutSpinBox.setValue(
            Preferences.getMicroPython("SerialTimeout") / 1000)
        # converted to seconds
        self.syncTimeCheckBox.setChecked(
            Preferences.getMicroPython("SyncTimeAfterConnect"))
        
        # REPL Pane
        self.colorSchemeComboBox.setCurrentIndex(
            self.colorSchemeComboBox.findText(
                Preferences.getMicroPython("ColorScheme")))
        self.replWrapCheckBox.setChecked(
            Preferences.getMicroPython("ReplLineWrap"))
        
        # Chart Pane
        index = self.chartThemeComboBox.findData(
            Preferences.getMicroPython("ChartColorTheme"))
        if index < 0:
            index = 0
        self.chartThemeComboBox.setCurrentIndex(index)
        
        # MPY Cross Compiler
        self.mpyCrossPicker.setText(
            Preferences.getMicroPython("MpyCrossCompiler"))
        
        # PyBoard specifics
        self.dfuUtilPathPicker.setText(
            Preferences.getMicroPython("DfuUtilPath"))
        
        # MicroPython URLs
        self.micropythonFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("MicroPythonFirmwareUrl"))
        self.micropythonDocuUrlLineEdit.setText(
            Preferences.getMicroPython("MicroPythonDocuUrl"))
        
        # CircuitPython URLs
        self.circuitpythonFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("CircuitPythonFirmwareUrl"))
        self.circuitpythonLibrariesUrlLineEdit.setText(
            Preferences.getMicroPython("CircuitPythonLibrariesUrl"))
        self.circuitpythonDocuUrlLineEdit.setText(
            Preferences.getMicroPython("CircuitPythonDocuUrl"))
        
        # BBC micro:bit URLs
        self.microbitFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("MicrobitFirmwareUrl"))
        self.microbitV1MicroPythonUrlLineEdit.setText(
            Preferences.getMicroPython("MicrobitMicroPythonUrl"))
        self.microbitV2MicroPythonUrlLineEdit.setText(
            Preferences.getMicroPython("MicrobitV2MicroPythonUrl"))
        self.microbitDocuUrlLineEdit.setText(
            Preferences.getMicroPython("MicrobitDocuUrl"))
        
        # Calliope mini URLs
        self.calliopeFirmwareUrlLineEdit.setText(
            Preferences.getMicroPython("CalliopeDAPLinkUrl"))
        self.calliopeMicroPythonUrlLineEdit.setText(
            Preferences.getMicroPython("CalliopeMicroPythonUrl"))
        self.calliopeDocuUrlLineEdit.setText(
            Preferences.getMicroPython("CalliopeDocuUrl"))
    
    def save(self):
        """
        Public slot to save the MicroPython configuration.
        """
        # workspace
        Preferences.setMicroPython(
            "MpyWorkspace",
            self.workspacePicker.text())
        
        # serial link parameters
        Preferences.setMicroPython(
            "SerialTimeout",
            self.timeoutSpinBox.value() * 1000)
        # converted to milliseconds
        Preferences.setMicroPython(
            "SyncTimeAfterConnect",
            self.syncTimeCheckBox.isChecked())
        
        # REPL Pane
        Preferences.setMicroPython(
            "ColorScheme",
            self.colorSchemeComboBox.currentText())
        Preferences.setMicroPython(
            "ReplLineWrap",
            self.replWrapCheckBox.isChecked())
        
        # Chart Pane
        Preferences.setMicroPython(
            "ChartColorTheme",
            self.chartThemeComboBox.currentData())
        
        # MPY Cross Compiler
        Preferences.setMicroPython(
            "MpyCrossCompiler",
            self.mpyCrossPicker.text())
        
        # PyBoard specifics
        Preferences.setMicroPython(
            "DfuUtilPath",
            self.dfuUtilPathPicker.text())
        
        # MicroPython URLs
        Preferences.setMicroPython(
            "MicroPythonFirmwareUrl",
            self.micropythonFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "MicroPythonDocuUrl",
            self.micropythonDocuUrlLineEdit.text())
        
        # CircuitPython URLs
        Preferences.setMicroPython(
            "CircuitPythonFirmwareUrl",
            self.circuitpythonFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "CircuitPythonLibrariesUrl",
            self.circuitpythonLibrariesUrlLineEdit.text())
        Preferences.setMicroPython(
            "CircuitPythonDocuUrl",
            self.circuitpythonDocuUrlLineEdit.text())
        
        # BBC micro:bit URLs
        Preferences.setMicroPython(
            "MicrobitFirmwareUrl",
            self.microbitFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "MicrobitMicroPythonUrl",
            self.microbitV1MicroPythonUrlLineEdit.text())
        Preferences.setMicroPython(
            "MicrobitV2MicroPythonUrl",
            self.microbitV2MicroPythonUrlLineEdit.text())
        Preferences.setMicroPython(
            "MicrobitDocuUrl",
            self.microbitDocuUrlLineEdit.text())
        
        # Calliope mini URLs
        Preferences.setMicroPython(
            "CalliopeDAPLinkUrl",
            self.calliopeFirmwareUrlLineEdit.text())
        Preferences.setMicroPython(
            "CalliopeMicroPythonUrl",
            self.calliopeMicroPythonUrlLineEdit.text())
        Preferences.setMicroPython(
            "CalliopeDocuUrl",
            self.calliopeDocuUrlLineEdit.text())


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    return MicroPythonPage()
