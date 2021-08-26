# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing the Git configuration page.
"""

import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Preferences.ConfigurationPages.ConfigurationPageBase import (
    ConfigurationPageBase
)
from .Ui_GitPage import Ui_GitPage


class GitPage(ConfigurationPageBase, Ui_GitPage):
    """
    Class implementing the Git configuration page.
    """
    def __init__(self, plugin):
        """
        Constructor
        
        @param plugin reference to the plugin object
        """
        super(GitPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("GitPage")
        
        self.__plugin = plugin
        
        # set initial values
        # log
        self.logSpinBox.setValue(
            self.__plugin.getPreferences("LogLimit"))
        self.logWidthSpinBox.setValue(
            self.__plugin.getPreferences("LogSubjectColumnWidth"))
        self.findHarderCheckBox.setChecked(
            self.__plugin.getPreferences("FindCopiesHarder"))
        # commit
        self.commitSpinBox.setValue(
            self.__plugin.getPreferences("CommitMessages"))
        self.commitIdSpinBox.setValue(
            self.__plugin.getPreferences("CommitIdLength"))
        # cleanup
        self.cleanupPatternEdit.setText(
            self.__plugin.getPreferences("CleanupPatterns"))
        # repository optimization
        self.aggressiveCheckBox.setChecked(
            self.__plugin.getPreferences("AggressiveGC"))
    
    def save(self):
        """
        Public slot to save the Git configuration.
        """
        # log
        self.__plugin.setPreferences(
            "LogLimit", self.logSpinBox.value())
        self.__plugin.setPreferences(
            "LogSubjectColumnWidth", self.logWidthSpinBox.value())
        self.__plugin.setPreferences(
            "FindCopiesHarder", self.findHarderCheckBox.isChecked())
        # commit
        self.__plugin.setPreferences(
            "CommitMessages", self.commitSpinBox.value())
        self.__plugin.setPreferences(
            "CommitMessages", self.commitIdSpinBox.value())
        # cleanup
        self.__plugin.setPreferences(
            "CleanupPatterns", self.cleanupPatternEdit.text())
        # repository optimization
        self.__plugin.setPreferences(
            "AggressiveGC", self.aggressiveCheckBox.isChecked())
    
    @pyqtSlot()
    def on_configButton_clicked(self):
        """
        Private slot to edit the (per user) Git configuration file.
        """
        from QScintilla.MiniEditor import MiniEditor
        cfgFile = self.__plugin.getConfigPath()
        if not os.path.exists(cfgFile):
            from ..GitUserConfigDataDialog import GitUserConfigDataDialog
            dlg = GitUserConfigDataDialog()
            if dlg.exec() == QDialog.DialogCode.Accepted:
                firstName, lastName, email = dlg.getData()
            else:
                firstName, lastName, email = (
                    "Firstname", "Lastname", "email_address")
            try:
                with open(cfgFile, "w") as f:
                    f.write("[user]\n")
                    f.write("    name = {0} {1}\n".format(firstName, lastName))
                    f.write("    email = {0}\n".format(email))
            except OSError:
                # ignore these
                pass
        editor = MiniEditor(cfgFile, "Properties", self)
        editor.show()
