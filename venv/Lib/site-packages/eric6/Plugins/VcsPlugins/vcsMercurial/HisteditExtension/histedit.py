# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the histedit extension interface.
"""

import os
import sys

from PyQt5.QtWidgets import QDialog

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog


class Histedit(HgExtension):
    """
    Class implementing the histedit extension interface.
    """
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        @type Hg
        """
        super(Histedit, self).__init__(vcs)
    
    def hgHisteditStart(self, rev=""):
        """
        Public method to start a histedit session.
        
        @param rev revision to start histedit at
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        from .HgHisteditConfigDialog import HgHisteditConfigDialog
        res = False
        dlg = HgHisteditConfigDialog(self.vcs.hgGetTagsList(),
                                     self.vcs.hgGetBranchesList(),
                                     self.vcs.hgGetBookmarksList(),
                                     rev)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            rev, force, keep = dlg.getData()
            
            args = self.vcs.initCommand("histedit")
            args.append("-v")
            if keep:
                args.append("--keep")
            if rev:
                if rev == "--outgoing":
                    if force:
                        args.append("--force")
                else:
                    args.append("--rev")
                args.append(rev)
            
            editor = os.path.join(
                os.path.dirname(__file__), "HgHisteditEditor.py")
            env = {"HGEDITOR": "{0} {1}".format(sys.executable, editor)}
            
            dia = HgDialog(
                self.tr("Starting histedit session"),
                self.vcs,
                useClient=False)
            res = dia.startProcess(args, environment=env)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.vcs.checkVCSStatus()
        return res
    
    def hgHisteditContinue(self):
        """
        Public method to continue an interrupted histedit session.
        
        @return flag indicating that the project should be reread
        @rtype bool
        """
        args = self.vcs.initCommand("histedit")
        args.append("--continue")
        args.append("-v")
        
        editor = os.path.join(
            os.path.dirname(__file__), "HgHisteditEditor.py")
        env = {"HGEDITOR": "{0} {1}".format(sys.executable, editor)}
        
        dia = HgDialog(
            self.tr("Continue histedit session"),
            self.vcs,
            useClient=False)
        res = dia.startProcess(args, environment=env)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
    
    def hgHisteditAbort(self, name):
        """
        Public method to abort an interrupted histedit session.
        
        @param name file/directory name
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        args = self.vcs.initCommand("histedit")
        args.append("--abort")
        args.append("-v")
        
        editor = os.path.join(
            os.path.dirname(__file__), "HgHisteditEditor.py")
        env = {"HGEDITOR": "{0} {1}".format(sys.executable, editor)}
        
        dia = HgDialog(
            self.tr("Abort histedit session"),
            self.vcs,
            useClient=False)
        res = dia.startProcess(args, environment=env)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
    
    def hgHisteditEditPlan(self):
        """
        Public method to edit the remaining actions list of an interrupted
        histedit session.
        
        @return flag indicating that the project should be reread
        @rtype bool
        """
        args = self.vcs.initCommand("histedit")
        args.append("--edit-plan")
        args.append("-v")
        
        editor = os.path.join(
            os.path.dirname(__file__), "HgHisteditEditor.py")
        env = {"HGEDITOR": "{0} {1}".format(sys.executable, editor)}
        
        dia = HgDialog(
            self.tr("Edit Plan"),
            self.vcs,
            useClient=False)
        res = dia.startProcess(args, environment=env)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
