# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the largefiles extension interface.
"""

import os

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog
from ..HgClient import HgClient


class Largefiles(HgExtension):
    """
    Class implementing the largefiles extension interface.
    """
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        """
        super(Largefiles, self).__init__(vcs)
    
    def hgLfconvert(self, direction, projectFile):
        """
        Public slot to convert the repository format of the current project.
        
        @param direction direction of the conversion (string, one of
            'largefiles' or 'normal')
        @param projectFile file name of the current project file (string)
        @exception ValueError raised to indicate a bad value for the
            'direction' parameter.
        """
        if direction not in ["largefiles", "normal"]:
            raise ValueError("Bad value for 'direction' parameter.")
        
        projectDir = os.path.dirname(projectFile)
        
        from .LfConvertDataDialog import LfConvertDataDialog
        dlg = LfConvertDataDialog(projectDir, direction)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            newName, minSize, patterns = dlg.getData()
            newProjectFile = os.path.join(
                newName, os.path.basename(projectFile))
            
            # step 1: convert the current project to new project
            args = self.vcs.initCommand("lfconvert")
            if direction == 'normal':
                args.append('--to-normal')
            else:
                args.append("--size")
                args.append(str(minSize))
            args.append(projectDir)
            args.append(newName)
            if direction == 'largefiles' and patterns:
                args.extend(patterns)
            
            dia = HgDialog(self.tr('Convert Project - Converting'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.normalExit() and os.path.isdir(
                    os.path.join(newName, self.vcs.adminDir))
            
            # step 2: create working directory contents
            if res:
                # step 2.1: start a command server client for the new repo
                client = HgClient(newName, "utf-8", self.vcs)
                ok, err = client.startServer()
                if not ok:
                    E5MessageBox.warning(
                        None,
                        self.tr("Mercurial Command Server"),
                        self.tr(
                            """<p>The Mercurial Command Server could not be"""
                            """ started.</p><p>Reason: {0}</p>""").format(err))
                    return
                
                # step 2.2: create working directory contents
                args = self.vcs.initCommand("update")
                args.append("--verbose")
                dia = HgDialog(self.tr('Convert Project - Extracting'),
                               self.vcs, client=client)
                res = dia.startProcess(args)
                if res:
                    dia.exec()
                    res = dia.normalExit() and os.path.isfile(newProjectFile)
                
                # step 2.3: stop the command server client for the new repo
                client.stopServer()
            
            # step 3: close current project and open new one
            if res:
                if direction == 'largefiles':
                    self.vcs.hgEditConfig(
                        repoName=newName,
                        largefilesData={"minsize": minSize,
                                        "pattern": patterns}
                    )
                else:
                    self.vcs.hgEditConfig(
                        repoName=newName,
                        withLargefiles=False
                    )
                QTimer.singleShot(
                    0, lambda: e5App().getObject("Project").openProject(
                        newProjectFile))
    
    def hgAdd(self, names, mode):
        """
        Public method used to add a file to the Mercurial repository.
        
        @param names file name(s) to be added (string or list of string)
        @param mode add mode (string one of 'normal' or 'large')
        """
        args = self.vcs.initCommand("add")
        args.append("-v")
        if mode == "large":
            args.append("--large")
        else:
            args.append("--normal")
        
        if isinstance(names, list):
            self.vcs.addArguments(args, names)
        else:
            args.append(names)
        
        dia = HgDialog(
            self.tr('Adding files to the Mercurial repository'),
            self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
    
    def hgLfPull(self, revisions=None):
        """
        Public method to pull missing large files into the local repository.
        
        @param revisions list of revisions to pull (list of string)
        """
        revs = []
        if revisions:
            revs = revisions
        else:
            from .LfRevisionsInputDialog import LfRevisionsInputDialog
            dlg = LfRevisionsInputDialog()
            if dlg.exec() == QDialog.DialogCode.Accepted:
                revs = dlg.getRevisions()
        
        if revs:
            args = self.vcs.initCommand("lfpull")
            args.append("-v")
            for rev in revs:
                args.append("--rev")
                args.append(rev)
            
            dia = HgDialog(self.tr("Pulling large files"), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgLfVerify(self, mode):
        """
        Public method to verify large files integrity.
        
        @param mode verify mode (string; one of 'large', 'lfa' or 'lfc')
        """
        args = self.vcs.initCommand("verify")
        if mode == "large":
            args.append("--large")
        elif mode == "lfa":
            args.append("--lfa")
        elif mode == "lfc":
            args.append("--lfc")
        else:
            return
        
        dia = HgDialog(
            self.tr('Verifying the integrity of large files'),
            self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
