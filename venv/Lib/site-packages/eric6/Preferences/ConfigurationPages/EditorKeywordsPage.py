# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the editor highlighter keywords configuration page.
"""

from PyQt5.QtCore import pyqtSlot

from E5Gui import E5MessageBox

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_EditorKeywordsPage import Ui_EditorKeywordsPage

import Preferences


class EditorKeywordsPage(ConfigurationPageBase, Ui_EditorKeywordsPage):
    """
    Class implementing the editor highlighter keywords configuration page.
    """
    MaxKeywordSets = 8          # max. 8 sets are allowed
    
    def __init__(self):
        """
        Constructor
        """
        super(EditorKeywordsPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("EditorKeywordsPage")
        
        # set initial values
        import QScintilla.Lexers
        from QScintilla.Lexers.LexerContainer import LexerContainer
        
        self.__keywords = {
            "": {
                "Sets": [""] * (self.MaxKeywordSets + 1),
                "Descriptions": [""] * (self.MaxKeywordSets + 1),
                "MaxSets": 0,
            }
        }
        
        languages = sorted(
            [''] + list(QScintilla.Lexers.getSupportedLanguages().keys()))
        for lang in languages:
            if lang:
                lex = QScintilla.Lexers.getLexer(lang)
                if isinstance(lex, LexerContainer):
                    continue
                keywords = Preferences.getEditorKeywords(lang)[:]
                if keywords:
                    # set empty entries to default values
                    for kwSet in range(1, self.MaxKeywordSets + 1):
                        if not keywords[kwSet]:
                            kw = lex.defaultKeywords(kwSet)
                            if kw is None:
                                kw = ""
                            keywords[kwSet] = kw
                else:
                    keywords = [""]
                    descriptions = [""]
                    for kwSet in range(1, self.MaxKeywordSets + 1):
                        kw = lex.keywords(kwSet)
                        if kw is None:
                            kw = ""
                        keywords.append(kw)
                descriptions = [""]
                for kwSet in range(1, self.MaxKeywordSets + 1):
                    desc = lex.keywordsDescription(kwSet)
                    descriptions.append(desc)
                defaults = [""]
                for kwSet in range(1, self.MaxKeywordSets + 1):
                    dkw = lex.defaultKeywords(kwSet)
                    if dkw is None:
                        dkw = ""
                    defaults.append(dkw)
                self.__keywords[lang] = {
                    "Sets": keywords,
                    "Descriptions": descriptions,
                    "DefaultSets": defaults,
                    "MaxSets": lex.maximumKeywordSet(),
                }
            self.languageCombo.addItem(
                QScintilla.Lexers.getLanguageIcon(lang, False),
                lang)
        
        self.currentLanguage = ''
        self.currentSet = 1
        self.on_languageCombo_activated(0)
    
    def save(self):
        """
        Public slot to save the editor highlighter keywords configuration.
        """
        lang = self.languageCombo.currentText()
        kwSet = self.setSpinBox.value()
        self.__keywords[lang]["Sets"][kwSet] = self.keywordsEdit.toPlainText()
        
        for lang, keywords in self.__keywords.items():
            Preferences.setEditorKeywords(lang, keywords["Sets"])
        
    @pyqtSlot(int)
    def on_languageCombo_activated(self, index):
        """
        Private slot to fill the keywords edit.
        
        @param index index of the selected entry
        @type int
        """
        language = self.languageCombo.itemText(index)
        
        self.defaultButton.setEnabled(bool(language))
        self.allDefaultButton.setEnabled(bool(language))
        
        if self.currentLanguage == language:
            return
        
        if self.setSpinBox.value() == 1:
            self.on_setSpinBox_valueChanged(1)
        if self.__keywords[language]["MaxSets"]:
            first = 1
            last = self.__keywords[language]["MaxSets"]
        else:
            first, last = self.MaxKeywordSets + 1, 0
            for kwSet in range(1, self.MaxKeywordSets + 1):
                if self.__keywords[language]["Descriptions"][kwSet] != "":
                    first = min(first, kwSet)
                    last = max(last, kwSet)
        self.setSpinBox.setEnabled(language != "" and
                                   first <= self.MaxKeywordSets)
        self.keywordsEdit.setEnabled(language != "" and
                                     first <= self.MaxKeywordSets)
        if first <= self.MaxKeywordSets:
            self.setSpinBox.setMinimum(first)
            self.setSpinBox.setMaximum(last)
            self.setSpinBox.setValue(first)
        else:
            self.setSpinBox.setMinimum(0)
            self.setSpinBox.setMaximum(0)
            self.setSpinBox.setValue(0)
    
    @pyqtSlot(int)
    def on_setSpinBox_valueChanged(self, kwSet):
        """
        Private slot to fill the keywords edit.
        
        @param kwSet number of the selected keyword set
        @type int
        """
        language = self.languageCombo.currentText()
        if self.currentLanguage == language and self.currentSet == kwSet:
            return
        
        self.__keywords[self.currentLanguage]["Sets"][self.currentSet] = (
            self.keywordsEdit.toPlainText()
        )
        
        self.currentLanguage = language
        self.currentSet = kwSet
        self.setDescriptionLabel.setText("<b>{0}</b>".format(
            self.__keywords[language]["Descriptions"][kwSet]))
        self.keywordsEdit.setPlainText(
            self.__keywords[language]["Sets"][kwSet])
    
    @pyqtSlot()
    def on_defaultButton_clicked(self):
        """
        Private slot to set the current keyword set to default values.
        """
        if bool(self.keywordsEdit.toPlainText()):
            ok = E5MessageBox.yesNo(
                self,
                self.tr("Reset to Default"),
                self.tr("Shall the current keyword set really be reset to"
                        " default values?"))
        else:
            ok = True
        if ok:
            language = self.languageCombo.currentText()
            kwSet = self.setSpinBox.value()
            self.__keywords[language]["Sets"][kwSet] = (
                self.__keywords[language]["DefaultSets"][kwSet]
            )
            self.keywordsEdit.setPlainText(
                self.__keywords[language]["Sets"][kwSet])
    
    @pyqtSlot()
    def on_allDefaultButton_clicked(self):
        """
        Private slot to set all keyword sets of the current language to default
        values.
        """
        ok = E5MessageBox.yesNo(
            self,
            self.tr("Reset All to Default"),
            self.tr("Shall all keyword sets of the current language really be"
                    " reset to default values?"))
        if ok:
            language = self.languageCombo.currentText()
            kwSet = self.setSpinBox.value()
            self.__keywords[language]["Sets"] = (
                self.__keywords[language]["DefaultSets"][:]
            )
            self.keywordsEdit.setPlainText(
                self.__keywords[language]["Sets"][kwSet])


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @type ConfigurationWidget
    @return reference to the instantiated page
    @rtype ConfigurationPageBase
    """
    page = EditorKeywordsPage()
    return page
