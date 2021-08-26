# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Time Tracker configuration page.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QListWidgetItem

from E5Gui import E5MessageBox

from Preferences.ConfigurationPages.ConfigurationPageBase import (
    ConfigurationPageBase
)
from .Ui_TranslatorPage import Ui_TranslatorPage

from ..TranslatorLanguagesDb import TranslatorLanguagesDb
from .. import TranslatorEngines


class TranslatorPage(ConfigurationPageBase, Ui_TranslatorPage):
    """
    Class implementing the Time Tracker configuration page.
    """
    def __init__(self, plugin):
        """
        Constructor
        
        @param plugin reference to the plugin object
        """
        super(TranslatorPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("TranslatorPage")
        
        self.__plugin = plugin
        self.__enableLanguageWarning = True
        
        self.deeplLabel.setText(self.tr(
            """<p>A key is <b>required</b> to use this service."""
            """ <a href="{0}">Get a commercial API key.</a></p>""").format(
                TranslatorEngines.getKeyUrl("deepl")))
        self.googlev2Label.setText(self.tr(
            """<p>A key is <b>required</b> to use this service."""
            """ <a href="{0}">Get a commercial API key.</a></p>""").format(
                TranslatorEngines.getKeyUrl("googlev2")))
        self.ibmLabel.setText(self.tr(
            """<p>A key is <b>required</b> to use this service."""
            """ <a href="{0}">Register with IBM Cloud.</a></p>""").format(
                TranslatorEngines.getKeyUrl("ibm_watson")))
        self.msLabel.setText(self.tr(
            """<p>A registration of the text translation service is"""
            """ <b>required</b>. <a href="{0}">Register with Microsoft"""
            """ Azure.</a></p>""").format(
                TranslatorEngines.getKeyUrl("microsoft")))
        self.mymemoryLabel.setText(self.tr(
            """<p>A key is <b>optional</b> to use this service."""
            """ <a href="{0}">Get a free API key.</a></p>""").format(
                TranslatorEngines.getKeyUrl("mymemory")))
        self.yandexLabel.setText(self.tr(
            """<p>A key is <b>required</b> to use this service."""
            """ <a href="{0}">Get a free API key.</a></p>""").format(
                TranslatorEngines.getKeyUrl("yandex")))
        
        # set initial values
        enabledLanguages = self.__plugin.getPreferences("EnabledLanguages")
        languages = TranslatorLanguagesDb()
        for languageCode in languages.getAllLanguages():
            itm = QListWidgetItem()
            itm.setText(languages.getLanguage(languageCode))
            itm.setIcon(languages.getLanguageIcon(languageCode))
            itm.setData(Qt.ItemDataRole.UserRole, languageCode)
            if languageCode in enabledLanguages or not enabledLanguages:
                itm.setCheckState(Qt.CheckState.Checked)
            else:
                itm.setCheckState(Qt.CheckState.Unchecked)
            self.languagesList.addItem(itm)
        self.languagesList.sortItems()
        
        # DeepL settings
        self.deeplKeyEdit.setText(
            self.__plugin.getPreferences("DeeplKey"))
        # Google settings
        self.dictionaryCheckBox.setChecked(
            self.__plugin.getPreferences("GoogleEnableDictionary"))
        self.googlev2KeyEdit.setText(
            self.__plugin.getPreferences("GoogleV2Key"))
        # IBM Watson settings
        self.ibmUrlEdit.setText(
            self.__plugin.getPreferences("IbmUrl"))
        self.ibmKeyEdit.setText(
            self.__plugin.getPreferences("IbmKey"))
        # Microsoft settings
        self.msSubscriptionKeyEdit.setText(
            self.__plugin.getPreferences("MsTranslatorKey"))
        # MyMemory settings
        self.mymemoryKeyEdit.setText(
            self.__plugin.getPreferences("MyMemoryKey"))
        self.mymemoryEmailEdit.setText(
            self.__plugin.getPreferences("MyMemoryEmail"))
        # Yandex settings
        self.yandexKeyEdit.setText(
            self.__plugin.getPreferences("YandexKey"))
    
    def save(self):
        """
        Public slot to save the Pyramid configuration.
        """
        enabledLanguages = [
            itm.data(Qt.ItemDataRole.UserRole)
            for itm in self.__checkedLanguageItems()
        ]
        self.__plugin.setPreferences(
            "EnabledLanguages", enabledLanguages)
        
        # DeepL settings
        self.__plugin.setPreferences(
            "DeeplKey", self.deeplKeyEdit.text())
        # Google settings
        self.__plugin.setPreferences(
            "GoogleEnableDictionary", self.dictionaryCheckBox.isChecked())
        self.__plugin.setPreferences(
            "GoogleV2Key", self.googlev2KeyEdit.text())
        # IBM Watson settings
        self.__plugin.setPreferences(
            "IbmUrl", self.ibmUrlEdit.text())
        self.__plugin.setPreferences(
            "IbmKey", self.ibmKeyEdit.text())
        # Microsoft settings
        self.__plugin.setPreferences(
            "MsTranslatorKey", self.msSubscriptionKeyEdit.text())
        # MyMemory settings
        self.__plugin.setPreferences(
            "MyMemoryKey", self.mymemoryKeyEdit.text())
        # Yandex settings
        self.__plugin.setPreferences(
            "YandexKey", self.yandexKeyEdit.text())
    
    def __checkedLanguageItems(self):
        """
        Private method to get a list of checked language items.
        
        @return list of checked language items (list of QListWidgetItem)
        """
        items = []
        for index in range(self.languagesList.count()):
            itm = self.languagesList.item(index)
            if itm.checkState() == Qt.CheckState.Checked:
                items.append(itm)
        
        return items
    
    @pyqtSlot()
    def on_setButton_clicked(self):
        """
        Private slot to set or unset all items.
        """
        self.__enableLanguageWarning = False
        
        unset = len(self.__checkedLanguageItems()) > 0
        for index in range(self.languagesList.count()):
            itm = self.languagesList.item(index)
            if unset:
                itm.setCheckState(Qt.CheckState.Unchecked)
            else:
                itm.setCheckState(Qt.CheckState.Checked)
        
        self.__enableLanguageWarning = True
    
    @pyqtSlot()
    def on_defaultButton_clicked(self):
        """
        Private slot to set the default languages.
        """
        self.__enableLanguageWarning = False
        
        defaults = self.__plugin.getPreferencesDefault("EnabledLanguages")
        for index in range(self.languagesList.count()):
            itm = self.languagesList.item(index)
            if itm.data(Qt.ItemDataRole.UserRole) in defaults:
                itm.setCheckState(Qt.CheckState.Checked)
            else:
                itm.setCheckState(Qt.CheckState.Unchecked)
        
        self.__enableLanguageWarning = True
    
    @pyqtSlot(QListWidgetItem)
    def on_languagesList_itemChanged(self, item):
        """
        Private slot to handle the selection of an item.
        
        @param item reference to the changed item (QListWidgetItem)
        """
        if (
            self.__enableLanguageWarning and
            len(self.__checkedLanguageItems()) < 2
        ):
            E5MessageBox.warning(
                self,
                self.tr("Enabled Languages"),
                self.tr("""At least two languages should be selected to"""
                        """ work correctly."""))
