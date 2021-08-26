# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the version control systems interface to Mercurial.
"""

import os
import shutil

from PyQt5.QtCore import (
    pyqtSignal, QFileInfo, QFileSystemWatcher, QCoreApplication
)
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox, E5FileDialog

from QScintilla.MiniEditor import MiniEditor

from VCS.VersionControl import VersionControl
from VCS.RepositoryInfoDialog import VcsRepositoryInfoDialog

from .HgDialog import HgDialog
from .HgClient import HgClient

import Utilities


class Hg(VersionControl):
    """
    Class implementing the version control systems interface to Mercurial.
    
    @signal committed() emitted after the commit action has completed
    @signal activeExtensionsChanged() emitted when the list of active
        extensions has changed
    @signal iniFileChanged() emitted when a Mercurial/repo configuration file
        has changed
    """
    committed = pyqtSignal()
    activeExtensionsChanged = pyqtSignal()
    iniFileChanged = pyqtSignal()
    
    IgnoreFileName = ".hgignore"
    
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
        self.tagsList = []
        self.branchesList = []
        self.allTagsBranchesList = []
        self.bookmarksList = []
        self.showedTags = False
        self.showedBranches = False
        
        self.tagTypeList = [
            'tags',
            'branches',
        ]
        
        self.commandHistory = []
        
        if "HG_ASP_DOT_NET_HACK" in os.environ:
            self.adminDir = '_hg'
        else:
            self.adminDir = '.hg'
        
        self.logBrowser = None
        self.logBrowserIncoming = None
        self.logBrowserOutgoing = None
        self.diff = None
        self.sbsDiff = None
        self.status = None
        self.summary = None
        self.tagbranchList = None
        self.annotate = None
        self.repoEditor = None
        self.serveDlg = None
        self.bookmarksListDlg = None
        self.bookmarksInOutDlg = None
        self.conflictsDlg = None
        
        self.bundleFile = None
        self.__lastChangeGroupPath = None
        
        self.statusCache = {}
        
        self.__commitData = {}
        self.__commitDialog = None
        
        self.__forgotNames = []
        
        self.__activeExtensions = []
        
        from .HgUtilities import getConfigPath
        self.__iniWatcher = QFileSystemWatcher(self)
        self.__iniWatcher.fileChanged.connect(self.__iniFileChanged)
        cfgFile = getConfigPath()
        if os.path.exists(cfgFile):
            self.__iniWatcher.addPath(cfgFile)
        
        self.__client = None
        self.__createClient()
        self.__projectHelper = None
        
        self.__repoDir = ""
        self.__repoIniFile = ""
        self.__defaultConfigured = False
        self.__defaultPushConfigured = False
        
        # instantiate the extensions
        from .QueuesExtension.queues import Queues
        from .PurgeExtension.purge import Purge
        from .GpgExtension.gpg import Gpg
        from .RebaseExtension.rebase import Rebase
        from .ShelveExtension.shelve import Shelve
        from .LargefilesExtension.largefiles import Largefiles
        from .StripExtension.strip import Strip
        from .HisteditExtension.histedit import Histedit
        from .CloseheadExtension.closehead import Closehead
        self.__extensions = {
            "mq": Queues(self),
            "purge": Purge(self),
            "gpg": Gpg(self),
            "rebase": Rebase(self),
            "shelve": Shelve(self),
            "largefiles": Largefiles(self),
            "strip": Strip(self),
            "histedit": Histedit(self),
            "closehead": Closehead(self),
        }
    
    def getPlugin(self):
        """
        Public method to get a reference to the plugin object.
        
        @return reference to the plugin object (VcsMercurialPlugin)
        """
        return self.__plugin
    
    def getEncoding(self):
        """
        Public method to get the encoding to be used by Mercurial.
        
        @return encoding (string)
        """
        return self.__plugin.getPreferences("Encoding")
    
    def vcsShutdown(self):
        """
        Public method used to shutdown the Mercurial interface.
        """
        if self.logBrowser is not None:
            self.logBrowser.close()
        if self.logBrowserIncoming is not None:
            self.logBrowserIncoming.close()
        if self.logBrowserOutgoing is not None:
            self.logBrowserOutgoing.close()
        if self.diff is not None:
            self.diff.close()
        if self.sbsDiff is not None:
            self.sbsDiff.close()
        if self.status is not None:
            self.status.close()
        if self.summary is not None:
            self.summary.close()
        if self.tagbranchList is not None:
            self.tagbranchList.close()
        if self.annotate is not None:
            self.annotate.close()
        if self.serveDlg is not None:
            self.serveDlg.close()
        
        if self.bookmarksListDlg is not None:
            self.bookmarksListDlg.close()
        if self.bookmarksInOutDlg is not None:
            self.bookmarksInOutDlg.close()
        
        if self.conflictsDlg is not None:
            self.conflictsDlg.close()
        
        if self.bundleFile and os.path.exists(self.bundleFile):
            os.remove(self.bundleFile)
        
        # shut down the project helpers
        if self.__projectHelper is not None:
            self.__projectHelper.shutdown()
        
        # shut down the extensions
        for extension in self.__extensions.values():
            extension.shutdown()
        
        # shut down the client
        self.__client and self.__client.stopServer()
    
    def initCommand(self, command):
        """
        Public method to initialize a command arguments list.
        
        @param command command name (string)
        @return list of command options (list of string)
        """
        args = [command]
        self.addArguments(args, self.__plugin.getGlobalOptions())
        return args
    
    def vcsExists(self):
        """
        Public method used to test for the presence of the hg executable.
        
        @return flag indicating the existence (boolean) and an error message
            (string)
        """
        from .HgUtilities import hgVersion
        
        self.versionStr, self.version, errMsg = hgVersion(self.__plugin)
        hgExists = errMsg == ""
        if hgExists:
            self.__getExtensionsInfo()
        return hgExists, errMsg
    
    def vcsInit(self, vcsDir, noDialog=False):
        """
        Public method used to initialize the mercurial repository.
        
        The initialization is done, when a project is converted into a
        Mercurial controlled project. Therefore we always return TRUE without
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
        Public method used to import the project into the Mercurial repository.
        
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
        dia = HgDialog(self.tr('Creating Mercurial repository'), self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        status = dia.normalExit()
        
        if status:
            self.stopClient()
            self.__repoDir = projectDir
            
            ignoreName = os.path.join(projectDir, Hg.IgnoreFileName)
            if not os.path.exists(ignoreName):
                status = self.hgCreateIgnoreFile(projectDir)
            
            if status and addAll:
                args = self.initCommand("commit")
                args.append('--addremove')
                args.append('--message')
                args.append(msg)
                dia = HgDialog(
                    self.tr('Initial commit to Mercurial repository'),
                    self)
                res = dia.startProcess(args)
                if res:
                    dia.exec()
                status = dia.normalExit()
        
        return status, False
    
    def vcsCheckout(self, vcsDataDict, projectDir, noDialog=False):
        """
        Public method used to check the project out of a Mercurial repository
        (clone).
        
        @param vcsDataDict dictionary of data required for the checkout
        @param projectDir project directory to create (string)
        @param noDialog flag indicating quiet operations
        @return flag indicating an execution without errors (boolean)
        """
        noDialog = False
        try:
            rev = vcsDataDict["revision"]
        except KeyError:
            rev = None
        vcsUrl = self.hgNormalizeURL(vcsDataDict["url"])
        
        args = self.initCommand("clone")
        if rev:
            args.append("--rev")
            args.append(rev)
        if vcsDataDict["largefiles"]:
            args.append("--all-largefiles")
        args.append(vcsUrl)
        args.append(projectDir)
        
        if noDialog:
            out, err = self.__client.runcommand(args)
            return err == ""
        else:
            dia = HgDialog(
                self.tr('Cloning project from a Mercurial repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
            return dia.normalExit()
    
    def vcsExport(self, vcsDataDict, projectDir):
        """
        Public method used to export a directory from the Mercurial repository.
        
        @param vcsDataDict dictionary of data required for the checkout
        @param projectDir project directory to create (string)
        @return flag indicating an execution without errors (boolean)
        """
        status = self.vcsCheckout(vcsDataDict, projectDir)
        shutil.rmtree(os.path.join(projectDir, self.adminDir), True)
        if os.path.exists(os.path.join(projectDir, Hg.IgnoreFileName)):
            os.remove(os.path.join(projectDir, Hg.IgnoreFileName))
        return status
    
    def vcsCommit(self, name, message, noDialog=False, closeBranch=False,
                  mq=False, merge=False):
        """
        Public method used to make the change of a file/directory permanent
        in the Mercurial repository.
        
        @param name file/directory name to be committed (string or list of
            strings)
        @param message message for this operation (string)
        @param noDialog flag indicating quiet operations
        @param closeBranch flag indicating a close branch commit (boolean)
        @param mq flag indicating a queue commit (boolean)
        @param merge flag indicating a merge commit (boolean)
        """
        msg = message
        
        if mq or merge:
            # ensure dialog is shown for a queue commit
            noDialog = False
        
        if not noDialog:
            # call CommitDialog and get message from there
            if self.__commitDialog is None:
                from .HgCommitDialog import HgCommitDialog
                self.__commitDialog = HgCommitDialog(self, msg, mq, merge,
                                                     self.__ui)
                self.__commitDialog.accepted.connect(self.__vcsCommit_Step2)
            self.__commitDialog.show()
            self.__commitDialog.raise_()
            self.__commitDialog.activateWindow()
        
        self.__commitData["name"] = name
        self.__commitData["msg"] = msg
        self.__commitData["noDialog"] = noDialog
        self.__commitData["closeBranch"] = closeBranch
        self.__commitData["mq"] = mq
        self.__commitData["merge"] = merge
        
        if noDialog:
            self.__vcsCommit_Step2()
    
    def __vcsCommit_Step2(self):
        """
        Private slot performing the second step of the commit action.
        """
        name = self.__commitData["name"]
        msg = self.__commitData["msg"]
        noDialog = self.__commitData["noDialog"]
        closeBranch = self.__commitData["closeBranch"]
        mq = self.__commitData["mq"]
        merge = self.__commitData["merge"]
        
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
            (msg, amend, commitSubrepositories, author,
             dateTime) = self.__commitDialog.getCommitData()
            self.__commitDialog.deleteLater()
            self.__commitDialog = None
            if amend and not msg:
                msg = self.__getMostRecentCommitMessage()
        else:
            amend = False
            commitSubrepositories = False
            author = ""
            dateTime = ""
        
        if not msg and not amend:
            msg = '***'
        
        args = self.initCommand("commit")
        args.append("-v")
        if mq:
            args.append("--mq")
        elif merge:
            if author:
                args.append("--user")
                args.append(author)
            if dateTime:
                args.append("--date")
                args.append(dateTime)
        else:
            if closeBranch:
                args.append("--close-branch")
            if amend:
                args.append("--amend")
            if commitSubrepositories:
                args.append("--subrepos")
            if author:
                args.append("--user")
                args.append(author)
            if dateTime:
                args.append("--date")
                args.append(dateTime)
        if msg:
            args.append("--message")
            args.append(msg)
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        dia = HgDialog(
            self.tr('Committing changes to Mercurial repository'),
            self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        self.committed.emit()
        if self.__forgotNames:
            model = e5App().getObject("Project").getModel()
            for name in self.__forgotNames:
                model.updateVCSStatus(name)
            self.__forgotNames = []
        self.checkVCSStatus()
    
    def __getMostRecentCommitMessage(self):
        """
        Private method to get the most recent commit message.
        
        Note: This message is extracted from the parent commit of the
        working directory.
        
        @return most recent commit message
        @rtype str
        """
        args = self.initCommand("log")
        args.append("--rev")
        args.append(".")
        args.append('--template')
        args.append('{desc}')
        
        output, error = self.__client.runcommand(args)
        
        return output
    
    def vcsUpdate(self, name=None, noDialog=False, revision=None):
        """
        Public method used to update a file/directory with the Mercurial
        repository.
        
        @param name file/directory name to be updated (not used)
        @param noDialog flag indicating quiet operations (boolean)
        @param revision revision to update to (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        args = self.initCommand("update")
        if "-v" not in args and "--verbose" not in args:
            args.append("-v")
        if revision:
            args.append("-r")
            args.append(revision)
        
        if noDialog:
            out, err = self.__client.runcommand(args)
            res = False
        else:
            dia = HgDialog(self.tr(
                'Synchronizing with the Mercurial repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def vcsAdd(self, name, isDir=False, noDialog=False):
        """
        Public method used to add a file/directory to the Mercurial repository.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        @param noDialog flag indicating quiet operations
        """
        args = self.initCommand("add")
        args.append("-v")
        
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        if noDialog:
            out, err = self.__client.runcommand(args)
        else:
            dia = HgDialog(
                self.tr(
                    'Adding files/directories to the Mercurial repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def vcsAddBinary(self, name, isDir=False):
        """
        Public method used to add a file/directory in binary mode to the
        Mercurial repository.
        
        @param name file/directory name to be added (string)
        @param isDir flag indicating name is a directory (boolean)
        """
        self.vcsAdd(name, isDir)
    
    def vcsAddTree(self, path):
        """
        Public method to add a directory tree rooted at path to the Mercurial
        repository.
        
        @param path root directory of the tree to be added (string or list of
            strings))
        """
        self.vcsAdd(path, isDir=False)
    
    def vcsRemove(self, name, project=False, noDialog=False):
        """
        Public method used to remove a file/directory from the Mercurial
        repository.
        
        The default operation is to remove the local copy as well.
        
        @param name file/directory name to be removed (string or list of
            strings))
        @param project flag indicating deletion of a project tree (boolean)
            (not needed)
        @param noDialog flag indicating quiet operations
        @return flag indicating successfull operation (boolean)
        """
        args = self.initCommand("remove")
        args.append("-v")
        if noDialog and '--force' not in args:
            args.append('--force')
        
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        if noDialog:
            out, err = self.__client.runcommand(args)
            res = err == ""
        else:
            dia = HgDialog(
                self.tr(
                    'Removing files/directories from the Mercurial'
                    ' repository'),
                self)
            res = dia.startProcess(args)
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
        @return flag indicating successfull operation (boolean)
        """
        isDir = os.path.isdir(name)
        
        res = False
        if noDialog:
            if target is None:
                return False
            force = True
            accepted = True
        else:
            from .HgCopyDialog import HgCopyDialog
            dlg = HgCopyDialog(name, None, True)
            accepted = dlg.exec() == QDialog.DialogCode.Accepted
            if accepted:
                target, force = dlg.getData()
        
        if accepted:
            args = self.initCommand("rename")
            args.append("-v")
            if force:
                args.append('--force')
            args.append(name)
            args.append(target)
            
            if noDialog:
                out, err = self.__client.runcommand(args)
                res = err == ""
            else:
                dia = HgDialog(self.tr('Renaming {0}').format(name), self)
                res = dia.startProcess(args)
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
    
    def vcsDiff(self, name):
        """
        Public method used to view the difference of a file/directory to the
        Mercurial repository.
        
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
            from .HgDiffDialog import HgDiffDialog
            self.diff = HgDiffDialog(self)
        self.diff.show()
        self.diff.raise_()
        QApplication.processEvents()
        self.diff.start(name, refreshable=True)
    
    def vcsStatus(self, name):
        """
        Public method used to view the status of files/directories in the
        Mercurial repository.
        
        @param name file/directory name(s) to show the status of
            (string or list of strings)
        """
        if self.status is None:
            from .HgStatusDialog import HgStatusDialog
            self.status = HgStatusDialog(self)
        self.status.show()
        self.status.raise_()
        self.status.start(name)
    
    def hgSummary(self, mq=False, largefiles=False):
        """
        Public method used to show some summary information of the
        working directory state.
        
        @param mq flag indicating to show the queue status as well (boolean)
        @param largefiles flag indicating to show the largefiles status as
            well (boolean)
        """
        if self.summary is None:
            from .HgSummaryDialog import HgSummaryDialog
            self.summary = HgSummaryDialog(self)
        self.summary.show()
        self.summary.raise_()
        self.summary.start(mq=mq, largefiles=largefiles)
    
    def vcsTag(self, name=None, revision=None, tagName=None):
        """
        Public method used to set/remove a tag in the Mercurial repository.
        
        @param name file/directory name to determine the repo root from
            (string)
        @param revision revision to set tag for (string)
        @param tagName name of the tag (string)
        @return flag indicating a performed tag action (boolean)
        """
        from .HgTagDialog import HgTagDialog
        dlg = HgTagDialog(self.hgGetTagsList(withType=True),
                          revision, tagName)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            tag, revision, tagOp, force = dlg.getParameters()
        else:
            return False
        
        args = self.initCommand("tag")
        msgPart = ""
        if tagOp in [HgTagDialog.CreateLocalTag, HgTagDialog.DeleteLocalTag]:
            args.append('--local')
            msgPart = "local "
        else:
            msgPart = "global "
        if tagOp in [HgTagDialog.DeleteGlobalTag, HgTagDialog.DeleteLocalTag]:
            args.append('--remove')
        if tagOp in [HgTagDialog.CreateGlobalTag, HgTagDialog.CreateLocalTag]:
            if revision:
                args.append("--rev")
                args.append(revision)
        if force:
            args.append("--force")
        args.append('--message')
        if tagOp in [HgTagDialog.CreateGlobalTag, HgTagDialog.CreateLocalTag]:
            tag = tag.strip().replace(" ", "_")
            args.append("Created {1}tag <{0}>.".format(tag, msgPart))
        else:
            args.append("Removed {1}tag <{0}>.".format(tag, msgPart))
        args.append(tag)
        
        dia = HgDialog(self.tr('Tagging in the Mercurial repository'),
                       self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        
        return True
    
    def hgRevert(self, name):
        """
        Public method used to revert changes made to a file/directory.
        
        @param name file/directory name to be reverted (string)
        @return flag indicating, that the update contained an add
            or delete (boolean)
        """
        args = self.initCommand("revert")
        if not self.getPlugin().getPreferences("CreateBackup"):
            args.append("--no-backup")
        args.append("-v")
        if isinstance(name, list):
            self.addArguments(args, name)
            names = name[:]
        else:
            args.append(name)
            names = [name]
        
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
            dia = HgDialog(self.tr('Reverting changes'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        else:
            res = False
        
        return res
    
    def vcsMerge(self, name, rev=""):
        """
        Public method used to merge a URL/revision into the local project.
        
        @param name file/directory name to be merged
        @type str
        @param rev revision to merge with
        @type str
        """
        if not rev:
            from .HgMergeDialog import HgMergeDialog
            dlg = HgMergeDialog(self.hgGetTagsList(),
                                self.hgGetBranchesList(),
                                self.hgGetBookmarksList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                rev, force = dlg.getParameters()
            else:
                return
        else:
            force = False
        
        args = self.initCommand("merge")
        if force:
            args.append("--force")
        if self.getPlugin().getPreferences("InternalMerge"):
            args.append("--tool")
            args.append("internal:merge")
        if rev:
            args.append("--rev")
            args.append(rev)
        
        dia = HgDialog(self.tr('Merging'), self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        self.checkVCSStatus()
    
    def hgReMerge(self, name):
        """
        Public method used to merge a URL/revision into the local project.
        
        @param name file/directory name to be merged (string)
        """
        args = self.initCommand("resolve")
        if self.getPlugin().getPreferences("InternalMerge"):
            args.append("--tool")
            args.append("internal:merge")
        if isinstance(name, list):
            self.addArguments(args, name)
            names = name[:]
        else:
            args.append(name)
            names = [name]
        
        project = e5App().getObject("Project")
        names = [project.getRelativePath(nam) for nam in names]
        if names[0]:
            from UI.DeleteFilesConfirmationDialog import (
                DeleteFilesConfirmationDialog
            )
            dlg = DeleteFilesConfirmationDialog(
                self.parent(),
                self.tr("Re-Merge"),
                self.tr(
                    "Do you really want to re-merge these files"
                    " or directories?"),
                names)
            yes = dlg.exec() == QDialog.DialogCode.Accepted
        else:
            yes = E5MessageBox.yesNo(
                None,
                self.tr("Re-Merge"),
                self.tr("""Do you really want to re-merge the project?"""))
        if yes:
            dia = HgDialog(self.tr('Re-Merging').format(name), self)
            res = dia.startProcess(args)
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
        from .HgRevisionSelectionDialog import HgRevisionSelectionDialog
        dlg = HgRevisionSelectionDialog(self.hgGetTagsList(),
                                        self.hgGetBranchesList(),
                                        self.hgGetBookmarksList(),
                                        self.tr("Current branch tip"))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            rev = dlg.getRevision()
            return self.vcsUpdate(name, revision=rev)
        
        return False

    def vcsRegisteredState(self, name):
        """
        Public method used to get the registered state of a file in the vcs.
        
        @param name file or directory name to check
        @type str
        @return a combination of canBeCommited and canBeAdded
        @rtype int
        """
        if name.endswith(os.sep):
            name = name[:-1]
        name = os.path.normcase(name)
        
        if (
            os.path.isdir(name) and
            os.path.isdir(os.path.join(name, self.adminDir))
        ):
            return self.canBeCommitted
        
        if name in self.statusCache:
            return self.statusCache[name]
        args = self.initCommand("status")
        args.append('--all')
        args.append('--noninteractive')
        
        output, error = self.__client.runcommand(args)
        
        if output:
            repodir = self.getClient().getRepository()
            for line in output.splitlines():
                if len(line) > 2 and line[0] in "MARC!?I" and line[1] == " ":
                    flag, path = line.split(" ", 1)
                    absname = Utilities.normcasepath(
                        os.path.join(repodir, path))
                    if flag not in "?I" and absname == name:
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
        
        found = False
        for name in list(self.statusCache.keys()):
            if name in names:
                found = True
                names[name] = self.statusCache[name]
        
        if not found:
            args = self.initCommand("status")
            args.append('--all')
            args.append('--noninteractive')
            
            output, error = self.__client.runcommand(args)
            
            if output:
                repoPath = self.getClient().getRepository()
                dirs = [x for x in names.keys() if os.path.isdir(x)]
                for line in output.splitlines():
                    if line and line[0] in "MARC!?I":
                        flag, path = line.split(" ", 1)
                        name = os.path.normcase(os.path.join(repoPath, path))
                        dirName = os.path.dirname(name)
                        if name.startswith(dname):
                            if flag not in "?I":
                                if name in names:
                                    names[name] = self.canBeCommitted
                                if dirName in names:
                                    names[dirName] = self.canBeCommitted
                                if dirs:
                                    for d in dirs:
                                        if name.startswith(d):
                                            names[d] = self.canBeCommitted
                                            dirs.remove(d)
                                            break
                        if flag not in "?I":
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
        
        @return always 'Mercurial' (string)
        """
        return "Mercurial"
    
    def vcsInitConfig(self, project):
        """
        Public method to initialize the VCS configuration.
        
        This method ensures, that an ignore file exists.
        
        @param project reference to the project (Project)
        """
        ppath = project.getProjectPath()
        if ppath:
            ignoreName = os.path.join(ppath, Hg.IgnoreFileName)
            if not os.path.exists(ignoreName):
                self.hgCreateIgnoreFile(project.getProjectPath(), autoAdd=True)
    
    def vcsCleanup(self, name):
        """
        Public method used to cleanup the working directory.
        
        @param name directory name to be cleaned up (string)
        """
        patterns = self.getPlugin().getPreferences("CleanupPatterns").split()
        
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
        Public method used to execute arbitrary mercurial commands.
        
        @param name directory name of the working directory (string)
        """
        from .HgCommandDialog import HgCommandDialog
        dlg = HgCommandDialog(self.commandHistory, name)
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
            
            dia = HgDialog(self.tr('Mercurial command'), self)
            res = dia.startProcess(args)
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
        @return reference to the instantiated options dialog (HgOptionsDialog)
        """
        from .HgOptionsDialog import HgOptionsDialog
        return HgOptionsDialog(self, project, parent)
    
    def vcsNewProjectOptionsDialog(self, parent=None):
        """
        Public method to get a dialog to enter repository info for getting a
        new project.
        
        @param parent parent widget (QWidget)
        @return reference to the instantiated options dialog
            (HgNewProjectOptionsDialog)
        """
        from .HgNewProjectOptionsDialog import HgNewProjectOptionsDialog
        return HgNewProjectOptionsDialog(self, parent)
    
    def vcsRepositoryInfos(self, ppath):
        """
        Public method to retrieve information about the repository.
        
        @param ppath local path to get the repository infos (string)
        @return string with ready formated info for display (string)
        """
        args = self.initCommand("parents")
        args.append('--template')
        args.append('{rev}:{node|short}@@@{tags}@@@{author|xmlescape}@@@'
                    '{date|isodate}@@@{branches}@@@{bookmarks}\n')
        
        output, error = self.__client.runcommand(args)
        
        infoBlock = []
        if output:
            index = 0
            for line in output.splitlines():
                index += 1
                (changeset, tags, author, date, branches,
                 bookmarks) = line.split("@@@")
                cdate, ctime = date.split()[:2]
                info = []
                info.append(QCoreApplication.translate(
                    "mercurial",
                    """<tr><td><b>Parent #{0}</b></td><td></td></tr>\n"""
                    """<tr><td><b>Changeset</b></td><td>{1}</td></tr>""")
                    .format(index, changeset))
                if tags:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Tags</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(tags.split())))
                if bookmarks:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Bookmarks</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(bookmarks.split())))
                if branches:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Branches</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(branches.split())))
                info.append(QCoreApplication.translate(
                    "mercurial",
                    """<tr><td><b>Last author</b></td><td>{0}</td></tr>\n"""
                    """<tr><td><b>Committed date</b></td><td>{1}</td></tr>\n"""
                    """<tr><td><b>Committed time</b></td><td>{2}</td></tr>""")
                    .format(author, cdate, ctime))
                infoBlock.append("\n".join(info))
        if infoBlock:
            infoStr = """<tr></tr>{0}""".format("<tr></tr>".join(infoBlock))
        else:
            infoStr = ""
        
        url = ""
        args = self.initCommand("showconfig")
        args.append('paths.default')
        
        output, error = self.__client.runcommand(args)
        
        if output:
            url = output.splitlines()[0].strip()
        else:
            url = ""
        
        return QCoreApplication.translate(
            'mercurial',
            """<h3>Repository information</h3>\n"""
            """<p><table>\n"""
            """<tr><td><b>Mercurial V.</b></td><td>{0}</td></tr>\n"""
            """<tr></tr>\n"""
            """<tr><td><b>URL</b></td><td>{1}</td></tr>\n"""
            """{2}"""
            """</table></p>\n"""
        ).format(self.versionStr, url, infoStr)
    
    def vcsSupportCommandOptions(self):
        """
        Public method to signal the support of user settable command options.
        
        @return flag indicating the support  of user settable command options
            (boolean)
        """
        return False
    
    ###########################################################################
    ## Private Mercurial specific methods are below.
    ###########################################################################
    
    def hgNormalizeURL(self, url):
        """
        Public method to normalize a url for Mercurial.
        
        @param url url string (string)
        @return properly normalized url for mercurial (string)
        """
        url = url.replace('\\', '/')
        if url.endswith('/'):
            url = url[:-1]
        urll = url.split('//')
        return "{0}//{1}".format(urll[0], '/'.join(urll[1:]))
    
    def hgCopy(self, name, project):
        """
        Public method used to copy a file/directory.
        
        @param name file/directory name to be copied (string)
        @param project reference to the project object
        @return flag indicating successful operation (boolean)
        """
        from .HgCopyDialog import HgCopyDialog
        dlg = HgCopyDialog(name)
        res = False
        if dlg.exec() == QDialog.DialogCode.Accepted:
            target, force = dlg.getData()
            
            args = self.initCommand("copy")
            args.append("-v")
            args.append(name)
            args.append(target)
            
            dia = HgDialog(
                self.tr('Copying {0}').format(name), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.normalExit()
                if (
                    res and
                    target.startswith(project.getProjectPath())
                ):
                    if os.path.isdir(name):
                        project.copyDirectory(name, target)
                    else:
                        project.appendFile(target)
        return res
    
    def hgGetTagsList(self, withType=False):
        """
        Public method to get the list of tags.
        
        @param withType flag indicating to get the tag type as well (boolean)
        @return list of tags (list of string) or list of tuples of
            tag name and flag indicating a local tag (list of tuple of string
            and boolean), if withType is True
        """
        args = self.initCommand("tags")
        args.append('--verbose')
        
        output, error = self.__client.runcommand(args)
        
        tagsList = []
        if output:
            for line in output.splitlines():
                li = line.strip().split()
                if li[-1][0] in "1234567890":
                    # last element is a rev:changeset
                    del li[-1]
                    isLocal = False
                else:
                    del li[-2:]
                    isLocal = True
                name = " ".join(li)
                if name not in ["tip", "default"]:
                    if withType:
                        tagsList.append((name, isLocal))
                    else:
                        tagsList.append(name)
        
        if withType:
            return tagsList
        else:
            if tagsList:
                self.tagsList = tagsList
            return self.tagsList[:]
    
    def hgGetBranchesList(self):
        """
        Public method to get the list of branches.
        
        @return list of branches (list of string)
        """
        args = self.initCommand("branches")
        args.append('--closed')
        
        output, error = self.__client.runcommand(args)
        
        if output:
            self.branchesList = []
            for line in output.splitlines():
                li = line.strip().split()
                if li[-1][0] in "1234567890":
                    # last element is a rev:changeset
                    del li[-1]
                else:
                    del li[-2:]
                name = " ".join(li)
                if name not in ["tip", "default"]:
                    self.branchesList.append(name)
        
        return self.branchesList[:]
    
    def hgListTagBranch(self, tags=True):
        """
        Public method used to list the available tags or branches.
        
        @param tags flag indicating listing of branches or tags
                (False = branches, True = tags)
        """
        from .HgTagBranchListDialog import HgTagBranchListDialog
        self.tagbranchList = HgTagBranchListDialog(self)
        self.tagbranchList.show()
        if tags:
            if not self.showedTags:
                self.showedTags = True
                allTagsBranchesList = self.allTagsBranchesList
            else:
                self.tagsList = []
                allTagsBranchesList = None
            self.tagbranchList.start(
                tags, self.tagsList, allTagsBranchesList)
        else:
            if not self.showedBranches:
                self.showedBranches = True
                allTagsBranchesList = self.allTagsBranchesList
            else:
                self.branchesList = []
                allTagsBranchesList = None
            self.tagbranchList.start(
                tags, self.branchesList, self.allTagsBranchesList)
    
    def hgAnnotate(self, name):
        """
        Public method to show the output of the hg annotate command.
        
        @param name file name to show the annotations for (string)
        """
        if self.annotate is None:
            from .HgAnnotateDialog import HgAnnotateDialog
            self.annotate = HgAnnotateDialog(self)
        self.annotate.show()
        self.annotate.raise_()
        self.annotate.start(name)
    
    def hgExtendedDiff(self, name):
        """
        Public method used to view the difference of a file/directory to the
        Mercurial repository.
        
        If name is a directory and is the project directory, all project files
        are saved first. If name is a file (or list of files), which is/are
        being edited and has unsaved modification, they can be saved or the
        operation may be aborted.
        
        This method gives the chance to enter the revisions to be compared.
        
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
        
        from .HgRevisionsSelectionDialog import HgRevisionsSelectionDialog
        dlg = HgRevisionsSelectionDialog(self.hgGetTagsList(),
                                         self.hgGetBranchesList(),
                                         self.hgGetBookmarksList())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            revisions = dlg.getRevisions()
            if self.diff is None:
                from .HgDiffDialog import HgDiffDialog
                self.diff = HgDiffDialog(self)
            self.diff.show()
            self.diff.raise_()
            self.diff.start(name, revisions)
    
    def __hgGetFileForRevision(self, name, rev=""):
        """
        Private method to get a file for a specific revision from the
        repository.
        
        @param name file name to get from the repository (string)
        @param rev revision to retrieve (string)
        @return contents of the file (string) and an error message (string)
        """
        args = self.initCommand("cat")
        if rev:
            args.append("--rev")
            args.append(rev)
        args.append(name)
        
        output, error = self.__client.runcommand(args)
        
        # return file contents with 'universal newlines'
        return output.replace('\r\n', '\n').replace('\r', '\n'), error
    
    def hgSbsDiff(self, name, extended=False, revisions=None):
        """
        Public method used to view the difference of a file to the Mercurial
        repository side-by-side.
        
        @param name file name to be diffed (string)
        @param extended flag indicating the extended variant (boolean)
        @param revisions tuple of two revisions (tuple of strings)
        @exception ValueError raised to indicate an invalid name parameter
        """
        if isinstance(name, list):
            raise ValueError("Wrong parameter type")
        
        if extended:
            from .HgRevisionsSelectionDialog import HgRevisionsSelectionDialog
            dlg = HgRevisionsSelectionDialog(self.hgGetTagsList(),
                                             self.hgGetBranchesList(),
                                             self.hgGetBookmarksList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                rev1, rev2 = dlg.getRevisions()
            else:
                return
        elif revisions:
            rev1, rev2 = revisions[0], revisions[1]
        else:
            rev1, rev2 = "", ""
        
        output1, error = self.__hgGetFileForRevision(name, rev=rev1)
        if error:
            E5MessageBox.critical(
                self.__ui,
                self.tr("Mercurial Side-by-Side Difference"),
                error)
            return
        name1 = "{0} (rev. {1})".format(name, rev1 and rev1 or ".")
        
        if rev2:
            output2, error = self.__hgGetFileForRevision(name, rev=rev2)
            if error:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Mercurial Side-by-Side Difference"),
                    error)
                return
            name2 = "{0} (rev. {1})".format(name, rev2)
        else:
            try:
                with open(name, "r", encoding="utf-8") as f1:
                    output2 = f1.read()
                name2 = "{0} (Work)".format(name)
            except OSError:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Mercurial Side-by-Side Difference"),
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
    
    def vcsLogBrowser(self, name=None, isFile=False):
        """
        Public method used to browse the log of a file/directory from the
        Mercurial repository.
        
        @param name file/directory name to show the log of (string)
        @param isFile flag indicating log for a file is to be shown
            (boolean)
        """
        if name == self.getClient().getRepository():
            name = None
        
        if self.logBrowser is None:
            from .HgLogBrowserDialog import HgLogBrowserDialog
            self.logBrowser = HgLogBrowserDialog(self)
        self.logBrowser.show()
        self.logBrowser.raise_()
        self.logBrowser.start(name=name, isFile=isFile)
    
    def hgIncoming(self):
        """
        Public method used to view the log of incoming changes from the
        Mercurial repository.
        """
        if self.logBrowserIncoming is None:
            from .HgLogBrowserDialog import HgLogBrowserDialog
            self.logBrowserIncoming = HgLogBrowserDialog(
                self, mode="incoming")
        self.logBrowserIncoming.show()
        self.logBrowserIncoming.raise_()
        self.logBrowserIncoming.start()
    
    def hgOutgoing(self):
        """
        Public method used to view the log of outgoing changes from the
        Mercurial repository.
        """
        if self.logBrowserOutgoing is None:
            from .HgLogBrowserDialog import HgLogBrowserDialog
            self.logBrowserOutgoing = HgLogBrowserDialog(
                self, mode="outgoing")
        self.logBrowserOutgoing.show()
        self.logBrowserOutgoing.raise_()
        self.logBrowserOutgoing.start()
    
    def hgPull(self, revisions=None):
        """
        Public method used to pull changes from a remote Mercurial repository.
        
        @param revisions list of revisions to be pulled
        @type list of str
        @return flag indicating, that the update contained an add
            or delete
        @rtype bool
        """
        if (
            self.getPlugin().getPreferences("PreferUnbundle") and
            self.bundleFile and
            os.path.exists(self.bundleFile) and
            revisions is None
        ):
            command = "unbundle"
            title = self.tr('Apply changegroups')
        else:
            command = "pull"
            title = self.tr('Pulling from a remote Mercurial repository')
        
        args = self.initCommand(command)
        args.append('-v')
        if self.getPlugin().getPreferences("PullUpdate"):
            args.append('--update')
        if command == "unbundle":
            args.append(self.bundleFile)
        if revisions:
            for rev in revisions:
                args.append("--rev")
                args.append(rev)
        
        dia = HgDialog(title, self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        if (
            self.bundleFile and
            os.path.exists(self.bundleFile)
        ):
            os.remove(self.bundleFile)
            self.bundleFile = None
        self.checkVCSStatus()
        return res
    
    def hgPush(self, force=False, newBranch=False, rev=None):
        """
        Public method used to push changes to a remote Mercurial repository.
        
        @param force flag indicating a forced push (boolean)
        @param newBranch flag indicating to push a new branch (boolean)
        @param rev revision to be pushed (including all ancestors) (string)
        """
        args = self.initCommand("push")
        args.append('-v')
        if force:
            args.append('-f')
        if newBranch:
            args.append('--new-branch')
        if rev:
            args.append('--rev')
            args.append(rev)
        
        dia = HgDialog(
            self.tr('Pushing to a remote Mercurial repository'), self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        self.checkVCSStatus()
    
    def hgInfo(self, mode="heads"):
        """
        Public method to show information about the heads of the repository.
        
        @param mode mode of the operation (string, one of heads, parents,
            tip)
        """
        if mode not in ("heads", "parents", "tip"):
            mode = "heads"
        
        info = []
        
        args = self.initCommand(mode)
        args.append('--template')
        args.append('{rev}:{node|short}@@@{tags}@@@{author|xmlescape}@@@'
                    '{date|isodate}@@@{branches}@@@{parents}@@@{bookmarks}\n')
        
        output, error = self.__client.runcommand(args)
        
        if output:
            index = 0
            for line in output.splitlines():
                index += 1
                (changeset, tags, author, date, branches, parents,
                 bookmarks) = line.split("@@@")
                cdate, ctime = date.split()[:2]
                info.append("""<p><table>""")
                if mode == "heads":
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Head #{0}</b></td><td></td></tr>\n""")
                        .format(index))
                elif mode == "parents":
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Parent #{0}</b></td><td></td></tr>\n""")
                        .format(index))
                elif mode == "tip":
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Tip</b></td><td></td></tr>\n"""))
                info.append(QCoreApplication.translate(
                    "mercurial",
                    """<tr><td><b>Changeset</b></td><td>{0}</td></tr>""")
                    .format(changeset))
                if tags:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Tags</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(tags.split())))
                if bookmarks:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Bookmarks</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(bookmarks.split())))
                if branches:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Branches</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(branches.split())))
                if parents:
                    info.append(QCoreApplication.translate(
                        "mercurial",
                        """<tr><td><b>Parents</b></td><td>{0}</td></tr>""")
                        .format('<br/>'.join(parents.split())))
                info.append(QCoreApplication.translate(
                    "mercurial",
                    """<tr><td><b>Last author</b></td><td>{0}</td></tr>\n"""
                    """<tr><td><b>Committed date</b></td><td>{1}</td></tr>\n"""
                    """<tr><td><b>Committed time</b></td><td>{2}</td></tr>\n"""
                    """</table></p>""")
                    .format(author, cdate, ctime))
            
            dlg = VcsRepositoryInfoDialog(None, "\n".join(info))
            dlg.exec()
    
    def hgConflicts(self):
        """
        Public method used to show a list of files containing conflicts.
        """
        if self.conflictsDlg is None:
            from .HgConflictsListDialog import HgConflictsListDialog
            self.conflictsDlg = HgConflictsListDialog(self)
        self.conflictsDlg.show()
        self.conflictsDlg.raise_()
        self.conflictsDlg.start()
    
    def hgResolved(self, name, unresolve=False):
        """
        Public method used to resolve conflicts of a file/directory.
        
        @param name file/directory name to be resolved (string)
        @param unresolve flag indicating to mark the file/directory as
            unresolved (boolean)
        """
        args = self.initCommand("resolve")
        if unresolve:
            args.append("--unmark")
        else:
            args.append("--mark")
        
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        if unresolve:
            title = self.tr("Marking as 'unresolved'")
        else:
            title = self.tr("Marking as 'resolved'")
        dia = HgDialog(title, self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
        self.checkVCSStatus()
    
    def hgAbortMerge(self):
        """
        Public method to abort an uncommitted merge.
        
        @return flag indicating, that the abortion contained an add
            or delete (boolean)
        """
        if self.version >= (4, 5, 0):
            args = self.initCommand("merge")
            args.append("--abort")
        else:
            args = self.initCommand("update")
            args.append("--clean")
        
        dia = HgDialog(
            self.tr('Aborting uncommitted merge'),
            self)
        res = dia.startProcess(args, showArgs=False)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
        self.checkVCSStatus()
        return res
    
    def hgBranch(self):
        """
        Public method used to create a branch in the Mercurial repository.
        """
        from .HgBranchInputDialog import HgBranchInputDialog
        dlg = HgBranchInputDialog(self.hgGetBranchesList())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, commit = dlg.getData()
            name = name.strip().replace(" ", "_")
            args = self.initCommand("branch")
            args.append(name)
            
            dia = HgDialog(
                self.tr('Creating branch in the Mercurial repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                if commit:
                    self.vcsCommit(
                        name,
                        self.tr("Created new branch <{0}>.").format(
                            name))
    
    def hgShowBranch(self):
        """
        Public method used to show the current branch of the working directory.
        """
        args = self.initCommand("branch")
        
        dia = HgDialog(self.tr('Showing current branch'), self)
        res = dia.startProcess(args, showArgs=False)
        if res:
            dia.exec()
    
    def hgGetCurrentBranch(self):
        """
        Public method to get the current branch of the working directory.
        
        @return name of the current branch
        @rtype str
        """
        args = self.initCommand("branch")
        
        output, error = self.__client.runcommand(args)
        
        return output.strip()
    
    def hgEditUserConfig(self):
        """
        Public method used to edit the user configuration file.
        """
        from .HgUserConfigDialog import HgUserConfigDialog
        dlg = HgUserConfigDialog(version=self.version)
        dlg.exec()
    
    def hgEditConfig(self, repoName=None,
                     withLargefiles=True, largefilesData=None):
        """
        Public method used to edit the repository configuration file.
        
        @param repoName directory name containing the repository
        @type str
        @param withLargefiles flag indicating to configure the largefiles
            section
        @type bool
        @param largefilesData dictionary with data for the largefiles
            section of the data dialog
        @type dict
        """
        if repoName is None:
            repoName = self.getClient().getRepository()
        
        cfgFile = os.path.join(repoName, self.adminDir, "hgrc")
        if not os.path.exists(cfgFile):
            # open dialog to enter the initial data
            withLargefiles = (self.isExtensionActive("largefiles") and
                              withLargefiles)
            from .HgRepoConfigDataDialog import HgRepoConfigDataDialog
            dlg = HgRepoConfigDataDialog(withLargefiles=withLargefiles,
                                         largefilesData=largefilesData)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                createContents = True
                defaultUrl, defaultPushUrl = dlg.getData()
                if withLargefiles:
                    lfMinSize, lfPattern = dlg.getLargefilesData()
            else:
                createContents = False
            try:
                with open(cfgFile, "w") as cfg:
                    if createContents:
                        # write the data entered
                        cfg.write("[paths]\n")
                        if defaultUrl:
                            cfg.write("default = {0}\n".format(defaultUrl))
                        if defaultPushUrl:
                            cfg.write("default-push = {0}\n".format(
                                defaultPushUrl))
                        if (
                            withLargefiles and
                            (lfMinSize, lfPattern) != (None, None)
                        ):
                            cfg.write("\n[largefiles]\n")
                            if lfMinSize is not None:
                                cfg.write("minsize = {0}\n".format(lfMinSize))
                            if lfPattern is not None:
                                cfg.write("patterns =\n")
                                cfg.write("  {0}\n".format(
                                    "\n  ".join(lfPattern)))
                self.__monitorRepoIniFile(repoName)
                self.__iniFileChanged(cfgFile)
            except OSError:
                pass
        self.repoEditor = MiniEditor(cfgFile, "Properties")
        self.repoEditor.show()
    
    def hgVerify(self):
        """
        Public method to verify the integrity of the repository.
        """
        args = self.initCommand("verify")
        
        dia = HgDialog(
            self.tr('Verifying the integrity of the Mercurial repository'),
            self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
    
    def hgShowConfig(self):
        """
        Public method to show the combined configuration.
        """
        args = self.initCommand("showconfig")
        args.append("--untrusted")
        
        dia = HgDialog(
            self.tr('Showing the combined configuration settings'),
            self)
        res = dia.startProcess(args, showArgs=False)
        if res:
            dia.exec()
    
    def hgShowPaths(self):
        """
        Public method to show the path aliases for remote repositories.
        """
        args = self.initCommand("paths")
        
        dia = HgDialog(
            self.tr('Showing aliases for remote repositories'),
            self)
        res = dia.startProcess(args, showArgs=False)
        if res:
            dia.exec()
    
    def hgRecover(self):
        """
        Public method to recover an interrupted transaction.
        """
        args = self.initCommand("recover")
        
        dia = HgDialog(
            self.tr('Recovering from interrupted transaction'),
            self)
        res = dia.startProcess(args, showArgs=False)
        if res:
            dia.exec()
    
    def hgIdentify(self):
        """
        Public method to identify the current working directory.
        """
        args = self.initCommand("identify")
        
        dia = HgDialog(self.tr('Identifying project directory'), self)
        res = dia.startProcess(args, showArgs=False)
        if res:
            dia.exec()
    
    def hgCreateIgnoreFile(self, name, autoAdd=False):
        """
        Public method to create the ignore file.
        
        @param name directory name to create the ignore file in (string)
        @param autoAdd flag indicating to add it automatically (boolean)
        @return flag indicating success
        """
        status = False
        ignorePatterns = [
            "glob:.eric6project",
            "glob:.ropeproject",
            "glob:.directory",
            "glob:**.pyc",
            "glob:**.pyo",
            "glob:**.orig",
            "glob:**.bak",
            "glob:**.rej",
            "glob:**~",
            "glob:cur",
            "glob:tmp",
            "glob:__pycache__",
            "glob:**.DS_Store",
        ]
        
        ignoreName = os.path.join(name, Hg.IgnoreFileName)
        if os.path.exists(ignoreName):
            res = E5MessageBox.yesNo(
                self.__ui,
                self.tr("Create .hgignore file"),
                self.tr("""<p>The file <b>{0}</b> exists already."""
                        """ Overwrite it?</p>""").format(ignoreName),
                icon=E5MessageBox.Warning)
        else:
            res = True
        if res:
            try:
                # create a .hgignore file
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
    
    def hgBundle(self, bundleData=None):
        """
        Public method to create a changegroup file.
        
        @param bundleData dictionary containing the bundle creation information
        @type dict
        """
        if bundleData is None:
            from .HgBundleDialog import HgBundleDialog
            dlg = HgBundleDialog(self.hgGetTagsList(),
                                 self.hgGetBranchesList(),
                                 self.hgGetBookmarksList(),
                                 version=self.version)
            if dlg.exec() != QDialog.DialogCode.Accepted:
                return
            
            revs, baseRevs, compression, bundleAll = dlg.getParameters()
        else:
            revs = bundleData["revs"]
            if bundleData["base"]:
                baseRevs = [bundleData["base"]]
            else:
                baseRevs = []
            compression = ""
            bundleAll = bundleData["all"]
        
        fname, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
            None,
            self.tr("Create changegroup"),
            self.__lastChangeGroupPath,
            self.tr("Mercurial Changegroup Files (*.hg)"),
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
                self.tr("Create changegroup"),
                self.tr("<p>The Mercurial changegroup file <b>{0}</b> "
                        "already exists. Overwrite it?</p>")
                    .format(fname),
                icon=E5MessageBox.Warning)
            if not res:
                return
        fname = Utilities.toNativeSeparators(fname)
        self.__lastChangeGroupPath = os.path.dirname(fname)
        
        args = self.initCommand("bundle")
        if bundleAll:
            args.append("--all")
        for rev in revs:
            args.append("--rev")
            args.append(rev)
        for baseRev in baseRevs:
            args.append("--base")
            args.append(baseRev)
        if compression:
            args.append("--type")
            args.append(compression)
        args.append(fname)
        
        dia = HgDialog(self.tr('Create changegroup'), self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
    
    def hgPreviewBundle(self):
        """
        Public method used to view the log of incoming changes from a
        changegroup file.
        """
        file = E5FileDialog.getOpenFileName(
            None,
            self.tr("Preview changegroup"),
            self.__lastChangeGroupPath,
            self.tr("Mercurial Changegroup Files (*.hg);;All Files (*)"))
        if file:
            self.__lastChangeGroupPath = os.path.dirname(file)
            
            if self.logBrowserIncoming is None:
                from .HgLogBrowserDialog import HgLogBrowserDialog
                self.logBrowserIncoming = HgLogBrowserDialog(
                    self, mode="incoming")
            self.logBrowserIncoming.show()
            self.logBrowserIncoming.raise_()
            self.logBrowserIncoming.start(bundle=file)
    
    def hgUnbundle(self, files=None):
        """
        Public method to apply changegroup files.
        
        @param files list of bundle files to be applied
        @type list of str
        @return flag indicating, that the update contained an add
            or delete
        @rtype bool
        """
        res = False
        if not files:
            files = E5FileDialog.getOpenFileNames(
                None,
                self.tr("Apply changegroups"),
                self.__lastChangeGroupPath,
                self.tr("Mercurial Changegroup Files (*.hg);;All Files (*)"))
        
        if files:
            self.__lastChangeGroupPath = os.path.dirname(files[0])
            
            update = E5MessageBox.yesNo(
                self.__ui,
                self.tr("Apply changegroups"),
                self.tr("""Shall the working directory be updated?"""),
                yesDefault=True)
            
            args = self.initCommand("unbundle")
            if update:
                args.append("--update")
                args.append("--verbose")
            args.extend(files)
            
            dia = HgDialog(self.tr('Apply changegroups'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        
        return res
    
    def hgBisect(self, subcommand):
        """
        Public method to perform bisect commands.
        
        @param subcommand name of the subcommand (one of 'good', 'bad',
            'skip' or 'reset')
        @type str
        @exception ValueError raised to indicate an invalid bisect subcommand
        """
        if subcommand not in ("good", "bad", "skip", "reset"):
            raise ValueError(
                self.tr("Bisect subcommand ({0}) invalid.")
                    .format(subcommand))
        
        rev = ""
        if subcommand in ("good", "bad", "skip"):
            from .HgRevisionSelectionDialog import HgRevisionSelectionDialog
            dlg = HgRevisionSelectionDialog(self.hgGetTagsList(),
                                            self.hgGetBranchesList(),
                                            self.hgGetBookmarksList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                rev = dlg.getRevision()
            else:
                return
        
        args = self.initCommand("bisect")
        args.append("--{0}".format(subcommand))
        if rev:
            args.append(rev)
        
        dia = HgDialog(
            self.tr('Mercurial Bisect ({0})').format(subcommand), self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
    
    def hgForget(self, name):
        """
        Public method used to remove a file from the Mercurial repository.
        
        This will not remove the file from the project directory.
        
        @param name file/directory name to be removed (string or list of
            strings))
        """
        args = self.initCommand("forget")
        args.append('-v')
        
        if isinstance(name, list):
            self.addArguments(args, name)
        else:
            args.append(name)
        
        dia = HgDialog(
            self.tr('Removing files from the Mercurial repository only'),
            self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            if isinstance(name, list):
                self.__forgotNames.extend(name)
            else:
                self.__forgotNames.append(name)
    
    def hgBackout(self):
        """
        Public method used to backout an earlier changeset from the Mercurial
        repository.
        """
        from .HgBackoutDialog import HgBackoutDialog
        dlg = HgBackoutDialog(self.hgGetTagsList(),
                              self.hgGetBranchesList(),
                              self.hgGetBookmarksList())
        if dlg.exec() == QDialog.DialogCode.Accepted:
            rev, merge, date, user, message = dlg.getParameters()
            if not rev:
                E5MessageBox.warning(
                    self.__ui,
                    self.tr("Backing out changeset"),
                    self.tr("""No revision given. Aborting..."""))
                return
            
            args = self.initCommand("backout")
            args.append('-v')
            if merge:
                args.append('--merge')
            if date:
                args.append('--date')
                args.append(date)
            if user:
                args.append('--user')
                args.append(user)
            args.append('--message')
            args.append(message)
            args.append(rev)
            
            dia = HgDialog(self.tr('Backing out changeset'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgRollback(self):
        """
        Public method used to rollback the last transaction.
        """
        res = E5MessageBox.yesNo(
            None,
            self.tr("Rollback last transaction"),
            self.tr("""Are you sure you want to rollback the last"""
                    """ transaction?"""),
            icon=E5MessageBox.Warning)
        if res:
            dia = HgDialog(self.tr('Rollback last transaction'), self)
            res = dia.startProcess(["rollback"])
            if res:
                dia.exec()

    def hgServe(self, repoPath):
        """
        Public method used to serve the project.
        
        @param repoPath directory containing the repository
        @type str
        """
        from .HgServeDialog import HgServeDialog
        self.serveDlg = HgServeDialog(self, repoPath)
        self.serveDlg.show()
    
    def hgImport(self):
        """
        Public method to import a patch file.
        
        @return flag indicating, that the import contained an add, a delete
            or a change to the project file (boolean)
        """
        from .HgImportDialog import HgImportDialog
        dlg = HgImportDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (patchFile, noCommit, message, date, user, withSecret, stripCount,
             force) = dlg.getParameters()
            
            args = self.initCommand("import")
            args.append("--verbose")
            if noCommit:
                args.append("--no-commit")
            else:
                if message:
                    args.append('--message')
                    args.append(message)
                if date:
                    args.append('--date')
                    args.append(date)
                if user:
                    args.append('--user')
                    args.append(user)
            if stripCount != 1:
                args.append("--strip")
                args.append(str(stripCount))
            if force:
                args.append("--force")
            if withSecret:
                args.append("--secret")
            args.append(patchFile)
            
            dia = HgDialog(self.tr("Import Patch"), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        else:
            res = False
        
        return res
    
    def hgExport(self):
        """
        Public method to export patches to files.
        """
        from .HgExportDialog import HgExportDialog
        dlg = HgExportDialog(self.hgGetBookmarksList(),
                             self.version >= (4, 7, 0))
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (filePattern, revisions, bookmark, switchParent, allText,
             noDates, git) = dlg.getParameters()
            
            args = self.initCommand("export")
            args.append("--output")
            args.append(filePattern)
            args.append("--verbose")
            if switchParent:
                args.append("--switch-parent")
            if allText:
                args.append("--text")
            if noDates:
                args.append("--nodates")
            if git:
                args.append("--git")
            if bookmark:
                args.append("--bookmark")
                args.append(bookmark)
            else:
                for rev in revisions:
                    args.append(rev)
            
            dia = HgDialog(self.tr("Export Patches"), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgPhase(self, data=None):
        """
        Public method to change the phase of revisions.
        
        @param data tuple giving phase data (list of revisions, phase, flag
            indicating a forced operation) (list of strings, string, boolean)
        @return flag indicating success (boolean)
        @exception ValueError raised to indicate an invalid phase
        """
        if data is None:
            from .HgPhaseDialog import HgPhaseDialog
            dlg = HgPhaseDialog()
            if dlg.exec() == QDialog.DialogCode.Accepted:
                data = dlg.getData()
        
        if data:
            revs, phase, force = data
            
            args = self.initCommand("phase")
            if phase == "p":
                args.append("--public")
            elif phase == "d":
                args.append("--draft")
            elif phase == "s":
                args.append("--secret")
            else:
                raise ValueError("Invalid phase given.")
            if force:
                args.append("--force")
            for rev in revs:
                args.append(rev)
            
            dia = HgDialog(self.tr("Change Phase"), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.normalExitWithoutErrors()
        else:
            res = False
        
        return res
    
    def hgGraft(self, revs=None):
        """
        Public method to copy changesets from another branch.
        
        @param revs list of revisions to show in the revisions pane (list of
            strings)
        @return flag indicating that the project should be reread (boolean)
        """
        from .HgGraftDialog import HgGraftDialog
        res = False
        dlg = HgGraftDialog(self, revs)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (revs,
             (userData, currentUser, userName),
             (dateData, currentDate, dateStr),
             log, dryrun, noCommit) = dlg.getData()
            
            args = self.initCommand("graft")
            args.append("--verbose")
            if userData:
                if currentUser:
                    args.append("--currentuser")
                else:
                    args.append("--user")
                    args.append(userName)
            if dateData:
                if currentDate:
                    args.append("--currentdate")
                else:
                    args.append("--date")
                    args.append(dateStr)
            if log:
                args.append("--log")
            if dryrun:
                args.append("--dry-run")
            if noCommit:
                args.append("--no-commit")
            args.extend(revs)
            
            dia = HgDialog(self.tr('Copy Changesets'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.checkVCSStatus()
        return res
    
    def __hgGraftSubCommand(self, subcommand, title):
        """
        Private method to perform a Mercurial graft subcommand.
        
        @param subcommand subcommand flag
        @type str
        @param title tirle of the dialog
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        args = self.initCommand("graft")
        args.append(subcommand)
        args.append("--verbose")
        
        dia = HgDialog(title, self)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.checkVCSStatus()
        return res
    
    def hgGraftContinue(self, path):
        """
        Public method to continue copying changesets from another branch.
        
        @param path directory name of the project
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        return self.__hgGraftSubCommand(
            "--continue", self.tr('Copy Changesets (Continue)'))
    
    def hgGraftStop(self, path):
        """
        Public method to stop an interrupted copying session.
        
        @param path directory name of the project
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        return self.__hgGraftSubCommand(
            "--stop", self.tr('Copy Changesets (Stop)'))
    
    def hgGraftAbort(self, path):
        """
        Public method to abort an interrupted copying session and perform
        a rollback.
        
        @param path directory name of the project
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        return self.__hgGraftSubCommand(
            "--abort", self.tr('Copy Changesets (Abort)'))
    
    def hgArchive(self):
        """
        Public method to create an unversioned archive from the repository.
        """
        from .HgArchiveDialog import HgArchiveDialog
        dlg = HgArchiveDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            archive, type_, prefix, subrepos = dlg.getData()
            
            args = self.initCommand("archive")
            if type_:
                args.append("--type")
                args.append(type_)
            if prefix:
                args.append("--prefix")
                args.append(prefix)
            if subrepos:
                args.append("--subrepos")
            args.append(archive)
            
            dia = HgDialog(self.tr("Create Unversioned Archive"), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgDeleteBackups(self):
        """
        Public method to delete all backup bundles in the backup area.
        """
        backupdir = os.path.join(self.getClient().getRepository(),
                                 self.adminDir, "strip-backup")
        yes = E5MessageBox.yesNo(
            self.__ui,
            self.tr("Delete All Backups"),
            self.tr("""<p>Do you really want to delete all backup bundles"""
                    """ stored the backup area <b>{0}</b>?</p>""").format(
                backupdir))
        if yes:
            shutil.rmtree(backupdir, True)
    
    ###########################################################################
    ## Methods to deal with sub-repositories are below.
    ###########################################################################
    
    def getHgSubPath(self):
        """
        Public method to get the path to the .hgsub file containing the
        definitions of sub-repositories.
        
        @return full path of the .hgsub file (string)
        """
        ppath = self.__projectHelper.getProject().getProjectPath()
        return os.path.join(ppath, ".hgsub")
    
    def hasSubrepositories(self):
        """
        Public method to check, if the project might have sub-repositories.
        
        @return flag indicating the existence of sub-repositories (boolean)
        """
        hgsub = self.getHgSubPath()
        return os.path.isfile(hgsub) and os.stat(hgsub).st_size > 0
    
    def hgAddSubrepository(self):
        """
        Public method to add a sub-repository.
        """
        from .HgAddSubrepositoryDialog import HgAddSubrepositoryDialog
        ppath = self.__projectHelper.getProject().getProjectPath()
        hgsub = self.getHgSubPath()
        dlg = HgAddSubrepositoryDialog(ppath)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            relPath, subrepoType, subrepoUrl = dlg.getData()
            if subrepoType == "hg":
                url = subrepoUrl
            else:
                url = "[{0}]{1}".format(subrepoType, subrepoUrl)
            entry = "{0} = {1}\n".format(relPath, url)
            
            contents = []
            if os.path.isfile(hgsub):
                # file exists; check, if such an entry exists already
                needsAdd = False
                try:
                    with open(hgsub, "r") as f:
                        contents = f.readlines()
                except OSError as err:
                    E5MessageBox.critical(
                        self.__ui,
                        self.tr("Add Sub-repository"),
                        self.tr(
                            """<p>The sub-repositories file .hgsub could not"""
                            """ be read.</p><p>Reason: {0}</p>""")
                        .format(str(err)))
                    return
                
                if entry in contents:
                    E5MessageBox.critical(
                        self.__ui,
                        self.tr("Add Sub-repository"),
                        self.tr(
                            """<p>The sub-repositories file .hgsub already"""
                            """ contains an entry <b>{0}</b>."""
                            """ Aborting...</p>""").format(entry))
                    return
            else:
                needsAdd = True
            
            if contents and not contents[-1].endswith("\n"):
                contents[-1] = contents[-1] + "\n"
            contents.append(entry)
            try:
                with open(hgsub, "w") as f:
                    f.writelines(contents)
            except OSError as err:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Add Sub-repository"),
                    self.tr(
                        """<p>The sub-repositories file .hgsub could not"""
                        """ be written to.</p><p>Reason: {0}</p>""")
                    .format(str(err)))
                return
            
            if needsAdd:
                self.vcsAdd(hgsub)
                self.__projectHelper.getProject().appendFile(hgsub)
    
    def hgRemoveSubrepositories(self):
        """
        Public method to remove sub-repositories.
        """
        hgsub = self.getHgSubPath()
        
        subrepositories = []
        if not os.path.isfile(hgsub):
            E5MessageBox.critical(
                self.__ui,
                self.tr("Remove Sub-repositories"),
                self.tr("""<p>The sub-repositories file .hgsub does not"""
                        """ exist. Aborting...</p>"""))
            return
            
        try:
            with open(hgsub, "r") as f:
                subrepositories = [line.strip() for line in f.readlines()]
        except OSError as err:
            E5MessageBox.critical(
                self.__ui,
                self.tr("Remove Sub-repositories"),
                self.tr("""<p>The sub-repositories file .hgsub could not"""
                        """ be read.</p><p>Reason: {0}</p>""")
                .format(str(err)))
            return
        
        from .HgRemoveSubrepositoriesDialog import (
            HgRemoveSubrepositoriesDialog
        )
        dlg = HgRemoveSubrepositoriesDialog(subrepositories)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            subrepositories, removedSubrepos, deleteSubrepos = dlg.getData()
            contents = "\n".join(subrepositories) + "\n"
            try:
                with open(hgsub, "w") as f:
                    f.write(contents)
            except OSError as err:
                E5MessageBox.critical(
                    self.__ui,
                    self.tr("Remove Sub-repositories"),
                    self.tr(
                        """<p>The sub-repositories file .hgsub could not"""
                        """ be written to.</p><p>Reason: {0}</p>""")
                    .format(str(err)))
                return
            
            if deleteSubrepos:
                ppath = self.__projectHelper.getProject().getProjectPath()
                for removedSubrepo in removedSubrepos:
                    subrepoPath = removedSubrepo.split("=", 1)[0].strip()
                    subrepoAbsPath = os.path.join(ppath, subrepoPath)
                    shutil.rmtree(subrepoAbsPath, True)
    
    ###########################################################################
    ## Methods to handle configuration dependent stuff are below.
    ###########################################################################
    
    def __checkDefaults(self):
        """
        Private method to check, if the default and default-push URLs
        have been configured.
        """
        args = self.initCommand("showconfig")
        args.append('paths')
        
        output, error = self.__client.runcommand(args)
        
        self.__defaultConfigured = False
        self.__defaultPushConfigured = False
        if output:
            for line in output.splitlines():
                line = line.strip()
                if (
                    line.startswith("paths.default=") and
                    not line.endswith("=")
                ):
                    self.__defaultConfigured = True
                if (
                    line.startswith("paths.default-push=") and
                    not line.endswith("=")
                ):
                    self.__defaultPushConfigured = True
    
    def canCommitMerge(self):
        """
        Public method to check, if the working directory is an uncommitted
        merge.
 
        @return flag indicating commit merge capability
        @rtype bool
        """
        args = self.initCommand("identify")
        
        output, error = self.__client.runcommand(args)
        
        return output.count('+') == 2

    def canPull(self):
        """
        Public method to check, if pull is possible.
        
        @return flag indicating pull capability (boolean)
        """
        return self.__defaultConfigured
    
    def canPush(self):
        """
        Public method to check, if push is possible.
        
        @return flag indicating push capability (boolean)
        """
        return self.__defaultPushConfigured or self.__defaultConfigured
    
    def __iniFileChanged(self, path):
        """
        Private slot to handle a change of the Mercurial configuration file.
        
        @param path name of the changed file (string)
        """
        if self.__client:
            ok, err = self.__client.restartServer()
            if not ok:
                E5MessageBox.warning(
                    None,
                    self.tr("Mercurial Command Server"),
                    self.tr(
                        """<p>The Mercurial Command Server could not be"""
                        """ restarted.</p><p>Reason: {0}</p>""").format(err))
        
        self.__getExtensionsInfo()
        
        if self.__repoIniFile and path == self.__repoIniFile:
            self.__checkDefaults()
        
        self.iniFileChanged.emit()
    
    def __monitorRepoIniFile(self, repodir):
        """
        Private slot to add a repository configuration file to the list of
        monitored files.
        
        @param repodir directory name of the repository
        @type str
        """
        cfgFile = os.path.join(repodir, self.adminDir, "hgrc")
        if os.path.exists(cfgFile):
            self.__iniWatcher.addPath(cfgFile)
            self.__repoIniFile = cfgFile
            self.__checkDefaults()
    
    ###########################################################################
    ## Methods to handle extensions are below.
    ###########################################################################
    
    def __getExtensionsInfo(self):
        """
        Private method to get the active extensions from Mercurial.
        """
        activeExtensions = sorted(self.__activeExtensions)
        self.__activeExtensions = []
        
        args = self.initCommand("showconfig")
        args.append('extensions')
        
        output, error = self.__client.runcommand(args)
        
        if output:
            for line in output.splitlines():
                extensionName = (
                    line.split("=", 1)[0].strip().split(".")[-1].strip()
                )
                self.__activeExtensions.append(extensionName)
        if self.version < (4, 8, 0) and "closehead" in self.__activeExtensions:
            self.__activeExtensions.remove["closehead"]
        
        if activeExtensions != sorted(self.__activeExtensions):
            self.activeExtensionsChanged.emit()
    
    def isExtensionActive(self, extensionName):
        """
        Public method to check, if an extension is active.
        
        @param extensionName name of the extension to check for (string)
        @return flag indicating an active extension (boolean)
        """
        extensionName = extensionName.strip()
        isActive = extensionName in self.__activeExtensions
        
        return isActive
    
    def getExtensionObject(self, extensionName):
        """
        Public method to get a reference to an extension object.
        
        @param extensionName name of the extension (string)
        @return reference to the extension object (boolean)
        """
        return self.__extensions[extensionName]
    
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
        from .ProjectBrowserHelper import HgProjectBrowserHelper
        return HgProjectBrowserHelper(self, browser, project,
                                      isTranslationsBrowser)
        
    def vcsGetProjectHelper(self, project):
        """
        Public method to instantiate a helper object for the project.
        
        @param project reference to the project object
        @return the project helper object
        """
        # find the root of the repo
        repodir = project.getProjectPath()
        while not os.path.isdir(os.path.join(repodir, self.adminDir)):
            repodir = os.path.dirname(repodir)
            if not repodir or os.path.splitdrive(repodir)[1] == os.sep:
                repodir = ""
                break
        
        self.__projectHelper = self.__plugin.getProjectHelper()
        self.__projectHelper.setObjects(self, project)
        
        if repodir:
            self.__repoDir = repodir
            self.__createClient(repodir)
            self.__monitorRepoIniFile(repodir)
        
        return self.__projectHelper
    
    ###########################################################################
    ## Methods to handle the Mercurial command server are below.
    ###########################################################################
    
    def __createClient(self, repodir=""):
        """
        Private method to create a Mercurial command server client.
        
        @param repodir path of the local repository
        @type str
        """
        self.stopClient()
        
        self.__client = HgClient(repodir, "utf-8", self)
        ok, err = self.__client.startServer()
        if not ok:
            E5MessageBox.warning(
                None,
                self.tr("Mercurial Command Server"),
                self.tr(
                    """<p>The Mercurial Command Server could not be"""
                    """ started.</p><p>Reason: {0}</p>""").format(err))
    
    def getClient(self):
        """
        Public method to get a reference to the command server interface.
        
        @return reference to the client (HgClient)
        """
        if self.__client is None:
            self.__createClient(self.__repoDir)
        
        return self.__client
    
    def stopClient(self):
        """
        Public method to stop the command server client.
        """
        if self.__client is not None:
            self.__client.stopServer()
            self.__client = None
    
    ###########################################################################
    ## Status Monitor Thread methods
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
        from .HgStatusMonitorThread import HgStatusMonitorThread
        return HgStatusMonitorThread(interval, project, self)

    ###########################################################################
    ## Bookmarks methods
    ###########################################################################

    def hgListBookmarks(self):
        """
        Public method used to list the available bookmarks.
        """
        self.bookmarksList = []
        
        if self.bookmarksListDlg is None:
            from .HgBookmarksListDialog import HgBookmarksListDialog
            self.bookmarksListDlg = HgBookmarksListDialog(self)
        self.bookmarksListDlg.show()
        self.bookmarksListDlg.raise_()
        self.bookmarksListDlg.start(self.bookmarksList)
    
    def hgGetBookmarksList(self):
        """
        Public method to get the list of bookmarks.
        
        @return list of bookmarks (list of string)
        """
        args = self.initCommand("bookmarks")
        
        client = self.getClient()
        output = client.runcommand(args)[0]
        
        self.bookmarksList = []
        for line in output.splitlines():
            li = line.strip().split()
            if li[-1][0] in "1234567890":
                # last element is a rev:changeset
                del li[-1]
                if li[0] == "*":
                    del li[0]
                name = " ".join(li)
                self.bookmarksList.append(name)
        
        return self.bookmarksList[:]
    
    def hgBookmarkDefine(self, revision=None, bookmark=None):
        """
        Public method to define a bookmark.
        
        @param revision revision to set bookmark for (string)
        @param bookmark name of the bookmark (string)
        """
        if bool(revision) and bool(bookmark):
            ok = True
        else:
            from .HgBookmarkDialog import HgBookmarkDialog
            dlg = HgBookmarkDialog(HgBookmarkDialog.DEFINE_MODE,
                                   self.hgGetTagsList(),
                                   self.hgGetBranchesList(),
                                   self.hgGetBookmarksList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                revision, bookmark = dlg.getData()
                ok = True
            else:
                ok = False
        
        if ok:
            args = self.initCommand("bookmarks")
            if revision:
                args.append("--rev")
                args.append(revision)
            args.append(bookmark)
            
            dia = HgDialog(self.tr('Mercurial Bookmark'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgBookmarkDelete(self, bookmark=None):
        """
        Public method to delete a bookmark.
        
        @param bookmark name of the bookmark (string)
        """
        if bookmark:
            ok = True
        else:
            bookmark, ok = QInputDialog.getItem(
                None,
                self.tr("Delete Bookmark"),
                self.tr("Select the bookmark to be deleted:"),
                [""] + sorted(self.hgGetBookmarksList()),
                0, True)
        if ok and bookmark:
            args = self.initCommand("bookmarks")
            args.append("--delete")
            args.append(bookmark)
            
            dia = HgDialog(self.tr('Delete Mercurial Bookmark'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgBookmarkRename(self, renameInfo=None):
        """
        Public method to rename a bookmark.
        
        @param renameInfo old and new names of the bookmark
        @type tuple of str and str
        """
        if not renameInfo:
            from .HgBookmarkRenameDialog import HgBookmarkRenameDialog
            dlg = HgBookmarkRenameDialog(self.hgGetBookmarksList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                renameInfo = dlg.getData()
        
        if renameInfo:
            args = self.initCommand("bookmarks")
            args.append("--rename")
            args.append(renameInfo[0])
            args.append(renameInfo[1])
            
            dia = HgDialog(self.tr('Rename Mercurial Bookmark'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgBookmarkMove(self, revision=None, bookmark=None):
        """
        Public method to move a bookmark.
        
        @param revision revision to set bookmark for (string)
        @param bookmark name of the bookmark (string)
        """
        if bool(revision) and bool(bookmark):
            ok = True
        else:
            from .HgBookmarkDialog import HgBookmarkDialog
            dlg = HgBookmarkDialog(HgBookmarkDialog.MOVE_MODE,
                                   self.hgGetTagsList(),
                                   self.hgGetBranchesList(),
                                   self.hgGetBookmarksList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                revision, bookmark = dlg.getData()
                ok = True
            else:
                ok = False
        
        if ok:
            args = self.initCommand("bookmarks")
            args.append("--force")
            if revision:
                args.append("--rev")
                args.append(revision)
            args.append(bookmark)
            
            dia = HgDialog(self.tr('Move Mercurial Bookmark'), self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgBookmarkIncoming(self):
        """
        Public method to show a list of incoming bookmarks.
        """
        from .HgBookmarksInOutDialog import HgBookmarksInOutDialog
        self.bookmarksInOutDlg = HgBookmarksInOutDialog(
            self, HgBookmarksInOutDialog.INCOMING)
        self.bookmarksInOutDlg.show()
        self.bookmarksInOutDlg.start()
    
    def hgBookmarkOutgoing(self):
        """
        Public method to show a list of outgoing bookmarks.
        """
        from .HgBookmarksInOutDialog import HgBookmarksInOutDialog
        self.bookmarksInOutDlg = HgBookmarksInOutDialog(
            self, HgBookmarksInOutDialog.OUTGOING)
        self.bookmarksInOutDlg.show()
        self.bookmarksInOutDlg.start()
    
    def __getInOutBookmarks(self, incoming):
        """
        Private method to get the list of incoming or outgoing bookmarks.
        
        @param incoming flag indicating to get incoming bookmarks (boolean)
        @return list of bookmarks (list of string)
        """
        bookmarksList = []
        
        if incoming:
            args = self.initCommand("incoming")
        else:
            args = self.initCommand("outgoing")
        args.append('--bookmarks')
        
        client = self.getClient()
        output = client.runcommand(args)[0]
        
        for line in output.splitlines():
            if line.startswith(" "):
                li = line.strip().split()
                del li[-1]
                name = " ".join(li)
                bookmarksList.append(name)
        
        return bookmarksList
    
    def hgBookmarkPull(self, current=False, bookmark=None):
        """
        Public method to pull a bookmark from a remote repository.
        
        @param current flag indicating to pull the current bookmark
        @type bool
        @param bookmark name of the bookmark
        @type str
        """
        if current:
            bookmark = "."
            ok = True
        elif bookmark:
            ok = True
        else:
            bookmarks = self.__getInOutBookmarks(True)
            bookmark, ok = QInputDialog.getItem(
                None,
                self.tr("Pull Bookmark"),
                self.tr("Select the bookmark to be pulled:"),
                [""] + sorted(bookmarks),
                0, True)
        
        if ok and bookmark:
            args = self.initCommand("pull")
            args.append('--bookmark')
            args.append(bookmark)
            
            dia = HgDialog(self.tr(
                'Pulling bookmark from a remote Mercurial repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgBookmarkPush(self, current=False, bookmark=None, allBookmarks=False):
        """
        Public method to push a bookmark to a remote repository.
        
        @param current flag indicating to push the current bookmark
        @type bool
        @param bookmark name of the bookmark
        @type str
        @param allBookmarks flag indicating to push all bookmarks
        @type bool
        """
        if current:
            bookmark = "."
            ok = True
        elif bookmark or allBookmarks:
            ok = True
        else:
            bookmarks = self.__getInOutBookmarks(False)
            bookmark, ok = QInputDialog.getItem(
                None,
                self.tr("Push Bookmark"),
                self.tr("Select the bookmark to be push:"),
                [""] + sorted(bookmarks),
                0, True)
        
        if ok and (bool(bookmark) or all):
            args = self.initCommand("push")
            if allBookmarks:
                args.append('--all-bookmarks')
            else:
                args.append('--bookmark')
                args.append(bookmark)
            
            dia = HgDialog(self.tr(
                'Pushing bookmark to a remote Mercurial repository'),
                self)
            res = dia.startProcess(args)
            if res:
                dia.exec()
