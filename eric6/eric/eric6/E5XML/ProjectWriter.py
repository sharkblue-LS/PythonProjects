# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the writer class for writing an XML project file.
"""

import time

from E5Gui.E5Application import e5App

from .XMLStreamWriterBase import XMLStreamWriterBase
from .Config import (
    projectFileFormatVersion, projectFileFormatVersionRcc,
    projectFileFormatVersionUic, projectFileFormatVersionIdl,
    projectFileFormatVersionMake, projectFileFormatVersionProto,
    projectFileFormatVersionAlt
)

import Preferences
import Utilities


class ProjectWriter(XMLStreamWriterBase):
    """
    Class implementing the writer class for writing an XML project file.
    """
    def __init__(self, device, projectName):
        """
        Constructor
        
        @param device reference to the I/O device to write to (QIODevice)
        @param projectName name of the project (string)
        """
        XMLStreamWriterBase.__init__(self, device)
        
        self.pdata = e5App().getObject("Project").pdata
        self.name = projectName
        
    def writeXML(self):
        """
        Public method to write the XML to the file.
        """
        XMLStreamWriterBase.writeXML(self)
        
        project = e5App().getObject("Project")
        if not project.hasDefaultDocstringParameter():
            fileFormatVersion = projectFileFormatVersion
        elif not project.hasDefaultRccCompilerParameters():
            fileFormatVersion = projectFileFormatVersionRcc
        elif not project.hasDefaultUicCompilerParameters():
            fileFormatVersion = projectFileFormatVersionUic
        elif not project.hasDefaultIdlCompilerParameters():
            fileFormatVersion = projectFileFormatVersionIdl
        elif not project.hasDefaultMakeParameters():
            fileFormatVersion = projectFileFormatVersionMake
        elif self.pdata["PROTOCOLS"]:
            fileFormatVersion = projectFileFormatVersionProto
        else:
            fileFormatVersion = projectFileFormatVersionAlt
        
        self.writeDTD('<!DOCTYPE Project SYSTEM "Project-{0}.dtd">'.format(
            fileFormatVersion))
        
        # add some generation comments
        self.writeComment(
            " eric project file for project {0} ".format(self.name))
        if Preferences.getProject("TimestampFile"):
            self.writeComment(
                " Saved: {0} ".format(time.strftime('%Y-%m-%d, %H:%M:%S')))
        self.writeComment(" Copyright (C) {0} {1}, {2} ".format(
            time.strftime('%Y'),
            self.pdata["AUTHOR"],
            self.pdata["EMAIL"]))
        
        # add the main tag
        self.writeStartElement("Project")
        self.writeAttribute("version", fileFormatVersion)
        
        # do the language (used for spell checking)
        self.writeTextElement("Language", self.pdata["SPELLLANGUAGE"])
        if self.pdata["SPELLWORDS"]:
            self.writeTextElement(
                "ProjectWordList",
                Utilities.fromNativeSeparators(self.pdata["SPELLWORDS"]))
        if self.pdata["SPELLEXCLUDES"]:
            self.writeTextElement(
                "ProjectExcludeList",
                Utilities.fromNativeSeparators(self.pdata["SPELLEXCLUDES"]))
        
        # do the hash
        self.writeTextElement("Hash", self.pdata["HASH"])
        
        # do the programming language
        self.writeStartElement("ProgLanguage")
        self.writeAttribute("mixed", str(int(self.pdata["MIXEDLANGUAGE"])))
        self.writeCharacters(self.pdata["PROGLANGUAGE"])
        self.writeEndElement()
        
        # do the UI type
        self.writeTextElement("ProjectType", self.pdata["PROJECTTYPE"])
        
        # do description
        if self.pdata["DESCRIPTION"]:
            self.writeTextElement("Description", self.pdata["DESCRIPTION"])
        
        # do version, author and email
        self.writeTextElement("Version", self.pdata["VERSION"])
        self.writeTextElement("Author", self.pdata["AUTHOR"])
        self.writeTextElement("Email", self.pdata["EMAIL"])
            
        # do the translation pattern
        if self.pdata["TRANSLATIONPATTERN"]:
            self.writeTextElement(
                "TranslationPattern",
                Utilities.fromNativeSeparators(
                    self.pdata["TRANSLATIONPATTERN"]))
        
        # do the binary translations path
        if self.pdata["TRANSLATIONSBINPATH"]:
            self.writeTextElement(
                "TranslationsBinPath",
                Utilities.fromNativeSeparators(
                    self.pdata["TRANSLATIONSBINPATH"]))
        
        # do the eol setting
        if self.pdata["EOL"] >= 0:
            self.writeEmptyElement("Eol")
            self.writeAttribute("index", str(int(self.pdata["EOL"])))
        
        # do the sources
        if self.pdata["SOURCES"]:
            self.writeStartElement("Sources")
            for name in sorted(self.pdata["SOURCES"]):
                self.writeTextElement(
                    "Source", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the forms
        if self.pdata["FORMS"]:
            self.writeStartElement("Forms")
            for name in sorted(self.pdata["FORMS"]):
                self.writeTextElement(
                    "Form", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the translations
        if self.pdata["TRANSLATIONS"]:
            self.writeStartElement("Translations")
            for name in sorted(self.pdata["TRANSLATIONS"]):
                self.writeTextElement(
                    "Translation", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the translation exceptions
        if self.pdata["TRANSLATIONEXCEPTIONS"]:
            self.writeStartElement("TranslationExceptions")
            for name in sorted(self.pdata["TRANSLATIONEXCEPTIONS"]):
                self.writeTextElement(
                    "TranslationException",
                    Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the resources
        if self.pdata["RESOURCES"]:
            self.writeStartElement("Resources")
            for name in sorted(self.pdata["RESOURCES"]):
                self.writeTextElement(
                    "Resource", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the interfaces (IDL)
        if self.pdata["INTERFACES"]:
            self.writeStartElement("Interfaces")
            for name in sorted(self.pdata["INTERFACES"]):
                self.writeTextElement(
                    "Interface", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the protocols (protobuf)
        if self.pdata["PROTOCOLS"]:
            self.writeStartElement("Protocols")
            for name in sorted(self.pdata["PROTOCOLS"]):
                self.writeTextElement(
                    "Protocol", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the others
        if self.pdata["OTHERS"]:
            self.writeStartElement("Others")
            for name in sorted(self.pdata["OTHERS"]):
                self.writeTextElement(
                    "Other", Utilities.fromNativeSeparators(name))
            self.writeEndElement()
        
        # do the main script
        if self.pdata["MAINSCRIPT"]:
            self.writeTextElement(
                "MainScript",
                Utilities.fromNativeSeparators(self.pdata["MAINSCRIPT"]))
        
        # do the vcs stuff
        self.writeStartElement("Vcs")
        if self.pdata["VCS"]:
            self.writeTextElement("VcsType", self.pdata["VCS"])
        if self.pdata["VCSOPTIONS"]:
            self.writeBasics("VcsOptions", self.pdata["VCSOPTIONS"])
        if self.pdata["VCSOTHERDATA"]:
            self.writeBasics("VcsOtherData", self.pdata["VCSOTHERDATA"])
        self.writeEndElement()
        
        # do the filetype associations
        self.writeStartElement("FiletypeAssociations")
        for pattern, filetype in sorted(self.pdata["FILETYPES"].items()):
            self.writeEmptyElement("FiletypeAssociation")
            self.writeAttribute("pattern", pattern)
            self.writeAttribute("type", filetype)
        self.writeEndElement()
        
        # do the lexer associations
        if self.pdata["LEXERASSOCS"]:
            self.writeStartElement("LexerAssociations")
            for pattern, lexer in sorted(self.pdata["LEXERASSOCS"].items()):
                self.writeEmptyElement("LexerAssociation")
                self.writeAttribute("pattern", pattern)
                self.writeAttribute("lexer", lexer)
            self.writeEndElement()
        
        # do the 'make' parameters
        if not e5App().getObject("Project").hasDefaultMakeParameters():
            self.writeStartElement("Make")
            self.writeBasics("MakeParameters", self.pdata["MAKEPARAMS"])
            self.writeEndElement()
        
        # do the 'IDL' parameters
        if not e5App().getObject("Project").hasDefaultIdlCompilerParameters():
            self.writeStartElement("IdlCompiler")
            self.writeBasics("IdlCompilerParameters", self.pdata["IDLPARAMS"])
            self.writeEndElement()
        
        # do the 'uic' parameters
        if not e5App().getObject("Project").hasDefaultUicCompilerParameters():
            self.writeStartElement("UicCompiler")
            self.writeBasics("UicCompilerParameters", self.pdata["UICPARAMS"])
            self.writeEndElement()
        
        # do the 'rcc' parameters
        if not e5App().getObject("Project").hasDefaultRccCompilerParameters():
            self.writeStartElement("RccCompiler")
            self.writeBasics("RccCompilerParameters", self.pdata["RCCPARAMS"])
            self.writeEndElement()
        
        # do the 'docstring' parameter
        if not e5App().getObject("Project").hasDefaultDocstringParameter():
            self.writeTextElement("DocstringStyle", self.pdata["DOCSTRING"])
        
        # do the extra project data stuff
        if len(self.pdata["PROJECTTYPESPECIFICDATA"]):
            self.writeStartElement("ProjectTypeSpecific")
            if self.pdata["PROJECTTYPESPECIFICDATA"]:
                self.writeBasics(
                    "ProjectTypeSpecificData",
                    self.pdata["PROJECTTYPESPECIFICDATA"])
            self.writeEndElement()
        
        # do the documentation generators stuff
        if len(self.pdata["DOCUMENTATIONPARMS"]):
            self.writeStartElement("Documentation")
            if self.pdata["DOCUMENTATIONPARMS"]:
                self.writeBasics(
                    "DocumentationParams", self.pdata["DOCUMENTATIONPARMS"])
            self.writeEndElement()
        
        # do the packagers stuff
        if len(self.pdata["PACKAGERSPARMS"]):
            self.writeStartElement("Packagers")
            if self.pdata["PACKAGERSPARMS"]:
                self.writeBasics(
                    "PackagersParams", self.pdata["PACKAGERSPARMS"])
            self.writeEndElement()
        
        # do the checkers stuff
        if len(self.pdata["CHECKERSPARMS"]):
            self.writeStartElement("Checkers")
            if self.pdata["CHECKERSPARMS"]:
                self.writeBasics(
                    "CheckersParams", self.pdata["CHECKERSPARMS"])
            self.writeEndElement()
        
        # do the other tools stuff
        if len(self.pdata["OTHERTOOLSPARMS"]):
            self.writeStartElement("OtherTools")
            if self.pdata["OTHERTOOLSPARMS"]:
                self.writeBasics(
                    "OtherToolsParams", self.pdata["OTHERTOOLSPARMS"])
            self.writeEndElement()
        
        self.writeEndElement()
        self.writeEndDocument()
