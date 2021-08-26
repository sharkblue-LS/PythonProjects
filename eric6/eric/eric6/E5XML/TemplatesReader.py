# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class for reading an XML templates file.
"""

from .Config import templatesFileFormatVersion
from .XMLStreamReaderBase import XMLStreamReaderBase


class TemplatesReader(XMLStreamReaderBase):
    """
    Class for reading an XML tasks file.
    """
    supportedVersions = ["4.0"]
    
    def __init__(self, device, viewer):
        """
        Constructor
        
        @param device reference to the I/O device to read from (QIODevice)
        @param viewer reference to the template viewer object (TemplateViewer)
        """
        XMLStreamReaderBase.__init__(self, device)
        
        self.__viewer = viewer
        
        self.version = ""
        self.groupName = "DEFAULT"
    
    def readXML(self):
        """
        Public method to read and parse the XML document.
        """
        while not self.atEnd():
            self.readNext()
            if self.isStartElement():
                if self.name() == "Templates":
                    self.version = self.attribute(
                        "version", templatesFileFormatVersion)
                    if self.version not in self.supportedVersions:
                        self.raiseUnsupportedFormatVersion(self.version)
                elif self.name() == "TemplateGroup":
                    self.__readTemplateGroup()
                else:
                    self.raiseUnexpectedStartTag(self.name())
        
        self.showErrorMessage()
    
    def __readTemplateGroup(self):
        """
        Private method to read a template group.
        """
        self.groupName = self.attribute('name', "DEFAULT")
        language = self.attribute('language', "All")
        self.__viewer.addGroup(self.groupName, language)
        
        while not self.atEnd():
            self.readNext()
            if self.isEndElement() and self.name() == "TemplateGroup":
                break
            
            if self.isStartElement():
                if self.name() == "Template":
                    self.__readTemplate()
                else:
                    self.raiseUnexpectedStartTag(self.name())
    
    def __readTemplate(self):
        """
        Private method to read the template definition.
        """
        templateName = self.attribute('name', '')
        templateDescription = ""
        templateText = ""
        
        while not self.atEnd():
            self.readNext()
            if (
                self.isEndElement() and
                self.name() == "Template" and
                templateName
            ):
                self.__viewer.addEntry(self.groupName, templateName,
                                       templateDescription, templateText,
                                       quiet=True)
                break
            
            if self.isStartElement():
                if self.name() == "TemplateDescription":
                    templateDescription = self.readElementText()
                elif self.name() == "TemplateText":
                    templateText = self.readElementText()
                else:
                    self.raiseUnexpectedStartTag(self.name())
