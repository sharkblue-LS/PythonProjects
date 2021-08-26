# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the closehead extension interface.
"""

from PyQt5.QtWidgets import QDialog

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog


class Closehead(HgExtension):
    """
    Class implementing the strip extension interface.
    """
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        @type Hg
        """
        super(Closehead, self).__init__(vcs)
    
    def hgCloseheads(self, revisions=None):
        """
        Public method to close arbitrary heads.
        
        @param revisions revisions of branch heads to be closed
        @type str
        """
        message = ""
        if not revisions:
            from .HgCloseHeadSelectionDialog import HgCloseHeadSelectionDialog
            dlg = HgCloseHeadSelectionDialog(self.vcs)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                revisions, message = dlg.getData()
        
        if not revisions:
            # still no revisions given; abort...
            return
        
        args = self.vcs.initCommand("close-head")
        if not message:
            if len(revisions) == 1:
                message = self.tr("Revision <{0}> closed.").format(
                    revisions[0])
            else:
                message = self.tr("Revisions <{0}> closed.").format(
                    ", ".join(revisions))
        args += ["--message", message]
        for revision in revisions:
            args += ["--rev", revision]
        
        dia = HgDialog(self.tr("Closing Heads"), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
