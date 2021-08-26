# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Editor Typing configuration page.
"""

from PyQt5.QtCore import pyqtSlot

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_EditorTypingPage import Ui_EditorTypingPage

import Preferences


class EditorTypingPage(ConfigurationPageBase, Ui_EditorTypingPage):
    """
    Class implementing the Editor Typing configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(EditorTypingPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("EditorTypingPage")
        
        # set initial values
        self.pageIds = {
            ' ': self.stackedWidget.indexOf(self.emptyPage),
            'Python': self.stackedWidget.indexOf(self.pythonPage),
            'Ruby': self.stackedWidget.indexOf(self.rubyPage),
            'YAML': self.stackedWidget.indexOf(self.yamlPage),
        }
        languages = sorted(list(self.pageIds.keys()))
        for language in languages:
            self.languageCombo.addItem(language, self.pageIds[language])
        
        # Python
        self.pythonGroup.setChecked(
            Preferences.getEditorTyping("Python/EnabledTypingAids"))
        self.pythonInsertClosingBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Python/InsertClosingBrace"))
        self.pythonSkipBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Python/SkipBrace"))
        self.pythonIndentBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Python/IndentBrace"))
        self.pythonInsertQuoteCheckBox.setChecked(
            Preferences.getEditorTyping("Python/InsertQuote"))
        self.pythonDedentElseCheckBox.setChecked(
            Preferences.getEditorTyping("Python/DedentElse"))
        self.pythonDedentExceptCheckBox.setChecked(
            Preferences.getEditorTyping("Python/DedentExcept"))
        self.pythonInsertImportCheckBox.setChecked(
            Preferences.getEditorTyping("Python/InsertImport"))
        self.pythonImportBraceTypeCheckBox.setChecked(
            Preferences.getEditorTyping("Python/ImportBraceType"))
        self.pythonInsertSelfCheckBox.setChecked(
            Preferences.getEditorTyping("Python/InsertSelf"))
        self.pythonInsertBlankCheckBox.setChecked(
            Preferences.getEditorTyping("Python/InsertBlank"))
        self.pythonColonDetectionCheckBox.setChecked(
            Preferences.getEditorTyping("Python/ColonDetection"))
        self.pythonDedentDefCheckBox.setChecked(
            Preferences.getEditorTyping("Python/DedentDef"))
        
        # Ruby
        self.rubyGroup.setChecked(
            Preferences.getEditorTyping("Ruby/EnabledTypingAids"))
        self.rubyInsertClosingBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/InsertClosingBrace"))
        self.rubySkipBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/SkipBrace"))
        self.rubyIndentBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/IndentBrace"))
        self.rubyInsertQuoteCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/InsertQuote"))
        self.rubyInsertBlankCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/InsertBlank"))
        self.rubyInsertHereDocCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/InsertHereDoc"))
        self.rubyInsertInlineDocCheckBox.setChecked(
            Preferences.getEditorTyping("Ruby/InsertInlineDoc"))
        
        # YAML
        self.yamlGroup.setChecked(
            Preferences.getEditorTyping("Yaml/EnabledTypingAids"))
        self.yamlInsertClosingBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/InsertClosingBrace"))
        self.yamlSkipBraceCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/SkipBrace"))
        self.yamlInsertQuoteCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/InsertQuote"))
        self.yamlAutoIndentationCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/AutoIndentation"))
        self.yamlColonDetectionCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/ColonDetection"))
        self.yamlInsertBlankDashCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/InsertBlankDash"))
        self.yamlInsertBlankColonCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/InsertBlankColon"))
        self.yamlInsertBlankQuestionCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/InsertBlankQuestion"))
        self.yamlInsertBlankCommaCheckBox.setChecked(
            Preferences.getEditorTyping("Yaml/InsertBlankComma"))
        
        self.on_languageCombo_activated(0)
    
    def save(self):
        """
        Public slot to save the Editor Typing configuration.
        """
        # Python
        Preferences.setEditorTyping(
            "Python/EnabledTypingAids",
            self.pythonGroup.isChecked())
        Preferences.setEditorTyping(
            "Python/InsertClosingBrace",
            self.pythonInsertClosingBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/SkipBrace",
            self.pythonSkipBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/IndentBrace",
            self.pythonIndentBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/InsertQuote",
            self.pythonInsertQuoteCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/DedentElse",
            self.pythonDedentElseCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/DedentExcept",
            self.pythonDedentExceptCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/InsertImport",
            self.pythonInsertImportCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/ImportBraceType",
            self.pythonImportBraceTypeCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/InsertSelf",
            self.pythonInsertSelfCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/InsertBlank",
            self.pythonInsertBlankCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/ColonDetection",
            self.pythonColonDetectionCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Python/DedentDef",
            self.pythonDedentDefCheckBox.isChecked())
        
        # Ruby
        Preferences.setEditorTyping(
            "Ruby/EnabledTypingAids",
            self.rubyGroup.isChecked())
        Preferences.setEditorTyping(
            "Ruby/InsertClosingBrace",
            self.rubyInsertClosingBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Ruby/SkipBrace",
            self.rubySkipBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Ruby/IndentBrace",
            self.rubyIndentBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Ruby/InsertQuote",
            self.rubyInsertQuoteCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Ruby/InsertBlank",
            self.rubyInsertBlankCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Ruby/InsertHereDoc",
            self.rubyInsertHereDocCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Ruby/InsertInlineDoc",
            self.rubyInsertInlineDocCheckBox.isChecked())
        
        # YAML
        Preferences.setEditorTyping(
            "Yaml/EnabledTypingAids",
            self.yamlGroup.isChecked())
        Preferences.setEditorTyping(
            "Yaml/InsertClosingBrace",
            self.yamlInsertClosingBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/SkipBrace",
            self.yamlSkipBraceCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/InsertQuote",
            self.yamlInsertQuoteCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/AutoIndentation",
            self.yamlAutoIndentationCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/ColonDetection",
            self.yamlColonDetectionCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/InsertBlankDash",
            self.yamlInsertBlankDashCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/InsertBlankColon",
            self.yamlInsertBlankColonCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/InsertBlankQuestion",
            self.yamlInsertBlankQuestionCheckBox.isChecked())
        Preferences.setEditorTyping(
            "Yaml/InsertBlankComma",
            self.yamlInsertBlankCommaCheckBox.isChecked())
    
    @pyqtSlot(int)
    def on_languageCombo_activated(self, index):
        """
        Private slot to select the page related to the selected language.
        
        @param index index of the selected entry
        @type int
        """
        language = self.languageCombo.itemText(index)
        try:
            index = self.pageIds[language]
        except KeyError:
            index = self.pageIds[' ']
        self.stackedWidget.setCurrentIndex(index)


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = EditorTypingPage()
    return page
