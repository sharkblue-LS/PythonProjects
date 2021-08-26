# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the multi project management functionality.
"""

import os
import shutil

from PyQt5.QtCore import (
    pyqtSignal, pyqtSlot, QFileInfo, QFile, QIODevice, QObject, QUuid
)
from PyQt5.QtWidgets import QMenu, QApplication, QDialog, QToolBar

from Globals import recentNameMultiProject

from E5Gui.E5Action import E5Action, createActionGroup
from E5Gui import E5FileDialog, E5MessageBox, E5PathPickerDialog
from E5Gui.E5PathPickerDialog import E5PathPickerModes
from E5Gui.E5OverrideCursor import E5OverrideCursor

import UI.PixmapCache

import Preferences
import Utilities

from .MultiProjectFile import MultiProjectFile


class MultiProject(QObject):
    """
    Class implementing the project management functionality.
    
    @signal dirty(bool) emitted when the dirty state changes
    @signal newMultiProject() emitted after a new multi project was generated
    @signal multiProjectOpened() emitted after a multi project file was read
    @signal multiProjectClosed() emitted after a multi project was closed
    @signal multiProjectPropertiesChanged() emitted after the multi project
            properties were changed
    @signal showMenu(string, QMenu) emitted when a menu is about to be shown.
            The name of the menu and a reference to the menu are given.
    @signal projectDataChanged(project data dict) emitted after a project entry
            has been changed
    @signal projectAdded(project data dict) emitted after a project entry
            has been added
    @signal projectRemoved(project data dict) emitted after a project entry
            has been removed
    @signal projectOpened(filename) emitted after the project has been opened
    """
    dirty = pyqtSignal(bool)
    newMultiProject = pyqtSignal()
    multiProjectOpened = pyqtSignal()
    multiProjectClosed = pyqtSignal()
    multiProjectPropertiesChanged = pyqtSignal()
    showMenu = pyqtSignal(str, QMenu)
    projectDataChanged = pyqtSignal(dict)
    projectAdded = pyqtSignal(dict)
    projectRemoved = pyqtSignal(dict)
    projectOpened = pyqtSignal(str)
    
    def __init__(self, project, parent=None, filename=None):
        """
        Constructor
        
        @param project reference to the project object (Project.Project)
        @param parent parent widget (usually the ui object) (QWidget)
        @param filename optional filename of a multi project file to open
            (string)
        """
        super(MultiProject, self).__init__(parent)
        
        self.ui = parent
        self.projectObject = project
        
        self.__initData()
        
        self.__multiProjectFile = MultiProjectFile(self)
        
        self.recent = []
        self.__loadRecent()
        
        if filename is not None:
            self.openMultiProject(filename)
    
    def __initData(self):
        """
        Private method to initialize the multi project data part.
        """
        self.loaded = False     # flag for the loaded status
        self.__dirty = False      # dirty flag
        self.pfile = ""         # name of the multi project file
        self.ppath = ""         # name of the multi project directory
        self.description = ""   # description of the multi project
        self.name = ""
        self.opened = False
        self.__projects = {}
        # dict of project info keyed by 'uid'; each info entry is a dictionary
        # 'name'        : name of the project
        # 'file'        : project file name
        # 'master'      : flag indicating the master
        #                 project
        # 'description' : description of the project
        # 'category'    : name of the group
        # 'uid'         : unique identifier
        self.categories = []
    
    def __loadRecent(self):
        """
        Private method to load the recently opened multi project filenames.
        """
        self.recent = []
        Preferences.Prefs.rsettings.sync()
        rp = Preferences.Prefs.rsettings.value(recentNameMultiProject)
        if rp is not None:
            for f in rp:
                if QFileInfo(f).exists():
                    self.recent.append(f)
    
    def __saveRecent(self):
        """
        Private method to save the list of recently opened filenames.
        """
        Preferences.Prefs.rsettings.setValue(
            recentNameMultiProject, self.recent)
        Preferences.Prefs.rsettings.sync()
    
    def getMostRecent(self):
        """
        Public method to get the most recently opened multiproject.
        
        @return path of the most recently opened multiproject (string)
        """
        if len(self.recent):
            return self.recent[0]
        else:
            return None
        
    def setDirty(self, b):
        """
        Public method to set the dirty state.
        
        It emits the signal dirty(int).
        
        @param b dirty state (boolean)
        """
        self.__dirty = b
        self.saveAct.setEnabled(b)
        self.dirty.emit(bool(b))
    
    def isDirty(self):
        """
        Public method to return the dirty state.
        
        @return dirty state (boolean)
        """
        return self.__dirty
    
    def isOpen(self):
        """
        Public method to return the opened state.
        
        @return open state (boolean)
        """
        return self.opened
    
    def getMultiProjectPath(self):
        """
        Public method to get the multi project path.
        
        @return multi project path (string)
        """
        return self.ppath
    
    def getMultiProjectFile(self):
        """
        Public method to get the path of the multi project file.
        
        @return path of the multi project file (string)
        """
        return self.pfile
    
    def __checkFilesExist(self):
        """
        Private method to check, if the files in a list exist.
        
        The project files are checked for existance in the
        filesystem. Non existant projects are removed from the list and the
        dirty state of the multi project is changed accordingly.
        """
        removelist = []
        for key, project in self.__projects.items():
            if not os.path.exists(project['file']):
                removelist.append(key)
        
        if removelist:
            for key in removelist:
                del self.__projects[key]
            self.setDirty(True)
    
    def __extractCategories(self):
        """
        Private slot to extract the categories used in the project definitions.
        """
        for project in self.__projects.values():
            if (
                project['category'] and
                project['category'] not in self.categories
            ):
                self.categories.append(project['category'])
    
    def getCategories(self):
        """
        Public method to get the list of defined categories.
        
        @return list of categories (list of string)
        """
        return [c for c in self.categories if c]
    
    def __readMultiProject(self, fn):
        """
        Private method to read in a multi project (.emj, .e4m, .e5m) file.
        
        @param fn filename of the multi project file to be read (string)
        @return flag indicating success
        """
        if os.path.splitext(fn)[1] == ".emj":
            # new JSON based format
            with E5OverrideCursor():
                res = self.__multiProjectFile.readFile(fn)
        else:
            # old XML based format
            f = QFile(fn)
            if f.open(QIODevice.OpenModeFlag.ReadOnly):
                with E5OverrideCursor():
                    from E5XML.MultiProjectReader import MultiProjectReader
                    reader = MultiProjectReader(f, self)
                    reader.readXML()
                    f.close()
                res = not reader.hasError()
            else:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Read Multi Project File"),
                    self.tr(
                        "<p>The multi project file <b>{0}</b> could not be"
                        " read.</p>").format(fn))
                res = False
        
        if res:
            self.pfile = os.path.abspath(fn)
            self.ppath = os.path.abspath(os.path.dirname(fn))
            
            self.__extractCategories()
            
            # insert filename into list of recently opened multi projects
            self.__syncRecent()
            
            self.name = os.path.splitext(os.path.basename(fn))[0]
            
            # check, if the files of the multi project still exist
            self.__checkFilesExist()
        
        return res

    def __writeMultiProject(self, fn=None):
        """
        Private method to save the multi project infos to a multi project file.
        
        @param fn optional filename of the multi project file to be written.
            If fn is None, the filename stored in the multi project object
            is used. This is the 'save' action. If fn is given, this filename
            is used instead of the one in the multi project object. This is the
            'save as' action.
        @return flag indicating success
        """
        if fn is None:
            fn = self.pfile
        
        if os.path.splitext(fn)[1] == ".emj":
            # new JSON based format
            res = self.__multiProjectFile.writeFile(fn)
        else:
            # old XML based format
            f = QFile(fn)
            if f.open(QIODevice.OpenModeFlag.WriteOnly):
                from E5XML.MultiProjectWriter import MultiProjectWriter
                MultiProjectWriter(
                    f,
                    self, os.path.splitext(os.path.basename(fn))[0]
                ).writeXML()
                res = True
            else:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Save Multi Project File"),
                    self.tr(
                        "<p>The multi project file <b>{0}</b> could not be "
                        "written.</p>").format(fn))
                res = False
        
        if res:
            self.pfile = os.path.abspath(fn)
            self.ppath = os.path.abspath(os.path.dirname(fn))
            self.name = os.path.splitext(os.path.basename(fn))[0]
            self.setDirty(False)
            
            # insert filename into list of recently opened projects
            self.__syncRecent()
        
        return res
    
    def addProject(self, project):
        """
        Public method to add a project to the multi-project.
        
        @param project dictionary containing the project data to be added
        @type dict
        """
        self.__projects[project['uid']] = project
    
    @pyqtSlot()
    def addNewProject(self, startdir="", category=""):
        """
        Public slot used to add a new project to the multi-project.
        
        @param startdir start directory for the selection dialog
        @type str
        @param category category to be preset
        @type str
        """
        from .AddProjectDialog import AddProjectDialog
        if not startdir:
            startdir = self.ppath
        if not startdir:
            startdir = Preferences.getMultiProject("Workspace")
        dlg = AddProjectDialog(self.ui, startdir=startdir,
                               categories=self.categories, category=category)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, filename, isMaster, description, category, uid = (
                dlg.getData()
            )
            
            # step 1: check, if project was already added
            for project in self.__projects.values():
                if project['file'] == filename:
                    return
            
            # step 2: check, if master should be changed
            if isMaster:
                for project in self.__projects.values():
                    if project['master']:
                        project['master'] = False
                        self.projectDataChanged.emit(project)
                        self.setDirty(True)
                        break
            
            # step 3: add the project entry
            project = {
                'name': name,
                'file': filename,
                'master': isMaster,
                'description': description,
                'category': category,
                'uid': uid,
            }
            self.__projects[uid] = project
            if category not in self.categories:
                self.categories.append(category)
            self.projectAdded.emit(project)
            self.setDirty(True)
    
    def copyProject(self, uid):
        """
        Public method to copy the project with given UID on disk.
        
        @param uid UID of the project to copy
        @type str
        """
        if uid in self.__projects:
            startdir = self.ppath
            if not startdir:
                startdir = Preferences.getMultiProject("Workspace")
            srcProject = self.__projects[uid]
            srcProjectDirectory = os.path.dirname(srcProject["file"])
            dstProjectDirectory, ok = E5PathPickerDialog.getPath(
                self.parent(),
                self.tr("Copy Project"),
                self.tr("Enter directory for the new project (must not exist"
                        " already):"),
                mode=E5PathPickerModes.DirectoryMode,
                path=srcProjectDirectory,
                defaultDirectory=startdir,
            )
            if (
                ok and
                dstProjectDirectory and
                not os.path.exists(dstProjectDirectory)
            ):
                try:
                    shutil.copytree(srcProjectDirectory, dstProjectDirectory)
                except shutil.Error:
                    E5MessageBox.critical(
                        self.parent(),
                        self.tr("Copy Project"),
                        self.tr("<p>The source project <b>{0}</b> could not"
                                " be copied to its destination <b>{1}</b>."
                                "</p>").format(srcProjectDirectory,
                                               dstProjectDirectory))
                    return
                
                dstUid = QUuid.createUuid().toString()
                dstProject = {
                    'name': self.tr("{0} - Copy").format(srcProject["name"]),
                    'file': os.path.join(dstProjectDirectory,
                                         os.path.basename(srcProject["file"])),
                    'master': False,
                    'description': srcProject["description"],
                    'category': srcProject["category"],
                    'uid': dstUid,
                }
                self.__projects[dstUid] = dstProject
                self.projectAdded.emit(dstProject)
                self.setDirty(True)
    
    def changeProjectProperties(self, pro):
        """
        Public method to change the data of a project entry.
        
        @param pro dictionary with the project data (string)
        """
        # step 1: check, if master should be changed
        if pro['master']:
            for project in self.__projects.values():
                if project['master']:
                    if project['uid'] != pro['uid']:
                        project['master'] = False
                        self.projectDataChanged.emit(project)
                        self.setDirty(True)
                    break
        
        # step 2: change the entry
        project = self.__projects[pro['uid']]
        # project UID is not changeable via interface
        project['file'] = pro['file']
        project['name'] = pro['name']
        project['master'] = pro['master']
        project['description'] = pro['description']
        project['category'] = pro['category']
        if project['category'] not in self.categories:
            self.categories.append(project['category'])
        self.projectDataChanged.emit(project)
        self.setDirty(True)
    
    def getProjects(self):
        """
        Public method to get all project entries.
        
        @return list of all project entries (list of dictionaries)
        """
        return self.__projects.values()
    
    def getProject(self, uid):
        """
        Public method to get a reference to a project entry.
        
        @param uid UID of the project to get
        @type str
        @return dictionary containing the project data
        @rtype dict
        """
        if uid in self.__projects:
            return self.__projects[uid]
        else:
            return None
    
    def removeProject(self, uid):
        """
        Public slot to remove a project from the multi project.
        
        @param uid UID of the project to be removed from the multi
            project
        @type str
        """
        if uid in self.__projects:
            project = self.__projects[uid]
            del self.__projects[uid]
            self.projectRemoved.emit(project)
            self.setDirty(True)
    
    def deleteProject(self, uid):
        """
        Public slot to delete project(s) from the multi project and disk.
        
        @param uid UID of the project to be removed from the multi
            project
        @type str
        """
        if uid in self.__projects:
            project = self.__projects[uid]
            projectPath = os.path.dirname(project["file"])
            shutil.rmtree(projectPath, True)
            
            self.removeProject(uid)
    
    def __newMultiProject(self):
        """
        Private slot to build a new multi project.
        
        This method displays the new multi project dialog and initializes
        the multi project object with the data entered.
        """
        if not self.checkDirty():
            return
            
        from .PropertiesDialog import PropertiesDialog
        dlg = PropertiesDialog(self, True)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.closeMultiProject()
            dlg.storeData()
            self.opened = True
            self.setDirty(True)
            self.closeAct.setEnabled(True)
            self.saveasAct.setEnabled(True)
            self.addProjectAct.setEnabled(True)
            self.propsAct.setEnabled(True)
            self.newMultiProject.emit()
    
    def __showProperties(self):
        """
        Private slot to display the properties dialog.
        """
        from .PropertiesDialog import PropertiesDialog
        dlg = PropertiesDialog(self, False)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.storeData()
            self.setDirty(True)
            self.multiProjectPropertiesChanged.emit()
    
    @pyqtSlot()
    @pyqtSlot(str)
    def openMultiProject(self, fn=None, openMaster=True):
        """
        Public slot to open a multi project.
        
        @param fn optional filename of the multi project file to be
            read
        @type str
        @param openMaster flag indicating, that the master project
            should be opened depending on the configuration
        @type bool
        """
        if not self.checkDirty():
            return
        
        if fn is None:
            fn = E5FileDialog.getOpenFileName(
                self.parent(),
                self.tr("Open Multi Project"),
                Preferences.getMultiProject("Workspace") or
                Utilities.getHomeDir(),
                self.tr("Multi Project Files (*.emj);;"
                        "XML Multi Project Files (*.e5m *.e4m)"))
            
            if fn == "":
                fn = None
        
        QApplication.processEvents()
        
        if fn is not None:
            self.closeMultiProject()
            ok = self.__readMultiProject(fn)
            if ok:
                self.opened = True
                
                self.closeAct.setEnabled(True)
                self.saveasAct.setEnabled(True)
                self.addProjectAct.setEnabled(True)
                self.propsAct.setEnabled(True)
                
                self.multiProjectOpened.emit()
                
                if openMaster and Preferences.getMultiProject(
                        "OpenMasterAutomatically"):
                    self.__openMasterProject(False)
    
    def saveMultiProject(self):
        """
        Public slot to save the current multi project.
        
        @return flag indicating success
        @rtype bool
        """
        if self.isDirty():
            if len(self.pfile) > 0:
                if self.pfile.endswith((".e4m", ".e5m")):
                    self.pfile = (self.pfile
                                  .replace(".e4m", ".emj")
                                  .replace(".e5m", ".emj"))
                    self.__syncRecent()
                ok = self.__writeMultiProject()
            else:
                ok = self.saveMultiProjectAs()
        else:
            ok = True
        return ok
    
    def saveMultiProjectAs(self):
        """
        Public slot to save the current multi project to a different file.
        
        @return flag indicating success
        @rtype bool
        """
        defaultFilter = self.tr("Multi Project Files (*.emj)")
        if self.ppath:
            defaultPath = self.ppath
        else:
            defaultPath = (
                Preferences.getMultiProject("Workspace") or
                Utilities.getHomeDir()
            )
        fn, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
            self.parent(),
            self.tr("Save multiproject as"),
            defaultPath,
            self.tr("Multi Project Files (*.emj);;"
                    "XML Multi Project Files (*.e5m)"),
            defaultFilter,
            E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
        
        if fn:
            ext = QFileInfo(fn).suffix()
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fn += ex
            if QFileInfo(fn).exists():
                res = E5MessageBox.yesNo(
                    self.parent(),
                    self.tr("Save File"),
                    self.tr("<p>The file <b>{0}</b> already exists."
                            " Overwrite it?</p>").format(fn),
                    icon=E5MessageBox.Warning)
                if not res:
                    return False
                
            self.name = QFileInfo(fn).baseName()
            self.__writeMultiProject(fn)
            
            self.multiProjectClosed.emit()
            self.multiProjectOpened.emit()
            return True
        else:
            return False
    
    def checkDirty(self):
        """
        Public method to check the dirty status and open a message window.
        
        @return flag indicating whether this operation was successful (boolean)
        """
        if self.isDirty():
            res = E5MessageBox.okToClearData(
                self.parent(),
                self.tr("Close Multiproject"),
                self.tr("The current multiproject has unsaved changes."),
                self.saveMultiProject)
            if res:
                self.setDirty(False)
            return res
        
        return True
    
    def closeMultiProject(self):
        """
        Public slot to close the current multi project.
        
        @return flag indicating success (boolean)
        """
        # save the list of recently opened projects
        self.__saveRecent()
        
        if not self.isOpen():
            return True
        
        if not self.checkDirty():
            return False
        
        # now close the current project, if it belongs to the multi project
        pfile = self.projectObject.getProjectFile()
        if pfile:
            for project in self.__projects.values():
                if project['file'] == pfile:
                    if not self.projectObject.closeProject():
                        return False
                    break
        
        self.__initData()
        self.closeAct.setEnabled(False)
        self.saveasAct.setEnabled(False)
        self.saveAct.setEnabled(False)
        self.addProjectAct.setEnabled(False)
        self.propsAct.setEnabled(False)
        
        self.multiProjectClosed.emit()
        
        return True

    def initActions(self):
        """
        Public slot to initialize the multi project related actions.
        """
        self.actions = []
        
        self.actGrp1 = createActionGroup(self)
        
        act = E5Action(
            self.tr('New multiproject'),
            UI.PixmapCache.getIcon("multiProjectNew"),
            self.tr('&New...'), 0, 0,
            self.actGrp1, 'multi_project_new')
        act.setStatusTip(self.tr('Generate a new multiproject'))
        act.setWhatsThis(self.tr(
            """<b>New...</b>"""
            """<p>This opens a dialog for entering the info for a"""
            """ new multiproject.</p>"""
        ))
        act.triggered.connect(self.__newMultiProject)
        self.actions.append(act)

        act = E5Action(
            self.tr('Open multiproject'),
            UI.PixmapCache.getIcon("multiProjectOpen"),
            self.tr('&Open...'), 0, 0,
            self.actGrp1, 'multi_project_open')
        act.setStatusTip(self.tr('Open an existing multiproject'))
        act.setWhatsThis(self.tr(
            """<b>Open...</b>"""
            """<p>This opens an existing multiproject.</p>"""
        ))
        act.triggered.connect(self.openMultiProject)
        self.actions.append(act)

        self.closeAct = E5Action(
            self.tr('Close multiproject'),
            UI.PixmapCache.getIcon("multiProjectClose"),
            self.tr('&Close'), 0, 0, self, 'multi_project_close')
        self.closeAct.setStatusTip(self.tr(
            'Close the current multiproject'))
        self.closeAct.setWhatsThis(self.tr(
            """<b>Close</b>"""
            """<p>This closes the current multiproject.</p>"""
        ))
        self.closeAct.triggered.connect(self.closeMultiProject)
        self.actions.append(self.closeAct)

        self.saveAct = E5Action(
            self.tr('Save multiproject'),
            UI.PixmapCache.getIcon("multiProjectSave"),
            self.tr('&Save'), 0, 0, self, 'multi_project_save')
        self.saveAct.setStatusTip(self.tr('Save the current multiproject'))
        self.saveAct.setWhatsThis(self.tr(
            """<b>Save</b>"""
            """<p>This saves the current multiproject.</p>"""
        ))
        self.saveAct.triggered.connect(self.saveMultiProject)
        self.actions.append(self.saveAct)

        self.saveasAct = E5Action(
            self.tr('Save multiproject as'),
            UI.PixmapCache.getIcon("multiProjectSaveAs"),
            self.tr('Save &as...'), 0, 0, self,
            'multi_project_save_as')
        self.saveasAct.setStatusTip(self.tr(
            'Save the current multiproject to a new file'))
        self.saveasAct.setWhatsThis(self.tr(
            """<b>Save as</b>"""
            """<p>This saves the current multiproject to a new file.</p>"""
        ))
        self.saveasAct.triggered.connect(self.saveMultiProjectAs)
        self.actions.append(self.saveasAct)

        self.addProjectAct = E5Action(
            self.tr('Add project to multiproject'),
            UI.PixmapCache.getIcon("fileProject"),
            self.tr('Add &project...'), 0, 0,
            self, 'multi_project_add_project')
        self.addProjectAct.setStatusTip(self.tr(
            'Add a project to the current multiproject'))
        self.addProjectAct.setWhatsThis(self.tr(
            """<b>Add project...</b>"""
            """<p>This opens a dialog for adding a project"""
            """ to the current multiproject.</p>"""
        ))
        self.addProjectAct.triggered.connect(self.addNewProject)
        self.actions.append(self.addProjectAct)

        self.propsAct = E5Action(
            self.tr('Multiproject properties'),
            UI.PixmapCache.getIcon("multiProjectProps"),
            self.tr('&Properties...'), 0, 0, self,
            'multi_project_properties')
        self.propsAct.setStatusTip(self.tr(
            'Show the multiproject properties'))
        self.propsAct.setWhatsThis(self.tr(
            """<b>Properties...</b>"""
            """<p>This shows a dialog to edit the multiproject"""
            """ properties.</p>"""
        ))
        self.propsAct.triggered.connect(self.__showProperties)
        self.actions.append(self.propsAct)

        self.closeAct.setEnabled(False)
        self.saveAct.setEnabled(False)
        self.saveasAct.setEnabled(False)
        self.addProjectAct.setEnabled(False)
        self.propsAct.setEnabled(False)
    
    def initMenu(self):
        """
        Public slot to initialize the multi project menu.
        
        @return the menu generated (QMenu)
        """
        menu = QMenu(self.tr('&Multiproject'), self.parent())
        self.recentMenu = QMenu(self.tr('Open &Recent Multiprojects'),
                                menu)
        
        self.__menus = {
            "Main": menu,
            "Recent": self.recentMenu,
        }
        
        # connect the aboutToShow signals
        self.recentMenu.aboutToShow.connect(self.__showContextMenuRecent)
        self.recentMenu.triggered.connect(self.__openRecent)
        menu.aboutToShow.connect(self.__showMenu)
        
        # build the main menu
        menu.setTearOffEnabled(True)
        menu.addActions(self.actGrp1.actions())
        self.menuRecentAct = menu.addMenu(self.recentMenu)
        menu.addSeparator()
        menu.addAction(self.closeAct)
        menu.addSeparator()
        menu.addAction(self.saveAct)
        menu.addAction(self.saveasAct)
        menu.addSeparator()
        menu.addAction(self.addProjectAct)
        menu.addSeparator()
        menu.addAction(self.propsAct)
        
        self.menu = menu
        return menu
    
    def initToolbar(self, toolbarManager):
        """
        Public slot to initialize the multi project toolbar.
        
        @param toolbarManager reference to a toolbar manager object
            (E5ToolBarManager)
        @return the toolbar generated (QToolBar)
        """
        tb = QToolBar(self.tr("Multiproject"), self.ui)
        tb.setIconSize(UI.Config.ToolBarIconSize)
        tb.setObjectName("MultiProjectToolbar")
        tb.setToolTip(self.tr('Multiproject'))
        
        tb.addActions(self.actGrp1.actions())
        tb.addAction(self.closeAct)
        tb.addSeparator()
        tb.addAction(self.saveAct)
        tb.addAction(self.saveasAct)
        
        toolbarManager.addToolBar(tb, tb.windowTitle())
        toolbarManager.addAction(self.addProjectAct, tb.windowTitle())
        toolbarManager.addAction(self.propsAct, tb.windowTitle())
        
        return tb
    
    def __showMenu(self):
        """
        Private method to set up the multi project menu.
        """
        self.menuRecentAct.setEnabled(len(self.recent) > 0)
        
        self.showMenu.emit("Main", self.__menus["Main"])
    
    def __syncRecent(self):
        """
        Private method to synchronize the list of recently opened multi
        projects with the central store.
        """
        for recent in self.recent[:]:
            if Utilities.samepath(self.pfile, recent):
                self.recent.remove(recent)
        self.recent.insert(0, self.pfile)
        maxRecent = Preferences.getProject("RecentNumber")
        if len(self.recent) > maxRecent:
            self.recent = self.recent[:maxRecent]
        self.__saveRecent()
    
    def __showContextMenuRecent(self):
        """
        Private method to set up the recent multi projects menu.
        """
        self.__loadRecent()
        
        self.recentMenu.clear()
        
        idx = 1
        for rp in self.recent:
            if idx < 10:
                formatStr = '&{0:d}. {1}'
            else:
                formatStr = '{0:d}. {1}'
            act = self.recentMenu.addAction(
                formatStr.format(
                    idx,
                    Utilities.compactPath(rp, self.ui.maxMenuFilePathLen)))
            act.setData(rp)
            act.setEnabled(QFileInfo(rp).exists())
            idx += 1
        
        self.recentMenu.addSeparator()
        self.recentMenu.addAction(self.tr('&Clear'), self.clearRecent)
    
    def __openRecent(self, act):
        """
        Private method to open a multi project from the list of rencently
        opened multi projects.
        
        @param act reference to the action that triggered (QAction)
        """
        file = act.data()
        if file:
            self.openMultiProject(file)
    
    def clearRecent(self):
        """
        Public method to clear the recent multi projects menu.
        """
        self.recent = []
        self.__saveRecent()
    
    def getActions(self):
        """
        Public method to get a list of all actions.
        
        @return list of all actions (list of E5Action)
        """
        return self.actions[:]
    
    def addE5Actions(self, actions):
        """
        Public method to add actions to the list of actions.
        
        @param actions list of actions (list of E5Action)
        """
        self.actions.extend(actions)
    
    def removeE5Actions(self, actions):
        """
        Public method to remove actions from the list of actions.
        
        @param actions list of actions (list of E5Action)
        """
        for act in actions:
            try:
                self.actions.remove(act)
            except ValueError:
                pass
    
    def getMenu(self, menuName):
        """
        Public method to get a reference to the main menu or a submenu.
        
        @param menuName name of the menu (string)
        @return reference to the requested menu (QMenu) or None
        """
        try:
            return self.__menus[menuName]
        except KeyError:
            return None
    
    def openProject(self, filename):
        """
        Public slot to open a project.
        
        @param filename filename of the project file (string)
        """
        self.projectObject.openProject(filename)
        self.projectOpened.emit(filename)
    
    def __openMasterProject(self, reopen=True):
        """
        Private slot to open the master project.
        
        @param reopen flag indicating, that the master project should be
            reopened, if it has been opened already (boolean)
        """
        for project in self.__projects.values():
            if project['master']:
                if (
                    reopen or
                    not self.projectObject.isOpen() or
                    self.projectObject.getProjectFile() != project['file']
                ):
                    self.openProject(project['file'])
                    return
    
    def getMasterProjectFile(self):
        """
        Public method to get the filename of the master project.
        
        @return name of the master project file (string)
        """
        for project in self.__projects:
            if project['master']:
                return project['file']
        
        return None
    
    def getDependantProjectFiles(self):
        """
        Public method to get the filenames of the dependent projects.
        
        @return names of the dependent project files (list of strings)
        """
        files = []
        for project in self.__projects.values():
            if not project['master']:
                files.append(project['file'])
        return files
