# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the commit message.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QDialogButtonBox

from .Ui_GitCommitDialog import Ui_GitCommitDialog


class GitCommitDialog(QWidget, Ui_GitCommitDialog):
    """
    Class implementing a dialog to enter the commit message.
    
    @signal accepted() emitted, if the dialog was accepted
    @signal rejected() emitted, if the dialog was rejected
    """
    accepted = pyqtSignal()
    rejected = pyqtSignal()
    
    def __init__(self, vcs, msg, amend, commitAll, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param msg initial message (string)
        @param amend flag indicating to amend the HEAD commit (boolean)
        @param commitAll flag indicating to commit all local changes (boolean)
        @param parent parent widget (QWidget)
        """
        super(GitCommitDialog, self).__init__(
            parent, Qt.WindowFlags(Qt.WindowType.Window))
        self.setupUi(self)
        
        self.__vcs = vcs
        
        self.logEdit.setPlainText(msg)
        self.amendCheckBox.setChecked(amend)
        self.stagedCheckBox.setChecked(not commitAll)
    
    def showEvent(self, evt):
        """
        Protected method called when the dialog is about to be shown.
        
        @param evt the event (QShowEvent)
        """
        commitMessages = self.__vcs.getPlugin().getPreferences('Commits')
        self.recentComboBox.clear()
        self.recentComboBox.addItem("")
        for message in commitMessages:
            abbrMsg = message[:60]
            if len(message) > 60:
                abbrMsg += "..."
            self.recentComboBox.addItem(abbrMsg, message)
        
        self.logEdit.setFocus(Qt.FocusReason.OtherFocusReason)
    
    def logMessage(self):
        """
        Public method to retrieve the log message.
        
        @return the log message (string)
        """
        msg = self.logEdit.toPlainText()
        if msg:
            commitMessages = self.__vcs.getPlugin().getPreferences('Commits')
            if msg in commitMessages:
                commitMessages.remove(msg)
            commitMessages.insert(0, msg)
            no = self.__vcs.getPlugin().getPreferences("CommitMessages")
            del commitMessages[no:]
            self.__vcs.getPlugin().setPreferences(
                'Commits', commitMessages)
        
        return msg
    
    def stagedOnly(self):
        """
        Public method to retrieve the state of the staged only flag.
        
        @return state of the staged only flag (boolean)
        """
        return self.stagedCheckBox.isChecked()
    
    def amend(self):
        """
        Public method to retrieve the state of the amend flag.
        
        @return state of the amend flag (boolean)
        """
        return self.amendCheckBox.isChecked()
    
    def resetAuthor(self):
        """
        Public method to retrieve the state of the reset author flag.
        
        @return state of the reset author flag (boolean)
        """
        return self.resetAuthorCheckBox.isChecked()
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.logEdit.clear()
    
    def on_buttonBox_accepted(self):
        """
        Private slot called by the buttonBox accepted signal.
        """
        self.close()
        self.accepted.emit()
    
    def on_buttonBox_rejected(self):
        """
        Private slot called by the buttonBox rejected signal.
        """
        self.close()
        self.rejected.emit()
    
    @pyqtSlot(int)
    def on_recentComboBox_activated(self, index):
        """
        Private slot to select a commit message from recent ones.
        
        @param index index of the selected entry
        @type int
        """
        txt = self.recentComboBox.itemText(index)
        if txt:
            self.logEdit.setPlainText(self.recentComboBox.currentData())
