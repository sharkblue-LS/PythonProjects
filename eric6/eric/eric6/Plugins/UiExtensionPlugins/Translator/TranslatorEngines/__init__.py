# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package containing the various translation engines.
"""

import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from E5Gui.E5Application import e5App

import UI.PixmapCache


def supportedEngineNames():
    """
    Module function to get the list of supported translation engines.
    
    @return names of supported engines (list of string)
    """
    return ["googlev1", "mymemory", "glosbe", "promt", "yandex", "googlev2",
            "microsoft", "deepl", "ibm_watson"]


def engineDisplayName(name):
    """
    Module function to get a translated name for an engine.
    
    @param name name of a translation engine (string)
    @return translated engine name (string)
    """
    if name == "googlev1":
        return QCoreApplication.translate("TranslatorEngines", "Google V.1")
    elif name == "mymemory":
        return QCoreApplication.translate("TranslatorEngines", "MyMemory")
    elif name == "glosbe":
        return QCoreApplication.translate("TranslatorEngines", "Glosbe")
    elif name == "promt":
        return QCoreApplication.translate("TranslatorEngines", "PROMT")
    elif name == "yandex":
        return QCoreApplication.translate("TranslatorEngines", "Yandex")
    elif name == "googlev2":
        return QCoreApplication.translate("TranslatorEngines", "Google V.2")
    elif name == "microsoft":
        return QCoreApplication.translate("TranslatorEngines", "Microsoft")
    elif name == "deepl":
        return QCoreApplication.translate("TranslatorEngines", "DeepL Pro")
    elif name == "ibm_watson":
        return QCoreApplication.translate("TranslatorEngines", "IBM Watson")
    else:
        return QCoreApplication.translate(
            "TranslatorEngines", "Unknow translation service name ({0})"
        ).format(name)


def getTranslationEngine(name, plugin, parent=None):
    """
    Module function to instantiate an engine object for the named service.
    
    @param name name of the online translation service (string)
    @param plugin reference to the plugin object (TranslatorPlugin)
    @param parent reference to the parent object
    @return translation engine (TranslatorEngine)
    """
    if name == "googlev1":
        from .GoogleV1Engine import GoogleV1Engine
        engine = GoogleV1Engine(plugin, parent)
    elif name == "mymemory":
        from .MyMemoryEngine import MyMemoryEngine
        engine = MyMemoryEngine(plugin, parent)
    elif name == "glosbe":
        from .GlosbeEngine import GlosbeEngine
        engine = GlosbeEngine(plugin, parent)
    elif name == "promt":
        from .PromtEngine import PromtEngine
        engine = PromtEngine(plugin, parent)
    elif name == "yandex":
        from .YandexEngine import YandexEngine
        engine = YandexEngine(plugin, parent)
    elif name == "googlev2":
        from .GoogleV2Engine import GoogleV2Engine
        engine = GoogleV2Engine(plugin, parent)
    elif name == "microsoft":
        from .MicrosoftEngine import MicrosoftEngine
        engine = MicrosoftEngine(plugin, parent)
    elif name == "deepl":
        from .DeepLEngine import DeepLEngine
        engine = DeepLEngine(plugin, parent)
    elif name == "ibm_watson":
        from .IbmWatsonEngine import IbmWatsonEngine
        engine = IbmWatsonEngine(plugin, parent)
    else:
        engine = None
    return engine


def getEngineIcon(name):
    """
    Module function to get the icon of the named engine.
    
    @param name name of the translation engine
    @type str
    @return engine icon
    @rtype QIcon
    """
    if e5App().usesDarkPalette():
        iconSuffix = "dark"
    else:
        iconSuffix = "light"
    if name in supportedEngineNames():
        icon = UI.PixmapCache.getIcon(os.path.join(
            os.path.dirname(__file__), "..", "icons", "engines",
            "{0}-{1}".format(name, iconSuffix)))
        if icon.isNull():
            # try variant without suffix
            icon = UI.PixmapCache.getIcon(os.path.join(
                os.path.dirname(__file__), "..", "icons", "engines",
                "{0}".format(name)))
        return icon
    else:
        return QIcon()


def getKeyUrl(name):
    """
    Module function to get an URL to request a user key.
    
    @param name name of the online translation service (string)
    @return key request URL (string)
    """
    if name == "mymemory":
        return "http://mymemory.translated.net/doc/keygen.php"
    elif name == "yandex":
        return "http://api.yandex.com/key/form.xml?service=trnsl"
    elif name == "googlev2":
        return "https://console.developers.google.com/"
    elif name == "microsoft":
        return "https://portal.azure.com"
    elif name == "ibm_watson":
        return "https://www.ibm.com/watson/services/language-translator/"
    elif name == "deepl":
        return "https://www.deepl.com/pro-registration.html"
    else:
        return ""
