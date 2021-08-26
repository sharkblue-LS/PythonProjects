# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the conda configuration page.
"""

from E5Gui.E5PathPicker import E5PathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_CondaPage import Ui_CondaPage

import Preferences


class CondaPage(ConfigurationPageBase, Ui_CondaPage):
    """
    Class implementing the conda configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(CondaPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("CondaPage")
        
        self.condaExePicker.setMode(E5PathPickerModes.OpenFileMode)
        self.condaExePicker.setToolTip(self.tr(
            "Press to select the conda executable via a file selection"
            " dialog."))
        
        # set initial values
        self.__condaExecutable = Preferences.getConda("CondaExecutable")
        self.condaExePicker.setText(self.__condaExecutable)
        
    def save(self):
        """
        Public slot to save the conda configuration.
        """
        condaExecutable = self.condaExePicker.text()
        if condaExecutable != self.__condaExecutable:
            Preferences.setConda("CondaExecutable", condaExecutable)
            
            import CondaInterface
            CondaInterface.resetInterface()
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = CondaPage()
    return page
