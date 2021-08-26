# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class to manage Python virtual environments.
"""

import os
import sys
import shutil
import json
import copy

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog

from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App

import Preferences


class VirtualenvManager(QObject):
    """
    Class implementing an object to manage Python virtual environments.
    
    @signal virtualEnvironmentAdded() emitted to indicate the addition of
        a virtual environment
    @signal virtualEnvironmentRemoved() emitted to indicate the removal and
        deletion of a virtual environment
    @signal virtualEnvironmentChanged(name) emitted to indicate a change of
        a virtual environment
    """
    DefaultKey = "<default>"
    
    virtualEnvironmentAdded = pyqtSignal()
    virtualEnvironmentRemoved = pyqtSignal()
    virtualEnvironmentChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent object
        @type QWidget
        """
        super(VirtualenvManager, self).__init__(parent)
        
        self.__ui = parent
        
        self.__loadSettings()
        
        self.__virtualenvManagerDialog = None
    
    def __loadSettings(self):
        """
        Private slot to load the virtual environments.
        """
        self.__virtualEnvironmentsBaseDir = Preferences.Prefs.settings.value(
            "PyVenv/VirtualEnvironmentsBaseDir", "")
        
        venvString = Preferences.Prefs.settings.value(
            "PyVenv/VirtualEnvironments", "{}")     # __IGNORE_WARNING_M613__
        environments = json.loads(venvString)
        
        self.__virtualEnvironments = {}
        # each environment entry is a dictionary:
        #   path:           the directory of the virtual environment
        #                   (empty for a global environment)
        #   interpreter:    the path of the Python interpreter
        #   variant:        Python variant (always 3)
        #   is_global:      a flag indicating a global environment
        #   is_conda:       a flag indicating an Anaconda environment
        #   is_remote:      a flag indicating a remotely accessed environment
        #   exec_path:      a string to be prefixed to the PATH environment
        #                   setting
        #
        envsToDelete = []
        for venvName in environments:
            environment = environments[venvName]
            if environment["variant"] == 2:
                # Python2 environment are not supported anymore, delete them
                envsToDelete.append(venvName)
                continue
            
            if (
                ("is_remote" in environment and environment["is_remote"]) or
                os.access(environment["interpreter"], os.X_OK)
            ):
                if "is_global" not in environment:
                    environment["is_global"] = environment["path"] == ""
                if "is_conda" not in environment:
                    environment["is_conda"] = False
                if "is_remote" not in environment:
                    environment["is_remote"] = False
                if "exec_path" not in environment:
                    environment["exec_path"] = ""
                self.__virtualEnvironments[venvName] = environment
        
        # now remove unsupported environments
        for venvName in envsToDelete:
            del environments[venvName]
        
        # check, if the interpreter used to run eric is in the environments
        defaultPy = sys.executable.replace("w.exe", ".exe")
        found = False
        for venvName in self.__virtualEnvironments:
            if (defaultPy ==
                    self.__virtualEnvironments[venvName]["interpreter"]):
                found = True
                break
        if not found:
            # add an environment entry for the default interpreter
            self.__virtualEnvironments[VirtualenvManager.DefaultKey] = {
                "path": "",
                "interpreter": defaultPy,
                "variant": 3,
                "is_global": True,
                "is_conda": False,
                "is_remote": False,
                "exec_path": "",
            }
        
        self.__saveSettings()
    
    def __saveSettings(self):
        """
        Private slot to save the virtual environments.
        """
        Preferences.Prefs.settings.setValue(
            "PyVenv/VirtualEnvironmentsBaseDir",
            self.__virtualEnvironmentsBaseDir)
        
        Preferences.Prefs.settings.setValue(
            "PyVenv/VirtualEnvironments",
            json.dumps(self.__virtualEnvironments)
        )
        Preferences.syncPreferences()
    
    def getDefaultEnvironment(self):
        """
        Public method to get the default virtual environment.
        
        Default is an environment with the key '<default>' or the first one
        having an interpreter matching sys.executable (i.e. the one used to
        execute eric with)
        
        @return tuple containing the environment name and a dictionary
            containing a copy of the default virtual environment
        @rtype tuple of (str, dict)
        """
        if VirtualenvManager.DefaultKey in self.__virtualEnvironments:
            return (
                VirtualenvManager.DefaultKey,
                copy.copy(
                    self.__virtualEnvironments[VirtualenvManager.DefaultKey])
            )
        
        else:
            defaultPy = sys.executable.replace("w.exe", ".exe")
            for venvName in self.__virtualEnvironments:
                if (defaultPy ==
                        self.__virtualEnvironments[venvName]["interpreter"]):
                    return (
                        venvName,
                        copy.copy(self.__virtualEnvironments[venvName])
                    )
        
        return ("", {})
    
    @pyqtSlot()
    def createVirtualEnv(self, baseDir=""):
        """
        Public slot to create a new virtual environment.
        
        @param baseDir base directory for the virtual environments
        @type str
        """
        from .VirtualenvConfigurationDialog import (
            VirtualenvConfigurationDialog
        )
        
        if not baseDir:
            baseDir = self.__virtualEnvironmentsBaseDir
        
        dlg = VirtualenvConfigurationDialog(baseDir=baseDir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            resultDict = dlg.getData()
            
            if resultDict["envType"] == "conda":
                # create the conda environment
                conda = e5App().getObject("Conda")
                ok, prefix, interpreter = conda.createCondaEnvironment(
                    resultDict["arguments"])
                if ok and "--dry-run" not in resultDict["arguments"]:
                    self.addVirtualEnv(resultDict["logicalName"],
                                       prefix,
                                       venvInterpreter=interpreter,
                                       isConda=True)
            else:
                # now do the call
                from .VirtualenvExecDialog import VirtualenvExecDialog
                dia = VirtualenvExecDialog(resultDict, self)
                dia.show()
                dia.start(resultDict["arguments"])
                dia.exec()
    
    def addVirtualEnv(self, venvName, venvDirectory, venvInterpreter="",
                      isGlobal=False, isConda=False, isRemote=False,
                      execPath=""):
        """
        Public method to add a virtual environment.
        
        @param venvName logical name for the virtual environment
        @type str
        @param venvDirectory directory of the virtual environment
        @type str
        @param venvInterpreter interpreter of the virtual environment
        @type str
        @param isGlobal flag indicating a global environment
        @type bool
        @param isConda flag indicating an Anaconda virtual environment
        @type bool
        @param isRemote flag indicating a remotely accessed environment
        @type bool
        @param execPath search path string to be prepended to the PATH
            environment variable
        @type str
        """
        if venvName in self.__virtualEnvironments:
            ok = E5MessageBox.yesNo(
                None,
                self.tr("Add Virtual Environment"),
                self.tr("""A virtual environment named <b>{0}</b> exists"""
                        """ already. Shall it be replaced?""")
                .format(venvName),
                icon=E5MessageBox.Warning)
            if not ok:
                from .VirtualenvNameDialog import VirtualenvNameDialog
                dlg = VirtualenvNameDialog(
                    list(self.__virtualEnvironments.keys()),
                    venvName)
                if dlg.exec() != QDialog.DialogCode.Accepted:
                    return
                
                venvName = dlg.getName()
        
        if not venvInterpreter:
            from .VirtualenvInterpreterSelectionDialog import (
                VirtualenvInterpreterSelectionDialog
            )
            dlg = VirtualenvInterpreterSelectionDialog(venvName, venvDirectory)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                venvInterpreter = dlg.getData()
        
        if venvInterpreter:
            self.__virtualEnvironments[venvName] = {
                "path": venvDirectory,
                "interpreter": venvInterpreter,
                "variant": 3,                   # always 3
                "is_global": isGlobal,
                "is_conda": isConda,
                "is_remote": isRemote,
                "exec_path": execPath,
            }
            
            self.__saveSettings()
            
            self.virtualEnvironmentAdded.emit()
            if self.__virtualenvManagerDialog:
                self.__virtualenvManagerDialog.refresh()
    
    def setVirtualEnv(self, venvName, venvDirectory, venvInterpreter,
                      isGlobal, isConda, isRemote, execPath):
        """
        Public method to change a virtual environment.
        
        @param venvName logical name of the virtual environment
        @type str
        @param venvDirectory directory of the virtual environment
        @type str
        @param venvInterpreter interpreter of the virtual environment
        @type str
        @param isGlobal flag indicating a global environment
        @type bool
        @param isConda flag indicating an Anaconda virtual environment
        @type bool
        @param isRemote flag indicating a remotely accessed environment
        @type bool
        @param execPath search path string to be prepended to the PATH
            environment variable
        @type str
        """
        if venvName not in self.__virtualEnvironments:
            E5MessageBox.yesNo(
                None,
                self.tr("Change Virtual Environment"),
                self.tr("""A virtual environment named <b>{0}</b> does not"""
                        """ exist. Aborting!""")
                .format(venvName),
                icon=E5MessageBox.Warning)
            return
        
        self.__virtualEnvironments[venvName] = {
            "path": venvDirectory,
            "interpreter": venvInterpreter,
            "variant": 3,                   # always 3
            "is_global": isGlobal,
            "is_conda": isConda,
            "is_remote": isRemote,
            "exec_path": execPath,
        }
        
        self.__saveSettings()
        
        self.virtualEnvironmentChanged.emit(venvName)
        if self.__virtualenvManagerDialog:
            self.__virtualenvManagerDialog.refresh()
    
    def renameVirtualEnv(self, oldVenvName, venvName, venvDirectory,
                         venvInterpreter, isGlobal, isConda,
                         isRemote, execPath):
        """
        Public method to substitute a virtual environment entry with a new
        name.
        
        @param oldVenvName old name of the virtual environment
        @type str
        @param venvName logical name for the virtual environment
        @type str
        @param venvDirectory directory of the virtual environment
        @type str
        @param venvInterpreter interpreter of the virtual environment
        @type str
        @param isGlobal flag indicating a global environment
        @type bool
        @param isConda flag indicating an Anaconda virtual environment
        @type bool
        @param isRemote flag indicating a remotely accessed environment
        @type bool
        @param execPath search path string to be prepended to the PATH
            environment variable
        @type str
        """
        if oldVenvName not in self.__virtualEnvironments:
            E5MessageBox.yesNo(
                None,
                self.tr("Rename Virtual Environment"),
                self.tr("""A virtual environment named <b>{0}</b> does not"""
                        """ exist. Aborting!""")
                .format(oldVenvName),
                icon=E5MessageBox.Warning)
            return
        
        del self.__virtualEnvironments[oldVenvName]
        self.addVirtualEnv(venvName, venvDirectory, venvInterpreter,
                           isGlobal, isConda, isRemote, execPath)
    
    def deleteVirtualEnvs(self, venvNames):
        """
        Public method to delete virtual environments from the list and disk.
        
        @param venvNames list of logical names for the virtual environments
        @type list of str
        """
        venvMessages = []
        for venvName in venvNames:
            if (
                venvName in self.__virtualEnvironments and
                bool(self.__virtualEnvironments[venvName]["path"])
            ):
                venvMessages.append(self.tr("{0} - {1}").format(
                    venvName, self.__virtualEnvironments[venvName]["path"]))
        if venvMessages:
            from UI.DeleteFilesConfirmationDialog import (
                DeleteFilesConfirmationDialog
            )
            dlg = DeleteFilesConfirmationDialog(
                None,
                self.tr("Delete Virtual Environments"),
                self.tr("""Do you really want to delete these virtual"""
                        """ environments?"""),
                venvMessages
            )
            if dlg.exec() == QDialog.DialogCode.Accepted:
                for venvName in venvNames:
                    if self.__isEnvironmentDeleteable(venvName):
                        if self.isCondaEnvironment(venvName):
                            conda = e5App().getObject("Conda")
                            path = self.__virtualEnvironments[venvName]["path"]
                            res = conda.removeCondaEnvironment(prefix=path)
                            if res:
                                del self.__virtualEnvironments[venvName]
                        else:
                            shutil.rmtree(
                                self.__virtualEnvironments[venvName]["path"],
                                True)
                            del self.__virtualEnvironments[venvName]
                
                self.__saveSettings()
                
                self.virtualEnvironmentRemoved.emit()
                if self.__virtualenvManagerDialog:
                    self.__virtualenvManagerDialog.refresh()
    
    def __isEnvironmentDeleteable(self, venvName):
        """
        Private method to check, if a virtual environment can be deleted from
        disk.
        
        @param venvName name of the virtual environment
        @type str
        @return flag indicating it can be deleted
        @rtype bool
        """
        ok = False
        if venvName in self.__virtualEnvironments:
            ok = True
            ok &= bool(self.__virtualEnvironments[venvName]["path"])
            ok &= not self.__virtualEnvironments[venvName]["is_global"]
            ok &= not self.__virtualEnvironments[venvName]["is_remote"]
            ok &= os.access(self.__virtualEnvironments[venvName]["path"],
                            os.W_OK)
        
        return ok
    
    def removeVirtualEnvs(self, venvNames):
        """
        Public method to delete virtual environment from the list.
        
        @param venvNames list of logical names for the virtual environments
        @type list of str
        """
        venvMessages = []
        for venvName in venvNames:
            if venvName in self.__virtualEnvironments:
                venvMessages.append(self.tr("{0} - {1}").format(
                    venvName, self.__virtualEnvironments[venvName]["path"]))
        if venvMessages:
            from UI.DeleteFilesConfirmationDialog import (
                DeleteFilesConfirmationDialog
            )
            dlg = DeleteFilesConfirmationDialog(
                None,
                self.tr("Remove Virtual Environments"),
                self.tr("""Do you really want to remove these virtual"""
                        """ environments?"""),
                venvMessages
            )
            if dlg.exec() == QDialog.DialogCode.Accepted:
                for venvName in venvNames:
                    if venvName in self.__virtualEnvironments:
                        del self.__virtualEnvironments[venvName]
                
                self.__saveSettings()
                
                self.virtualEnvironmentRemoved.emit()
                if self.__virtualenvManagerDialog:
                    self.__virtualenvManagerDialog.refresh()
    
    def getEnvironmentEntries(self):
        """
        Public method to get a dictionary containing the defined virtual
        environment entries.
        
        @return dictionary containing a copy of the defined virtual
            environments
        @rtype dict
        """
        return copy.deepcopy(self.__virtualEnvironments)
    
    @pyqtSlot()
    def showVirtualenvManagerDialog(self, modal=False):
        """
        Public slot to show the virtual environment manager dialog.
        
        @param modal flag indicating that the dialog should be shown in
            a blocking mode
        """
        if self.__virtualenvManagerDialog is None:
            from .VirtualenvManagerDialog import VirtualenvManagerDialog
            self.__virtualenvManagerDialog = VirtualenvManagerDialog(
                self, self.__ui)
        
        if modal:
            self.__virtualenvManagerDialog.exec()
        else:
            self.__virtualenvManagerDialog.show()
    
    def shutdown(self):
        """
        Public method to shutdown the manager.
        """
        if self.__virtualenvManagerDialog is not None:
            self.__virtualenvManagerDialog.close()
            self.__virtualenvManagerDialog = None
    
    def isUnique(self, venvName):
        """
        Public method to check, if the give logical name is unique.
        
        @param venvName logical name for the virtual environment
        @type str
        @return flag indicating uniqueness
        @rtype bool
        """
        return venvName not in self.__virtualEnvironments
    
    def getVirtualenvInterpreter(self, venvName):
        """
        Public method to get the interpreter for a virtual environment.
        
        @param venvName logical name for the virtual environment
        @type str
        @return interpreter path
        @rtype str
        """
        if venvName in self.__virtualEnvironments:
            return self.__virtualEnvironments[venvName]["interpreter"]
        else:
            return ""
    
    def getVirtualenvDirectory(self, venvName):
        """
        Public method to get the directory of a virtual environment.
        
        @param venvName logical name for the virtual environment
        @type str
        @return directory path
        @rtype str
        """
        if venvName in self.__virtualEnvironments:
            return self.__virtualEnvironments[venvName]["path"]
        else:
            return ""
    
    def getVirtualenvNames(self, noRemote=False, noConda=False):
        """
        Public method to get a list of defined virtual environments.
        
        @param noRemote flag indicating to exclude environments for remote
            debugging
        @type bool
        @param noConda flag indicating to exclude Conda environments
        @type bool
        @return list of defined virtual environments
        @rtype list of str
        """
        environments = list(self.__virtualEnvironments.keys())
        if noRemote:
            environments = [name for name in environments
                            if not self.isRemoteEnvironment(name)]
        if noConda:
            environments = [name for name in environments
                            if not self.isCondaEnvironment(name)]
        
        return environments
    
    def isGlobalEnvironment(self, venvName):
        """
        Public method to test, if a given environment is a global one.
        
        @param venvName logical name of the virtual environment
        @type str
        @return flag indicating a global environment
        @rtype bool
        """
        if venvName in self.__virtualEnvironments:
            return self.__virtualEnvironments[venvName]["is_global"]
        else:
            return False
    
    def isCondaEnvironment(self, venvName):
        """
        Public method to test, if a given environment is an Anaconda
        environment.
        
        @param venvName logical name of the virtual environment
        @type str
        @return flag indicating an Anaconda environment
        @rtype bool
        """
        if venvName in self.__virtualEnvironments:
            return self.__virtualEnvironments[venvName]["is_conda"]
        else:
            return False
    
    def isRemoteEnvironment(self, venvName):
        """
        Public method to test, if a given environment is a remotely accessed
        environment.
        
        @param venvName logical name of the virtual environment
        @type str
        @return flag indicating a remotely accessed environment
        @rtype bool
        """
        if venvName in self.__virtualEnvironments:
            return self.__virtualEnvironments[venvName]["is_remote"]
        else:
            return False
    
    def getVirtualenvExecPath(self, venvName):
        """
        Public method to get the search path prefix of a virtual environment.
        
        @param venvName logical name for the virtual environment
        @type str
        @return search path prefix
        @rtype str
        """
        if venvName in self.__virtualEnvironments:
            return self.__virtualEnvironments[venvName]["exec_path"]
        else:
            return ""
    
    def setVirtualEnvironmentsBaseDir(self, baseDir):
        """
        Public method to set the base directory for the virtual environments.
        
        @param baseDir base directory for the virtual environments
        @type str
        """
        self.__virtualEnvironmentsBaseDir = baseDir
        self.__saveSettings()
    
    def getVirtualEnvironmentsBaseDir(self):
        """
        Public method to set the base directory for the virtual environments.
        
        @return base directory for the virtual environments
        @rtype str
        """
        return self.__virtualEnvironmentsBaseDir
