# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the multi project browser.
"""

import os
import glob

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QDialog, QMenu

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox

import UI.PixmapCache


class MultiProjectBrowser(QTreeWidget):
    """
    Class implementing the multi project browser.
    """
    ProjectFileNameRole = Qt.ItemDataRole.UserRole
    ProjectUidRole = Qt.ItemDataRole.UserRole + 1
    
    def __init__(self, multiProject, project, parent=None):
        """
        Constructor
        
        @param multiProject reference to the multi project object
        @type MultiProject
        @param project reference to the project object
        @type Project
        @param parent parent widget
        @type QWidget
        """
        super(MultiProjectBrowser, self).__init__(parent)
        self.multiProject = multiProject
        self.project = project
        
        self.setWindowIcon(UI.PixmapCache.getIcon("eric"))
        self.setAlternatingRowColors(True)
        self.setHeaderHidden(True)
        self.setItemsExpandable(False)
        self.setRootIsDecorated(False)
        self.setSortingEnabled(True)
        
        self.__openingProject = False
        
        self.multiProject.newMultiProject.connect(
            self.__newMultiProject)
        self.multiProject.multiProjectOpened.connect(
            self.__multiProjectOpened)
        self.multiProject.multiProjectClosed.connect(
            self.__multiProjectClosed)
        self.multiProject.projectDataChanged.connect(
            self.__projectDataChanged)
        self.multiProject.projectAdded.connect(
            self.__projectAdded)
        self.multiProject.projectRemoved.connect(
            self.__projectRemoved)
        
        self.project.projectOpened.connect(self.__projectOpened)
        self.project.projectClosed.connect(self.__projectClosed)
        
        self.__createPopupMenu()
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenuRequested)
        self.itemActivated.connect(self.__openItem)
        
        self.setEnabled(False)
    
    ###########################################################################
    ## Slot handling methods below
    ###########################################################################
    
    def __newMultiProject(self):
        """
        Private slot to handle the creation of a new multi project.
        """
        self.clear()
        self.setEnabled(True)
    
    def __multiProjectOpened(self):
        """
        Private slot to handle the opening of a multi project.
        """
        for project in self.multiProject.getProjects():
            self.__addProject(project)
        
        self.sortItems(0, Qt.SortOrder.AscendingOrder)
        
        self.setEnabled(True)
    
    def __multiProjectClosed(self):
        """
        Private slot to handle the closing of a multi project.
        """
        self.clear()
        self.setEnabled(False)
    
    def __projectAdded(self, project):
        """
        Private slot to handle the addition of a project to the multi project.
        
        @param project reference to the project data dictionary
        """
        self.__addProject(project)
        self.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    def __projectRemoved(self, project):
        """
        Private slot to handle the removal of a project from the multi project.
        
        @param project reference to the project data dictionary
        """
        itm = self.__findProjectItem(project)
        if itm:
            parent = itm.parent()
            parent.removeChild(itm)
            del itm
            if parent.childCount() == 0:
                top = self.takeTopLevelItem(self.indexOfTopLevelItem(parent))
                # __IGNORE_WARNING__
                del top
    
    def __projectDataChanged(self, project):
        """
        Private slot to handle the change of a project of the multi project.
        
        @param project reference to the project data dictionary
        """
        itm = self.__findProjectItem(project)
        if itm:
            parent = itm.parent()
            if parent.text(0) != project["category"]:
                self.__projectRemoved(project)
                self.__addProject(project)
            else:
                self.__setItemData(itm, project)
            
        self.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    def __projectOpened(self):
        """
        Private slot to handle the opening of a project.
        """
        projectfile = self.project.getProjectFile()
        project = {
            'name': "",
            'file': projectfile,
            'master': False,
            'description': "",
            'category': "",
            'uid': "",
        }
        itm = self.__findProjectItem(project)
        if itm:
            font = itm.font(0)
            font.setBold(True)
            itm.setFont(0, font)
    
    def __projectClosed(self):
        """
        Private slot to handle the closing of a project.
        """
        for topIndex in range(self.topLevelItemCount()):
            topItem = self.topLevelItem(topIndex)
            for childIndex in range(topItem.childCount()):
                childItem = topItem.child(childIndex)
                font = childItem.font(0)
                font.setBold(False)
                childItem.setFont(0, font)
    
    def __contextMenuRequested(self, coord):
        """
        Private slot to show the context menu.
        
        @param coord the position of the mouse pointer (QPoint)
        """
        itm = self.itemAt(coord)
        if itm is None or itm.parent() is None:
            self.__backMenu.popup(self.mapToGlobal(coord))
        else:
            self.__menu.popup(self.mapToGlobal(coord))
    
    def __openItem(self, itm=None):
        """
        Private slot to open a project.
        
        @param itm reference to the project item to be opened (QTreeWidgetItem)
        """
        if itm is None:
            itm = self.currentItem()
            if itm is None or itm.parent() is None:
                return
        
        if not self.__openingProject:
            filename = itm.data(0, MultiProjectBrowser.ProjectFileNameRole)
            if filename:
                self.__openingProject = True
                self.multiProject.openProject(filename)
                self.__openingProject = False
    
    ###########################################################################
    ## Private methods below
    ###########################################################################
    
    def __findCategoryItem(self, category):
        """
        Private method to find the item for a category.
        
        @param category category to search for (string)
        @return reference to the category item or None, if there is
            no such item (QTreeWidgetItem or None)
        """
        if category == "":
            category = self.tr("Not categorized")
        for index in range(self.topLevelItemCount()):
            itm = self.topLevelItem(index)
            if itm.text(0) == category:
                return itm
        
        return None
    
    def __addProject(self, project):
        """
        Private method to add a project to the list.
        
        @param project reference to the project data dictionary
        """
        parent = self.__findCategoryItem(project['category'])
        if parent is None:
            if project['category']:
                parent = QTreeWidgetItem(self, [project['category']])
            else:
                parent = QTreeWidgetItem(self, [self.tr("Not categorized")])
            parent.setExpanded(True)
        itm = QTreeWidgetItem(parent)
        self.__setItemData(itm, project)
    
    def __setItemData(self, itm, project):
        """
        Private method to set the data of a project item.
        
        @param itm reference to the item to be set (QTreeWidgetItem)
        @param project reference to the project data dictionary
        """
        itm.setText(0, project['name'])
        if project['master']:
            itm.setIcon(0, UI.PixmapCache.getIcon("masterProject"))
        else:
            itm.setIcon(0, UI.PixmapCache.getIcon("empty"))
        itm.setToolTip(0, project['file'])
        itm.setData(0, MultiProjectBrowser.ProjectFileNameRole,
                    project['file'])
        itm.setData(0, MultiProjectBrowser.ProjectUidRole, project['uid'])
    
    def __findProjectItem(self, project):
        """
        Private method to search a specific project item.
        
        @param project reference to the project data dictionary
        @return reference to the item (QTreeWidgetItem) or None
        """
        if project["uid"]:
            compareData = project["uid"]
            compareRole = MultiProjectBrowser.ProjectUidRole
        else:
            compareData = project["file"]
            compareRole = MultiProjectBrowser.ProjectFileNameRole
        
        for topIndex in range(self.topLevelItemCount()):
            topItm = self.topLevelItem(topIndex)
            for childIndex in range(topItm.childCount()):
                itm = topItm.child(childIndex)
                data = itm.data(0, compareRole)
                if data == compareData:
                    return itm
        
        return None
    
    def __removeProject(self):
        """
        Private method to handle the Remove context menu entry.
        """
        itm = self.currentItem()
        if itm is not None and itm.parent() is not None:
            uid = itm.data(0, MultiProjectBrowser.ProjectUidRole)
            if uid:
                self.multiProject.removeProject(uid)
    
    def __deleteProject(self):
        """
        Private method to handle the Delete context menu entry.
        """
        itm = self.currentItem()
        if itm is not None and itm.parent() is not None:
            projectFile = itm.data(0, MultiProjectBrowser.ProjectFileNameRole)
            projectPath = os.path.dirname(projectFile)
            
            if self.project.getProjectPath() == projectPath:
                E5MessageBox.warning(
                    self,
                    self.tr("Delete Project"),
                    self.tr("""The current project cannot be deleted."""
                            """ Please close it first."""))
            else:
                projectFiles = glob.glob(os.path.join(projectPath, "*.epj"))
                projectFiles += glob.glob(os.path.join(projectPath, "*.e4p"))
                if not projectFiles:
                    # Oops, that should not happen; play it save
                    res = False
                elif len(projectFiles) == 1:
                    res = E5MessageBox.yesNo(
                        self,
                        self.tr("Delete Project"),
                        self.tr("""<p>Shall the project <b>{0}</b> (Path:"""
                                """ {1}) really be deleted?</p>""").format(
                            itm.text(0), projectPath))
                else:
                    res = E5MessageBox.yesNo(
                        self,
                        self.tr("Delete Project"),
                        self.tr("""<p>Shall the project <b>{0}</b> (Path:"""
                                """ {1}) really be deleted?</p>"""
                                """<p><b>Warning:</b> It contains <b>{2}</b>"""
                                """ sub-projects.</p>""").format(
                            itm.text(0), projectPath, len(projectFiles)))
                if res:
                    for subprojectFile in projectFiles:
                        # remove all sub-projects before deleting the directory
                        if subprojectFile != projectFile:
                            projectData = {
                                'name': "",
                                'file': subprojectFile,
                                'master': False,
                                'description': "",
                                'category': "",
                                'uid': "",
                            }
                            pitm = self.__findProjectItem(projectData)
                            if pitm:
                                uid = pitm.data(
                                    0, MultiProjectBrowser.ProjectUidRole)
                                if uid:
                                    self.multiProject.removeProject(uid)
                        
                    uid = itm.data(0, MultiProjectBrowser.ProjectUidRole)
                    if uid:
                        self.multiProject.deleteProject(uid)
    
    def __showProjectProperties(self):
        """
        Private method to show the data of a project entry.
        """
        itm = self.currentItem()
        if itm is not None and itm.parent() is not None:
            uid = itm.data(0, MultiProjectBrowser.ProjectUidRole)
            if uid:
                project = self.multiProject.getProject(uid)
                if project is not None:
                    from .AddProjectDialog import AddProjectDialog
                    dlg = AddProjectDialog(
                        self, project=project,
                        categories=self.multiProject.getCategories())
                    if dlg.exec() == QDialog.DialogCode.Accepted:
                        (name, filename, isMaster, description, category,
                         uid) = dlg.getData()
                        project = {
                            'name': name,
                            'file': filename,
                            'master': isMaster,
                            'description': description,
                            'category': category,
                            'uid': uid,
                        }
                        self.multiProject.changeProjectProperties(project)
    
    def __addNewProject(self):
        """
        Private method to add a new project entry.
        """
        itm = self.currentItem()
        if itm is not None:
            if itm.parent() is None:
                # current item is a category item
                category = itm.text(0)
            else:
                category = itm.parent().text(0)
        else:
            category = ""
        self.multiProject.addNewProject(category=category)
    
    def __copyProject(self):
        """
        Private method to copy the selected project on disk.
        """
        itm = self.currentItem()
        if itm and itm.parent():
            # it is a project item and not a category
            uid = itm.data(0, MultiProjectBrowser.ProjectUidRole)
            if uid:
                self.multiProject.copyProject(uid)
    
    def __createPopupMenu(self):
        """
        Private method to create the popup menu.
        """
        self.__menu = QMenu(self)
        self.__menu.addAction(self.tr("Open"), self.__openItem)
        self.__menu.addAction(self.tr("Remove from Multi Project"),
                              self.__removeProject)
        self.__menu.addAction(self.tr("Delete from Disk"),
                              self.__deleteProject)
        self.__menu.addAction(self.tr("Properties"),
                              self.__showProjectProperties)
        self.__menu.addSeparator()
        self.__menu.addAction(self.tr("Add Project..."),
                              self.__addNewProject)
        self.__menu.addAction(self.tr("Copy Project..."),
                              self.__copyProject)
        self.__menu.addSeparator()
        self.__menu.addAction(self.tr("Configure..."), self.__configure)
        
        self.__backMenu = QMenu(self)
        self.__backMenu.addAction(self.tr("Add Project..."),
                                  self.__addNewProject)
        self.__backMenu.addSeparator()
        self.__backMenu.addAction(self.tr("Configure..."),
                                  self.__configure)
    
    def __configure(self):
        """
        Private method to open the configuration dialog.
        """
        e5App().getObject("UserInterface").showPreferences("multiProjectPage")
