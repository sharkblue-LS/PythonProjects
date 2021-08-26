# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the MyMemory translation engine.
"""

import json

from PyQt5.QtCore import QUrl, QTimer

from .TranslationEngine import TranslationEngine


class MyMemoryEngine(TranslationEngine):
    """
    Class implementing the translation engine for the MyMemory
    translation service.
    """
    TranslatorUrl = "http://api.mymemory.translated.net/get"
    TranslatorLimit = 500
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(MyMemoryEngine, self).__init__(plugin, parent)
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name (string)
        """
        return "mymemory"
    
    def supportedLanguages(self):
        """
        Public method to get the supported languages.
        
        @return list of supported language codes (list of string)
        """
        return ["ar", "be", "bg", "bs", "ca", "cs", "da", "de", "el", "en",
                "es", "et", "fi", "fr", "ga", "gl", "hi", "hr", "hu", "id",
                "is", "it", "iw", "ja", "ka", "ko", "lt", "lv", "mk", "mt",
                "nl", "no", "pl", "pt", "ro", "ru", "sk", "sl", "sq", "sr",
                "sv", "th", "tl", "tr", "uk", "vi", "zh-CN", "zh-TW",
                ]
    
    def getTranslation(self, requestObject, text, originalLanguage,
                       translationLanguage):
        """
        Public method to translate the given text.
        
        @param requestObject reference to the request object
            (TranslatorRequest)
        @param text text to be translated (string)
        @param originalLanguage language code of the original (string)
        @param translationLanguage language code of the translation (string)
        @return tuple of translated text (string) and flag indicating
            success (boolean)
        """
        if len(text) > self.TranslatorLimit:
            return (
                self.tr("MyMemory: Only texts up to {0} characters are"
                        " allowed.")
                .format(self.TranslatorLimit),
                False
            )
        
        myMemoryKey = self.plugin.getPreferences("MyMemoryKey")
        if myMemoryKey:
            keyParam = "&key={0}".format(myMemoryKey)
        else:
            keyParam = ""
        myMemoryEmail = self.plugin.getPreferences("MyMemoryEmail")
        if myMemoryEmail:
            emailParam = "&de={0}".format(myMemoryEmail)
        else:
            emailParam = ""
        params = "?of=json{3}{4}&langpair={0}|{1}&q={2}".format(
            originalLanguage, translationLanguage, text,
            keyParam, emailParam)
        url = QUrl(self.TranslatorUrl + params)
        response, ok = requestObject.get(url)
        if ok:
            response = str(response, "utf-8", "replace")
            try:
                responseDict = json.loads(response)
            except ValueError:
                return self.tr("MyMemory: Invalid response received"), False
            result = responseDict["responseData"]["translatedText"]
        else:
            result = response
        return result, ok
