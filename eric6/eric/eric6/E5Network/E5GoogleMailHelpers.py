# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some helpers for Google mail.
"""

import os

import Globals

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'eric_client_secret.json'          # secok
TOKEN_FILE = 'eric_python_email_send_token.json'        # secok
APPLICATION_NAME = 'Eric Python Send Email'

RequiredPackages = (
    "google-api-python-client",
    "requests-oauthlib",
)


def isClientSecretFileAvailable():
    """
    Module function to check, if the client secret file has been installed.
    
    @return flag indicating, that the credentials file is there
    @rtype bool
    """
    return os.path.exists(
        os.path.join(Globals.getConfigDir(), CLIENT_SECRET_FILE))


def getInstallCommand():
    """
    Module function to get the install command to get the Google mail support
    activated.
    
    @return install command
    @rtype str
    """
    pipCommand = "pip install --upgrade {0}".format(
        " ".join(RequiredPackages))
    
    return pipCommand
