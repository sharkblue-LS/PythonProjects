# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the VCS project browser helper for Git.
"""

import os

from PyQt5.QtWidgets import QMenu, QDialog

from E5Gui.E5Application import e5App

from Project.ProjectBrowserModel import ProjectBrowserFileItem

from VCS.ProjectBrowserHelper import VcsProjectBrowserHelper

import UI.PixmapCache


class GitProjectBrowserHelper(VcsProjectBrowserHelper):
    """
    Class implementing the VCS project browser helper for Git.
    """
    def __init__(self, vcsObject, browserObject, projectObject,
                 isTranslationsBrowser, parent=None, name=None):
        """
        Constructor
        
        @param vcsObject reference to the vcs object
        @param browserObject reference to the project browser object
        @param projectObject reference to the project object
        @param isTranslationsBrowser flag indicating, the helper is requested
            for the translations browser (this needs some special treatment)
        @param parent parent widget (QWidget)
        @param name name of this object (string)
        """
        VcsProjectBrowserHelper.__init__(self, vcsObject, browserObject,
                                         projectObject, isTranslationsBrowser,
                                         parent, name)
    
    def showContextMenu(self, menu, standardItems):
        """
        Public slot called before the context menu is shown.
        
        It enables/disables the VCS menu entries depending on the overall
        VCS status and the file status.
        
        @param menu reference to the menu to be shown
        @param standardItems array of standard items that need
            activation/deactivation depending on the overall VCS status
        """
        if self.browser.currentItem().data(1) == self.vcs.vcsName():
            for act in self.vcsMenuActions:
                act.setEnabled(True)
            for act in standardItems:
                act.setEnabled(False)
        else:
            for act in self.vcsMenuActions:
                act.setEnabled(False)
            for act in standardItems:
                act.setEnabled(True)
    
    def showContextMenuMulti(self, menu, standardItems):
        """
        Public slot called before the context menu (multiple selections) is
        shown.
        
        It enables/disables the VCS menu entries depending on the overall
        VCS status and the files status.
        
        @param menu reference to the menu to be shown
        @param standardItems array of standard items that need
            activation/deactivation depending on the overall VCS status
        """
        vcsName = self.vcs.vcsName()
        items = self.browser.getSelectedItems()
        vcsItems = 0
        # determine number of selected items under VCS control
        for itm in items:
            if itm.data(1) == vcsName:
                vcsItems += 1
        
        if vcsItems > 0:
            if vcsItems != len(items):
                for act in self.vcsMultiMenuActions:
                    act.setEnabled(False)
            else:
                for act in self.vcsMultiMenuActions:
                    act.setEnabled(True)
            for act in standardItems:
                act.setEnabled(False)
        else:
            for act in self.vcsMultiMenuActions:
                act.setEnabled(False)
            for act in standardItems:
                act.setEnabled(True)
    
    def showContextMenuDir(self, menu, standardItems):
        """
        Public slot called before the context menu is shown.
        
        It enables/disables the VCS menu entries depending on the overall
        VCS status and the directory status.
        
        @param menu reference to the menu to be shown
        @param standardItems array of standard items that need
            activation/deactivation depending on the overall VCS status
        """
        if self.browser.currentItem().data(1) == self.vcs.vcsName():
            for act in self.vcsDirMenuActions:
                act.setEnabled(True)
            for act in standardItems:
                act.setEnabled(False)
        else:
            for act in self.vcsDirMenuActions:
                act.setEnabled(False)
            for act in standardItems:
                act.setEnabled(True)
    
    def showContextMenuDirMulti(self, menu, standardItems):
        """
        Public slot called before the context menu is shown.
        
        It enables/disables the VCS menu entries depending on the overall
        VCS status and the directory status.
        
        @param menu reference to the menu to be shown
        @param standardItems array of standard items that need
            activation/deactivation depending on the overall VCS status
        """
        vcsName = self.vcs.vcsName()
        items = self.browser.getSelectedItems()
        vcsItems = 0
        # determine number of selected items under VCS control
        for itm in items:
            if itm.data(1) == vcsName:
                vcsItems += 1
        
        if vcsItems > 0:
            if vcsItems != len(items):
                for act in self.vcsDirMultiMenuActions:
                    act.setEnabled(False)
            else:
                for act in self.vcsDirMultiMenuActions:
                    act.setEnabled(True)
            for act in standardItems:
                act.setEnabled(False)
        else:
            for act in self.vcsDirMultiMenuActions:
                act.setEnabled(False)
            for act in standardItems:
                act.setEnabled(True)
    
    ###########################################################################
    ## Protected menu generation methods below
    ###########################################################################
    
    def _addVCSMenu(self, mainMenu):
        """
        Protected method used to add the VCS menu to all project browsers.
        
        @param mainMenu reference to the menu to be amended
        """
        self.vcsMenuActions = []
        self.vcsAddMenuActions = []
        
        menu = QMenu(self.tr("Version Control"))
        
        act = menu.addAction(
            UI.PixmapCache.getIcon(
                os.path.join("VcsPlugins", "vcsGit", "icons", "git.svg")),
            self.vcs.vcsName(), self._VCSInfoDisplay)
        font = act.font()
        font.setBold(True)
        act.setFont(font)
        menu.addSeparator()
        
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsCommit"),
            self.tr('Commit changes to repository...'),
            self._VCSCommit)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsAdd"),
            self.tr('Add/Stage to repository'),
            self._VCSAdd)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Unstage changes'),
            self.__GitUnstage)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRemove"),
            self.tr('Remove from repository (and disk)'),
            self._VCSRemove)
        self.vcsMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRemove"),
            self.tr('Remove from repository only'),
            self.__GitForget)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(self.tr('Copy'), self.__GitCopy)
        self.vcsMenuActions.append(act)
        act = menu.addAction(self.tr('Move'), self.__GitMove)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsLog"),
            self.tr('Show log browser'), self._VCSLogBrowser)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsStatus"),
            self.tr('Show status'), self._VCSStatus)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences'), self._VCSDiff)
        self.vcsMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsSbsDiff"),
            self.tr('Show differences side-by-side'), self.__GitSbsDiff)
        self.vcsMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences (extended)'),
            self.__GitExtendedDiff)
        self.vcsMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsSbsDiff"),
            self.tr('Show differences side-by-side (extended)'),
            self.__GitSbsExtendedDiff)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        self.annotateAct = menu.addAction(
            self.tr('Show annotated file'),
            self.__GitBlame)
        self.vcsMenuActions.append(self.annotateAct)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Revert changes'), self.__GitRevert)
        self.vcsMenuActions.append(act)
        menu.addSeparator()
        menu.addAction(self.tr('Select all local file entries'),
                       self.browser.selectLocalEntries)
        menu.addAction(self.tr('Select all versioned file entries'),
                       self.browser.selectVCSEntries)
        menu.addAction(self.tr('Select all local directory entries'),
                       self.browser.selectLocalDirEntries)
        menu.addAction(self.tr('Select all versioned directory entries'),
                       self.browser.selectVCSDirEntries)
        menu.addSeparator()
        menu.addAction(self.tr("Configure..."), self.__GitConfigure)
        
        mainMenu.addSeparator()
        mainMenu.addMenu(menu)
        self.menu = menu
    
    def _addVCSMenuMulti(self, mainMenu):
        """
        Protected method used to add the VCS menu for multi selection to all
        project browsers.
        
        @param mainMenu reference to the menu to be amended
        """
        self.vcsMultiMenuActions = []
        
        menu = QMenu(self.tr("Version Control"))
        
        act = menu.addAction(
            UI.PixmapCache.getIcon(
                os.path.join("VcsPlugins", "vcsGit", "icons", "git.svg")),
            self.vcs.vcsName(), self._VCSInfoDisplay)
        font = act.font()
        font.setBold(True)
        act.setFont(font)
        menu.addSeparator()
        
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsCommit"),
            self.tr('Commit changes to repository...'),
            self._VCSCommit)
        self.vcsMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsAdd"),
            self.tr('Add/Stage to repository'), self._VCSAdd)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Unstage changes'),
            self.__GitUnstage)
        self.vcsMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRemove"),
            self.tr('Remove from repository (and disk)'),
            self._VCSRemove)
        self.vcsMultiMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRemove"),
            self.tr('Remove from repository only'),
            self.__GitForget)
        self.vcsMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsStatus"),
            self.tr('Show status'), self._VCSStatus)
        self.vcsMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences'), self._VCSDiff)
        self.vcsMultiMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences (extended)'),
            self.__GitExtendedDiff)
        self.vcsMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Revert changes'), self.__GitRevert)
        self.vcsMultiMenuActions.append(act)
        menu.addSeparator()
        
        menu.addSeparator()
        menu.addAction(self.tr('Select all local file entries'),
                       self.browser.selectLocalEntries)
        menu.addAction(self.tr('Select all versioned file entries'),
                       self.browser.selectVCSEntries)
        menu.addAction(self.tr('Select all local directory entries'),
                       self.browser.selectLocalDirEntries)
        menu.addAction(self.tr('Select all versioned directory entries'),
                       self.browser.selectVCSDirEntries)
        menu.addSeparator()
        menu.addAction(self.tr("Configure..."), self.__GitConfigure)
        
        mainMenu.addSeparator()
        mainMenu.addMenu(menu)
        self.menuMulti = menu
    
    def _addVCSMenuBack(self, mainMenu):
        """
        Protected method used to add the VCS menu to all project browsers.
        
        @param mainMenu reference to the menu to be amended
        """
        menu = QMenu(self.tr("Version Control"))
        
        act = menu.addAction(
            UI.PixmapCache.getIcon(
                os.path.join("VcsPlugins", "vcsGit", "icons", "git.svg")),
            self.vcs.vcsName(), self._VCSInfoDisplay)
        font = act.font()
        font.setBold(True)
        act.setFont(font)
        menu.addSeparator()
        
        menu.addAction(self.tr('Select all local file entries'),
                       self.browser.selectLocalEntries)
        menu.addAction(self.tr('Select all versioned file entries'),
                       self.browser.selectVCSEntries)
        menu.addAction(self.tr('Select all local directory entries'),
                       self.browser.selectLocalDirEntries)
        menu.addAction(self.tr('Select all versioned directory entries'),
                       self.browser.selectVCSDirEntries)
        menu.addSeparator()
        menu.addAction(self.tr("Configure..."), self.__GitConfigure)
        
        mainMenu.addSeparator()
        mainMenu.addMenu(menu)
        self.menuBack = menu
    
    def _addVCSMenuDir(self, mainMenu):
        """
        Protected method used to add the VCS menu to all project browsers.
        
        @param mainMenu reference to the menu to be amended
        """
        if mainMenu is None:
            return
        
        self.vcsDirMenuActions = []
        self.vcsAddDirMenuActions = []
        
        menu = QMenu(self.tr("Version Control"))
        
        act = menu.addAction(
            UI.PixmapCache.getIcon(
                os.path.join("VcsPlugins", "vcsGit", "icons", "git.svg")),
            self.vcs.vcsName(), self._VCSInfoDisplay)
        font = act.font()
        font.setBold(True)
        act.setFont(font)
        menu.addSeparator()
        
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsCommit"),
            self.tr('Commit changes to repository...'),
            self._VCSCommit)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsAdd"),
            self.tr('Add/Stage to repository'), self._VCSAdd)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Unstage changes'),
            self.__GitUnstage)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRemove"),
            self.tr('Remove from repository (and disk)'),
            self._VCSRemove)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(self.tr('Copy'), self.__GitCopy)
        self.vcsDirMenuActions.append(act)
        act = menu.addAction(self.tr('Move'), self.__GitMove)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsLog"),
            self.tr('Show log browser'), self._VCSLogBrowser)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsStatus"),
            self.tr('Show status'), self._VCSStatus)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences'), self._VCSDiff)
        self.vcsDirMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences (extended)'),
            self.__GitExtendedDiff)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Revert changes'), self.__GitRevert)
        self.vcsDirMenuActions.append(act)
        menu.addSeparator()
        
        menu.addSeparator()
        menu.addAction(self.tr('Select all local file entries'),
                       self.browser.selectLocalEntries)
        menu.addAction(self.tr('Select all versioned file entries'),
                       self.browser.selectVCSEntries)
        menu.addAction(self.tr('Select all local directory entries'),
                       self.browser.selectLocalDirEntries)
        menu.addAction(self.tr('Select all versioned directory entries'),
                       self.browser.selectVCSDirEntries)
        menu.addSeparator()
        menu.addAction(self.tr("Configure..."), self.__GitConfigure)
        
        mainMenu.addSeparator()
        mainMenu.addMenu(menu)
        self.menuDir = menu
    
    def _addVCSMenuDirMulti(self, mainMenu):
        """
        Protected method used to add the VCS menu to all project browsers.
        
        @param mainMenu reference to the menu to be amended
        """
        if mainMenu is None:
            return
        
        self.vcsDirMultiMenuActions = []
        
        menu = QMenu(self.tr("Version Control"))
        
        act = menu.addAction(
            UI.PixmapCache.getIcon(
                os.path.join("VcsPlugins", "vcsGit", "icons", "git.svg")),
            self.vcs.vcsName(), self._VCSInfoDisplay)
        font = act.font()
        font.setBold(True)
        act.setFont(font)
        menu.addSeparator()
        
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsCommit"),
            self.tr('Commit changes to repository...'),
            self._VCSCommit)
        self.vcsDirMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsAdd"),
            self.tr('Add/Stage to repository'), self._VCSAdd)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Unstage changes'),
            self.__GitUnstage)
        self.vcsDirMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRemove"),
            self.tr('Remove from repository (and disk)'),
            self._VCSRemove)
        self.vcsDirMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsStatus"),
            self.tr('Show status'), self._VCSStatus)
        self.vcsDirMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences'), self._VCSDiff)
        self.vcsDirMultiMenuActions.append(act)
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsDiff"),
            self.tr('Show differences (extended)'),
            self.__GitExtendedDiff)
        self.vcsDirMultiMenuActions.append(act)
        menu.addSeparator()
        act = menu.addAction(
            UI.PixmapCache.getIcon("vcsRevert"),
            self.tr('Revert changes'), self.__GitRevert)
        self.vcsDirMultiMenuActions.append(act)
        menu.addSeparator()
        
        menu.addSeparator()
        menu.addAction(self.tr('Select all local file entries'),
                       self.browser.selectLocalEntries)
        menu.addAction(self.tr('Select all versioned file entries'),
                       self.browser.selectVCSEntries)
        menu.addAction(self.tr('Select all local directory entries'),
                       self.browser.selectLocalDirEntries)
        menu.addAction(self.tr('Select all versioned directory entries'),
                       self.browser.selectVCSDirEntries)
        menu.addSeparator()
        menu.addAction(self.tr("Configure..."), self.__GitConfigure)
        
        mainMenu.addSeparator()
        mainMenu.addMenu(menu)
        self.menuDirMulti = menu
    
    def __GitConfigure(self):
        """
        Private method to open the configuration dialog.
        """
        e5App().getObject("UserInterface").showPreferences("zzz_gitPage")
    
    def __GitForget(self):
        """
        Private slot called by the context menu to remove the selected file
        from the Git repository leaving a copy in the project directory.
        """
        from UI.DeleteFilesConfirmationDialog import (
            DeleteFilesConfirmationDialog
        )
        if self.isTranslationsBrowser:
            items = self.browser.getSelectedItems([ProjectBrowserFileItem])
            names = [itm.fileName() for itm in items]
            
            dlg = DeleteFilesConfirmationDialog(
                self.parent(),
                self.tr("Remove from repository only"),
                self.tr(
                    "Do you really want to remove these files"
                    " from the repository?"),
                names)
        else:
            items = self.browser.getSelectedItems()
            names = [itm.fileName() for itm in items]
            files = [self.browser.project.getRelativePath(name)
                     for name in names]
            
            dlg = DeleteFilesConfirmationDialog(
                self.parent(),
                self.tr("Remove from repository only"),
                self.tr(
                    "Do you really want to remove these files"
                    " from the repository?"),
                files)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.vcs.vcsRemove(names, stageOnly=True)
        
        for fn in names:
            self._updateVCSStatus(fn)
    
    def __GitCopy(self):
        """
        Private slot called by the context menu to copy the selected file.
        """
        itm = self.browser.currentItem()
        try:
            fn = itm.fileName()
        except AttributeError:
            fn = itm.dirName()
        self.vcs.gitCopy(fn, self.project)
    
    def __GitMove(self):
        """
        Private slot called by the context menu to move the selected file.
        """
        itm = self.browser.currentItem()
        try:
            fn = itm.fileName()
        except AttributeError:
            fn = itm.dirName()
        isFile = os.path.isfile(fn)
        movefiles = self.browser.project.getFiles(fn)
        self.browser.project.stopFileSystemMonitoring()
        if self.vcs.vcsMove(fn, self.project):
            if isFile:
                self.browser.closeSourceWindow.emit(fn)
            else:
                for mf in movefiles:
                    self.browser.closeSourceWindow.emit(mf)
        self.browser.project.startFileSystemMonitoring()
    
    def __GitExtendedDiff(self):
        """
        Private slot called by the context menu to show the difference of a
        file to the repository.
        
        This gives the chance to enter the revisions to compare.
        """
        names = []
        for itm in self.browser.getSelectedItems():
            try:
                names.append(itm.fileName())
            except AttributeError:
                names.append(itm.dirName())
        self.vcs.gitExtendedDiff(names)
    
    def __GitSbsDiff(self):
        """
        Private slot called by the context menu to show the difference of a
        file to the repository side-by-side.
        """
        itm = self.browser.currentItem()
        fn = itm.fileName()
        self.vcs.gitSbsDiff(fn)
    
    def __GitSbsExtendedDiff(self):
        """
        Private slot called by the context menu to show the difference of a
        file to the repository side-by-side.
       
        It allows the selection of revisions to compare.
        """
        itm = self.browser.currentItem()
        fn = itm.fileName()
        self.vcs.gitSbsDiff(fn, extended=True)
    
    def __GitUnstage(self):
        """
        Private slot to unstage changes.
        """
        names = []
        for itm in self.browser.getSelectedItems():
            try:
                name = itm.fileName()
            except AttributeError:
                name = itm.dirName()
            names.append(name)
        self.vcs.gitUnstage(names)
    
    def __GitRevert(self):
        """
        Private slot to revert changes of the working area.
        """
        names = []
        for itm in self.browser.getSelectedItems():
            try:
                name = itm.fileName()
            except AttributeError:
                name = itm.dirName()
            names.append(name)
        self.vcs.gitRevert(names)
    
    def __GitBlame(self):
        """
        Private slot called by the context menu to show the annotations of a
        file.
        """
        itm = self.browser.currentItem()
        fn = itm.fileName()
        self.vcs.gitBlame(fn)
