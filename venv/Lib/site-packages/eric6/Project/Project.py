# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the project management functionality.
"""

import os
import time
import shutil
import glob
import fnmatch
import copy
import zipfile

from PyQt5.QtCore import (
    pyqtSlot, QFile, QFileInfo, pyqtSignal, QCryptographicHash, QIODevice,
    QByteArray, QObject, QProcess
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QLineEdit, QToolBar, QDialog, QInputDialog, QApplication, QMenu, QAction
)
from PyQt5.Qsci import QsciScintilla

from E5Gui.E5Application import e5App
from E5Gui import E5FileDialog, E5MessageBox
from E5Gui.E5ListSelectionDialog import E5ListSelectionDialog
from E5Gui.E5ProgressDialog import E5ProgressDialog
from E5Gui.E5OverrideCursor import E5OverrideCursor, E5OverridenCursor

from Globals import recentNameProject

import UI.PixmapCache
from UI.NotificationWidget import NotificationTypes

from E5Gui.E5Action import E5Action, createActionGroup

import Preferences
import Utilities

from .ProjectFile import ProjectFile
from .UserProjectFile import UserProjectFile
from .DebuggerPropertiesFile import DebuggerPropertiesFile

from Sessions.SessionFile import SessionFile

from Tasks.TasksFile import TasksFile


class Project(QObject):
    """
    Class implementing the project management functionality.
    
    @signal dirty(bool) emitted when the dirty state changes
    @signal projectLanguageAdded(str) emitted after a new language was added
    @signal projectLanguageAddedByCode(str) emitted after a new language was
        added. The language code is sent by this signal.
    @signal projectLanguageRemoved(str) emitted after a language was removed
    @signal projectFormAdded(str) emitted after a new form was added
    @signal projectFormRemoved(str) emitted after a form was removed
    @signal projectFormCompiled(str) emitted after a form was compiled
    @signal projectSourceAdded(str) emitted after a new source file was added
    @signal projectSourceRemoved(str) emitted after a source was removed
    @signal projectInterfaceAdded(str) emitted after a new IDL file was added
    @signal projectInterfaceRemoved(str) emitted after a IDL file was removed
    @signal projectProtocolAdded(str) emitted after a new proto file was added
    @signal projectProtocolRemoved(str) emitted after a proto file was removed
    @signal projectResourceAdded(str) emitted after a new resource file was
        added
    @signal projectResourceRemoved(str) emitted after a resource was removed
    @signal projectOthersAdded(str) emitted after a file or directory was added
        to the OTHERS project data area
    @signal projectOthersRemoved(str) emitted after a file was removed from the
        OTHERS project data area
    @signal projectAboutToBeCreated() emitted just before the project will be
        created
    @signal newProjectHooks() emitted after a new project was generated but
        before the newProject() signal is sent
    @signal newProject() emitted after a new project was generated
    @signal sourceFile(str) emitted after a project file was read to
        open the main script
    @signal designerFile(str) emitted to open a found designer file
    @signal linguistFile(str) emitted to open a found translation file
    @signal projectOpenedHooks() emitted after a project file was read but
        before the projectOpened() signal is sent
    @signal projectOpened() emitted after a project file was read
    @signal projectClosedHooks() emitted after a project file was closed but
        before the projectClosed() signal is sent
    @signal projectClosed() emitted after a project was closed
    @signal projectFileRenamed(str, str) emitted after a file of the project
        has been renamed
    @signal projectPropertiesChanged() emitted after the project properties
        were changed
    @signal directoryRemoved(str) emitted after a directory has been removed
        from the project
    @signal prepareRepopulateItem(str) emitted before an item of the model is
        repopulated
    @signal completeRepopulateItem(str) emitted after an item of the model was
        repopulated
    @signal vcsStatusMonitorStatus(str, str) emitted to signal the status of
        the monitoring thread (ok, nok, op, off) and a status message
    @signal vcsStatusMonitorInfo(str) emitted to signal some info of the
        monitoring thread
    @signal reinitVCS() emitted after the VCS has been reinitialized
    @signal showMenu(str, QMenu) emitted when a menu is about to be shown. The
        name of the menu and a reference to the menu are given.
    @signal lexerAssociationsChanged() emitted after the lexer associations
        have been changed
    @signal projectChanged() emitted to signal a change of the project
    @signal appendStdout(str) emitted after something was received from
        a QProcess on stdout
    @signal appendStderr(str) emitted after something was received from
        a QProcess on stderr
    """
    dirty = pyqtSignal(bool)
    projectLanguageAdded = pyqtSignal(str)
    projectLanguageAddedByCode = pyqtSignal(str)
    projectLanguageRemoved = pyqtSignal(str)
    projectFormAdded = pyqtSignal(str)
    projectFormRemoved = pyqtSignal(str)
    projectFormCompiled = pyqtSignal(str)
    projectSourceAdded = pyqtSignal(str)
    projectSourceRemoved = pyqtSignal(str)
    projectInterfaceAdded = pyqtSignal(str)
    projectInterfaceRemoved = pyqtSignal(str)
    projectProtocolAdded = pyqtSignal(str)
    projectProtocolRemoved = pyqtSignal(str)
    projectResourceAdded = pyqtSignal(str)
    projectResourceRemoved = pyqtSignal(str)
    projectOthersAdded = pyqtSignal(str)
    projectOthersRemoved = pyqtSignal(str)
    projectAboutToBeCreated = pyqtSignal()
    newProjectHooks = pyqtSignal()
    newProject = pyqtSignal()
    sourceFile = pyqtSignal(str)
    designerFile = pyqtSignal(str)
    linguistFile = pyqtSignal(str)
    projectOpenedHooks = pyqtSignal()
    projectOpened = pyqtSignal()
    projectClosedHooks = pyqtSignal()
    projectClosed = pyqtSignal()
    projectFileRenamed = pyqtSignal(str, str)
    projectPropertiesChanged = pyqtSignal()
    directoryRemoved = pyqtSignal(str)
    prepareRepopulateItem = pyqtSignal(str)
    completeRepopulateItem = pyqtSignal(str)
    vcsStatusMonitorStatus = pyqtSignal(str, str)
    vcsStatusMonitorInfo = pyqtSignal(str)
    reinitVCS = pyqtSignal()
    showMenu = pyqtSignal(str, QMenu)
    lexerAssociationsChanged = pyqtSignal()
    projectChanged = pyqtSignal()
    appendStdout = pyqtSignal(str)
    appendStderr = pyqtSignal(str)
    
    eols = [os.linesep, "\n", "\r", "\r\n"]
    
    DefaultMake = "make"
    DefaultMakefile = "makefile"
    
    def __init__(self, parent=None, filename=None):
        """
        Constructor
        
        @param parent parent widget (usually the ui object) (QWidget)
        @param filename optional filename of a project file to open (string)
        """
        super(Project, self).__init__(parent)
        
        self.ui = parent
        
        self.__progLanguages = [
            "Python3",
            "MicroPython",
            "Ruby",
            "JavaScript",
        ]
        
        self.__dbgFilters = {
            "Python3": self.tr(
                "Python3 Files (*.py *.py3);;"
                "Python3 GUI Files (*.pyw *.pyw3);;"),
        }
        
        self.vcsMenu = None
        self.__makeProcess = None
        
        self.__initProjectTypes()
        
        self.__initData()
        
        self.__projectFile = ProjectFile(self)
        self.__userProjectFile = UserProjectFile(self)
        self.__debuggerPropertiesFile = DebuggerPropertiesFile(self)
        self.__sessionFile = SessionFile(False)
        self.__tasksFile = TasksFile(False)
        
        self.recent = []
        self.__loadRecent()
        
        if filename is not None:
            self.openProject(filename)
        else:
            self.vcs = self.initVCS()
        
        from .ProjectBrowserModel import ProjectBrowserModel
        self.__model = ProjectBrowserModel(self)
        
        self.codemetrics = None
        self.codecoverage = None
        self.profiledata = None
        self.applicationDiagram = None
        self.loadedDiagram = None
        self.__findProjectFileDialog = None
        
    def __sourceExtensions(self, language):
        """
        Private method to get the source extensions of a programming language.
        
        @param language programming language (string)
        @return source extensions (list of string)
        """
        if language == "Python3":
            extensions = Preferences.getPython("Python3Extensions")
            # *.py and *.pyw should always be associated with source files
            for ext in [".py", ".pyw"]:
                if ext not in extensions:
                    extensions.append(ext)
            return extensions
        elif language == "MicroPython":
            extensions = Preferences.getPython("Python3Extensions")
            # *.py should always be associated with source files
            for ext in [".py"]:
                if ext not in extensions:
                    extensions.append(ext)
            return extensions
        elif language == "Ruby":
            return ['.rb']
        elif language == "JavaScript":
            return ['.js']
        elif language == "Mixed":
            return (Preferences.getPython("Python3Extensions") +
                    ['.rb', '.js'])
        else:
            return [""]
        
    def getProgrammingLanguages(self):
        """
        Public method to get the programming languages supported by project.
        
        @return list of supported programming languages (list of string)
        """
        return self.__progLanguages[:]
    
    def getDebuggerFilters(self, language):
        """
        Public method to get the debugger filters for a programming language.
        
        @param language programming language
        @type str
        @return filter string
        @rtype str
        """
        try:
            return self.__dbgFilters[language]
        except KeyError:
            return ""
    
    def __initProjectTypes(self):
        """
        Private method to initialize the list of supported project types.
        """
        self.__fileTypeCallbacks = {}
        self.__lexerAssociationCallbacks = {}
        self.__binaryTranslationsCallbacks = {}
        
        self.__projectTypes = {
            "PyQt5": self.tr("PyQt5 GUI"),
            "PyQt5C": self.tr("PyQt5 Console"),
            "PyQt6": self.tr("PyQt6 GUI"),
            "PyQt6C": self.tr("PyQt6 Console"),
            "E6Plugin": self.tr("Eric6 Plugin"),
            "Console": self.tr("Console"),
            "Other": self.tr("Other"),
        }
        
        self.__projectProgLanguages = {
            "Python3": ["PyQt5", "PyQt5C", "PyQt6", "PyQt6C", "E6Plugin",
                        "Console", "Other"],
            "MicroPython": ["Console", "Other"],
            "Ruby": ["Console", "Other"],
            "JavaScript": ["Other"],
        }
        
        if Utilities.checkPyside(variant=2):
            self.__projectTypes["PySide2"] = self.tr("PySide2 GUI")
            self.__projectTypes["PySide2C"] = self.tr("PySide2 Console")
            self.__projectProgLanguages["Python3"].extend(
                ["PySide2", "PySide2C"])
        
        if Utilities.checkPyside(variant=6):
            self.__projectTypes["PySide6"] = self.tr("PySide6 GUI")
            self.__projectTypes["PySide6C"] = self.tr("PySide6 Console")
            self.__projectProgLanguages["Python3"].extend(
                ["PySide6", "PySide6C"])
        
    def getProjectTypes(self, progLanguage=""):
        """
        Public method to get the list of supported project types.
        
        @param progLanguage programming language to get project types for
            (string)
        @return reference to the dictionary of project types.
        """
        if progLanguage and progLanguage in self.__projectProgLanguages:
            ptypes = {}
            for ptype in self.__projectProgLanguages[progLanguage]:
                ptypes[ptype] = self.__projectTypes[ptype]
            return ptypes
        else:
            return self.__projectTypes
        
    def hasProjectType(self, type_, progLanguage=""):
        """
        Public method to check, if a project type is already registered.
        
        @param type_ internal type designator (string)
        @param progLanguage programming language of the project type (string)
        @return flag indicating presence of the project type (boolean)
        """
        if progLanguage:
            return (
                progLanguage in self.__projectProgLanguages and
                type_ in self.__projectProgLanguages[progLanguage]
            )
        else:
            return type_ in self.__projectTypes
        
    def registerProjectType(self, type_, description, fileTypeCallback=None,
                            binaryTranslationsCallback=None,
                            lexerAssociationCallback=None, progLanguages=None):
        """
        Public method to register a project type.
        
        @param type_ internal type designator to be registered (string)
        @param description more verbose type name (display string) (string)
        @param fileTypeCallback reference to a method returning a dictionary
            of filetype associations.
        @param binaryTranslationsCallback reference to a method returning
            the name of the binary translation file given the name of the raw
            translation file
        @param lexerAssociationCallback reference to a method returning the
            lexer type to be used for syntax highlighting given the name of
            a file
        @param progLanguages programming languages supported by the
            project type (list of string)
        """
        if progLanguages:
            for progLanguage in progLanguages:
                if progLanguage in ["Python", "Python2"]:
                    # ignore that silently for Python2
                    return
                
                if progLanguage not in self.__projectProgLanguages:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Registering Project Type"),
                        self.tr(
                            """<p>The Programming Language <b>{0}</b> is not"""
                            """ supported (project type: {1}).</p>""")
                        .format(progLanguage, type_)
                    )
                    return
                
                if type_ in self.__projectProgLanguages[progLanguage]:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Registering Project Type"),
                        self.tr(
                            """<p>The Project type <b>{0}</b> is already"""
                            """ registered with Programming Language"""
                            """ <b>{1}</b>.</p>""")
                        .format(type_, progLanguage)
                    )
                    return
            
        if type_ in self.__projectTypes:
            E5MessageBox.critical(
                self.ui,
                self.tr("Registering Project Type"),
                self.tr("""<p>The Project type <b>{0}</b> is already"""
                        """ registered.</p>""").format(type_)
            )
        else:
            self.__projectTypes[type_] = description
            self.__fileTypeCallbacks[type_] = fileTypeCallback
            self.__lexerAssociationCallbacks[type_] = lexerAssociationCallback
            self.__binaryTranslationsCallbacks[type_] = (
                binaryTranslationsCallback
            )
            if progLanguages:
                for progLanguage in progLanguages:
                    self.__projectProgLanguages[progLanguage].append(type_)
            else:
                # no specific programming languages given -> add to all
                for progLanguage in self.__projectProgLanguages:
                    self.__projectProgLanguages[progLanguage].append(type_)
        
    def unregisterProjectType(self, type_):
        """
        Public method to unregister a project type.
        
        @param type_ internal type designator to be unregistered (string)
        """
        for progLanguage in self.__projectProgLanguages:
            if type_ in self.__projectProgLanguages[progLanguage]:
                self.__projectProgLanguages[progLanguage].remove(type_)
        if type_ in self.__projectTypes:
            del self.__projectTypes[type_]
        if type_ in self.__fileTypeCallbacks:
            del self.__fileTypeCallbacks[type_]
        if type_ in self.__lexerAssociationCallbacks:
            del self.__lexerAssociationCallbacks[type_]
        if type_ in self.__binaryTranslationsCallbacks:
            del self.__binaryTranslationsCallbacks[type_]
        
    def __initData(self):
        """
        Private method to initialize the project data part.
        """
        self.loaded = False     # flag for the loaded status
        self.__dirty = False      # dirty flag
        self.pfile = ""         # name of the project file
        self.ppath = ""         # name of the project directory
        self.translationsRoot = ""  # the translations prefix
        self.name = ""
        self.opened = False
        self.subdirs = []
        # record the project dir as a relative path (i.e. empty path)
        self.otherssubdirs = []
        self.vcs = None
        self.vcsRequested = False
        self.dbgVirtualEnv = ''
        self.dbgCmdline = ''
        self.dbgWd = ''
        self.dbgEnv = ''
        self.dbgReportExceptions = True
        self.dbgExcList = []
        self.dbgExcIgnoreList = []
        self.dbgAutoClearShell = True
        self.dbgTracePython = False
        self.dbgAutoContinue = True
        self.dbgEnableMultiprocess = True
        self.dbgMultiprocessNoDebug = ""
        self.dbgGlobalConfigOverride = {
            "enable": False,
            "redirect": True,
        }
        
        self.pdata = {
            "DESCRIPTION": "",
            "VERSION": "",
            "SOURCES": [],
            "FORMS": [],
            "RESOURCES": [],
            "INTERFACES": [],
            "PROTOCOLS": [],
            "OTHERS": [],
            "TRANSLATIONS": [],
            "TRANSLATIONEXCEPTIONS": [],
            "TRANSLATIONPATTERN": "",
            "TRANSLATIONSBINPATH": "",
            "MAINSCRIPT": "",
            "VCS": "None",
            "VCSOPTIONS": {},
            "VCSOTHERDATA": {},
            "AUTHOR": '',
            "EMAIL": '',
            "HASH": '',
            "PROGLANGUAGE": "Python3",
            "MIXEDLANGUAGE": False,
            "PROJECTTYPE": "PyQt5",
            "SPELLLANGUAGE":
                Preferences.getEditor("SpellCheckingDefaultLanguage"),
            "SPELLWORDS": '',
            "SPELLEXCLUDES": '',
            "FILETYPES": {},
            "LEXERASSOCS": {},
            "PROJECTTYPESPECIFICDATA": {},
            "CHECKERSPARMS": {},
            "PACKAGERSPARMS": {},
            "DOCUMENTATIONPARMS": {},
            "OTHERTOOLSPARMS": {},
            "MAKEPARAMS": {
                "MakeEnabled": False,
                "MakeExecutable": "",
                "MakeFile": "",
                "MakeTarget": "",
                "MakeParameters": "",
                "MakeTestOnly": True,
            },
            "IDLPARAMS": {
                "IncludeDirs": [],
                "DefinedNames": [],
                "UndefinedNames": [],
            },
            "UICPARAMS": {
                "Package": "",
                "RcSuffix": "",
                "PackagesRoot": "",
            },
            "RCCPARAMS": {
                "CompressionThreshold": 70,     # default value
                "CompressLevel": 0,             # use zlib default
                "CompressionDisable": False,
                "PathPrefix": "",
            },
            "EOL": -1,
            "DOCSTRING": "",
        }
        
        self.__initDebugProperties()
        
        self.pudata = {
            "VCSOVERRIDE": "",
            "VCSSTATUSMONITORINTERVAL": 0,
        }
        
        self.vcs = self.initVCS()
        
    def getData(self, category, key):
        """
        Public method to get data out of the project data store.
        
        @param category category of the data to get (string, one of
            PROJECTTYPESPECIFICDATA, CHECKERSPARMS, PACKAGERSPARMS,
            DOCUMENTATIONPARMS or OTHERTOOLSPARMS)
        @param key key of the data entry to get (string).
        @return a copy of the requested data or None
        """
        # __IGNORE_WARNING_D202__
        if (
            category in ["PROJECTTYPESPECIFICDATA", "CHECKERSPARMS",
                         "PACKAGERSPARMS", "DOCUMENTATIONPARMS",
                         "OTHERTOOLSPARMS"] and
            key in self.pdata[category]
        ):
            return copy.deepcopy(self.pdata[category][key])
        else:
            return None
        
    def setData(self, category, key, data):
        """
        Public method to store data in the project data store.
        
        @param category category of the data to get (string, one of
            PROJECTTYPESPECIFICDATA, CHECKERSPARMS, PACKAGERSPARMS,
            DOCUMENTATIONPARMS or OTHERTOOLSPARMS)
        @param key key of the data entry to get (string).
        @param data data to be stored
        @return flag indicating success (boolean)
        """
        # __IGNORE_WARNING_D202__
        if category not in ["PROJECTTYPESPECIFICDATA", "CHECKERSPARMS",
                            "PACKAGERSPARMS", "DOCUMENTATIONPARMS",
                            "OTHERTOOLSPARMS"]:
            return False
        
        # test for changes of data and save them in the project
        # 1. there were none, now there are
        if key not in self.pdata[category] and len(data) > 0:
            self.pdata[category][key] = copy.deepcopy(data)
            self.setDirty(True)
        # 2. there were some, now there aren't
        elif key in self.pdata[category] and len(data) == 0:
            del self.pdata[category][key]
            self.setDirty(True)
        # 3. there were some and still are
        elif key in self.pdata[category] and len(data) > 0:
            if data != self.pdata[category][key]:
                self.pdata[category][key] = copy.deepcopy(data)
                self.setDirty(True)
        # 4. there were none and none are given
        else:
            return False
        return True
        
    def initFileTypes(self):
        """
        Public method to initialize the filetype associations with default
        values.
        """
        self.pdata["FILETYPES"] = {
            "*.txt": "OTHERS",
            "*.md": "OTHERS",
            "*.rst": "OTHERS",
            "README": "OTHERS",
            "README.*": "OTHERS",
            "*.e4p": "OTHERS",
            "*.epj": "OTHERS",
            "GNUmakefile": "OTHERS",
            "makefile": "OTHERS",
            "Makefile": "OTHERS",
        }
        
        # Sources
        if self.pdata["MIXEDLANGUAGE"]:
            sourceKey = "Mixed"
        else:
            sourceKey = self.pdata["PROGLANGUAGE"]
        for ext in self.__sourceExtensions(sourceKey):
            self.pdata["FILETYPES"]["*{0}".format(ext)] = "SOURCES"
        
        # IDL interfaces
        self.pdata["FILETYPES"]["*.idl"] = "INTERFACES"
        
        # Protobuf Files
        self.pdata["FILETYPES"]["*.proto"] = "PROTOCOLS"
        
        # Forms
        if self.pdata["PROJECTTYPE"] in ["E6Plugin",
                                         "PyQt5",
                                         "PyQt6",
                                         "PySide2",
                                         "PySide6"]:
            self.pdata["FILETYPES"]["*.ui"] = "FORMS"
        
        # Resources
        if self.pdata["PROJECTTYPE"] in ["E6Plugin",
                                         "PyQt5", "PyQt5C",
                                         "PySide2", "PySide2C",
                                         "PySide6", "PySide6C"]:
            self.pdata["FILETYPES"]["*.qrc"] = "RESOURCES"
        
        # Translations
        if self.pdata["PROJECTTYPE"] in ["E6Plugin",
                                         "PyQt5", "PyQt5C",
                                         "PyQt6", "PyQt6C",
                                         "PySide2", "PySide2C",
                                         "PySide6", "PySide6C"]:
            self.pdata["FILETYPES"]["*.ts"] = "TRANSLATIONS"
            self.pdata["FILETYPES"]["*.qm"] = "TRANSLATIONS"
        
        # Project type specific ones
        try:
            if self.__fileTypeCallbacks[
                    self.pdata["PROJECTTYPE"]] is not None:
                ftypes = self.__fileTypeCallbacks[self.pdata["PROJECTTYPE"]]()
                self.pdata["FILETYPES"].update(ftypes)
        except KeyError:
            pass
        
        self.setDirty(True)
        
    def updateFileTypes(self):
        """
        Public method to update the filetype associations with new default
        values.
        """
        if self.pdata["PROJECTTYPE"] in ["E6Plugin",
                                         "PyQt5", "PyQt5C",
                                         "PyQt6", "PyQt6C",
                                         "PySide2", "PySide2C",
                                         "PySide6", "PySide6C"]:
            if "*.ts" not in self.pdata["FILETYPES"]:
                self.pdata["FILETYPES"]["*.ts"] = "TRANSLATIONS"
            if "*.qm" not in self.pdata["FILETYPES"]:
                self.pdata["FILETYPES"]["*.qm"] = "TRANSLATIONS"
        try:
            if self.__fileTypeCallbacks[
                    self.pdata["PROJECTTYPE"]] is not None:
                ftypes = self.__fileTypeCallbacks[self.pdata["PROJECTTYPE"]]()
                for pattern, ftype in list(ftypes.items()):
                    if pattern not in self.pdata["FILETYPES"]:
                        self.pdata["FILETYPES"][pattern] = ftype
                        self.setDirty(True)
        except KeyError:
            pass
        
    def __loadRecent(self):
        """
        Private method to load the recently opened project filenames.
        """
        self.recent = []
        Preferences.Prefs.rsettings.sync()
        rp = Preferences.Prefs.rsettings.value(recentNameProject)
        if rp is not None:
            for f in rp:
                if QFileInfo(f).exists():
                    self.recent.append(f)
    
    def __saveRecent(self):
        """
        Private method to save the list of recently opened filenames.
        """
        Preferences.Prefs.rsettings.setValue(recentNameProject, self.recent)
        Preferences.Prefs.rsettings.sync()
        
    def getMostRecent(self):
        """
        Public method to get the most recently opened project.
        
        @return path of the most recently opened project (string)
        """
        if len(self.recent):
            return self.recent[0]
        else:
            return None
        
    def getModel(self):
        """
        Public method to get a reference to the project browser model.
        
        @return reference to the project browser model (ProjectBrowserModel)
        """
        return self.__model
    
    def startFileSystemMonitoring(self):
        """
        Public method to (re)start monitoring the project file system.
        """
        self.__model.startFileSystemMonitoring()
    
    def stopFileSystemMonitoring(self):
        """
        Public method to stop monitoring the project file system.
        """
        self.__model.stopFileSystemMonitoring()
        
    def getVcs(self):
        """
        Public method to get a reference to the VCS object.
        
        @return reference to the VCS object
        """
        return self.vcs
        
    def handlePreferencesChanged(self):
        """
        Public slot used to handle the preferencesChanged signal.
        """
        if self.pudata["VCSSTATUSMONITORINTERVAL"]:
            self.setStatusMonitorInterval(
                self.pudata["VCSSTATUSMONITORINTERVAL"])
        else:
            self.setStatusMonitorInterval(
                Preferences.getVCS("StatusMonitorInterval"))
        
        self.__model.preferencesChanged()
        
    def setDirty(self, dirty):
        """
        Public method to set the dirty state.
        
        It emits the signal dirty(bool).
        
        @param dirty dirty state
        @type bool
        """
        self.__dirty = dirty
        self.saveAct.setEnabled(dirty)
        self.dirty.emit(dirty)
        if self.__dirty:
            self.projectChanged.emit()
        
    def isDirty(self):
        """
        Public method to return the dirty state.
        
        @return dirty state (boolean)
        """
        return self.__dirty
        
    def isOpen(self):
        """
        Public method to return the opened state.
        
        @return open state (boolean)
        """
        return self.opened
        
    def __checkFilesExist(self, index):
        """
        Private method to check, if the files in a list exist.
        
        The files in the indicated list are checked for existance in the
        filesystem. Non existant files are removed from the list and the
        dirty state of the project is changed accordingly.
        
        @param index key of the list to be checked (string)
        """
        removed = False
        removelist = []
        for file in self.pdata[index]:
            if not os.path.exists(os.path.join(self.ppath, file)):
                removelist.append(file)
                removed = True
                
        if removed:
            for file in removelist:
                self.pdata[index].remove(file)
            self.setDirty(True)
        
    def __readProject(self, fn):
        """
        Private method to read in a project (.epj or .e4p) file.
        
        @param fn filename of the project file to be read (string)
        @return flag indicating success
        """
        if os.path.splitext(fn)[1] == ".epj":
            # new JSON based format
            with E5OverrideCursor():
                res = self.__projectFile.readFile(fn)
        else:
            # old XML based format
            f = QFile(fn)
            if f.open(QIODevice.OpenModeFlag.ReadOnly):
                from E5XML.ProjectReader import ProjectReader
                reader = ProjectReader(f, self)
                reader.readXML()
                res = not reader.hasError()
                f.close()
                
                # create hash value, if it doesn't have one
                if reader.version.startswith("5.") and not self.pdata["HASH"]:
                    hashStr = str(QCryptographicHash.hash(
                        QByteArray(self.ppath.encode("utf-8")),
                        QCryptographicHash.Algorithm.Sha1).toHex(),
                        encoding="utf-8")
                    self.pdata["HASH"] = hashStr
                    self.setDirty(True)
            else:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Read Project File"),
                    self.tr(
                        "<p>The project file <b>{0}</b> could not be read."
                        "</p>")
                    .format(fn))
                res = False
        
        if res:
            self.pfile = os.path.abspath(fn)
            self.ppath = os.path.abspath(os.path.dirname(fn))
            
            # insert filename into list of recently opened projects
            self.__syncRecent()
            
            if self.pdata["TRANSLATIONPATTERN"]:
                self.translationsRoot = self.pdata["TRANSLATIONPATTERN"].split(
                    "%language%")[0]
            elif self.pdata["MAINSCRIPT"]:
                self.translationsRoot = os.path.splitext(
                    self.pdata["MAINSCRIPT"])[0]
            if os.path.isdir(os.path.join(self.ppath, self.translationsRoot)):
                dn = self.translationsRoot
            else:
                dn = os.path.dirname(self.translationsRoot)
            if dn not in self.subdirs:
                self.subdirs.append(dn)
                
            self.name = os.path.splitext(os.path.basename(fn))[0]
            
            # check, if the files of the project still exist in the
            # project directory
            self.__checkFilesExist("SOURCES")
            self.__checkFilesExist("FORMS")
            self.__checkFilesExist("INTERFACES")
            self.__checkFilesExist("PROTOCOLS")
            self.__checkFilesExist("TRANSLATIONS")
            self.__checkFilesExist("RESOURCES")
            self.__checkFilesExist("OTHERS")
            
            # get the names of subdirectories the files are stored in
            for fn in (
                self.pdata["SOURCES"] +
                self.pdata["FORMS"] +
                self.pdata["INTERFACES"] +
                self.pdata["PROTOCOLS"] +
                self.pdata["RESOURCES"] +
                self.pdata["TRANSLATIONS"]
            ):
                dn = os.path.dirname(fn)
                if dn not in self.subdirs:
                    self.subdirs.append(dn)
            
            # get the names of other subdirectories
            for fn in self.pdata["OTHERS"]:
                dn = os.path.dirname(fn)
                if dn not in self.otherssubdirs:
                    self.otherssubdirs.append(dn)
            
        return res

    def __writeProject(self, fn=None):
        """
        Private method to save the project infos to a project file.
        
        @param fn optional filename of the project file to be written (string).
            If fn is None, the filename stored in the project object
            is used. This is the 'save' action. If fn is given, this filename
            is used instead of the one in the project object. This is the
            'save as' action.
        @return flag indicating success
        """
        if self.vcs is not None:
            self.pdata["VCSOPTIONS"] = copy.deepcopy(self.vcs.vcsGetOptions())
            self.pdata["VCSOTHERDATA"] = copy.deepcopy(
                self.vcs.vcsGetOtherData())
        
        if not self.pdata["HASH"]:
            hashStr = str(QCryptographicHash.hash(
                QByteArray(self.ppath.encode("utf-8")),
                QCryptographicHash.Algorithm.Sha1).toHex(),
                encoding="utf-8")
            self.pdata["HASH"] = hashStr
        
        if fn is None:
            fn = self.pfile
        
        if os.path.splitext(fn)[1] == ".epj":
            # new JSON based format
            with E5OverrideCursor():
                res = self.__projectFile.writeFile(fn)
        else:
            # old XML based format
            f = QFile(fn)
            if f.open(QIODevice.OpenModeFlag.WriteOnly):
                from E5XML.ProjectWriter import ProjectWriter
                ProjectWriter(f, os.path.splitext(
                    os.path.basename(fn))[0]).writeXML()
                res = True
            else:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Save Project File"),
                    self.tr(
                        "<p>The project file <b>{0}</b> could not be"
                        " written.</p>").format(fn))
                res = False
        
        if res:
            self.pfile = os.path.abspath(fn)
            self.ppath = os.path.abspath(os.path.dirname(fn))
            self.name = os.path.splitext(os.path.basename(fn))[0]
            self.setDirty(False)
            
            # insert filename into list of recently opened projects
            self.__syncRecent()
        
        return res
        
    def __readUserProperties(self):
        """
        Private method to read in the user specific project file (.eqj or
        .e4q).
        """
        if self.pfile is None:
            return
        
        fn1, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(),
                          '{0}.eqj'.format(fn1))
        if os.path.exists(fn):
            # try the new JSON based format first
            self.__userProjectFile.readFile(fn)
        else:
            # try the old XML based format second
            fn = os.path.join(self.getProjectManagementDir(),
                              '{0}.e4q'.format(fn1))
            if os.path.exists(fn):
                f = QFile(fn)
                if f.open(QIODevice.OpenModeFlag.ReadOnly):
                    from E5XML.UserProjectReader import UserProjectReader
                    reader = UserProjectReader(f, self)
                    reader.readXML()
                    f.close()
                else:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Read User Project Properties"),
                        self.tr(
                            "<p>The user specific project properties file"
                            " <b>{0}</b> could not be read.</p>").format(fn))
        
    def __writeUserProperties(self):
        """
        Private method to write the user specific project data to a JSON file.
        """
        if self.pfile is None:
            return
        
        fn, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(), '{0}.eqj'.format(fn))
        
        with E5OverrideCursor():
            self.__userProjectFile.writeFile(fn)
    
    def __showContextMenuSession(self):
        """
        Private slot called before the Session menu is shown.
        """
        enable = True
        if self.pfile is None:
            enable = False
        else:
            fn, ext = os.path.splitext(os.path.basename(self.pfile))
            fn_new = os.path.join(self.getProjectManagementDir(),
                                  '{0}.esj'.format(fn))
            fn_old = os.path.join(self.getProjectManagementDir(),
                                  '{0}.e5s'.format(fn))
            enable = os.path.exists(fn_new) or os.path.exists(fn_old)
        self.sessActGrp.findChild(
            QAction, "project_load_session").setEnabled(enable)
        self.sessActGrp.findChild(
            QAction, "project_delete_session").setEnabled(enable)
        
    @pyqtSlot()
    def __readSession(self, quiet=False, indicator=""):
        """
        Private method to read in the project session file (.esj or .e5s).
        
        @param quiet flag indicating quiet operations.
                If this flag is true, no errors are reported.
        @param indicator indicator string (string)
        """
        if self.pfile is None:
            if not quiet:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Read Project Session"),
                    self.tr("Please save the project first."))
            return
            
        fn1, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(),
                          '{0}{1}.esj'.format(fn1, indicator))
        if os.path.exists(fn):
            # try the new JSON based format first
            self.__sessionFile.readFile(fn)
        else:
            # try the old XML based format second
            fn = os.path.join(self.getProjectManagementDir(),
                              '{0}{1}.e5s'.format(fn1, indicator))
            if os.path.exists(fn):
                f = QFile(fn)
                if f.open(QIODevice.OpenModeFlag.ReadOnly):
                    from E5XML.SessionReader import SessionReader
                    reader = SessionReader(f, False)
                    reader.readXML(quiet=quiet)
                    f.close()
                else:
                    if not quiet:
                        E5MessageBox.critical(
                            self.ui,
                            self.tr("Read project session"),
                            self.tr(
                                "<p>The project session file <b>{0}</b> could"
                                " not be read.</p>").format(fn))
        
    @pyqtSlot()
    def __writeSession(self, quiet=False, indicator=""):
        """
        Private method to write the session data to an XML file (.esj).
        
        @param quiet flag indicating quiet operations.
            If this flag is true, no errors are reported.
        @param indicator indicator string (string)
        """
        if self.pfile is None:
            if not quiet:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Save Project Session"),
                    self.tr("Please save the project first."))
            return
        
        fn, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(),
                          '{0}{1}.esj'.format(fn, indicator))
        
        self.__sessionFile.writeFile(fn)
    
    def __deleteSession(self):
        """
        Private method to delete the session file.
        """
        if self.pfile is None:
            E5MessageBox.critical(
                self.ui,
                self.tr("Delete Project Session"),
                self.tr("Please save the project first."))
            return
            
        fname, ext = os.path.splitext(os.path.basename(self.pfile))
        
        for ext in (".esj", ".e5s", ".e4s"):
            fn = os.path.join(
                self.getProjectManagementDir(), "{0}{1}".format(fname, ext)),
            if os.path.exists(fn):
                try:
                    os.remove(fn)
                except OSError:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Delete Project Session"),
                        self.tr(
                            "<p>The project session file <b>{0}</b> could"
                            " not be deleted.</p>").format(fn))
        
    def __readTasks(self):
        """
        Private method to read in the project tasks file (.etj or .e6t).
        """
        if self.pfile is None:
            E5MessageBox.critical(
                self.ui,
                self.tr("Read Tasks"),
                self.tr("Please save the project first."))
            return
        
        base, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(),
                          '{0}.etj'.format(base))
        if os.path.exists(fn):
            # try new style JSON file first
            self.__tasksFile.readFile(fn)
        else:
            # try old style XML file second
            fn = os.path.join(self.getProjectManagementDir(),
                              '{0}.e6t'.format(base))
            if os.path.exists(fn):
                f = QFile(fn)
                if f.open(QIODevice.OpenModeFlag.ReadOnly):
                    from E5XML.TasksReader import TasksReader
                    reader = TasksReader(f, True)
                    reader.readXML()
                    f.close()
                else:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Read Tasks"),
                        self.tr(
                            "<p>The tasks file <b>{0}</b> could not be read."
                            "</p>")
                        .format(fn))
        
    def writeTasks(self):
        """
        Public method to write the tasks data to a JSON file (.etj).
        """
        if self.pfile is None:
            return
            
        fn, ext = os.path.splitext(os.path.basename(self.pfile))
        
        fn = os.path.join(self.getProjectManagementDir(),
                          '{0}.etj'.format(fn))
        self.__tasksFile.writeFile(fn)
    
    def __showContextMenuDebugger(self):
        """
        Private slot called before the Debugger menu is shown.
        """
        enable = True
        if self.pfile is None:
            enable = False
        else:
            fn, ext = os.path.splitext(os.path.basename(self.pfile))
            # try new style file first
            fn = os.path.join(self.getProjectManagementDir(),
                              '{0}.edj'.format(fn))
            if not os.path.exists(fn):
                # try old style file second
                fn = os.path.join(self.getProjectManagementDir(),
                                  '{0}.e4d'.format(fn))
            enable = os.path.exists(fn)
        self.dbgActGrp.findChild(
            QAction, "project_debugger_properties_load").setEnabled(enable)
        self.dbgActGrp.findChild(
            QAction, "project_debugger_properties_delete").setEnabled(enable)
        
    @pyqtSlot()
    def __readDebugProperties(self, quiet=False):
        """
        Private method to read in the project debugger properties file
        (.edj or .e4d).
        
        @param quiet flag indicating quiet operations.
            If this flag is true, no errors are reported.
        """
        if self.pfile is None:
            if not quiet:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Read Debugger Properties"),
                    self.tr("Please save the project first."))
            return
        
        fn1, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(),
                          '{0}.edj'.format(fn1))
        if os.path.exists(fn):
            # try the new JSON based format first
            self.__debuggerPropertiesFile.readFile(fn)
        else:
            # try the old XML based format second
            fn = os.path.join(self.getProjectManagementDir(),
                              '{0}.e4d'.format(fn1))
            
            f = QFile(fn)
            if f.open(QIODevice.OpenModeFlag.ReadOnly):
                from E5XML.DebuggerPropertiesReader import (
                    DebuggerPropertiesReader
                )
                reader = DebuggerPropertiesReader(f, self)
                reader.readXML(quiet=quiet)
                f.close()
                self.debugPropertiesLoaded = True
                self.debugPropertiesChanged = False
            else:
                if not quiet:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Read Debugger Properties"),
                        self.tr(
                            "<p>The project debugger properties file"
                            " <b>{0}</b> could not be read.</p>").format(fn))
    
    @pyqtSlot()
    def __writeDebugProperties(self, quiet=False):
        """
        Private method to write the project debugger properties file (.edj).
        
        @param quiet flag indicating quiet operations.
                If this flag is true, no errors are reported.
        """
        if self.pfile is None:
            if not quiet:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Save Debugger Properties"),
                    self.tr("Please save the project first."))
            return
        
        fn, ext = os.path.splitext(os.path.basename(self.pfile))
        fn = os.path.join(self.getProjectManagementDir(), '{0}.edj'.format(fn))
        
        with E5OverrideCursor():
            self.__debuggerPropertiesFile.writeFile(fn)
    
    def __deleteDebugProperties(self):
        """
        Private method to delete the project debugger properties file
        (.edj or .e4d).
        """
        if self.pfile is None:
            E5MessageBox.critical(
                self.ui,
                self.tr("Delete Debugger Properties"),
                self.tr("Please save the project first."))
            return
            
        fname, ext = os.path.splitext(os.path.basename(self.pfile))
        
        for ext in (".edj", ".e4d"):
            fn = os.path.join(self.getProjectManagementDir(),
                              "{0}{1}".format(fname, ext))
            if os.path.exists(fn):
                try:
                    os.remove(fn)
                except OSError:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Delete Debugger Properties"),
                        self.tr(
                            "<p>The project debugger properties file"
                            " <b>{0}</b> could not be deleted.</p>")
                        .format(fn))
        
    def __initDebugProperties(self):
        """
        Private method to initialize the debug properties.
        """
        self.debugPropertiesLoaded = False
        self.debugPropertiesChanged = False
        self.debugProperties = {
            "VIRTUALENV": "",
            "DEBUGCLIENT": "",
            "ENVIRONMENTOVERRIDE": False,
            "ENVIRONMENTSTRING": "",
            "REMOTEDEBUGGER": False,
            "REMOTEHOST": "",
            "REMOTECOMMAND": "",
            "PATHTRANSLATION": False,
            "REMOTEPATH": "",
            "LOCALPATH": "",
            "CONSOLEDEBUGGER": False,
            "CONSOLECOMMAND": "",
            "REDIRECT": False,
            "NOENCODING": False,
        }
    
    def isDebugPropertiesLoaded(self):
        """
        Public method to return the status of the debug properties.
        
        @return load status of debug properties (boolean)
        """
        return self.debugPropertiesLoaded
        
    def __showDebugProperties(self):
        """
        Private slot to display the debugger properties dialog.
        """
        from .DebuggerPropertiesDialog import DebuggerPropertiesDialog
        dlg = DebuggerPropertiesDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.storeData()
        
    def getDebugProperty(self, key):
        """
        Public method to retrieve a debugger property.
        
        @param key key of the property (string)
        @return value of the property
        """
        if key == "INTERPRETER":
            return (
                e5App().getObject("VirtualEnvManager")
                .getVirtualenvInterpreter(self.debugProperties["VIRTUALENV"])
            )
        else:
            return self.debugProperties[key]
    
    def setDbgInfo(self, venvName, argv, wd, env, excReporting, excList,
                   excIgnoreList, autoClearShell, tracePython=None,
                   autoContinue=None, enableMultiprocess=None,
                   multiprocessNoDebug=None, configOverride=None):
        """
        Public method to set the debugging information.
        
        @param venvName name of the virtual environment used
        @type str
        @param argv command line arguments to be used
        @type str
        @param wd working directory
        @type str
        @param env environment setting
        @type str
        @param excReporting flag indicating the highlighting of exceptions
        @type bool
        @param excList list of exceptions to be highlighted
        @type list of str
        @param excIgnoreList list of exceptions to be ignored
        @type list of str
        @param autoClearShell flag indicating, that the interpreter window
            should be cleared
        @type bool
        @param tracePython flag to indicate if the Python library should be
            traced as well
        @type bool
        @param autoContinue flag indicating, that the debugger should not
            stop at the first executable line
        @type bool
        @param enableMultiprocess flag indicating, that the debugger should
            run in multi process mode
        @type bool
        @param multiprocessNoDebug list of programs not to be debugged in
            multi process mode
        @type str
        @param configOverride dictionary containing the global config override
            data
        @type dict
        """
        self.dbgVirtualEnv = venvName
        self.dbgCmdline = argv
        self.dbgWd = wd
        self.dbgEnv = env
        self.dbgReportExceptions = excReporting
        self.dbgExcList = excList[:]                # keep a copy of the list
        self.dbgExcIgnoreList = excIgnoreList[:]    # keep a copy of the list
        self.dbgAutoClearShell = autoClearShell
        if tracePython is not None:
            self.dbgTracePython = tracePython
        if autoContinue is not None:
            self.dbgAutoContinue = autoContinue
        if enableMultiprocess is not None:
            self.dbgEnableMultiprocess = enableMultiprocess
        if multiprocessNoDebug is not None:
            self.dbgMultiprocessNoDebug = multiprocessNoDebug
        if configOverride is not None:
            self.dbgGlobalConfigOverride = copy.deepcopy(configOverride)
    
    def getTranslationPattern(self):
        """
        Public method to get the translation pattern.
        
        @return translation pattern (string)
        """
        return self.pdata["TRANSLATIONPATTERN"]
    
    def setTranslationPattern(self, pattern):
        """
        Public method to set the translation pattern.
        
        @param pattern translation pattern
        @type str
        """
        self.pdata["TRANSLATIONPATTERN"] = pattern
    
    def addLanguage(self):
        """
        Public slot used to add a language to the project.
        """
        if not self.pdata["TRANSLATIONPATTERN"]:
            E5MessageBox.critical(
                self.ui,
                self.tr("Add Language"),
                self.tr(
                    "You have to specify a translation pattern first."))
            return
        
        from .AddLanguageDialog import AddLanguageDialog
        dlg = AddLanguageDialog(self.parent())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            lang = dlg.getSelectedLanguage()
            if self.pdata["PROJECTTYPE"] in [
                "PyQt5", "PyQt5C", "PyQt6", "PyQt6C", "E6Plugin",
                "PySide2", "PySide2C", "PySide6", "PySide6C"
            ]:
                langFile = self.pdata["TRANSLATIONPATTERN"].replace(
                    "%language%", lang)
                self.appendFile(langFile)
            self.projectLanguageAddedByCode.emit(lang)
        
    def __binaryTranslationFile(self, langFile):
        """
        Private method to calculate the filename of the binary translations
        file given the name of the raw translations file.
        
        @param langFile name of the raw translations file (string)
        @return name of the binary translations file (string)
        """
        qmFile = ""
        try:
            if self.__binaryTranslationsCallbacks[
                    self.pdata["PROJECTTYPE"]] is not None:
                qmFile = self.__binaryTranslationsCallbacks[
                    self.pdata["PROJECTTYPE"]](langFile)
        except KeyError:
            qmFile = langFile.replace('.ts', '.qm')
        if qmFile == langFile:
            qmFile = ""
        return qmFile
        
    def checkLanguageFiles(self):
        """
        Public slot to check the language files after a release process.
        """
        tbPath = self.pdata["TRANSLATIONSBINPATH"]
        for langFile in self.pdata["TRANSLATIONS"][:]:
            qmFile = self.__binaryTranslationFile(langFile)
            if qmFile:
                if (
                    qmFile not in self.pdata["TRANSLATIONS"] and
                    os.path.exists(os.path.join(self.ppath, qmFile))
                ):
                    self.appendFile(qmFile)
                if tbPath:
                    qmFile = os.path.join(tbPath, os.path.basename(qmFile))
                    if (
                        qmFile not in self.pdata["TRANSLATIONS"] and
                        os.path.exists(os.path.join(self.ppath, qmFile))
                    ):
                        self.appendFile(qmFile)
        
    def removeLanguageFile(self, langFile):
        """
        Public slot to remove a translation from the project.
        
        The translation file is not deleted from the project directory.
        
        @param langFile the translation file to be removed (string)
        """
        langFile = self.getRelativePath(langFile)
        qmFile = self.__binaryTranslationFile(langFile)
        self.pdata["TRANSLATIONS"].remove(langFile)
        self.__model.removeItem(langFile)
        if qmFile:
            try:
                if self.pdata["TRANSLATIONSBINPATH"]:
                    qmFile = self.getRelativePath(
                        os.path.join(self.pdata["TRANSLATIONSBINPATH"],
                                     os.path.basename(qmFile)))
                self.pdata["TRANSLATIONS"].remove(qmFile)
                self.__model.removeItem(qmFile)
            except ValueError:
                pass
        self.setDirty(True)
        
    def deleteLanguageFile(self, langFile):
        """
        Public slot to delete a translation from the project directory.
        
        @param langFile the translation file to be removed (string)
        """
        try:
            from ThirdParty.Send2Trash.send2trash import send2trash as s2t
        except ImportError:
            s2t = os.remove
        
        langFile = self.getRelativePath(langFile)
        qmFile = self.__binaryTranslationFile(langFile)
        
        try:
            fn = os.path.join(self.ppath, langFile)
            if os.path.exists(fn):
                s2t(fn)
        except OSError as err:
            E5MessageBox.critical(
                self.ui,
                self.tr("Delete translation"),
                self.tr(
                    "<p>The selected translation file <b>{0}</b> could not be"
                    " deleted.</p><p>Reason: {1}</p>").format(
                    langFile, str(err)))
            return
        
        self.removeLanguageFile(langFile)
        
        # now get rid of the .qm file
        if qmFile:
            try:
                if self.pdata["TRANSLATIONSBINPATH"]:
                    qmFile = self.getRelativePath(
                        os.path.join(self.pdata["TRANSLATIONSBINPATH"],
                                     os.path.basename(qmFile)))
                fn = os.path.join(self.ppath, qmFile)
                if os.path.exists(fn):
                    s2t(fn)
            except OSError as err:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Delete translation"),
                    self.tr(
                        "<p>The selected translation file <b>{0}</b> could"
                        " not be deleted.</p><p>Reason: {1}</p>").format(
                        qmFile, str(err)))
                return
        
    def appendFile(self, fn, isSourceFile=False, updateModel=True):
        """
        Public method to append a file to the project.
        
        @param fn filename to be added to the project (string)
        @param isSourceFile flag indicating that this is a source file
            even if it doesn't have the source extension (boolean)
        @param updateModel flag indicating an update of the model is
            requested (boolean)
        """
        dirty = False
        
        if os.path.isabs(fn):
            # make it relative to the project root, if it starts with that path
            newfn = self.getRelativePath(fn)
        else:
            # assume relative paths are relative to the project root
            newfn = fn
        newdir = os.path.dirname(newfn)
        
        if isSourceFile:
            filetype = "SOURCES"
        else:
            filetype = "OTHERS"
            bfn = os.path.basename(newfn)
            if fnmatch.fnmatch(bfn, '*.ts') or fnmatch.fnmatch(bfn, '*.qm'):
                filetype = "TRANSLATIONS"
            else:
                for pattern in reversed(
                        sorted(self.pdata["FILETYPES"].keys())):
                    if fnmatch.fnmatch(bfn, pattern):
                        filetype = self.pdata["FILETYPES"][pattern]
                        break
        
        if filetype == "__IGNORE__":
            return
        
        if filetype in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS",
                        "RESOURCES"]:
            if filetype == "SOURCES":
                if newfn not in self.pdata["SOURCES"]:
                    self.pdata["SOURCES"].append(newfn)
                    self.projectSourceAdded.emit(newfn)
                    updateModel and self.__model.addNewItem("SOURCES", newfn)
                    dirty = True
                else:
                    updateModel and self.repopulateItem(newfn)
            elif filetype == "FORMS":
                if newfn not in self.pdata["FORMS"]:
                    self.pdata["FORMS"].append(newfn)
                    self.projectFormAdded.emit(newfn)
                    updateModel and self.__model.addNewItem("FORMS", newfn)
                    dirty = True
                else:
                    updateModel and self.repopulateItem(newfn)
            elif filetype == "INTERFACES":
                if newfn not in self.pdata["INTERFACES"]:
                    self.pdata["INTERFACES"].append(newfn)
                    self.projectInterfaceAdded.emit(newfn)
                    (updateModel and
                     self.__model.addNewItem("INTERFACES", newfn))
                    dirty = True
                else:
                    updateModel and self.repopulateItem(newfn)
            elif filetype == "PROTOCOLS":
                if newfn not in self.pdata["PROTOCOLS"]:
                    self.pdata["PROTOCOLS"].append(newfn)
                    self.projectProtocolAdded.emit(newfn)
                    (updateModel and
                     self.__model.addNewItem("PROTOCOLS", newfn))
                    dirty = True
                else:
                    updateModel and self.repopulateItem(newfn)
            elif filetype == "RESOURCES":
                if newfn not in self.pdata["RESOURCES"]:
                    self.pdata["RESOURCES"].append(newfn)
                    self.projectResourceAdded.emit(newfn)
                    updateModel and self.__model.addNewItem("RESOURCES", newfn)
                    dirty = True
                else:
                    updateModel and self.repopulateItem(newfn)
            if newdir not in self.subdirs:
                self.subdirs.append(newdir)
        elif filetype == "TRANSLATIONS":
            if newfn not in self.pdata["TRANSLATIONS"]:
                self.pdata["TRANSLATIONS"].append(newfn)
                updateModel and self.__model.addNewItem("TRANSLATIONS", newfn)
                self.projectLanguageAdded.emit(newfn)
                dirty = True
            else:
                updateModel and self.repopulateItem(newfn)
        else:   # filetype == "OTHERS"
            if newfn not in self.pdata["OTHERS"]:
                self.pdata['OTHERS'].append(newfn)
                self.othersAdded(newfn, updateModel)
                dirty = True
            else:
                updateModel and self.repopulateItem(newfn)
            if newdir not in self.otherssubdirs:
                self.otherssubdirs.append(newdir)
        
        if dirty:
            self.setDirty(True)
        
    @pyqtSlot()
    def addFiles(self, fileTypeFilter=None, startdir=None):
        """
        Public slot used to add files to the project.
        
        @param fileTypeFilter filter to be used by the add file dialog
        @type str out of source, form, resource, interface, protocol, others
        @param startdir start directory for the selection dialog
        @type str
        """
        if startdir is None:
            startdir = self.ppath
        from .AddFileDialog import AddFileDialog
        dlg = AddFileDialog(self, self.parent(), fileTypeFilter,
                            startdir=startdir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            fnames, target, isSource = dlg.getData()
            if target != '':
                for fn in fnames:
                    targetfile = os.path.join(target, os.path.basename(fn))
                    if not Utilities.samepath(os.path.dirname(fn), target):
                        try:
                            if not os.path.isdir(target):
                                os.makedirs(target)
                                
                            if os.path.exists(targetfile):
                                res = E5MessageBox.yesNo(
                                    self.ui,
                                    self.tr("Add file"),
                                    self.tr(
                                        "<p>The file <b>{0}</b> already"
                                        " exists.</p><p>Overwrite it?</p>")
                                    .format(targetfile),
                                    icon=E5MessageBox.Warning)
                                if not res:
                                    return  # don't overwrite
                                    
                            shutil.copy(fn, target)
                        except OSError as why:
                            E5MessageBox.critical(
                                self.ui,
                                self.tr("Add file"),
                                self.tr(
                                    "<p>The selected file <b>{0}</b> could"
                                    " not be added to <b>{1}</b>.</p>"
                                    "<p>Reason: {2}</p>")
                                .format(fn, target, str(why)))
                            continue
                    
                    self.appendFile(targetfile,
                                    isSource or fileTypeFilter == 'source')
            else:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Add file"),
                    self.tr("The target directory must not be empty."))
        
    def __addSingleDirectory(self, filetype, source, target, quiet=False):
        """
        Private method used to add all files of a single directory to the
        project.
        
        @param filetype type of files to add (string)
        @param source source directory (string)
        @param target target directory (string)
        @param quiet flag indicating quiet operations (boolean)
        """
        # get all relevant filename patterns
        patterns = []
        ignorePatterns = []
        for pattern, patterntype in list(self.pdata["FILETYPES"].items()):
            if patterntype == filetype:
                patterns.append(pattern)
            elif patterntype == "__IGNORE__":
                ignorePatterns.append(pattern)
        
        files = []
        for pattern in patterns:
            sstring = "{0}{1}{2}".format(source, os.sep, pattern)
            files.extend(glob.glob(sstring))
        
        if len(files) == 0:
            if not quiet:
                E5MessageBox.information(
                    self.ui,
                    self.tr("Add directory"),
                    self.tr(
                        "<p>The source directory doesn't contain"
                        " any files belonging to the selected category.</p>"))
            return
        
        if (
            not Utilities.samepath(target, source) and
            not os.path.isdir(target)
        ):
            try:
                os.makedirs(target)
            except OSError as why:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Add directory"),
                    self.tr(
                        "<p>The target directory <b>{0}</b> could not be"
                        " created.</p><p>Reason: {1}</p>")
                    .format(target, str(why)))
                return
        
        for file in files:
            for pattern in ignorePatterns:
                if fnmatch.fnmatch(file, pattern):
                    continue
            
            targetfile = os.path.join(target, os.path.basename(file))
            if not Utilities.samepath(target, source):
                try:
                    if os.path.exists(targetfile):
                        res = E5MessageBox.yesNo(
                            self.ui,
                            self.tr("Add directory"),
                            self.tr(
                                "<p>The file <b>{0}</b> already exists.</p>"
                                "<p>Overwrite it?</p>")
                            .format(targetfile),
                            icon=E5MessageBox.Warning)
                        if not res:
                            continue
                            # don't overwrite, carry on with next file
                            
                    shutil.copy(file, target)
                except OSError:
                    continue
            self.appendFile(targetfile)
        
    def __addRecursiveDirectory(self, filetype, source, target):
        """
        Private method used to add all files of a directory tree.
        
        The tree is rooted at source to another one rooted at target. This
        method decents down to the lowest subdirectory.
        
        @param filetype type of files to add (string)
        @param source source directory (string)
        @param target target directory (string)
        """
        # first perform the addition of source
        self.__addSingleDirectory(filetype, source, target, True)
        
        ignore_patterns = [pattern for pattern, filetype in
                           self.pdata["FILETYPES"].items()
                           if filetype == '__IGNORE__']
        
        # now recurse into subdirectories
        for name in os.listdir(source):
            ns = os.path.join(source, name)
            if os.path.isdir(ns):
                skip = False
                for ignore_pattern in ignore_patterns:
                    if fnmatch.fnmatch(name, ignore_pattern):
                        skip = True
                        break
                if skip:
                    continue
                
                nt = os.path.join(target, name)
                self.__addRecursiveDirectory(filetype, ns, nt)
        
    @pyqtSlot()
    def addDirectory(self, fileTypeFilter=None, startdir=None):
        """
        Public method used to add all files of a directory to the project.
        
        @param fileTypeFilter filter to be used by the add directory dialog
        @type str out of source, form, resource, interface, protocol, others
        @param startdir start directory for the selection dialog
        @type str
        """
        if startdir is None:
            startdir = self.ppath
        from .AddDirectoryDialog import AddDirectoryDialog
        dlg = AddDirectoryDialog(
            self, fileTypeFilter, self.parent(), startdir=startdir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            filetype, source, target, recursive = dlg.getData()
            if target == '':
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Add directory"),
                    self.tr("The target directory must not be empty."))
                return
            
            if filetype == 'OTHERS':
                self.addToOthers(source)
                return
            
            if source == '':
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Add directory"),
                    self.tr("The source directory must not be empty."))
                return
            
            if recursive:
                self.__addRecursiveDirectory(filetype, source, target)
            else:
                self.__addSingleDirectory(filetype, source, target)
        
    def addToOthers(self, fn):
        """
        Public method to add a file/directory to the OTHERS project data.
        
        @param fn file name or directory name to add (string)
        """
        if fn:
            # if it is below the project directory, make it relative to that
            fn = self.getRelativePath(fn)
            
            # if it ends with the directory separator character, remove it
            if fn.endswith(os.sep):
                fn = fn[:-1]
            
            if fn not in self.pdata["OTHERS"]:
                self.pdata['OTHERS'].append(fn)
                self.othersAdded(fn)
                self.setDirty(True)
            
            if os.path.isdir(fn) and fn not in self.otherssubdirs:
                self.otherssubdirs.append(fn)
        
    def addSourceFiles(self):
        """
        Public slot to add source files to the current project.
        """
        self.addFiles('source')
        
    def addUiFiles(self):
        """
        Public slot to add forms to the current project.
        """
        self.addFiles('form')
        
    def addIdlFiles(self):
        """
        Public slot to add IDL interfaces to the current project.
        """
        self.addFiles('interface')
        
    def addProtoFiles(self):
        """
        Public slot to add protocol files to the current project.
        """
        self.addFiles('protocol')
        
    def addResourceFiles(self):
        """
        Public slot to add Qt resources to the current project.
        """
        self.addFiles('resource')
        
    def addOthersFiles(self):
        """
        Public slot to add files to the OTHERS project data.
        """
        self.addFiles('others')
        
    def addSourceDir(self):
        """
        Public slot to add all source files of a directory to the current
        project.
        """
        self.addDirectory('source')
        
    def addUiDir(self):
        """
        Public slot to add all forms of a directory to the current project.
        """
        self.addDirectory('form')
        
    def addIdlDir(self):
        """
        Public slot to add all IDL interfaces of a directory to the current
        project.
        """
        self.addDirectory('interface')
        
    def addProtoDir(self):
        """
        Public slot to add all protocol files of a directory to the current
        project.
        """
        self.addDirectory('protocol')
        
    def addResourceDir(self):
        """
        Public slot to add all Qt resource files of a directory to the current
        project.
        """
        self.addDirectory('resource')
        
    def addOthersDir(self):
        """
        Public slot to add a directory to the OTHERS project data.
        """
        self.addDirectory('others')
        
    def renameMainScript(self, oldfn, newfn):
        """
        Public method to rename the main script.
        
        @param oldfn old filename (string)
        @param newfn new filename of the main script (string)
        """
        if self.pdata["MAINSCRIPT"]:
            ofn = self.getRelativePath(oldfn)
            if ofn != self.pdata["MAINSCRIPT"]:
                return
            
            fn = self.getRelativePath(newfn)
            self.pdata["MAINSCRIPT"] = fn
            self.setDirty(True)
        
    def renameFile(self, oldfn, newfn=None):
        """
        Public slot to rename a file of the project.
        
        @param oldfn old filename of the file (string)
        @param newfn new filename of the file (string)
        @return flag indicating success
        """
        fn = self.getRelativePath(oldfn)
        isSourceFile = fn in self.pdata["SOURCES"]
        
        if newfn is None:
            newfn = E5FileDialog.getSaveFileName(
                None,
                self.tr("Rename file"),
                oldfn,
                "",
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
            if not newfn:
                return False
            newfn = Utilities.toNativeSeparators(newfn)
        
        if os.path.exists(newfn):
            res = E5MessageBox.yesNo(
                self.ui,
                self.tr("Rename File"),
                self.tr("""<p>The file <b>{0}</b> already exists."""
                        """ Overwrite it?</p>""")
                    .format(newfn),
                icon=E5MessageBox.Warning)
            if not res:
                return False
        
        try:
            os.rename(oldfn, newfn)
        except OSError as msg:
            E5MessageBox.critical(
                self.ui,
                self.tr("Rename File"),
                self.tr(
                    """<p>The file <b>{0}</b> could not be renamed.<br />"""
                    """Reason: {1}</p>""").format(oldfn, str(msg)))
            return False

        if (
            fn in self.pdata["SOURCES"] or
            fn in self.pdata["FORMS"] or
            fn in self.pdata["TRANSLATIONS"] or
            fn in self.pdata["INTERFACES"] or
            fn in self.pdata["PROTOCOLS"] or
            fn in self.pdata["RESOURCES"] or
            fn in self.pdata["OTHERS"]
        ):
            self.renameFileInPdata(oldfn, newfn, isSourceFile)
        
        return True
        
    def renameFileInPdata(self, oldname, newname, isSourceFile=False):
        """
        Public method to rename a file in the pdata structure.
        
        @param oldname old filename (string)
        @param newname new filename (string)
        @param isSourceFile flag indicating that this is a source file
                even if it doesn't have the source extension (boolean)
        """
        fn = self.getRelativePath(oldname)
        if os.path.dirname(oldname) == os.path.dirname(newname):
            if self.__isInPdata(oldname):
                self.removeFile(oldname, False)
                self.appendFile(newname, isSourceFile, False)
            self.__model.renameItem(fn, newname)
        else:
            self.removeFile(oldname)
            self.appendFile(newname, isSourceFile)
        self.projectFileRenamed.emit(oldname, newname)
        
        self.renameMainScript(fn, newname)
        
    def getFiles(self, start):
        """
        Public method to get all files starting with a common prefix.
        
        @param start prefix (string)
        @return list of files starting with a common prefix (list of strings)
        """
        filelist = []
        start = self.getRelativePath(start)
        for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS", "RESOURCES",
                    "OTHERS"]:
            for entry in self.pdata[key][:]:
                if entry.startswith(start):
                    filelist.append(os.path.join(self.ppath, entry))
        return filelist
        
    def __reorganizeFiles(self):
        """
        Private method to reorganize files stored in the project.
        """
        reorganized = False
        
        # init data store for the reorganization
        newPdata = {}
        for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS", "RESOURCES",
                    "OTHERS", "TRANSLATIONS"]:
            newPdata[key] = []
        
        # iterate over all files checking for a reassignment
        for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS", "RESOURCES",
                    "OTHERS", "TRANSLATIONS"]:
            for fn in self.pdata[key][:]:
                filetype = key
                bfn = os.path.basename(fn)
                for pattern in reversed(
                        sorted(self.pdata["FILETYPES"].keys())):
                    if fnmatch.fnmatch(bfn, pattern):
                        filetype = self.pdata["FILETYPES"][pattern]
                        break
        
                if filetype != "__IGNORE__":
                    newPdata[filetype].append(fn)
                    if filetype != key:
                        reorganized = True
        
        if reorganized:
            # copy the reorganized files back to the project
            for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS",
                        "RESOURCES", "OTHERS", "TRANSLATIONS"]:
                self.pdata[key] = newPdata[key][:]
            
            # repopulate the model
            self.__model.projectClosed()
            self.__model.projectOpened()
        
    def copyDirectory(self, olddn, newdn):
        """
        Public slot to copy a directory.
        
        @param olddn original directory name (string)
        @param newdn new directory name (string)
        """
        olddn = self.getRelativePath(olddn)
        newdn = self.getRelativePath(newdn)
        for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS", "RESOURCES",
                    "OTHERS"]:
            for entry in self.pdata[key][:]:
                if entry.startswith(olddn):
                    entry = entry.replace(olddn, newdn)
                    self.appendFile(os.path.join(self.ppath, entry),
                                    key == "SOURCES")
        self.setDirty(True)
        
    def moveDirectory(self, olddn, newdn):
        """
        Public slot to move a directory.
        
        @param olddn old directory name (string)
        @param newdn new directory name (string)
        """
        olddn = self.getRelativePath(olddn)
        newdn = self.getRelativePath(newdn)
        typeStrings = []
        for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS", "RESOURCES",
                    "OTHERS"]:
            for entry in self.pdata[key][:]:
                if entry.startswith(olddn):
                    if key not in typeStrings:
                        typeStrings.append(key)
                    self.pdata[key].remove(entry)
                    entry = entry.replace(olddn, newdn)
                    self.pdata[key].append(entry)
            if key == "OTHERS":
                if newdn not in self.otherssubdirs:
                    self.otherssubdirs.append(newdn)
            else:
                if newdn not in self.subdirs:
                    self.subdirs.append(newdn)
        if typeStrings:
            # the directory is controlled by the project
            self.setDirty(True)
            self.__model.removeItem(olddn)
            typeString = typeStrings[0]
            del typeStrings[0]
            self.__model.addNewItem(typeString, newdn, typeStrings)
        else:
            self.__model.renameItem(olddn, self.getAbsolutePath(newdn))
        self.directoryRemoved.emit(olddn)
        
    def removeFile(self, fn, updateModel=True):
        """
        Public slot to remove a file from the project.
        
        The file is not deleted from the project directory.
        
        @param fn filename to be removed from the project
        @param updateModel flag indicating an update of the model is
            requested (boolean)
        """
        fn = self.getRelativePath(fn)
        dirty = True
        if fn in self.pdata["SOURCES"]:
            self.pdata["SOURCES"].remove(fn)
            self.projectSourceRemoved.emit(fn)
        elif fn in self.pdata["FORMS"]:
            self.pdata["FORMS"].remove(fn)
            self.projectFormRemoved.emit(fn)
        elif fn in self.pdata["INTERFACES"]:
            self.pdata["INTERFACES"].remove(fn)
            self.projectInterfaceRemoved.emit(fn)
        elif fn in self.pdata["PROTOCOLS"]:
            self.pdata["PROTOCOLS"].remove(fn)
            self.projectProtocolRemoved.emit(fn)
        elif fn in self.pdata["RESOURCES"]:
            self.pdata["RESOURCES"].remove(fn)
            self.projectResourceRemoved.emit(fn)
        elif fn in self.pdata["OTHERS"]:
            self.pdata["OTHERS"].remove(fn)
            self.projectOthersRemoved.emit(fn)
        elif fn in self.pdata["TRANSLATIONS"]:
            self.pdata["TRANSLATIONS"].remove(fn)
            self.projectLanguageRemoved.emit(fn)
        else:
            dirty = False
        updateModel and self.__model.removeItem(fn)
        if dirty:
            self.setDirty(True)
        
    def removeDirectory(self, dn):
        """
        Public method to remove a directory from the project.
        
        The directory is not deleted from the project directory.
        
        @param dn directory name to be removed from the project
        """
        dirty = False
        dn = self.getRelativePath(dn)
        for entry in self.pdata["OTHERS"][:]:
            if entry.startswith(dn):
                self.pdata["OTHERS"].remove(entry)
                dirty = True
        if not dn.endswith(os.sep):
            dn2 = dn + os.sep
        else:
            dn2 = dn
        for key in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS", "RESOURCES",
                    "TRANSLATIONS", ]:
            for entry in self.pdata[key][:]:
                if entry.startswith(dn2):
                    self.pdata[key].remove(entry)
                    dirty = True
        self.__model.removeItem(dn)
        if dirty:
            self.setDirty(True)
        self.directoryRemoved.emit(dn)
        
    def deleteFile(self, fn):
        """
        Public method to delete a file from the project directory.
        
        @param fn filename to be deleted from the project
        @return flag indicating success (boolean)
        """
        try:
            from ThirdParty.Send2Trash.send2trash import send2trash as s2t
        except ImportError:
            s2t = os.remove
        
        try:
            s2t(os.path.join(self.ppath, fn))
            path, ext = os.path.splitext(fn)
            if ext == '.ui':
                fn2 = os.path.join(self.ppath, '{0}.h'.format(fn))
                if os.path.isfile(fn2):
                    s2t(fn2)
            head, tail = os.path.split(path)
            for ext in ['.pyc', '.pyo']:
                fn2 = os.path.join(self.ppath, path + ext)
                if os.path.isfile(fn2):
                    s2t(fn2)
                pat = os.path.join(
                    self.ppath, head,
                    "__pycache__", "{0}.*{1}".format(tail, ext))
                for f in glob.glob(pat):
                    s2t(f)
        except OSError as err:
            E5MessageBox.critical(
                self.ui,
                self.tr("Delete file"),
                self.tr(
                    "<p>The selected file <b>{0}</b> could not be"
                    " deleted.</p><p>Reason: {1}</p>").format(
                    fn, str(err)))
            return False
        
        self.removeFile(fn)
        if ext == '.ui':
            self.removeFile(fn + '.h')
        return True
        
    def deleteDirectory(self, dn):
        """
        Public method to delete a directory from the project directory.
        
        @param dn directory name to be removed from the project
        @return flag indicating success (boolean)
        """
        if not os.path.isabs(dn):
            dn = os.path.join(self.ppath, dn)
        try:
            try:
                from ThirdParty.Send2Trash.send2trash import send2trash
                send2trash(dn)
            except ImportError:
                shutil.rmtree(dn, True)
        except OSError as err:
            E5MessageBox.critical(
                self.ui,
                self.tr("Delete directory"),
                self.tr(
                    "<p>The selected directory <b>{0}</b> could not be"
                    " deleted.</p><p>Reason: {1}</p>").format(dn, str(err)))
            return False
        
        self.removeDirectory(dn)
        return True
    
    def hasEntry(self, fn):
        """
        Public method to check the project for a file.
        
        @param fn filename to be checked (string)
        @return flag indicating, if the project contains the file (boolean)
        """
        fn = self.getRelativePath(fn)
        if (
            fn in self.pdata["SOURCES"] or
            fn in self.pdata["FORMS"] or
            fn in self.pdata["INTERFACES"] or
            fn in self.pdata["PROTOCOLS"] or
            fn in self.pdata["RESOURCES"] or
            fn in self.pdata["OTHERS"]
        ):
            return True
        else:
            return False
        
    def createNewProject(self):
        """
        Public slot to built a new project.
        
        This method displays the new project dialog and initializes
        the project object with the data entered.
        """
        if not self.checkDirty():
            return
            
        from .PropertiesDialog import PropertiesDialog
        dlg = PropertiesDialog(self, True)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.closeProject()
            dlg.storeData()
            self.pdata["VCS"] = 'None'
            self.opened = True
            if not self.pdata["FILETYPES"]:
                self.initFileTypes()
            self.setDirty(True)
            self.closeAct.setEnabled(True)
            self.saveasAct.setEnabled(True)
            self.actGrp2.setEnabled(True)
            self.propsAct.setEnabled(True)
            self.userPropsAct.setEnabled(True)
            self.filetypesAct.setEnabled(True)
            self.lexersAct.setEnabled(True)
            self.sessActGrp.setEnabled(False)
            self.dbgActGrp.setEnabled(True)
            self.menuDebuggerAct.setEnabled(True)
            self.menuSessionAct.setEnabled(False)
            self.menuCheckAct.setEnabled(True)
            self.menuShowAct.setEnabled(True)
            self.menuDiagramAct.setEnabled(True)
            self.menuApidocAct.setEnabled(True)
            self.menuPackagersAct.setEnabled(True)
            self.pluginGrp.setEnabled(
                self.pdata["PROJECTTYPE"] in ["E6Plugin"])
            self.addLanguageAct.setEnabled(
                bool(self.pdata["TRANSLATIONPATTERN"]))
            self.makeGrp.setEnabled(
                self.pdata["MAKEPARAMS"]["MakeEnabled"])
            self.menuMakeAct.setEnabled(
                self.pdata["MAKEPARAMS"]["MakeEnabled"])
            
            self.projectAboutToBeCreated.emit()
            
            hashStr = str(QCryptographicHash.hash(
                QByteArray(self.ppath.encode("utf-8")),
                QCryptographicHash.Algorithm.Sha1).toHex(),
                encoding="utf-8")
            self.pdata["HASH"] = hashStr
            
            if self.pdata["PROGLANGUAGE"] == "MicroPython":
                # change the lexer association for *.py files
                self.pdata["LEXERASSOCS"] = {
                    "*.py": "MicroPython",
                }
            
            # create the project directory if it doesn't exist already
            if not os.path.isdir(self.ppath):
                try:
                    os.makedirs(self.ppath)
                except OSError:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Create project directory"),
                        self.tr(
                            "<p>The project directory <b>{0}</b> could not"
                            " be created.</p>")
                        .format(self.ppath))
                    self.vcs = self.initVCS()
                    return
                
                # create an empty __init__.py file to make it a Python package
                # (only for Python and Python3)
                if self.pdata["PROGLANGUAGE"] in [
                    "Python3", "MicroPython"
                ]:
                    fn = os.path.join(self.ppath, "__init__.py")
                    with open(fn, "w", encoding="utf-8"):
                        pass
                    self.appendFile(fn, True)
                
                # create an empty main script file, if a name was given
                if self.pdata["MAINSCRIPT"]:
                    if not os.path.isabs(self.pdata["MAINSCRIPT"]):
                        ms = os.path.join(
                            self.ppath, self.pdata["MAINSCRIPT"])
                    else:
                        ms = self.pdata["MAINSCRIPT"]
                    os.makedirs(os.path.dirname(ms), exist_ok=True)
                    with open(ms, "w"):
                        pass
                    self.appendFile(ms, True)
                
                if self.pdata["MAKEPARAMS"]["MakeEnabled"]:
                    mf = self.pdata["MAKEPARAMS"]["MakeFile"]
                    if mf:
                        if not os.path.isabs(mf):
                            mf = os.path.join(self.ppath, mf)
                    else:
                        mf = os.path.join(self.ppath, Project.DefaultMakefile)
                    os.makedirs(os.path.dirname(mf), exist_ok=True)
                    with open(mf, "w"):
                        pass
                    self.appendFile(mf)
                
                tpd = os.path.join(self.ppath, self.translationsRoot)
                if not self.translationsRoot.endswith(os.sep):
                    tpd = os.path.dirname(tpd)
                if not os.path.isdir(tpd):
                    os.makedirs(tpd, exist_ok=True)
                if self.pdata["TRANSLATIONSBINPATH"]:
                    tpd = os.path.join(
                        self.ppath, self.pdata["TRANSLATIONSBINPATH"])
                    if not os.path.isdir(tpd):
                        os.makedirs(tpd, exist_ok=True)
                
                # create management directory if not present
                self.createProjectManagementDir()
                
                self.saveProject()
                addAllToVcs = True
            else:
                try:
                    # create management directory if not present
                    self.createProjectManagementDir()
                except OSError:
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Create project management directory"),
                        self.tr(
                            "<p>The project directory <b>{0}</b> is not"
                            " writable.</p>")
                        .format(self.ppath))
                    return
                
                if self.pdata["MAINSCRIPT"]:
                    if not os.path.isabs(self.pdata["MAINSCRIPT"]):
                        ms = os.path.join(
                            self.ppath, self.pdata["MAINSCRIPT"])
                    else:
                        ms = self.pdata["MAINSCRIPT"]
                    if not os.path.exists(ms):
                        try:
                            os.makedirs(os.path.dirname(ms))
                            with open(ms, "w"):
                                pass
                        except OSError as err:
                            E5MessageBox.critical(
                                self.ui,
                                self.tr("Create main script"),
                                self.tr(
                                    "<p>The mainscript <b>{0}</b> could not"
                                    " be created.<br/>Reason: {1}</p>")
                                .format(ms, str(err)))
                    self.appendFile(ms, True)
                else:
                    ms = ""
                
                if self.pdata["MAKEPARAMS"]["MakeEnabled"]:
                    mf = self.pdata["MAKEPARAMS"]["MakeFile"]
                    if mf:
                        if not os.path.isabs(mf):
                            mf = os.path.join(self.ppath, mf)
                    else:
                        mf = os.path.join(self.ppath, Project.DefaultMakefile)
                    if not os.path.exists(mf):
                        try:
                            os.makedirs(os.path.dirname(mf))
                            with open(mf, "w"):
                                pass
                        except OSError as err:
                            E5MessageBox.critical(
                                self.ui,
                                self.tr("Create Makefile"),
                                self.tr(
                                    "<p>The makefile <b>{0}</b> could not"
                                    " be created.<br/>Reason: {1}</p>")
                                .format(mf, str(err)))
                    self.appendFile(mf)
                
                # add existing files to the project
                res = E5MessageBox.yesNo(
                    self.ui,
                    self.tr("New Project"),
                    self.tr("""Add existing files to the project?"""),
                    yesDefault=True)
                if res:
                    self.newProjectAddFiles(ms)
                addAllToVcs = res
                # create an empty __init__.py file to make it a Python package
                # if none exists (only for Python and Python3)
                if self.pdata["PROGLANGUAGE"] in [
                    "Python3", "MicroPython"
                ]:
                    fn = os.path.join(self.ppath, "__init__.py")
                    if not os.path.exists(fn):
                        with open(fn, "w", encoding="utf-8"):
                            pass
                        self.appendFile(fn, True)
                self.saveProject()
                
                # check, if the existing project directory is already under
                # VCS control
                pluginManager = e5App().getObject("PluginManager")
                for indicator, vcsData in list(
                        pluginManager.getVcsSystemIndicators().items()):
                    if os.path.exists(os.path.join(self.ppath, indicator)):
                        if len(vcsData) > 1:
                            vcsList = []
                            for _vcsSystemStr, vcsSystemDisplay in vcsData:
                                vcsList.append(vcsSystemDisplay)
                            res, vcs_ok = QInputDialog.getItem(
                                None,
                                self.tr("New Project"),
                                self.tr("Select Version Control System"),
                                vcsList,
                                0, False)
                            if vcs_ok:
                                for vcsSystemStr, vcsSystemDisplay in vcsData:
                                    if res == vcsSystemDisplay:
                                        vcsSystem = vcsSystemStr
                                        break
                                else:
                                    vcsSystem = "None"
                            else:
                                vcsSystem = "None"
                        else:
                            vcsSystem = vcsData[0][1]
                        self.pdata["VCS"] = vcsSystem
                        self.vcs = self.initVCS()
                        self.setDirty(True)
                        if self.vcs is not None:
                            # edit VCS command options
                            if self.vcs.vcsSupportCommandOptions():
                                vcores = E5MessageBox.yesNo(
                                    self.ui,
                                    self.tr("New Project"),
                                    self.tr(
                                        """Would you like to edit the VCS"""
                                        """ command options?"""))
                            else:
                                vcores = False
                            if vcores:
                                from VCS.CommandOptionsDialog import (
                                    VcsCommandOptionsDialog
                                )
                                codlg = VcsCommandOptionsDialog(self.vcs)
                                if codlg.exec() == QDialog.DialogCode.Accepted:
                                    self.vcs.vcsSetOptions(codlg.getOptions())
                            # add project file to repository
                            if res == 0:
                                apres = E5MessageBox.yesNo(
                                    self.ui,
                                    self.tr("New project"),
                                    self.tr(
                                        "Shall the project file be added"
                                        " to the repository?"),
                                    yesDefault=True)
                                if apres:
                                    self.saveProject()
                                    self.vcs.vcsAdd(self.pfile)
                        else:
                            self.pdata["VCS"] = 'None'
                        self.saveProject()
                        break
            
            # put the project under VCS control
            if (
                self.vcs is None and
                self.vcsSoftwareAvailable() and
                self.vcsRequested
            ):
                vcsSystemsDict = (
                    e5App().getObject("PluginManager")
                    .getPluginDisplayStrings("version_control")
                )
                vcsSystemsDisplay = [self.tr("None")]
                keys = sorted(vcsSystemsDict.keys())
                for key in keys:
                    vcsSystemsDisplay.append(vcsSystemsDict[key])
                vcsSelected, ok = QInputDialog.getItem(
                    None,
                    self.tr("New Project"),
                    self.tr(
                        "Select version control system for the project"),
                    vcsSystemsDisplay,
                    0, False)
                if ok and vcsSelected != self.tr("None"):
                    for vcsSystem, vcsSystemDisplay in vcsSystemsDict.items():
                        if vcsSystemDisplay == vcsSelected:
                            self.pdata["VCS"] = vcsSystem
                            break
                    else:
                        self.pdata["VCS"] = 'None'
                else:
                    self.pdata["VCS"] = 'None'
                self.vcs = self.initVCS()
                if self.vcs is not None:
                    vcsdlg = self.vcs.vcsOptionsDialog(self, self.name)
                    if vcsdlg.exec() == QDialog.DialogCode.Accepted:
                        vcsDataDict = vcsdlg.getData()
                    else:
                        self.pdata["VCS"] = 'None'
                        self.vcs = self.initVCS()
                self.setDirty(True)
                if self.vcs is not None:
                    # edit VCS command options
                    if self.vcs.vcsSupportCommandOptions():
                        vcores = E5MessageBox.yesNo(
                            self.ui,
                            self.tr("New Project"),
                            self.tr(
                                """Would you like to edit the VCS command"""
                                """ options?"""))
                    else:
                        vcores = False
                    if vcores:
                        from VCS.CommandOptionsDialog import (
                            VcsCommandOptionsDialog
                        )
                        codlg = VcsCommandOptionsDialog(self.vcs)
                        if codlg.exec() == QDialog.DialogCode.Accepted:
                            self.vcs.vcsSetOptions(codlg.getOptions())
                    
                    # create the project in the VCS
                    self.vcs.vcsSetDataFromDict(vcsDataDict)
                    self.saveProject()
                    self.vcs.vcsConvertProject(vcsDataDict, self,
                                               addAll=addAllToVcs)
                else:
                    self.newProjectHooks.emit()
                    self.newProject.emit()
            
            else:
                self.newProjectHooks.emit()
                self.newProject.emit()

    def newProjectAddFiles(self, mainscript):
        """
        Public method to add files to a new project.
        
        @param mainscript name of the mainscript (string)
        """
        # Show the file type associations for the user to change
        self.__showFiletypeAssociations()
        
        with E5OverrideCursor():
            # search the project directory for files with known extensions
            filespecs = list(self.pdata["FILETYPES"].keys())
            for filespec in filespecs:
                files = Utilities.direntries(self.ppath, True, filespec)
                for file in files:
                    self.appendFile(file)
            
            # special handling for translation files
            if self.translationsRoot:
                tpd = os.path.join(self.ppath, self.translationsRoot)
                if not self.translationsRoot.endswith(os.sep):
                    tpd = os.path.dirname(tpd)
            else:
                tpd = self.ppath
            tslist = []
            if self.pdata["TRANSLATIONPATTERN"]:
                pattern = os.path.basename(self.pdata["TRANSLATIONPATTERN"])
                if "%language%" in pattern:
                    pattern = pattern.replace("%language%", "*")
                else:
                    tpd = self.pdata["TRANSLATIONPATTERN"].split(
                        "%language%")[0]
            else:
                pattern = "*.ts"
            tslist.extend(Utilities.direntries(tpd, True, pattern))
            pattern = self.__binaryTranslationFile(pattern)
            if pattern:
                tslist.extend(Utilities.direntries(tpd, True, pattern))
            if tslist:
                if '_' in os.path.basename(tslist[0]):
                    # the first entry determines the mainscript name
                    mainscriptname = (
                        os.path.splitext(mainscript)[0] or
                        os.path.basename(tslist[0]).split('_')[0]
                    )
                    self.pdata["TRANSLATIONPATTERN"] = os.path.join(
                        os.path.dirname(tslist[0]),
                        "{0}_%language%{1}".format(
                            os.path.basename(tslist[0]).split('_')[0],
                            os.path.splitext(tslist[0])[1]))
                else:
                    mainscriptname = ""
                    pattern, ok = QInputDialog.getText(
                        None,
                        self.tr("Translation Pattern"),
                        self.tr(
                            "Enter the path pattern for translation files "
                            "(use '%language%' in place of the language"
                            " code):"),
                        QLineEdit.EchoMode.Normal,
                        tslist[0])
                    if pattern:
                        self.pdata["TRANSLATIONPATTERN"] = pattern
                if self.pdata["TRANSLATIONPATTERN"]:
                    self.pdata["TRANSLATIONPATTERN"] = self.getRelativePath(
                        self.pdata["TRANSLATIONPATTERN"])
                    pattern = self.pdata["TRANSLATIONPATTERN"].replace(
                        "%language%", "*")
                    for ts in tslist:
                        if fnmatch.fnmatch(ts, pattern):
                            self.pdata["TRANSLATIONS"].append(ts)
                            self.projectLanguageAdded.emit(ts)
                    if self.pdata["TRANSLATIONSBINPATH"]:
                        tpd = os.path.join(self.ppath,
                                           self.pdata["TRANSLATIONSBINPATH"])
                        pattern = os.path.basename(
                            self.pdata["TRANSLATIONPATTERN"]).replace(
                            "%language%", "*")
                        pattern = self.__binaryTranslationFile(pattern)
                        qmlist = Utilities.direntries(tpd, True, pattern)
                        for qm in qmlist:
                            self.pdata["TRANSLATIONS"].append(qm)
                            self.projectLanguageAdded.emit(qm)
                if not self.pdata["MAINSCRIPT"] and bool(mainscriptname):
                    if self.pdata["PROGLANGUAGE"] in [
                        "Python3", "MicroPython"
                    ]:
                        self.pdata["MAINSCRIPT"] = '{0}.py'.format(
                            mainscriptname)
                    elif self.pdata["PROGLANGUAGE"] == "Ruby":
                        self.pdata["MAINSCRIPT"] = '{0}.rb'.format(
                            mainscriptname)
            self.setDirty(True)
    
    def __showProperties(self):
        """
        Private slot to display the properties dialog.
        """
        from .PropertiesDialog import PropertiesDialog
        dlg = PropertiesDialog(self, False)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            projectType = self.pdata["PROJECTTYPE"]
            dlg.storeData()
            self.setDirty(True)
            if self.pdata["MAINSCRIPT"]:
                if not os.path.isabs(self.pdata["MAINSCRIPT"]):
                    ms = os.path.join(
                        self.ppath, self.pdata["MAINSCRIPT"])
                else:
                    ms = self.pdata["MAINSCRIPT"]
                if os.path.exists(ms):
                    self.appendFile(ms)
            
            if self.pdata["MAKEPARAMS"]["MakeEnabled"]:
                mf = self.pdata["MAKEPARAMS"]["MakeFile"]
                if mf:
                    if not os.path.isabs(mf):
                        mf = os.path.join(self.ppath, mf)
                else:
                    mf = os.path.join(self.ppath, Project.DefaultMakefile)
                if not os.path.exists(mf):
                    try:
                        with open(mf, "w"):
                            pass
                    except OSError as err:
                        E5MessageBox.critical(
                            self.ui,
                            self.tr("Create Makefile"),
                            self.tr(
                                "<p>The makefile <b>{0}</b> could not"
                                " be created.<br/>Reason: {1}</p>")
                            .format(mf, str(err)))
                self.appendFile(mf)
            
            if self.pdata["PROJECTTYPE"] != projectType:
                # reinitialize filetype associations
                self.initFileTypes()
            
            if self.translationsRoot:
                tp = os.path.join(self.ppath, self.translationsRoot)
                if not self.translationsRoot.endswith(os.sep):
                    tp = os.path.dirname(tp)
            else:
                tp = self.ppath
            if not os.path.isdir(tp):
                os.makedirs(tp)
            if tp != self.ppath and tp not in self.subdirs:
                self.subdirs.append(tp)
            
            if self.pdata["TRANSLATIONSBINPATH"]:
                tp = os.path.join(
                    self.ppath, self.pdata["TRANSLATIONSBINPATH"])
                if not os.path.isdir(tp):
                    os.makedirs(tp)
                if tp != self.ppath and tp not in self.subdirs:
                    self.subdirs.append(tp)
            
            self.pluginGrp.setEnabled(
                self.pdata["PROJECTTYPE"] in ["E6Plugin"])
            
            self.__model.projectPropertiesChanged()
            self.projectPropertiesChanged.emit()
            
            if self.pdata["PROJECTTYPE"] != projectType:
                self.__reorganizeFiles()
        
    def __showUserProperties(self):
        """
        Private slot to display the user specific properties dialog.
        """
        vcsSystem = self.pdata["VCS"] or None
        vcsSystemOverride = self.pudata["VCSOVERRIDE"] or None
        
        from .UserPropertiesDialog import UserPropertiesDialog
        dlg = UserPropertiesDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.storeData()
            
            if (
                (self.pdata["VCS"] and
                 self.pdata["VCS"] != vcsSystem) or
                (self.pudata["VCSOVERRIDE"] and
                 self.pudata["VCSOVERRIDE"] != vcsSystemOverride) or
                (vcsSystemOverride is not None and
                    not self.pudata["VCSOVERRIDE"])
            ):
                # stop the VCS monitor thread and shutdown VCS
                if self.vcs is not None:
                    self.vcs.stopStatusMonitor()
                    self.vcs.vcsShutdown()
                    self.vcs.deleteLater()
                    self.vcs = None
                    e5App().getObject("PluginManager").deactivateVcsPlugins()
                # reinit VCS
                self.vcs = self.initVCS()
                # start the VCS monitor thread
                if self.vcs is not None:
                    self.vcs.startStatusMonitor(self)
                    self.vcs.vcsStatusMonitorData.connect(
                        self.__model.changeVCSStates)
                    self.vcs.vcsStatusMonitorStatus.connect(
                        self.__statusMonitorStatus)
                    self.vcs.vcsStatusMonitorInfo.connect(
                        self.vcsStatusMonitorInfo)
                    self.vcs.vcsStatusChanged.connect(self.__vcsStatusChanged)
                self.reinitVCS.emit()
            
            if self.pudata["VCSSTATUSMONITORINTERVAL"]:
                self.setStatusMonitorInterval(
                    self.pudata["VCSSTATUSMONITORINTERVAL"])
            else:
                self.setStatusMonitorInterval(
                    Preferences.getVCS("StatusMonitorInterval"))
        
    def __showFiletypeAssociations(self):
        """
        Private slot to display the filetype association dialog.
        """
        from .FiletypeAssociationDialog import FiletypeAssociationDialog
        dlg = FiletypeAssociationDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.transferData()
            self.setDirty(True)
            self.__reorganizeFiles()
    
    def getFiletypeAssociations(self, associationType):
        """
        Public method to get the list of file type associations for
        the given association type.
        
        @param associationType type of the association (one of FORMS,
            INTERFACES, OTHERS, PROTOCOLS, RESOURCES, SOURCES or
            TRANSLATIONS)
        @type str
        @return list of file patterns for the given type
        @rtype list of str
        """
        return [assoc for assoc in self.pdata["FILETYPES"]
                if self.pdata["FILETYPES"][assoc] == associationType]
    
    def __showLexerAssociations(self):
        """
        Private slot to display the lexer association dialog.
        """
        from .LexerAssociationDialog import LexerAssociationDialog
        dlg = LexerAssociationDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            dlg.transferData()
            self.setDirty(True)
            self.lexerAssociationsChanged.emit()
        
    def getEditorLexerAssoc(self, filename):
        """
        Public method to retrieve a lexer association.
        
        @param filename filename used to determine the associated lexer
            language (string)
        @return the requested lexer language (string)
        """
        # try user settings first
        for pattern, language in list(self.pdata["LEXERASSOCS"].items()):
            if fnmatch.fnmatch(filename, pattern):
                return language
        
        # try project type specific defaults next
        projectType = self.pdata["PROJECTTYPE"]
        try:
            if self.__lexerAssociationCallbacks[projectType] is not None:
                return self.__lexerAssociationCallbacks[projectType](filename)
        except KeyError:
            pass
        
        # return empty string to signal to use the global setting
        return ""
        
    @pyqtSlot()
    @pyqtSlot(str)
    def openProject(self, fn=None, restoreSession=True, reopen=False):
        """
        Public slot to open a project.
        
        @param fn optional filename of the project file to be read
        @param restoreSession flag indicating to restore the project
            session (boolean)
        @param reopen flag indicating a reopening of the project (boolean)
        """
        if not self.checkDirty():
            return
        
        if fn is None:
            fn = E5FileDialog.getOpenFileName(
                self.parent(),
                self.tr("Open project"),
                Preferences.getMultiProject("Workspace") or
                Utilities.getHomeDir(),
                self.tr("Project Files (*.epj);;XML Project Files (*.e4p)"))
        
        QApplication.processEvents()
        
        if fn:
            if self.closeProject():
                with E5OverrideCursor():
                    ok = self.__readProject(fn)
                if ok:
                    self.opened = True
                    if not self.pdata["FILETYPES"]:
                        self.initFileTypes()
                    else:
                        self.updateFileTypes()
                    
                    try:
                        # create management directory if not present
                        self.createProjectManagementDir()
                    except OSError:
                        E5MessageBox.critical(
                            self.ui,
                            self.tr("Create project management directory"),
                            self.tr(
                                "<p>The project directory <b>{0}</b> is not"
                                " writable.</p>")
                            .format(self.ppath))
                        return
                    
                    # read a user specific project file
                    self.__readUserProperties()
                    
                    with E5OverrideCursor():
                        oldState = self.isDirty()
                        self.vcs = self.initVCS()
                        if self.vcs is None and self.isDirty() == oldState:
                            # check, if project is version controlled
                            pluginManager = e5App().getObject("PluginManager")
                            for indicator, vcsData in (
                                pluginManager.getVcsSystemIndicators().items()
                            ):
                                if os.path.exists(
                                        os.path.join(self.ppath, indicator)):
                                    if len(vcsData) > 1:
                                        vcsList = []
                                        for (
                                            _vcsSystemStr, vcsSystemDisplay
                                        ) in vcsData:
                                            vcsList.append(vcsSystemDisplay)
                                        with E5OverridenCursor():
                                            res, vcs_ok = QInputDialog.getItem(
                                                None,
                                                self.tr("New Project"),
                                                self.tr(
                                                    "Select Version Control"
                                                    " System"),
                                                vcsList,
                                                0, False)
                                        if vcs_ok:
                                            for (
                                                vcsSystemStr, vcsSystemDisplay
                                            ) in vcsData:
                                                if res == vcsSystemDisplay:
                                                    vcsSystem = vcsSystemStr
                                                    break
                                            else:
                                                vcsSystem = "None"
                                        else:
                                            vcsSystem = "None"
                                    else:
                                        vcsSystem = vcsData[0][0]
                                    self.pdata["VCS"] = vcsSystem
                                    self.vcs = self.initVCS()
                                    self.setDirty(True)
                        if (
                            self.vcs is not None and
                            (self.vcs.vcsRegisteredState(self.ppath) !=
                                self.vcs.canBeCommitted)
                        ):
                            self.pdata["VCS"] = 'None'
                            self.vcs = self.initVCS()
                        self.closeAct.setEnabled(True)
                        self.saveasAct.setEnabled(True)
                        self.actGrp2.setEnabled(True)
                        self.propsAct.setEnabled(True)
                        self.userPropsAct.setEnabled(True)
                        self.filetypesAct.setEnabled(True)
                        self.lexersAct.setEnabled(True)
                        self.sessActGrp.setEnabled(True)
                        self.dbgActGrp.setEnabled(True)
                        self.menuDebuggerAct.setEnabled(True)
                        self.menuSessionAct.setEnabled(True)
                        self.menuCheckAct.setEnabled(True)
                        self.menuShowAct.setEnabled(True)
                        self.menuDiagramAct.setEnabled(True)
                        self.menuApidocAct.setEnabled(True)
                        self.menuPackagersAct.setEnabled(True)
                        self.pluginGrp.setEnabled(
                            self.pdata["PROJECTTYPE"] in ["E6Plugin"])
                        self.addLanguageAct.setEnabled(
                            bool(self.pdata["TRANSLATIONPATTERN"]))
                        self.makeGrp.setEnabled(
                            self.pdata["MAKEPARAMS"]["MakeEnabled"])
                        self.menuMakeAct.setEnabled(
                            self.pdata["MAKEPARAMS"]["MakeEnabled"])
                        
                        # open a project debugger properties file being quiet
                        # about errors
                        if Preferences.getProject("AutoLoadDbgProperties"):
                            self.__readDebugProperties(True)
                        
                        self.__model.projectOpened()
                        self.projectOpenedHooks.emit()
                        self.projectOpened.emit()
                    
                    if Preferences.getProject("SearchNewFiles"):
                        self.__doSearchNewFiles()
                    
                    # read a project tasks file
                    self.__readTasks()
                    self.ui.taskViewer.setProjectOpen(True)
                    # rescan project tasks
                    if Preferences.getProject("TasksProjectRescanOnOpen"):
                        e5App().getObject("TaskViewer"
                                          ).regenerateProjectTasks(quiet=True)
                    
                    if restoreSession:
                        # open the main script
                        if self.pdata["MAINSCRIPT"]:
                            if not os.path.isabs(self.pdata["MAINSCRIPT"]):
                                ms = os.path.join(
                                    self.ppath, self.pdata["MAINSCRIPT"])
                            else:
                                ms = self.pdata["MAINSCRIPT"]
                            self.sourceFile.emit(ms)
                        
                        # open a project session file being quiet about errors
                        if reopen:
                            self.__readSession(quiet=True, indicator="_tmp")
                        elif Preferences.getProject("AutoLoadSession"):
                            self.__readSession(quiet=True)
                    
                    # start the VCS monitor thread
                    if self.vcs is not None:
                        self.vcs.startStatusMonitor(self)
                        self.vcs.vcsStatusMonitorData.connect(
                            self.__model.changeVCSStates)
                        self.vcs.vcsStatusMonitorStatus.connect(
                            self.__statusMonitorStatus)
                        self.vcs.vcsStatusMonitorInfo.connect(
                            self.vcsStatusMonitorInfo)
                        self.vcs.vcsStatusChanged.connect(
                            self.__vcsStatusChanged)
        
    def reopenProject(self):
        """
        Public slot to reopen the current project.
        """
        projectFile = self.pfile
        res = self.closeProject(reopen=True)
        if res:
            self.openProject(projectFile, reopen=True)
        
    def saveProject(self):
        """
        Public slot to save the current project.
        
        @return flag indicating success
        """
        if self.isDirty():
            if len(self.pfile) > 0:
                if self.pfile.endswith(".e4p"):
                    self.pfile = self.pfile.replace(".e4p", ".epj")
                    self.__syncRecent()
                ok = self.__writeProject()
            else:
                ok = self.saveProjectAs()
        else:
            ok = True
        self.sessActGrp.setEnabled(ok)
        self.menuSessionAct.setEnabled(ok)
        return ok
        
    def saveProjectAs(self):
        """
        Public slot to save the current project to a different file.
        
        @return flag indicating success (boolean)
        """
        defaultFilter = self.tr("Project Files (*.epj)")
        if self.ppath:
            defaultPath = self.ppath
        else:
            defaultPath = (
                Preferences.getMultiProject("Workspace") or
                Utilities.getHomeDir()
            )
        fn, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
            self.parent(),
            self.tr("Save project as"),
            defaultPath,
            self.tr("Project Files (*.epj);;"
                    "XML Project Files (*.e4p)"),
            defaultFilter,
            E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
        
        if fn:
            ext = QFileInfo(fn).suffix()
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fn += ex
            if QFileInfo(fn).exists():
                res = E5MessageBox.yesNo(
                    self.ui,
                    self.tr("Save File"),
                    self.tr("""<p>The file <b>{0}</b> already exists."""
                            """ Overwrite it?</p>""").format(fn),
                    icon=E5MessageBox.Warning)
                if not res:
                    return False
                
            self.name = QFileInfo(fn).baseName()
            ok = self.__writeProject(fn)
            
            if ok:
                # create management directory if not present
                self.createProjectManagementDir()
                
                # now save the tasks
                self.writeTasks()
            
            self.sessActGrp.setEnabled(ok)
            self.menuSessionAct.setEnabled(ok)
            self.projectClosedHooks.emit()
            self.projectClosed.emit()
            self.projectOpenedHooks.emit()
            self.projectOpened.emit()
            return ok
        else:
            return False
    
    def checkDirty(self):
        """
        Public method to check dirty status and open a message window.
        
        @return flag indicating whether this operation was successful (boolean)
        """
        if self.isDirty():
            res = E5MessageBox.okToClearData(
                self.parent(),
                self.tr("Close Project"),
                self.tr("The current project has unsaved changes."),
                self.saveProject)
            if res:
                self.setDirty(False)
            return res
            
        return True
        
    def __closeAllWindows(self):
        """
        Private method to close all project related windows.
        """
        self.codemetrics and self.codemetrics.close()
        self.codecoverage and self.codecoverage.close()
        self.profiledata and self.profiledata.close()
        self.applicationDiagram and self.applicationDiagram.close()
        self.loadedDiagram and self.loadedDiagram.close()
        
    @pyqtSlot()
    def closeProject(self, reopen=False, noSave=False):
        """
        Public slot to close the current project.
        
        @param reopen flag indicating a reopening of the project (boolean)
        @param noSave flag indicating to not perform save actions (boolean)
        @return flag indicating success (boolean)
        """
        # save the list of recently opened projects
        self.__saveRecent()
        
        if not self.isOpen():
            return True
        
        if not self.checkDirty():
            return False
        
        e5App().getObject("TaskViewer").stopProjectTaskExtraction()
        
        # save the user project properties
        if not noSave:
            self.__writeUserProperties()
        
        # save the project session file being quiet about error
        if reopen:
            self.__writeSession(quiet=True, indicator="_tmp")
        elif Preferences.getProject("AutoSaveSession") and not noSave:
            self.__writeSession(quiet=True)
        
        # save the project debugger properties file being quiet about error
        if (
            Preferences.getProject("AutoSaveDbgProperties") and
            self.isDebugPropertiesLoaded() and
            not noSave and self.debugPropertiesChanged
        ):
            self.__writeDebugProperties(True)
        
        vm = e5App().getObject("ViewManager")
        
        # check dirty status of all project files first
        for fn in vm.getOpenFilenames():
            if self.isProjectFile(fn):
                reset = vm.checkFileDirty(fn)
                if not reset:
                    # abort shutting down
                    return False
        
        # close all project related editors
        success = True
        for fn in vm.getOpenFilenames():
            if self.isProjectFile(fn):
                success &= vm.closeWindow(fn, ignoreDirty=True)
        if not success:
            return False
        
        # stop the VCS monitor thread
        if self.vcs is not None:
            self.vcs.stopStatusMonitor()
        
        # now save the tasks
        if not noSave:
            self.writeTasks()
        self.ui.taskViewer.clearProjectTasks()
        self.ui.taskViewer.setProjectOpen(False)
        
        # now shutdown the vcs interface
        if self.vcs:
            self.vcs.vcsShutdown()
            self.vcs.deleteLater()
            self.vcs = None
            e5App().getObject("PluginManager").deactivateVcsPlugins()
        
        # now close all project related tool windows
        self.__closeAllWindows()
        
        self.__initData()
        self.closeAct.setEnabled(False)
        self.saveasAct.setEnabled(False)
        self.saveAct.setEnabled(False)
        self.actGrp2.setEnabled(False)
        self.propsAct.setEnabled(False)
        self.userPropsAct.setEnabled(False)
        self.filetypesAct.setEnabled(False)
        self.lexersAct.setEnabled(False)
        self.sessActGrp.setEnabled(False)
        self.dbgActGrp.setEnabled(False)
        self.menuDebuggerAct.setEnabled(False)
        self.menuSessionAct.setEnabled(False)
        self.menuCheckAct.setEnabled(False)
        self.menuShowAct.setEnabled(False)
        self.menuDiagramAct.setEnabled(False)
        self.menuApidocAct.setEnabled(False)
        self.menuPackagersAct.setEnabled(False)
        self.pluginGrp.setEnabled(False)
        self.makeGrp.setEnabled(False)
        self.menuMakeAct.setEnabled(False)
        
        self.__model.projectClosed()
        self.projectClosedHooks.emit()
        self.projectClosed.emit()
        
        return True

    def saveAllScripts(self, reportSyntaxErrors=False):
        """
        Public method to save all scripts belonging to the project.
        
        @param reportSyntaxErrors flag indicating special reporting
            for syntax errors (boolean)
        @return flag indicating success (boolean)
        """
        vm = e5App().getObject("ViewManager")
        success = True
        filesWithSyntaxErrors = 0
        for fn in vm.getOpenFilenames():
            rfn = self.getRelativePath(fn)
            if rfn in self.pdata["SOURCES"] or rfn in self.pdata["OTHERS"]:
                editor = vm.getOpenEditor(fn)
                success &= vm.saveEditorEd(editor)
                if reportSyntaxErrors and editor.hasSyntaxErrors():
                    filesWithSyntaxErrors += 1
        
        if reportSyntaxErrors and filesWithSyntaxErrors > 0:
            E5MessageBox.critical(
                self.ui,
                self.tr("Syntax errors detected"),
                self.tr(
                    """The project contains %n file(s) with syntax errors.""",
                    "", filesWithSyntaxErrors)
            )
            return False
        else:
            return success
        
    def checkAllScriptsDirty(self, reportSyntaxErrors=False):
        """
        Public method to check all scripts belonging to the project for
        their dirty status.
        
        @param reportSyntaxErrors flag indicating special reporting
            for syntax errors (boolean)
        @return flag indicating success (boolean)
        """
        vm = e5App().getObject("ViewManager")
        success = True
        filesWithSyntaxErrors = 0
        for fn in vm.getOpenFilenames():
            rfn = self.getRelativePath(fn)
            if rfn in self.pdata["SOURCES"] or rfn in self.pdata["OTHERS"]:
                editor = vm.getOpenEditor(fn)
                success &= editor.checkDirty()
                if reportSyntaxErrors and editor.hasSyntaxErrors():
                    filesWithSyntaxErrors += 1
        
        if reportSyntaxErrors and filesWithSyntaxErrors > 0:
            E5MessageBox.critical(
                self.ui,
                self.tr("Syntax errors detected"),
                self.tr(
                    """The project contains %n file(s) with syntax errors.""",
                    "", filesWithSyntaxErrors)
            )
            return False
        else:
            return success

    def getMainScript(self, normalized=False):
        """
        Public method to return the main script filename.
        
        @param normalized flag indicating a normalized filename is wanted
            (boolean)
        @return filename of the projects main script (string)
        """
        if self.pdata["MAINSCRIPT"]:
            if normalized:
                return os.path.join(self.ppath, self.pdata["MAINSCRIPT"])
            else:
                return self.pdata["MAINSCRIPT"]
        else:
            return None
        
    def getSources(self, normalized=False):
        """
        Public method to return the source script files.
        
        @param normalized flag indicating a normalized filename is wanted
            (boolean)
        @return list of the projects scripts (list of string)
        """
        return self.getProjectFiles("SOURCES", normalized=normalized)
    
    def getProjectFiles(self, fileType, normalized=False):
        """
        Public method to get the file entries of the given type.
        
        @param fileType project file type (one of SOURCES, FORMS, RESOURCES,
            INTERFACES, PROTOCOLS, OTHERS, TRANSLATIONS)
        @type str
        @param normalized flag indicating normalized file names are wanted
        @type boolean
        @return list of file names
        @rtype list of str
        @exception ValueError raised when an unsupported file type is given
        """
        if fileType not in ["SOURCES", "FORMS", "RESOURCES", "INTERFACES",
                            "PROTOCOLS", "OTHERS", "TRANSLATIONS"]:
            raise ValueError("Given file type has incorrect value.")
        
        if normalized:
            return [os.path.join(self.ppath, fn) for fn in
                    self.pdata[fileType]]
        else:
            return self.pdata[fileType]
        
    def getProjectType(self):
        """
        Public method to get the type of the project.
        
        @return UI type of the project (string)
        """
        return self.pdata["PROJECTTYPE"]
        
    def getProjectLanguage(self):
        """
        Public method to get the project's programming language.
        
        @return programming language (string)
        """
        return self.pdata["PROGLANGUAGE"]
        
    def isMixedLanguageProject(self):
        """
        Public method to check, if this is a mixed language project.
        
        @return flag indicating a mixed language project
        @rtype bool
        """
        return self.pdata["MIXEDLANGUAGE"]
        
    def isPythonProject(self):
        """
        Public method to check, if this project is a Python3 or MicroPython
        project.
        
        @return flag indicating a Python project (boolean)
        """
        return self.pdata["PROGLANGUAGE"] in ["Python3", "MicroPython"]
        
    def isPy3Project(self):
        """
        Public method to check, if this project is a Python3 project.
        
        @return flag indicating a Python3 project (boolean)
        """
        return self.pdata["PROGLANGUAGE"] == "Python3"
    
    def isMicroPythonProject(self):
        """
        Public method to check, if this project is a MicroPython project.
        
        @return flag indicating a MicroPython project
        @rtype bool
        """
        return self.pdata["PROGLANGUAGE"] == "MicroPython"
        
    def isRubyProject(self):
        """
        Public method to check, if this project is a Ruby project.
        
        @return flag indicating a Ruby project (boolean)
        """
        return self.pdata["PROGLANGUAGE"] == "Ruby"
        
    def isJavaScriptProject(self):
        """
        Public method to check, if this project is a JavaScript project.
        
        @return flag indicating a JavaScript project (boolean)
        """
        return self.pdata["PROGLANGUAGE"] == "JavaScript"
        
    def getProjectSpellLanguage(self):
        """
        Public method to get the project's programming language.
        
        @return programming language (string)
        """
        return self.pdata["SPELLLANGUAGE"]
        
    def getProjectDictionaries(self):
        """
        Public method to get the names of the project specific dictionaries.
        
        @return tuple of two strings giving the absolute path names of the
            project specific word and exclude list
        """
        pwl = ""
        if self.pdata["SPELLWORDS"]:
            pwl = os.path.join(self.ppath, self.pdata["SPELLWORDS"])
        
        pel = ""
        if self.pdata["SPELLEXCLUDES"]:
            pel = os.path.join(self.ppath, self.pdata["SPELLEXCLUDES"])
        
        return (pwl, pel)
        
    def getDefaultSourceExtension(self):
        """
        Public method to get the default extension for the project's
        programming language.
        
        @return default extension (including the dot) (string)
        """
        lang = self.pdata["PROGLANGUAGE"]
        if lang == "":
            lang = "Python3"
        elif lang == "Python":
            lang = "Python3"
        return self.__sourceExtensions(lang)[0]
        
    def getProjectPath(self):
        """
        Public method to get the project path.
        
        @return project path (string)
        """
        return self.ppath
        
    def startswithProjectPath(self, path):
        """
        Public method to check, if a path starts with the project path.
        
        @param path path to be checked (string)
        @return flag indicating that the path starts with the project path
            (boolean)
        """
        if self.ppath:
            if path == self.ppath:
                return True
            elif (
                Utilities.normcasepath(Utilities.toNativeSeparators(path))
                .startswith(Utilities.normcasepath(
                    Utilities.toNativeSeparators(self.ppath + "/")))
            ):
                return True
            else:
                return False
        else:
            return False
        
    def getProjectFile(self):
        """
        Public method to get the path of the project file.
        
        @return path of the project file (string)
        """
        return self.pfile
        
    def getProjectName(self):
        """
        Public method to get the name of the project.
        
        The project name is determined from the name of the project file.
        
        @return name of the project (string)
        """
        if self.pfile:
            name = os.path.splitext(self.pfile)[0]
            return os.path.basename(name)
        else:
            return ""
        
    def getProjectManagementDir(self):
        """
        Public method to get the path of the management directory.
        
        @return path of the management directory (string)
        """
        if Utilities.isWindowsPlatform():
            # migrate the old project management directory ( < v18.06)
            oldDir = os.path.join(self.ppath, "_eric6project")
            if os.path.exists(oldDir):
                os.rename(
                    oldDir,
                    os.path.join(self.ppath, ".eric6project")
                )
        
        return os.path.join(self.ppath, ".eric6project")
        
    def createProjectManagementDir(self):
        """
        Public method to create the project management directory.
        
        It does nothing, if it already exists.
        """
        # create management directory if not present
        mgmtDir = self.getProjectManagementDir()
        if not os.path.exists(mgmtDir):
            os.makedirs(mgmtDir)
        
    def getHash(self):
        """
        Public method to get the project hash.
        
        @return project hash as a hex string (string)
        """
        return self.pdata["HASH"]
        
    def getRelativePath(self, path):
        """
        Public method to convert a file path to a project relative
        file path.
        
        @param path file or directory name to convert (string)
        @return project relative path or unchanged path, if path doesn't
            belong to the project (string)
        """
        if self.startswithProjectPath(path):
            if self.ppath and path == self.ppath:
                return ""
            else:
                relpath = path[len(self.ppath):]
                if relpath.startswith(("/", "\\")):
                    relpath = relpath[1:]
                return relpath
        else:
            return path
        
    def getRelativeUniversalPath(self, path):
        """
        Public method to convert a file path to a project relative
        file path with universal separators.
        
        @param path file or directory name to convert (string)
        @return project relative path or unchanged path, if path doesn't
            belong to the project (string)
        """
        return Utilities.fromNativeSeparators(self.getRelativePath(path))
        
    def getAbsolutePath(self, fn):
        """
        Public method to convert a project relative file path to an absolute
        file path.
        
        @param fn file or directory name to convert (string)
        @return absolute path (string)
        """
        if not os.path.isabs(fn):
            fn = os.path.join(self.ppath, fn)
        return fn
        
    def getAbsoluteUniversalPath(self, fn):
        """
        Public method to convert a project relative file path with universal
        separators to an absolute file path.
        
        @param fn file or directory name to convert (string)
        @return absolute path (string)
        """
        if not os.path.isabs(fn):
            fn = os.path.join(self.ppath, Utilities.toNativeSeparators(fn))
        return fn
        
    def getEolString(self):
        """
        Public method to get the EOL-string to be used by the project.
        
        @return eol string (string)
        """
        if self.pdata["EOL"] >= 0:
            return self.eols[self.pdata["EOL"]]
        else:
            eolMode = Preferences.getEditor("EOLMode")
            if eolMode == QsciScintilla.EolMode.EolWindows:
                eol = '\r\n'
            elif eolMode == QsciScintilla.EolMode.EolUnix:
                eol = '\n'
            elif eolMode == QsciScintilla.EolMode.EolMac:
                eol = '\r'
            else:
                eol = os.linesep
            return eol
        
    def useSystemEol(self):
        """
        Public method to check, if the project uses the system eol setting.
        
        @return flag indicating the usage of system eol (boolean)
        """
        return self.pdata["EOL"] == 0
    
    def getProjectVersion(self):
        """
        Public mehod to get the version number of the project.
        
        @return version number
        @rtype str
        """
        return self.pdata["VERSION"]
    
    def getProjectAuthor(self):
        """
        Public method to get the author of the project.
        
        @return author name
        @rtype str
        """
        return self.pdata["AUTHOR"]
    
    def getProjectAuthorEmail(self):
        """
        Public method to get the email address of the project author.
        
        @return project author email
        @rtype str
        """
        return self.pdata["EMAIL"]
    
    def getProjectDescription(self):
        """
        Public method to get the description of the project.
        
        @return project description
        @rtype str
        """
        return self.pdata["DESCRIPTION"]
    
    def __isInPdata(self, fn):
        """
        Private method used to check, if the passed in filename is project
        controlled..
        
        @param fn filename to be checked
        @type str
        @return flag indicating membership
        @rtype bool
        """
        newfn = os.path.abspath(fn)
        newfn = self.getRelativePath(newfn)
        for group in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS",
                      "RESOURCES", "TRANSLATIONS", "OTHERS"]:
            if newfn in self.pdata[group]:
                return True
        return False
    
    def isProjectFile(self, fn):
        """
        Public method used to check, if the passed in filename belongs to the
        project.
        
        @param fn filename to be checked (string)
        @return flag indicating membership (boolean)
        """
        for group in ["SOURCES", "FORMS", "INTERFACES", "PROTOCOLS",
                      "RESOURCES", "TRANSLATIONS", "OTHERS"]:
            if self.__checkProjectFileGroup(fn, group):
                return True
        
        return False
        
    def __checkProjectFileGroup(self, fn, group):
        """
        Private method to check, if a file is in a specific file group of the
        project.
        
        @param fn filename to be checked (string)
        @param group group to check (string)
        @return flag indicating membership (boolean)
        """
        newfn = os.path.abspath(fn)
        newfn = self.getRelativePath(newfn)
        if newfn in self.pdata[group]:
            return True
        elif group == "OTHERS":
            for entry in self.pdata[group]:
                if newfn.startswith(entry):
                    return True
        
        if Utilities.isWindowsPlatform():
            # try the above case-insensitive
            newfn = newfn.lower()
            for entry in self.pdata[group]:
                if entry.lower() == newfn:
                    return True
        elif group == "OTHERS":
            for entry in self.pdata[group]:
                if newfn.startswith(entry.lower()):
                    return True
        
        return False
        
    def isProjectSource(self, fn):
        """
        Public method used to check, if the passed in filename belongs to the
        project sources.
        
        @param fn filename to be checked (string)
        @return flag indicating membership (boolean)
        """
        return self.__checkProjectFileGroup(fn, "SOURCES")
        
    def isProjectForm(self, fn):
        """
        Public method used to check, if the passed in filename belongs to the
        project forms.
        
        @param fn filename to be checked (string)
        @return flag indicating membership (boolean)
        """
        return self.__checkProjectFileGroup(fn, "FORMS")
        
    def isProjectInterface(self, fn):
        """
        Public method used to check, if the passed in filename belongs to the
        project interfaces.
        
        @param fn filename to be checked (string)
        @return flag indicating membership (boolean)
        """
        return self.__checkProjectFileGroup(fn, "INTERFACES")
        
    def isProjectProtocol(self, fn):
        """
        Public method used to check, if the passed in filename belongs to the
        project protocols.
        
        @param fn filename to be checked
        @type str
        @return flag indicating membership
        @rtype bool
        """
        return self.__checkProjectFileGroup(fn, "PROTOCOLS")
    
    def isProjectResource(self, fn):
        """
        Public method used to check, if the passed in filename belongs to the
        project resources.
        
        @param fn filename to be checked (string)
        @return flag indicating membership (boolean)
        """
        return self.__checkProjectFileGroup(fn, "RESOURCES")
        
    def initActions(self):
        """
        Public slot to initialize the project related actions.
        """
        self.actions = []
        
        self.actGrp1 = createActionGroup(self)
        
        act = E5Action(
            self.tr('New project'),
            UI.PixmapCache.getIcon("projectNew"),
            self.tr('&New...'), 0, 0,
            self.actGrp1, 'project_new')
        act.setStatusTip(self.tr('Generate a new project'))
        act.setWhatsThis(self.tr(
            """<b>New...</b>"""
            """<p>This opens a dialog for entering the info for a"""
            """ new project.</p>"""
        ))
        act.triggered.connect(self.createNewProject)
        self.actions.append(act)

        act = E5Action(
            self.tr('Open project'),
            UI.PixmapCache.getIcon("projectOpen"),
            self.tr('&Open...'), 0, 0,
            self.actGrp1, 'project_open')
        act.setStatusTip(self.tr('Open an existing project'))
        act.setWhatsThis(self.tr(
            """<b>Open...</b>"""
            """<p>This opens an existing project.</p>"""
        ))
        act.triggered.connect(self.openProject)
        self.actions.append(act)

        self.closeAct = E5Action(
            self.tr('Close project'),
            UI.PixmapCache.getIcon("projectClose"),
            self.tr('&Close'), 0, 0, self, 'project_close')
        self.closeAct.setStatusTip(self.tr('Close the current project'))
        self.closeAct.setWhatsThis(self.tr(
            """<b>Close</b>"""
            """<p>This closes the current project.</p>"""
        ))
        self.closeAct.triggered.connect(self.closeProject)
        self.actions.append(self.closeAct)

        self.saveAct = E5Action(
            self.tr('Save project'),
            UI.PixmapCache.getIcon("projectSave"),
            self.tr('&Save'), 0, 0, self, 'project_save')
        self.saveAct.setStatusTip(self.tr('Save the current project'))
        self.saveAct.setWhatsThis(self.tr(
            """<b>Save</b>"""
            """<p>This saves the current project.</p>"""
        ))
        self.saveAct.triggered.connect(self.saveProject)
        self.actions.append(self.saveAct)

        self.saveasAct = E5Action(
            self.tr('Save project as'),
            UI.PixmapCache.getIcon("projectSaveAs"),
            self.tr('Save &as...'), 0, 0, self, 'project_save_as')
        self.saveasAct.setStatusTip(self.tr(
            'Save the current project to a new file'))
        self.saveasAct.setWhatsThis(self.tr(
            """<b>Save as</b>"""
            """<p>This saves the current project to a new file.</p>"""
        ))
        self.saveasAct.triggered.connect(self.saveProjectAs)
        self.actions.append(self.saveasAct)

        self.actGrp2 = createActionGroup(self)
        
        self.addFilesAct = E5Action(
            self.tr('Add files to project'),
            UI.PixmapCache.getIcon("fileMisc"),
            self.tr('Add &files...'), 0, 0,
            self.actGrp2, 'project_add_file')
        self.addFilesAct.setStatusTip(self.tr(
            'Add files to the current project'))
        self.addFilesAct.setWhatsThis(self.tr(
            """<b>Add files...</b>"""
            """<p>This opens a dialog for adding files"""
            """ to the current project. The place to add is"""
            """ determined by the file extension.</p>"""
        ))
        self.addFilesAct.triggered.connect(self.addFiles)
        self.actions.append(self.addFilesAct)

        self.addDirectoryAct = E5Action(
            self.tr('Add directory to project'),
            UI.PixmapCache.getIcon("dirOpen"),
            self.tr('Add directory...'), 0, 0,
            self.actGrp2, 'project_add_directory')
        self.addDirectoryAct.setStatusTip(
            self.tr('Add a directory to the current project'))
        self.addDirectoryAct.setWhatsThis(self.tr(
            """<b>Add directory...</b>"""
            """<p>This opens a dialog for adding a directory"""
            """ to the current project.</p>"""
        ))
        self.addDirectoryAct.triggered.connect(self.addDirectory)
        self.actions.append(self.addDirectoryAct)

        self.addLanguageAct = E5Action(
            self.tr('Add translation to project'),
            UI.PixmapCache.getIcon("linguist4"),
            self.tr('Add &translation...'), 0, 0,
            self.actGrp2, 'project_add_translation')
        self.addLanguageAct.setStatusTip(
            self.tr('Add a translation to the current project'))
        self.addLanguageAct.setWhatsThis(self.tr(
            """<b>Add translation...</b>"""
            """<p>This opens a dialog for add a translation"""
            """ to the current project.</p>"""
        ))
        self.addLanguageAct.triggered.connect(self.addLanguage)
        self.actions.append(self.addLanguageAct)

        act = E5Action(
            self.tr('Search new files'),
            self.tr('Searc&h new files...'), 0, 0,
            self.actGrp2, 'project_search_new_files')
        act.setStatusTip(self.tr(
            'Search new files in the project directory.'))
        act.setWhatsThis(self.tr(
            """<b>Search new files...</b>"""
            """<p>This searches for new files (sources, *.ui, *.idl,"""
            """ *.proto) in the project directory and registered"""
            """ subdirectories.</p>"""
        ))
        act.triggered.connect(self.__searchNewFiles)
        self.actions.append(act)

        act = E5Action(
            self.tr('Search Project File'),
            self.tr('Search Project File...'),
            QKeySequence(self.tr("Alt+Ctrl+P", "Project|Search Project File")),
            0,
            self.actGrp2, 'project_search_project_file')
        act.setStatusTip(self.tr(
            'Search for a file in the project list of files.'))
        act.setWhatsThis(self.tr(
            """<b>Search Project File</b>"""
            """<p>This searches for a file in the project list of files.</p>"""
        ))
        act.triggered.connect(self.__searchProjectFile)
        self.actions.append(act)
        
        self.propsAct = E5Action(
            self.tr('Project properties'),
            UI.PixmapCache.getIcon("projectProps"),
            self.tr('&Properties...'), 0, 0, self,
            'project_properties')
        self.propsAct.setStatusTip(self.tr('Show the project properties'))
        self.propsAct.setWhatsThis(self.tr(
            """<b>Properties...</b>"""
            """<p>This shows a dialog to edit the project properties.</p>"""
        ))
        self.propsAct.triggered.connect(self.__showProperties)
        self.actions.append(self.propsAct)

        self.userPropsAct = E5Action(
            self.tr('User project properties'),
            UI.PixmapCache.getIcon("projectUserProps"),
            self.tr('&User Properties...'), 0, 0, self,
            'project_user_properties')
        self.userPropsAct.setStatusTip(self.tr(
            'Show the user specific project properties'))
        self.userPropsAct.setWhatsThis(self.tr(
            """<b>User Properties...</b>"""
            """<p>This shows a dialog to edit the user specific project"""
            """ properties.</p>"""
        ))
        self.userPropsAct.triggered.connect(self.__showUserProperties)
        self.actions.append(self.userPropsAct)

        self.filetypesAct = E5Action(
            self.tr('Filetype Associations'),
            self.tr('Filetype Associations...'), 0, 0,
            self, 'project_filetype_associations')
        self.filetypesAct.setStatusTip(
            self.tr('Show the project file type associations'))
        self.filetypesAct.setWhatsThis(self.tr(
            """<b>Filetype Associations...</b>"""
            """<p>This shows a dialog to edit the file type associations of"""
            """ the project. These associations determine the type"""
            """ (source, form, interface, protocol or others) with a"""
            """ filename pattern. They are used when adding a file to the"""
            """ project and when performing a search for new files.</p>"""
        ))
        self.filetypesAct.triggered.connect(
            self.__showFiletypeAssociations)
        self.actions.append(self.filetypesAct)

        self.lexersAct = E5Action(
            self.tr('Lexer Associations'),
            self.tr('Lexer Associations...'), 0, 0,
            self, 'project_lexer_associations')
        self.lexersAct.setStatusTip(self.tr(
            'Show the project lexer associations (overriding defaults)'))
        self.lexersAct.setWhatsThis(self.tr(
            """<b>Lexer Associations...</b>"""
            """<p>This shows a dialog to edit the lexer associations of"""
            """ the project. These associations override the global lexer"""
            """ associations. Lexers are used to highlight the editor"""
            """ text.</p>"""
        ))
        self.lexersAct.triggered.connect(self.__showLexerAssociations)
        self.actions.append(self.lexersAct)

        self.dbgActGrp = createActionGroup(self)
        
        act = E5Action(
            self.tr('Debugger Properties'),
            self.tr('Debugger &Properties...'), 0, 0,
            self.dbgActGrp, 'project_debugger_properties')
        act.setStatusTip(self.tr('Show the debugger properties'))
        act.setWhatsThis(self.tr(
            """<b>Debugger Properties...</b>"""
            """<p>This shows a dialog to edit project specific debugger"""
            """ settings.</p>"""
        ))
        act.triggered.connect(self.__showDebugProperties)
        self.actions.append(act)
        
        act = E5Action(
            self.tr('Load'),
            self.tr('&Load'), 0, 0,
            self.dbgActGrp, 'project_debugger_properties_load')
        act.setStatusTip(self.tr('Load the debugger properties'))
        act.setWhatsThis(self.tr(
            """<b>Load Debugger Properties</b>"""
            """<p>This loads the project specific debugger settings.</p>"""
        ))
        act.triggered.connect(self.__readDebugProperties)
        self.actions.append(act)
        
        act = E5Action(
            self.tr('Save'),
            self.tr('&Save'), 0, 0,
            self.dbgActGrp, 'project_debugger_properties_save')
        act.setStatusTip(self.tr('Save the debugger properties'))
        act.setWhatsThis(self.tr(
            """<b>Save Debugger Properties</b>"""
            """<p>This saves the project specific debugger settings.</p>"""
        ))
        act.triggered.connect(self.__writeDebugProperties)
        self.actions.append(act)
        
        act = E5Action(
            self.tr('Delete'),
            self.tr('&Delete'), 0, 0,
            self.dbgActGrp, 'project_debugger_properties_delete')
        act.setStatusTip(self.tr('Delete the debugger properties'))
        act.setWhatsThis(self.tr(
            """<b>Delete Debugger Properties</b>"""
            """<p>This deletes the file containing the project specific"""
            """ debugger settings.</p>"""
        ))
        act.triggered.connect(self.__deleteDebugProperties)
        self.actions.append(act)
        
        act = E5Action(
            self.tr('Reset'),
            self.tr('&Reset'), 0, 0,
            self.dbgActGrp, 'project_debugger_properties_resets')
        act.setStatusTip(self.tr('Reset the debugger properties'))
        act.setWhatsThis(self.tr(
            """<b>Reset Debugger Properties</b>"""
            """<p>This resets the project specific debugger settings.</p>"""
        ))
        act.triggered.connect(self.__initDebugProperties)
        self.actions.append(act)
        
        self.sessActGrp = createActionGroup(self)

        act = E5Action(
            self.tr('Load session'),
            self.tr('Load session'), 0, 0,
            self.sessActGrp, 'project_load_session')
        act.setStatusTip(self.tr('Load the projects session file.'))
        act.setWhatsThis(self.tr(
            """<b>Load session</b>"""
            """<p>This loads the projects session file. The session consists"""
            """ of the following data.<br>"""
            """- all open source files<br>"""
            """- all breakpoint<br>"""
            """- the commandline arguments<br>"""
            """- the working directory<br>"""
            """- the exception reporting flag</p>"""
        ))
        act.triggered.connect(self.__readSession)
        self.actions.append(act)

        act = E5Action(
            self.tr('Save session'),
            self.tr('Save session'), 0, 0,
            self.sessActGrp, 'project_save_session')
        act.setStatusTip(self.tr('Save the projects session file.'))
        act.setWhatsThis(self.tr(
            """<b>Save session</b>"""
            """<p>This saves the projects session file. The session consists"""
            """ of the following data.<br>"""
            """- all open source files<br>"""
            """- all breakpoint<br>"""
            """- the commandline arguments<br>"""
            """- the working directory<br>"""
            """- the exception reporting flag</p>"""
        ))
        act.triggered.connect(self.__writeSession)
        self.actions.append(act)
        
        act = E5Action(
            self.tr('Delete session'),
            self.tr('Delete session'), 0, 0,
            self.sessActGrp, 'project_delete_session')
        act.setStatusTip(self.tr('Delete the projects session file.'))
        act.setWhatsThis(self.tr(
            """<b>Delete session</b>"""
            """<p>This deletes the projects session file</p>"""
        ))
        act.triggered.connect(self.__deleteSession)
        self.actions.append(act)
        
        self.chkGrp = createActionGroup(self)

        self.codeMetricsAct = E5Action(
            self.tr('Code Metrics'),
            self.tr('&Code Metrics...'), 0, 0,
            self.chkGrp, 'project_code_metrics')
        self.codeMetricsAct.setStatusTip(
            self.tr('Show some code metrics for the project.'))
        self.codeMetricsAct.setWhatsThis(self.tr(
            """<b>Code Metrics...</b>"""
            """<p>This shows some code metrics for all Python files in"""
            """ the project.</p>"""
        ))
        self.codeMetricsAct.triggered.connect(self.__showCodeMetrics)
        self.actions.append(self.codeMetricsAct)

        self.codeCoverageAct = E5Action(
            self.tr('Python Code Coverage'),
            self.tr('Code Co&verage...'), 0, 0,
            self.chkGrp, 'project_code_coverage')
        self.codeCoverageAct.setStatusTip(
            self.tr('Show code coverage information for the project.'))
        self.codeCoverageAct.setWhatsThis(self.tr(
            """<b>Code Coverage...</b>"""
            """<p>This shows the code coverage information for all Python"""
            """ files in the project.</p>"""
        ))
        self.codeCoverageAct.triggered.connect(self.__showCodeCoverage)
        self.actions.append(self.codeCoverageAct)

        self.codeProfileAct = E5Action(
            self.tr('Profile Data'),
            self.tr('&Profile Data...'), 0, 0,
            self.chkGrp, 'project_profile_data')
        self.codeProfileAct.setStatusTip(
            self.tr('Show profiling data for the project.'))
        self.codeProfileAct.setWhatsThis(self.tr(
            """<b>Profile Data...</b>"""
            """<p>This shows the profiling data for the project.</p>"""
        ))
        self.codeProfileAct.triggered.connect(self.__showProfileData)
        self.actions.append(self.codeProfileAct)

        self.graphicsGrp = createActionGroup(self)

        self.applicationDiagramAct = E5Action(
            self.tr('Application Diagram'),
            self.tr('&Application Diagram...'), 0, 0,
            self.graphicsGrp, 'project_application_diagram')
        self.applicationDiagramAct.setStatusTip(
            self.tr('Show a diagram of the project.'))
        self.applicationDiagramAct.setWhatsThis(self.tr(
            """<b>Application Diagram...</b>"""
            """<p>This shows a diagram of the project.</p>"""
        ))
        self.applicationDiagramAct.triggered.connect(
            self.handleApplicationDiagram)
        self.actions.append(self.applicationDiagramAct)

        self.loadDiagramAct = E5Action(
            self.tr('Load Diagram'),
            self.tr('&Load Diagram...'), 0, 0,
            self.graphicsGrp, 'project_load_diagram')
        self.loadDiagramAct.setStatusTip(
            self.tr('Load a diagram from file.'))
        self.loadDiagramAct.setWhatsThis(self.tr(
            """<b>Load Diagram...</b>"""
            """<p>This loads a diagram from file.</p>"""
        ))
        self.loadDiagramAct.triggered.connect(self.__loadDiagram)
        self.actions.append(self.loadDiagramAct)

        self.pluginGrp = createActionGroup(self)

        self.pluginPkgListAct = E5Action(
            self.tr('Create Package List'),
            UI.PixmapCache.getIcon("pluginArchiveList"),
            self.tr('Create &Package List'), 0, 0,
            self.pluginGrp, 'project_plugin_pkglist')
        self.pluginPkgListAct.setStatusTip(
            self.tr('Create an initial PKGLIST file for an eric plugin.'))
        self.pluginPkgListAct.setWhatsThis(self.tr(
            """<b>Create Package List</b>"""
            """<p>This creates an initial list of files to include in an"""
            """ eric plugin archive. The list is created from the project"""
            """ file.</p>"""
        ))
        self.pluginPkgListAct.triggered.connect(self.__pluginCreatePkgList)
        self.actions.append(self.pluginPkgListAct)

        self.pluginArchiveAct = E5Action(
            self.tr('Create Plugin Archives'),
            UI.PixmapCache.getIcon("pluginArchive"),
            self.tr('Create Plugin &Archives'), 0, 0,
            self.pluginGrp, 'project_plugin_archive')
        self.pluginArchiveAct.setStatusTip(
            self.tr('Create eric plugin archive files.'))
        self.pluginArchiveAct.setWhatsThis(self.tr(
            """<b>Create Plugin Archives</b>"""
            """<p>This creates eric plugin archive files using the list"""
            """ of files given in a PKGLIST* file. The archive name is"""
            """ built from the main script name if not designated in"""
            """ the package list file.</p>"""
        ))
        self.pluginArchiveAct.triggered.connect(self.__pluginCreateArchives)
        self.actions.append(self.pluginArchiveAct)
    
        self.pluginSArchiveAct = E5Action(
            self.tr('Create Plugin Archives (Snapshot)'),
            UI.PixmapCache.getIcon("pluginArchiveSnapshot"),
            self.tr('Create Plugin Archives (&Snapshot)'), 0, 0,
            self.pluginGrp, 'project_plugin_sarchive')
        self.pluginSArchiveAct.setStatusTip(self.tr(
            'Create eric plugin archive files (snapshot releases).'))
        self.pluginSArchiveAct.setWhatsThis(self.tr(
            """<b>Create Plugin Archives (Snapshot)</b>"""
            """<p>This creates eric plugin archive files using the list"""
            """ of files given in the PKGLIST* file. The archive name is"""
            """ built from the main script name if not designated in"""
            """ the package list file. The version entry of the main script"""
            """ is modified to reflect a snapshot release.</p>"""
        ))
        self.pluginSArchiveAct.triggered.connect(
            self.__pluginCreateSnapshotArchives)
        self.actions.append(self.pluginSArchiveAct)

        self.makeGrp = createActionGroup(self)

        self.makeExecuteAct = E5Action(
            self.tr('Execute Make'),
            self.tr('&Execute Make'), 0, 0,
            self.makeGrp, 'project_make_execute')
        self.makeExecuteAct.setStatusTip(
            self.tr("Perform a 'make' run."))
        self.makeExecuteAct.setWhatsThis(self.tr(
            """<b>Execute Make</b>"""
            """<p>This performs a 'make' run to rebuild the configured"""
            """ target.</p>"""
        ))
        self.makeExecuteAct.triggered.connect(self.__executeMake)
        self.actions.append(self.makeExecuteAct)

        self.makeTestAct = E5Action(
            self.tr('Test for Changes'),
            self.tr('&Test for Changes'), 0, 0,
            self.makeGrp, 'project_make_test')
        self.makeTestAct.setStatusTip(
            self.tr("Question 'make', if a rebuild is needed."))
        self.makeTestAct.setWhatsThis(self.tr(
            """<b>Test for Changes</b>"""
            """<p>This questions 'make', if a rebuild of the configured"""
            """ target is necessary.</p>"""
        ))
        self.makeTestAct.triggered.connect(
            lambda: self.__executeMake(questionOnly=True))
        self.actions.append(self.makeTestAct)

        self.closeAct.setEnabled(False)
        self.saveAct.setEnabled(False)
        self.saveasAct.setEnabled(False)
        self.actGrp2.setEnabled(False)
        self.propsAct.setEnabled(False)
        self.userPropsAct.setEnabled(False)
        self.filetypesAct.setEnabled(False)
        self.lexersAct.setEnabled(False)
        self.sessActGrp.setEnabled(False)
        self.dbgActGrp.setEnabled(False)
        self.pluginGrp.setEnabled(False)
        
    def initMenus(self):
        """
        Public slot to initialize the project menus.
        
        @return tuple of generated menus
        @rtype tuple of (QMenu, QMenu)
        """
        menu = QMenu(self.tr('&Project'), self.parent())
        self.recentMenu = QMenu(self.tr('Open &Recent Projects'), menu)
        self.sessionMenu = QMenu(self.tr('Session'), menu)
        self.debuggerMenu = QMenu(self.tr('Debugger'), menu)
        
        toolsMenu = QMenu(self.tr('Project-T&ools'), self.parent())
        self.vcsMenu = QMenu(self.tr('&Version Control'), toolsMenu)
        self.vcsMenu.setTearOffEnabled(True)
        self.vcsProjectHelper.initMenu(self.vcsMenu)
        self.vcsMenu.setEnabled(self.vcsSoftwareAvailable())
        self.checksMenu = QMenu(self.tr('Chec&k'), toolsMenu)
        self.checksMenu.setTearOffEnabled(True)
        self.menuShow = QMenu(self.tr('Sho&w'), toolsMenu)
        self.graphicsMenu = QMenu(self.tr('&Diagrams'), toolsMenu)
        self.packagersMenu = QMenu(self.tr('Pac&kagers'), toolsMenu)
        self.apidocMenu = QMenu(self.tr('Source &Documentation'), toolsMenu)
        self.apidocMenu.setTearOffEnabled(True)
        self.makeMenu = QMenu(self.tr('Make'), toolsMenu)
        
        self.__menus = {
            "Main": menu,
            "Recent": self.recentMenu,
            "VCS": self.vcsMenu,
            "Checks": self.checksMenu,
            "Show": self.menuShow,
            "Graphics": self.graphicsMenu,
            "Session": self.sessionMenu,
            "Apidoc": self.apidocMenu,
            "Debugger": self.debuggerMenu,
            "Packagers": self.packagersMenu,
            "Make": self.makeMenu,
        }
        
        # connect the aboutToShow signals
        self.recentMenu.aboutToShow.connect(self.__showContextMenuRecent)
        self.recentMenu.triggered.connect(self.__openRecent)
        self.vcsMenu.aboutToShow.connect(self.__showContextMenuVCS)
        self.checksMenu.aboutToShow.connect(self.__showContextMenuChecks)
        self.menuShow.aboutToShow.connect(self.__showContextMenuShow)
        self.graphicsMenu.aboutToShow.connect(self.__showContextMenuGraphics)
        self.apidocMenu.aboutToShow.connect(self.__showContextMenuApiDoc)
        self.packagersMenu.aboutToShow.connect(self.__showContextMenuPackagers)
        self.sessionMenu.aboutToShow.connect(self.__showContextMenuSession)
        self.debuggerMenu.aboutToShow.connect(self.__showContextMenuDebugger)
        self.makeMenu.aboutToShow.connect(self.__showContextMenuMake)
        menu.aboutToShow.connect(self.__showMenu)
        
        # build the show menu
        self.menuShow.setTearOffEnabled(True)
        self.menuShow.addAction(self.codeMetricsAct)
        self.menuShow.addAction(self.codeCoverageAct)
        self.menuShow.addAction(self.codeProfileAct)
        
        # build the diagrams menu
        self.graphicsMenu.setTearOffEnabled(True)
        self.graphicsMenu.addAction(self.applicationDiagramAct)
        self.graphicsMenu.addSeparator()
        self.graphicsMenu.addAction(self.loadDiagramAct)
        
        # build the session menu
        self.sessionMenu.setTearOffEnabled(True)
        self.sessionMenu.addActions(self.sessActGrp.actions())
        
        # build the debugger menu
        self.debuggerMenu.setTearOffEnabled(True)
        self.debuggerMenu.addActions(self.dbgActGrp.actions())
        
        # build the packagers menu
        self.packagersMenu.setTearOffEnabled(True)
        self.packagersMenu.addActions(self.pluginGrp.actions())
        self.packagersMenu.addSeparator()
        
        # build the make menu
        self.makeMenu.setTearOffEnabled(True)
        self.makeMenu.addActions(self.makeGrp.actions())
        self.makeMenu.addSeparator()
        
        # build the project main menu
        menu.setTearOffEnabled(True)
        menu.addActions(self.actGrp1.actions())
        self.menuRecentAct = menu.addMenu(self.recentMenu)
        menu.addSeparator()
        menu.addAction(self.closeAct)
        menu.addSeparator()
        menu.addAction(self.saveAct)
        menu.addAction(self.saveasAct)
        menu.addSeparator()
        menu.addActions(self.actGrp2.actions())
        menu.addSeparator()
        menu.addAction(self.propsAct)
        menu.addAction(self.userPropsAct)
        menu.addAction(self.filetypesAct)
        menu.addAction(self.lexersAct)
        menu.addSeparator()
        self.menuDebuggerAct = menu.addMenu(self.debuggerMenu)
        self.menuSessionAct = menu.addMenu(self.sessionMenu)
        
        # build the project tools menu
        toolsMenu.setTearOffEnabled(True)
        toolsMenu.addSeparator()
        self.menuMakeAct = toolsMenu.addMenu(self.makeMenu)
        toolsMenu.addSeparator()
        self.menuDiagramAct = toolsMenu.addMenu(self.graphicsMenu)
        toolsMenu.addSeparator()
        self.menuCheckAct = toolsMenu.addMenu(self.checksMenu)
        toolsMenu.addSeparator()
        toolsMenu.addMenu(self.vcsMenu)
        toolsMenu.addSeparator()
        self.menuShowAct = toolsMenu.addMenu(self.menuShow)
        toolsMenu.addSeparator()
        self.menuApidocAct = toolsMenu.addMenu(self.apidocMenu)
        toolsMenu.addSeparator()
        self.menuPackagersAct = toolsMenu.addMenu(self.packagersMenu)
        
        self.menuCheckAct.setEnabled(False)
        self.menuShowAct.setEnabled(False)
        self.menuDiagramAct.setEnabled(False)
        self.menuSessionAct.setEnabled(False)
        self.menuDebuggerAct.setEnabled(False)
        self.menuApidocAct.setEnabled(False)
        self.menuPackagersAct.setEnabled(False)
        self.menuMakeAct.setEnabled(False)
        
        self.__menu = menu
        self.__toolsMenu = toolsMenu
        
        return menu, toolsMenu
        
    def initToolbars(self, toolbarManager):
        """
        Public slot to initialize the project toolbar and the basic VCS
        toolbar.
        
        @param toolbarManager reference to a toolbar manager object
            (E5ToolBarManager)
        @return tuple of the generated toolbars (tuple of two QToolBar)
        """
        tb = QToolBar(self.tr("Project"), self.ui)
        tb.setIconSize(UI.Config.ToolBarIconSize)
        tb.setObjectName("ProjectToolbar")
        tb.setToolTip(self.tr('Project'))
        
        tb.addActions(self.actGrp1.actions())
        tb.addAction(self.closeAct)
        tb.addSeparator()
        tb.addAction(self.saveAct)
        tb.addAction(self.saveasAct)
        
        toolbarManager.addToolBar(tb, tb.windowTitle())
        toolbarManager.addAction(self.addFilesAct, tb.windowTitle())
        toolbarManager.addAction(self.addDirectoryAct, tb.windowTitle())
        toolbarManager.addAction(self.addLanguageAct, tb.windowTitle())
        toolbarManager.addAction(self.propsAct, tb.windowTitle())
        toolbarManager.addAction(self.userPropsAct, tb.windowTitle())
        
        import VCS
        vcstb = VCS.getBasicHelper(self).initBasicToolbar(
            self.ui, toolbarManager)
        
        return tb, vcstb
        
    def __showMenu(self):
        """
        Private method to set up the project menu.
        """
        self.menuRecentAct.setEnabled(len(self.recent) > 0)
        
        self.showMenu.emit("Main", self.__menus["Main"])
        
    def __syncRecent(self):
        """
        Private method to synchronize the list of recently opened projects
        with the central store.
        """
        for recent in self.recent[:]:
            if Utilities.samepath(self.pfile, recent):
                self.recent.remove(recent)
        self.recent.insert(0, self.pfile)
        maxRecent = Preferences.getProject("RecentNumber")
        if len(self.recent) > maxRecent:
            self.recent = self.recent[:maxRecent]
        self.__saveRecent()
        
    def __showContextMenuRecent(self):
        """
        Private method to set up the recent projects menu.
        """
        self.__loadRecent()
        
        self.recentMenu.clear()
        
        idx = 1
        for rp in self.recent:
            if idx < 10:
                formatStr = '&{0:d}. {1}'
            else:
                formatStr = '{0:d}. {1}'
            act = self.recentMenu.addAction(
                formatStr.format(
                    idx,
                    Utilities.compactPath(rp, self.ui.maxMenuFilePathLen)))
            act.setData(rp)
            act.setEnabled(QFileInfo(rp).exists())
            idx += 1
        
        self.recentMenu.addSeparator()
        self.recentMenu.addAction(self.tr('&Clear'), self.clearRecent)
        
    def __openRecent(self, act):
        """
        Private method to open a project from the list of rencently opened
        projects.
        
        @param act reference to the action that triggered (QAction)
        """
        file = act.data()
        if file:
            self.openProject(file)
        
    def clearRecent(self):
        """
        Public method to clear the recent projects menu.
        """
        self.recent = []
        self.__saveRecent()
    
    def clearHistories(self):
        """
        Public method to clear the project related histories.
        """
        self.clearRecent()
        
        for key in ["DebugClientsHistory", "DebuggerInterpreterHistory"]:
            Preferences.setProject(key, [])
        Preferences.syncPreferences()
    
    def __searchNewFiles(self):
        """
        Private slot used to handle the search new files action.
        """
        self.__doSearchNewFiles(False, True)
    
    def __searchProjectFile(self):
        """
        Private slot to show the Find Project File dialog.
        """
        if self.__findProjectFileDialog is None:
            from .QuickFindFileDialog import QuickFindFileDialog
            self.__findProjectFileDialog = QuickFindFileDialog(self)
            self.__findProjectFileDialog.sourceFile.connect(
                self.sourceFile)
            self.__findProjectFileDialog.designerFile.connect(
                self.designerFile)
            self.__findProjectFileDialog.linguistFile.connect(
                self.linguistFile)
        self.__findProjectFileDialog.show()
        self.__findProjectFileDialog.raise_()
        self.__findProjectFileDialog.activateWindow()
        
    def __doSearchNewFiles(self, AI=True, onUserDemand=False):
        """
        Private method to search for new files in the project directory.
        
        If new files were found, it shows a dialog listing these files and
        gives the user the opportunity to select the ones he wants to
        include. If 'Automatic Inclusion' is enabled, the new files are
        automatically added to the project.
        
        @param AI flag indicating whether the automatic inclusion should
                be honoured (boolean)
        @param onUserDemand flag indicating whether this method was
                requested by the user via a menu action (boolean)
        """
        autoInclude = Preferences.getProject("AutoIncludeNewFiles")
        recursiveSearch = Preferences.getProject("SearchNewFilesRecursively")
        newFiles = []
        
        ignore_patterns = [pattern for pattern, filetype in
                           self.pdata["FILETYPES"].items()
                           if filetype == '__IGNORE__']
        
        dirs = self.subdirs[:]
        for directory in dirs:
            skip = False
            for ignore_pattern in ignore_patterns:
                if fnmatch.fnmatch(directory, ignore_pattern):
                    skip = True
                    break
            if skip:
                continue
            
            curpath = os.path.join(self.ppath, directory)
            try:
                newSources = os.listdir(curpath)
            except OSError:
                newSources = []
            if self.pdata["TRANSLATIONPATTERN"]:
                pattern = (
                    self.pdata["TRANSLATIONPATTERN"]
                    .replace("%language%", "*")
                )
            else:
                pattern = "*.ts"
            binpattern = self.__binaryTranslationFile(pattern)
            for ns in newSources:
                # ignore hidden files and directories
                if ns.startswith('.'):
                    continue
                if (
                    Utilities.isWindowsPlatform() and
                    os.path.isdir(os.path.join(curpath, ns)) and
                    ns.startswith('_')
                ):
                    # dot net hack
                    continue
                
                # set fn to project relative name
                # then reset ns to fully qualified name for insertion,
                # possibly.
                if directory == "":
                    fn = ns
                else:
                    fn = os.path.join(directory, ns)
                ns = os.path.abspath(os.path.join(curpath, ns))
                
                # do not bother with dirs here...
                if os.path.isdir(ns):
                    if recursiveSearch:
                        d = self.getRelativePath(ns)
                        if d not in dirs:
                            dirs.append(d)
                    continue
                
                filetype = ""
                bfn = os.path.basename(fn)
                for pattern in reversed(
                        sorted(self.pdata["FILETYPES"].keys())):
                    if fnmatch.fnmatch(bfn, pattern):
                        filetype = self.pdata["FILETYPES"][pattern]
                        break
                
                if (
                    (filetype == "SOURCES" and
                     fn not in self.pdata["SOURCES"]) or
                    (filetype == "FORMS" and
                     fn not in self.pdata["FORMS"]) or
                    (filetype == "INTERFACES" and
                     fn not in self.pdata["INTERFACES"]) or
                    (filetype == "PROTOCOLS" and
                     fn not in self.pdata["PROTOCOLS"]) or
                    (filetype == "RESOURCES" and
                     fn not in self.pdata["RESOURCES"]) or
                    (filetype == "OTHERS" and
                     fn not in self.pdata["OTHERS"])
                ):
                    if autoInclude and AI:
                        self.appendFile(ns)
                    else:
                        newFiles.append(ns)
                elif (
                    filetype == "TRANSLATIONS" and
                    fn not in self.pdata["TRANSLATIONS"]
                ):
                    if (
                        fnmatch.fnmatch(ns, pattern) or
                        fnmatch.fnmatch(ns, binpattern)
                    ):
                        if autoInclude and AI:
                            self.appendFile(ns)
                        else:
                            newFiles.append(ns)
        
        # if autoInclude is set there is no more work left
        if (autoInclude and AI):
            return
        
        # if newfiles is empty, put up message box informing user nothing found
        if not newFiles:
            if onUserDemand:
                E5MessageBox.information(
                    self.ui,
                    self.tr("Search New Files"),
                    self.tr("There were no new files found to be added."))
            return
            
        # autoInclude is not set, show a dialog
        from .AddFoundFilesDialog import AddFoundFilesDialog
        dlg = AddFoundFilesDialog(newFiles, self.parent(), None)
        res = dlg.exec()
        
        # the 'Add All' button was pressed
        if res == 1:
            for file in newFiles:
                self.appendFile(file)
            
        # the 'Add Selected' button was pressed
        elif res == 2:
            files = dlg.getSelection()
            for file in files:
                self.appendFile(file)
        
    def othersAdded(self, fn, updateModel=True):
        """
        Public slot to be called, if something was added to the OTHERS project
        data area.
        
        @param fn filename or directory name added (string)
        @param updateModel flag indicating an update of the model is requested
            (boolean)
        """
        self.projectOthersAdded.emit(fn)
        updateModel and self.__model.addNewItem("OTHERS", fn)
        
    def getActions(self):
        """
        Public method to get a list of all actions.
        
        @return list of all actions (list of E5Action)
        """
        return self.actions[:]
        
    def addE5Actions(self, actions):
        """
        Public method to add actions to the list of actions.
        
        @param actions list of actions (list of E5Action)
        """
        self.actions.extend(actions)
        
    def removeE5Actions(self, actions):
        """
        Public method to remove actions from the list of actions.
        
        @param actions list of actions (list of E5Action)
        """
        for act in actions:
            try:
                self.actions.remove(act)
            except ValueError:
                pass
        
    def getMenu(self, menuName):
        """
        Public method to get a reference to the main menu or a submenu.
        
        @param menuName name of the menu (string)
        @return reference to the requested menu (QMenu) or None
        """
        try:
            return self.__menus[menuName]
        except KeyError:
            return None
        
    def repopulateItem(self, fullname):
        """
        Public slot to repopulate a named item.
        
        @param fullname full name of the item to repopulate (string)
        """
        if not self.isOpen():
            return
        
        with E5OverrideCursor():
            name = self.getRelativePath(fullname)
            self.prepareRepopulateItem.emit(name)
            self.__model.repopulateItem(name)
            self.completeRepopulateItem.emit(name)
    
    ##############################################################
    ## Below is the VCS interface
    ##############################################################
    
    def initVCS(self, vcsSystem=None, nooverride=False):
        """
        Public method used to instantiate a vcs system.
        
        @param vcsSystem type of VCS to be used (string)
        @param nooverride flag indicating to ignore an override request
            (boolean)
        @return a reference to the vcs object
        """
        vcs = None
        forProject = True
        override = False
        
        if vcsSystem is None:
            if self.pdata["VCS"] and self.pdata["VCS"] != 'None':
                vcsSystem = self.pdata["VCS"]
        else:
            forProject = False
        
        if forProject and self.pdata["VCS"] and self.pdata["VCS"] != 'None':
            if (
                self.pudata["VCSOVERRIDE"] and
                not nooverride
            ):
                vcsSystem = self.pudata["VCSOVERRIDE"]
                override = True
        
        if vcsSystem is not None:
            import VCS
            try:
                vcs = VCS.factory(vcsSystem)
            except ImportError:
                if override:
                    # override failed, revert to original
                    self.pudata["VCSOVERRIDE"] = ""
                    return self.initVCS(nooverride=True)
        
        if vcs:
            vcsExists, msg = vcs.vcsExists()
            if not vcsExists:
                if override:
                    # override failed, revert to original
                    with E5OverridenCursor():
                        E5MessageBox.critical(
                            self.ui,
                            self.tr("Version Control System"),
                            self.tr(
                                "<p>The selected VCS <b>{0}</b> could not be"
                                " found. <br/>Reverting override.</p><p>{1}"
                                "</p>")
                            .format(vcsSystem, msg))
                        self.pudata["VCSOVERRIDE"] = ""
                    return self.initVCS(nooverride=True)
                
                with E5OverridenCursor():
                    E5MessageBox.critical(
                        self.ui,
                        self.tr("Version Control System"),
                        self.tr(
                            "<p>The selected VCS <b>{0}</b> could not be"
                            " found.<br/>Disabling version control.</p>"
                            "<p>{1}</p>").format(vcsSystem, msg))
                vcs = None
                if forProject:
                    self.pdata["VCS"] = 'None'
                    self.setDirty(True)
            else:
                vcs.vcsInitConfig(self)
        
        if vcs and forProject:
            # set the vcs options
            if vcs.vcsSupportCommandOptions():
                try:
                    vcsopt = copy.deepcopy(self.pdata["VCSOPTIONS"])
                    vcs.vcsSetOptions(vcsopt)
                except LookupError:
                    pass
            # set vcs specific data
            try:
                vcsother = copy.deepcopy(self.pdata["VCSOTHERDATA"])
                vcs.vcsSetOtherData(vcsother)
            except LookupError:
                pass
        
        if forProject:
            if vcs is None:
                import VCS
                self.vcsProjectHelper = VCS.getBasicHelper(self)
                self.vcsBasicHelper = True
            else:
                self.vcsProjectHelper = vcs.vcsGetProjectHelper(self)
                self.vcsBasicHelper = False
            if self.vcsMenu is not None:
                self.vcsProjectHelper.initMenu(self.vcsMenu)
                self.vcsMenu.setEnabled(self.vcsSoftwareAvailable())
        
        return vcs
    
    def resetVCS(self):
        """
        Public method to reset the VCS.
        """
        self.pdata["VCS"] = 'None'
        self.vcs = self.initVCS()
        e5App().getObject("PluginManager").deactivateVcsPlugins()
    
    def __showContextMenuVCS(self):
        """
        Private slot called before the vcs menu is shown.
        """
        self.vcsProjectHelper.showMenu()
        if self.vcsBasicHelper:
            self.showMenu.emit("VCS", self.vcsMenu)
    
    def vcsSoftwareAvailable(self):
        """
        Public method to check, if some supported VCS software is available
        to the IDE.
        
        @return flag indicating availability of VCS software (boolean)
        """
        vcsSystemsDict = (
            e5App().getObject("PluginManager")
            .getPluginDisplayStrings("version_control")
        )
        return len(vcsSystemsDict) != 0
    
    def __vcsStatusChanged(self):
        """
        Private slot to handle a change of the overall VCS status.
        """
        self.projectChanged.emit()
    
    #########################################################################
    ## Below is the interface to the checker tools
    #########################################################################
    
    def __showContextMenuChecks(self):
        """
        Private slot called before the checks menu is shown.
        """
        self.showMenu.emit("Checks", self.checksMenu)
    
    #########################################################################
    ## Below is the interface to the packagers tools
    #########################################################################
    
    def __showContextMenuPackagers(self):
        """
        Private slot called before the packagers menu is shown.
        """
        self.showMenu.emit("Packagers", self.packagersMenu)
    
    #########################################################################
    ## Below is the interface to the apidoc tools
    #########################################################################
    
    def __showContextMenuApiDoc(self):
        """
        Private slot called before the apidoc menu is shown.
        """
        self.showMenu.emit("Apidoc", self.apidocMenu)
    
    #########################################################################
    ## Below is the interface to the show tools
    #########################################################################
    
    def __showCodeMetrics(self):
        """
        Private slot used to calculate some code metrics for the project files.
        """
        files = [os.path.join(self.ppath, file)
                 for file in self.pdata["SOURCES"] if file.endswith(".py")]
        from DataViews.CodeMetricsDialog import CodeMetricsDialog
        self.codemetrics = CodeMetricsDialog()
        self.codemetrics.show()
        self.codemetrics.prepare(files, self)

    def __showCodeCoverage(self):
        """
        Private slot used to show the code coverage information for the
        project files.
        """
        fn = self.getMainScript(True)
        if fn is None:
            E5MessageBox.critical(
                self.ui,
                self.tr("Coverage Data"),
                self.tr(
                    "There is no main script defined for the"
                    " current project. Aborting"))
            return
        
        tfn = Utilities.getTestFileName(fn)
        basename = os.path.splitext(fn)[0]
        tbasename = os.path.splitext(tfn)[0]
        
        # determine name of coverage file to be used
        files = []
        f = "{0}.coverage".format(basename)
        tf = "{0}.coverage".format(tbasename)
        if os.path.isfile(f):
            files.append(f)
        if os.path.isfile(tf):
            files.append(tf)
        
        if files:
            if len(files) > 1:
                fn, ok = QInputDialog.getItem(
                    None,
                    self.tr("Code Coverage"),
                    self.tr("Please select a coverage file"),
                    files,
                    0, False)
                if not ok:
                    return
            else:
                fn = files[0]
        else:
            return
        
        files = [os.path.join(self.ppath, file)
                 for file in self.pdata["SOURCES"]
                 if os.path.splitext(file)[1].startswith(".py")]
        from DataViews.PyCoverageDialog import PyCoverageDialog
        self.codecoverage = PyCoverageDialog()
        self.codecoverage.show()
        self.codecoverage.start(fn, files)

    def __showProfileData(self):
        """
        Private slot used to show the profiling information for the project.
        """
        fn = self.getMainScript(True)
        if fn is None:
            E5MessageBox.critical(
                self.ui,
                self.tr("Profile Data"),
                self.tr(
                    "There is no main script defined for the"
                    " current project. Aborting"))
            return
        
        tfn = Utilities.getTestFileName(fn)
        basename = os.path.splitext(fn)[0]
        tbasename = os.path.splitext(tfn)[0]
        
        # determine name of profile file to be used
        files = []
        f = "{0}.profile".format(basename)
        tf = "{0}.profile".format(tbasename)
        if os.path.isfile(f):
            files.append(f)
        if os.path.isfile(tf):
            files.append(tf)
        
        if files:
            if len(files) > 1:
                fn, ok = QInputDialog.getItem(
                    None,
                    self.tr("Profile Data"),
                    self.tr("Please select a profile file"),
                    files,
                    0, False)
                if not ok:
                    return
            else:
                fn = files[0]
        else:
            return
        
        from DataViews.PyProfileDialog import PyProfileDialog
        self.profiledata = PyProfileDialog()
        self.profiledata.show()
        self.profiledata.start(fn)
        
    def __showContextMenuShow(self):
        """
        Private slot called before the show menu is shown.
        """
        fn = self.getMainScript(True)
        if fn is not None:
            tfn = Utilities.getTestFileName(fn)
            basename = os.path.splitext(fn)[0]
            tbasename = os.path.splitext(tfn)[0]
            self.codeProfileAct.setEnabled(
                os.path.isfile("{0}.profile".format(basename)) or
                os.path.isfile("{0}.profile".format(tbasename)))
            self.codeCoverageAct.setEnabled(
                self.isPy3Project() and
                (os.path.isfile("{0}.coverage".format(basename)) or
                 os.path.isfile("{0}.coverage".format(tbasename))))
        else:
            self.codeProfileAct.setEnabled(False)
            self.codeCoverageAct.setEnabled(False)
        
        self.showMenu.emit("Show", self.menuShow)
    
    #########################################################################
    ## Below is the interface to the diagrams
    #########################################################################
    
    def __showContextMenuGraphics(self):
        """
        Private slot called before the graphics menu is shown.
        """
        self.showMenu.emit("Graphics", self.graphicsMenu)
    
    def handleApplicationDiagram(self):
        """
        Public method to handle the application diagram context menu action.
        """
        res = E5MessageBox.yesNo(
            self.ui,
            self.tr("Application Diagram"),
            self.tr("""Include module names?"""),
            yesDefault=True)
        
        from Graphics.UMLDialog import UMLDialog
        self.applicationDiagram = UMLDialog(UMLDialog.ApplicationDiagram, self,
                                            self.parent(), noModules=not res)
        self.applicationDiagram.show()
    
    def __loadDiagram(self):
        """
        Private slot to load a diagram from file.
        """
        from Graphics.UMLDialog import UMLDialog
        self.loadedDiagram = None
        loadedDiagram = UMLDialog(UMLDialog.NoDiagram,
                                  self, parent=self.parent())
        if loadedDiagram.load():
            self.loadedDiagram = loadedDiagram
            self.loadedDiagram.show(fromFile=True)
    
    #########################################################################
    ## Below is the interface to the VCS monitor thread
    #########################################################################
    
    def __statusMonitorStatus(self, status, statusMsg):
        """
        Private method to receive the status monitor status.
        
        It simply reemits the received status.
        
        @param status status of the monitoring thread (string, ok, nok or off)
        @param statusMsg explanotory text for the signaled status (string)
        """
        self.vcsStatusMonitorStatus.emit(status, statusMsg)
        
    def setStatusMonitorInterval(self, interval):
        """
        Public method to se the interval of the VCS status monitor thread.
        
        @param interval status monitor interval in seconds (integer)
        """
        if self.vcs is not None:
            self.vcs.setStatusMonitorInterval(interval, self)
        
    def getStatusMonitorInterval(self):
        """
        Public method to get the monitor interval.
        
        @return interval in seconds (integer)
        """
        if self.vcs is not None:
            return self.vcs.getStatusMonitorInterval()
        else:
            return 0
        
    def setStatusMonitorAutoUpdate(self, auto):
        """
        Public method to enable the auto update function.
        
        @param auto status of the auto update function (boolean)
        """
        if self.vcs is not None:
            self.vcs.setStatusMonitorAutoUpdate(auto)
        
    def getStatusMonitorAutoUpdate(self):
        """
        Public method to retrieve the status of the auto update function.
        
        @return status of the auto update function (boolean)
        """
        if self.vcs is not None:
            return self.vcs.getStatusMonitorAutoUpdate()
        else:
            return False
        
    def checkVCSStatus(self):
        """
        Public method to wake up the VCS status monitor thread.
        """
        if self.vcs is not None:
            self.vcs.checkVCSStatus()
        
    def clearStatusMonitorCachedState(self, name):
        """
        Public method to clear the cached VCS state of a file/directory.
        
        @param name name of the entry to be cleared (string)
        """
        if self.vcs is not None:
            self.vcs.clearStatusMonitorCachedState(name)
        
    def startStatusMonitor(self):
        """
        Public method to start the VCS status monitor thread.
        """
        if self.vcs is not None:
            self.vcs.startStatusMonitor(self)
        
    def stopStatusMonitor(self):
        """
        Public method to stop the VCS status monitor thread.
        """
        if self.vcs is not None:
            self.vcs.stopStatusMonitor()
    
    #########################################################################
    ## Below are the plugin development related methods
    #########################################################################
    
    def __pluginVersionToTuple(self, versionStr):
        """
        Private method to convert a plug-in version string into a version
        tuple.
        
        @param versionStr version string to be converted
        @type str
        @return version info as a tuple
        @rtype tuple of int and str
        """
        vParts = []
        if "-" in versionStr:
            versionStr, additional = versionStr.split("-", 1)
        else:
            additional = ""
        for part in versionStr.split("."):
            try:
                vParts.append(int(part))
            except ValueError:
                vParts.append(part)
        
        if additional:
            vParts.append(additional)
        
        return tuple(vParts)
    
    def __pluginCreatePkgList(self):
        """
        Private slot to create a PKGLIST file needed for archive file creation.
        """
        pkglist = os.path.join(self.ppath, "PKGLIST")
        if os.path.exists(pkglist):
            res = E5MessageBox.yesNo(
                self.ui,
                self.tr("Create Package List"),
                self.tr(
                    "<p>The file <b>PKGLIST</b> already"
                    " exists.</p><p>Overwrite it?</p>"),
                icon=E5MessageBox.Warning)
            if not res:
                return  # don't overwrite
        
        # build the list of entries
        lst_ = []
        for key in ["SOURCES", "FORMS", "RESOURCES", "TRANSLATIONS",
                    "INTERFACES", "PROTOCOLS", "OTHERS"]:
            lst_.extend(self.pdata[key])
        lst = []
        for entry in lst_:
            if os.path.isdir(self.getAbsolutePath(entry)):
                lst.extend(
                    [self.getRelativePath(p) for p in
                     Utilities.direntries(self.getAbsolutePath(entry), True)])
                continue
            else:
                lst.append(entry)
        lst.sort()
        if "PKGLIST" in lst:
            lst.remove("PKGLIST")
        
        # build the header to indicate a freshly generated list
        header = [
            ";",
            "; initial_list (REMOVE THIS LINE WHEN DONE)",
            ";",
            " ",
        ]
        
        # write the file
        try:
            if self.pdata["EOL"] == 0:
                newline = None
            else:
                newline = self.getEolString()
            with open(pkglist, "w", encoding="utf-8",
                      newline=newline) as pkglistFile:
                pkglistFile.write("\n".join(header) + "\n")
                pkglistFile.write(
                    "\n".join([Utilities.fromNativeSeparators(f)
                               for f in lst]))
                pkglistFile.write("\n")
                # ensure the file ends with an empty line
        except OSError as why:
            E5MessageBox.critical(
                self.ui,
                self.tr("Create Package List"),
                self.tr(
                    """<p>The file <b>PKGLIST</b> could not be created.</p>"""
                    """<p>Reason: {0}</p>""").format(str(why)))
            return
        
        if "PKGLIST" not in self.pdata["OTHERS"]:
            self.appendFile("PKGLIST")
        
    @pyqtSlot()
    def __pluginCreateArchives(self, snapshot=False):
        """
        Private slot to create eric plugin archives.
        
        @param snapshot flag indicating snapshot archives (boolean)
        """
        if not self.pdata["MAINSCRIPT"]:
            E5MessageBox.critical(
                self.ui,
                self.tr("Create Plugin Archive"),
                self.tr(
                    """The project does not have a main script defined. """
                    """Aborting..."""))
            return
        
        selectedLists = []
        pkglists = [os.path.basename(f) for f in
                    glob.glob(os.path.join(self.ppath, "PKGLIST*"))]
        if len(pkglists) == 1:
            selectedLists = [os.path.join(self.ppath, pkglists[0])]
        elif len(pkglists) > 1:
            dlg = E5ListSelectionDialog(
                sorted(pkglists), title=self.tr("Create Plugin Archive"),
                message=self.tr("Select package lists:"),
                checkBoxSelection=True)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                selectedLists = [os.path.join(self.ppath, s)
                                 for s in dlg.getSelection()]
            else:
                return
        
        if not selectedLists:
            E5MessageBox.critical(
                self.ui,
                self.tr("Create Plugin Archive"),
                self.tr("""<p>No package list files (PKGLIST*) available or"""
                        """ selected. Aborting...</p>"""))
            return
        
        progress = E5ProgressDialog(
            self.tr("Creating plugin archives..."), self.tr("Abort"),
            0, len(selectedLists), self.tr("%v/%m Archives"))
        progress.setMinimumDuration(0)
        progress.setWindowTitle(self.tr("Create Plugin Archives"))
        count = 0
        errors = 0
        for pkglist in selectedLists:
            progress.setValue(count)
            if progress.wasCanceled():
                break
            
            try:
                with open(pkglist, "r", encoding="utf-8") as pkglistFile:
                    names = pkglistFile.read()
            except OSError as why:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Create Plugin Archive"),
                    self.tr(
                        """<p>The file <b>{0}</b> could not be read.</p>"""
                        """<p>Reason: {1}</p>""").format(
                        os.path.basename(pkglist), str(why)))
                errors += 1
                count += 1
                continue
            
            lines = names.splitlines()
            archiveName = ""
            archiveVersion = ""
            names = []
            listOK = True
            for line in lines:
                if line.startswith(";"):
                    line = line[1:].strip()
                    # it's a comment possibly containing a directive
                    # supported directives are:
                    # - archive_name= defines the name of the archive
                    # - archive_version= defines the version of the archive
                    if line.startswith("archive_name="):
                        archiveName = line.split("=")[1]
                    elif line.startswith("archive_version="):
                        archiveVersion = line.split("=")[1]
                    elif line.startswith("initial_list "):
                        E5MessageBox.critical(
                            self.ui,
                            self.tr("Create Plugin Archive"),
                            self.tr(
                                """<p>The file <b>{0}</b> is not ready yet."""
                                """</p><p>Please rework it and delete the"""
                                """'; initial_list' line of the header."""
                                """</p>""").format(os.path.basename(pkglist)))
                        errors += 1
                        count += 1
                        listOK = False
                        break
                elif line.strip():
                    names.append(line.strip())
            
            if not listOK:
                continue
            
            names = sorted(names)
            if archiveName:
                archive = os.path.join(self.ppath, archiveName)
            else:
                archive = os.path.join(
                    self.ppath,
                    self.pdata["MAINSCRIPT"].replace(".py", ".zip"))
            try:
                archiveFile = zipfile.ZipFile(archive, "w")
            except OSError as why:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Create Plugin Archive"),
                    self.tr(
                        """<p>The eric plugin archive file <b>{0}</b>"""
                        """ could not be created.</p>"""
                        """<p>Reason: {1}</p>""").format(archive, str(why)))
                errors += 1
                count += 1
                continue
            
            for name in names:
                if name:
                    try:
                        self.__createZipDirEntries(
                            os.path.split(name)[0], archiveFile)
                        if snapshot and name == self.pdata["MAINSCRIPT"]:
                            snapshotSource, version = (
                                self.__createSnapshotSource(
                                    os.path.join(self.ppath,
                                                 self.pdata["MAINSCRIPT"]))
                            )
                            archiveFile.writestr(name, snapshotSource)
                        else:
                            archiveFile.write(os.path.join(self.ppath, name),
                                              name)
                            if name == self.pdata["MAINSCRIPT"]:
                                version = self.__pluginExtractVersion(
                                    os.path.join(self.ppath,
                                                 self.pdata["MAINSCRIPT"]))
                                if archiveVersion and (
                                    self.__pluginVersionToTuple(version) <
                                    self.__pluginVersionToTuple(archiveVersion)
                                ):
                                    version = archiveVersion
                    except OSError as why:
                        E5MessageBox.critical(
                            self.ui,
                            self.tr("Create Plugin Archive"),
                            self.tr(
                                """<p>The file <b>{0}</b> could not be"""
                                """ stored in the archive. Ignoring it.</p>"""
                                """<p>Reason: {1}</p>""")
                            .format(os.path.join(self.ppath, name), str(why)))
            archiveFile.writestr("VERSION", version.encode("utf-8"))
            archiveFile.close()
            
            if archive not in self.pdata["OTHERS"]:
                self.appendFile(archive)
            
            count += 1
        
        progress.setValue(len(selectedLists))
        
        if errors:
            self.ui.showNotification(
                UI.PixmapCache.getPixmap("pluginArchive48"),
                self.tr("Create Plugin Archive"),
                self.tr("<p>The eric plugin archive files were "
                        "created with some errors.</p>"),
                kind=NotificationTypes.Critical,
                timeout=0)
        else:
            self.ui.showNotification(
                UI.PixmapCache.getPixmap("pluginArchive48"),
                self.tr("Create Plugin Archive"),
                self.tr("<p>The eric plugin archive files were "
                        "created successfully.</p>"))
    
    def __pluginCreateSnapshotArchives(self):
        """
        Private slot to create eric plugin archive snapshot releases.
        """
        self.__pluginCreateArchives(True)
    
    def __createZipDirEntries(self, path, zipFile):
        """
        Private method to create dir entries in the zip file.
        
        @param path name of the directory entry to create (string)
        @param zipFile open ZipFile object (zipfile.ZipFile)
        """
        if path == "" or path == "/" or path == "\\":
            return
        
        if not path.endswith("/") and not path.endswith("\\"):
            path = "{0}/".format(path)
        
        if path not in zipFile.namelist():
            self.__createZipDirEntries(os.path.split(path[:-1])[0], zipFile)
            zipFile.writestr(path, b"")
    
    def __createSnapshotSource(self, filename):
        """
        Private method to create a snapshot plugin version.
        
        The version entry in the plugin module is modified to signify
        a snapshot version. This method appends the string "-snapshot-"
        and date indicator to the version string.
        
        @param filename name of the plugin file to modify (string)
        @return modified source (bytes), snapshot version string (string)
        """
        try:
            sourcelines, encoding = Utilities.readEncodedFile(filename)
            sourcelines = sourcelines.splitlines(True)
        except (OSError, UnicodeError) as why:
            E5MessageBox.critical(
                self.ui,
                self.tr("Create Plugin Archive"),
                self.tr("""<p>The plugin file <b>{0}</b> could """
                        """not be read.</p>"""
                        """<p>Reason: {1}</p>""")
                .format(filename, str(why)))
            return b"", ""
        
        lineno = 0
        while lineno < len(sourcelines):
            if sourcelines[lineno].startswith("version = "):
                # found the line to modify
                datestr = time.strftime("%Y%m%d")
                lineend = sourcelines[lineno].replace(
                    sourcelines[lineno].rstrip(), "")
                sversion = "{0}-snapshot-{1}".format(
                    sourcelines[lineno].replace("version = ", "")
                    .strip()[1:-1],
                    datestr)
                sourcelines[lineno] = '{0} + "-snapshot-{1}"{2}'.format(
                    sourcelines[lineno].rstrip(), datestr, lineend)
                break
            
            lineno += 1
        
        source = Utilities.encode("".join(sourcelines), encoding)[0]
        return source, sversion
    
    def __pluginExtractVersion(self, filename):
        """
        Private method to extract the version number entry.
        
        @param filename name of the plugin file (string)
        @return version string (string)
        """
        version = "0.0.0"
        try:
            sourcelines = Utilities.readEncodedFile(filename)[0]
            sourcelines = sourcelines.splitlines(True)
        except (OSError, UnicodeError) as why:
            E5MessageBox.critical(
                self.ui,
                self.tr("Create Plugin Archive"),
                self.tr(
                    """<p>The plugin file <b>{0}</b> could """
                    """not be read.</p> <p>Reason: {1}</p>""")
                .format(filename, str(why)))
            return ""
        
        for sourceline in sourcelines:
            if sourceline.startswith("version = "):
                version = (
                    sourceline.replace("version = ", "").strip()
                    .replace('"', "").replace("'", "")
                )
                break
        
        return version
    
    #########################################################################
    ## Below are methods implementing the 'make' support
    #########################################################################
    
    def __showContextMenuMake(self):
        """
        Private slot called before the make menu is shown.
        """
        self.showMenu.emit("Make", self.makeMenu)
    
    def hasDefaultMakeParameters(self):
        """
        Public method to test, if the project contains the default make
        parameters.
        
        @return flag indicating default parameter set
        @rtype bool
        """
        return self.pdata["MAKEPARAMS"] == {
            "MakeEnabled": False,
            "MakeExecutable": "",
            "MakeFile": "",
            "MakeTarget": "",
            "MakeParameters": "",
            "MakeTestOnly": True,
        }
    
    def isMakeEnabled(self):
        """
        Public method to test, if make is enabled for the project.
        
        @return flag indicating enabled make support
        @rtype bool
        """
        return self.pdata["MAKEPARAMS"]["MakeEnabled"]
    
    @pyqtSlot()
    def executeMake(self):
        """
        Public slot to execute a project specific make run (auto-run)
        (execute or question).
        """
        self.__executeMake(
            questionOnly=self.pdata["MAKEPARAMS"]["MakeTestOnly"],
            interactive=False)
    
    @pyqtSlot()
    def __executeMake(self, questionOnly=False, interactive=True):
        """
        Private method to execute a project specific make run.
        
        @param questionOnly flag indicating to ask make for changes only
        @type bool
        @param interactive flag indicating an interactive invocation (i.e.
            through a menu action)
        @type bool
        """
        if (
            not self.pdata["MAKEPARAMS"]["MakeEnabled"] or
            self.__makeProcess is not None
        ):
            return
        
        if self.pdata["MAKEPARAMS"]["MakeExecutable"]:
            prog = self.pdata["MAKEPARAMS"]["MakeExecutable"]
        else:
            prog = Project.DefaultMake
        
        args = []
        if self.pdata["MAKEPARAMS"]["MakeParameters"]:
            args.extend(Utilities.parseOptionString(
                self.pdata["MAKEPARAMS"]["MakeParameters"]))
        
        if self.pdata["MAKEPARAMS"]["MakeFile"]:
            args.append("--makefile={0}".format(
                self.pdata["MAKEPARAMS"]["MakeFile"]))
        
        if questionOnly:
            args.append("--question")
        
        if self.pdata["MAKEPARAMS"]["MakeTarget"]:
            args.append(self.pdata["MAKEPARAMS"]["MakeTarget"])
        
        self.__makeProcess = QProcess(self)
        self.__makeProcess.readyReadStandardOutput.connect(
            self.__makeReadStdOut)
        self.__makeProcess.readyReadStandardError.connect(
            self.__makeReadStdErr)
        self.__makeProcess.finished.connect(
            lambda exitCode, exitStatus: self.__makeFinished(
                exitCode, exitStatus, questionOnly, interactive))
        self.__makeProcess.setWorkingDirectory(self.getProjectPath())
        self.__makeProcess.start(prog, args)
        
        if not self.__makeProcess.waitForStarted():
            E5MessageBox.critical(
                self.ui,
                self.tr("Execute Make"),
                self.tr("""The make process did not start."""))
            
            self.__cleanupMake()
    
    @pyqtSlot()
    def __makeReadStdOut(self):
        """
        Private slot to process process output received via stdout.
        """
        if self.__makeProcess is not None:
            output = str(self.__makeProcess.readAllStandardOutput(),
                         Preferences.getSystem("IOEncoding"),
                         'replace')
            self.appendStdout.emit(output)
    
    @pyqtSlot()
    def __makeReadStdErr(self):
        """
        Private slot to process process output received via stderr.
        """
        if self.__makeProcess is not None:
            error = str(self.__makeProcess.readAllStandardError(),
                        Preferences.getSystem("IOEncoding"),
                        'replace')
            self.appendStderr.emit(error)
    
    def __makeFinished(self, exitCode, exitStatus, questionOnly,
                       interactive=True):
        """
        Private slot handling the make process finished signal.
        
        @param exitCode exit code of the make process
        @type int
        @param exitStatus exit status of the make process
        @type QProcess.ExitStatus
        @param questionOnly flag indicating a test only run
        @type bool
        @param interactive flag indicating an interactive invocation (i.e.
            through a menu action)
        @type bool
        """
        if exitStatus == QProcess.ExitStatus.CrashExit:
            E5MessageBox.critical(
                self.ui,
                self.tr("Execute Make"),
                self.tr("""The make process crashed."""))
        else:
            if questionOnly and exitCode == 1:
                # a rebuild is needed
                title = self.tr("Test for Changes")
                
                if self.pdata["MAKEPARAMS"]["MakeTarget"]:
                    message = self.tr(
                        """<p>There are changes that require the configured"""
                        """ make target <b>{0}</b> to be rebuilt.</p>"""
                    ).format(self.pdata["MAKEPARAMS"]["MakeTarget"])
                else:
                    message = self.tr(
                        """<p>There are changes that require the default"""
                        """ make target to be rebuilt.</p>""")
                
                self.ui.showNotification(
                    UI.PixmapCache.getPixmap("makefile48"),
                    title,
                    message,
                    kind=NotificationTypes.Warning,
                    timeout=0)
            elif exitCode > 1:
                E5MessageBox.critical(
                    self.ui,
                    self.tr("Execute Make"),
                    self.tr("""The makefile contains errors."""))
        
        self.__cleanupMake()
    
    def __cleanupMake(self):
        """
        Private method to clean up make related stuff.
        """
        self.__makeProcess.readyReadStandardOutput.disconnect()
        self.__makeProcess.readyReadStandardError.disconnect()
        self.__makeProcess.finished.disconnect()
        self.__makeProcess.deleteLater()
        self.__makeProcess = None
    
    #########################################################################
    ## Below are methods implementing some 'IDL' support functions
    #########################################################################
    
    def hasDefaultIdlCompilerParameters(self):
        """
        Public method to test, if the project contains the default IDL compiler
        parameters.
        
        @return flag indicating default parameter set
        @rtype bool
        """
        return self.pdata["IDLPARAMS"] == {
            "IncludeDirs": [],
            "DefinedNames": [],
            "UndefinedNames": [],
        }
    
    #########################################################################
    ## Below are methods implementing some 'UIC' support functions
    #########################################################################
    
    def hasDefaultUicCompilerParameters(self):
        """
        Public method to test, if the project contains the default uic compiler
        parameters.
        
        @return flag indicating default parameter set
        @rtype bool
        """
        return self.pdata["UICPARAMS"] == {
            "Package": "",
            "RcSuffix": "",
            "PackagesRoot": "",
        }
    
    def getUicParameter(self, name):
        """
        Public method to get a named uic related parameter.
        
        @param name name of the parameter
        @type str
        @return value of the given parameter
        @rtype any, None in case on non-existence
        """
        if name in self.pdata["UICPARAMS"]:
            return self.pdata["UICPARAMS"][name]
        else:
            return None
    
    #########################################################################
    ## Below are methods implementing some 'RCC' support functions
    #########################################################################
    
    def hasDefaultRccCompilerParameters(self):
        """
        Public method to test, if the project contains the default rcc compiler
        parameters.
        
        @return flag indicating default parameter set
        @rtype bool
        """
        return (
            self.pdata["RCCPARAMS"] == self.getDefaultRccCompilerParameters()
        )
    
    def getDefaultRccCompilerParameters(self):
        """
        Public method to get the default rcc compiler parameters.
        
        @return dictionary containing the default rcc compiler parameters
        @rtype dict
        """
        return {
            "CompressionThreshold": 70,     # default value
            "CompressLevel": 0,             # use zlib default
            "CompressionDisable": False,
            "PathPrefix": "",
        }
    
    #########################################################################
    ## Below are methods implementing some 'docstring' support functions
    #########################################################################
    
    def hasDefaultDocstringParameter(self):
        """
        Public method to test, if the project contains the default docstring
        parameter.
        
        @return flag indicating default parameter
        @rtype bool
        """
        return self.pdata["DOCSTRING"] == ""
    
    def getDocstringType(self):
        """
        Public method to get the configured docstring style.
        
        @return configured docstring style
        @rtype str
        """
        return self.pdata["DOCSTRING"]

#
# eflag: noqa = M601
