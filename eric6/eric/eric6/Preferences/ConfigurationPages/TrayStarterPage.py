# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the tray starter configuration page.
"""

import os

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_TrayStarterPage import Ui_TrayStarterPage

import Preferences
import UI.PixmapCache


class TrayStarterPage(ConfigurationPageBase, Ui_TrayStarterPage):
    """
    Class implementing the tray starter configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(TrayStarterPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("TrayStarterPage")
        
        self.standardButton.setIcon(UI.PixmapCache.getIcon("erict"))
        self.highContrastButton.setIcon(UI.PixmapCache.getIcon("erict-hc"))
        self.blackWhiteButton.setIcon(UI.PixmapCache.getIcon("erict-bw"))
        self.blackWhiteInverseButton.setIcon(
            UI.PixmapCache.getIcon("erict-bwi"))
        
        # set initial values
        iconName = os.path.splitext(
            Preferences.getTrayStarter("TrayStarterIcon"))[0]
        if iconName == "erict":
            self.standardButton.setChecked(True)
        elif iconName == "erict-hc":
            self.highContrastButton.setChecked(True)
        elif iconName == "erict-bw":
            self.blackWhiteButton.setChecked(True)
        elif iconName == "erict-bwi":
            self.blackWhiteInverseButton.setChecked(True)
    
    def save(self):
        """
        Public slot to save the Python configuration.
        """
        if self.standardButton.isChecked():
            iconName = "erict"
        elif self.highContrastButton.isChecked():
            iconName = "erict-hc"
        elif self.blackWhiteButton.isChecked():
            iconName = "erict-bw"
        elif self.blackWhiteInverseButton.isChecked():
            iconName = "erict-bwi"
        Preferences.setTrayStarter("TrayStarterIcon", iconName)
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = TrayStarterPage()
    return page
