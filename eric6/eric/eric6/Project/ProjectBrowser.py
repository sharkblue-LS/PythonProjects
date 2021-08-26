# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the project browser part of the eric UI.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

from E5Gui.E5TabWidget import E5TabWidget
from E5Gui.E5Led import E5ClickableLed

import UI.PixmapCache
import Preferences

from .ProjectBrowserFlags import (
    SourcesBrowserFlag, FormsBrowserFlag, ResourcesBrowserFlag,
    TranslationsBrowserFlag, InterfacesBrowserFlag, OthersBrowserFlag,
    ProtocolsBrowserFlag, AllBrowsersFlag
)


class ProjectBrowser(E5TabWidget):
    """
    Class implementing the project browser part of the eric UI.
    
    It generates a widget with up to seven tabs. The individual tabs contain
    the project sources browser, the project forms browser,
    the project resources browser, the project translations browser,
    the project interfaces (IDL) browser and a browser for stuff,
    that doesn't fit these categories. Optionally it contains an additional
    tab with the file system browser.
    """
    def __init__(self, project, parent=None):
        """
        Constructor
        
        @param project reference to the project object
        @param parent parent widget (QWidget)
        """
        E5TabWidget.__init__(self, parent)
        self.project = project
        
        self.setWindowIcon(UI.PixmapCache.getIcon("eric"))
        
        self.setUsesScrollButtons(True)
        
        self.vcsStatusIndicator = E5ClickableLed(self)
        self.setCornerWidget(self.vcsStatusIndicator, Qt.Corner.TopLeftCorner)
        self.vcsStatusIndicator.clicked.connect(
            self.__vcsStatusIndicatorClicked)
        self.vcsStatusColorNames = {
            "A": "VcsAdded",
            "M": "VcsModified",
            "O": "VcsRemoved",
            "R": "VcsReplaced",
            "U": "VcsUpdate",
            "Z": "VcsConflict",
        }
        self.vcsStatusText = {
            " ": self.tr("up to date"),
            "A": self.tr("files added"),
            "M": self.tr("local modifications"),
            "O": self.tr("files removed"),
            "R": self.tr("files replaced"),
            "U": self.tr("update required"),
            "Z": self.tr("conflict"),
        }
        self.__vcsStateChanged(" ")
        
        # step 1: create all the individual browsers
        from .ProjectSourcesBrowser import ProjectSourcesBrowser
        from .ProjectFormsBrowser import ProjectFormsBrowser
        from .ProjectTranslationsBrowser import ProjectTranslationsBrowser
        from .ProjectResourcesBrowser import ProjectResourcesBrowser
        from .ProjectInterfacesBrowser import ProjectInterfacesBrowser
        from .ProjectOthersBrowser import ProjectOthersBrowser
        from .ProjectProtocolsBrowser import ProjectProtocolsBrowser
        # sources browser
        self.psBrowser = ProjectSourcesBrowser(self.project)
        # forms browser
        self.pfBrowser = ProjectFormsBrowser(self.project)
        # resources browser
        self.prBrowser = ProjectResourcesBrowser(self.project)
        # translations browser
        self.ptBrowser = ProjectTranslationsBrowser(self.project)
        # interfaces (IDL) browser
        self.piBrowser = ProjectInterfacesBrowser(self.project)
        # protocols (protobuf) browser
        self.ppBrowser = ProjectProtocolsBrowser(self.project)
        # others browser
        self.poBrowser = ProjectOthersBrowser(self.project)
        
        # step 2: connect all the browsers
        # connect the sources browser
        self.project.projectClosed.connect(self.psBrowser._projectClosed)
        self.project.projectOpened.connect(self.psBrowser._projectOpened)
        self.project.newProject.connect(self.psBrowser._newProject)
        self.project.reinitVCS.connect(self.psBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.psBrowser._initMenusAndVcs)
        
        # connect the forms browser
        self.project.projectClosed.connect(self.pfBrowser._projectClosed)
        self.project.projectOpened.connect(self.pfBrowser._projectOpened)
        self.project.newProject.connect(self.pfBrowser._newProject)
        self.project.reinitVCS.connect(self.pfBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.pfBrowser._initMenusAndVcs)
        
        # connect the resources browser
        self.project.projectClosed.connect(self.prBrowser._projectClosed)
        self.project.projectOpened.connect(self.prBrowser._projectOpened)
        self.project.newProject.connect(self.prBrowser._newProject)
        self.project.reinitVCS.connect(self.prBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.prBrowser._initMenusAndVcs)
        
        # connect the translations browser
        self.project.projectClosed.connect(self.ptBrowser._projectClosed)
        self.project.projectOpened.connect(self.ptBrowser._projectOpened)
        self.project.newProject.connect(self.ptBrowser._newProject)
        self.project.reinitVCS.connect(self.ptBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.ptBrowser._initMenusAndVcs)
        
        # connect the interfaces (IDL)  browser
        self.project.projectClosed.connect(self.piBrowser._projectClosed)
        self.project.projectOpened.connect(self.piBrowser._projectOpened)
        self.project.newProject.connect(self.piBrowser._newProject)
        self.project.reinitVCS.connect(self.piBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.piBrowser._initMenusAndVcs)
        
        # connect the protocols (protobuf)  browser
        self.project.projectClosed.connect(self.ppBrowser._projectClosed)
        self.project.projectOpened.connect(self.ppBrowser._projectOpened)
        self.project.newProject.connect(self.ppBrowser._newProject)
        self.project.reinitVCS.connect(self.ppBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.ppBrowser._initMenusAndVcs)
        
        # connect the others browser
        self.project.projectClosed.connect(self.poBrowser._projectClosed)
        self.project.projectOpened.connect(self.poBrowser._projectOpened)
        self.project.newProject.connect(self.poBrowser._newProject)
        self.project.reinitVCS.connect(self.poBrowser._initMenusAndVcs)
        self.project.projectPropertiesChanged.connect(
            self.poBrowser._initMenusAndVcs)
        
        # add signal connection to ourselves
        self.project.projectOpened.connect(self.__projectOpened)
        self.project.projectClosed.connect(self.__projectClosed)
        self.project.newProject.connect(self.__newProject)
        self.project.projectPropertiesChanged.connect(
            self.__projectPropertiesChanged)
        self.currentChanged.connect(self.__currentChanged)
        self.project.getModel().vcsStateChanged.connect(self.__vcsStateChanged)
        
        self.__currentBrowsersFlags = 0
        self.__projectPropertiesChanged()
        self.setCurrentIndex(0)
        
    def __setBrowsersAvailable(self, browserFlags):
        """
        Private method to add selected browsers to the project browser.
        
        @param browserFlags flags indicating the browsers to add (integer)
        """
        # step 1: remove all tabs
        while self.count() > 0:
            self.removeTab(0)
        
        # step 2: add browsers
        if browserFlags & SourcesBrowserFlag:
            index = self.addTab(
                self.psBrowser,
                UI.PixmapCache.getIcon("projectSources"), '')
            self.setTabToolTip(index, self.psBrowser.windowTitle())
        
        if browserFlags & FormsBrowserFlag:
            index = self.addTab(
                self.pfBrowser,
                UI.PixmapCache.getIcon("projectForms"), '')
            self.setTabToolTip(index, self.pfBrowser.windowTitle())
        
        if browserFlags & ResourcesBrowserFlag:
            index = self.addTab(
                self.prBrowser,
                UI.PixmapCache.getIcon("projectResources"), '')
            self.setTabToolTip(index, self.prBrowser.windowTitle())
        
        if browserFlags & TranslationsBrowserFlag:
            index = self.addTab(
                self.ptBrowser,
                UI.PixmapCache.getIcon("projectTranslations"), '')
            self.setTabToolTip(index, self.ptBrowser.windowTitle())
        
        if browserFlags & InterfacesBrowserFlag:
            index = self.addTab(
                self.piBrowser,
                UI.PixmapCache.getIcon("projectInterfaces"), '')
            self.setTabToolTip(index, self.piBrowser.windowTitle())
        
        if browserFlags & ProtocolsBrowserFlag:
            index = self.addTab(
                self.ppBrowser,
                UI.PixmapCache.getIcon("protobuf"), '')
            self.setTabToolTip(index, self.ppBrowser.windowTitle())
        
        if browserFlags & OthersBrowserFlag:
            index = self.addTab(
                self.poBrowser,
                UI.PixmapCache.getIcon("projectOthers"), '')
            self.setTabToolTip(index, self.poBrowser.windowTitle())
        
        QApplication.processEvents()
        
    def __currentChanged(self, index):
        """
        Private slot to handle the currentChanged(int) signal.
        
        @param index index of the tab (integer)
        """
        if index > -1:
            browser = self.widget(index)
            if browser is not None:
                browser.layoutDisplay()
        
    def __projectOpened(self):
        """
        Private slot to handle the projectOpened signal.
        """
        self.__projectPropertiesChanged()
        self.setCurrentIndex(0)
        self.__vcsStateChanged(" ")
        
    def __projectClosed(self):
        """
        Private slot to handle the projectClosed signal.
        """
        self.__projectPropertiesChanged()
        self.setCurrentIndex(0)
        self.__setSourcesIcon()
        self.__vcsStateChanged(" ")
        
    def __newProject(self):
        """
        Private slot to handle the newProject signal.
        """
        self.setCurrentIndex(0)
        self.__projectPropertiesChanged()
        
    def __projectPropertiesChanged(self):
        """
        Private slot to handle the projectPropertiesChanged signal.
        """
        if self.project.isOpen():
            flags = Preferences.getProjectBrowserFlags(
                self.project.getProjectType())
        else:
            flags = AllBrowsersFlag
        
        if flags != self.__currentBrowsersFlags:
            self.__currentBrowsersFlags = flags
            self.__setBrowsersAvailable(flags)
        
        endIndex = self.count()
        for index in range(endIndex):
            self.setTabEnabled(index, self.project.isOpen())
        
        self.__setSourcesIcon()
        
    def __setSourcesIcon(self):
        """
        Private method to set the right icon for the sources browser tab.
        """
        if not self.project.isOpen():
            icon = UI.PixmapCache.getIcon("projectSources")
        else:
            if self.project.getProjectLanguage() == "Python3":
                if self.project.isMixedLanguageProject():
                    icon = UI.PixmapCache.getIcon("projectSourcesPyMixed")
                else:
                    icon = UI.PixmapCache.getIcon("projectSourcesPy")
            elif self.project.getProjectLanguage() == "MicroPython":
                icon = UI.PixmapCache.getIcon("micropython")
            elif self.project.getProjectLanguage() == "Ruby":
                if self.project.isMixedLanguageProject():
                    icon = UI.PixmapCache.getIcon("projectSourcesRbMixed")
                else:
                    icon = UI.PixmapCache.getIcon("projectSourcesRb")
            elif self.project.getProjectLanguage() == "JavaScript":
                icon = UI.PixmapCache.getIcon("projectSourcesJavaScript")
            else:
                icon = UI.PixmapCache.getIcon("projectSources")
        self.setTabIcon(self.indexOf(self.psBrowser), icon)
        
    def handleEditorChanged(self, fn):
        """
        Public slot to handle the editorChanged signal.
        
        @param fn filename of the changed file (string)
        """
        if Preferences.getProject("FollowEditor"):
            if self.project.isProjectSource(fn):
                self.psBrowser.selectFile(fn)
            elif self.project.isProjectForm(fn):
                self.pfBrowser.selectFile(fn)
            elif self.project.isProjectInterface(fn):
                self.piBrowser.selectFile(fn)
            elif self.project.isProjectProtocol(fn):
                self.ppBrowser.selectFile(fn)
            elif self.project.isProjectProtocol(fn):
                self.ppBrowser.selectFile(fn)
    
    def handleEditorLineChanged(self, fn, lineno):
        """
        Public slot to handle the editorLineChanged signal.
        
        @param fn filename of the changed file (string)
        @param lineno one based line number of the item (integer)
        """
        if (
            Preferences.getProject("FollowEditor") and
            Preferences.getProject("FollowCursorLine")
        ):
            if self.project.isProjectSource(fn):
                self.psBrowser.selectFileLine(fn, lineno)
    
    def getProjectBrowsers(self):
        """
        Public method to get references to the individual project browsers.
        
        @return list of references to project browsers
        """
        return [self.psBrowser, self.pfBrowser, self.prBrowser,
                self.ptBrowser, self.piBrowser, self.ppBrowser,
                self.poBrowser]
    
    def getProjectBrowser(self, name):
        """
        Public method to get a reference to the named project browser.
        
        @param name name of the requested project browser (string).
            Valid names are "sources, forms, resources, translations,
            interfaces, protocols, others".
        @return reference to the requested browser or None
        """
        if name == "sources":
            return self.psBrowser
        elif name == "forms":
            return self.pfBrowser
        elif name == "resources":
            return self.prBrowser
        elif name == "translations":
            return self.ptBrowser
        elif name == "interfaces":
            return self.piBrowser
        elif name == "protocols":
            return self.ppBrowser
        elif name == "others":
            return self.poBrowser
        else:
            return None
    
    def getProjectBrowserNames(self):
        """
        Public method to get the names of the various project browsers.
        
        @return list of project browser names (list of string)
        """
        return ["sources", "forms", "resources",
                "translations", "interfaces", "protocols", "others"]
    
    def handlePreferencesChanged(self):
        """
        Public slot used to handle the preferencesChanged signal.
        """
        self.__projectPropertiesChanged()
        self.__vcsStateChanged(self.currentVcsStatus)
    
    def __vcsStateChanged(self, state):
        """
        Private slot to handle a change in the vcs state.
        
        @param state new vcs state (string)
        """
        self.currentVcsStatus = state
        if state == " " or state not in self.vcsStatusColorNames:
            self.vcsStatusIndicator.setColor(QColor(Qt.GlobalColor.lightGray))
        else:
            self.vcsStatusIndicator.setColor(
                Preferences.getProjectBrowserColour(
                    self.vcsStatusColorNames[state]))
        if state not in self.vcsStatusText:
            self.vcsStatusIndicator.setToolTip(self.tr("unknown status"))
        else:
            self.vcsStatusIndicator.setToolTip(self.vcsStatusText[state])
    
    def __vcsStatusIndicatorClicked(self, pos):
        """
        Private slot to react upon clicks on the VCS indicator LED.
        
        @param pos position of the click (QPoint)
        """
        vcs = self.project.getVcs()
        if vcs:
            if self.currentVcsStatus == " ":
                # call log browser dialog
                vcs.vcsLogBrowser(self.project.getProjectPath())
            else:
                # call status dialog
                vcs.vcsStatus(self.project.getProjectPath())
