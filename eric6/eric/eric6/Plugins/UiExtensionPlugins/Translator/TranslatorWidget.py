# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the translator widget.
"""

from PyQt5.QtCore import pyqtSlot, QTemporaryFile
from PyQt5.QtWidgets import QWidget
try:
    from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
    MULTIMEDIA_AVAILABLE = True
except ImportError:
    MULTIMEDIA_AVAILABLE = False

from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App

from .Ui_TranslatorWidget import Ui_TranslatorWidget

from .TranslatorLanguagesDb import TranslatorLanguagesDb
from . import TranslatorEngines

import UI.PixmapCache


class TranslatorWidget(QWidget, Ui_TranslatorWidget):
    """
    Class implementing the translator widget.
    """
    def __init__(self, plugin, translator, parent=None):
        """
        Constructor
        
        @param plugin reference to the plugin object (TranslatorPlugin)
        @param translator reference to the translator object (Translator)
        @param parent reference to the parent widget (QWidget)
        """
        super(TranslatorWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.__plugin = plugin
        self.__translator = translator
        
        self.__languages = TranslatorLanguagesDb(self)
        
        self.__translatorRequest = None
        self.__translationEngine = None
        
        self.__mediaPlayer = None
        self.__mediaFile = None
        
        audioAvailable = (MULTIMEDIA_AVAILABLE and
                          bool(QMediaPlayer.hasSupport("audio/mpeg")))
        self.pronounceOrigButton.setVisible(audioAvailable)
        self.pronounceTransButton.setVisible(audioAvailable)
        
        self.pronounceOrigButton.setIcon(
            self.__translator.getAppIcon("pronounce"))
        self.pronounceTransButton.setIcon(
            self.__translator.getAppIcon("pronounce"))
        self.swapButton.setIcon(
            self.__translator.getAppIcon("swap"))
        self.translateButton.setIcon(
            self.__translator.getAppIcon("translate"))
        self.clearButton.setIcon(UI.PixmapCache.getIcon("editDelete"))
        self.preferencesButton.setIcon(UI.PixmapCache.getIcon("configure"))
        
        self.translateButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.pronounceOrigButton.setEnabled(False)
        self.pronounceTransButton.setEnabled(False)
        
        selectedEngine = self.__plugin.getPreferences("SelectedEngine")
        
        self.__updateEngines()
        engineIndex = self.engineComboBox.findData(selectedEngine)
        self.engineComboBox.setCurrentIndex(engineIndex)
        self.__engineComboBoxCurrentIndexChanged(engineIndex)
        
        self.engineComboBox.currentIndexChanged.connect(
            self.__engineComboBoxCurrentIndexChanged)
        self.__plugin.updateLanguages.connect(self.__updateLanguages)
    
    def __updateLanguages(self):
        """
        Private slot to update the language combo boxes.
        """
        self.__ensureTranslationEngineReady()
        if self.__translationEngine is not None:
            supportedCodes = self.__translationEngine.supportedLanguages()
            enabledCodes = self.__plugin.getPreferences("EnabledLanguages")
            
            # 1. save current selections
            origLanguage = self.origLanguageComboBox.itemData(
                self.origLanguageComboBox.currentIndex())
            
            # 2. reload the original language combo box
            self.origLanguageComboBox.blockSignals(True)
            self.origLanguageComboBox.clear()
            for code in enabledCodes:
                if code in supportedCodes:
                    language = self.__languages.getLanguage(code)
                    if language:
                        icon = self.__languages.getLanguageIcon(code)
                        self.origLanguageComboBox.addItem(
                            icon, language, code)
            self.origLanguageComboBox.model().sort(0)
            origIndex = self.origLanguageComboBox.findData(origLanguage)
            if origIndex == -1:
                origIndex = 0
            self.origLanguageComboBox.blockSignals(False)
            self.origLanguageComboBox.setCurrentIndex(origIndex)
    
    def __updateEngines(self):
        """
        Private slot to update the engines combo box.
        """
        currentEngine = self.engineComboBox.itemData(
            self.engineComboBox.currentIndex())
        self.engineComboBox.clear()
        for engineName in TranslatorEngines.supportedEngineNames():
            icon = TranslatorEngines.getEngineIcon(engineName)
            self.engineComboBox.addItem(
                icon,
                TranslatorEngines.engineDisplayName(engineName),
                engineName)
        self.engineComboBox.model().sort(0)
        self.engineComboBox.setCurrentIndex(
            self.engineComboBox.findData(currentEngine))
    
    def __originalLanguage(self):
        """
        Private method to return the code of the selected original language.
        
        @return code of the original language (string)
        """
        return self.origLanguageComboBox.itemData(
            self.origLanguageComboBox.currentIndex())
    
    def __translationLanguage(self):
        """
        Private method to return the code of the selected translation language.
        
        @return code of the translation language (string)
        """
        return self.transLanguageComboBox.itemData(
            self.transLanguageComboBox.currentIndex())
    
    @pyqtSlot()
    def on_translateButton_clicked(self):
        """
        Private slot to translate the entered text.
        """
        self.transEdit.clear()
        result, ok = self.__translate(
            self.origEdit.toPlainText(),
            self.__originalLanguage(),
            self.__translationLanguage())
        if ok:
            self.transEdit.setHtml(result)
        else:
            E5MessageBox.critical(
                self,
                self.tr("Translation Error"),
                result)
    
    @pyqtSlot()
    def on_pronounceOrigButton_clicked(self):
        """
        Private slot to pronounce the original text.
        """
        self.__pronounce(
            self.origEdit.toPlainText(), self.__originalLanguage())
    
    @pyqtSlot()
    def on_pronounceTransButton_clicked(self):
        """
        Private slot to pronounce the translated text.
        """
        self.__pronounce(
            self.transEdit.toPlainText(), self.__translationLanguage())
    
    @pyqtSlot()
    def on_swapButton_clicked(self):
        """
        Private slot to swap the languages.
        """
        # save selected language codes
        oLanguage = self.origLanguageComboBox.itemData(
            self.origLanguageComboBox.currentIndex())
        
        tLanguage = self.transLanguageComboBox.itemData(
            self.transLanguageComboBox.currentIndex())
        
        oIdx = self.origLanguageComboBox.findData(tLanguage)
        if oIdx < 0:
            oIdx = 0
        self.origLanguageComboBox.setCurrentIndex(oIdx)
        
        tIdx = self.transLanguageComboBox.findData(oLanguage)
        if tIdx < 0:
            tIdx = 0
        self.transLanguageComboBox.setCurrentIndex(tIdx)
        
        origText = self.origEdit.toPlainText()
        self.origEdit.setPlainText(self.transEdit.toPlainText())
        self.transEdit.setPlainText(origText)
    
    @pyqtSlot()
    def on_clearButton_clicked(self):
        """
        Private slot to clear the text fields.
        """
        self.origEdit.clear()
        self.transEdit.clear()
    
    @pyqtSlot()
    def on_origEdit_textChanged(self):
        """
        Private slot to handle changes of the original text.
        """
        self.__updatePronounceButtons()
        self.__updateClearButton()
        self.__updateTranslateButton()
    
    @pyqtSlot()
    def on_transEdit_textChanged(self):
        """
        Private slot to handle changes of the translation text.
        """
        self.__updatePronounceButtons()
        self.__updateClearButton()
    
    @pyqtSlot(int)
    def on_origLanguageComboBox_currentIndexChanged(self, index):
        """
        Private slot to handle the selection of the original language.
        
        @param index current index (integer)
        """
        self.__plugin.setPreferences(
            "OriginalLanguage", self.origLanguageComboBox.itemData(index))
        
        supportedTargetCodes = (
            self.__translationEngine.supportedTargetLanguages(
                self.origLanguageComboBox.itemData(index)
            )
        )
        if supportedTargetCodes is not None:
            enabledCodes = self.__plugin.getPreferences("EnabledLanguages")
            transLanguage = self.transLanguageComboBox.itemData(
                self.transLanguageComboBox.currentIndex())
            self.transLanguageComboBox.clear()
            if len(supportedTargetCodes) > 0:
                for code in enabledCodes:
                    if code in supportedTargetCodes:
                        language = self.__languages.getLanguage(code)
                        if language:
                            icon = self.__languages.getLanguageIcon(code)
                            self.transLanguageComboBox.addItem(
                                icon, language, code)
                self.transLanguageComboBox.model().sort(0)
                index = self.transLanguageComboBox.findData(transLanguage)
                if index == -1:
                    index = 0
                self.transLanguageComboBox.setCurrentIndex(index)
        
        self.__updateTranslateButton()
    
    @pyqtSlot(int)
    def on_transLanguageComboBox_currentIndexChanged(self, index):
        """
        Private slot to handle the selection of the translation language.
        
        @param index current index (integer)
        """
        self.__plugin.setPreferences(
            "TranslationLanguage", self.transLanguageComboBox.itemData(index))
    
    @pyqtSlot()
    def __availableTranslationsLoaded(self):
        """
        Private slot to handle the availability of translations.
        """
        origLanguage = self.__plugin.getPreferences("OriginalLanguage")
        transLanguage = self.__plugin.getPreferences("TranslationLanguage")
        
        self.__updateLanguages()
        
        origIndex = self.origLanguageComboBox.findData(origLanguage)
        self.origLanguageComboBox.setCurrentIndex(origIndex)
        self.on_origLanguageComboBox_currentIndexChanged(origIndex)
        self.transLanguageComboBox.setCurrentIndex(
            self.transLanguageComboBox.findData(transLanguage))
    
    def __ensureTranslationEngineReady(self):
        """
        Private slot to ensure, that the currently selected translation engine
        is ready.
        """
        engineName = self.engineComboBox.itemData(
            self.engineComboBox.currentIndex())
        if (
            self.__translationEngine is not None and
            self.__translationEngine.engineName() != engineName
        ):
            self.__translationEngine.availableTranslationsLoaded.disconnect(
                self.__availableTranslationsLoaded)
            self.__translationEngine.deleteLater()
            self.__translationEngine = None
        
        if self.__translationEngine is None:
            self.__translationEngine = TranslatorEngines.getTranslationEngine(
                engineName, self.__plugin, self)
            if self.__translationEngine is not None:
                self.__translationEngine.availableTranslationsLoaded.connect(
                    self.__availableTranslationsLoaded)
    
    @pyqtSlot(int)
    def __engineComboBoxCurrentIndexChanged(self, index):
        """
        Private slot to handle the selection of a translation service.
        
        @param index current index
        @type int
        """
        self.__ensureTranslationEngineReady()
        if self.__translationEngine is not None:
            self.__updateTranslateButton()
            self.__updatePronounceButtons()
            
            self.__plugin.setPreferences(
                "SelectedEngine", self.engineComboBox.itemData(index))
    
    def __updatePronounceButtons(self):
        """
        Private slot to set the state of the pronounce buttons.
        """
        if self.__translationEngine is not None:
            hasTTS = self.__translationEngine.hasTTS()
        else:
            hasTTS = False
        self.pronounceOrigButton.setEnabled(
            hasTTS and bool(self.origEdit.toPlainText()))
        self.pronounceTransButton.setEnabled(
            hasTTS and bool(self.transEdit.toPlainText()))
    
    def __updateClearButton(self):
        """
        Private slot to set the state of the clear button.
        """
        enable = (
            bool(self.origEdit.toPlainText()) or
            bool(self.transEdit.toPlainText())
        )
        self.clearButton.setEnabled(enable)
    
    def __updateTranslateButton(self):
        """
        Private slot to set the state of the translate button.
        """
        enable = bool(self.origEdit.toPlainText())
        enable &= bool(self.__translationLanguage())
        enable &= bool(self.__originalLanguage())
        self.translateButton.setEnabled(enable)
    
    def __translate(self, text, originalLanguage, translationLanguage):
        """
        Private method to translate the given text.
        
        @param text text to be translated (string)
        @param originalLanguage language code of the original (string)
        @param translationLanguage language code of the translation (string)
        @return tuple of translated text (string) and flag indicating
            success (boolean)
        """
        if self.__translatorRequest is None:
            from .TranslatorRequest import TranslatorRequest
            self.__translatorRequest = TranslatorRequest(self)
        
        self.__ensureTranslationEngineReady()
        if self.__translationEngine is None:
            return "", False
        else:
            result, ok = self.__translationEngine.getTranslation(
                self.__translatorRequest, text, originalLanguage,
                translationLanguage)
            
            return result, ok
    
    def __pronounce(self, text, language):
        """
        Private method to pronounce the given text.
        
        @param text text to be pronounced (string)
        @param language language code of the text (string)
        """
        if not text or not language:
            return
        
        if self.__translatorRequest is None:
            from .TranslatorRequest import TranslatorRequest
            self.__translatorRequest = TranslatorRequest(self)
        
        if self.__mediaPlayer is None:
            self.__mediaPlayer = QMediaPlayer(self)
            self.__mediaPlayer.stateChanged.connect(
                self.__mediaPlayerStateChanged)
        
        if self.__mediaPlayer.state() == QMediaPlayer.State.PlayingState:
            return
        
        self.__ensureTranslationEngineReady()
        if self.__translationEngine is not None:
            if not self.__translationEngine.hasTTS():
                E5MessageBox.critical(
                    self,
                    self.tr("Translation Error"),
                    self.tr("The selected translation service does not"
                            " support the Text-to-Speech function."))
                return
            
            data, ok = self.__translationEngine.getTextToSpeechData(
                self.__translatorRequest, text, language)
            if ok:
                self.__mediaFile = QTemporaryFile(self)
                self.__mediaFile.open()
                self.__mediaFile.setAutoRemove(False)
                self.__mediaFile.write(data)
                
                self.__mediaPlayer.setMedia(QMediaContent(), self.__mediaFile)
                self.__mediaPlayer.play()
            else:
                E5MessageBox.critical(
                    self,
                    self.tr("Translation Error"),
                    data)
    
    def __mediaPlayerStateChanged(self, state):
        """
        Private slot handling changes of the media player state.
        
        @param state media player state (QAudio.State)
        """
        if state == QMediaPlayer.State.StoppedState:
            self.__mediaFile.close()
            self.__mediaFile.remove()
            self.__mediaFile = None
    
    @pyqtSlot()
    def on_preferencesButton_clicked(self):
        """
        Private slot to open the Translator configuration page.
        """
        e5App().getObject("UserInterface").showPreferences("translatorPage")
