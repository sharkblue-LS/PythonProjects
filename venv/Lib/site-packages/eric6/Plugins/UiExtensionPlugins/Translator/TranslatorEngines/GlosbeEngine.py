# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Glosbe translation engine.
"""

import json

from PyQt5.QtCore import QUrl, QTimer

from .TranslationEngine import TranslationEngine


class GlosbeEngine(TranslationEngine):
    """
    Class implementing the translation engine for the Glosbe
    translation service.
    """
    TranslatorUrl = "https://glosbe.com/gapi/translate"
    TranslatorLimit = 500
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(GlosbeEngine, self).__init__(plugin, parent)
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name (string)
        """
        return "glosbe"
    
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
        from ..TranslatorLanguagesDb import TranslatorLanguagesDb
        languages = TranslatorLanguagesDb(self)
        
        params = "?from={0}&dest={1}&format=json&phrase={2}".format(
            languages.convertTwoToThree(originalLanguage),
            languages.convertTwoToThree(translationLanguage),
            text)
        url = QUrl(self.TranslatorUrl + params)
        response, ok = requestObject.get(url)
        if ok:
            response = str(response, "utf-8", "replace")
            try:
                responseDict = json.loads(response)
            except ValueError:
                return self.tr("Glosbe: Invalid response received"), False
            
            result = ""
            for translation in responseDict["tuc"]:
                if "phrase" in translation:
                    result += "<b>{0}</b>".format(
                        translation["phrase"]["text"])
                    if "meanings" in translation:
                        for meaning in translation["meanings"]:
                            result += "<br/><i>({0})</i>".format(
                                meaning["text"])
                    if translation != responseDict["tuc"][-1]:
                        result += "<hr/>"
            if not result:
                result = self.tr("Glosbe: No translation found.")
                ok = False
        else:
            result = response
        return result, ok
