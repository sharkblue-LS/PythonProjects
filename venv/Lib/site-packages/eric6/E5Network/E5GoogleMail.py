# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to send bug reports.
"""

import os
import base64
import json
import datetime

from googleapiclient import discovery
from google.oauth2.credentials import Credentials
from requests_oauthlib import OAuth2Session

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QUrl, QUrlQuery
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from E5Gui.E5TextInputDialog import E5TextInputDialog

import Globals

from .E5GoogleMailHelpers import (
    CLIENT_SECRET_FILE, SCOPES, TOKEN_FILE, APPLICATION_NAME
)


class E5GoogleMailAuthBrowser(QDialog):
    """
    Class implementing a simple web browser to perform the OAuth2
    authentication process.
    
    @signal approvalCodeReceived(str) emitted to indicate the receipt of the
        approval code
    """
    approvalCodeReceived = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5GoogleMailAuthBrowser, self).__init__(parent)
        
        self.__layout = QVBoxLayout(self)
        
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        self.__browser = QWebEngineView(self)
        self.__browser.titleChanged.connect(self.__titleChanged)
        self.__browser.loadFinished.connect(self.__pageLoadFinished)
        self.__layout.addWidget(self.__browser)
        
        self.__buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close)
        self.__buttonBox.rejected.connect(self.reject)
        self.__layout.addWidget(self.__buttonBox)
        
        self.resize(600, 700)
    
    @pyqtSlot(str)
    def __titleChanged(self, title):
        """
        Private slot handling changes of the web page title.
        
        @param title web page title
        @type str
        """
        self.setWindowTitle(title)
    
    @pyqtSlot()
    def __pageLoadFinished(self):
        """
        Private slot handling the loadFinished signal.
        """
        url = self.__browser.url()
        if url.toString().startswith(
                "https://accounts.google.com/o/oauth2/approval/v2"):
            urlQuery = QUrlQuery(url)
            approvalCode = urlQuery.queryItemValue(
                "approvalCode", QUrl.ComponentFormattingOption.FullyDecoded)
            if approvalCode:
                self.approvalCodeReceived.emit(approvalCode)
                self.close()
    
    def load(self, url):
        """
        Public method to start the authorization flow by loading the given URL.
        
        @param url URL to be laoded
        @type str or QUrl
        """
        self.__browser.setUrl(QUrl(url))


class E5GoogleMail(QObject):
    """
    Class implementing the logic to send emails via Google Mail.
    
    @signal sendResult(bool, str) emitted to indicate the transmission result
        and a result message
    """
    sendResult = pyqtSignal(bool, str)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object
        @type QObject
        """
        super(E5GoogleMail, self).__init__(parent=parent)
        
        self.__messages = []
        
        self.__session = None
        self.__clientConfig = {}
        
        self.__browser = None
    
    def sendMessage(self, message):
        """
        Public method to send a message via Google Mail.
        
        @param message email message to be sent
        @type email.mime.text.MIMEBase
        """
        self.__messages.append(message)
        
        if not self.__session:
            self.__startSession()
        else:
            self.__doSendMessages()
    
    def __prepareMessage(self, message):
        """
        Private method to prepare the message for sending.
        
        @param message message to be prepared
        @type email.mime.text.MIMEBase
        @return prepared message dictionary
        @rtype dict
        """
        messageAsBase64 = base64.urlsafe_b64encode(message.as_bytes())
        raw = messageAsBase64.decode()
        return {'raw': raw}
    
    def __startSession(self):
        """
        Private method to start an authorized session and optionally start the
        authorization flow.
        """
        # check for availability of secrets file
        if not os.path.exists(os.path.join(Globals.getConfigDir(),
                                           CLIENT_SECRET_FILE)):
            self.sendResult.emit(
                False,
                self.tr("The client secrets file is not present. Has the Gmail"
                        " API been enabled?")
            )
            return
        
        with open(os.path.join(Globals.getConfigDir(), CLIENT_SECRET_FILE),
                  "r") as clientSecret:
            clientData = json.load(clientSecret)
            self.__clientConfig = clientData['installed']
        token = self.__loadToken()
        if token is None:
            # no valid OAuth2 token available
            self.__session = OAuth2Session(
                self.__clientConfig['client_id'],
                scope=SCOPES,
                redirect_uri=self.__clientConfig['redirect_uris'][0]
            )
            authorizationUrl, _ = self.__session.authorization_url(
                self.__clientConfig['auth_uri'],
                access_type="offline",
                prompt="select_account"
            )
            if self.__browser is None:
                try:
                    self.__browser = E5GoogleMailAuthBrowser()
                    self.__browser.approvalCodeReceived.connect(
                        self.__processAuthorization)
                except ImportError:
                    pass
            if self.__browser:
                self.__browser.show()
                self.__browser.load(QUrl(authorizationUrl))
            else:
                from PyQt5.QtGui import QDesktopServices
                QDesktopServices.openUrl(QUrl(authorizationUrl))
                ok, authCode = E5TextInputDialog.getText(
                    None,
                    self.tr("OAuth2 Authorization Code"),
                    self.tr("Enter the OAuth2 authorization code:"))
                if ok and authCode:
                    self.__processAuthorization(authCode)
                else:
                    self.__session = None
        else:
            self.__session = OAuth2Session(
                self.__clientConfig['client_id'],
                scope=SCOPES,
                redirect_uri=self.__clientConfig['redirect_uris'][0],
                token=token,
                auto_refresh_kwargs={
                    'client_id': self.__clientConfig['client_id'],
                    'client_secret': self.__clientConfig['client_secret'],
                },
                auto_refresh_url=self.__clientConfig['token_uri'],
                token_updater=self.__saveToken)
            self.__doSendMessages()
    
    @pyqtSlot(str)
    def __processAuthorization(self, authCode):
        """
        Private slot to process the received authorization code.
        
        @param authCode received authorization code
        @type str
        """
        self.__session.fetch_token(
            self.__clientConfig['token_uri'],
            client_secret=self.__clientConfig['client_secret'],
            code=authCode)
        self.__saveToken(self.__session.token)
        
        # authorization completed; now send all queued messages
        self.__doSendMessages()
    
    def __doSendMessages(self):
        """
        Private method to send all queued messages.
        """
        if not self.__session:
            self.sendResult.emit(
                False,
                self.tr("No authorized session available.")
            )
            return
        
        try:
            results = []
            credentials = self.__credentialsFromSession()
            service = discovery.build('gmail', 'v1', credentials=credentials,
                                      cache_discovery=False)
            count = 0
            while self.__messages:
                count += 1
                message = self.__messages.pop(0)
                message1 = self.__prepareMessage(message)
                service.users().messages().send(
                    userId="me", body=message1).execute()
                results.append(self.tr("Message #{0} sent.").format(count))

            self.sendResult.emit(True, "\n\n".join(results))
        except Exception as error:
            self.sendResult.emit(False, str(error))
    
    def __loadToken(self):
        """
        Private method to load a token from the token file.
        
        @return loaded token
        @rtype dict or None
        """
        homeDir = os.path.expanduser('~')
        credentialsDir = os.path.join(homeDir, '.credentials')
        if not os.path.exists(credentialsDir):
            os.makedirs(credentialsDir)
        tokenPath = os.path.join(credentialsDir, TOKEN_FILE)
        
        if os.path.exists(tokenPath):
            with open(tokenPath, "r") as tokenFile:
                return json.load(tokenFile)
        else:
            return None
    
    def __saveToken(self, token):
        """
        Private method to save a token to the token file.
        
        @param token token to be saved
        @type dict
        """
        homeDir = os.path.expanduser('~')
        credentialsDir = os.path.join(homeDir, '.credentials')
        if not os.path.exists(credentialsDir):
            os.makedirs(credentialsDir)
        tokenPath = os.path.join(credentialsDir, TOKEN_FILE)
        
        with open(tokenPath, "w") as tokenFile:
            json.dump(token, tokenFile)
    
    def __credentialsFromSession(self):
        """
        Private method to create a credentials object.
        
        @return created credentials object
        @rtype google.oauth2.credentials.Credentials
        """
        credentials = None
        
        if self.__clientConfig and self.__session:
            token = self.__session.token
            if token:
                credentials = Credentials(
                    token['access_token'],
                    refresh_token=token.get('refresh_token'),
                    id_token=token.get('id_token'),
                    token_uri=self.__clientConfig['token_uri'],
                    client_id=self.__clientConfig['client_id'],
                    client_secret=self.__clientConfig['client_secret'],
                    scopes=SCOPES
                )
                credentials.expiry = datetime.datetime.fromtimestamp(
                    token['expires_at'])
        
        return credentials


