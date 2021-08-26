# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Promt translation engine.
"""

import json

from PyQt5.QtCore import QUrl, QByteArray, QTimer

import Utilities

from .TranslationEngine import TranslationEngine


class PromtEngine(TranslationEngine):
    """
    Class implementing the translation engine for the Promt
    translation service.
    """
    TranslatorUrl = (
        "http://www.online-translator.com/services/"
        "TranslationService.asmx/GetTranslation"
    )
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(PromtEngine, self).__init__(plugin, parent)
        
        self.__mapping = {
            "de": "g",
            "en": "e",
            "es": "s",
            "fr": "f",
            "it": "i",
            "ja": "j",
            "pt": "p",
            "ru": "r",
        }
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name (string)
        """
        return "promt"
    
    def supportedLanguages(self):
        """
        Public method to get the supported languages.
        
        @return list of supported language codes (list of string)
        """
        return ["de", "en", "es", "fr", "it", "ja", "pt", "ru", ]
    
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
        encodedText = str(
            QUrl.toPercentEncoding(Utilities.html_encode(text + ".")),
            "utf-8")
        request = QByteArray(
            "{{dirCode:'{0}{1}', template:'General', text:'{2}', lang:'de',"
            " limit:3000, useAutoDetect:true, key:'', ts:'MainSite', tid:''}}"
            .format(self.__mapping[originalLanguage],
                    self.__mapping[translationLanguage],
                    encodedText).encode("utf-8")
        )
        response, ok = requestObject.post(QUrl(self.TranslatorUrl), request,
                                          "json")
        if ok:
            try:
                responseDict = json.loads(response)
            except ValueError:
                return self.tr("Promt: Invalid response received"), False
            
            if "d" in responseDict:
                responseDict = responseDict["d"]
            
            result = responseDict["result"][:-1]    # get rid of stub
            
            if responseDict["errCode"] == 0:
                if responseDict["ptsDirCode"] == "":
                    result = self.tr(
                        "Promt: This direction of translation is not"
                        " available.")
                    ok = False
            else:
                result = responseDict["errMessage"]
                ok = False
        else:
            result = response
        return result, ok
