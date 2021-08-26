# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the highlighting styles JSON file.
"""

import json
import time

from PyQt5.QtCore import QObject

from E5Gui import E5MessageBox
from E5Gui.E5OverrideCursor import E5OverridenCursor

import Preferences


class HighlightingStylesFile(QObject):
    """
    Class representing the highlighting styles JSON file.
    """
    def __init__(self, parent: QObject = None):
        """
        Constructor
        
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super(HighlightingStylesFile, self).__init__(parent)
        
        self.__lexerAliases = {
            "PO": "Gettext",
            "POV": "Povray",
        }
    
    def writeFile(self, filename: str, lexers: list) -> bool:
        """
        Public method to write the highlighting styles data to a highlighting
        styles JSON file.
        
        @param filename name of the highlighting styles file
        @type str
        @param lexers list of lexers for which to export the styles
        @type list of PreferencesLexer
        @return flag indicating a successful write
        @rtype bool
        """
        stylesDict = {}
        # step 0: header
        stylesDict["header"] = {
            "comment": "eric highlighting styles file",
            "saved": time.strftime('%Y-%m-%d, %H:%M:%S'),
            "author": Preferences.getUser("Email"),
        }
        
        # step 1: add the lexer style data
        stylesDict["lexers"] = []
        for lexer in lexers:
            name = lexer.language()
            if name in self.__lexerAliases:
                name = self.__lexerAliases[name]
            lexerDict = {
                "name": name,
                "styles": [],
            }
            for description, style, substyle in lexer.getStyles():
                lexerDict["styles"].append({
                    "description": description,
                    "style": style,
                    "substyle": substyle,
                    "color": lexer.color(style, substyle).name(),
                    "paper": lexer.paper(style, substyle).name(),
                    "font": lexer.font(style, substyle).toString(),
                    "eolfill": lexer.eolFill(style, substyle),
                    "words": lexer.words(style, substyle).strip(),
                })
            stylesDict["lexers"].append(lexerDict)
        
        try:
            jsonString = json.dumps(stylesDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, EnvironmentError) as err:
            with E5OverridenCursor():
                E5MessageBox.critical(
                    None,
                    self.tr("Export Highlighting Styles"),
                    self.tr(
                        "<p>The highlighting styles file <b>{0}</b> could not"
                        " be written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> list:
        """
        Public method to read the highlighting styles data from a highlighting
        styles JSON file.
        
        @param filename name of the highlighting styles file
        @type str
        @return list of read lexer style definitions
        @rtype list of dict
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            stylesDict = json.loads(jsonString)
        except (EnvironmentError, json.JSONDecodeError) as err:
            E5MessageBox.critical(
                None,
                self.tr("Import Highlighting Styles"),
                self.tr(
                    "<p>The highlighting styles file <b>{0}</b> could not be"
                    " read.</p><p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return []
        
        return stylesDict["lexers"]
