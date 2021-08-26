# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the pip configuration page.
"""

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_PipPage import Ui_PipPage

from PipInterface.Pip import Pip

import Preferences


class PipPage(ConfigurationPageBase, Ui_PipPage):
    """
    Class implementing the pip configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(PipPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("PipPage")
        
        self.indexLabel.setText(self.tr(
            '<b>Note:</b> Leave empty to use the default index URL ('
            '<a href="{0}">{0}</a>).')
            .format(Pip.DefaultPyPiUrl))
        
        # set initial values
        self.indexEdit.setText(Preferences.getPip("PipSearchIndex"))
        self.noCondaCheckBox.setChecked(
            Preferences.getPip("ExcludeCondaEnvironments"))
    
    def save(self):
        """
        Public slot to save the pip configuration.
        """
        Preferences.setPip(
            "PipSearchIndex", self.indexEdit.text().strip())
        Preferences.setPip(
            "ExcludeCondaEnvironments", self.noCondaCheckBox.isChecked())


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = PipPage()
    return page
