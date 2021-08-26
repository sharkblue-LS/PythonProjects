# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the base class of the VCS project helper.
"""

import os
import shutil
import copy

from PyQt5.QtCore import pyqtSlot, QDir, QFileInfo, QObject, QCoreApplication
from PyQt5.QtWidgets import QDialog, QInputDialog, QToolBar

from E5Gui.E5Action import E5Action
from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App

import Preferences
import UI.PixmapCache
import UI.Config


class VcsProjectHelper(QObject):
    """
    Class implementing the base class of the VCS project helper.
    """
    def __init__(self, vcsObject, projectObject, parent=None, name=None):
        """
        Constructor
        
        @param vcsObject reference to the vcs object
        @param projectObject reference to the project object
        @param parent parent widget (QWidget)
        @param name name of this object (string)
        """
        super(VcsProjectHelper, self).__init__(parent)
        if name:
            self.setObjectName(name)
        
        self.vcs = vcsObject
        self.project = projectObject
        
        self.actions = []
        
        self.vcsAddAct = None
        
        self.initActions()
        
    def setObjects(self, vcsObject, projectObject):
        """
        Public method to set references to the vcs and project objects.
        
        @param vcsObject reference to the vcs object
        @param projectObject reference to the project object
        """
        self.vcs = vcsObject
        self.project = projectObject
    
    def initActions(self):
        """
        Public method to generate the action objects.
        """
        self.vcsNewAct = E5Action(
            QCoreApplication.translate(
                "VcsProjectHelper", 'New from repository'),
            UI.PixmapCache.getIcon("vcsCheckout"),
            QCoreApplication.translate(
                "VcsProjectHelper", '&New from repository...'),
            0, 0, self, 'vcs_new')
        self.vcsNewAct.setStatusTip(QCoreApplication.translate(
            "VcsProjectHelper",
            'Create a new project from the VCS repository'
        ))
        self.vcsNewAct.setWhatsThis(QCoreApplication.translate(
            "VcsProjectHelper",
            """<b>New from repository</b>"""
            """<p>This creates a new local project from the VCS"""
            """ repository.</p>"""
        ))
        self.vcsNewAct.triggered.connect(self._vcsCheckout)
        self.actions.append(self.vcsNewAct)
        
        self.vcsExportAct = E5Action(
            QCoreApplication.translate(
                "VcsProjectHelper", 'Export from repository'),
            UI.PixmapCache.getIcon("vcsExport"),
            QCoreApplication.translate(
                "VcsProjectHelper", '&Export from repository...'),
            0, 0, self, 'vcs_export')
        self.vcsExportAct.setStatusTip(QCoreApplication.translate(
            "VcsProjectHelper",
            'Export a project from the repository'
        ))
        self.vcsExportAct.setWhatsThis(QCoreApplication.translate(
            "VcsProjectHelper",
            """<b>Export from repository</b>"""
            """<p>This exports a project from the repository.</p>"""
        ))
        self.vcsExportAct.triggered.connect(self._vcsExport)
        self.actions.append(self.vcsExportAct)
        
        self.vcsAddAct = E5Action(
            QCoreApplication.translate(
                "VcsProjectHelper", 'Add to repository'),
            UI.PixmapCache.getIcon("vcsCommit"),
            QCoreApplication.translate(
                "VcsProjectHelper", '&Add to repository...'),
            0, 0, self, 'vcs_add')
        self.vcsAddAct.setStatusTip(QCoreApplication.translate(
            "VcsProjectHelper",
            'Add the local project to the VCS repository'
        ))
        self.vcsAddAct.setWhatsThis(QCoreApplication.translate(
            "VcsProjectHelper",
            """<b>Add to repository</b>"""
            """<p>This adds (imports) the local project to the VCS"""
            """ repository.</p>"""
        ))
        self.vcsAddAct.triggered.connect(self._vcsImport)
        self.actions.append(self.vcsAddAct)
    
    def initMenu(self, menu):
        """
        Public method to generate the VCS menu.
        
        @param menu reference to the menu to be populated (QMenu)
        """
        menu.clear()
        
        menu.addAction(self.vcsNewAct)
        menu.addAction(self.vcsExportAct)
        menu.addSeparator()
        menu.addAction(self.vcsAddAct)
        menu.addSeparator()

    def initToolbar(self, ui, toolbarManager):
        """
        Public slot to initialize the VCS toolbar.
        
        @param ui reference to the main window (UserInterface)
        @param toolbarManager reference to a toolbar manager object
            (E5ToolBarManager)
        @return the toolbar generated (QToolBar)
        """
        return None     # __IGNORE_WARNING_M831__
    
    def initBasicToolbar(self, ui, toolbarManager):
        """
        Public slot to initialize the basic VCS toolbar.
        
        @param ui reference to the main window (UserInterface)
        @param toolbarManager reference to a toolbar manager object
            (E5ToolBarManager)
        @return the toolbar generated (QToolBar)
        """
        tb = QToolBar(QCoreApplication.translate("VcsProjectHelper", "VCS"),
                      ui)
        tb.setIconSize(UI.Config.ToolBarIconSize)
        tb.setObjectName("VersionControlToolbar")
        tb.setToolTip(QCoreApplication.translate("VcsProjectHelper", 'VCS'))
        
        tb.addAction(self.vcsNewAct)
        tb.addAction(self.vcsExportAct)
        tb.addSeparator()
        tb.addAction(self.vcsAddAct)
        
        toolbarManager.addToolBar(tb, tb.windowTitle())
        
        return tb
    
    def showMenu(self):
        """
        Public slot called before the vcs menu is shown.
        """
        if self.vcsAddAct:
            self.vcsAddAct.setEnabled(self.project and self.project.isOpen())
    
    @pyqtSlot()
    def _vcsCheckout(self, export=False):
        """
        Protected slot used to create a local project from the repository.
        
        @param export flag indicating whether an export or a checkout
                should be performed
        """
        if not self.project or not self.project.checkDirty():
            return
        
        vcsSystemsDict = e5App().getObject(
            "PluginManager").getPluginDisplayStrings("version_control")
        if not vcsSystemsDict:
            # no version control system found
            return
        
        vcsSystemsDisplay = []
        keys = sorted(vcsSystemsDict.keys())
        for key in keys:
            vcsSystemsDisplay.append(vcsSystemsDict[key])
        vcsSelected, ok = QInputDialog.getItem(
            None,
            QCoreApplication.translate("VcsProjectHelper", "New Project"),
            QCoreApplication.translate(
                "VcsProjectHelper",
                "Select version control system for the project"),
            vcsSystemsDisplay,
            0, False)
        if not ok:
            return
        
        selectedVcsSystem = None
        for vcsSystem, vcsSystemDisplay in list(vcsSystemsDict.items()):
            if vcsSystemDisplay == vcsSelected:
                selectedVcsSystem = vcsSystem
                break
        
        if not self.project.closeProject():
            return
        
        vcs = self.project.initVCS(selectedVcsSystem)
        if vcs is not None:
            vcsdlg = vcs.vcsNewProjectOptionsDialog()
            if vcsdlg.exec() == QDialog.DialogCode.Accepted:
                projectdir, vcsDataDict = vcsdlg.getData()
                # edit VCS command options
                if vcs.vcsSupportCommandOptions():
                    vcores = E5MessageBox.yesNo(
                        self.parent(),
                        QCoreApplication.translate(
                            "VcsProjectHelper", "New Project"),
                        QCoreApplication.translate(
                            "VcsProjectHelper",
                            """Would you like to edit the VCS command"""
                            """ options?"""))
                else:
                    vcores = False
                if vcores:
                    from .CommandOptionsDialog import VcsCommandOptionsDialog
                    codlg = VcsCommandOptionsDialog(vcs)
                    if codlg.exec() == QDialog.DialogCode.Accepted:
                        vcs.vcsSetOptions(codlg.getOptions())
                
                # create the project directory if it doesn't exist already
                if not os.path.isdir(projectdir):
                    try:
                        os.makedirs(projectdir)
                    except OSError:
                        E5MessageBox.critical(
                            self.parent(),
                            QCoreApplication.translate(
                                "VcsProjectHelper",
                                "Create project directory"),
                            QCoreApplication.translate(
                                "VcsProjectHelper",
                                "<p>The project directory <b>{0}</b> could not"
                                " be created.</p>").format(projectdir))
                        self.project.resetVCS()
                        return
                
                # create the project from the VCS
                vcs.vcsSetDataFromDict(vcsDataDict)
                if export:
                    ok = vcs.vcsExport(vcsDataDict, projectdir)
                else:
                    ok = vcs.vcsCheckout(vcsDataDict, projectdir, False)
                if ok:
                    projectdir = os.path.normpath(projectdir)
                    filters = ["*.epj", "*.e4p"]
                    d = QDir(projectdir)
                    plist = d.entryInfoList(filters)
                    if len(plist):
                        if len(plist) == 1:
                            self.project.openProject(
                                plist[0].absoluteFilePath())
                        else:
                            pfilenamelist = d.entryList(filters)
                            pfilename, ok = QInputDialog.getItem(
                                None,
                                QCoreApplication.translate(
                                    "VcsProjectHelper",
                                    "New project from repository"),
                                QCoreApplication.translate(
                                    "VcsProjectHelper",
                                    "Select a project file to open."),
                                pfilenamelist, 0, False)
                            if ok:
                                self.project.openProject(
                                    QFileInfo(d, pfilename).absoluteFilePath())
                        if export:
                            self.project.pdata["VCS"] = 'None'
                            self.project.vcs = self.project.initVCS()
                            self.project.setDirty(True)
                            self.project.saveProject()
                    else:
                        res = E5MessageBox.yesNo(
                            self.parent(),
                            QCoreApplication.translate(
                                "VcsProjectHelper",
                                "New project from repository"),
                            QCoreApplication.translate(
                                "VcsProjectHelper",
                                "The project retrieved from the repository"
                                " does not contain an eric project file"
                                " (*.epj). Create it?"),
                            yesDefault=True)
                        if res:
                            self.project.ppath = projectdir
                            self.project.opened = True
                            
                            from Project.PropertiesDialog import (
                                PropertiesDialog
                            )
                            dlg = PropertiesDialog(self.project, False)
                            if dlg.exec() == QDialog.DialogCode.Accepted:
                                dlg.storeData()
                                self.project.initFileTypes()
                                self.project.pdata["VCS"] = selectedVcsSystem
                                self.project.setDirty(True)
                                if self.project.pdata["MAINSCRIPT"]:
                                    ms = os.path.join(
                                        self.project.ppath,
                                        self.project.pdata["MAINSCRIPT"])
                                    if os.path.exists(ms):
                                        self.project.appendFile(ms)
                                else:
                                    ms = ""
                                self.project.newProjectAddFiles(ms)
                                self.project.createProjectManagementDir()
                                self.project.saveProject()
                                self.project.openProject(self.project.pfile)
                                if not export:
                                    res = E5MessageBox.yesNo(
                                        self.parent(),
                                        QCoreApplication.translate(
                                            "VcsProjectHelper",
                                            "New project from repository"),
                                        QCoreApplication.translate(
                                            "VcsProjectHelper",
                                            "Shall the project file be added"
                                            " to the repository?"),
                                        yesDefault=True)
                                    if res:
                                        self.project.vcs.vcsAdd(
                                            self.project.pfile)
                else:
                    E5MessageBox.critical(
                        self.parent(),
                        QCoreApplication.translate(
                            "VcsProjectHelper", "New project from repository"),
                        QCoreApplication.translate(
                            "VcsProjectHelper",
                            """The project could not be retrieved from"""
                            """ the repository."""))
                    self.project.resetVCS()

    def _vcsExport(self):
        """
        Protected slot used to export a project from the repository.
        """
        self._vcsCheckout(True)

    def _vcsImport(self):
        """
        Protected slot used to import the local project into the repository.
        
        <b>NOTE</b>:
            This does not necessarily make the local project a vcs controlled
            project. You may have to checkout the project from the repository
            in order to accomplish that.
        """
        def revertChanges():
            """
            Local function to revert the changes made to the project object.
            """
            self.project.pdata["VCS"] = pdata_vcs
            self.project.pdata["VCSOPTIONS"] = copy.deepcopy(pdata_vcsoptions)
            self.project.pdata["VCSOTHERDATA"] = copy.deepcopy(pdata_vcsother)
            self.project.vcs = vcs
            self.project.vcsProjectHelper = vcsHelper
            self.project.vcsBasicHelper = vcs is None
            self.initMenu(self.project.vcsMenu)
            self.project.setDirty(True)
            self.project.saveProject()
        
        pdata_vcs = self.project.pdata["VCS"]
        pdata_vcsoptions = copy.deepcopy(self.project.pdata["VCSOPTIONS"])
        pdata_vcsother = copy.deepcopy(self.project.pdata["VCSOTHERDATA"])
        vcs = self.project.vcs
        vcsHelper = self.project.vcsProjectHelper
        vcsSystemsDict = e5App().getObject(
            "PluginManager").getPluginDisplayStrings("version_control")
        if not vcsSystemsDict:
            # no version control system found
            return
        
        vcsSystemsDisplay = []
        keys = sorted(list(vcsSystemsDict.keys()))
        for key in keys:
            vcsSystemsDisplay.append(vcsSystemsDict[key])
        vcsSelected, ok = QInputDialog.getItem(
            None,
            QCoreApplication.translate("VcsProjectHelper", "Import Project"),
            QCoreApplication.translate(
                "VcsProjectHelper",
                "Select version control system for the project"),
            vcsSystemsDisplay,
            0, False)
        if not ok:
            return
        
        selectedVcsSystem = None
        for vcsSystem, vcsSystemDisplay in list(vcsSystemsDict.items()):
            if vcsSystemDisplay == vcsSelected:
                selectedVcsSystem = vcsSystem
                break
        
        if selectedVcsSystem is not None:
            self.project.pdata["VCS"] = selectedVcsSystem
            self.project.vcs = self.project.initVCS(selectedVcsSystem)
            if self.project.vcs is not None:
                vcsdlg = self.project.vcs.vcsOptionsDialog(
                    self.project, self.project.name, 1)
                if vcsdlg.exec() == QDialog.DialogCode.Accepted:
                    vcsDataDict = vcsdlg.getData()
                    # edit VCS command options
                    if self.project.vcs.vcsSupportCommandOptions():
                        vcores = E5MessageBox.yesNo(
                            self.parent(),
                            QCoreApplication.translate(
                                "VcsProjectHelper", "Import Project"),
                            QCoreApplication.translate(
                                "VcsProjectHelper",
                                """Would you like to edit the VCS command"""
                                """ options?"""))
                    else:
                        vcores = False
                    if vcores:
                        from .CommandOptionsDialog import (
                            VcsCommandOptionsDialog
                        )
                        codlg = VcsCommandOptionsDialog(self.project.vcs)
                        if codlg.exec() == QDialog.DialogCode.Accepted:
                            self.project.vcs.vcsSetOptions(codlg.getOptions())
                    self.project.setDirty(True)
                    self.project.vcs.vcsSetDataFromDict(vcsDataDict)
                    self.project.saveProject()
                    isVcsControlled = self.project.vcs.vcsImport(
                        vcsDataDict, self.project.ppath)[0]
                    if isVcsControlled:
                        # reopen the project
                        self.project.openProject(self.project.pfile)
                    else:
                        # revert the changes to the local project
                        # because the project dir is not a VCS directory
                        revertChanges()
                else:
                    # revert the changes because user cancelled
                    revertChanges()

    def _vcsUpdate(self):
        """
        Protected slot used to update the local project from the repository.
        """
        if self.vcs is None:
            # just in case
            return
        
        shouldReopen = self.vcs.vcsUpdate(self.project.ppath)
        if shouldReopen:
            res = E5MessageBox.yesNo(
                self.parent(),
                QCoreApplication.translate("VcsProjectHelper", "Update"),
                QCoreApplication.translate(
                    "VcsProjectHelper",
                    """The project should be reread. Do this now?"""),
                yesDefault=True)
            if res:
                self.project.reopenProject()
        
    def _vcsCommit(self):
        """
        Protected slot used to commit changes to the local project to the
        repository.
        """
        if self.vcs is None:
            # just in case
            return
        
        if Preferences.getVCS("AutoSaveProject"):
            self.project.saveProject()
        if Preferences.getVCS("AutoSaveFiles"):
            self.project.saveAllScripts()
        self.vcs.vcsCommit(self.project.ppath, '')
        
    def _vcsRemove(self):
        """
        Protected slot used to remove the local project from the repository.
        
        Depending on the parameters set in the vcs object the project
        may be removed from the local disk as well.
        """
        if self.vcs is None:
            # just in case
            return
        
        res = E5MessageBox.yesNo(
            self.parent(),
            QCoreApplication.translate(
                "VcsProjectHelper",
                "Remove project from repository"),
            QCoreApplication.translate(
                "VcsProjectHelper",
                "Dou you really want to remove this project from"
                " the repository (and disk)?"))
        if res:
            self.vcs.vcsRemove(self.project.ppath, True)
            self._vcsCommit()
            if not os.path.exists(self.project.pfile):
                ppath = self.project.ppath
                self.setDirty(False)
                self.project.closeProject()
                shutil.rmtree(ppath, True)
        
    def _vcsCommandOptions(self):
        """
        Protected slot to edit the VCS command options.
        """
        if self.vcs is None:
            # just in case
            return
        
        if self.vcs.vcsSupportCommandOptions():
            from .CommandOptionsDialog import VcsCommandOptionsDialog
            codlg = VcsCommandOptionsDialog(self.vcs)
            if codlg.exec() == QDialog.DialogCode.Accepted:
                self.vcs.vcsSetOptions(codlg.getOptions())
                self.project.setDirty(True)
        
    def _vcsLog(self):
        """
        Protected slot used to show the log of the local project.
        """
        # kept for backward compatibility for plug-ins
        self._vcsLogBrowser()
        
    def _vcsLogBrowser(self):
        """
        Protected slot used to show the log of the local project with a
        log browser dialog.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsLogBrowser(self.project.ppath)
        
    def _vcsDiff(self):
        """
        Protected slot used to show the difference of the local project to
        the repository.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsDiff(self.project.ppath)
        
    def _vcsStatus(self):
        """
        Protected slot used to show the status of the local project.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsStatus(self.project.ppath)
        
    def _vcsTag(self):
        """
        Protected slot used to tag the local project in the repository.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsTag(self.project.ppath)
        
    def _vcsRevert(self):
        """
        Protected slot used to revert changes made to the local project.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsRevert(self.project.ppath)
        
    def _vcsSwitch(self):
        """
        Protected slot used to switch the local project to another tag/branch.
        """
        if self.vcs is None:
            # just in case
            return
        
        shouldReopen = self.vcs.vcsSwitch(self.project.ppath)
        if shouldReopen:
            res = E5MessageBox.yesNo(
                self.parent(),
                QCoreApplication.translate("VcsProjectHelper", "Switch"),
                QCoreApplication.translate(
                    "VcsProjectHelper",
                    """The project should be reread. Do this now?"""),
                yesDefault=True)
            if res:
                self.project.reopenProject()
        
    def _vcsMerge(self):
        """
        Protected slot used to merge changes of a tag/revision into the local
        project.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsMerge(self.project.ppath)
        
    def _vcsCleanup(self):
        """
        Protected slot used to cleanup the local project.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsCleanup(self.project.ppath)
        
    def _vcsCommand(self):
        """
        Protected slot used to execute an arbitrary vcs command.
        """
        if self.vcs is None:
            # just in case
            return
        
        self.vcs.vcsCommandLine(self.project.ppath)

    def _vcsInfoDisplay(self):
        """
        Protected slot called to show some vcs information.
        """
        if self.vcs is None:
            # just in case
            return
        
        from .RepositoryInfoDialog import VcsRepositoryInfoDialog
        info = self.vcs.vcsRepositoryInfos(self.project.ppath)
        dlg = VcsRepositoryInfoDialog(None, info)
        dlg.exec()
