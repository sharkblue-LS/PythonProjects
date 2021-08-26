# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing a class for reading a highlighting styles XML file.
"""

from .Config import highlightingStylesFileFormatVersion
from .XMLStreamReaderBase import XMLStreamReaderBase


class HighlightingStylesReader(XMLStreamReaderBase):
    """
    Class for reading a highlighting styles XML file.
    """
    supportedVersions = ["4.3", "6.0"]
    
    def __init__(self, device, lexers):
        """
        Constructor
        
        @param device reference to the I/O device to read from (QIODevice)
        @param lexers dictionary of lexer objects for which to import the
            styles
        """
        XMLStreamReaderBase.__init__(self, device)
        
        self.lexers = lexers
        
        self.version = ""
    
    def readXML(self):
        """
        Public method to read and parse the XML document.
        
        @return list of read lexer style definitions
        @rtype list of dict
        """
        self.__lexersList = []
        
        while not self.atEnd():
            self.readNext()
            if self.isStartElement():
                if self.name() == "HighlightingStyles":
                    self.version = self.attribute(
                        "version",
                        highlightingStylesFileFormatVersion)
                    if self.version not in self.supportedVersions:
                        self.raiseUnsupportedFormatVersion(self.version)
                elif self.name() == "Lexer":
                    self.__readLexer()
                else:
                    self.raiseUnexpectedStartTag(self.name())
        
        self.showErrorMessage()
        
        return self.__lexersList
    
    def __readLexer(self):
        """
        Private method to read the lexer info.
        """
        language = self.attribute("name")
        self.__lexersList.append({
            "name": language,
            "styles": [],
        })
        if language and language in self.lexers:
            lexer = self.lexers[language]
        else:
            lexer = None
        
        while not self.atEnd():
            self.readNext()
            if self.isEndElement() and self.name() == "Lexer":
                break
            
            if self.isStartElement():
                if self.name() == "Style":
                    self.__readStyle(lexer)
                else:
                    self.raiseUnexpectedStartTag(self.name())
    
    def __readStyle(self, lexer):
        """
        Private method to read the style info.
        
        @param lexer reference to the lexer object
        """
        if lexer is not None:
            style = self.attribute("style")
            if style:
                style = int(style)
                substyle = int(self.attribute("substyle", "-1"))
                # -1 is default for base styles
                
                styleDict = {
                    "style": style,
                    "substyle": substyle,
                }
                
                color = self.attribute("color")
                if color:
                    styleDict["color"] = color
                else:
                    styleDict["color"] = (
                        lexer.defaultColor(style, substyle).name()
                    )
                
                paper = self.attribute("paper")
                if paper:
                    styleDict["paper"] = paper
                else:
                    styleDict["paper"] = (
                        lexer.defaultPaper(style, substyle).name()
                    )
                
                fontStr = self.attribute("font")
                if fontStr:
                    styleDict["font"] = fontStr
                else:
                    styleDict["font"] = (
                        lexer.defaultFont(style, substyle).toString()
                    )
                
                eolfill = self.attribute("eolfill")
                if eolfill:
                    eolfill = self.toBool(eolfill)
                    if eolfill is None:
                        eolfill = lexer.defaulEolFill(style, substyle)
                else:
                    eolfill = lexer.defaulEolFill(style, substyle)
                styleDict["eolfill"] = eolfill
        
                while not self.atEnd():
                    self.readNext()
                    if self.isStartElement():
                        if self.name() == "Description":
                            description = self.readElementText().strip()
                            if not description:
                                description = lexer.defaultDescription(
                                    style, substyle)
                            styleDict["description"] = description
                        elif self.name() == "Words":
                            words = self.readElementText().strip()
                            if not words:
                                words = lexer.defaultWords(style, substyle)
                            styleDict["words"] = words
                    
                    if self.isEndElement() and self.name() == "Style":
                        if "description" not in styleDict:
                            styleDict["description"] = ""
                        if "words" not in styleDict:
                            styleDict["words"] = ""
                        self.__lexersList[-1]["styles"].append(styleDict)
                        return
        
        while not self.atEnd():
            self.readNext()
            if self.isEndElement() and self.name() == "Style":
                break
