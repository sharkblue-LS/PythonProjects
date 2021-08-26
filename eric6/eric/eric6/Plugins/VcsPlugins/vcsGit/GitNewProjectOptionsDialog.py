# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Git Options Dialog for a new project from the
repository.
"""

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui.E5Completers import E5DirCompleter
from E5Gui import E5FileDialog

from .Ui_GitNewProjectOptionsDialog import Ui_GitNewProjectOptionsDialog
from .Config import ConfigGitSchemes

import Utilities
import Preferences
import UI.PixmapCache


class GitNewProjectOptionsDialog(QDialog, Ui_GitNewProjectOptionsDialog):
    """
    Class implementing the Options Dialog for a new project from the
    repository.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the version control object
        @param parent parent widget (QWidget)
        """
        super(GitNewProjectOptionsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__vcs = vcs
        
        self.projectDirButton.setIcon(UI.PixmapCache.getIcon("open"))
        self.vcsUrlButton.setIcon(UI.PixmapCache.getIcon("open"))
        self.vcsUrlClearHistoryButton.setIcon(
            UI.PixmapCache.getIcon("editDelete"))
        
        vcsUrlHistory = self.__vcs.getPlugin().getPreferences(
            "RepositoryUrlHistory")
        self.vcsUrlCombo.addItems(vcsUrlHistory)
        self.vcsUrlCombo.setEditText("")
        
        self.vcsDirectoryCompleter = E5DirCompleter(self.vcsUrlCombo)
        self.vcsProjectDirCompleter = E5DirCompleter(self.vcsProjectDirEdit)
        
        ipath = (
            Preferences.getMultiProject("Workspace") or
            Utilities.getHomeDir()
        )
        self.__initPaths = [
            Utilities.fromNativeSeparators(ipath),
            Utilities.fromNativeSeparators(ipath) + "/",
        ]
        self.vcsProjectDirEdit.setText(
            Utilities.toNativeSeparators(self.__initPaths[0]))
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    @pyqtSlot(str)
    def on_vcsProjectDirEdit_textChanged(self, txt):
        """
        Private slot to handle a change of the project directory.
        
        @param txt name of the project directory (string)
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(txt) and
            Utilities.fromNativeSeparators(txt) not in self.__initPaths)
    
    @pyqtSlot()
    def on_vcsUrlButton_clicked(self):
        """
        Private slot to display a selection dialog.
        """
        directory = E5FileDialog.getExistingDirectory(
            self,
            self.tr("Select Repository-Directory"),
            self.vcsUrlCombo.currentText(),
            E5FileDialog.Options(E5FileDialog.ShowDirsOnly))
        
        if directory:
            self.vcsUrlCombo.setEditText(
                Utilities.toNativeSeparators(directory))
    
    @pyqtSlot()
    def on_projectDirButton_clicked(self):
        """
        Private slot to display a directory selection dialog.
        """
        directory = E5FileDialog.getExistingDirectory(
            self,
            self.tr("Select Project Directory"),
            self.vcsProjectDirEdit.text(),
            E5FileDialog.Options(E5FileDialog.ShowDirsOnly))
        
        if directory:
            self.vcsProjectDirEdit.setText(
                Utilities.toNativeSeparators(directory))
    
    @pyqtSlot(str)
    def on_vcsUrlCombo_editTextChanged(self, txt):
        """
        Private slot to handle changes of the URL.
        
        @param txt current text of the combo box
        @type str
        """
        enable = False
        vcsUrlEnable = False
        
        if txt:
            url = QUrl.fromUserInput(txt)
            if url.isValid():
                if url.scheme() in ConfigGitSchemes:
                    enable = True
                    vcsUrlEnable = url.scheme() == "file"
            elif ':' in txt:
                # assume scp like repository URL
                enable = True
        else:
            vcsUrlEnable = True
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enable)
        self.vcsUrlButton.setEnabled(vcsUrlEnable)
    
    @pyqtSlot()
    def on_vcsUrlClearHistoryButton_clicked(self):
        """
        Private slot to clear the history of entered repository URLs.
        """
        currentVcsUrl = self.vcsUrlCombo.currentText()
        self.vcsUrlCombo.clear()
        self.vcsUrlCombo.setEditText(currentVcsUrl)
        
        self.__saveHistory()
    
    def getData(self):
        """
        Public slot to retrieve the data entered into the dialog.
        
        @return a tuple of a string (project directory) and a dictionary
            containing the data entered.
        """
        self.__saveHistory()
        
        vcsdatadict = {
            "url": self.vcsUrlCombo.currentText().replace("\\", "/"),
        }
        return (self.vcsProjectDirEdit.text(), vcsdatadict)
    
    def __saveHistory(self):
        """
        Private method to save the repository URL history.
        """
        url = self.vcsUrlCombo.currentText()
        vcsUrlHistory = []
        for index in range(self.vcsUrlCombo.count()):
            vcsUrlHistory.append(self.vcsUrlCombo.itemText(index))
        if url not in vcsUrlHistory:
            vcsUrlHistory.insert(0, url)
        
        # max. list sizes is hard coded to 20 entries
        newVcsUrlHistory = [url for url in vcsUrlHistory if url]
        if len(newVcsUrlHistory) > 20:
            newVcsUrlHistory = newVcsUrlHistory[:20]
        
        self.__vcs.getPlugin().setPreferences(
            "RepositoryUrlHistory", newVcsUrlHistory)
