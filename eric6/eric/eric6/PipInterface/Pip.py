# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the pip GUI logic.
"""

import os
import sys
import json

from PyQt5.QtCore import pyqtSlot, QObject, QProcess, QUrl, QCoreApplication
from PyQt5.QtWidgets import QDialog, QInputDialog, QLineEdit
from PyQt5.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)

from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App

from E5Network.E5NetworkProxyFactory import proxyAuthenticationRequired
try:
    from E5Network.E5SslErrorHandler import E5SslErrorHandler
    SSL_AVAILABLE = True
except ImportError:
    SSL_AVAILABLE = False

from .PipDialog import PipDialog

import Preferences
import Globals


class Pip(QObject):
    """
    Class implementing the pip GUI logic.
    """
    DefaultPyPiUrl = "https://pypi.org"
    DefaultIndexUrlPypi = DefaultPyPiUrl + "/pypi"
    DefaultIndexUrlSimple = DefaultPyPiUrl + "/simple"
    DefaultIndexUrlSearch = DefaultPyPiUrl + "/search/"
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent
        @type QObject
        """
        super(Pip, self).__init__(parent)
        
        # attributes for the network objects
        self.__networkManager = QNetworkAccessManager(self)
        self.__networkManager.proxyAuthenticationRequired.connect(
            proxyAuthenticationRequired)
        if SSL_AVAILABLE:
            self.__sslErrorHandler = E5SslErrorHandler(self)
            self.__networkManager.sslErrors.connect(
                self.__sslErrorHandler.sslErrorsReply)
        self.__replies = []
    
    def getNetworkAccessManager(self):
        """
        Public method to get a reference to the network access manager object.
        
        @return reference to the network access manager object
        @rtype QNetworkAccessManager
        """
        return self.__networkManager
    
    ##########################################################################
    ## Methods below implement some utility functions
    ##########################################################################
    
    def runProcess(self, args, interpreter):
        """
        Public method to execute the current pip with the given arguments.
        
        The selected pip executable is called with the given arguments and
        waited for its end.
        
        @param args list of command line arguments
        @type list of str
        @param interpreter path of the Python interpreter to be used
        @type str
        @return tuple containing a flag indicating success and the output
            of the process
        @rtype tuple of (bool, str)
        """
        ioEncoding = Preferences.getSystem("IOEncoding")
        
        process = QProcess()
        process.start(interpreter, args)
        procStarted = process.waitForStarted()
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished:
                if process.exitCode() == 0:
                    output = str(process.readAllStandardOutput(), ioEncoding,
                                 'replace')
                    return True, output
                else:
                    return (False,
                            self.tr("python exited with an error ({0}).")
                            .format(process.exitCode()))
            else:
                process.terminate()
                process.waitForFinished(2000)
                process.kill()
                process.waitForFinished(3000)
                return False, self.tr("python did not finish within"
                                      " 30 seconds.")
        
        return False, self.tr("python could not be started.")
    
    def getUserConfig(self):
        """
        Public method to get the name of the user configuration file.
        
        @return path of the user configuration file
        @rtype str
        """
        # Unix:     ~/.config/pip/pip.conf
        # OS X:     ~/Library/Application Support/pip/pip.conf
        # Windows:  %APPDATA%\pip\pip.ini
        # Environment: $PIP_CONFIG_FILE
        
        try:
            return os.environ["PIP_CONFIG_FILE"]
        except KeyError:
            pass
        
        if Globals.isWindowsPlatform():
            config = os.path.join(os.environ["APPDATA"], "pip", "pip.ini")
        elif Globals.isMacPlatform():
            config = os.path.expanduser(
                "~/Library/Application Support/pip/pip.conf")
        else:
            config = os.path.expanduser("~/.config/pip/pip.conf")
        
        return config
    
    def getVirtualenvConfig(self, venvName):
        """
        Public method to get the name of the virtualenv configuration file.
        
        @param venvName name of the environment to get config file path for
        @type str
        @return path of the virtualenv configuration file
        @rtype str
        """
        # Unix, OS X:   $VIRTUAL_ENV/pip.conf
        # Windows:      %VIRTUAL_ENV%\pip.ini
        
        if Globals.isWindowsPlatform():
            pip = "pip.ini"
        else:
            pip = "pip.conf"
        
        venvManager = e5App().getObject("VirtualEnvManager")
        if venvManager.isGlobalEnvironment(venvName):
            venvDirectory = os.path.dirname(self.getUserConfig())
        else:
            venvDirectory = venvManager.getVirtualenvDirectory(venvName)
        
        if venvDirectory:
            config = os.path.join(venvDirectory, pip)
        else:
            config = ""
        
        return config
    
    def getProjectEnvironmentString(self):
        """
        Public method to get the string for the project environment.
        
        @return string for the project environment
        @rtype str
        """
        if e5App().getObject("Project").isOpen():
            return self.tr("<project>")
        else:
            return ""
    
    def getVirtualenvInterpreter(self, venvName):
        """
        Public method to get the interpreter for a virtual environment.
        
        @param venvName logical name for the virtual environment
        @type str
        @return interpreter path
        @rtype str
        """
        if venvName == self.getProjectEnvironmentString():
            venvName = (
                e5App().getObject("Project")
                .getDebugProperty("VIRTUALENV")
            )
            if not venvName:
                # fall back to interpreter used to run eric6
                return sys.executable
        
        interpreter = (
            e5App().getObject("VirtualEnvManager")
            .getVirtualenvInterpreter(venvName)
        )
        if not interpreter:
            E5MessageBox.critical(
                None,
                self.tr("Interpreter for Virtual Environment"),
                self.tr("""No interpreter configured for the selected"""
                        """ virtual environment."""))
        
        return interpreter
    
    def getVirtualenvNames(self, noRemote=False, noConda=False):
        """
        Public method to get a sorted list of virtual environment names.
        
        @param noRemote flag indicating to exclude environments for remote
            debugging
        @type bool
        @param noConda flag indicating to exclude Conda environments
        @type bool
        @return sorted list of virtual environment names
        @rtype list of str
        """
        return sorted(
            e5App().getObject("VirtualEnvManager").getVirtualenvNames(
                noRemote=noRemote, noConda=noConda))
    
    def installPip(self, venvName, userSite=False):
        """
        Public method to install pip.
        
        @param venvName name of the environment to install pip into
        @type str
        @param userSite flag indicating an install to the user install
            directory
        @type bool
        """
        interpreter = self.getVirtualenvInterpreter(venvName)
        if not interpreter:
            return
        
        dia = PipDialog(self.tr('Install PIP'))
        if userSite:
            commands = [(interpreter, ["-m", "ensurepip", "--user"])]
        else:
            commands = [(interpreter, ["-m", "ensurepip"])]
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
            args = ["-m", "pip", "install", "--index-url", indexUrl,
                    "--upgrade"]
        else:
            args = ["-m", "pip", "install", "--upgrade"]
        if userSite:
            args.append("--user")
        args.append("pip")
        commands.append((interpreter, args[:]))
    
        res = dia.startProcesses(commands)
        if res:
            dia.exec()
    
    @pyqtSlot()
    def repairPip(self, venvName):
        """
        Public method to repair the pip installation.
        
        @param venvName name of the environment to install pip into
        @type str
        """
        interpreter = self.getVirtualenvInterpreter(venvName)
        if not interpreter:
            return
        
        # python -m pip install --ignore-installed pip
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
            args = ["-m", "pip", "install", "--index-url", indexUrl,
                    "--ignore-installed"]
        else:
            args = ["-m", "pip", "install", "--ignore-installed"]
        args.append("pip")
        
        dia = PipDialog(self.tr('Repair PIP'))
        res = dia.startProcess(interpreter, args)
        if res:
            dia.exec()
    
    def __checkUpgradePyQt(self, packages):
        """
        Private method to check, if an upgrade of PyQt packages is attempted.
        
        @param packages list of packages to upgrade
        @type list of str
        @return flag indicating to abort the upgrade attempt
        @rtype bool
        """
        pyqtPackages = [p for p in packages
                        if p.lower() in ["pyqt5", "pyqt5-sip", "pyqtwebengine",
                                         "qscintilla", "sip"]]
        
        if bool(pyqtPackages):
            abort = not E5MessageBox.yesNo(
                None,
                self.tr("Upgrade Packages"),
                self.tr(
                    """You are trying to upgrade PyQt packages. This might"""
                    """ not work for the current instance of Python ({0})."""
                    """ Do you want to continue?""").format(sys.executable),
                icon=E5MessageBox.Critical)
        else:
            abort = False
        
        return abort
    
    def upgradePackages(self, packages, venvName, userSite=False):
        """
        Public method to upgrade the given list of packages.
        
        @param packages list of packages to upgrade
        @type list of str
        @param venvName name of the virtual environment to be used
        @type str
        @param userSite flag indicating an install to the user install
            directory
        @type bool
        @return flag indicating a successful execution
        @rtype bool
        """
        if self.__checkUpgradePyQt(packages):
            return False
        
        if not venvName:
            return False
        
        interpreter = self.getVirtualenvInterpreter(venvName)
        if not interpreter:
            return False
        
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
            args = ["-m", "pip", "install", "--index-url", indexUrl,
                    "--upgrade"]
        else:
            args = ["-m", "pip", "install", "--upgrade"]
        if userSite:
            args.append("--user")
        args += packages
        dia = PipDialog(self.tr('Upgrade Packages'))
        res = dia.startProcess(interpreter, args)
        if res:
            dia.exec()
        return res
    
    def installPackages(self, packages, venvName="", userSite=False,
                        interpreter="", forceReinstall=False):
        """
        Public method to install the given list of packages.
        
        @param packages list of packages to install
        @type list of str
        @param venvName name of the virtual environment to be used
        @type str
        @param userSite flag indicating an install to the user install
            directory
        @type bool
        @param interpreter interpreter to be used for execution
        @type str
        @param forceReinstall flag indicating to force a reinstall of
            the packages
        @type bool
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if not interpreter:
                return
        
        if interpreter:
            if Preferences.getPip("PipSearchIndex"):
                indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                args = ["-m", "pip", "install", "--index-url", indexUrl]
            else:
                args = ["-m", "pip", "install"]
            if userSite:
                args.append("--user")
            if forceReinstall:
                args.append("--force-reinstall")
            args += packages
            dia = PipDialog(self.tr('Install Packages'))
            res = dia.startProcess(interpreter, args)
            if res:
                dia.exec()
    
    def installRequirements(self, venvName):
        """
        Public method to install packages as given in a requirements file.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        from .PipFileSelectionDialog import PipFileSelectionDialog
        dlg = PipFileSelectionDialog(self, "requirements")
        if dlg.exec() == QDialog.DialogCode.Accepted:
            requirements, user = dlg.getData()
            if requirements and os.path.exists(requirements):
                interpreter = self.getVirtualenvInterpreter(venvName)
                if not interpreter:
                    return
                
                if Preferences.getPip("PipSearchIndex"):
                    indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                    args = ["-m", "pip", "install", "--index-url", indexUrl]
                else:
                    args = ["-m", "pip", "install"]
                if user:
                    args.append("--user")
                args += ["--requirement", requirements]
                dia = PipDialog(self.tr('Install Packages from Requirements'))
                res = dia.startProcess(interpreter, args)
                if res:
                    dia.exec()
    
    def uninstallPackages(self, packages, venvName):
        """
        Public method to uninstall the given list of packages.
        
        @param packages list of packages to uninstall
        @type list of str
        @param venvName name of the virtual environment to be used
        @type str
        @return flag indicating a successful execution
        @rtype bool
        """
        res = False
        if packages and venvName:
            from UI.DeleteFilesConfirmationDialog import (
                DeleteFilesConfirmationDialog
            )
            dlg = DeleteFilesConfirmationDialog(
                self.parent(),
                self.tr("Uninstall Packages"),
                self.tr(
                    "Do you really want to uninstall these packages?"),
                packages)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                interpreter = self.getVirtualenvInterpreter(venvName)
                if not interpreter:
                    return False
                args = ["-m", "pip", "uninstall", "--yes"] + packages
                dia = PipDialog(self.tr('Uninstall Packages'))
                res = dia.startProcess(interpreter, args)
                if res:
                    dia.exec()
        return res
    
    def uninstallRequirements(self, venvName):
        """
        Public method to uninstall packages as given in a requirements file.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            from .PipFileSelectionDialog import PipFileSelectionDialog
            dlg = PipFileSelectionDialog(self, "requirements",
                                         install=False)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                requirements, _user = dlg.getData()
                if requirements and os.path.exists(requirements):
                    try:
                        with open(requirements, "r") as f:
                            reqs = f.read().splitlines()
                    except OSError:
                        return
                    
                    from UI.DeleteFilesConfirmationDialog import (
                        DeleteFilesConfirmationDialog
                    )
                    dlg = DeleteFilesConfirmationDialog(
                        self.parent(),
                        self.tr("Uninstall Packages"),
                        self.tr(
                            "Do you really want to uninstall these packages?"),
                        reqs)
                    if dlg.exec() == QDialog.DialogCode.Accepted:
                        interpreter = self.getVirtualenvInterpreter(venvName)
                        if not interpreter:
                            return
                        
                        args = ["-m", "pip", "uninstall", "--requirement",
                                requirements]
                        dia = PipDialog(
                            self.tr('Uninstall Packages from Requirements'))
                        res = dia.startProcess(interpreter, args)
                        if res:
                            dia.exec()
    
    def getIndexUrl(self):
        """
        Public method to get the index URL for PyPI.
        
        @return index URL for PyPI
        @rtype str
        """
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
        else:
            indexUrl = Pip.DefaultIndexUrlSimple
        
        return indexUrl
    
    def getIndexUrlPypi(self):
        """
        Public method to get the index URL for PyPI API calls.
        
        @return index URL for XML RPC calls
        @rtype str
        """
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/pypi"
        else:
            indexUrl = Pip.DefaultIndexUrlPypi
        
        return indexUrl
    
    def getIndexUrlSearch(self):
        """
        Public method to get the index URL for PyPI API calls.
        
        @return index URL for XML RPC calls
        @rtype str
        """
        if Preferences.getPip("PipSearchIndex"):
            indexUrl = Preferences.getPip("PipSearchIndex") + "/search/"
        else:
            indexUrl = Pip.DefaultIndexUrlSearch
        
        return indexUrl
    
    def getInstalledPackages(self, envName, localPackages=True,
                             notRequired=False, usersite=False):
        """
        Public method to get the list of installed packages.
        
        @param envName name of the environment to get the packages for
        @type str
        @param localPackages flag indicating to get local packages only
        @type bool
        @param notRequired flag indicating to list packages that are not
            dependencies of installed packages as well
        @type bool
        @param usersite flag indicating to only list packages installed
            in user-site
        @type bool
        @return list of tuples containing the package name and version
        @rtype list of tuple of (str, str)
        """
        packages = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                args = [
                    "-m", "pip",
                    "list",
                    "--format=json",
                ]
                if localPackages:
                    args.append("--local")
                if notRequired:
                    args.append("--not-required")
                if usersite:
                    args.append("--user")
                
                if Preferences.getPip("PipSearchIndex"):
                    indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                    args += ["--index-url", indexUrl]
                
                proc = QProcess()
                proc.start(interpreter, args)
                if proc.waitForStarted(15000):
                    if proc.waitForFinished(30000):
                        output = str(proc.readAllStandardOutput(),
                                     Preferences.getSystem("IOEncoding"),
                                     'replace').strip()
                        try:
                            jsonList = json.loads(output)
                        except Exception:
                            jsonList = []
                        
                        for package in jsonList:
                            if isinstance(package, dict):
                                packages.append((
                                    package["name"],
                                    package["version"],
                                ))
           
        return packages
    
    def getOutdatedPackages(self, envName, localPackages=True,
                            notRequired=False, usersite=False):
        """
        Public method to get the list of outdated packages.
        
        @param envName name of the environment to get the packages for
        @type str
        @param localPackages flag indicating to get local packages only
        @type bool
        @param notRequired flag indicating to list packages that are not
            dependencies of installed packages as well
        @type bool
        @param usersite flag indicating to only list packages installed
            in user-site
        @type bool
        @return list of tuples containing the package name, installed version
            and available version
        @rtype list of tuple of (str, str, str)
        """
        packages = []
        
        if envName:
            interpreter = self.getVirtualenvInterpreter(envName)
            if interpreter:
                args = [
                    "-m", "pip",
                    "list",
                    "--outdated",
                    "--format=json",
                ]
                if localPackages:
                    args.append("--local")
                if notRequired:
                    args.append("--not-required")
                if usersite:
                    args.append("--user")
                
                if Preferences.getPip("PipSearchIndex"):
                    indexUrl = Preferences.getPip("PipSearchIndex") + "/simple"
                    args += ["--index-url", indexUrl]
                
                proc = QProcess()
                proc.start(interpreter, args)
                if proc.waitForStarted(15000):
                    if proc.waitForFinished(30000):
                        output = str(proc.readAllStandardOutput(),
                                     Preferences.getSystem("IOEncoding"),
                                     'replace').strip()
                        try:
                            jsonList = json.loads(output)
                        except Exception:
                            jsonList = []
                        
                        for package in jsonList:
                            if isinstance(package, dict):
                                packages.append((
                                    package["name"],
                                    package["version"],
                                    package["latest_version"],
                                ))
           
        return packages
    
    def getPackageDetails(self, name, version):
        """
        Public method to get package details using the PyPI JSON interface.
        
        @param name package name
        @type str
        @param version package version
        @type str
        @return dictionary containing PyPI package data
        @rtype dict
        """
        result = {}
        
        if name and version:
            url = "{0}/{1}/{2}/json".format(
                self.getIndexUrlPypi(), name, version)
            request = QNetworkRequest(QUrl(url))
            reply = self.__networkManager.get(request)
            while not reply.isFinished():
                QCoreApplication.processEvents()
            
            reply.deleteLater()
            if reply.error() == QNetworkReply.NetworkError.NoError:
                data = str(reply.readAll(),
                           Preferences.getSystem("IOEncoding"),
                           'replace')
                try:
                    result = json.loads(data)
                except Exception:           # secok
                    # ignore JSON exceptions
                    pass
        
        return result
    
    #######################################################################
    ## Cache handling methods below
    #######################################################################
    
    def showCacheInfo(self, venvName):
        """
        Public method to show some information about the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                args = ["-m", "pip", "cache", "info"]
                dia = PipDialog(self.tr("Cache Info"))
                res = dia.startProcess(interpreter, args, showArgs=False)
                if res:
                    dia.exec()
    
    def cacheList(self, venvName):
        """
        Public method to list files contained in the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                pattern, ok = QInputDialog.getText(
                    None,
                    self.tr("List Cached Files"),
                    self.tr("Enter a file pattern (empty for all):"),
                    QLineEdit.EchoMode.Normal)
                
                if ok:
                    args = ["-m", "pip", "cache", "list"]
                    if pattern.strip():
                        args.append(pattern.strip())
                    dia = PipDialog(self.tr("List Cached Files"))
                    res = dia.startProcess(interpreter, args,
                                           showArgs=False)
                    if res:
                        dia.exec()
    
    def cacheRemove(self, venvName):
        """
        Public method to remove files from the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                pattern, ok = QInputDialog.getText(
                    None,
                    self.tr("Remove Cached Files"),
                    self.tr("Enter a file pattern:"),
                    QLineEdit.EchoMode.Normal)
                
                if ok and pattern.strip():
                    args = ["-m", "pip", "cache", "remove", pattern.strip()]
                    dia = PipDialog(self.tr("Remove Cached Files"))
                    res = dia.startProcess(interpreter, args,
                                           showArgs=False)
                    if res:
                        dia.exec()
    
    def cachePurge(self, venvName):
        """
        Public method to remove all files from the pip cache.
        
        @param venvName name of the virtual environment to be used
        @type str
        """
        if venvName:
            interpreter = self.getVirtualenvInterpreter(venvName)
            if interpreter:
                ok = E5MessageBox.yesNo(
                    None,
                    self.tr("Purge Cache"),
                    self.tr("Do you really want to purge the pip cache? All"
                            " files need to be downloaded again."))
                if ok:
                    args = ["-m", "pip", "cache", "purge"]
                    dia = PipDialog(self.tr("Purge Cache"))
                    res = dia.startProcess(interpreter, args,
                                           showArgs=False)
                    if res:
                        dia.exec()
