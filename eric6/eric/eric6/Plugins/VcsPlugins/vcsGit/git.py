# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the version control systems interface to Git.
"""

import os
import shutil
import re

from PyQt5.QtCore import QProcess, pyqtSignal, QFileInfo
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox, E5FileDialog

from QScintilla.MiniEditor import MiniEditor

from VCS.VersionControl import VersionControl
from VCS.RepositoryInfoDialog import VcsRepositoryInfoDialog

from .GitDialog import GitDialog

import Utilities
import Preferences


class Git(VersionControl):
    """
    Class implementing the version control systems interface to Git.
    
    @signal committed() emitted after the commit action has completed
    """
    committed = pyqtSignal()
    
    IgnoreFileName = ".gitignore"
    
    def __init__(self, plugin, parent=None, name=None):
        """
        Constructor
        
        @param plugin reference to the plugin object
        @param parent parent widget (QWidget)
        @param name name of this object (string)
        """
        VersionControl.__init__(self, parent, name)
        self.defaultOptions = {
            'global': [''],
            'commit': [''],
            'checkout': [''],
            'update': [''],
            'add': [''],
            'remove': [''],
            'diff': [''],
            'log': [''],
            'history': [''],
            'status': [''],
            'tag': [''],
            'export': ['']
        }
        
        self.__plugin = plugin
        self.__ui = parent
        
        self.options = self.defaultOptions
        
        self.tagTypeList = [
            'tags',
            'branches',
        ]
        
        self.commandHistory = []
        
        self.adminDir = '.git'
        
        self.log = None
        self.logBrowser = None
        self.reflogBrowser = None
        self.diff = None
        self.sbsDiff = None
        self.tagbranchList = None
        self.status = None
        self.remotesDialog = None
        self.describeDialog = None
        self.blame = None
        self.stashBrowser = None
        self.repoEditor = None
        self.userEditor = None
        self.bisectlogBrowser = None
        self.bisectReplayEditor = None
        self.patchStatisticsDialog = None
        self.submoduleStatusDialog = None
        
        self.__lastBundlePath = None
        self.__lastReplayPath = None
        
        self.statusCache = {}
        
        self.__commitData = {}
        self.__commitDialog = None
        
        self.__patchCheckData = None
        
        self.__projectHelper = None
    
    def getPlugin(self):
        """
        Public method to get a reference to the plugin object.
        
        @return reference to the plugin object (VcsGitPlugin)
        """
        return self.__plugin
    
    def vcsShutdown(self):
        """
        Public method used to shutdown the Git interface.
        """
        if self.log is not None:
            self.log.close()
        if self.logBrowser is not None:
            self.logBrowser.close()
        if self.reflogBrowser is not None:
            self.reflogBrowser.close()
        if self.diff is not None:
            self.diff.close()
        if self.sbsDiff is not None:
            self.sbsDiff.close()
        if self.tagbranchList is not None:
            self.tagbranchList.close()
        if self.status is not None:
            self.status.close()
        if self.remotesDialog is not None:
            self.remotesDialog.close()
        if self.describeDialog is not None:
            self.describeDialog.close()
        if self.blame is not None:
            self.blame.close()
        if self.stashBrowser is not None:
            self.stashBrowser.close()
        if self.bisectlogBrowser is not None:
            self.bisectlogBrowser.close()
        if self.bisectReplayEditor is not None:
            self.bisectReplayEditor.close()
        if self.repoEditor is not None:
            self.repoEditor.close()
        if self.userEditor is not None:
            self.userEditor.close()
        if self.patchStatisticsDialog is not None:
            self.patchStatisticsDialog.close()
        if self.submoduleStatusDialog is not None:
            self.submoduleStatusDialog.close()
        
        # shut down the project helpers
        if self.__projectHelper is not None:
            self.__projectHelper.shutdown()
    
    def initCommand(self, command):
        """
        Public method to initialize a command arguments list.
        
        @param command command name (string)
        @return list of command options (list of string)
        """
        args = [command]
        return args
    
    def vcsExists(self):
        """
        Public method used to test for the presence of the git executable.
        
        @return flag indicating the existance (boolean) and an error message
            (string)
        """
        self.versionStr = ''
        errMsg = ""
        ioEncoding = Preferences.getSystem("IOEncoding")
        
        args = self.initCommand("version")
        process = QProcess()
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             ioEncoding, 'replace')
                versionLine = output.splitlines()[0]
                v = list(re.match(r'.*?(\d+)\.(\d+)\.?(\d+)?\.?(\d+)?',
                                  versionLine).groups())
                for i in range(4):
                    try:
                        v[i] = int(v[i])
                    except TypeError:
                        v[i] = 0
                    except IndexError:
                        v.append(0)
                self.version = tuple(v)
                self.versionStr = '.'.join([str(v) for v in self.version])
                return True, errMsg
            else:
                if finished:
                    errMsg = self.tr(
                        "The git process finished with the exit code {0}"
                    ).format(process.exitCode())
                else:
                    errMsg = self.tr(
                        "The git process did not finish within 30s.")
        else:
            errMsg = self.tr("Could not start the git executable.")
        
        return False, errMsg
    
    def vcsInit(self, vcsDir, noDialog=False):
        """
        Public method used to initialize the Git repository.
        
        The initialization is done, when a project is converted into a
        Git controlled project. Therefore we always return TRUE without
        doing anything.
        
        @param vcsDir name of the VCS directory (string)
        @param noDialog flag indicating quiet operations (boolean)
        @return always TRUE
        """
        return True
    
    def vcsConvertProject(self, vcsDataDict, project, addAll=True):
        """
        Public method to convert an uncontrolled project to a version
        controlled project.
        
        @param vcsDataDict dictionary of data required for the conversion
        @type dict
        @param project reference to the project object
        @type Project
        @param addAll flag indicating to add all files to the repository
        @type bool
        """
        success = self.vcsImport(vcsDataDict, project.ppath, addAll=addAll)[0]
        if not success:
            E5MessageBox.critical(
                self.__ui,
                self.tr("Create project repository"),
                self.tr(
                    """The project repository could not be created."""))
        else:
            pfn = project.pfile
            if not os.path.isfile(pfn):
                pfn += "z"
            project.closeProject()
            project.openProject(pfn)
    
    def vcsImport(self, vcsDataDict, projectDir, noDialog=False, addAll=True):
        """
        Public method used to import the project into the Git repository.
        
        @param vcsDataDict dictionary of data required for the import
        @type dict
        @param projectDir project directory (string)
        @type str
        @param noDialog flag indicating quiet operations
        @type bool
        @param addAll flag indicating to add all files to the repository
        @type bool
        @return tuple containing a flag indicating an execution without errors
            and a flag indicating the version controll status
        @rtype tuple of (bool, bool)
        """
        msg = vcsDataDict["message"]
        if not msg:
            msg = '***'
        
        args = self.initCommand("init")
        args.append(projectDir)
        dia = GitDialog(self.tr('Creating Git repository'), self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        status = dia.normalExit()
        
        if status:
            ignoreName = os.path.join(projectDir, Git.IgnoreFileName)
            if not os.path.exists(ignoreName):
                status = self.gitCreateIgnoreFile(projectDir)
            
            if status and addAll:
                args = self.initCommand("add")
                args.append("-v")
                args.append(".")
                dia = GitDialog(
                    self.tr('Adding files to Git repository'),
                    self)
                res = dia.startProcess(args, projectDir)
                if res:
                    dia.exec()
                status = dia.normalExit()
                
                if status:
                    args = self.initCommand("commit")
                    args.append('--message={0}'.format(msg))
                    dia = GitDialog(
                        self.tr('Initial commit to Git repository'),
                        self)
                    res = dia.startProcess(args, projectDir)
                    if res:
                        dia.exec()
                    status = dia.normalExit()
        
        return status, False
    
    def vcsCheckout(self, vcsDataDict, projectDir, noDialog=False):
        """
        Public method used to check the project out of a Git repository
        (clone).
        
        @param vcsDataDict dictionary of data required for the checkout
        @param projectDir project directory to create (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating an execution without errors (boolean)
        """
        noDialog = False
        vcsUrl = self.gitNormalizeURL(vcsDataDict["url"])
        
        args = self.initCommand("clone")
        args.append(vcsUrl)
        args.append(projectDir)
        
        if noDialog:
            return self.startSynchronizedProcess(QProcess(), 'git', args)
        else:
            dia = GitDialog(
                self.tr('Cloning project from a Git repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
            return dia.normalExit()
    
    def vcsExport(self, vcsDataDict, projectDir):
        """
        Public method used to export a directory from the Git repository.
        
        @param vcsDataDict dictionary of data required for the checkout
        @param projectDir project directory to create (string)
        @return flag indicating an execution without errors (boolean)
        """
        status = self.vcsCheckout(vcsDataDict, projectDir)
        shutil.rmtree(os.path.join(projectDir, self.adminDir), True)
        if os.path.exists(os.path.join(projectDir, Git.IgnoreFileName)):
            os.remove(os.path.join(projectDir, Git.IgnoreFileName))
        return status
    
    def vcsCommit(self, name, message="", noDialog=False, commitAll=True,
                  amend=False):
        """
        Public method used to make the change of a file/directory permanent
        in the Git repository.
        
        @param name file/directory name to be committed (string or list of
            strings)
        @param message message for this operation (string)
        @param noDialog flag indicating quiet operations (boolean)
        @param commitAll flag indicating to commit all local changes (boolean)
        @param amend flag indicating to amend the HEAD commit (boolean)
        """
        if not noDialog:
            # call CommitDialog and get message from there
            if self.__commitDialog is None:
                from .GitCommitDialog import GitCommitDialog
                self.__commitDialog = GitCommitDialog(self, message, amend,
                                                      commitAll, self.__ui)
                self.__commitDialog.accepted.connect(self.__vcsCommit_Step2)
            self.__commitDialog.show()
            self.__commitDialog.raise_()
            self.__commitDialog.activateWindow()
        
        self.__commitData["name"] = name
        self.__commitData["msg"] = message
        self.__commitData["noDialog"] = noDialog
        self.__commitData["all"] = commitAll
        
        if noDialog:
            self.__vcsCommit_Step2()
    
    def __vcsCommit_Step2(self):
        """
        Private slot performing the second step of the commit action.
        """
        name = self.__commitData["name"]
        msg = self.__commitData["msg"]
        noDialog = self.__commitData["noDialog"]
        commitAll = self.__commitData["all"]
        
        if not noDialog:
            # check, if there are unsaved changes, that should be committed
            if isinstance(name, list):
                nameList = name
            else:
                nameList = [name]
            ok = True
            for nam in nameList:
                # check for commit of the project
                if os.path.isdir(nam):
                    project = e5App().getObject("Project")
                    if nam == project.getProjectPath():
                        ok &= (
                            project.checkAllScriptsDirty(
                                reportSyntaxErrors=True) and
                            project.checkDirty()
                        )
                        continue
                elif os.path.isfile(nam):
                    editor = (
                        e5App().getObject("ViewManager").getOpenEditor(nam)
                    )
                    if editor:
                        ok &= editor.checkDirty()
                if not ok:
                    break
            
            if not ok:
                res = E5MessageBox.yesNo(
                    self.__ui,
                    self.tr("Commit Changes"),
                    self.tr(
                        """The commit affects files, that have unsaved"""
                        """ changes. Shall the commit be continued?"""),
                    icon=E5MessageBox.Warning)
                if not res:
                    return
        
        if self.__commitDialog is not None:
            msg = self.__commitDialog.logMessage()
            amend = self.__commitDialog.amend()
            resetAuthor = self.__commitDialog.resetAuthor()
            commitAll = not self.__commitDialog.stagedOnly()
            self.__commitDialog.deleteLater()
            self.__commitDialog = None
        else:
            amend = False
            resetAuthor = False
        
        if not msg and not amend:
            msg = '***'
        
        args = self.initCommand("commit")
        if amend:
            args.append("--amend")
        if resetAuthor:
            args.append("--reset-author")
        if msg:
            args.append("--message")
            args.append(msg)
        
        if isinstance(name, list):
            dname, fnames = self.splitPathList(name)
        else:
            dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        if isinstance(name, list):
            args.append("--")
            self.addArguments(args, fnames)
        else:
            if dname != repodir or fname != ".":
                args.append("--")
                args.append(fname)
            else:
                if commitAll:
                    args.append("--all")
        
        if noDialog:
            self.startSynchronizedProcess(QProcess(), "git", args, dname)
        else:
            dia = GitDialog(
                self.tr('Committing changes to Git repository'),
                self)
            res = dia.startProcess(args, dname)
            if res:
                dia.exec()
        self.committed.emit()
        self.checkVCSStatus()
    
    def vcsUpdate(self, name, noDialog=False, revision=None):
        """
        Public method used to update a file/directory with the Git
        repository.
        
        @param name file/directory name to be updated (string or list of
            strings)
        @param noDialog flag indicating quiet operations (boolean)
        @param revision revision to update to (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        args = self.initCommand("checkout")
        if revision:
            res = E5MessageBox.yesNo(
                None,
                self.tr("Switch"),
                self.tr("""<p>Do you really want to switch to <b>{0}</b>?"""
                        """</p>""").format(revision),
                yesDefault=True)
            if not res:
                return False
            args.append(revision)
        
        if isinstance(name, list):
            args.append("--")
            dname, fnames = self.splitPathList(name)
            self.addArguments(args, fnames)
        else:
            dname, fname = self.splitPath(name)
            if fname != ".":
                args.append("--")
                args.append(fname)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        if noDialog:
            self.startSynchronizedProcess(QProcess(), 'git', args, repodir)
            res = False
        else:
            dia = GitDialog(self.tr(
                'Synchronizing with the Git repository'),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def vcsAdd(self, name, isDir=False, noDialog=False):
        """
        Public method used to add a file/directory to the Git repository.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        @param noDialog flag indicating quiet operations
        """
        args = self.initCommand("add")
        args.append("-v")
        
        if isinstance(name, list):
            if isDir:
                dname, fname = os.path.split(name[0])
            else:
                dname, fnames = self.splitPathList(name)
        else:
            if isDir:
                dname, fname = os.path.split(name)
            else:
                dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        if noDialog:
            self.startSynchronizedProcess(QProcess(), 'git', args, repodir)
        else:
            dia = GitDialog(
                self.tr(
                    'Adding files/directories to the Git repository'),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def vcsAddBinary(self, name, isDir=False):
        """
        Public method used to add a file/directory in binary mode to the
        Git repository.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        """
        self.vcsAdd(name, isDir)
    
    def vcsAddTree(self, path):
        """
        Public method to add a directory tree rooted at path to the Git
        repository.
        
        @param path root directory of the tree to be added (string or list of
            strings))
        """
        self.vcsAdd(path, isDir=False)
    
    def vcsRemove(self, name, project=False, noDialog=False, stageOnly=False):
        """
        Public method used to remove a file/directory from the Git
        repository.
        
        The default operation is to remove the local copy as well.
        
        @param name file/directory name to be removed (string or list of
            strings))
        @param project flag indicating deletion of a project tree (boolean)
            (not needed)
        @param noDialog flag indicating quiet operations (boolean)
        @param stageOnly flag indicating to just remove the file from the
            staging area (boolean)
        @return flag indicating successful operation (boolean)
        """
        args = self.initCommand("rm")
        if noDialog and '--force' not in args:
            args.append('--force')
        if stageOnly:
            args.append('--cached')
        
        if isinstance(name, list):
            if os.path.isdir(name[0]):
                args.append("-r")
            dname, fnames = self.splitPathList(name)
            args.append("--")
            self.addArguments(args, name)
        else:
            if os.path.isdir(name):
                args.append("-r")
            dname, fname = self.splitPath(name)
            args.append("--")
            args.append(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        if noDialog:
            res = self.startSynchronizedProcess(
                QProcess(), 'git', args, repodir)
        else:
            dia = GitDialog(
                self.tr(
                    'Removing files/directories from the Git'
                    ' repository'),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.normalExitWithoutErrors()
        
        return res
    
    def vcsMove(self, name, project, target=None, noDialog=False):
        """
        Public method used to move a file/directory.
        
        @param name file/directory name to be moved (string)
        @param project reference to the project object
        @param target new name of the file/directory (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating successful operation (boolean)
        """
        isDir = os.path.isdir(name)
        
        res = False
        if noDialog:
            if target is None:
                return False
            force = True
            accepted = True
        else:
            from .GitCopyDialog import GitCopyDialog
            dlg = GitCopyDialog(name, None, True)
            accepted = dlg.exec() == QDialog.DialogCode.Accepted
            if accepted:
                target, force = dlg.getData()
        
        if accepted:
            args = self.initCommand("mv")
            args.append("-v")
            if force:
                args.append('--force')
            args.append(name)
            args.append(target)
            
            dname, fname = self.splitPath(name)
            # find the root of the repo
            repodir = dname
            while not os.path.isdir(os.path.join(repodir, self.adminDir)):
                repodir = os.path.dirname(repodir)
                if os.path.splitdrive(repodir)[1] == os.sep:
                    return False
            
            if noDialog:
                res = self.startSynchronizedProcess(
                    QProcess(), 'git', args, repodir)
            else:
                dia = GitDialog(self.tr('Renaming {0}').format(name), self)
                res = dia.startProcess(args, repodir)
                if res:
                    dia.exec()
                    res = dia.normalExit()
            if res:
                if target.startswith(project.getProjectPath()):
                    if isDir:
                        project.moveDirectory(name, target)
                    else:
                        project.renameFileInPdata(name, target)
                else:
                    if isDir:
                        project.removeDirectory(name)
                    else:
                        project.removeFile(name)
        return res
    
    def vcsLogBrowser(self, name, isFile=False):
        """
        Public method used to browse the log of a file/directory from the
        Git repository.
        
        @param name file/directory name to show the log of (string)
        @param isFile flag indicating log for a file is to be shown
            (boolean)
        """
        if self.logBrowser is None:
            from .GitLogBrowserDialog import GitLogBrowserDialog
            self.logBrowser = GitLogBrowserDialog(self)
        self.logBrowser.show()
        self.logBrowser.raise_()
        self.logBrowser.start(name, isFile=isFile)
    
    def gitReflogBrowser(self, projectDir):
        """
        Public method used to browse the reflog of the project.
        
        @param projectDir name of the project directory (string)
        """
        if self.reflogBrowser is None:
            from .GitReflogBrowserDialog import GitReflogBrowserDialog
            self.reflogBrowser = GitReflogBrowserDialog(self)
        self.reflogBrowser.show()
        self.reflogBrowser.raise_()
        self.reflogBrowser.start(projectDir)
    
    def vcsDiff(self, name):
        """
        Public method used to view the difference of a file/directory to the
        Git repository.
        
        If name is a directory and is the project directory, all project files
        are saved first. If name is a file (or list of files), which is/are
        being edited and has unsaved modification, they can be saved or the
        operation may be aborted.
        
        @param name file/directory name to be diffed (string)
        """
        if isinstance(name, list):
            names = name[:]
        else:
            names = [name]
        for nam in names:
            if os.path.isfile(nam):
                editor = e5App().getObject("ViewManager").getOpenEditor(nam)
                if editor and not editor.checkDirty():
                    return
            else:
                project = e5App().getObject("Project")
                if nam == project.ppath and not project.saveAllScripts():
                    return
        if self.diff is None:
            from .GitDiffDialog import GitDiffDialog
            self.diff = GitDiffDialog(self)
        self.diff.show()
        self.diff.raise_()
        QApplication.processEvents()
        self.diff.start(name, diffMode="work2stage2repo", refreshable=True)
    
    def vcsStatus(self, name):
        """
        Public method used to view the status of files/directories in the
        Git repository.
        
        @param name file/directory name(s) to show the status of
            (string or list of strings)
        """
        if self.status is None:
            from .GitStatusDialog import GitStatusDialog
            self.status = GitStatusDialog(self)
        self.status.show()
        self.status.raise_()
        self.status.start(name)
    
    def gitUnstage(self, name):
        """
        Public method used to unstage a file/directory.
        
        @param name file/directory name to be reverted (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        if isinstance(name, list):
            dname, fnames = self.splitPathList(name)
        else:
            dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        args = self.initCommand("reset")
        args.append("HEAD")
        args.append("--")
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        dia = GitDialog(
            self.tr('Unstage files/directories'),
            self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        
        return res
    
    def gitRevert(self, name):
        """
        Public method used to revert changes made to a file/directory.
        
        @param name file/directory name to be reverted (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        args = self.initCommand("checkout")
        args.append("--")
        if isinstance(name, list):
            dname, fnames = self.splitPathList(name)
            self.addArguments(args, name)
            names = name[:]
        else:
            dname, fname = self.splitPath(name)
            args.append(name)
            names = [name]
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        project = e5App().getObject("Project")
        names = [project.getRelativePath(nam) for nam in names]
        if names[0]:
            from UI.DeleteFilesConfirmationDialog import (
                DeleteFilesConfirmationDialog
            )
            dlg = DeleteFilesConfirmationDialog(
                self.parent(),
                self.tr("Revert changes"),
                self.tr(
                    "Do you really want to revert all changes to these files"
                    " or directories?"),
                names)
            yes = dlg.exec() == QDialog.DialogCode.Accepted
        else:
            yes = E5MessageBox.yesNo(
                None,
                self.tr("Revert changes"),
                self.tr("""Do you really want to revert all changes of"""
                        """ the project?"""))
        if yes:
            dia = GitDialog(self.tr('Reverting changes'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        else:
            res = False
        
        return res
    
    def vcsMerge(self, name):
        """
        Public method used to merge a URL/revision into the local project.
        
        @param name file/directory name to be merged (string)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitMergeDialog import GitMergeDialog
        dlg = GitMergeDialog(self.gitGetTagsList(repodir),
                             self.gitGetBranchesList(repodir, withMaster=True),
                             self.gitGetCurrentBranch(repodir),
                             self.gitGetBranchesList(repodir, remotes=True))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            commit, doCommit, commitMessage, addLog, diffStat = (
                dlg.getParameters()
            )
            args = self.initCommand("merge")
            if doCommit:
                args.append("--commit")
                args.append("-m")
                args.append(commitMessage)
                if addLog:
                    args.append("--log")
                else:
                    args.append("--no-log")
            else:
                args.append("--no-commit")
            if diffStat:
                args.append("--stat")
            else:
                args.append("--no-stat")
            if commit:
                args.append(commit)
            
            dia = GitDialog(self.tr('Merging').format(name), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
            self.checkVCSStatus()
    
    def vcsSwitch(self, name):
        """
        Public method used to switch a working directory to a different
        revision.
        
        @param name directory name to be switched (string)
        @return flag indicating, that the switch contained an add
            or delete (boolean)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        from .GitRevisionSelectionDialog import GitRevisionSelectionDialog
        dlg = GitRevisionSelectionDialog(
            self.gitGetTagsList(repodir),
            self.gitGetBranchesList(repodir),
            trackingBranchesList=self.gitGetBranchesList(
                repodir, remotes=True),
            noneLabel=self.tr("Master branch head"))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            rev = dlg.getRevision()
            return self.vcsUpdate(name, revision=rev)
        
        return False

    def vcsRegisteredState(self, name):
        """
        Public method used to get the registered state of a file in the vcs.
        
        @param name filename to check (string)
        @return a combination of canBeCommited and canBeAdded
        """
        if name.endswith(os.sep):
            name = name[:-1]
        name = os.path.normcase(name)
        dname, fname = self.splitPath(name)
        
        if fname == '.' and os.path.isdir(os.path.join(dname, self.adminDir)):
            return self.canBeCommitted
        
        if name in self.statusCache:
            return self.statusCache[name]
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return 0
        
        args = self.initCommand("status")
        args.append('--porcelain')
        args.append(name)
        
        ioEncoding = Preferences.getSystem("IOEncoding")
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             ioEncoding, 'replace')
        
        if output:
            for line in output.splitlines():
                if line and line[0] in " MADRCU!?":
                    flag = line[1]
                    path = line[3:].split(" -> ")[-1]
                    absname = os.path.join(repodir, os.path.normcase(path))
                    if absname.endswith(("/", "\\")):
                        absname = absname[:-1]
                    if flag not in "?!":
                        if fname == '.':
                            if absname.startswith(dname + os.path.sep):
                                return self.canBeCommitted
                            if absname == dname:
                                return self.canBeCommitted
                        else:
                            if absname == name:
                                return self.canBeCommitted
        else:
            return self.canBeCommitted
        
        return self.canBeAdded
    
    def vcsAllRegisteredStates(self, names, dname, shortcut=True):
        """
        Public method used to get the registered states of a number of files
        in the vcs.
        
        <b>Note:</b> If a shortcut is to be taken, the code will only check,
        if the named directory has been scanned already. If so, it is assumed,
        that the states for all files have been populated by the previous run.
        
        @param names dictionary with all filenames to be checked as keys
        @param dname directory to check in (string)
        @param shortcut flag indicating a shortcut should be taken (boolean)
        @return the received dictionary completed with a combination of
            canBeCommited and canBeAdded or None in order to signal an error
        """
        if dname.endswith(os.sep):
            dname = dname[:-1]
        dname = os.path.normcase(dname)
        
        # revert the logic because git status doesn't show unchanged files
        for name in names:
            names[name] = self.canBeCommitted
        
        found = False
        for name in self.statusCache:
            if name in names:
                found = True
                names[name] = self.statusCache[name]
        
        if not found:
            # find the root of the repo
            repodir = dname
            while not os.path.isdir(os.path.join(repodir, self.adminDir)):
                repodir = os.path.dirname(repodir)
                if os.path.splitdrive(repodir)[1] == os.sep:
                    return names
        
            args = self.initCommand("status")
            args.append('--porcelain')
            
            ioEncoding = Preferences.getSystem("IOEncoding")
            output = ""
            process = QProcess()
            process.setWorkingDirectory(dname)
            process.start('git', args)
            procStarted = process.waitForStarted(5000)
            if procStarted:
                finished = process.waitForFinished(30000)
                if finished and process.exitCode() == 0:
                    output = str(process.readAllStandardOutput(),
                                 ioEncoding, 'replace')
            
            if output:
                for line in output.splitlines():
                    if line and line[0] in " MADRCU!?":
                        flag = line[1]
                        path = line[3:].split(" -> ")[-1]
                        name = os.path.normcase(os.path.join(repodir, path))
                        dirName = os.path.dirname(name)
                        if name.startswith(dname):
                            if flag in "?!":
                                isDir = name.endswith(("/", "\\"))
                                if isDir:
                                    name = name[:-1]
                                if name in names:
                                    names[name] = self.canBeAdded
                                if isDir:
                                    # it's a directory
                                    for nname in names:
                                        if nname.startswith(name):
                                            names[nname] = self.canBeAdded
                        if flag not in "?!":
                            self.statusCache[name] = self.canBeCommitted
                            self.statusCache[dirName] = self.canBeCommitted
                        else:
                            self.statusCache[name] = self.canBeAdded
                            if dirName not in self.statusCache:
                                self.statusCache[dirName] = self.canBeAdded
        
        return names
    
    def clearStatusCache(self):
        """
        Public method to clear the status cache.
        """
        self.statusCache = {}
    
    def vcsName(self):
        """
        Public method returning the name of the vcs.
        
        @return always 'Git' (string)
        """
        return "Git"
    
    def vcsInitConfig(self, project):
        """
        Public method to initialize the VCS configuration.
        
        This method ensures, that an ignore file exists.
        
        @param project reference to the project (Project)
        """
        ppath = project.getProjectPath()
        if ppath:
            ignoreName = os.path.join(ppath, Git.IgnoreFileName)
            if not os.path.exists(ignoreName):
                self.gitCreateIgnoreFile(project.getProjectPath(),
                                         autoAdd=True)
    
    def vcsCleanup(self, name):
        """
        Public method used to cleanup the working directory.
        
        @param name directory name to be cleaned up (string)
        """
        patterns = self.__plugin.getPreferences("CleanupPatterns").split()
        
        entries = []
        for pat in patterns:
            entries.extend(Utilities.direntries(name, True, pat))
        
        for entry in entries:
            try:
                os.remove(entry)
            except OSError:
                pass
    
    def vcsCommandLine(self, name):
        """
        Public method used to execute arbitrary Git commands.
        
        @param name directory name of the working directory (string)
        """
        from .GitCommandDialog import GitCommandDialog
        dlg = GitCommandDialog(self.commandHistory, name)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            command = dlg.getData()
            commandList = Utilities.parseOptionString(command)
            
            # This moves any previous occurrence of these arguments to the head
            # of the list.
            if command in self.commandHistory:
                self.commandHistory.remove(command)
            self.commandHistory.insert(0, command)
            
            args = []
            self.addArguments(args, commandList)
            
            # find the root of the repo
            repodir = name
            while not os.path.isdir(os.path.join(repodir, self.adminDir)):
                repodir = os.path.dirname(repodir)
                if os.path.splitdrive(repodir)[1] == os.sep:
                    return
            
            dia = GitDialog(self.tr('Git Command'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def vcsOptionsDialog(self, project, archive, editable=False, parent=None):
        """
        Public method to get a dialog to enter repository info.
        
        @param project reference to the project object
        @param archive name of the project in the repository (string)
        @param editable flag indicating that the project name is editable
            (boolean)
        @param parent parent widget (QWidget)
        @return reference to the instantiated options dialog (GitOptionsDialog)
        """
        from .GitOptionsDialog import GitOptionsDialog
        return GitOptionsDialog(self, project, parent)
    
    def vcsNewProjectOptionsDialog(self, parent=None):
        """
        Public method to get a dialog to enter repository info for getting a
        new project.
        
        @param parent parent widget (QWidget)
        @return reference to the instantiated options dialog
            (GitNewProjectOptionsDialog)
        """
        from .GitNewProjectOptionsDialog import GitNewProjectOptionsDialog
        return GitNewProjectOptionsDialog(self, parent)
    
    def vcsRepositoryInfos(self, ppath):
        """
        Public method to retrieve information about the repository.
        
        @param ppath local path to get the repository infos (string)
        @return string with ready formated info for display (string)
        """
        formatTemplate = (
            'format:'
            '%h%n'
            '%p%n'
            '%an%n'
            '%ae%n'
            '%ai%n'
            '%cn%n'
            '%ce%n'
            '%ci%n'
            '%d%n'
            '%s')
        
        args = self.initCommand("show")
        args.append("--abbrev-commit")
        args.append("--abbrev={0}".format(
            self.__plugin.getPreferences("CommitIdLength")))
        args.append("--format={0}".format(formatTemplate))
        args.append("--no-patch")
        args.append("HEAD")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(ppath)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        if output:
            info = []
            (commit, parents, author, authorMail, authorDate,
             committer, committerMail, committerDate, refs, subject) = (
                output.splitlines()
            )
            tags = []
            branches = []
            for name in refs.strip()[1:-1].split(","):
                name = name.strip()
                if name:
                    if name.startswith("tag: "):
                        tags.append(name.split()[1])
                    elif name != "HEAD":
                        branches.append(name)
            
            info.append(self.tr(
                "<tr><td><b>Commit</b></td><td>{0}</td></tr>").format(
                commit))
            if parents:
                info.append(self.tr(
                    "<tr><td><b>Parents</b></td><td>{0}</td></tr>").format(
                    '<br/>'.join(parents.strip().split())))
            if tags:
                info.append(self.tr(
                    "<tr><td><b>Tags</b></td><td>{0}</td></tr>").format(
                    '<br/>'.join(tags)))
            if branches:
                info.append(self.tr(
                    "<tr><td><b>Branches</b></td><td>{0}</td></tr>").format(
                    '<br/>'.join(branches)))
            info.append(self.tr(
                "<tr><td><b>Author</b></td><td>{0} &lt;{1}&gt;</td></tr>")
                .format(author, authorMail))
            info.append(self.tr(
                "<tr><td><b>Date</b></td><td>{0}</td></tr>").format(
                authorDate.rsplit(":", 1)[0]))
            info.append(self.tr(
                "<tr><td><b>Committer</b></td><td>{0} &lt;{1}&gt;</td></tr>")
                .format(committer, committerMail))
            info.append(self.tr(
                "<tr><td><b>Committed Date</b></td><td>{0}</td></tr>").format(
                committerDate.rsplit(":", 1)[0]))
            info.append(self.tr(
                "<tr><td><b>Subject</b></td><td>{0}</td></tr>").format(
                subject))
            infoStr = "\n".join(info)
        else:
            infoStr = ""
        
        return self.tr(
            """<h3>Repository information</h3>\n"""
            """<p><table>\n"""
            """<tr><td><b>Git V.</b></td><td>{0}</td></tr>\n"""
            """<tr></tr>\n"""
            """{1}"""
            """</table></p>\n"""
        ).format(self.versionStr, infoStr)
    
    def vcsSupportCommandOptions(self):
        """
        Public method to signal the support of user settable command options.
        
        @return flag indicating the support  of user settable command options
            (boolean)
        """
        return False
    
    ###########################################################################
    ## Git specific methods are below.
    ###########################################################################
    
    def gitNormalizeURL(self, url):
        """
        Public method to normalize a url for Git.
        
        @param url url string (string)
        @return properly normalized url for git (string)
        """
        url = url.replace('\\', '/')
        if url.endswith('/'):
            url = url[:-1]
        urll = url.split('//')
        if len(urll) > 1:
            url = "{0}//{1}".format(urll[0], '/'.join(urll[1:]))
        
        return url
    
    def gitCreateIgnoreFile(self, name, autoAdd=False):
        """
        Public method to create the ignore file.
        
        @param name directory name to create the ignore file in (string)
        @param autoAdd flag indicating to add it automatically (boolean)
        @return flag indicating success
        """
        status = False
        ignorePatterns = [
            ".eric6project/",
            ".ropeproject/",
            ".directory/",
            "*.pyc",
            "*.pyo",
            "*.orig",
            "*.bak",
            "*.rej",
            "*~",
            "cur/",
            "tmp/",
            "__pycache__/",
            "*.DS_Store",
        ]
        
        ignoreName = os.path.join(name, Git.IgnoreFileName)
        if os.path.exists(ignoreName):
            res = E5MessageBox.yesNo(
                self.__ui,
                self.tr("Create {0} file").format(ignoreName),
                self.tr("""<p>The file <b>{0}</b> exists already."""
                        """ Overwrite it?</p>""").format(ignoreName),
                icon=E5MessageBox.Warning)
        else:
            res = True
        if res:
            try:
                # create a .gitignore file
                with open(ignoreName, "w") as ignore:
                    ignore.write("\n".join(ignorePatterns))
                    ignore.write("\n")
                status = True
            except OSError:
                status = False
            
            if status and autoAdd:
                self.vcsAdd(ignoreName, noDialog=True)
                project = e5App().getObject("Project")
                project.appendFile(ignoreName)
        
        return status
    
    def gitCopy(self, name, project):
        """
        Public method used to copy a file/directory.
        
        @param name file/directory name to be copied (string)
        @param project reference to the project object
        @return flag indicating successful operation (boolean)
        """
        from .GitCopyDialog import GitCopyDialog
        dlg = GitCopyDialog(name)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            target, force = dlg.getData()
            
            # step 1: copy the file/directory:
            if os.path.isdir(name):
                try:
                    shutil.copytree(name, target)
                except (OSError, shutil.Error) as why:
                    E5MessageBox.critical(
                        self,
                        self.tr("Git Copy"),
                        self.tr("""<p>Copying the directory <b>{0}</b>"""
                                """ failed.</p><p>Reason: {1}</p>""").format(
                            name, str(why)))
                    return False
                self.vcsAdd(target, isDir=True)
                if target.startswith(project.getProjectPath()):
                    project.copyDirectory(name, target)

            else:
                try:
                    shutil.copy2(name, target)
                except (OSError, shutil.Error) as why:
                    E5MessageBox.critical(
                        self,
                        self.tr("Git Copy"),
                        self.tr("""<p>Copying the file <b>{0}</b>"""
                                """ failed.</p><p>Reason: {1}</p>""").format(
                            name, str(why)))
                    return False
                self.vcsAdd(target, isDir=False)
                if target.startswith(project.getProjectPath()):
                    project.appendFile(target)
            self.checkVCSStatus()
        return True
    
    def gitBlame(self, name):
        """
        Public method to show the output of the git blame command.
        
        @param name file name to show the annotations for (string)
        """
        if self.blame is None:
            from .GitBlameDialog import GitBlameDialog
            self.blame = GitBlameDialog(self)
        self.blame.show()
        self.blame.raise_()
        self.blame.start(name)
    
    def gitExtendedDiff(self, name):
        """
        Public method used to view the difference of a file/directory to the
        Git repository.
        
        If name is a directory and is the project directory, all project files
        are saved first. If name is a file (or list of files), which is/are
        being edited and has unsaved modification, they can be saved or the
        operation may be aborted.
        
        This method gives the chance to enter the revisions to be compared.
        
        @param name file/directory name to be diffed (string)
        """
        if isinstance(name, list):
            dname, fnames = self.splitPathList(name)
            names = name[:]
        else:
            dname, fname = self.splitPath(name)
            names = [name]
        for nam in names:
            if os.path.isfile(nam):
                editor = e5App().getObject("ViewManager").getOpenEditor(nam)
                if editor and not editor.checkDirty():
                    return
            else:
                project = e5App().getObject("Project")
                if nam == project.ppath and not project.saveAllScripts():
                    return
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitRevisionsSelectionDialog import GitRevisionsSelectionDialog
        dlg = GitRevisionsSelectionDialog(self.gitGetTagsList(repodir),
                                          self.gitGetBranchesList(repodir))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            revisions = dlg.getRevisions()
            if self.diff is None:
                from .GitDiffDialog import GitDiffDialog
                self.diff = GitDiffDialog(self)
            self.diff.show()
            self.diff.raise_()
            self.diff.start(name, revisions)
    
    def __gitGetFileForRevision(self, name, rev=""):
        """
        Private method to get a file for a specific revision from the
        repository.
        
        @param name file name to get from the repository (string)
        @param rev revision to retrieve (string)
        @return contents of the file (string) and an error message (string)
        """
        # find the root of the repo
        repodir = self.splitPath(name)[0]
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        args = self.initCommand("cat-file")
        args.append("blob")
        args.append("{0}:{1}".format(rev, name.replace(repodir + os.sep, "")))
        
        output = ""
        error = ""
        
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished:
                if process.exitCode() == 0:
                    output = str(process.readAllStandardOutput(),
                                 Preferences.getSystem("IOEncoding"),
                                 'replace')
                else:
                    error = str(process.readAllStandardError(),
                                Preferences.getSystem("IOEncoding"),
                                'replace')
            else:
                error = self.tr(
                    "The git process did not finish within 30s.")
        else:
            error = self.tr(
                'The process {0} could not be started. '
                'Ensure, that it is in the search path.').format('git')
        
        # return file contents with 'universal newlines'
        return output.replace('\r\n', '\n').replace('\r', '\n'), error
    
    def gitSbsDiff(self, name, extended=False, revisions=None):
        """
        Public method used to view the difference of a file to the Git
        repository side-by-side.
        
        @param name file name to be diffed (string)
        @param extended flag indicating the extended variant (boolean)
        @param revisions tuple of two revisions (tuple of strings)
        @exception ValueError raised to indicate an invalid name parameter
        """
        if isinstance(name, list):
            raise ValueError("Wrong parameter type")
        
        if extended:
            # find the root of the repo
            repodir = self.splitPath(name)[0]
            while not os.path.isdir(os.path.join(repodir, self.adminDir)):
                repodir = os.path.dirname(repodir)
                if os.path.splitdrive(repodir)[1] == os.sep:
                    return
            
            from .GitRevisionsSelectionDialog import (
                GitRevisionsSelectionDialog
            )
            dlg = GitRevisionsSelectionDialog(self.gitGetTagsList(repodir),
                                              self.gitGetBranchesList(repodir))
            if dlg.exec() == QDialog.DialogCode.Accepted:
                rev1, rev2 = dlg.getRevisions()
        elif revisions:
            rev1, rev2 = revisions[0], revisions[1]
        else:
            rev1, rev2 = "", ""
        
        output1, error = self.__gitGetFileForRevision(name, rev=rev1)
        if error:
            E5MessageBox.critical(
                self.__ui,
                self.tr("Git Side-by-Side Difference"),
                error)
            return
        name1 = "{0} (rev. {1})".format(name, rev1 and rev1 or "Stage")
        
        if rev2:
            if rev2 == "Stage":
                rev2 = ""
            output2, error = self.__gitGetFileForRevision(name, rev=rev2)
            if error:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Git Side-by-Side Difference"),
                    error)
                return
            name2 = "{0} (rev. {1})".format(name, rev2)
        else:
            try:
                with open(name, "r", encoding="utf-8") as f1:
                    output2 = f1.read()
                    f1.close()
                name2 = "{0} (Work)".format(name)
            except OSError:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Git Side-by-Side Difference"),
                    self.tr(
                        """<p>The file <b>{0}</b> could not be read.</p>""")
                    .format(name))
                return
        
        if self.sbsDiff is None:
            from UI.CompareDialog import CompareDialog
            self.sbsDiff = CompareDialog()
        self.sbsDiff.show()
        self.sbsDiff.raise_()
        self.sbsDiff.compare(output1, output2, name1, name2)
    
    def gitFetch(self, name):
        """
        Public method to fetch changes from a remote repository.
        
        @param name directory name (string)
        """
        # find the root of the repo
        repodir = self.splitPath(name)[0]
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitFetchDialog import GitFetchDialog
        dlg = GitFetchDialog(self, repodir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (remote, url, remoteBranches, localBranch, fetchAll, prune,
             includeTags) = dlg.getData()
            
            args = self.initCommand("fetch")
            args.append('--verbose')
            if prune:
                args.append('--prune')
            if includeTags:
                args.append("--tags")
            if fetchAll:
                args.append('--all')
            else:
                args.append(remote) if remote else args.append(url)
                if len(remoteBranches) == 1 and localBranch:
                    args.append(remoteBranches[0] + ":" + localBranch)
                else:
                    args.extend(remoteBranches)
        
            dia = GitDialog(self.tr('Fetching from a remote Git repository'),
                            self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
            self.checkVCSStatus()
    
    def gitPull(self, name):
        """
        Public method used to pull changes from a remote Git repository.
        
        @param name directory name of the project to be pulled to (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = self.splitPath(name)[0]
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        from .GitPullDialog import GitPullDialog
        dlg = GitPullDialog(self, repodir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            remote, url, branches, pullAll, prune = dlg.getData()
            
            args = self.initCommand('pull')
            args.append('--no-commit')
            args.append('--verbose')
            if prune:
                args.append('--prune')
            if pullAll:
                args.append('--all')
            else:
                args.append(remote) if remote else args.append(url)
                args.extend(branches)
            
            dia = GitDialog(self.tr('Pulling from a remote Git repository'),
                            self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
            return res
        else:
            return False
    
    def gitPush(self, name):
        """
        Public method used to push changes to a remote Git repository.
        
        @param name directory name of the project to be pushed from (string)
        """
        # find the root of the repo
        repodir = self.splitPath(name)[0]
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitPushDialog import GitPushDialog
        dlg = GitPushDialog(self, repodir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            remote, refspecs, tags, tracking, submodule = dlg.getData()
            
            args = self.initCommand("push")
            args.append('--verbose')
            args.append('--porcelain')
            if tags:
                args.append("--tags")
            if tracking:
                args.append("--set-upstream")
            if submodule:
                args.append("--recurse-submodules={0}".format(submodule))
            args.append(remote)
            args.extend(refspecs)
            
            dia = GitDialog(
                self.tr('Pushing to a remote Git repository'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
            self.checkVCSStatus()
    
    def gitCommitMerge(self, name):
        """
        Public method to commit a failed merge.
        
        @param name file/directory name (string)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        import sys
        editor = sys.argv[0].replace(".py", "_editor.py")
        env = {"GIT_EDITOR": "{0} {1}".format(sys.executable, editor)}
        
        args = self.initCommand("commit")
        
        dia = GitDialog(self.tr('Committing failed merge'), self)
        res = dia.startProcess(args, repodir, environment=env)
        if res:
            dia.exec()
        self.committed.emit()
        self.checkVCSStatus()
    
    def gitCancelMerge(self, name):
        """
        Public method to cancel an uncommitted or failed merge.
        
        @param name file/directory name (string)
        @return flag indicating, that the cancellation contained an add
            or delete (boolean)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        args = self.initCommand("merge")
        args.append("--abort")
        
        dia = GitDialog(
            self.tr('Aborting uncommitted/failed merge'),
            self)
        res = dia.startProcess(args, repodir, False)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def gitApply(self, repodir, patchFile, cached=False, reverse=False,
                 noDialog=False):
        """
        Public method to apply a patch stored in a given file.
        
        @param repodir directory name of the repository (string)
        @param patchFile name of the patch file (string)
        @param cached flag indicating to apply the patch to the staging area
            (boolean)
        @param reverse flag indicating to apply the patch in reverse (boolean)
        @param noDialog flag indicating quiet operations (boolean)
        """
        args = self.initCommand("apply")
        if cached:
            args.append("--index")
            args.append("--cached")
        if reverse:
            args.append("--reverse")
        args.append(patchFile)
        
        if noDialog:
            self.startSynchronizedProcess(QProcess(), "git", args, repodir)
        else:
            dia = GitDialog(
                self.tr('Applying patch'),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitApplyCheckPatches(self, projectDir, check=False):
        """
        Public method to apply a list of patch files or check, if they would
        apply cleanly.
        
        @param projectDir directory name of the project (string)
        @param check flag indicating to perform a check operation (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitPatchFilesDialog import GitPatchFilesDialog
        dlg = GitPatchFilesDialog(repodir, self.__patchCheckData)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            patchFilesList, stripCount, inaccurateEof, recount = dlg.getData()
            if patchFilesList:
                args = self.initCommand("apply")
                if check:
                    args.append("--check")
                    self.__patchCheckData = (
                        patchFilesList, stripCount, inaccurateEof, recount)
                    title = self.tr('Check patch files')
                else:
                    self.__patchCheckData = None
                    title = self.tr('Apply patch files')
                if inaccurateEof:
                    args.append("--inaccurate-eof")
                if recount:
                    args.append("--recount")
                args.append("-p{0}".format(stripCount))
                args.extend(patchFilesList)
                
                dia = GitDialog(
                    title,
                    self)
                res = dia.startProcess(args, repodir)
                if res:
                    dia.exec()
                    if not check:
                        self.checkVCSStatus()
    
    def gitShowPatchesStatistics(self, projectDir):
        """
        Public method to show statistics for a set of patch files.
        
        @param projectDir directory name of the project (string)
        """
        if self.patchStatisticsDialog is None:
            from .GitPatchStatisticsDialog import GitPatchStatisticsDialog
            self.patchStatisticsDialog = GitPatchStatisticsDialog(self)
        self.patchStatisticsDialog.show()
        self.patchStatisticsDialog.raise_()
        self.patchStatisticsDialog.start(projectDir, self.__patchCheckData)
        self.__patchCheckData = self.patchStatisticsDialog.getData()
    
    ###########################################################################
    ## Methods for tag handling.
    ###########################################################################
    
    def vcsTag(self, name, revision=None, tagName=None):
        """
        Public method used to set/remove a tag in the Git repository.
        
        @param name file/directory name to determine the repo root from
            (string)
        @param revision revision to set tag for (string)
        @param tagName name of the tag (string)
        @return flag indicating a performed tag action (boolean)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        from .GitTagDialog import GitTagDialog
        dlg = GitTagDialog(self.gitGetTagsList(repodir), revision, tagName)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            tag, revision, tagOp, tagType, force = dlg.getParameters()
        else:
            return False
        
        args = self.initCommand("tag")
        if tagOp == GitTagDialog.CreateTag:
            msg = "Created tag <{0}>.".format(tag)
            if tagType == GitTagDialog.AnnotatedTag:
                args.append("--annotate")
                args.append("--message={0}".format(msg))
            elif tagType == GitTagDialog.SignedTag:
                args.append("--sign")
                args.append("--message={0}".format(msg))
            if force:
                args.append("--force")
        elif tagOp == GitTagDialog.DeleteTag:
            args.append("--delete")
        elif tagOp == GitTagDialog.VerifyTag:
            args.append("--verify")
        else:
            return False
        args.append(tag)
        if tagOp == GitTagDialog.CreateTag and revision:
            args.append(revision)
        
        dia = GitDialog(self.tr('Tagging in the Git repository'),
                        self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
        
        return True
    
    def gitGetTagsList(self, repodir, withType=False):
        """
        Public method to get the list of tags.
        
        @param repodir directory name of the repository (string)
        @param withType flag indicating to get the tag type as well (boolean)
        @return list of tags (list of string) or list of tuples of
            tag name and flag indicating a local tag (list of tuple of string
            and boolean), if withType is True
        """
        args = self.initCommand("tag")
        args.append('--list')
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        tagsList = []
        if output:
            for line in output.splitlines():
                name = line.strip()
                tagsList.append(name)
        
        return tagsList
    
    def gitListTagBranch(self, path, tags=True, listAll=True, merged=True):
        """
        Public method used to list the available tags or branches.
        
        @param path directory name of the project (string)
        @param tags flag indicating listing of branches or tags
            (False = branches, True = tags)
        @param listAll flag indicating to show all tags or branches (boolean)
        @param merged flag indicating to show only merged or non-merged
            branches (boolean)
        """
        if self.tagbranchList is None:
            from .GitTagBranchListDialog import GitTagBranchListDialog
            self.tagbranchList = GitTagBranchListDialog(self)
        self.tagbranchList.show()
        self.tagbranchList.raise_()
        if tags:
            self.tagbranchList.start(path, tags)
        else:
            self.tagbranchList.start(path, tags, listAll, merged)
    
    ###########################################################################
    ## Methods for branch handling.
    ###########################################################################
    
    def gitGetBranchesList(self, repodir, withMaster=False, allBranches=False,
                           remotes=False):
        """
        Public method to get the list of branches.
        
        @param repodir directory name of the repository (string)
        @param withMaster flag indicating to get 'master' as well (boolean)
        @param allBranches flag indicating to return all branches (boolean)
        @param remotes flag indicating to return remote branches only (boolean)
        @return list of branches (list of string)
        """
        args = self.initCommand("branch")
        args.append('--list')
        if allBranches:
            args.append("--all")
        elif remotes:
            args.append("--remotes")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        branchesList = []
        if output:
            for line in output.splitlines():
                name = line[2:].strip()
                if (
                    (name != "master" or withMaster) and
                    "->" not in name and
                    not name.startswith("(") and
                    not name.endswith(")")
                ):
                    branchesList.append(name)
        
        return branchesList
    
    def gitGetCurrentBranch(self, repodir):
        """
        Public method used to show the current branch of the working directory.
        
        @param repodir directory name of the repository (string)
        @return name of the current branch (string)
        """
        args = self.initCommand("branch")
        args.append('--list')
        
        branchName = ""
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        if output:
            for line in output.splitlines():
                if line.startswith("* "):
                    branchName = line[2:].strip()
                    if branchName.startswith("(") and branchName.endswith(")"):
                        # not a valid branch name, probably detached head
                        branchName = ""
                    break
        
        return branchName
    
    def gitBranch(self, name, revision=None, branchName=None, branchOp=None):
        """
        Public method used to create, delete or move a branch in the Git
        repository.
        
        @param name file/directory name to be branched (string)
        @param revision revision to set tag for (string)
        @param branchName name of the branch (string)
        @param branchOp desired branch operation (integer)
        @return flag indicating a performed branch action (boolean) and
            a flag indicating, that the branch operation contained an add
            or delete (boolean)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False, False
        
        from .GitBranchDialog import GitBranchDialog
        dlg = GitBranchDialog(
            self.gitGetBranchesList(repodir, allBranches=True),
            revision, branchName, branchOp)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            branchOp, branch, revision, newBranch, remoteBranch, force = (
                dlg.getParameters()
            )
        else:
            return False, False
        
        if branchOp in [GitBranchDialog.CreateBranch,
                        GitBranchDialog.DeleteBranch,
                        GitBranchDialog.RenameBranch,
                        GitBranchDialog.SetTrackingBranch,
                        GitBranchDialog.UnsetTrackingBranch]:
            args = self.initCommand("branch")
            if branchOp == GitBranchDialog.CreateBranch:
                if force:
                    args.append("--force")
                args.append(branch)
                if revision:
                    args.append(revision)
            elif branchOp == GitBranchDialog.DeleteBranch:
                if force:
                    args.append("-D")
                else:
                    args.append("-d")
                args.append(branch)
            elif branchOp == GitBranchDialog.RenameBranch:
                if force:
                    args.append("-M")
                else:
                    args.append("-m")
                args.append(branch)
                args.append(newBranch)
            elif branchOp == GitBranchDialog.SetTrackingBranch:
                args.append("--set-upstream-to={0}".format(remoteBranch))
                if branch:
                    args.append(branch)
            elif branchOp == GitBranchDialog.UnsetTrackingBranch:
                args.append("--unset-upstream")
                if branch:
                    args.append(branch)
        elif branchOp in [GitBranchDialog.CreateSwitchBranch,
                          GitBranchDialog.CreateTrackingBranch]:
            args = self.initCommand("checkout")
            if branchOp == GitBranchDialog.CreateSwitchBranch:
                if force:
                    args.append("-B")
                else:
                    args.append("-b")
                args.append(branch)
                if revision:
                    args.append(revision)
            elif branchOp == GitBranchDialog.CreateTrackingBranch:
                args.append("--track")
                args.append(branch)
        else:
            return False, False
        
        dia = GitDialog(self.tr('Branching in the Git repository'),
                        self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            if branchOp in [GitBranchDialog.CreateSwitchBranch,
                            GitBranchDialog.CreateTrackingBranch]:
                update = dia.hasAddOrDelete()
                self.checkVCSStatus()
            else:
                update = False
        
        return True, update
    
    def gitDeleteRemoteBranch(self, name):
        """
        Public method to delete a branch from a remote repository.
        
        @param name file/directory name (string)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitBranchPushDialog import GitBranchPushDialog
        dlg = GitBranchPushDialog(self.gitGetBranchesList(repodir),
                                  self.gitGetRemotesList(repodir),
                                  delete=True)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            branchName, remoteName = dlg.getData()[:2]
            
            args = self.initCommand("push")
            args.append(remoteName)
            args.append(":{0}".format(branchName))
            
            dia = GitDialog(self.tr('Delete Remote Branch'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitShowBranch(self, name):
        """
        Public method used to show the current branch of the working directory.
        
        @param name file/directory name (string)
        """
        dname, fname = self.splitPath(name)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        branchName = self.gitGetCurrentBranch(repodir)
        E5MessageBox.information(
            None,
            self.tr("Current Branch"),
            self.tr("""<p>The current branch is <b>{0}</b>."""
                    """</p>""").format(branchName))
    
    ###########################################################################
    ## Methods for bundles handling.
    ###########################################################################
    
    def gitBundle(self, projectDir):
        """
        Public method to create a bundle file.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitBundleDialog import GitBundleDialog
        dlg = GitBundleDialog(self.gitGetTagsList(repodir),
                              self.gitGetBranchesList(repodir))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            revs = dlg.getData()
            
            fname, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
                None,
                self.tr("Create Bundle"),
                self.__lastBundlePath or repodir,
                self.tr("Git Bundle Files (*.bundle)"),
                None,
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
            
            if not fname:
                return  # user aborted
            
            ext = QFileInfo(fname).suffix()
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fname += ex
            if QFileInfo(fname).exists():
                res = E5MessageBox.yesNo(
                    self.__ui,
                    self.tr("Create Bundle"),
                    self.tr("<p>The Git bundle file <b>{0}</b> "
                            "already exists. Overwrite it?</p>")
                        .format(fname),
                    icon=E5MessageBox.Warning)
                if not res:
                    return
            fname = Utilities.toNativeSeparators(fname)
            self.__lastBundlePath = os.path.dirname(fname)
            
            args = self.initCommand("bundle")
            args.append("create")
            args.append(fname)
            for rev in revs:
                args.append(rev)
            
            dia = GitDialog(self.tr('Create Bundle'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitVerifyBundle(self, projectDir):
        """
        Public method to verify a bundle file.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        fname = E5FileDialog.getOpenFileName(
            None,
            self.tr("Verify Bundle"),
            self.__lastBundlePath or repodir,
            self.tr("Git Bundle Files (*.bundle);;All Files (*)"))
        if fname:
            self.__lastBundlePath = os.path.dirname(fname)
            
            args = self.initCommand("bundle")
            args.append("verify")
            args.append(fname)
            
            dia = GitDialog(self.tr('Verify Bundle'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitBundleListHeads(self, projectDir):
        """
        Public method to list the heads contained in a bundle file.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        fname = E5FileDialog.getOpenFileName(
            None,
            self.tr("List Bundle Heads"),
            self.__lastBundlePath or repodir,
            self.tr("Git Bundle Files (*.bundle);;All Files (*)"))
        if fname:
            self.__lastBundlePath = os.path.dirname(fname)
            
            args = self.initCommand("bundle")
            args.append("list-heads")
            args.append(fname)
            
            dia = GitDialog(self.tr('List Bundle Heads'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitGetBundleHeads(self, repodir, bundleFile):
        """
        Public method to get a list of heads contained in a bundle file.
        
        @param repodir directory name of the repository (string)
        @param bundleFile file name of a git bundle file (string)
        @return list of heads (list of strings)
        """
        args = self.initCommand("bundle")
        args.append("list-heads")
        args.append(bundleFile)
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        heads = []
        if output:
            for line in output.splitlines():
                head = line.strip().split(None, 1)[1]  # commit id, head
                heads.append(head.replace("refs/heads/", ""))
        
        return heads
    
    def gitBundleFetch(self, projectDir):
        """
        Public method to fetch a head of a bundle file into the local
        repository.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        fname = E5FileDialog.getOpenFileName(
            None,
            self.tr("Apply Bundle"),
            self.__lastBundlePath or repodir,
            self.tr("Git Bundle Files (*.bundle);;All Files (*)"))
        if fname:
            self.__lastBundlePath = os.path.dirname(fname)
            
            from .GitApplyBundleDataDialog import GitApplyBundleDataDialog
            dlg = GitApplyBundleDataDialog(
                self.gitGetBundleHeads(repodir, fname),
                self.gitGetBranchesList(repodir))
            if dlg.exec() == QDialog.DialogCode.Accepted:
                bundleHead, branch = dlg.getData()
                
                args = self.initCommand("fetch")
                args.append('--verbose')
                args.append(fname)
                if branch:
                    args.append(bundleHead + ":" + branch)
                else:
                    args.append(bundleHead)
                
                dia = GitDialog(self.tr('Applying a bundle file (fetch)'),
                                self)
                res = dia.startProcess(args, repodir)
                if res:
                    dia.exec()
                    res = dia.hasAddOrDelete()
                self.checkVCSStatus()
    
    def gitBundlePull(self, projectDir):
        """
        Public method to pull a head of a bundle file into the local
        repository and working area.
        
        @param projectDir name of the project directory (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        res = False
        fname = E5FileDialog.getOpenFileName(
            None,
            self.tr("Apply Bundle"),
            self.__lastBundlePath or repodir,
            self.tr("Git Bundle Files (*.bundle);;All Files (*)"))
        if fname:
            self.__lastBundlePath = os.path.dirname(fname)
            
            from .GitApplyBundleDataDialog import GitApplyBundleDataDialog
            dlg = GitApplyBundleDataDialog(
                self.gitGetBundleHeads(repodir, fname),
                self.gitGetBranchesList(repodir))
            if dlg.exec() == QDialog.DialogCode.Accepted:
                bundleHead, branch = dlg.getData()
                
                args = self.initCommand("pull")
                args.append('--verbose')
                args.append(fname)
                if branch:
                    args.append(bundleHead + ":" + branch)
                else:
                    args.append(bundleHead)
                
                dia = GitDialog(self.tr('Applying a bundle file (fetch)'),
                                self)
                res = dia.startProcess(args, repodir)
                if res:
                    dia.exec()
                    res = dia.hasAddOrDelete()
                self.checkVCSStatus()
        
        return res
    
    ###########################################################################
    ## Methods for bisect handling.
    ###########################################################################
    
    def gitBisect(self, projectDir, subcommand):
        """
        Public method to perform bisect commands.
        
        @param projectDir name of the project directory (string)
        @param subcommand name of the subcommand (string, one of 'start',
            'start_extended', 'good', 'bad', 'skip' or 'reset')
        @return flag indicating, that the update contained an add
            or delete (boolean)
        @exception ValueError raised to indicate an invalid bisect subcommand
        """
        if subcommand not in ("start", "start_extended", "good", "bad",
                              "skip", "reset"):
            raise ValueError(
                self.tr("Bisect subcommand ({0}) invalid.")
                    .format(subcommand))
        
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        res = False
        rev = ""
        if subcommand in ("good", "bad", "skip", "reset"):
            showBranches = subcommand == "reset"
            showHead = subcommand == "reset"
            from .GitRevisionSelectionDialog import GitRevisionSelectionDialog
            dlg = GitRevisionSelectionDialog(self.gitGetTagsList(repodir),
                                             self.gitGetBranchesList(repodir),
                                             showBranches=showBranches,
                                             showHead=showHead)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                rev = dlg.getRevision()
            else:
                return False
        
        args = self.initCommand("bisect")
        if subcommand == "start_extended":
            from .GitBisectStartDialog import GitBisectStartDialog
            dlg = GitBisectStartDialog()
            if dlg.exec() == QDialog.DialogCode.Accepted:
                bad, good, noCheckout = dlg.getData()
                args.append("start")
                if noCheckout:
                    args.append("--no-checkout")
                args.append(bad)
                args.extend(good)
                args.append("--")
            else:
                return False
        else:
            args.append(subcommand)
            if rev:
                args.extend(rev.split())
                # treat rev as a list separated by whitespace
        
        dia = GitDialog(
            self.tr('Git Bisect ({0})').format(subcommand), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        
        return res
    
    def gitBisectLogBrowser(self, projectDir):
        """
        Public method used to browse the bisect log of the project.
        
        @param projectDir name of the project directory (string)
        """
        if self.bisectlogBrowser is None:
            from .GitBisectLogBrowserDialog import GitBisectLogBrowserDialog
            self.bisectlogBrowser = GitBisectLogBrowserDialog(self)
        self.bisectlogBrowser.show()
        self.bisectlogBrowser.raise_()
        self.bisectlogBrowser.start(projectDir)
    
    def gitBisectCreateReplayFile(self, projectDir):
        """
        Public method used to create a bisect replay file for the project.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("bisect")
        args.append("log")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        else:
            E5MessageBox.critical(
                self,
                self.tr('Process Generation Error'),
                self.tr(
                    'The process {0} could not be started. '
                    'Ensure, that it is in the search path.'
                ).format('git'))
            return
        
        if output:
            fname, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
                None,
                self.tr("Create Bisect Replay File"),
                self.__lastBundlePath or repodir,
                self.tr("Git Bisect Replay Files (*.replay)"),
                None,
                E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
            
            if not fname:
                return  # user aborted
            
            ext = QFileInfo(fname).suffix()
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fname += ex
            if QFileInfo(fname).exists():
                res = E5MessageBox.yesNo(
                    self.__ui,
                    self.tr("Create Bisect Replay File"),
                    self.tr("<p>The Git bisect replay file <b>{0}</b> "
                            "already exists. Overwrite it?</p>")
                        .format(fname),
                    icon=E5MessageBox.Warning)
                if not res:
                    return
            fname = Utilities.toNativeSeparators(fname)
            self.__lastReplayPath = os.path.dirname(fname)
            
            try:
                with open(fname, "w") as f:
                    f.write(output)
            except OSError as err:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Create Bisect Replay File"),
                    self.tr(
                        """<p>The file <b>{0}</b> could not be written.</p>"""
                        """<p>Reason: {1}</p>""")
                    .format(fname, str(err)))
    
    def gitBisectEditReplayFile(self, projectDir):
        """
        Public method used to edit a bisect replay file.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        fname = E5FileDialog.getOpenFileName(
            None,
            self.tr("Edit Bisect Replay File"),
            self.__lastReplayPath or repodir,
            self.tr("Git Bisect Replay Files (*.replay);;All Files (*)"))
        if fname:
            self.__lastReplayPath = os.path.dirname(fname)
            
            self.bisectReplayEditor = MiniEditor(fname)
            self.bisectReplayEditor.show()
    
    def gitBisectReplay(self, projectDir):
        """
        Public method to replay a bisect session.
        
        @param projectDir name of the project directory (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        res = False
        fname = E5FileDialog.getOpenFileName(
            None,
            self.tr("Bisect Replay"),
            self.__lastReplayPath or repodir,
            self.tr("Git Bisect Replay Files (*.replay);;All Files (*)"))
        if fname:
            self.__lastReplayPath = os.path.dirname(fname)
            
            args = self.initCommand("bisect")
            args.append("replay")
            args.append(fname)
            
            dia = GitDialog(
                self.tr('Git Bisect ({0})').format("replay"), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        
        return res
    
    ###########################################################################
    ## Methods for remotes handling.
    ###########################################################################
    
    def gitGetRemotesList(self, repodir):
        """
        Public method to get the list of remote repos.
        
        @param repodir directory name of the repository (string)
        @return list of remote repos (list of string)
        """
        args = self.initCommand("remote")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        remotesList = []
        if output:
            for line in output.splitlines():
                name = line.strip()
                remotesList.append(name)
        
        return remotesList
    
    def gitGetRemoteUrlsList(self, repodir, forFetch=True):
        """
        Public method to get the list of remote repos and their URLs.
        
        @param repodir directory name of the repository (string)
        @param forFetch flag indicating to get Fetch info (string)
        @return list of tuples of remote repo name and repo URL (list of
            tuple of two strings)
        """
        args = self.initCommand("remote")
        args.append("--verbose")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        remotesList = []
        if output:
            for line in output.splitlines():
                name, urlmode = line.strip().split(None, 1)
                url, mode = urlmode.rsplit(None, 1)
                if (
                    (forFetch and mode == "(fetch)") or
                    ((not forFetch) and mode == "(push)")
                ):
                    remotesList.append((name, url))
        
        return remotesList
    
    def gitGetRemoteUrl(self, repodir, remoteName):
        """
        Public method to get the URL of a remote repository.
        
        @param repodir directory name of the repository
        @type str
        @param remoteName name of the remote repository
        @type str
        @return URL of the remote repository
        @rtype str
        """
        args = self.initCommand("remote")
        args.append("get-url")
        args.append(remoteName)
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace').strip()
        
        return output
    
    def gitGetRemoteBranchesList(self, repodir, remote):
        """
        Public method to get the list of a remote repository branches.
        
        @param repodir directory name of the repository (string)
        @param remote remote repository name (string)
        @return list of remote repository branches (list of string)
        """
        args = self.initCommand("ls-remote")
        args.append("--heads")
        args.append(remote)
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        remoteBranches = []
        if output:
            for line in output.splitlines():
                branch = line.strip().split()[-1].split("/")[-1]
                remoteBranches.append(branch)
        
        return remoteBranches
    
    def gitShowRemote(self, projectDir, remoteName):
        """
        Public method to show information about a remote repository.
        
        @param projectDir name of the project directory (string)
        @param remoteName name of the remote repository (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("remote")
        args.append("show")
        args.append(remoteName)
        
        dia = GitDialog(self.tr('Show Remote Info'), self)
        res = dia.startProcess(args, repodir, showArgs=False)
        if res:
            dia.exec()
    
    def gitShowRemotes(self, projectDir):
        """
        Public method to show available remote repositories.
        
        @param projectDir name of the project directory (string)
        """
        if self.remotesDialog is None:
            from .GitRemoteRepositoriesDialog import (
                GitRemoteRepositoriesDialog
            )
            self.remotesDialog = GitRemoteRepositoriesDialog(self)
        self.remotesDialog.show()
        self.remotesDialog.raise_()
        self.remotesDialog.start(projectDir)
    
    def gitAddRemote(self, projectDir):
        """
        Public method to add a remote repository.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitAddRemoteDialog import GitAddRemoteDialog
        dlg = GitAddRemoteDialog()
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, url = dlg.getData()
            args = self.initCommand("remote")
            args.append("add")
            args.append(name)
            args.append(url)
            
            self.startSynchronizedProcess(QProcess(), "git", args,
                                          workingDir=repodir)
    
    def gitRenameRemote(self, projectDir, remoteName):
        """
        Public method to rename a remote repository.
        
        @param projectDir name of the project directory (string)
        @param remoteName name of the remote repository (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        newName, ok = QInputDialog.getText(
            None,
            self.tr("Rename Remote Repository"),
            self.tr("Enter new name for remote repository:"),
            QLineEdit.EchoMode.Normal)
        if ok and newName and newName != remoteName:
            args = self.initCommand("remote")
            args.append("rename")
            args.append(remoteName)
            args.append(newName)
            
            self.startSynchronizedProcess(QProcess(), "git", args,
                                          workingDir=repodir)
    
    def gitChangeRemoteUrl(self, projectDir, remoteName, remoteUrl=""):
        """
        Public method to change the URL of a remote repository.
        
        @param projectDir name of the project directory
        @type str
        @param remoteName name of the remote repository
        @type str
        @param remoteUrl URL of the remote repository
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        if not remoteUrl:
            remoteUrl = self.gitGetRemoteUrl(repodir, remoteName)
        
        from .GitChangeRemoteUrlDialog import GitChangeRemoteUrlDialog
        dlg = GitChangeRemoteUrlDialog(remoteName, remoteUrl)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, url = dlg.getData()
            if url != remoteUrl:
                args = self.initCommand("remote")
                args.append("set-url")
                args.append(name)
                args.append(url)
                
                self.startSynchronizedProcess(QProcess(), "git", args,
                                              workingDir=repodir)
    
    def gitChangeRemoteCredentials(self, projectDir, remoteName, remoteUrl=""):
        """
        Public method to change the user credentials of a remote repository.
        
        @param projectDir name of the project directory
        @type str
        @param remoteName name of the remote repository
        @type str
        @param remoteUrl URL of the remote repository
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        if not remoteUrl:
            remoteUrl = self.gitGetRemoteUrl(repodir, remoteName)
        
        from .GitRemoteCredentialsDialog import GitRemoteCredentialsDialog
        dlg = GitRemoteCredentialsDialog(remoteName, remoteUrl)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, url = dlg.getData()
            if url != remoteUrl:
                args = self.initCommand("remote")
                args.append("set-url")
                args.append(name)
                args.append(url)
                
                self.startSynchronizedProcess(QProcess(), "git", args,
                                              workingDir=repodir)
    
    def gitRemoveRemote(self, projectDir, remoteName):
        """
        Public method to remove a remote repository.
        
        @param projectDir name of the project directory (string)
        @param remoteName name of the remote repository (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("remote")
        args.append("remove")
        args.append(remoteName)
        
        self.startSynchronizedProcess(QProcess(), "git", args,
                                      workingDir=repodir)
    
    def gitPruneRemote(self, projectDir, remoteName):
        """
        Public method to prune stale remote-tracking branches.
        
        @param projectDir name of the project directory (string)
        @param remoteName name of the remote repository (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("remote")
        args.append("prune")
        args.append(remoteName)
        
        dia = GitDialog(self.tr('Show Remote Info'), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
    
    def gitShortlog(self, projectDir, commit):
        """
        Public method to show a short log suitable for inclusion in release
        announcements.
        
        @param projectDir name of the project directory (string)
        @param commit commit to start the log at (strings)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("shortlog")
        args.append("-w")
        args.append(commit)
        
        dia = GitDialog(self.tr('Show Shortlog'), self)
        res = dia.startProcess(args, repodir, showArgs=False)
        if res:
            dia.exec()
    
    def gitDescribe(self, projectDir, commits):
        """
        Public method to find the most recent tag reachable from each commit.
        
        @param projectDir name of the project directory (string)
        @param commits list of commits to start the search from
            (list of strings)
        """
        if self.describeDialog is None:
            from .GitDescribeDialog import GitDescribeDialog
            self.describeDialog = GitDescribeDialog(self)
        self.describeDialog.show()
        self.describeDialog.raise_()
        self.describeDialog.start(projectDir, commits)
    
    ###########################################################################
    ## Methods for cherry-pick handling.
    ###########################################################################
    
    def gitCherryPick(self, projectDir, commits=None):
        """
        Public method to cherry pick commits and apply them to the current
        branch.
        
        @param projectDir name of the project directory (string)
        @param commits list of commits to be applied (list of strings)
        @return flag indicating that the project should be reread (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        res = False
        
        from .GitCherryPickDialog import GitCherryPickDialog
        dlg = GitCherryPickDialog(commits)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            commits, cherrypickInfo, signoff, nocommit = (
                dlg.getData()
            )
            
            args = self.initCommand("cherry-pick")
            args.append("-Xpatience")
            if cherrypickInfo:
                args.append("-x")
            if signoff:
                args.append("--signoff")
            if nocommit:
                args.append("--no-commit")
            args.extend(commits)
            
            dia = GitDialog(self.tr('Cherry-pick'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.checkVCSStatus()
        return res
    
    def gitCherryPickContinue(self, projectDir):
        """
        Public method to continue the last copying session after conflicts
        were resolved.
        
        @param projectDir name of the project directory (string)
        @return flag indicating that the project should be reread (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        import sys
        editor = sys.argv[0].replace(".py", "_editor.py")
        env = {"GIT_EDITOR": "{0} {1}".format(sys.executable, editor)}
        
        args = self.initCommand("cherry-pick")
        args.append("--continue")
        
        dia = GitDialog(self.tr('Copy Changesets (Continue)'), self)
        res = dia.startProcess(args, repodir, environment=env)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        return res
    
    def gitCherryPickQuit(self, projectDir):
        """
        Public method to quit the current copying operation.
        
        @param projectDir name of the project directory (string)
        @return flag indicating that the project should be reread (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        args = self.initCommand("cherry-pick")
        args.append("--quit")
        
        dia = GitDialog(self.tr('Copy Changesets (Quit)'), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        return res
    
    def gitCherryPickAbort(self, projectDir):
        """
        Public method to cancel the last copying session and return to
        the previous state.
        
        @param projectDir name of the project directory (string)
        @return flag indicating that the project should be reread (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        args = self.initCommand("cherry-pick")
        args.append("--abort")
        
        dia = GitDialog(self.tr('Copy Changesets (Cancel)'), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        return res
    
    ###########################################################################
    ## Methods for stash handling.
    ###########################################################################
    
    def __gitGetStashesList(self, projectDir):
        """
        Private method to get a list of stash names.
        
        @param projectDir name of the project directory (string)
        @return list of available stashes (list of string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return []
        
        args = self.initCommand("stash")
        args.append("list")
        args.append("--format=format:%gd")
        
        stashesList = []
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        if output:
            stashesList = output.strip().splitlines()
        
        return stashesList
    
    def gitStashSave(self, projectDir):
        """
        Public method to save the current changes to a new stash.
        
        @param projectDir name of the project directory (string)
        @return flag indicating, that the save contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        res = False
        from .GitStashDataDialog import GitStashDataDialog
        dlg = GitStashDataDialog()
        if dlg.exec() == QDialog.DialogCode.Accepted:
            message, keepIndex, untracked = dlg.getData()
            args = self.initCommand("stash")
            args.append("save")
            if keepIndex:
                args.append("--keep-index")
            if untracked == GitStashDataDialog.UntrackedOnly:
                args.append("--include-untracked")
            elif untracked == GitStashDataDialog.UntrackedAndIgnored:
                args.append("--all")
            if message:
                args.append(message)
            
            dia = GitDialog(self.tr('Saving stash'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        return res
    
    def gitStashBrowser(self, projectDir):
        """
        Public method used to browse the stashed changes.
        
        @param projectDir name of the project directory (string)
        """
        if self.stashBrowser is None:
            from .GitStashBrowserDialog import GitStashBrowserDialog
            self.stashBrowser = GitStashBrowserDialog(self)
        self.stashBrowser.show()
        self.stashBrowser.raise_()
        self.stashBrowser.start(projectDir)
    
    def gitStashShowPatch(self, projectDir, stashName=""):
        """
        Public method to show the contents of a stash.
        
        @param projectDir name of the project directory (string)
        @param stashName name of a stash (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        if not stashName:
            availableStashes = self.__gitGetStashesList(repodir)
            stashName, ok = QInputDialog.getItem(
                None,
                self.tr("Show Stash"),
                self.tr("Select a stash (empty for latest stash):"),
                [""] + availableStashes,
                0, False)
            if not ok:
                return
        
        if self.diff is None:
            from .GitDiffDialog import GitDiffDialog
            self.diff = GitDiffDialog(self)
        self.diff.show()
        self.diff.raise_()
        self.diff.start(repodir, diffMode="stash", stashName=stashName)
    
    def gitStashApply(self, projectDir, stashName=""):
        """
        Public method to apply a stash but keep it.
        
        @param projectDir name of the project directory (string)
        @param stashName name of a stash (string)
        @return flag indicating, that the restore contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        if not stashName:
            availableStashes = self.__gitGetStashesList(repodir)
            stashName, ok = QInputDialog.getItem(
                None,
                self.tr("Restore Stash"),
                self.tr("Select a stash (empty for latest stash):"),
                [""] + availableStashes,
                0, False)
            if not ok:
                return False
        
        args = self.initCommand("stash")
        args.append("apply")
        if stashName:
            args.append(stashName)
        
        dia = GitDialog(self.tr('Restoring stash'), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def gitStashPop(self, projectDir, stashName=""):
        """
        Public method to apply a stash and delete it.
        
        @param projectDir name of the project directory (string)
        @param stashName name of a stash (string)
        @return flag indicating, that the restore contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        if not stashName:
            availableStashes = self.__gitGetStashesList(repodir)
            stashName, ok = QInputDialog.getItem(
                None,
                self.tr("Restore Stash"),
                self.tr("Select a stash (empty for latest stash):"),
                [""] + availableStashes,
                0, False)
            if not ok:
                return False
        
        args = self.initCommand("stash")
        args.append("pop")
        if stashName:
            args.append(stashName)
        
        dia = GitDialog(self.tr('Restoring stash'), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def gitStashBranch(self, projectDir, stashName=""):
        """
        Public method to create a branch from a stash.
        
        @param projectDir name of the project directory (string)
        @param stashName name of a stash (string)
        @return flag indicating, that the restore contained an add
            or delete (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        branchName, ok = QInputDialog.getText(
            None,
            self.tr("Create Branch"),
            self.tr("Enter a branch name to restore a stash to:"),
            QLineEdit.EchoMode.Normal)
        if not ok or branchName == "":
            return False
        
        if not stashName:
            availableStashes = self.__gitGetStashesList(repodir)
            stashName, ok = QInputDialog.getItem(
                None,
                self.tr("Create Branch"),
                self.tr("Select a stash (empty for latest stash):"),
                [""] + availableStashes,
                0, False)
            if not ok:
                return False
        
        args = self.initCommand("stash")
        args.append("branch")
        args.append(branchName)
        if stashName:
            args.append(stashName)
        
        dia = GitDialog(self.tr('Creating branch'), self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def gitStashDrop(self, projectDir, stashName=""):
        """
        Public method to delete a stash.
        
        @param projectDir name of the project directory (string)
        @param stashName name of a stash (string)
        @return flag indicating a successful deletion (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        if not stashName:
            availableStashes = self.__gitGetStashesList(repodir)
            stashName, ok = QInputDialog.getItem(
                None,
                self.tr("Show Stash"),
                self.tr("Select a stash (empty for latest stash):"),
                [""] + availableStashes,
                0, False)
            if not ok:
                return False
        
        res = E5MessageBox.yesNo(
            None,
            self.tr("Delete Stash"),
            self.tr("""Do you really want to delete the stash <b>{0}</b>?""")
            .format(stashName))
        if res:
            args = self.initCommand("stash")
            args.append("drop")
            if stashName:
                args.append(stashName)
            
            dia = GitDialog(self.tr('Deleting stash'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
        return res
    
    def gitStashClear(self, projectDir):
        """
        Public method to delete all stashes.
        
        @param projectDir name of the project directory (string)
        @return flag indicating a successful deletion (boolean)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return False
        
        res = E5MessageBox.yesNo(
            None,
            self.tr("Delete All Stashes"),
            self.tr("""Do you really want to delete all stashes?"""))
        if res:
            args = self.initCommand("stash")
            args.append("clear")
            
            dia = GitDialog(self.tr('Deleting all stashes'), self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
        return res
    
    def gitEditConfig(self, projectDir):
        """
        Public method used to edit the repository configuration file.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        cfgFile = os.path.join(repodir, self.adminDir, "config")
        if not os.path.exists(cfgFile):
            # create an empty one
            try:
                with open(cfgFile, "w"):
                    pass
            except OSError:
                pass
        self.repoEditor = MiniEditor(cfgFile, "Properties")
        self.repoEditor.show()
    
    def gitEditUserConfig(self):
        """
        Public method used to edit the user configuration file.
        """
        from .GitUtilities import getConfigPath
        cfgFile = getConfigPath()
        if not os.path.exists(cfgFile):
            from .GitUserConfigDataDialog import GitUserConfigDataDialog
            dlg = GitUserConfigDataDialog()
            if dlg.exec() == QDialog.DialogCode.Accepted:
                firstName, lastName, email = dlg.getData()
            else:
                firstName, lastName, email = (
                    "Firstname", "Lastname", "email_address")
            try:
                with open(cfgFile, "w") as f:
                    f.write("[user]\n")
                    f.write("    name = {0} {1}\n".format(firstName, lastName))
                    f.write("    email = {0}\n".format(email))
            except OSError:
                # ignore these
                pass
        self.userEditor = MiniEditor(cfgFile, "Properties")
        self.userEditor.show()
    
    def gitShowConfig(self, projectDir):
        """
        Public method to show the combined configuration.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("config")
        args.append("--list")
        
        dia = GitDialog(
            self.tr('Showing the combined configuration settings'),
            self)
        res = dia.startProcess(args, repodir, False)
        if res:
            dia.exec()
    
    def gitVerify(self, projectDir):
        """
        Public method to verify the connectivity and validity of objects
        of the database.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("fsck")
        args.append("--strict")
        args.append("--full")
        args.append("--cache")
        
        dia = GitDialog(
            self.tr('Verifying the integrity of the Git repository'),
            self)
        res = dia.startProcess(args, repodir, False)
        if res:
            dia.exec()
    
    def gitHouseKeeping(self, projectDir):
        """
        Public method to cleanup and optimize the local repository.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("gc")
        args.append("--prune")
        if self.__plugin.getPreferences("AggressiveGC"):
            args.append("--aggressive")
        
        dia = GitDialog(
            self.tr('Performing Repository Housekeeping'),
            self)
        res = dia.startProcess(args, repodir)
        if res:
            dia.exec()
    
    def gitStatistics(self, projectDir):
        """
        Public method to show some statistics of the local repository.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.initCommand("count-objects")
        args.append("-v")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        info = []
        if output:
            statistics = {}
            for line in output.splitlines():
                key, value = line.strip().split(": ", 1)
                statistics[key] = value
            
            info.append("""<p><table>""")
            info.append(self.tr("""<tr><td><b>Statistics</b></td></tr>"""))
            info.append(
                self.tr("""<tr><td>Number of loose objects: </td>"""
                        """<td>{0}</td></tr>""")
                    .format(statistics["count"]))
            info.append(
                self.tr("""<tr><td>Disk space used by loose objects: </td>"""
                        """<td>{0} KiB</td></tr>""")
                    .format(statistics["size"]))
            info.append(
                self.tr("""<tr><td>Number of packed objects: </td>"""
                        """<td>{0}</td></tr>""")
                    .format(statistics["in-pack"]))
            info.append(
                self.tr("""<tr><td>Number of packs: </td>"""
                        """<td>{0}</td></tr>""")
                    .format(statistics["packs"]))
            info.append(
                self.tr("""<tr><td>Disk space used by packed objects: </td>"""
                        """<td>{0} KiB</td></tr>""")
                    .format(statistics["size-pack"]))
            info.append(
                self.tr("""<tr><td>Packed objects waiting for pruning: </td>"""
                        """<td>{0}</td></tr>""")
                    .format(statistics["prune-packable"]))
            info.append(
                self.tr("""<tr><td>Garbage files: </td>"""
                        """<td>{0}</td></tr>""")
                    .format(statistics["garbage"]))
            info.append(
                self.tr("""<tr><td>Disk space used by garbage files: </td>"""
                        """<td>{0} KiB</td></tr>""")
                    .format(statistics["size-garbage"]))
            info.append("""</table></p>""")
        else:
            info.append(self.tr("<p><b>No statistics available.</b></p>"))
        dlg = VcsRepositoryInfoDialog(None, "\n".join(info))
        dlg.exec()
    
    def gitGetArchiveFormats(self, repodir):
        """
        Public method to get a list of supported archive formats.
        
        @param repodir directory name of the repository (string)
        @return list of supported archive formats (list of strings)
        """
        args = self.initCommand("archive")
        args.append("--list")
        
        output = ""
        process = QProcess()
        process.setWorkingDirectory(repodir)
        process.start('git', args)
        procStarted = process.waitForStarted(5000)
        if procStarted:
            finished = process.waitForFinished(30000)
            if finished and process.exitCode() == 0:
                output = str(process.readAllStandardOutput(),
                             Preferences.getSystem("IOEncoding"),
                             'replace')
        
        archiveFormats = []
        if output:
            for line in output.splitlines():
                archiveFormat = line.strip()
                archiveFormats.append(archiveFormat)
        
        return archiveFormats
    
    def gitCreateArchive(self, projectDir):
        """
        Public method to show some statistics of the local repository.
        
        @param projectDir name of the project directory (string)
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitArchiveDataDialog import GitArchiveDataDialog
        dlg = GitArchiveDataDialog(
            self.gitGetTagsList(repodir),
            self.gitGetBranchesList(repodir, withMaster=True),
            self.gitGetArchiveFormats(repodir)
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            commit, archiveFormat, fileName, prefix = dlg.getData()
            args = self.initCommand("archive")
            args.append("--format={0}".format(archiveFormat))
            args.append("--output={0}".format(fileName))
            if prefix:
                prefix = Utilities.fromNativeSeparators(prefix)
                if not prefix.endswith("/"):
                    prefix += "/"
                args.append("--prefix={0}".format(prefix))
            args.append(commit)
            
            dia = GitDialog(
                self.tr('Creating Archive'),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    ###########################################################################
    ## Methods related to submodules.
    ###########################################################################
    
    def gitSubmoduleAdd(self, projectDir):
        """
        Public method to add a submodule to the project.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitSubmoduleAddDialog import GitSubmoduleAddDialog
        dlg = GitSubmoduleAddDialog(self, repodir)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            repo, branch, name, path, force = dlg.getData()
            args = self.initCommand("submodule")
            args.append("add")
            if branch:
                args.append("--branch")
                args.append(branch)
            if force:
                args.append("--force")
            if name:
                args.append("--name")
                args.append(name)
            args.append(repo)
            if path:
                args.append(path)
            
            dia = GitDialog(
                self.tr("Add Submodule"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def __gitSubmodulesList(self, repodir):
        """
        Private method to get the data of defined submodules.
        
        @param repodir name of the directory containing the repo subdirectory
        @type str
        @return list of dictionaries with submodule name, path, URL and branch
        @rtype list of dict
        """
        submodulesFile = os.path.join(repodir, ".gitmodules")
        if not os.path.exists(submodulesFile):
            return []
        
        try:
            with open(submodulesFile, "r") as modulesFile:
                contents = modulesFile.readlines()
        except OSError:
            # silently ignore them
            return []
        
        submodules = []
        submoduleDict = None
        for line in contents:
            line = line.strip()
            if line.startswith("[submodule"):
                if submoduleDict:
                    if "branch" not in submoduleDict:
                        submoduleDict["branch"] = ""
                    submodules.append(submoduleDict)
                submoduleDict = {"name": line.split(None, 1)[1][1:-2]}
            elif "=" in line:
                option, value = line.split("=", 1)
                submoduleDict[option.strip()] = value.strip()
        if submoduleDict:
            if "branch" not in submoduleDict:
                submoduleDict["branch"] = ""
            submodules.append(submoduleDict)
        
        return submodules
    
    def gitSubmoduleList(self, projectDir):
        """
        Public method to show a list of all submodules of the project.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        submodulesList = self.__gitSubmodulesList(repodir)
        if submodulesList:
            from .GitSubmodulesListDialog import GitSubmodulesListDialog
            dlg = GitSubmodulesListDialog(submodulesList)
            dlg.exec()
        else:
            E5MessageBox.information(
                None,
                self.tr("List Submodules"),
                self.tr("""No submodules defined for the project."""))
    
    def __selectSubmodulePath(self, repodir):
        """
        Private method to select a submodule path.
        
        @param repodir name of the directory containing the repo subdirectory
        @type str
        @return tuple of selected submodule path and flag indicating
            a cancellation
        @rtype tuple of (str, bool)
        """
        allEntry = self.tr("All")
        paths = [submodule["path"]
                 for submodule in self.__gitSubmodulesList(repodir)]
        submodulePath, ok = QInputDialog.getItem(
            None,
            self.tr("Submodule Path"),
            self.tr("Select a submodule path:"),
            [allEntry] + sorted(paths),
            0, False)
        if submodulePath == allEntry:
            submodulePath = ""
        
        return submodulePath, ok
    
    def __selectSubmodulePaths(self, repodir):
        """
        Private method to select a list of submodule paths.
        
        @param repodir name of the directory containing the repo subdirectory
        @type str
        @return tuple of selected submodule paths and flag indicating
            a cancellation
        @rtype tuple of (list of str, bool)
        """
        paths = [submodule["path"]
                 for submodule in self.__gitSubmodulesList(repodir)]
        
        from .GitListDialog import GitListDialog
        dlg = GitListDialog(sorted(paths))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            selectedPaths = dlg.getSelection()
            return selectedPaths, True
        else:
            return [], False
    
    def gitSubmoduleInit(self, projectDir):
        """
        Public method to initialize one or all submodules.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        submodulePaths, ok = self.__selectSubmodulePaths(repodir)
        if ok:
            args = self.initCommand("submodule")
            args.append("init")
            args.extend(submodulePaths)
            
            dia = GitDialog(
                self.tr("Initialize Submodules"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitSubmoduleDeinit(self, projectDir):
        """
        Public method to unregister submodules.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        paths = [submodule["path"]
                 for submodule in self.__gitSubmodulesList(repodir)]
        
        from .GitSubmodulesDeinitDialog import GitSubmodulesDeinitDialog
        dlg = GitSubmodulesDeinitDialog(paths)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            deinitAll, submodulePaths, force = dlg.getData()
            args = self.initCommand("submodule")
            args.append("deinit")
            if deinitAll:
                args.append("--all")
            else:
                args.extend(submodulePaths)
            if force:
                args.append("--force")
            
            dia = GitDialog(
                self.tr("Unregister Submodules"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitSubmoduleUpdate(self, projectDir, initialize=False, remote=False):
        """
        Public method to update submodules.
        
        @param projectDir name of the project directory
        @type str
        @param initialize flag indicating an initialize and update operation
        @type bool
        @param remote flag indicating a fetch and update operation
        @type bool
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        submodulePaths, ok = self.__selectSubmodulePaths(repodir)
        if ok:
            args = self.initCommand("submodule")
            args.append("update")
            if initialize:
                args.append("--init")
            if remote:
                args.append("--remote")
            args.extend(submodulePaths)
            
            dia = GitDialog(
                self.tr("Update Submodules"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitSubmoduleUpdateWithOptions(self, projectDir):
        """
        Public method to update submodules offering a dialog to select the
        update options.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        paths = [submodule["path"]
                 for submodule in self.__gitSubmodulesList(repodir)]
        
        from .GitSubmodulesUpdateOptionsDialog import (
            GitSubmodulesUpdateOptionsDialog
        )
        dlg = GitSubmodulesUpdateOptionsDialog(paths)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            procedure, init, remote, noFetch, force, submodulePaths = (
                dlg.getData()
            )
            
            args = self.initCommand("submodule")
            args.append("update")
            args.append(procedure)
            if init:
                args.append("--init")
            if remote:
                args.append("--remote")
            if noFetch:
                args.append("--no-fetch")
            if force:
                args.append("--force")
            args.extend(submodulePaths)
            
            dia = GitDialog(
                self.tr("Update Submodules"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitSubmoduleSync(self, projectDir):
        """
        Public method to synchronize submodules.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        paths = [submodule["path"]
                 for submodule in self.__gitSubmodulesList(repodir)]
        
        from .GitSubmodulesSyncDialog import GitSubmodulesSyncDialog
        dlg = GitSubmodulesSyncDialog(paths)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            submodulePaths, recursive = dlg.getData()
            args = self.initCommand("submodule")
            args.append("sync")
            if recursive:
                args.append("--recursive")
            args.extend(submodulePaths)
            
            dia = GitDialog(
                self.tr("Synchronize Submodules"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    def gitSubmoduleStatus(self, projectDir):
        """
        Public method to show the status of the submodules.
        
        @param projectDir name of the project directory
        @type str
        """
        if self.submoduleStatusDialog is None:
            from .GitSubmodulesStatusDialog import GitSubmodulesStatusDialog
            self.submoduleStatusDialog = GitSubmodulesStatusDialog(self)
        self.submoduleStatusDialog.show()
        self.submoduleStatusDialog.raise_()
        self.submoduleStatusDialog.start(projectDir)
    
    def gitSubmoduleSummary(self, projectDir):
        """
        Public method to show the status of the submodules.
        
        @param projectDir name of the project directory
        @type str
        """
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        paths = [submodule["path"]
                 for submodule in self.__gitSubmodulesList(repodir)]
        
        from .GitSubmodulesSummaryOptionsDialog import (
            GitSubmodulesSummaryOptionsDialog
        )
        dlg = GitSubmodulesSummaryOptionsDialog(paths)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            submodulePaths, superProject, index, commit, limit = dlg.getData()
            args = self.initCommand("submodule")
            args.append("summary")
            if superProject:
                args.append("--files")
            if index:
                args.append("--cached")
            if limit > -1:
                args.append("--summary-limit")
                args.append(str(limit))
            if commit:
                args.append(commit)
                if submodulePaths:
                    args.append("--")
            args.extend(submodulePaths)
            
            dia = GitDialog(
                self.tr("Submodules Summary"),
                self)
            res = dia.startProcess(args, repodir)
            if res:
                dia.exec()
    
    ###########################################################################
    ## Methods to get the helper objects are below.
    ###########################################################################
    
    def vcsGetProjectBrowserHelper(self, browser, project,
                                   isTranslationsBrowser=False):
        """
        Public method to instantiate a helper object for the different
        project browsers.
        
        @param browser reference to the project browser object
        @param project reference to the project object
        @param isTranslationsBrowser flag indicating, the helper is requested
            for the translations browser (this needs some special treatment)
        @return the project browser helper object
        """
        from .ProjectBrowserHelper import GitProjectBrowserHelper
        return GitProjectBrowserHelper(self, browser, project,
                                       isTranslationsBrowser)
        
    def vcsGetProjectHelper(self, project):
        """
        Public method to instantiate a helper object for the project.
        
        @param project reference to the project object
        @return the project helper object
        """
        self.__projectHelper = self.__plugin.getProjectHelper()
        self.__projectHelper.setObjects(self, project)
        return self.__projectHelper

    ###########################################################################
    ##  Status Monitor Thread methods
    ###########################################################################

    def _createStatusMonitorThread(self, interval, project):
        """
        Protected method to create an instance of the VCS status monitor
        thread.
        
        @param interval check interval for the monitor thread in seconds
            (integer)
        @param project reference to the project object (Project)
        @return reference to the monitor thread (QThread)
        """
        from .GitStatusMonitorThread import GitStatusMonitorThread
        return GitStatusMonitorThread(interval, project, self)
