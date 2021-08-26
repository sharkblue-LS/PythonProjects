# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class to store task data.
"""

import os
import time

from PyQt5.QtCore import Qt, QUuid
from PyQt5.QtWidgets import QTreeWidgetItem

import UI.PixmapCache
import Preferences


class Task(QTreeWidgetItem):
    """
    Class implementing the task data structure.
    """
    TypeNone = -1
    TypeFixme = 0
    TypeTodo = 1
    TypeWarning = 2
    TypeNote = 3
    TypeTest = 4
    TypeDocu = 5
    
    TaskType2IconName = {
        TypeFixme: "taskFixme",
        TypeTodo: "taskTodo",
        TypeWarning: "taskWarning",
        TypeNote: "taskNote",
        TypeTest: "taskTest",
        TypeDocu: "taskDocu",
    }
    TaskType2ColorName = {
        TypeFixme: "TasksFixmeColor",
        TypeTodo: "TasksTodoColor",
        TypeWarning: "TasksWarningColor",
        TypeNote: "TasksNoteColor",
        TypeTest: "TasksTestColor",
        TypeDocu: "TasksDocuColor",
    }
    TaskType2MarkersName = {
        TypeFixme: "TasksFixmeMarkers",
        TypeTodo: "TasksTodoMarkers",
        TypeWarning: "TasksWarningMarkers",
        TypeNote: "TasksNoteMarkers",
        TypeTest: "TasksTestMarkers",
        TypeDocu: "TasksDocuMarkers",
    }
    
    def __init__(self, summary, priority=1, filename="", lineno=0,
                 completed=False, _time=0, isProjectTask=False,
                 taskType=TypeTodo, project=None, description="",
                 uid="", parentUid=""):
        """
        Constructor
        
        @param summary summary text of the task (string)
        @param priority priority of the task (0=high, 1=normal, 2=low)
        @param filename filename containing the task (string)
        @param lineno line number containing the task (integer)
        @param completed flag indicating completion status (boolean)
        @param _time creation time of the task (float, if 0 use current time)
        @param isProjectTask flag indicating a task related to the current
            project (boolean)
        @param taskType type of the task (one of TypeFixme, TypeTodo,
            TypeWarning, TypeNote, TypeTest, TypeDocu)
        @param project reference to the project object (Project)
        @param description explanatory text of the task (string)
        @param uid unique id of the task (string)
        @param parentUid unique id of the parent task (string)
        """
        super(Task, self).__init__()
        
        self.summary = summary
        self.description = description
        if priority in [0, 1, 2]:
            self.priority = priority
        else:
            self.priority = 1
        self.filename = filename
        self.lineno = lineno
        self.completed = completed
        self.created = _time and _time or time.time()
        self._isProjectTask = isProjectTask
        self.taskType = taskType
        self.project = project
        if uid:
            self.uid = uid
        else:
            self.uid = QUuid.createUuid().toString()
        self.parentUid = parentUid
        
        if isProjectTask:
            self.filename = self.project.getRelativePath(self.filename)
            
        self.setData(0, Qt.ItemDataRole.DisplayRole, "")
        self.setData(1, Qt.ItemDataRole.DisplayRole, "")
        self.setData(2, Qt.ItemDataRole.DisplayRole, self.summary)
        self.setData(3, Qt.ItemDataRole.DisplayRole, self.filename)
        self.setData(4, Qt.ItemDataRole.DisplayRole, self.lineno or "")
        
        if self.completed:
            self.setIcon(0, UI.PixmapCache.getIcon("taskCompleted"))
            strikeOut = True
        else:
            self.setIcon(0, UI.PixmapCache.getIcon("empty"))
            strikeOut = False
        for column in range(2, 5):
            f = self.font(column)
            f.setStrikeOut(strikeOut)
            self.setFont(column, f)
        
        if self.priority == 1:
            self.setIcon(1, UI.PixmapCache.getIcon("empty"))
        elif self.priority == 0:
            self.setIcon(1, UI.PixmapCache.getIcon("taskPrioHigh"))
        elif self.priority == 2:
            self.setIcon(1, UI.PixmapCache.getIcon("taskPrioLow"))
        else:
            self.setIcon(1, UI.PixmapCache.getIcon("empty"))
        
        try:
            self.setIcon(2, UI.PixmapCache.getIcon(
                Task.TaskType2IconName[self.taskType]))
        except KeyError:
            self.setIcon(2, UI.PixmapCache.getIcon("empty"))
        
        self.colorizeTask()
        self.setTextAlignment(4, Qt.AlignmentFlag.AlignRight)
    
    def colorizeTask(self):
        """
        Public slot to set the colors of the task item.
        """
        boldFont = self.font(0)
        boldFont.setBold(True)
        nonBoldFont = self.font(0)
        nonBoldFont.setBold(False)
        for col in range(5):
            try:
                self.setBackground(
                    col, Preferences.getTasks(
                        Task.TaskType2ColorName[self.taskType]))
            except KeyError:
                # do not set background color if type is not known
                pass
            
            if self._isProjectTask:
                self.setFont(col, boldFont)
            else:
                self.setFont(col, nonBoldFont)
    
    def setSummary(self, summary):
        """
        Public slot to update the description.
        
        @param summary summary text of the task (string)
        """
        self.summary = summary
        self.setText(2, self.summary)
    
    def setDescription(self, description):
        """
        Public slot to update the description field.
        
        @param description descriptive text of the task (string)
        """
        self.description = description
    
    def setPriority(self, priority):
        """
        Public slot to update the priority.
        
        @param priority priority of the task (0=high, 1=normal, 2=low)
        """
        if priority in [0, 1, 2]:
            self.priority = priority
        else:
            self.priority = 1
        
        if self.priority == 1:
            self.setIcon(1, UI.PixmapCache.getIcon("empty"))
        elif self.priority == 0:
            self.setIcon(1, UI.PixmapCache.getIcon("taskPrioHigh"))
        elif self.priority == 2:
            self.setIcon(1, UI.PixmapCache.getIcon("taskPrioLow"))
        else:
            self.setIcon(1, UI.PixmapCache.getIcon("empty"))
    
    def setCompleted(self, completed):
        """
        Public slot to update the completed flag.
        
        @param completed flag indicating completion status (boolean)
        """
        self.completed = completed
        if self.completed:
            self.setIcon(0, UI.PixmapCache.getIcon("taskCompleted"))
            strikeOut = True
        else:
            self.setIcon(0, UI.PixmapCache.getIcon("empty"))
            strikeOut = False
        for column in range(2, 5):
            f = self.font(column)
            f.setStrikeOut(strikeOut)
            self.setFont(column, f)
        
        # set the completion status for all children
        for index in range(self.childCount()):
            self.child(index).setCompleted(completed)
    
    def isCompleted(self):
        """
        Public slot to return the completion status.
        
        @return flag indicating the completion status (boolean)
        """
        return self.completed
    
    def getFilename(self):
        """
        Public method to retrieve the task's filename.
        
        @return filename (string)
        """
        if self._isProjectTask and self.filename:
            return os.path.join(self.project.getProjectPath(), self.filename)
        else:
            return self.filename
    
    def isFileTask(self):
        """
        Public slot to get an indication, if this task is related to a file.
        
        @return flag indicating a file task (boolean)
        """
        return self.filename != ""
    
    def getLineno(self):
        """
        Public method to retrieve the task's linenumber.
        
        @return linenumber (integer)
        """
        return self.lineno
    
    def getUuid(self):
        """
        Public method to get the task's uid.
        
        @return uid (string)
        """
        return self.uid
    
    def getParentUuid(self):
        """
        Public method to get the parent task's uid.
        
        @return parent uid (string)
        """
        return self.parentUid
    
    def setProjectTask(self, pt):
        """
        Public method to set the project relation flag.
        
        @param pt flag indicating a project task (boolean)
        """
        self._isProjectTask = pt
        self.colorizeTask()
    
    def isProjectTask(self):
        """
        Public slot to return the project relation status.
        
        @return flag indicating the project relation status (boolean)
        """
        return self._isProjectTask
    
    def isProjectFileTask(self):
        """
        Public slot to get an indication, if this task is related to a
        project file.
        
        @return flag indicating a project file task (boolean)
        """
        return self._isProjectTask and self.filename != ""
    
    def toDict(self):
        """
        Public method to convert the task data to a dictionary.
        
        @return dictionary containing the task data
        @rtype dict
        """
        return {
            "summary": self.summary.strip(),
            "description": self.description.strip(),
            "priority": self.priority,
            "lineno": self.lineno,
            "completed": self.completed,
            "created": self.created,
            "type": self.taskType,
            "uid": self.uid,
            "parent_uid": self.parentUid,
            "expanded": self.isExpanded(),
            "filename": self.getFilename(),
        }
