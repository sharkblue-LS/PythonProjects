# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the tasks JSON file.
"""

import json
import time

from PyQt5.QtCore import QObject

from E5Gui import E5MessageBox
from E5Gui.E5OverrideCursor import E5OverridenCursor
from E5Gui.E5Application import e5App

import Preferences


class TasksFile(QObject):
    """
    Class representing the tasks JSON file.
    """
    def __init__(self, isGlobal: bool, parent: QObject = None):
        """
        Constructor
        
        @param isGlobal flag indicating a file for global tasks
        @type bool
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super(TasksFile, self).__init__(parent)
        self.__isGlobal = isGlobal
    
    def writeFile(self, filename: str) -> bool:
        """
        Public method to write the tasks data to a tasks JSON file.
        
        @param filename name of the tasks file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        # prepare the tasks data dictionary
        # step 0: header
        tasksDict = {}
        if self.__isGlobal:
            tasksDict["header"] = {
                "comment": "eric tasks file",
                "saved": time.strftime('%Y-%m-%d, %H:%M:%S'),
                "warning": (
                    "This file was generated automatically, do not edit."
                ),
            }
            # step 1: project scan filter
            tasksDict["ProjectScanFilter"] = ""
            
            # step 2: tasks
            tasksDict["Tasks"] = [
                task.toDict()
                for task in e5App().getObject("TaskViewer").getGlobalTasks()
            ]
        else:
            tasksDict["header"] = {
                "comment": "eric tasks file for project {0}".format(
                    e5App().getObject("Project").getProjectName()),
                "warning": (
                    "This file was generated automatically, do not edit."
                ),
            }
            if Preferences.getProject("TimestampFile"):
                tasksDict["header"]["saved"] = (
                    time.strftime('%Y-%m-%d, %H:%M:%S')
                )
            # step 1: project scan filter
            tasksDict["ProjectScanFilter"] = (
                e5App().getObject("TaskViewer").getTasksScanFilter()
            )
            
            # step 2: tasks
            tasksDict["Tasks"] = [
                task.toDict()
                for task in e5App().getObject("TaskViewer").getProjectTasks()
            ]
        
        try:
            jsonString = json.dumps(tasksDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, EnvironmentError) as err:
            with E5OverridenCursor():
                E5MessageBox.critical(
                    None,
                    self.tr("Save Tasks"),
                    self.tr(
                        "<p>The tasks file <b>{0}</b> could not be"
                        " written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the tasks data from a task JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            tasksDict = json.loads(jsonString)
        except (EnvironmentError, json.JSONDecodeError) as err:
            E5MessageBox.critical(
                None,
                self.tr("Read Tasks"),
                self.tr(
                    "<p>The tasks file <b>{0}</b> could not be read.</p>"
                    "<p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        viewer = e5App().getObject("TaskViewer")
        if tasksDict["ProjectScanFilter"]:
            viewer.setTasksScanFilter(tasksDict["ProjectScanFilter"])
        
        addedTasks = []
        for task in tasksDict["Tasks"]:
            addedTask = viewer.addTask(
                task["summary"], priority=task["priority"],
                filename=task["filename"], lineno=task["lineno"],
                completed=task["completed"], _time=task["created"],
                isProjectTask=not self.__isGlobal, taskType=task["type"],
                description=task["description"], uid=task["uid"],
                parentTask=task["parent_uid"])
            addedTasks.append((addedTask, task["expanded"]))
        
        for task, expanded in addedTasks:
            task.setExpanded(expanded)
        
        return True
