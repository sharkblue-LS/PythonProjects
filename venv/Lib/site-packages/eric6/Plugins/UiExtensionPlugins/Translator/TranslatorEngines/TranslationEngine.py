# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the translation engine base class.
"""

from PyQt5.QtCore import pyqtSignal, QObject


class TranslationEngine(QObject):
    """
    Class implementing the translation engine base class containing
    default methods.
    
    @signal availableTranslationsLoaded() emitted to indicate the availability
        of the list of supported translation languages
    """
    availableTranslationsLoaded = pyqtSignal()
    
    def __init__(self, plugin, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param parent reference to the parent object (QObject)
        """
        super(TranslationEngine, self).__init__(parent)
        
        self.plugin = plugin
    
    def engineName(self):
        """
        Public method to get the name of the engine.
        
        @return engine name (string)
        """
        return ""
    
    def supportedLanguages(self):
        """
        Public method to get the supported languages.
        
        @return list of supported language codes (list of string)
        """
        return []
    
    def supportedTargetLanguages(self, original):
        """
        Public method to get a list of supported target languages for an
        original language.
        
        Note: The default implementation return the list of supported languages
        (i.e. the same as those for the source) with the given original
        removed.
        
        @param original original language
        @type str
        @return list of supported target languages for the given original
        @rtype list of str
        """
        targetLanguages = self.supportedLanguages()[:]
        try:
            targetLanguages.remove(original)
        except ValueError:
            # original is not in the list of target languages
            pass
        
        return targetLanguages
    
    def hasTTS(self):
        """
        Public method indicating the Text-to-Speech capability.
        
        @return flag indicating the Text-to-Speech capability (boolean)
        """
        return False
    
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
        return self.tr("No pronounce data available"), False
    
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
        return self.tr("No translation available"), False
