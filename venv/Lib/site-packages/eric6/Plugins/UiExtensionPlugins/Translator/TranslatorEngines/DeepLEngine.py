# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the DeepL translation engine.
"""

import json

from PyQt5.QtCore import QUrl, QByteArray, QTimer

import Utilities

from .TranslationEngine import TranslationEngine


class DeepLEngine(TranslationEngine):
    """
    Class implementing the translation engine for the DeepL
    translation service.
    """
    TranslatorUrl = "https://api.deepl.com/v1/translate"
    MaxTranslationTextLen = 30 * 1024
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object
        @type TranslatorPlugin
        @param parent reference to the parent object
        @type QObject
        """
        super(DeepLEngine, self).__init__(plugin, parent)
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name
        @rtype str
        """
        return "deepl"
    
    def supportedLanguages(self):
        """
        Public method to get the supported languages.
        
        @return list of supported language codes
        @rtype list of str
        """
        return ["de", "en", "es", "fr", "it", "nl", "pl", ]
    
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
        if len(text) > self.MaxTranslationTextLen:
            return (
                self.tr("DeepL: Text to be translated exceeds the translation"
                        " limit of {0} characters.")
                .format(self.MaxTranslationTextLen),
                False
            )
        
        apiKey = self.plugin.getPreferences("DeeplKey")
        if not apiKey:
            return self.tr("A valid DeepL Pro key is required."), False
        
        params = QByteArray(
            "auth_key={0}&source_lang={1}&target_lang={2}&text=".format(
                apiKey, originalLanguage.upper(), translationLanguage.upper())
            .encode("utf-8"))
        encodedText = (
            QByteArray(Utilities.html_encode(text).encode("utf-8"))
            .toPercentEncoding()
        )
        request = params + encodedText
        response, ok = requestObject.post(QUrl(self.TranslatorUrl), request)
        if ok:
            try:
                responseDict = json.loads(response)
            except ValueError:
                return self.tr("Invalid response received from DeepL"), False
            
            if "translations" not in responseDict:
                return self.tr("DeepL call returned an unknown result"), False
            
            translations = responseDict["translations"]
            if len(translations) == 0:
                return self.tr("<p>DeepL: No translation found</p>"), True
            
            # show sentence by sentence separated by a line
            result = (
                "<p>" +
                "<hr/>".join([t["text"] for t in translations]) +
                "</p>"
            )
        
        else:
            result = response
        return result, ok
