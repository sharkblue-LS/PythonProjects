# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Google V1 translation engine.
"""

import json
import re

from PyQt5.QtCore import QByteArray, QUrl, QTimer

import Utilities

from .TranslationEngine import TranslationEngine


class GoogleV1Engine(TranslationEngine):
    """
    Class implementing the translation engine for the old Google
    translation service.
    """
    TranslatorUrl = "https://translate.googleapis.com/translate_a/single"
    TextToSpeechUrl = "https://translate.google.com/translate_tts"
    TextToSpeechLimit = 100
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(GoogleV1Engine, self).__init__(plugin, parent)
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name (string)
        """
        return "googlev1"
    
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
    
    def hasTTS(self):
        """
        Public method indicating the Text-to-Speech capability.
        
        @return flag indicating the Text-to-Speech capability (boolean)
        """
        return False        # doesn't work reliably
    
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
        params = QByteArray(
            "client=gtx&sl={0}&tl={1}&dt=t&dt=bd&ie=utf-8&oe=utf-8&q=".format(
                originalLanguage, translationLanguage).encode("utf-8"))
        encodedText = (
            QByteArray(Utilities.html_encode(text).encode("utf-8"))
            .toPercentEncoding()
        )
        request = params + encodedText
        response, ok = requestObject.post(QUrl(self.TranslatorUrl), request)
        if ok:
            try:
                # clean up the response
                response = re.sub(r',{2,}', ',', response)
                responseDict = json.loads(response)
            except ValueError:
                return self.tr("Google V1: Invalid response received"), False
            
            if isinstance(responseDict, dict):
                sentences = responseDict["sentences"]
                result = ""
                for sentence in sentences:
                    result += sentence["trans"].replace("\n", "<br/>")
                
                if (
                    self.plugin.getPreferences("GoogleEnableDictionary") and
                    "dict" in responseDict
                ):
                    dictionary = responseDict["dict"]
                    for value in dictionary:
                        result += "<hr/><u><b>{0}</b> - {1}</u><br/>".format(
                            text, value["pos"])
                        for entry in value["entry"]:
                            if "previous_word" in entry:
                                previous = entry["previous_word"] + " "
                            else:
                                previous = ""
                            word = entry["word"]
                            reverse = entry["reverse_translation"]
                            result += "<br/>{0}<b>{1}</b> - {2}".format(
                                previous, word, ", ".join(reverse))
                        if value != dictionary[-1]:
                            result += "<br/>"
            elif isinstance(responseDict, list):
                sentences = responseDict[0]
                result = (
                    "".join([s[0] for s in sentences]).replace("\n", "<br/>")
                )
                if (
                    self.plugin.getPreferences("GoogleEnableDictionary") and
                    len(responseDict) > 2
                ):
                    if not responseDict[1]:
                        result = self.tr("Google V1: No translation found.")
                        ok = False
                    else:
                        for wordTypeList in responseDict[1]:
                            result += "<hr/><u><b>{0}</b> - {1}</u>".format(
                                wordTypeList[0], wordTypeList[-2])
                            for wordsList in wordTypeList[2]:
                                reverse = wordsList[0]
                                words = wordsList[1]
                                result += "<br/><b>{0}</b> - {1}".format(
                                    reverse, ", ".join(words))
            else:
                result = responseDict
        else:
            result = response
        return result, ok
    
    def getTextToSpeechData(self, requestObject, text, language):
        """
        Public method to pronounce the given text.
        
        @param requestObject reference to the request object
            (TranslatorRequest)
        @param text text to be pronounced (string)
        @param language language code of the text (string)
        @return tuple with pronounce data (QByteArray) or error string (string)
            and success flag (boolean)
        """
        text = text.split("\n\n", 1)[0]
        if len(text) > self.TextToSpeechLimit:
            return (self.tr("Google V1: Only texts up to {0} characters are"
                            " allowed.")
                    .format(self.TextToSpeechLimit), False)
        
        url = QUrl(self.TextToSpeechUrl +
                   "?client=tw-ob&ie=utf-8&tl={0}&q={1}".format(
                       language, text))
        return requestObject.get(url)
