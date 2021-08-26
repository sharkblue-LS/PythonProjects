# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Editor Calltips configuration page.
"""

from PyQt5.Qsci import QsciScintilla

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_EditorCalltipsPage import Ui_EditorCalltipsPage

import Preferences


class EditorCalltipsPage(ConfigurationPageBase, Ui_EditorCalltipsPage):
    """
    Class implementing the Editor Calltips configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(EditorCalltipsPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("EditorCalltipsPage")
        
        self.positionComboBox.addItem(
            self.tr("Below Text"),
            QsciScintilla.CallTipsPosition.CallTipsBelowText)
        self.positionComboBox.addItem(
            self.tr("Above Text"),
            QsciScintilla.CallTipsPosition.CallTipsAboveText)
        
        # set initial values
        self.ctEnabledCheckBox.setChecked(
            Preferences.getEditor("CallTipsEnabled"))
        
        self.ctVisibleSlider.setValue(
            Preferences.getEditor("CallTipsVisible"))
        
        self.initColour("CallTipsBackground", self.calltipsBackgroundButton,
                        Preferences.getEditorColour)
        self.initColour("CallTipsForeground", self.calltipsForegroundButton,
                        Preferences.getEditorColour)
        self.initColour("CallTipsHighlight", self.calltipsHighlightButton,
                        Preferences.getEditorColour)
        
        self.ctScintillaCheckBox.setChecked(
            Preferences.getEditor("CallTipsScintillaOnFail"))
        
        self.positionComboBox.setCurrentIndex(
            self.positionComboBox.findData(
                Preferences.getEditor("CallTipsPosition")))
        
    def save(self):
        """
        Public slot to save the EditorCalltips configuration.
        """
        Preferences.setEditor(
            "CallTipsEnabled",
            self.ctEnabledCheckBox.isChecked())
        
        Preferences.setEditor(
            "CallTipsVisible",
            self.ctVisibleSlider.value())
        
        self.saveColours(Preferences.setEditorColour)
        
        Preferences.setEditor(
            "CallTipsScintillaOnFail",
            self.ctScintillaCheckBox.isChecked())
        
        Preferences.setEditor(
            "CallTipsPosition",
            self.positionComboBox.itemData(
                self.positionComboBox.currentIndex()))


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = EditorCalltipsPage()
    return page
