# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Google V2 translation engine.
"""

import json

from PyQt5.QtCore import QUrl, QTimer

from .TranslationEngine import TranslationEngine


class GoogleV2Engine(TranslationEngine):
    """
    Class implementing the translation engine for the new Google
    translation service.
    """
    TranslatorUrl = "https://www.googleapis.com/language/translate/v2"
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(GoogleV2Engine, self).__init__(plugin, parent)
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name (string)
        """
        return "googlev2"
    
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
        apiKey = self.plugin.getPreferences("GoogleV2Key")
        if not apiKey:
            return self.tr("Google V2: A valid Google Translate key is"
                           " required."), False
        
        params = "?key={3}&source={0}&target={1}&q={2}".format(
            originalLanguage, translationLanguage, text, apiKey)
        url = QUrl(self.TranslatorUrl + params)
        response, ok = requestObject.get(url)
        if ok:
            response = str(response, "utf-8", "replace")
            try:
                responseDict = json.loads(response)
            except ValueError:
                return self.tr("Google V2: Invalid response received"), False
            
            if (
                "data" not in responseDict or
                "translations" not in responseDict["data"]
            ):
                return self.tr("Google V2: No translation available."), False
            
            result = ""
            translations = responseDict["data"]["translations"]
            for translation in translations:
                result += translation["translatedText"]
                if translation != translations[-1]:
                    result += "<br/>"
        else:
            result = response
        return result, ok
