# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to browse the change lists.
"""

import os

import pysvn

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem

from E5Gui.E5OverrideCursor import E5OverrideCursor

from E5Utilities.E5MutexLocker import E5MutexLocker

from .SvnDialogMixin import SvnDialogMixin

from .Ui_SvnChangeListsDialog import Ui_SvnChangeListsDialog


class SvnChangeListsDialog(QDialog, SvnDialogMixin, Ui_SvnChangeListsDialog):
    """
    Class implementing a dialog to browse the change lists.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param parent parent widget (QWidget)
        """
        super(SvnChangeListsDialog, self).__init__(parent)
        self.setupUi(self)
        SvnDialogMixin.__init__(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.vcs = vcs
        
        self.client = self.vcs.getClient()
        self.client.callback_cancel = self._clientCancelCallback
        self.client.callback_get_login = self._clientLoginCallback
        self.client.callback_ssl_server_trust_prompt = (
            self._clientSslServerTrustPromptCallback
        )
    
    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_changeLists_currentItemChanged(self, current, previous):
        """
        Private slot to handle the selection of a new item.
        
        @param current current item (QListWidgetItem)
        @param previous previous current item (QListWidgetItem)
        """
        self.filesList.clear()
        if current is not None:
            changelist = current.text()
            if changelist in self.changeListsDict:
                self.filesList.addItems(
                    sorted(self.changeListsDict[changelist]))
    
    def start(self, path):
        """
        Public slot to populate the data.
        
        @param path directory name to show change lists for (string)
        """
        self.changeListsDict = {}
        self.cancelled = False
        
        self.filesLabel.setText(
            self.tr("Files (relative to {0}):").format(path))
        
        with E5OverrideCursor():
            try:
                with E5MutexLocker(self.vcs.vcsExecutionMutex):
                    entries = self.client.get_changelist(
                        path, depth=pysvn.depth.infinity)
                for entry in entries:
                    file = entry[0]
                    changelist = entry[1]
                    if changelist not in self.changeListsDict:
                        self.changeListsDict[changelist] = []
                    filename = file.replace(path + os.sep, "")
                    if filename not in self.changeListsDict[changelist]:
                        self.changeListsDict[changelist].append(filename)
            except pysvn.ClientError as e:
                self.__showError(e.args[0])
        self.__finish()
    
    def __finish(self):
        """
        Private slot called when the user pressed the button.
        """
        self.changeLists.addItems(sorted(self.changeListsDict.keys()))
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        
        if len(self.changeListsDict) == 0:
            self.changeLists.addItem(self.tr("No changelists found"))
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Close).setFocus(
                    Qt.FocusReason.OtherFocusReason)
        else:
            self.changeLists.setCurrentRow(0)
            self.changeLists.setFocus(Qt.FocusReason.OtherFocusReason)
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.cancelled = True
            self.__finish()
