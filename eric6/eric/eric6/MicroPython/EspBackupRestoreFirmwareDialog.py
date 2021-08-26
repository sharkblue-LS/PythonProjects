# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select the ESP chip type and the backup and
restore parameters.
"""

import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_EspBackupRestoreFirmwareDialog import (
    Ui_EspBackupRestoreFirmwareDialog
)


class EspBackupRestoreFirmwareDialog(QDialog,
                                     Ui_EspBackupRestoreFirmwareDialog):
    """
    Class implementing a dialog to select the ESP chip type and the backup and
    restore parameters.
    """
    FlashModes = [
        ("Quad I/O", "qio"),
        ("Quad Output", "qout"),
        ("Dual I/O", "dio"),
        ("Dual Output", "dout"),
    ]
    FlashSizes = {
        "ESP32": [
            (" 1 MB", "0x100000"),
            (" 2 MB", "0x200000"),
            (" 4 MB", "0x400000"),
            (" 8 MB", "0x800000"),
            ("16 MB", "0x1000000"),
        ],
        "ESP8266": [
            ("256 KB", "0x40000"),
            ("512 KB", "0x80000"),
            (" 1 MB", "0x100000"),
            (" 2 MB", "0x200000"),
            (" 4 MB", "0x400000"),
            (" 8 MB", "0x800000"),
            ("16 MB", "0x1000000"),
        ],
    }
    
    def __init__(self, backupMode=True, parent=None):
        """
        Constructor
        
        @param backupMode flag indicating parameters for a firmware backup are
            requested
        @type bool
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EspBackupRestoreFirmwareDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__isBackupMode = backupMode
        
        self.espComboBox.addItems(["", "ESP32", "ESP8266"])
        
        self.firmwarePicker.setFilters(
            self.tr("Firmware Files (*.img);;All Files (*)"))
        if self.__isBackupMode:
            self.firmwarePicker.setMode(
                E5PathPickerModes.SaveFileEnsureExtensionMode)
            self.modeComboBox.setEnabled(False)
            self.setWindowTitle(self.tr("Backup Firmware"))
        else:
            self.firmwarePicker.setMode(E5PathPickerModes.OpenFileMode)
            for text, mode in self.FlashModes:
                self.modeComboBox.addItem(text, mode)
            self.setWindowTitle(self.tr("Restore Firmware"))
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateOkButton(self):
        """
        Private method to update the state of the OK button.
        """
        firmwareFile = self.firmwarePicker.text()
        enable = (bool(self.espComboBox.currentText()) and
                  bool(firmwareFile))
        if self.__isBackupMode:
            enable &= bool(self.sizeComboBox.currentText())
        else:
            enable &= os.path.exists(firmwareFile)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enable)
    
    @pyqtSlot(str)
    def on_espComboBox_currentTextChanged(self, chip):
        """
        Private slot to handle the selection of a chip type.
        
        @param chip selected chip type
        @type str
        """
        selectedSize = self.sizeComboBox.currentText()
        self.sizeComboBox.clear()
        if chip and chip in self.FlashSizes:
            self.sizeComboBox.addItem("")
            for text, data in self.FlashSizes[chip]:
                self.sizeComboBox.addItem(text, data)
            
            self.sizeComboBox.setCurrentText(selectedSize)
        
        self.__updateOkButton()
    
    @pyqtSlot(str)
    def on_firmwarePicker_textChanged(self, firmware):
        """
        Private slot handling a change of the firmware path.
        
        @param firmware path to the firmware
        @type str
        """
        self.__updateOkButton()
    
    def getData(self):
        """
        Public method to get the entered data.
        
        @return tuple containing the selected chip type, the firmware size,
            the flash mode and the path of the firmware file
        @rtype tuple of (str, str, str, str)
        """
        return (
            self.espComboBox.currentText().lower(),
            self.sizeComboBox.currentData(),
            self.modeComboBox.currentData(),
            self.firmwarePicker.text(),
        )
