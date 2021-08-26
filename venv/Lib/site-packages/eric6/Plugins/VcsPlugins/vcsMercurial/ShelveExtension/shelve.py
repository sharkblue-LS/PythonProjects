# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the shelve extension interface.
"""

from PyQt5.QtWidgets import QDialog

from E5Gui import E5MessageBox

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog


class Shelve(HgExtension):
    """
    Class implementing the shelve extension interface.
    """
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        """
        super(Shelve, self).__init__(vcs)
        
        self.__unshelveKeep = False
        
        self.__shelveBrowserDialog = None
    
    def shutdown(self):
        """
        Public method used to shutdown the shelve interface.
        """
        if self.__shelveBrowserDialog is not None:
            self.__shelveBrowserDialog.close()
    
    def __hgGetShelveNamesList(self):
        """
        Private method to get the list of shelved changes.
        
        @return list of shelved changes (list of string)
        """
        args = self.vcs.initCommand("shelve")
        args.append('--list')
        args.append('--quiet')
        
        client = self.vcs.getClient()
        output = client.runcommand(args)[0]
        
        shelveNamesList = []
        for line in output.splitlines():
            shelveNamesList.append(line.strip())
        
        return shelveNamesList[:]
    
    def hgShelve(self, name):
        """
        Public method to shelve current changes of files or directories.
        
        @param name directory or file name (string) or list of directory
            or file names (list of string)
        @return flag indicating that the project should be reread (boolean)
        """
        res = False
        from .HgShelveDataDialog import HgShelveDataDialog
        dlg = HgShelveDataDialog(self.vcs.version)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            shelveName, dateTime, message, addRemove, keep = dlg.getData()
            
            args = self.vcs.initCommand("shelve")
            if shelveName:
                args.append("--name")
                args.append(shelveName)
            if message:
                args.append("--message")
                args.append(message)
            if addRemove:
                args.append("--addremove")
            if dateTime.isValid():
                args.append("--date")
                args.append(dateTime.toString("yyyy-MM-dd hh:mm:ss"))
            if self.vcs.version >= (5, 0, 0) and keep:
                args.append("--keep")
            args.append("-v")
            
            if isinstance(name, list):
                self.vcs.addArguments(args, name)
            else:
                args.append(name)
            
            dia = HgDialog(self.tr('Shelve current changes'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.vcs.checkVCSStatus()
        return res
    
    def hgShelveBrowser(self):
        """
        Public method to show the shelve browser dialog.
        """
        if self.__shelveBrowserDialog is None:
            from .HgShelveBrowserDialog import HgShelveBrowserDialog
            self.__shelveBrowserDialog = HgShelveBrowserDialog(
                self.vcs)
        self.__shelveBrowserDialog.show()
        self.__shelveBrowserDialog.start()
    
    def hgUnshelve(self, shelveName=""):
        """
        Public method to restore shelved changes to the project directory.
        
        @param shelveName name of the shelve to restore (string)
        @return flag indicating that the project should be reread (boolean)
        """
        res = False
        from .HgUnshelveDataDialog import HgUnshelveDataDialog
        dlg = HgUnshelveDataDialog(self.__hgGetShelveNamesList(),
                                   shelveName=shelveName)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            shelveName, keep = dlg.getData()
            self.__unshelveKeep = keep  # store for potential continue
            
            args = self.vcs.initCommand("unshelve")
            if keep:
                args.append("--keep")
            if shelveName:
                args.append(shelveName)
            
            dia = HgDialog(self.tr('Restore shelved changes'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                res = dia.hasAddOrDelete()
                self.vcs.checkVCSStatus()
        return res
    
    def hgUnshelveAbort(self):
        """
        Public method to abort the ongoing restore operation.
        
        @return flag indicating that the project should be reread (boolean)
        """
        args = self.vcs.initCommand("unshelve")
        args.append("--abort")
        
        dia = HgDialog(self.tr('Abort restore operation'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
    
    def hgUnshelveContinue(self):
        """
        Public method to continue the ongoing restore operation.
        
        @return flag indicating that the project should be reread (boolean)
        """
        args = self.vcs.initCommand("unshelve")
        if self.__unshelveKeep:
            args.append("--keep")
        args.append("--continue")
        
        dia = HgDialog(self.tr('Continue restore operation'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
    
    def hgDeleteShelves(self, shelveNames=None):
        """
        Public method to delete named shelves.
        
        @param shelveNames name of shelves to delete (list of string)
        """
        if not shelveNames:
            from .HgShelvesSelectionDialog import HgShelvesSelectionDialog
            dlg = HgShelvesSelectionDialog(
                self.tr("Select the shelves to be deleted:"),
                self.__hgGetShelveNamesList())
            if dlg.exec() == QDialog.DialogCode.Accepted:
                shelveNames = dlg.getSelectedShelves()
            else:
                return
        
        from UI.DeleteFilesConfirmationDialog import (
            DeleteFilesConfirmationDialog
        )
        dlg = DeleteFilesConfirmationDialog(
            None,
            self.tr("Delete shelves"),
            self.tr("Do you really want to delete these shelves?"),
            shelveNames)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            args = self.vcs.initCommand("shelve")
            args.append("--delete")
            args.extend(shelveNames)
            
            dia = HgDialog(self.tr('Delete shelves'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
    
    def hgCleanupShelves(self):
        """
        Public method to delete all shelves.
        """
        res = E5MessageBox.yesNo(
            None,
            self.tr("Delete all shelves"),
            self.tr("""Do you really want to delete all shelved changes?"""))
        if res:
            args = self.vcs.initCommand("shelve")
            args.append("--cleanup")
            
            dia = HgDialog(self.tr('Delete all shelves'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
