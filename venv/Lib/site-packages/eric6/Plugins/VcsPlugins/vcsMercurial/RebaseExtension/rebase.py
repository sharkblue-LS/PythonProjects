# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the rebase extension interface.
"""

from PyQt5.QtWidgets import QDialog

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog


class Rebase(HgExtension):
    """
    Class implementing the rebase extension interface.
    """
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        """
        super(Rebase, self).__init__(vcs)
    
    def hgRebase(self):
        """
        Public method to rebase changesets to a different branch.
        
        @return flag indicating that the project should be reread (boolean)
        """
        res = False
        from .HgRebaseDialog import HgRebaseDialog
        dlg = HgRebaseDialog(self.vcs.hgGetTagsList(),
                             self.vcs.hgGetBranchesList(),
                             self.vcs.hgGetBookmarksList(),
                             self.vcs.version)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (indicator, sourceRev, destRev, collapse, keep, keepBranches,
             detach, dryRunOnly, dryRunConfirm) = dlg.getData()
            
            args = self.vcs.initCommand("rebase")
            if indicator == "S":
                args.append("--source")
                args.append(sourceRev)
            elif indicator == "B":
                args.append("--base")
                args.append(sourceRev)
            if destRev:
                args.append("--dest")
                args.append(destRev)
            if collapse:
                args.append("--collapse")
            if keep:
                args.append("--keep")
            if keepBranches:
                args.append("--keepbranches")
            if detach:
                args.append("--detach")
            if dryRunOnly:
                args.append("--dry-run")
            elif dryRunConfirm:
                args.append("--confirm")
            args.append("--verbose")
            
            dia = HgDialog(self.tr('Rebase Changesets'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.vcs.checkVCSStatus()
        return res
    
    def hgRebaseContinue(self):
        """
        Public method to continue rebasing changesets from another branch.
        
        @return flag indicating that the project should be reread (boolean)
        """
        args = self.vcs.initCommand("rebase")
        args.append("--continue")
        args.append("--verbose")
        
        dia = HgDialog(self.tr('Rebase Changesets (Continue)'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
    
    def hgRebaseAbort(self):
        """
        Public method to abort rebasing changesets from another branch.
        
        @return flag indicating that the project should be reread (boolean)
        """
        args = self.vcs.initCommand("rebase")
        args.append("--abort")
        args.append("--verbose")
        
        dia = HgDialog(self.tr('Rebase Changesets (Abort)'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
