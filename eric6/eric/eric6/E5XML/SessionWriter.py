# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the writer class for writing an XML session file.
"""

import time

from E5Gui.E5Application import e5App

from .XMLStreamWriterBase import XMLStreamWriterBase
from .Config import sessionFileFormatVersion

import Preferences


class SessionWriter(XMLStreamWriterBase):
    """
    Class implementing the writer class for writing an XML session file.
    """
    def __init__(self, device, projectName):
        """
        Constructor
        
        @param device reference to the I/O device to write to
        @type QIODevice
        @param projectName name of the project or None for the
            global session
        @type str or None
        """
        XMLStreamWriterBase.__init__(self, device)
        
        self.name = projectName
        self.project = e5App().getObject("Project")
        self.projectBrowser = e5App().getObject("ProjectBrowser")
        self.multiProject = e5App().getObject("MultiProject")
        self.vm = e5App().getObject("ViewManager")
        self.dbg = e5App().getObject("DebugUI")
        self.dbs = e5App().getObject("DebugServer")
        
    def writeXML(self):
        """
        Public method to write the XML to the file.
        """
        isGlobal = self.name is None
        
        XMLStreamWriterBase.writeXML(self)
        
        self.writeDTD('<!DOCTYPE Session SYSTEM "Session-{0}.dtd">'.format(
            sessionFileFormatVersion))
        
        # add some generation comments
        if not isGlobal:
            self.writeComment(
                " eric session file for project {0} ".format(self.name))
        self.writeComment(
            " This file was generated automatically, do not edit. ")
        if Preferences.getProject("TimestampFile") or isGlobal:
            self.writeComment(
                " Saved: {0} ".format(time.strftime('%Y-%m-%d, %H:%M:%S')))
        
        # add the main tag
        self.writeStartElement("Session")
        self.writeAttribute("version", sessionFileFormatVersion)
        
        # step 0: save open multi project and project for the global session
        if isGlobal:
            if self.multiProject.isOpen():
                self.writeTextElement(
                    "MultiProject", self.multiProject.getMultiProjectFile())
            if self.project.isOpen():
                self.writeTextElement("Project", self.project.getProjectFile())
        
        # step 1: save all open (project) filenames and the active window
        if self.vm.canSplit():
            self.writeEmptyElement("ViewManagerSplits")
            self.writeAttribute("count", str(self.vm.splitCount()))
            self.writeAttribute("orientation",
                                str(self.vm.getSplitOrientation()))
        
        allOpenEditorLists = self.vm.getOpenEditorsForSession()
        editorDict = {}     # remember editors by file name to detect clones
        self.writeStartElement("Filenames")
        for splitIndex, openEditorList in enumerate(allOpenEditorLists):
            for editorIndex, editor in enumerate(openEditorList):
                fileName = editor.getFileName()
                if isGlobal or self.project.isProjectFile(fileName):
                    line, index = editor.getCursorPosition()
                    folds = ','.join(
                        [str(i + 1) for i in editor.contractedFolds()])
                    zoom = editor.getZoom()
                    if fileName in editorDict:
                        isClone = int(editorDict[fileName].isClone(editor))
                    else:
                        isClone = 0
                        editorDict[fileName] = editor
                    self.writeStartElement("Filename")
                    self.writeAttribute("cline", str(line))
                    self.writeAttribute("cindex", str(index))
                    self.writeAttribute("folds", folds)
                    self.writeAttribute("zoom", str(zoom))
                    self.writeAttribute("cloned", str(isClone))
                    self.writeAttribute("splitindex", str(splitIndex))
                    self.writeAttribute("editorindex", str(editorIndex))
                    self.writeCharacters(fileName)
                    self.writeEndElement()
        self.writeEndElement()
        
        aw = self.vm.getActiveName()
        if aw and (isGlobal or self.project.isProjectFile(aw)):
            ed = self.vm.getOpenEditor(aw)
            line, index = ed.getCursorPosition()
            self.writeStartElement("ActiveWindow")
            self.writeAttribute("cline", str(line))
            self.writeAttribute("cindex", str(index))
            self.writeCharacters(aw)
            self.writeEndElement()
        
        # step 2a: save all breakpoints
        allBreaks = Preferences.getProject("SessionAllBreakpoints")
        projectFiles = self.project.getSources(True)
        bpModel = self.dbs.getBreakPointModel()
        self.writeStartElement("Breakpoints")
        for row in range(bpModel.rowCount()):
            index = bpModel.index(row, 0)
            fname, lineno, cond, temp, enabled, count = (
                bpModel.getBreakPointByIndex(index)[:6]
            )
            if isGlobal or allBreaks or fname in projectFiles:
                self.writeStartElement("Breakpoint")
                self.writeTextElement("BpFilename", fname)
                self.writeEmptyElement("Linenumber")
                self.writeAttribute("value", str(lineno))
                self.writeTextElement("Condition", str(cond))
                self.writeEmptyElement("Temporary")
                self.writeAttribute("value", str(temp))
                self.writeEmptyElement("Enabled")
                self.writeAttribute("value", str(enabled))
                self.writeEmptyElement("Count")
                self.writeAttribute("value", str(count))
                self.writeEndElement()
        self.writeEndElement()
        
        # step 2b: save all watch expressions
        self.writeStartElement("Watchexpressions")
        wpModel = self.dbs.getWatchPointModel()
        for row in range(wpModel.rowCount()):
            index = wpModel.index(row, 0)
            cond, special, temp, enabled, count = (
                wpModel.getWatchPointByIndex(index)[:5]
            )
            self.writeStartElement("Watchexpression")
            self.writeTextElement("Condition", str(cond))
            self.writeEmptyElement("Temporary")
            self.writeAttribute("value", str(temp))
            self.writeEmptyElement("Enabled")
            self.writeAttribute("value", str(enabled))
            self.writeEmptyElement("Count")
            self.writeAttribute("value", str(count))
            self.writeTextElement("Special", special)
            self.writeEndElement()
        self.writeEndElement()
        
        # step 3: save the debug info
        self.writeStartElement("DebugInfo")
        if isGlobal:
            if len(self.dbg.argvHistory):
                dbgCmdline = str(self.dbg.argvHistory[0])
            else:
                dbgCmdline = ""
            if len(self.dbg.wdHistory):
                dbgWd = self.dbg.wdHistory[0]
            else:
                dbgWd = ""
            if len(self.dbg.envHistory):
                dbgEnv = self.dbg.envHistory[0]
            else:
                dbgEnv = ""
            if len(self.dbg.multiprocessNoDebugHistory):
                dbgMultiprocessNoDebug = self.dbg.multiprocessNoDebugHistory[0]
            else:
                dbgMultiprocessNoDebug = ""
            
            self.writeTextElement("VirtualEnv", self.dbg.lastUsedVenvName)
            self.writeTextElement("CommandLine", dbgCmdline)
            self.writeTextElement("WorkingDirectory", dbgWd)
            self.writeTextElement("Environment", dbgEnv)
            self.writeEmptyElement("ReportExceptions")
            self.writeAttribute("value", str(self.dbg.exceptions))
            self.writeStartElement("Exceptions")
            for exc in self.dbg.excList:
                self.writeTextElement("Exception", exc)
            self.writeEndElement()
            self.writeStartElement("IgnoredExceptions")
            for iexc in self.dbg.excIgnoreList:
                self.writeTextElement("IgnoredException", iexc)
            self.writeEndElement()
            self.writeEmptyElement("AutoClearShell")
            self.writeAttribute("value", str(self.dbg.autoClearShell))
            self.writeEmptyElement("TracePython")
            self.writeAttribute("value", str(self.dbg.tracePython))
            self.writeEmptyElement("AutoContinue")
            self.writeAttribute("value", str(self.dbg.autoContinue))
            self.writeEmptyElement("EnableMultiprocess")
            self.writeAttribute("value", str(self.dbg.enableMultiprocess))
            self.writeTextElement("MultiprocessNoDebug",
                                  dbgMultiprocessNoDebug)
            self.writeEmptyElement("CovexcPattern")    # kept for compatibility
            self.writeEmptyElement("GlobalConfigOverride")
            self.writeAttribute(
                "enable", str(self.dbg.overrideGlobalConfig["enable"]))
            self.writeAttribute(
                "redirect", str(self.dbg.overrideGlobalConfig["redirect"]))
        else:
            self.writeTextElement("VirtualEnv", self.project.dbgVirtualEnv)
            self.writeTextElement("CommandLine", self.project.dbgCmdline)
            self.writeTextElement("WorkingDirectory", self.project.dbgWd)
            self.writeTextElement("Environment", self.project.dbgEnv)
            self.writeEmptyElement("ReportExceptions")
            self.writeAttribute("value", str(self.project.dbgReportExceptions))
            self.writeStartElement("Exceptions")
            for exc in self.project.dbgExcList:
                self.writeTextElement("Exception", exc)
            self.writeEndElement()
            self.writeStartElement("IgnoredExceptions")
            for iexc in self.project.dbgExcIgnoreList:
                self.writeTextElement("IgnoredException", iexc)
            self.writeEndElement()
            self.writeEmptyElement("AutoClearShell")
            self.writeAttribute("value", str(self.project.dbgAutoClearShell))
            self.writeEmptyElement("TracePython")
            self.writeAttribute("value", str(self.project.dbgTracePython))
            self.writeEmptyElement("AutoContinue")
            self.writeAttribute("value", str(self.project.dbgAutoContinue))
            self.writeEmptyElement("EnableMultiprocess")
            self.writeAttribute("value",
                                str(self.project.dbgEnableMultiprocess))
            self.writeTextElement("MultiprocessNoDebug",
                                  self.project.dbgMultiprocessNoDebug)
            self.writeEmptyElement("CovexcPattern")    # kept for compatibility
            self.writeEmptyElement("GlobalConfigOverride")
            self.writeAttribute(
                "enable", str(self.project.dbgGlobalConfigOverride["enable"]))
            self.writeAttribute(
                "redirect",
                str(self.project.dbgGlobalConfigOverride["redirect"]))
        self.writeEndElement()
        
        # step 4: save bookmarks of all open (project) files
        self.writeStartElement("Bookmarks")
        for fileName in editorDict:
            if isGlobal or self.project.isProjectFile(fileName):
                editor = editorDict[fileName]
                for bookmark in editor.getBookmarks():
                    self.writeStartElement("Bookmark")
                    self.writeTextElement("BmFilename", fileName)
                    self.writeEmptyElement("Linenumber")
                    self.writeAttribute("value", str(bookmark))
                    self.writeEndElement()
        self.writeEndElement()
        
        # step 5: save state of the various project browsers
        if not isGlobal:
            self.writeStartElement("ProjectBrowserStates")
            for browserName in self.projectBrowser.getProjectBrowserNames():
                self.writeStartElement("ProjectBrowserState")
                self.writeAttribute("name", browserName)
                # get the names of expanded files and directories
                names = self.projectBrowser.getProjectBrowser(
                    browserName).getExpandedItemNames()
                for name in names:
                    self.writeTextElement("ExpandedItemName", name)
                self.writeEndElement()
            self.writeEndElement()
        
        # add the main end tag
        self.writeEndElement()
        self.writeEndDocument()
