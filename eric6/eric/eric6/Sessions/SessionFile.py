# -*- coding: utf-8 -*-

# Copyright (c) 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the session JSON file.
"""

import json
import time

from PyQt5.QtCore import QObject

from E5Gui import E5MessageBox
from E5Gui.E5OverrideCursor import E5OverridenCursor
from E5Gui.E5Application import e5App

import Preferences


class SessionFile(QObject):
    """
    Class representing the session JSON file.
    """
    def __init__(self, isGlobal: bool, parent: QObject = None):
        """
        Constructor
        
        @param isGlobal flag indicating a file for a global session
        @type bool
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super(SessionFile, self).__init__(parent)
        
        self.__isGlobal = isGlobal
    
    def writeFile(self, filename: str) -> bool:
        """
        Public method to write the session data to a session JSON file.
        
        @param filename name of the session file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        # get references to objects we need
        project = e5App().getObject("Project")
        projectBrowser = e5App().getObject("ProjectBrowser")
        multiProject = e5App().getObject("MultiProject")
        vm = e5App().getObject("ViewManager")
        dbg = e5App().getObject("DebugUI")
        dbs = e5App().getObject("DebugServer")
        
        # prepare the session data dictionary
        # step 0: header
        sessionDict = {}
        sessionDict["header"] = {}
        if not self.__isGlobal:
            sessionDict["header"]["comment"] = (
                "eric session file for project {0}"
                .format(project.getProjectName())
            )
        sessionDict["header"]["warning"] = (
            "This file was generated automatically, do not edit."
        )
        
        if Preferences.getProject("TimestampFile") or self.__isGlobal:
            sessionDict["header"]["saved"] = (
                time.strftime('%Y-%m-%d, %H:%M:%S')
            )
        
        # step 1: open multi project and project for global session
        sessionDict["MultiProject"] = ""
        sessionDict["Project"] = ""
        if self.__isGlobal:
            if multiProject.isOpen():
                sessionDict["MultiProject"] = (
                    multiProject.getMultiProjectFile()
                )
            if project.isOpen():
                sessionDict["Project"] = project.getProjectFile()
        
        # step 2: all open (project) filenames and the active editor
        if vm.canSplit():
            sessionDict["ViewManagerSplits"] = {
                "Count": vm.splitCount(),
                "Orientation": vm.getSplitOrientation(),
            }
        else:
            sessionDict["ViewManagerSplits"] = {
                "Count": 0,
                "Orientation": 1,
            }
        
        editorsDict = {}    # remember editors by file name to detect clones
        sessionDict["Editors"] = []
        allOpenEditorLists = vm.getOpenEditorsForSession()
        for splitIndex, openEditorList in enumerate(allOpenEditorLists):
            for editorIndex, editor in enumerate(openEditorList):
                fileName = editor.getFileName()
                if self.__isGlobal or project.isProjectFile(fileName):
                    if fileName in editorsDict:
                        isClone = editorsDict[fileName].isClone(editor)
                    else:
                        isClone = False
                        editorsDict[fileName] = editor
                    editorDict = {
                        "Filename": fileName,
                        "Cursor": editor.getCursorPosition(),
                        "Folds": editor.contractedFolds(),
                        "Zoom": editor.getZoom(),
                        "Clone": isClone,
                        "Splitindex": splitIndex,
                        "Editorindex": editorIndex,
                    }
                    sessionDict["Editors"].append(editorDict)
        
        aw = vm.getActiveName()
        sessionDict["ActiveWindow"] = {}
        if aw and (self.__isGlobal or project.isProjectFile(aw)):
            ed = vm.getOpenEditor(aw)
            sessionDict["ActiveWindow"] = {
                "Filename": aw,
                "Cursor": ed.getCursorPosition(),
            }
        
        # step 3: breakpoints
        allBreaks = Preferences.getProject("SessionAllBreakpoints")
        projectFiles = project.getSources(True)
        bpModel = dbs.getBreakPointModel()
        if self.__isGlobal or allBreaks:
            sessionDict["Breakpoints"] = bpModel.getAllBreakpoints()
        else:
            sessionDict["Breakpoints"] = [
                bp
                for bp in bpModel.getAllBreakpoints()
                if bp[0] in projectFiles
            ]
        
        # step 4: watch expressions
        wpModel = dbs.getWatchPointModel()
        sessionDict["Watchpoints"] = wpModel.getAllWatchpoints()
        
        # step 5: debug info
        if self.__isGlobal:
            if len(dbg.argvHistory):
                dbgCmdline = dbg.argvHistory[0]
            else:
                dbgCmdline = ""
            if len(dbg.wdHistory):
                dbgWd = dbg.wdHistory[0]
            else:
                dbgWd = ""
            if len(dbg.envHistory):
                dbgEnv = dbg.envHistory[0]
            else:
                dbgEnv = ""
            if len(dbg.multiprocessNoDebugHistory):
                dbgMultiprocessNoDebug = (
                    dbg.multiprocessNoDebugHistory[0]
                )
            else:
                dbgMultiprocessNoDebug = ""
            sessionDict["DebugInfo"] = {
                "VirtualEnv": dbg.lastUsedVenvName,
                "CommandLine": dbgCmdline,
                "WorkingDirectory": dbgWd,
                "Environment": dbgEnv,
                "ReportExceptions": dbg.exceptions,
                "Exceptions": dbg.excList,
                "IgnoredExceptions": dbg.excIgnoreList,
                "AutoClearShell": dbg.autoClearShell,
                "TracePython": dbg.tracePython,
                "AutoContinue": dbg.autoContinue,
                "EnableMultiprocess": dbg.enableMultiprocess,
                "MultiprocessNoDebug": dbgMultiprocessNoDebug,
                "GlobalConfigOverride": dbg.overrideGlobalConfig,
            }
        else:
            sessionDict["DebugInfo"] = {
                "VirtualEnv": project.dbgVirtualEnv,
                "CommandLine": project.dbgCmdline,
                "WorkingDirectory": project.dbgWd,
                "Environment": project.dbgEnv,
                "ReportExceptions": project.dbgReportExceptions,
                "Exceptions": project.dbgExcList,
                "IgnoredExceptions": project.dbgExcIgnoreList,
                "AutoClearShell": project.dbgAutoClearShell,
                "TracePython": project.dbgTracePython,
                "AutoContinue": project.dbgAutoContinue,
                "EnableMultiprocess": project.dbgEnableMultiprocess,
                "MultiprocessNoDebug": project.dbgMultiprocessNoDebug,
                "GlobalConfigOverride": project.dbgGlobalConfigOverride,
            }
        
        # step 6: bookmarks
        bookmarksList = []
        for fileName in editorsDict:
            if self.__isGlobal or project.isProjectFile(fileName):
                editor = editorsDict[fileName]
                bookmarks = editor.getBookmarks()
                if bookmarks:
                    bookmarksList.append({
                        "Filename": fileName,
                        "Lines": bookmarks,
                    })
        sessionDict["Bookmarks"] = bookmarksList
        
        # step 7: state of the various project browsers
        browsersList = []
        for browserName in projectBrowser.getProjectBrowserNames():
            expandedItems = (
                projectBrowser.getProjectBrowser(browserName)
                .getExpandedItemNames()
            )
            if expandedItems:
                browsersList.append({
                    "Name": browserName,
                    "ExpandedItems": expandedItems,
                })
        sessionDict["ProjectBrowserStates"] = browsersList
        
        try:
            jsonString = json.dumps(sessionDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, EnvironmentError) as err:
            with E5OverridenCursor():
                E5MessageBox.critical(
                    None,
                    self.tr("Save Session"),
                    self.tr(
                        "<p>The session file <b>{0}</b> could not be"
                        " written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the session data from a session JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            sessionDict = json.loads(jsonString)
        except (EnvironmentError, json.JSONDecodeError) as err:
            E5MessageBox.critical(
                None,
                self.tr("Read Session"),
                self.tr(
                    "<p>The session file <b>{0}</b> could not be read.</p>"
                    "<p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        # get references to objects we need
        project = e5App().getObject("Project")
        projectBrowser = e5App().getObject("ProjectBrowser")
        multiProject = e5App().getObject("MultiProject")
        vm = e5App().getObject("ViewManager")
        dbg = e5App().getObject("DebugUI")
        dbs = e5App().getObject("DebugServer")
        
        # step 1: multi project and project
        # =================================
        if sessionDict["MultiProject"]:
            multiProject.openMultiProject(sessionDict["MultiProject"], False)
        if sessionDict["Project"]:
            project.openProject(sessionDict["Project"], False)
        
        # step 2: (project) filenames and the active editor
        # =================================================
        vm.setSplitOrientation(sessionDict["ViewManagerSplits"]["Orientation"])
        vm.setSplitCount(sessionDict["ViewManagerSplits"]["Count"])
        
        editorsDict = {}
        for editorDict in sessionDict["Editors"]:
            if editorDict["Clone"] and editorDict["Filename"] in editorsDict:
                editor = editorsDict[editorDict["Filename"]]
                ed = vm.newEditorView(
                    editorDict["Filename"], editor, editor.getFileType(),
                    indexes=(editorDict["Splitindex"],
                             editorDict["Editorindex"])
                )
            else:
                ed = vm.openSourceFile(
                    editorDict["Filename"],
                    indexes=(editorDict["Splitindex"],
                             editorDict["Editorindex"])
                )
                editorsDict[editorDict["Filename"]] = ed
            if ed is not None:
                ed.zoomTo(editorDict["Zoom"])
                if editorDict["Folds"]:
                    ed.recolor()
                    ed.setContractedFolds(editorDict["Folds"])
                    ed.setCursorPosition(*editorDict["Cursor"])
        
        # step 3: breakpoints
        # ===================
        bpModel = dbs.getBreakPointModel()
        bpModel.addBreakPoints(sessionDict["Breakpoints"])
        
        # step 4: watch expressions
        # =========================
        wpModel = dbs.getWatchPointModel()
        wpModel.addWatchPoints(sessionDict["Watchpoints"])
        
        # step 5: debug info
        # ==================
        debugInfoDict = sessionDict["DebugInfo"]
        
        # adjust for newer session types
        if "GlobalConfigOverride" not in debugInfoDict:
            debugInfoDict["GlobalConfigOverride"] = {
                "enable": False,
                "redirect": True,
            }
        
        dbg.lastUsedVenvName = debugInfoDict["VirtualEnv"]
        dbg.setArgvHistory(debugInfoDict["CommandLine"])
        dbg.setWdHistory(debugInfoDict["WorkingDirectory"])
        dbg.setEnvHistory(debugInfoDict["Environment"])
        dbg.setExceptionReporting(debugInfoDict["ReportExceptions"])
        dbg.setExcList(debugInfoDict["Exceptions"])
        dbg.setExcIgnoreList(debugInfoDict["IgnoredExceptions"])
        dbg.setAutoClearShell(debugInfoDict["AutoClearShell"])
        dbg.setTracePython(debugInfoDict["TracePython"])
        dbg.setAutoContinue(debugInfoDict["AutoContinue"])
        dbg.setEnableMultiprocess(debugInfoDict["EnableMultiprocess"])
        dbg.setMultiprocessNoDebugHistory(debugInfoDict["MultiprocessNoDebug"])
        dbg.setEnableGlobalConfigOverride(
            debugInfoDict["GlobalConfigOverride"])
        if not self.__isGlobal:
            project.setDbgInfo(
                debugInfoDict["VirtualEnv"],
                debugInfoDict["CommandLine"],
                debugInfoDict["WorkingDirectory"],
                debugInfoDict["Environment"],
                debugInfoDict["ReportExceptions"],
                debugInfoDict["Exceptions"],
                debugInfoDict["IgnoredExceptions"],
                debugInfoDict["AutoClearShell"],
                debugInfoDict["TracePython"],
                debugInfoDict["AutoContinue"],
                debugInfoDict["EnableMultiprocess"],
                debugInfoDict["MultiprocessNoDebug"],
                debugInfoDict["GlobalConfigOverride"],
            )
        
        # step 6: bookmarks
        # =================
        for bookmark in sessionDict["Bookmarks"]:
            editor = vm.getOpenEditor(bookmark["Filename"])
            if editor is not None:
                for lineno in bookmark["Lines"]:
                    editor.toggleBookmark(lineno)
        
        # step 7: state of the various project browsers
        # =============================================
        for browserState in sessionDict["ProjectBrowserStates"]:
            browser = projectBrowser.getProjectBrowser(browserState["Name"])
            if browser is not None:
                browser.expandItemsByName(browserState["ExpandedItems"])
        
        # step 8: active window
        # =====================
        if sessionDict["ActiveWindow"]:
            vm.openFiles(sessionDict["ActiveWindow"]["Filename"])
            ed = vm.getOpenEditor(sessionDict["ActiveWindow"]["Filename"])
            if ed is not None:
                ed.setCursorPosition(*sessionDict["ActiveWindow"]["Cursor"])
                ed.ensureCursorVisible()
        
        return True
