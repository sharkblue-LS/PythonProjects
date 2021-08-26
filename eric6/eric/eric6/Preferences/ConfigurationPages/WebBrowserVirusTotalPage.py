# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing VirusTotal configuration page (web browser variant).
"""

from PyQt5.QtCore import pyqtSlot

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_WebBrowserVirusTotalPage import Ui_WebBrowserVirusTotalPage

import Preferences


class WebBrowserVirusTotalPage(ConfigurationPageBase,
                               Ui_WebBrowserVirusTotalPage):
    """
    Class implementing VirusTotal configuration page (web browser variant).
    """
    def __init__(self):
        """
        Constructor
        """
        super(WebBrowserVirusTotalPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("HelpVirusTotalPage")
        
        self.testResultLabel.setHidden(True)
        
        from WebBrowser.VirusTotal.VirusTotalApi import VirusTotalAPI
        self.__vt = VirusTotalAPI(self)
        self.__vt.checkServiceKeyFinished.connect(
            self.__checkServiceKeyFinished)
        
        # set initial values
        self.vtEnabledCheckBox.setChecked(
            Preferences.getWebBrowser("VirusTotalEnabled"))
        self.vtSecureCheckBox.setChecked(
            Preferences.getWebBrowser("VirusTotalSecure"))
        self.vtServiceKeyEdit.setText(
            Preferences.getWebBrowser("VirusTotalServiceKey"))
    
    def save(self):
        """
        Public slot to save the VirusTotal configuration.
        """
        Preferences.setWebBrowser(
            "VirusTotalEnabled",
            self.vtEnabledCheckBox.isChecked())
        Preferences.setWebBrowser(
            "VirusTotalSecure",
            self.vtSecureCheckBox.isChecked())
        Preferences.setWebBrowser(
            "VirusTotalServiceKey",
            self.vtServiceKeyEdit.text())
    
    @pyqtSlot(str)
    def on_vtServiceKeyEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the service key.
        
        @param txt entered service key (string)
        """
        self.testButton.setEnabled(txt != "")
    
    @pyqtSlot()
    def on_testButton_clicked(self):
        """
        Private slot to test the entered service key.
        """
        self.testResultLabel.setHidden(False)
        self.testResultLabel.setText(
            self.tr("Checking validity of the service key..."))
        if self.vtSecureCheckBox.isChecked():
            protocol = "https"
        else:
            protocol = "http"
        self.__vt.checkServiceKeyValidity(
            self.vtServiceKeyEdit.text(), protocol)
    
    @pyqtSlot(bool, str)
    def __checkServiceKeyFinished(self, result, msg):
        """
        Private slot to receive the result of the service key check.
        
        @param result flag indicating a successful check (boolean)
        @param msg network error message (str)
        """
        if result:
            self.testResultLabel.setText(
                self.tr("The service key is valid."))
        else:
            if msg == "":
                self.testResultLabel.setText(self.tr(
                    '<font color="#FF0000">The service key is'
                    ' not valid.</font>'))
            else:
                self.testResultLabel.setText(self.tr(
                    '<font color="#FF0000"><b>Error:</b> {0}</font>')
                    .format(msg))
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = WebBrowserVirusTotalPage()
    return page
