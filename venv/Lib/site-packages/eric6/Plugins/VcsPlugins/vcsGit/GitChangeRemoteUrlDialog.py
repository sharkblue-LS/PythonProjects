# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to change the URL of a remote git repository.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QUrl
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_GitChangeRemoteUrlDialog import Ui_GitChangeRemoteUrlDialog


class GitChangeRemoteUrlDialog(QDialog, Ui_GitChangeRemoteUrlDialog):
    """
    Class implementing a dialog to change the URL of a remote git repository.
    """
    def __init__(self, remoteName, remoteUrl, parent=None):
        """
        Constructor
        
        @param remoteName name of the remote repository
        @type str
        @param remoteUrl URL of the remote repository
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GitChangeRemoteUrlDialog, self).__init__(parent)
        self.setupUi(self)
        
        url = QUrl(remoteUrl)
        self.__userInfo = url.userInfo()
        
        self.nameEdit.setText(remoteName)
        self.urlEdit.setText(
            url.toString(QUrl.UrlFormattingOption.RemoveUserInfo))
        
        self.__updateOK()
        
        self.newUrlEdit.setFocus(Qt.FocusReason.OtherFocusReason)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateOK(self):
        """
        Private method to update the status of the OK button.
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(self.newUrlEdit.text())
        )
    
    @pyqtSlot(str)
    def on_newUrlEdit_textChanged(self, txt):
        """
        Private slot handling changes of the entered URL.
        
        @param txt current text
        @type str
        """
        self.__updateOK()
    
    def getData(self):
        """
        Public method to get the entered data.
        
        @return tuple with name and new URL of the remote repository
        @rtype tuple of (str, str)
        """
        url = QUrl.fromUserInput(self.newUrlEdit.text())
        if self.__userInfo:
            url.setUserInfo(self.__userInfo)
        
        return self.nameEdit.text(), url.toString()
