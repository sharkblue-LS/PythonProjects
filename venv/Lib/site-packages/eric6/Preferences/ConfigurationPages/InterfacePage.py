# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Interface configuration page.
"""

import glob
import os

from PyQt5.QtCore import pyqtSlot, QTranslator
from PyQt5.QtWidgets import QStyleFactory

from E5Gui.E5PathPicker import E5PathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_InterfacePage import Ui_InterfacePage

import Preferences
import Utilities

from eric6config import getConfig


class InterfacePage(ConfigurationPageBase, Ui_InterfacePage):
    """
    Class implementing the Interface configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(InterfacePage, self).__init__()
        self.setupUi(self)
        self.setObjectName("InterfacePage")
        
        self.styleSheetPicker.setMode(E5PathPickerModes.OpenFileMode)
        self.styleSheetPicker.setFilters(self.tr(
            "Qt Style Sheets (*.qss);;Cascading Style Sheets (*.css);;"
            "All files (*)"))
        self.styleSheetPicker.setDefaultDirectory(getConfig("ericStylesDir"))
        
        # set initial values
        self.__populateStyleCombo()
        self.__populateLanguageCombo()
        self.__populateShellPositionCombo()
        
        self.uiBrowsersListFoldersFirstCheckBox.setChecked(
            Preferences.getUI("BrowsersListFoldersFirst"))
        self.uiBrowsersHideNonPublicCheckBox.setChecked(
            Preferences.getUI("BrowsersHideNonPublic"))
        self.uiBrowsersSortByOccurrenceCheckBox.setChecked(
            Preferences.getUI("BrowsersListContentsByOccurrence"))
        self.browserShowCodingCheckBox.setChecked(
            Preferences.getUI("BrowserShowCoding"))
        self.fileFiltersEdit.setText(
            Preferences.getUI("BrowsersFileFilters"))
        
        self.uiCaptionShowsFilenameGroupBox.setChecked(
            Preferences.getUI("CaptionShowsFilename"))
        self.filenameLengthSpinBox.setValue(
            Preferences.getUI("CaptionFilenameLength"))
        self.styleSheetPicker.setText(Preferences.getUI("StyleSheet"))
        
        layoutType = Preferences.getUI("LayoutType")
        if layoutType == "Sidebars":
            index = 0
        elif layoutType == "Toolboxes":
            index = 1
        else:
            index = 0   # default for bad values
        self.layoutComboBox.setCurrentIndex(index)
        
        # integrated tools activation
        # left side
        self.templateViewerCheckBox.setChecked(
            Preferences.getUI("ShowTemplateViewer"))
        self.fileBrowserCheckBox.setChecked(
            Preferences.getUI("ShowFileBrowser"))
        self.symbolsCheckBox.setChecked(
            Preferences.getUI("ShowSymbolsViewer"))
        # right side
        self.codeDocumentationViewerCheckBox.setChecked(
            Preferences.getUI("ShowCodeDocumentationViewer"))
        self.microPythonCheckBox.setChecked(
            Preferences.getUI("ShowMicroPython"))
        self.pypiCheckBox.setChecked(
            Preferences.getUI("ShowPyPIPackageManager"))
        self.condaCheckBox.setChecked(
            Preferences.getUI("ShowCondaPackageManager"))
        self.cooperationCheckBox.setChecked(
            Preferences.getUI("ShowCooperation"))
        self.ircCheckBox.setChecked(
            Preferences.getUI("ShowIrc"))
        # bottom side
        self.numbersCheckBox.setChecked(
            Preferences.getUI("ShowNumbersViewer"))
        
        self.delaySpinBox.setValue(Preferences.getUI("SidebarDelay"))
        
    def save(self):
        """
        Public slot to save the Interface configuration.
        """
        # save the style settings
        styleIndex = self.styleComboBox.currentIndex()
        style = self.styleComboBox.itemData(styleIndex)
        Preferences.setUI("Style", style)
        
        # save the other UI related settings
        Preferences.setUI(
            "BrowsersListFoldersFirst",
            self.uiBrowsersListFoldersFirstCheckBox.isChecked())
        Preferences.setUI(
            "BrowsersHideNonPublic",
            self.uiBrowsersHideNonPublicCheckBox.isChecked())
        Preferences.setUI(
            "BrowsersListContentsByOccurrence",
            self.uiBrowsersSortByOccurrenceCheckBox.isChecked())
        Preferences.setUI(
            "BrowserShowCoding",
            self.browserShowCodingCheckBox.isChecked())
        Preferences.setUI(
            "BrowsersFileFilters",
            self.fileFiltersEdit.text())
        
        Preferences.setUI(
            "CaptionShowsFilename",
            self.uiCaptionShowsFilenameGroupBox.isChecked())
        Preferences.setUI(
            "CaptionFilenameLength",
            self.filenameLengthSpinBox.value())
        Preferences.setUI(
            "StyleSheet",
            self.styleSheetPicker.text())
        
        # save the language settings
        uiLanguageIndex = self.languageComboBox.currentIndex()
        if uiLanguageIndex:
            uiLanguage = self.languageComboBox.itemData(uiLanguageIndex)
        else:
            uiLanguage = None
        Preferences.setUILanguage(uiLanguage)
        
        # save the interface layout settings
        if self.layoutComboBox.currentIndex() == 0:
            layoutType = "Sidebars"
        elif self.layoutComboBox.currentIndex() == 1:
            layoutType = "Toolboxes"
        else:
            layoutType = "Sidebars"    # just in case
        Preferences.setUI("LayoutType", layoutType)
        
        # save the shell position setting
        shellPositionIndex = self.shellPositionComboBox.currentIndex()
        shellPosition = self.shellPositionComboBox.itemData(shellPositionIndex)
        Preferences.setUI("ShellPosition", shellPosition)
        
        # save the integrated tools activation
        # left side
        Preferences.setUI(
            "ShowTemplateViewer",
            self.templateViewerCheckBox.isChecked())
        Preferences.setUI(
            "ShowFileBrowser",
            self.fileBrowserCheckBox.isChecked())
        Preferences.setUI(
            "ShowSymbolsViewer",
            self.symbolsCheckBox.isChecked())
        # right side
        Preferences.setUI(
            "ShowCodeDocumentationViewer",
            self.codeDocumentationViewerCheckBox.isChecked())
        Preferences.setUI(
            "ShowMicroPython",
            self.microPythonCheckBox.isChecked())
        Preferences.setUI(
            "ShowPyPIPackageManager",
            self.pypiCheckBox.isChecked())
        Preferences.setUI(
            "ShowCondaPackageManager",
            self.condaCheckBox.isChecked())
        Preferences.setUI(
            "ShowCooperation",
            self.cooperationCheckBox.isChecked())
        Preferences.setUI(
            "ShowIrc",
            self.ircCheckBox.isChecked())
        # bottom side
        Preferences.setUI(
            "ShowNumbersViewer",
            self.numbersCheckBox.isChecked())
        
        Preferences.setUI("SidebarDelay", self.delaySpinBox.value())
        
    def __populateStyleCombo(self):
        """
        Private method to populate the style combo box.
        """
        curStyle = Preferences.getUI("Style")
        styles = sorted(list(QStyleFactory.keys()))
        self.styleComboBox.addItem(self.tr('System'), "System")
        for style in styles:
            self.styleComboBox.addItem(style, style)
        currentIndex = self.styleComboBox.findData(curStyle)
        if currentIndex == -1:
            currentIndex = 0
        self.styleComboBox.setCurrentIndex(currentIndex)
        
    def __populateLanguageCombo(self):
        """
        Private method to initialize the language combo box.
        """
        self.languageComboBox.clear()
        
        fnlist = (
            glob.glob("eric6_*.qm") +
            glob.glob(os.path.join(
                getConfig('ericTranslationsDir'), "eric6_*.qm")) +
            glob.glob(os.path.join(Utilities.getConfigDir(), "eric6_*.qm"))
        )
        locales = {}
        for fn in fnlist:
            locale = os.path.basename(fn)[6:-3]
            if locale not in locales:
                translator = QTranslator()
                translator.load(fn)
                locales[locale] = (
                    translator.translate(
                        "InterfacePage", "English",
                        "Translate this with your language") +
                    " ({0})".format(locale)
                )
        localeList = sorted(list(locales.keys()))
        try:
            uiLanguage = Preferences.getUILanguage()
            if uiLanguage == "None" or uiLanguage is None:
                currentIndex = 0
            elif uiLanguage == "System":
                currentIndex = 1
            else:
                currentIndex = localeList.index(uiLanguage) + 2
        except ValueError:
            currentIndex = 0
        self.languageComboBox.clear()
        
        self.languageComboBox.addItem("English (default)", "None")
        self.languageComboBox.addItem(self.tr('System'), "System")
        for locale in localeList:
            self.languageComboBox.addItem(locales[locale], locale)
        self.languageComboBox.setCurrentIndex(currentIndex)
    
    def __populateShellPositionCombo(self):
        """
        Private method to initialize the shell position combo box.
        """
        self.shellPositionComboBox.addItem(self.tr("Left Side"), "left")
        self.shellPositionComboBox.addItem(self.tr("Right Side"), "right")
        self.shellPositionComboBox.addItem(self.tr("Bottom Side"), "bottom")
        
        shellPosition = Preferences.getUI("ShellPosition")
        if shellPosition not in ("left", "right", "bottom"):
            shellPosition = "bottom"
        index = self.shellPositionComboBox.findData(shellPosition)
        self.shellPositionComboBox.setCurrentIndex(index)
    
    @pyqtSlot()
    def on_resetLayoutButton_clicked(self):
        """
        Private method to reset layout to factory defaults.
        """
        Preferences.resetLayout()
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = InterfacePage()
    return page
