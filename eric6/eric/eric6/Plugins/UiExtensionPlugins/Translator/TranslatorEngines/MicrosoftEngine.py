# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Microsoft translation engine.
"""

from PyQt5.QtCore import QUrl, QDateTime, QByteArray, QTimer

from .TranslationEngine import TranslationEngine


class MicrosoftEngine(TranslationEngine):
    """
    Class implementing the translation engine for the Microsoft
    translation service.
    """
    AccessTokenUrl = (
        "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
    )
    TranslatorUrl = "https://api.microsofttranslator.com/V2/Http.svc/Translate"
    TextToSpeechUrl = "https://api.microsofttranslator.com/V2/Http.svc/Speak"
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(MicrosoftEngine, self).__init__(plugin, parent)
        
        self.__mappings = {
            "zh-CN": "zh-CHS",
            "zh-TW": "zh-CHT",
        }
        
        QTimer.singleShot(0, self.availableTranslationsLoaded.emit)
    
    def engineName(self):
        """
        Public method to return the name of the engine.
        
        @return engine name (string)
        """
        return "microsoft"
    
    def supportedLanguages(self):
        """
        Public method to get the supported languages.
        
        @return list of supported language codes (list of string)
        """
        return ["ar", "bg", "ca", "cs", "da", "de", "en",
                "es", "et", "fi", "fr", "hi", "hu", "id",
                "it", "ja", "ko", "lt", "lv", "mt",
                "nl", "no", "pl", "pt", "ro", "ru", "sk", "sl",
                "sv", "th", "tr", "uk", "vi", "zh-CN", "zh-TW",
                ]
    
    def hasTTS(self):
        """
        Public method indicating the Text-to-Speech capability.
        
        @return flag indicating the Text-to-Speech capability (boolean)
        """
        return True
    
    def __mapLanguageCode(self, code):
        """
        Private method to map a language code to the Microsoft code.
        
        @param code language code (string)
        @return mapped language code (string)
        """
        if code in self.__mappings:
            return self.__mapping[code]
        else:
            return code
    
    def __getClientDataAzure(self):
        """
        Private method to retrieve the client data.
        
        @return tuple giving the API subscription key and a flag indicating
            validity
        @rtype tuple of (str, bool)
        """
        subscriptionKey = self.plugin.getPreferences("MsTranslatorKey")
        valid = bool(subscriptionKey)
        return subscriptionKey, valid
    
    def __getAccessToken(self, requestObject):
        """
        Private slot to get an access token.
        
        If the stored token is no longer valid, get a new one and store it.
        
        @param requestObject reference to the request object
            (TranslatorRequest)
        @return access token (string)
        """
        if (
            self.plugin.getPreferences("MsAuthTokenExpire") >
            QDateTime.currentDateTime()
        ):
            return self.plugin.getPreferences("MsAuthToken")
        
        # Token expired, get a new one
        subscriptionKey, valid = self.__getClientDataAzure()
        if not valid:
            return ""
        
        subscriptionHeader = (b"Ocp-Apim-Subscription-Key",
                              subscriptionKey.encode("utf-8"))
        response, ok = requestObject.post(
            QUrl(self.AccessTokenUrl), QByteArray(b""),
            extraHeaders=[subscriptionHeader])
        if ok:
            self.plugin.setPreferences("MsAuthToken", response)
            self.plugin.setPreferences(
                "MsAuthTokenExpire",
                QDateTime.currentDateTime().addSecs(8 * 60))
            return response
        else:
            return ""
    
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
        subscriptionKey, valid = self.__getClientDataAzure()
        if not valid:
            return (self.tr("""You have not registered for the Microsoft"""
                            """ Translation service."""),
                    False)
        
        accessToken = self.__getAccessToken(requestObject)
        if not accessToken:
            return (
                self.tr("MS Translator: No valid access token available."),
                False
            )
        
        authHeader = (b"Authorization",
                      "Bearer {0}".format(accessToken).encode("utf-8"))
        params = "?appid=&from={0}&to={1}&text={2}".format(
            self.__mapLanguageCode(originalLanguage),
            self.__mapLanguageCode(translationLanguage),
            text)
        url = QUrl(self.TranslatorUrl + params)
        response, ok = requestObject.get(url, extraHeaders=[authHeader])
        if ok:
            response = str(response, "utf-8", "replace").strip()
            if (
                response.startswith("<string") and
                response.endswith("</string>")
            ):
                result = response.split(">", 1)[1].rsplit("<", 1)[0]
            else:
                result = self.tr("MS Translator: No translation available.")
                ok = False
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
        subscriptionKey, valid = self.__getClientDataAzure()
        if not valid:
            return (self.tr("""You have not registered for the Microsoft"""
                            """ Translation service."""),
                    False)
        
        accessToken = self.__getAccessToken(requestObject)
        if not accessToken:
            return (
                self.tr("MS Translator: No valid access token available."),
                False
            )
        
        params = "?language={0}&format={1}&options={2}&text={3}".format(
            self.__mapLanguageCode(language),
            "audio/wav",
            "MaxQuality",
            text)
        authHeader = (b"Authorization",
                      "Bearer {0}".format(accessToken).encode("utf-8"))
        url = QUrl(self.TextToSpeechUrl + params)
        data, ok = requestObject.get(url, extraHeaders=[authHeader])
        if not ok:
            data = self.tr("MS Translator: No Text-to-Speech for the selected"
                           " language available.")
        return data, ok
