# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Git version control plugin.
"""

import os

from PyQt5.QtCore import QObject, QCoreApplication, QTranslator, QByteArray

from E5Gui.E5Application import e5App

import Preferences
from Preferences.Shortcuts import readShortcuts

from VcsPlugins.vcsGit.GitUtilities import getConfigPath

import Utilities
import UI.Info

# Start-Of-Header
name = "Git Plugin"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = False
deactivateable = True
version = UI.Info.VersionOnly
pluginType = "version_control"
pluginTypename = "Git"
className = "VcsGitPlugin"
packageName = "__core__"
shortDescription = "Implements the Git version control interface."
longDescription = (
    """This plugin provides the Git version control interface."""
)
pyqtApi = 2
# End-Of-Header

error = ""


def exeDisplayData():
    """
    Public method to support the display of some executable info.
    
    @return dictionary containing the data to query the presence of
        the executable
    """
    exe = 'git'
    if Utilities.isWindowsPlatform():
        exe += '.exe'
    
    data = {
        "programEntry": True,
        "header": QCoreApplication.translate(
            "VcsGitPlugin", "Version Control - Git"),
        "exe": exe,
        "versionCommand": 'version',
        "versionStartsWith": 'git',
        "versionPosition": 2,
        "version": "",
        "versionCleanup": None,
    }
    
    return data


def getVcsSystemIndicator():
    """
    Public function to get the indicators for this version control system.
    
    @return dictionary with indicator as key and a tuple with the vcs name
        (string) and vcs display string (string)
    """
    global pluginTypename
    data = {}
    exe = 'git'
    if Utilities.isWindowsPlatform():
        exe += '.exe'
    if Utilities.isinpath(exe):
        data[".git"] = (pluginTypename, displayString())
        data["_git"] = (pluginTypename, displayString())
    return data


def displayString():
    """
    Public function to get the display string.
    
    @return display string (string)
    """
    exe = 'git'
    if Utilities.isWindowsPlatform():
        exe += '.exe'
    if Utilities.isinpath(exe):
        return QCoreApplication.translate('VcsGitPlugin', 'Git')
    else:
        return ""


gitCfgPluginObject = None


def createConfigurationPage(configDlg):
    """
    Module function to create the configuration page.
    
    @param configDlg reference to the configuration dialog (QDialog)
    @return reference to the configuration page
    """
    global gitCfgPluginObject
    from VcsPlugins.vcsGit.ConfigurationPage.GitPage import (
        GitPage
    )
    if gitCfgPluginObject is None:
        gitCfgPluginObject = VcsGitPlugin(None)
    page = GitPage(gitCfgPluginObject)
    return page
    

def getConfigData():
    """
    Module function returning data as required by the configuration dialog.
    
    @return dictionary with key "zzz_gitPage" containing the relevant
        data
    """
    return {
        "zzz_gitPage":
        [QCoreApplication.translate("VcsGitPlugin", "Git"),
            os.path.join("VcsPlugins", "vcsGit", "icons",
                         "preferences-git.svg"),
            createConfigurationPage, "vcsPage", None],
    }


def prepareUninstall():
    """
    Module function to prepare for an uninstallation.
    """
    if not e5App().getObject("PluginManager").isPluginLoaded(
            "PluginVcsGit"):
        Preferences.Prefs.settings.remove("Git")


def clearPrivateData():
    """
    Module function to clear the private data of the plug-in.
    """
    for key in ["RepositoryUrlHistory"]:
        VcsGitPlugin.setPreferences(key, [])
    

class VcsGitPlugin(QObject):
    """
    Class implementing the Git version control plugin.
    """
    GitDefaults = {
        "StopLogOnCopy": True,          # used in log browser
        "ShowAuthorColumns": True,      # used in log browser
        "ShowCommitterColumns": True,   # used in log browser
        "ShowCommitIdColumn": True,     # used in log browser
        "ShowBranchesColumn": True,     # used in log browser
        "ShowTagsColumn": True,         # used in log browser
        "FindCopiesHarder": False,      # used in log browser
        "LogLimit": 20,
        "LogSubjectColumnWidth": 30,
        "LogBrowserGeometry": QByteArray(),
        "LogBrowserSplitterStates": [QByteArray(), QByteArray(),
                                     QByteArray()],
        # mainSplitter, detailsSplitter, diffSplitter
        "StatusDialogGeometry": QByteArray(),
        "StatusDialogSplitterStates": [QByteArray(), QByteArray()],
        # vertical splitter, horizontal splitter
        "CommitMessages": 20,
        "Commits": [],
        "CommitIdLength": 10,
        "CleanupPatterns": "*.orig *.rej *~",
        "AggressiveGC": True,
        "RepositoryUrlHistory": [],
    }
    
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object (UI.UserInterface)
        """
        super(VcsGitPlugin, self).__init__(ui)
        self.__ui = ui
        
        self.__translator = None
        self.__loadTranslator()
        
        from VcsPlugins.vcsGit.ProjectHelper import GitProjectHelper
        self.__projectHelperObject = GitProjectHelper(None, None)
        try:
            e5App().registerPluginObject(
                pluginTypename, self.__projectHelperObject, pluginType)
        except KeyError:
            pass    # ignore duplicate registration
        
        readShortcuts(pluginName=pluginTypename)
    
    def getProjectHelper(self):
        """
        Public method to get a reference to the project helper object.
        
        @return reference to the project helper object
        """
        return self.__projectHelperObject

    def initToolbar(self, ui, toolbarManager):
        """
        Public slot to initialize the VCS toolbar.
        
        @param ui reference to the main window (UserInterface)
        @param toolbarManager reference to a toolbar manager object
            (E5ToolBarManager)
        """
        if self.__projectHelperObject:
            self.__projectHelperObject.initToolbar(ui, toolbarManager)
    
    def activate(self):
        """
        Public method to activate this plugin.
        
        @return tuple of reference to instantiated viewmanager and
            activation status (boolean)
        """
        from VcsPlugins.vcsGit.git import Git
        self.__object = Git(self, self.__ui)
        
        tb = self.__ui.getToolbar("vcs")[1]
        tb.setVisible(False)
        tb.setEnabled(False)
        
        tb = self.__ui.getToolbar("git")[1]
        tb.setVisible(Preferences.getVCS("ShowVcsToolbar"))
        tb.setEnabled(True)
        
        return self.__object, True
    
    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        self.__object = None
        
        tb = self.__ui.getToolbar("git")[1]
        tb.setVisible(False)
        tb.setEnabled(False)
        
        tb = self.__ui.getToolbar("vcs")[1]
        tb.setVisible(Preferences.getVCS("ShowVcsToolbar"))
        tb.setEnabled(True)
    
    @classmethod
    def getPreferences(cls, key):
        """
        Class method to retrieve the various settings.
        
        @param key the key of the value to get
        @return the requested setting
        """
        if key in ["StopLogOnCopy", "ShowReflogInfo", "ShowAuthorColumns",
                   "ShowCommitterColumns", "ShowCommitIdColumn",
                   "ShowBranchesColumn", "ShowTagsColumn", "FindCopiesHarder",
                   "AggressiveGC"]:
            return Preferences.toBool(Preferences.Prefs.settings.value(
                "Git/" + key, cls.GitDefaults[key]))
        elif key in ["LogLimit", "CommitMessages", "CommitIdLength",
                     "LogSubjectColumnWidth"]:
            return int(Preferences.Prefs.settings.value(
                "Git/" + key, cls.GitDefaults[key]))
        elif key in ["Commits", "RepositoryUrlHistory"]:
            return Preferences.toList(Preferences.Prefs.settings.value(
                "Git/" + key))
        elif key in ["LogBrowserGeometry", "StatusDialogGeometry"]:
            v = Preferences.Prefs.settings.value("Git/" + key)
            if v is not None:
                return v
            else:
                return cls.GitDefaults[key]
        elif key in ["LogBrowserSplitterStates", "StatusDialogSplitterStates"]:
            states = Preferences.Prefs.settings.value("Git/" + key)
            if states is not None:
                return states
            else:
                return cls.GitDefaults[key]
        else:
            return Preferences.Prefs.settings.value(
                "Git/" + key, cls.GitDefaults[key])
    
    @classmethod
    def setPreferences(cls, key, value):
        """
        Class method to store the various settings.
        
        @param key the key of the setting to be set
        @param value the value to be set
        """
        Preferences.Prefs.settings.setValue("Git/" + key, value)

    def getConfigPath(self):
        """
        Public method to get the filename of the config file.
        
        @return filename of the config file (string)
        """
        return getConfigPath()
    
    def prepareUninstall(self):
        """
        Public method to prepare for an uninstallation.
        """
        e5App().unregisterPluginObject(pluginTypename)
    
    def prepareUnload(self):
        """
        Public method to prepare for an unload.
        """
        if self.__projectHelperObject:
            self.__projectHelperObject.removeToolbar(
                self.__ui, e5App().getObject("ToolbarManager"))
        e5App().unregisterPluginObject(pluginTypename)
    
    def __loadTranslator(self):
        """
        Private method to load the translation file.
        """
        if self.__ui is not None:
            loc = self.__ui.getLocale()
            if loc and loc != "C":
                locale_dir = os.path.join(
                    os.path.dirname(__file__), "vcsGit", "i18n")
                translation = "git_{0}".format(loc)
                translator = QTranslator(None)
                loaded = translator.load(translation, locale_dir)
                if loaded:
                    self.__translator = translator
                    e5App().installTranslator(self.__translator)
                else:
                    print("Warning: translation file '{0}' could not be"
                          " loaded.".format(translation))
                    print("Using default.")

#
# eflag: noqa = M801
