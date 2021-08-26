# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Email configuration page.
"""

import smtplib
import socket
import sys

from PyQt5.QtCore import pyqtSlot

from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App
from E5Gui.E5OverrideCursor import E5OverrideCursor

from E5Network.E5GoogleMailHelpers import getInstallCommand, RequiredPackages

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_EmailPage import Ui_EmailPage

import Preferences


class EmailPage(ConfigurationPageBase, Ui_EmailPage):
    """
    Class implementing the Email configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(EmailPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("EmailPage")
        
        self.__helpDialog = None
        
        pipPackages = [
            "google-api-python-client",
            "google-auth-oauthlib",
        ]
        self.__pipCommand = "pip install --upgrade {0}".format(
            " ".join(pipPackages))
        
        # set initial values
        self.__checkGoogleMail()
        
        self.mailServerEdit.setText(Preferences.getUser("MailServer"))
        self.portSpin.setValue(Preferences.getUser("MailServerPort"))
        self.emailEdit.setText(Preferences.getUser("Email"))
        self.signatureEdit.setPlainText(Preferences.getUser("Signature"))
        self.mailAuthenticationGroup.setChecked(
            Preferences.getUser("MailServerAuthentication"))
        self.mailUserEdit.setText(Preferences.getUser("MailServerUser"))
        self.mailPasswordEdit.setText(
            Preferences.getUser("MailServerPassword"))
        encryption = Preferences.getUser("MailServerEncryption")
        if encryption == "TLS":
            self.useTlsButton.setChecked(True)
        elif encryption == "SSL":
            self.useSslButton.setChecked(True)
        else:
            self.noEncryptionButton.setChecked(True)
    
    def save(self):
        """
        Public slot to save the Email configuration.
        """
        Preferences.setUser(
            "UseGoogleMailOAuth2",
            self.googleMailCheckBox.isChecked())
        Preferences.setUser(
            "MailServer",
            self.mailServerEdit.text())
        Preferences.setUser(
            "MailServerPort",
            self.portSpin.value())
        Preferences.setUser(
            "Email",
            self.emailEdit.text())
        Preferences.setUser(
            "Signature",
            self.signatureEdit.toPlainText())
        Preferences.setUser(
            "MailServerAuthentication",
            self.mailAuthenticationGroup.isChecked())
        Preferences.setUser(
            "MailServerUser",
            self.mailUserEdit.text())
        Preferences.setUser(
            "MailServerPassword",
            self.mailPasswordEdit.text())
        if self.useTlsButton.isChecked():
            encryption = "TLS"
        elif self.useSslButton.isChecked():
            encryption = "SSL"
        else:
            encryption = "No"
        Preferences.setUser("MailServerEncryption", encryption)
    
    def __updatePortSpin(self):
        """
        Private slot to set the value of the port spin box depending upon
        the selected encryption method.
        """
        if self.useSslButton.isChecked():
            self.portSpin.setValue(465)
        elif self.useTlsButton.isChecked():
            self.portSpin.setValue(587)
        else:
            self.portSpin.setValue(25)
    
    @pyqtSlot(bool)
    def on_noEncryptionButton_toggled(self, checked):
        """
        Private slot handling a change of no encryption button.
        
        @param checked current state of the button
        @type bool
        """
        self.__updatePortSpin()
    
    @pyqtSlot(bool)
    def on_useSslButton_toggled(self, checked):
        """
        Private slot handling a change of SSL encryption button.
        
        @param checked current state of the button
        @type bool
        """
        self.__updatePortSpin()
    
    @pyqtSlot(bool)
    def on_useTlsButton_toggled(self, checked):
        """
        Private slot handling a change of TLS encryption button.
        
        @param checked current state of the button
        @type bool
        """
        self.__updatePortSpin()
    
    def __updateTestButton(self):
        """
        Private slot to update the enabled state of the test button.
        """
        self.testButton.setEnabled(
            self.mailAuthenticationGroup.isChecked() and
            self.mailUserEdit.text() != "" and
            self.mailPasswordEdit.text() != "" and
            self.mailServerEdit.text() != ""
        )
    
    @pyqtSlot(str)
    def on_mailServerEdit_textChanged(self, txt):
        """
        Private slot to handle a change of the text of the mail server edit.
        
        @param txt current text of the edit (string)
        @type str
        """
        self.__updateTestButton()
    
    @pyqtSlot(bool)
    def on_mailAuthenticationGroup_toggled(self, checked):
        """
        Private slot to handle a change of the state of the authentication
        group.
        
        @param checked state of the group (boolean)
        """
        self.__updateTestButton()
    
    @pyqtSlot(str)
    def on_mailUserEdit_textChanged(self, txt):
        """
        Private slot to handle a change of the text of the user edit.
        
        @param txt current text of the edit (string)
        """
        self.__updateTestButton()
    
    @pyqtSlot(str)
    def on_mailPasswordEdit_textChanged(self, txt):
        """
        Private slot to handle a change of the text of the user edit.
        
        @param txt current text of the edit (string)
        """
        self.__updateTestButton()
    
    @pyqtSlot()
    def on_testButton_clicked(self):
        """
        Private slot to test the mail server login data.
        """
        try:
            with E5OverrideCursor():
                if self.useSslButton.isChecked():
                    server = smtplib.SMTP_SSL(self.mailServerEdit.text(),
                                              self.portSpin.value(),
                                              timeout=10)
                else:
                    server = smtplib.SMTP(self.mailServerEdit.text(),
                                          self.portSpin.value(),
                                          timeout=10)
                    if self.useTlsButton.isChecked():
                        server.starttls()
                server.login(self.mailUserEdit.text(),
                             self.mailPasswordEdit.text())
                server.quit()
            E5MessageBox.information(
                self,
                self.tr("Login Test"),
                self.tr("""The login test succeeded."""))
        except (smtplib.SMTPException, OSError) as e:
            if isinstance(e, smtplib.SMTPResponseException):
                errorStr = e.smtp_error.decode()
            elif isinstance(e, socket.timeout):
                errorStr = str(e)
            elif isinstance(e, OSError):
                try:
                    errorStr = e[1]
                except TypeError:
                    errorStr = str(e)
            else:
                errorStr = str(e)
            E5MessageBox.critical(
                self,
                self.tr("Login Test"),
                self.tr(
                    """<p>The login test failed.<br>Reason: {0}</p>""")
                .format(errorStr))
    
    @pyqtSlot()
    def on_googleHelpButton_clicked(self):
        """
        Private slot to show some help text "how to turn on the Gmail API".
        """
        if self.__helpDialog is None:
            try:
                from E5Network.E5GoogleMail import GoogleMailHelp
                helpStr = GoogleMailHelp()
            except ImportError:
                helpStr = self.tr(
                    "<p>The Google Mail Client API is not installed."
                    " Use <code>{0}</code> to install it.</p>"
                ).format(getInstallCommand())
            
            from E5Gui.E5SimpleHelpDialog import E5SimpleHelpDialog
            self.__helpDialog = E5SimpleHelpDialog(
                title=self.tr("Gmail API Help"),
                helpStr=helpStr, parent=self)
        
        self.__helpDialog.show()
    
    @pyqtSlot()
    def on_googleInstallButton_clicked(self):
        """
        Private slot to install the required packages for use of Google Mail.
        """
        pip = e5App().getObject("Pip")
        pip.installPackages(RequiredPackages, interpreter=sys.executable)
        self.__checkGoogleMail()
    
    @pyqtSlot()
    def on_googleCheckAgainButton_clicked(self):
        """
        Private slot to check again the availability of Google Mail.
        """
        self.__checkGoogleMail()
    
    def __checkGoogleMail(self):
        """
        Private method to check the Google Mail availability and set the
        widgets accordingly.
        """
        self.googleMailInfoLabel.hide()
        self.googleInstallButton.show()
        self.googleCheckAgainButton.show()
        self.googleHelpButton.setEnabled(True)
        self.googleMailCheckBox.setEnabled(True)
        
        try:
            import E5Network.E5GoogleMail      # __IGNORE_WARNING__
            from E5Network.E5GoogleMailHelpers import (
                isClientSecretFileAvailable
            )
            
            self.googleInstallButton.hide()
            if not isClientSecretFileAvailable():
                # secrets file is not installed
                self.googleMailCheckBox.setChecked(False)
                self.googleMailCheckBox.setEnabled(False)
                self.googleMailInfoLabel.setText(self.tr(
                    "<p>The client secrets file is not present."
                    " Has the Gmail API been enabled?</p>"))
                self.googleMailInfoLabel.show()
                Preferences.setUser("UseGoogleMailOAuth2", False)
            else:
                self.googleMailCheckBox.setChecked(
                    Preferences.getUser("UseGoogleMailOAuth2"))
                self.googleMailInfoLabel.hide()
                self.googleCheckAgainButton.hide()
        except ImportError:
            # missing libraries, disable Google Mail
            self.googleMailCheckBox.setChecked(False)
            self.googleMailCheckBox.setEnabled(False)
            self.googleMailInfoLabel.setText(self.tr(
                "<p>The Google Mail Client API is not installed."
                " Use <code>{0}</code> to install it.</p>"
            ).format(getInstallCommand()))
            self.googleMailInfoLabel.show()
            self.googleHelpButton.setEnabled(False)
            Preferences.setUser("UseGoogleMailOAuth2", False)


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = EmailPage()
    return page