def GoogleMailHelp():
    """
    Module function to get some help about how to enable the Google Mail
    OAuth2 service.
    
    @return help text
    @rtype str
    """
    return (
        "<h2>Steps to turn on the Gmail API</h2>"
        "<ol>"
        "<li>Use <a href='{0}'>this wizard</a> to create or select a project"
        " in the Google Developers Console and automatically turn on the API."
        " Click <b>Continue</b>, then <b>Go to credentials</b>.</li>"
        "<li>At the top of the page, select the <b>OAuth consent screen</b>"
        " tab. Select an <b>Email address</b>, enter a <b>Product name</b> if"
        " not already set, and click the <b>Save</b> button.</li>"
        "<li>Select the <b>Credentials</b> tab, click the <b>Add credentials"
        "</b> button and select <b>OAuth 2.0 client ID</b>.</li>"
        "<li>Select the application type <b>Other</b>, enter the name &quot;"
        "{1}&quot;, and click the <b>Create</b>"
        " button.</li>"
        "<li>Click <b>OK</b> to dismiss the resulting dialog.</li>"
        "<li>Click the (Download JSON) button to the right of the client ID."
        "</li>"
        "<li>Move this file to the eric configuration directory"
        " <code>{2}</code> and rename it <code>{3}</code>.</li>"
        "</ol>".format(
            "https://console.developers.google.com/start/api?id=gmail",
            APPLICATION_NAME,
            Globals.getConfigDir(),
            CLIENT_SECRET_FILE
        )
    )
