# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the strip extension interface.
"""

from PyQt5.QtWidgets import QDialog

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog


class Strip(HgExtension):
    """
    Class implementing the strip extension interface.
    """
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        @type Hg
        """
        super(Strip, self).__init__(vcs)
    
    def hgStrip(self, rev=""):
        """
        Public method to strip revisions from a repository.
        
        @param rev revision to strip from
        @type str
        @return flag indicating that the project should be reread
        @rtype bool
        """
        from .HgStripDialog import HgStripDialog
        res = False
        dlg = HgStripDialog(self.vcs.hgGetTagsList(),
                            self.vcs.hgGetBranchesList(),
                            self.vcs.hgGetBookmarksList(),
                            rev)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            rev, bookmark, force, noBackup, keep = dlg.getData()
            
            args = self.vcs.initCommand("strip")
            if bookmark:
                args.append("--bookmark")
                args.append(bookmark)
            if force:
                args.append("--force")
            if noBackup:
                args.append("--no-backup")
            if keep:
                args.append("--keep")
            args.append("-v")
            args.append(rev)
            
            dia = HgDialog(
                self.tr("Stripping changesets from repository"),
                self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.vcs.checkVCSStatus()
        return res
