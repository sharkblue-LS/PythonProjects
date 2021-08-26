# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the shortcuts JSON file.
"""

import json
import time
import typing

from PyQt5.QtCore import QObject

from E5Gui import E5MessageBox
from E5Gui.E5OverrideCursor import E5OverridenCursor
from E5Gui.E5Application import e5App

import Preferences

HelpViewer = typing.TypeVar("WebBrowserWindow")


class ShortcutsFile(QObject):
    """
    Class representing the shortcuts JSON file.
    """
    def __init__(self, parent: QObject = None):
        """
        Constructor
        
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super(ShortcutsFile, self).__init__(parent)
    
    def __addActionsToDict(self, category: str, actions: list,
                           actionsDict: dict):
        """
        Private method to add a list of actions to the actions dictionary.
        
        @param category category of the actions
        @type str
        @param actions list of actions
        @type list of QAction
        @param actionsDict reference to the actions dictionary to be modified
        @type dict
        """
        if actions:
            if category not in actionsDict:
                actionsDict[category] = {}
            for act in actions:
                if act.objectName():
                    # shortcuts are only exported, if their objectName is set
                    actionsDict[category][act.objectName()] = (
                        act.shortcut().toString(),
                        act.alternateShortcut().toString()
                    )
    
    def writeFile(self, filename: str, helpViewer: HelpViewer = None) -> bool:
        """
        Public method to write the shortcuts data to a shortcuts JSON file.
        
        @param filename name of the shortcuts file
        @type str
        @param helpViewer reference to the help window object
        @type WebBrowserWindow
        @return flag indicating a successful write
        @rtype bool
        """
        actionsDict = {}
        
        # step 1: collect all the shortcuts
        if helpViewer is None:
            self.__addActionsToDict(
                "Project",
                e5App().getObject("Project").getActions(),
                actionsDict
            )
            self.__addActionsToDict(
                "General",
                e5App().getObject("UserInterface").getActions('ui'),
                actionsDict
            )
            self.__addActionsToDict(
                "Wizards",
                e5App().getObject("UserInterface").getActions('wizards'),
                actionsDict
            )
            self.__addActionsToDict(
                "Debug",
                e5App().getObject("DebugUI").getActions(),
                actionsDict
            )
            self.__addActionsToDict(
                "Edit",
                e5App().getObject("ViewManager").getActions('edit'),
                actionsDict
            )
            self.__addActionsToDict(
                "File",
                e5App().getObject("ViewManager").getActions('file'),
                actionsDict
            )
            self.__addActionsToDict(
                "Search",
                e5App().getObject("ViewManager").getActions('search'),
                actionsDict
            )
            self.__addActionsToDict(
                "View",
                e5App().getObject("ViewManager").getActions('view'),
                actionsDict
            )
            self.__addActionsToDict(
                "Macro",
                e5App().getObject("ViewManager").getActions('macro'),
                actionsDict
            )
            self.__addActionsToDict(
                "Bookmarks",
                e5App().getObject("ViewManager").getActions('bookmark'),
                actionsDict
            )
            self.__addActionsToDict(
                "Spelling",
                e5App().getObject("ViewManager").getActions('spelling'),
                actionsDict
            )
            self.__addActionsToDict(
                "Window",
                e5App().getObject("ViewManager").getActions('window'),
                actionsDict
            )
            
            for category, ref in e5App().getPluginObjects():
                if hasattr(ref, "getActions"):
                    self.__addActionsToDict(
                        category, ref.getActions(), actionsDict
                    )
        
        else:
            self.__addActionsToDict(
                helpViewer.getActionsCategory(),
                helpViewer.getActions(),
                actionsDict
            )
        
        # step 2: assemble the data structure to be written
        shortcutsDict = {}
        # step 2.0: header
        shortcutsDict["header"] = {
            "comment": "eric keyboard shortcuts file",
            "saved": time.strftime('%Y-%m-%d, %H:%M:%S'),
            "author": Preferences.getUser("Email"),
        }
        # step 2.1: keyboard shortcuts
        shortcutsDict["shortcuts"] = actionsDict
        
        try:
            jsonString = json.dumps(shortcutsDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, EnvironmentError) as err:
            with E5OverridenCursor():
                E5MessageBox.critical(
                    None,
                    self.tr("Export Keyboard Shortcuts"),
                    self.tr(
                        "<p>The keyboard shortcuts file <b>{0}</b> could not"
                        " be written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the shortcuts data from a shortcuts JSON file.
        
        @param filename name of the shortcuts file
        @type str
        @return Dictionary of dictionaries of shortcuts. The keys of the
            dictionary are the shortcuts categories, the values are
            dictionaries. These dictionaries have the shortcut name as their
            key and a tuple of accelerators as their value.
        @rtype dict
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            shortcutsDict = json.loads(jsonString)
        except (EnvironmentError, json.JSONDecodeError) as err:
            E5MessageBox.critical(
                None,
                self.tr("Import Keyboard Shortcuts"),
                self.tr(
                    "<p>The keyboard shortcuts file <b>{0}</b> could not be"
                    " read.</p><p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return {}
        
        return shortcutsDict["shortcuts"]
