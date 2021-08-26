# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the templates JSON file.
"""

import json
import time
import typing

from PyQt5.QtCore import QObject

from E5Gui import E5MessageBox
from E5Gui.E5OverrideCursor import E5OverridenCursor


TemplateViewer = typing.TypeVar("TemplateViewer")


class TemplatesFile(QObject):
    """
    Class representing the templates JSON file.
    """
    def __init__(self, viewer: TemplateViewer, parent: QObject = None):
        """
        Constructor
        
        @param viewer reference to the template viewer object
        @type TemplateViewer
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super(TemplatesFile, self).__init__(parent)
        self.__viewer = viewer
    
    def writeFile(self, filename: str) -> bool:
        """
        Public method to write the templates data to a templates JSON file.
        
        @param filename name of the templates file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        templatesDict = {}
        # step 0: header
        templatesDict["header"] = {
            "comment": "eric templates file",
            "saved": time.strftime('%Y-%m-%d, %H:%M:%S'),
            "warning": (
                "This file was generated automatically, do not edit."
            ),
        }
        
        # step 1: template groups and templates
        templateGroups = []
        for group in self.__viewer.getAllGroups():
            templates = []
            for template in group.getAllEntries():
                templates.append({
                    "name": template.getName(),
                    "description": template.getDescription().strip(),
                    "text": template.getTemplateText()
                })
            templateGroups.append({
                "name": group.getName(),
                "language": group.getLanguage(),
                "templates": templates,
            })
        templatesDict["template_groups"] = templateGroups
        
        try:
            jsonString = json.dumps(templatesDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, EnvironmentError) as err:
            with E5OverridenCursor():
                E5MessageBox.critical(
                    None,
                    self.tr("Save Templates"),
                    self.tr(
                        "<p>The templates file <b>{0}</b> could not be"
                        " written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the templates data from a templates JSON file.
        
        @param filename name of the templates file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            templatesDict = json.loads(jsonString)
        except (EnvironmentError, json.JSONDecodeError) as err:
            E5MessageBox.critical(
                None,
                self.tr("Read Templates"),
                self.tr(
                    "<p>The templates file <b>{0}</b> could not be read.</p>"
                    "<p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        for templateGroup in templatesDict["template_groups"]:
            self.__viewer.addGroup(templateGroup["name"],
                                   templateGroup["language"])
            for template in templateGroup["templates"]:
                self.__viewer.addEntry(templateGroup["name"],
                                       template["name"],
                                       template["description"],
                                       template["text"],
                                       quiet=True)
        
        return True
