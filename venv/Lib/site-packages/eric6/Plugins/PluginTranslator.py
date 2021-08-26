# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Translator plugin.
"""

import os

from PyQt5.QtCore import pyqtSignal, QObject, QCoreApplication, QDateTime, Qt

from E5Gui.E5Application import e5App

import Preferences

from UiExtensionPlugins.Translator.Translator import Translator

import UI.Info

# Start-Of-Header
name = "Translator Plugin"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = UI.Info.VersionOnly
className = "TranslatorPlugin"
packageName = "__core__"
shortDescription = "Translation utility using various translators."
longDescription = (
    """This plug-in implements a utility to translate text using"""
    """ various online translation services."""
)
needsRestart = False
pyqtApi = 2
# End-Of-Header

error = ""

translatorPluginObject = None
    

def createTranslatorPage(configDlg):
    """
    Module function to create the Translator configuration page.
    
    @param configDlg reference to the configuration dialog
    @return reference to the configuration page
    """
    from UiExtensionPlugins.Translator.ConfigurationPage import TranslatorPage
    page = TranslatorPage.TranslatorPage(translatorPluginObject)
    return page
    

def getConfigData():
    """
    Module function returning data as required by the configuration dialog.
    
    @return dictionary containing the relevant data
    """
    if e5App().usesDarkPalette():
        icon = os.path.join("UiExtensionPlugins", "Translator", "icons",
                            "flag-dark")
    else:
        icon = os.path.join("UiExtensionPlugins", "Translator", "icons",
                            "flag-light")
    return {
        "translatorPage": [
            QCoreApplication.translate("TranslatorPlugin",
                                       "Translator"),
            icon, createTranslatorPage, None, None],
    }


def prepareUninstall():
    """
    Module function to prepare for an uninstallation.
    """
    Preferences.Prefs.settings.remove(TranslatorPlugin.PreferencesKey)


class TranslatorPlugin(QObject):
    """
    Class implementing the Translator plug-in.
    
    @signal updateLanguages() emitted to indicate a languages update
    """
    PreferencesKey = "Translator"
    
    updateLanguages = pyqtSignal()
    
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object (UI.UserInterface)
        """
        super(TranslatorPlugin, self).__init__(ui)
        self.__ui = ui
        self.__initialize()
        
        self.__defaults = {
            "OriginalLanguage": "en",
            "TranslationLanguage": "de",
            "SelectedEngine": "deepl",
            "EnabledLanguages": ["en", "de", "fr", "cs", "es", "pt",
                                 "ru", "tr", "zh-CN", "zh-TW"],
            # service specific settings below
            # DeepL
            "DeeplKey": "",
            # Google
            "GoogleEnableDictionary": False,
            "GoogleV2Key": "",
            # IBM Watson Language Translator
            "IbmUrl": "",
            "IbmKey": "",
            # Microsoft
            "MsTranslatorKey": "",
            "MsAuthToken": "",
            "MsAuthTokenExpire": QDateTime(),
            # MyMemory
            "MyMemoryKey": "",
            "MyMemoryEmail": "",
            # Yandex
            "YandexKey": "",
        }
    
    def __initialize(self):
        """
        Private slot to (re)initialize the plugin.
        """
        self.__object = None
    
    def activate(self):
        """
        Public method to activate this plugin.
        
        @return tuple of None and activation status (boolean)
        """
        global error
        error = ""     # clear previous error
        
        global translatorPluginObject
        translatorPluginObject = self
        
        self.__object = Translator(self, e5App().usesDarkPalette(), self.__ui)
        self.__object.activate()
        e5App().registerPluginObject("Translator", self.__object)
        
        return None, True
    
    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        e5App().unregisterPluginObject("Translator")
        self.__object.deactivate()
        
        self.__initialize()
    
    def getPreferencesDefault(self, key):
        """
        Public method to retrieve the various default settings.
        
        @param key the key of the value to get
        @return the requested setting
        """
        return self.__defaults[key]
    
    def getPreferences(self, key):
        """
        Public method to retrieve the various settings.
        
        @param key the key of the value to get
        @return the requested setting
        """
        if key in ["EnabledLanguages"]:
            return Preferences.toList(
                Preferences.Prefs.settings.value(
                    self.PreferencesKey + "/" + key, self.__defaults[key]))
        elif key in ["GoogleEnableDictionary"]:
            return Preferences.toBool(
                Preferences.Prefs.settings.value(
                    self.PreferencesKey + "/" + key, self.__defaults[key]))
        elif key in ["MsAuthTokenExpire"]:
            value = Preferences.Prefs.settings.value(
                self.PreferencesKey + "/" + key, self.__defaults[key])
            if isinstance(value, str):
                if value.startswith("@QDateTime"):
                    # old value, replace with default
                    value = self.__defaults[key]
                else:
                    value = QDateTime.fromString(value, Qt.DateFormat.ISODate)
            return value
        else:
            return Preferences.Prefs.settings.value(
                self.PreferencesKey + "/" + key, self.__defaults[key])
    
    def setPreferences(self, key, value):
        """
        Public method to store the various settings.
        
        @param key the key of the setting to be set (string)
        @param value the value to be set
        """
        if key in ["MsAuthTokenExpire"]:
            Preferences.Prefs.settings.setValue(
                self.PreferencesKey + "/" + key,
                value.toString(Qt.DateFormat.ISODate))
        else:
            Preferences.Prefs.settings.setValue(
                self.PreferencesKey + "/" + key, value)
        
        if key in ["EnabledLanguages"]:
            self.updateLanguages.emit()

#
# eflag: noqa = M801
