# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Debugger Python3 configuration page.
"""

from PyQt5.QtCore import pyqtSlot

from E5Gui.E5Application import e5App
from E5Gui.E5PathPicker import E5PathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_DebuggerPython3Page import Ui_DebuggerPython3Page

import Preferences
import UI.PixmapCache


class DebuggerPython3Page(ConfigurationPageBase, Ui_DebuggerPython3Page):
    """
    Class implementing the Debugger Python3 configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(DebuggerPython3Page, self).__init__()
        self.setupUi(self)
        self.setObjectName("DebuggerPython3Page")
        
        try:
            self.__virtualenvManager = e5App().getObject("VirtualEnvManager")
        except KeyError:
            from VirtualEnv.VirtualenvManager import VirtualenvManager
            self.__virtualenvManager = VirtualenvManager()
        
        self.venvDlgButton.setIcon(UI.PixmapCache.getIcon("virtualenv"))
        
        self.debugClientPicker.setMode(E5PathPickerModes.OpenFileMode)
        self.debugClientPicker.setToolTip(self.tr(
            "Press to select the Debug Client via a file selection dialog"))
        self.debugClientPicker.setFilters(self.tr("Python Files (*.py *.py3)"))
        
        self.__populateAndSetVenvComboBox()
        
        # set initial values
        dct = Preferences.getDebugger("DebugClientType3")
        if dct == "standard":
            self.standardButton.setChecked(True)
        else:
            self.customButton.setChecked(True)
        self.debugClientPicker.setText(
            Preferences.getDebugger("DebugClient3"), toNative=False)
        self.pyRedirectCheckBox.setChecked(
            Preferences.getDebugger("Python3Redirect"))
        self.pyNoEncodingCheckBox.setChecked(
            Preferences.getDebugger("Python3NoEncoding"))
        self.sourceExtensionsEdit.setText(
            Preferences.getDebugger("Python3Extensions"))
    
    def save(self):
        """
        Public slot to save the Debugger Python configuration.
        """
        Preferences.setDebugger(
            "Python3VirtualEnv",
            self.venvComboBox.currentText())
        if self.standardButton.isChecked():
            dct = "standard"
        else:
            dct = "custom"
        Preferences.setDebugger("DebugClientType3", dct)
        Preferences.setDebugger(
            "DebugClient3",
            self.debugClientPicker.text(toNative=False))
        Preferences.setDebugger(
            "Python3Redirect",
            self.pyRedirectCheckBox.isChecked())
        Preferences.setDebugger(
            "Python3NoEncoding",
            self.pyNoEncodingCheckBox.isChecked())
    
    def __populateAndSetVenvComboBox(self):
        """
        Private method to populate and set the virtual environment combo box.
        """
        self.venvComboBox.clear()
        self.venvComboBox.addItems(
            [""] +
            sorted(self.__virtualenvManager.getVirtualenvNames())
        )
        
        # set initial value
        venvName = Preferences.getDebugger("Python3VirtualEnv")
        if venvName:
            index = self.venvComboBox.findText(venvName)
            if index < 0:
                index = 0
            self.venvComboBox.setCurrentIndex(index)
    
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """
        Private slot handling a click of the refresh button.
        """
        self.sourceExtensionsEdit.setText(
            Preferences.getDebugger("Python3Extensions"))
    
    @pyqtSlot()
    def on_venvDlgButton_clicked(self):
        """
        Private slot to show the virtual environment manager dialog.
        """
        self.__virtualenvManager.showVirtualenvManagerDialog(modal=True)
        self.__populateAndSetVenvComboBox()
        self.activateWindow()
        self.raise_()
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = DebuggerPython3Page()
    return page
