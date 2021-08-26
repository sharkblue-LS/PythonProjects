# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Project Browser configuration page.
"""

from PyQt5.QtCore import pyqtSlot

from E5Gui.E5Application import e5App

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_ProjectBrowserPage import Ui_ProjectBrowserPage

import Preferences


class ProjectBrowserPage(ConfigurationPageBase, Ui_ProjectBrowserPage):
    """
    Class implementing the Project Browser configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(ProjectBrowserPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("ProjectBrowserPage")
        
        self.__currentProjectTypeIndex = 0
        
        # set initial values
        self.projectTypeCombo.addItem('', '')
        self.__projectBrowserFlags = {'': 0}
        try:
            projectTypes = e5App().getObject("Project").getProjectTypes()
            for projectType in sorted(projectTypes.keys()):
                self.projectTypeCombo.addItem(projectTypes[projectType],
                                              projectType)
                self.__projectBrowserFlags[projectType] = (
                    Preferences.getProjectBrowserFlags(projectType)
                )
        except KeyError:
            self.pbGroup.setEnabled(False)
        
        self.initColour(
            "Highlighted", self.pbHighlightedButton,
            Preferences.getProjectBrowserColour)
        
        self.followEditorCheckBox.setChecked(
            Preferences.getProject("FollowEditor"))
        self.followCursorLineCheckBox.setChecked(
            Preferences.getProject("FollowCursorLine"))
        self.autoPopulateCheckBox.setChecked(
            Preferences.getProject("AutoPopulateItems"))
        self.hideGeneratedCheckBox.setChecked(
            Preferences.getProject("HideGeneratedForms"))
        self.showHiddenCheckBox.setChecked(
            Preferences.getProject("BrowsersListHiddenFiles"))
        
    def save(self):
        """
        Public slot to save the Project Browser configuration.
        """
        self.saveColours(Preferences.setProjectBrowserColour)
        
        Preferences.setProject(
            "FollowEditor",
            self.followEditorCheckBox.isChecked())
        Preferences.setProject(
            "FollowCursorLine",
            self.followCursorLineCheckBox.isChecked())
        Preferences.setProject(
            "AutoPopulateItems",
            self.autoPopulateCheckBox.isChecked())
        Preferences.setProject(
            "HideGeneratedForms",
            self.hideGeneratedCheckBox.isChecked())
        Preferences.setProject(
            "BrowsersListHiddenFiles",
            self.showHiddenCheckBox.isChecked())
        
        if self.pbGroup.isEnabled():
            self.__storeProjectBrowserFlags(
                self.projectTypeCombo.itemData(self.__currentProjectTypeIndex))
            for projectType, flags in list(self.__projectBrowserFlags.items()):
                if projectType != '':
                    Preferences.setProjectBrowserFlags(projectType, flags)
        
    def __storeProjectBrowserFlags(self, projectType):
        """
        Private method to store the flags for the selected project type.
        
        @param projectType type of the selected project (string)
        """
        from Project.ProjectBrowserFlags import (
            SourcesBrowserFlag, FormsBrowserFlag, ResourcesBrowserFlag,
            TranslationsBrowserFlag, InterfacesBrowserFlag, OthersBrowserFlag,
            ProtocolsBrowserFlag
        )
        
        flags = 0
        if self.sourcesBrowserCheckBox.isChecked():
            flags |= SourcesBrowserFlag
        if self.formsBrowserCheckBox.isChecked():
            flags |= FormsBrowserFlag
        if (
            self.resourcesBrowserCheckBox.isChecked() and
            projectType not in ("PyQt6", "PyQt6C")
        ):
            flags |= ResourcesBrowserFlag
        if self.translationsBrowserCheckBox.isChecked():
            flags |= TranslationsBrowserFlag
        if self.interfacesBrowserCheckBox.isChecked():
            flags |= InterfacesBrowserFlag
        if self.othersBrowserCheckBox.isChecked():
            flags |= OthersBrowserFlag
        if self.protocolsBrowserCheckBox.isChecked():
            flags |= ProtocolsBrowserFlag
        
        self.__projectBrowserFlags[projectType] = flags
    
    def __setProjectBrowsersCheckBoxes(self, projectType):
        """
        Private method to set the checkboxes according to the selected project
        type.
        
        @param projectType type of the selected project (string)
        """
        from Project.ProjectBrowserFlags import (
            SourcesBrowserFlag, FormsBrowserFlag, ResourcesBrowserFlag,
            TranslationsBrowserFlag, InterfacesBrowserFlag, OthersBrowserFlag,
            ProtocolsBrowserFlag
        )
        
        flags = self.__projectBrowserFlags[projectType]
        
        self.sourcesBrowserCheckBox.setChecked(flags & SourcesBrowserFlag)
        self.formsBrowserCheckBox.setChecked(flags & FormsBrowserFlag)
        self.resourcesBrowserCheckBox.setEnabled(
            projectType not in ("PyQt6", "PyQt6C"))
        if projectType in ("PyQt6", "PyQt6C"):
            self.resourcesBrowserCheckBox.setChecked(False)
        else:
            self.resourcesBrowserCheckBox.setChecked(
                flags & ResourcesBrowserFlag)
        self.translationsBrowserCheckBox.setChecked(
            flags & TranslationsBrowserFlag)
        self.interfacesBrowserCheckBox.setChecked(
            flags & InterfacesBrowserFlag)
        self.othersBrowserCheckBox.setChecked(flags & OthersBrowserFlag)
        self.protocolsBrowserCheckBox.setChecked(flags & ProtocolsBrowserFlag)
    
    @pyqtSlot(int)
    def on_projectTypeCombo_activated(self, index):
        """
        Private slot to set the browser checkboxes according to the selected
        project type.
        
        @param index index of the selected project type (integer)
        """
        if self.__currentProjectTypeIndex == index:
            return
        
        self.__storeProjectBrowserFlags(
            self.projectTypeCombo.itemData(self.__currentProjectTypeIndex))
        self.__setProjectBrowsersCheckBoxes(
            self.projectTypeCombo.itemData(index))
        self.__currentProjectTypeIndex = index
    
    @pyqtSlot(bool)
    def on_followEditorCheckBox_toggled(self, checked):
        """
        Private slot to handle the change of the 'Follow Editor' checkbox.
        
        @param checked flag indicating the state of the checkbox
        """
        if not checked:
            self.followCursorLineCheckBox.setChecked(False)
    
    @pyqtSlot(bool)
    def on_followCursorLineCheckBox_toggled(self, checked):
        """
        Private slot to handle the change of the 'Follow Cursor Line' checkbox.
        
        @param checked flag indicating the state of the checkbox
        """
        if checked:
            self.followEditorCheckBox.setChecked(True)
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = ProjectBrowserPage()
    return page
