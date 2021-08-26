# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the queues extension interface.
"""

from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog

from E5Gui import E5MessageBox

from ..HgExtension import HgExtension
from ..HgDialog import HgDialog


class Queues(HgExtension):
    """
    Class implementing the queues extension interface.
    """
    APPLIED_LIST = 0
    UNAPPLIED_LIST = 1
    SERIES_LIST = 2
    
    POP = 0
    PUSH = 1
    GOTO = 2
    
    QUEUE_DELETE = 0
    QUEUE_PURGE = 1
    QUEUE_ACTIVATE = 2
    
    def __init__(self, vcs):
        """
        Constructor
        
        @param vcs reference to the Mercurial vcs object
        """
        super(Queues, self).__init__(vcs)
        
        self.qdiffDialog = None
        self.qheaderDialog = None
        self.queuesListDialog = None
        self.queuesListGuardsDialog = None
        self.queuesListAllGuardsDialog = None
        self.queuesDefineGuardsDialog = None
        self.queuesListQueuesDialog = None
        self.queueStatusDialog = None
    
    def shutdown(self):
        """
        Public method used to shutdown the queues interface.
        """
        if self.qdiffDialog is not None:
            self.qdiffDialog.close()
        if self.qheaderDialog is not None:
            self.qheaderDialog.close()
        if self.queuesListDialog is not None:
            self.queuesListDialog.close()
        if self.queuesListGuardsDialog is not None:
            self.queuesListGuardsDialog.close()
        if self.queuesListAllGuardsDialog is not None:
            self.queuesListAllGuardsDialog.close()
        if self.queuesDefineGuardsDialog is not None:
            self.queuesDefineGuardsDialog.close()
        if self.queuesListQueuesDialog is not None:
            self.queuesListQueuesDialog.close()
        if self.queueStatusDialog is not None:
            self.queueStatusDialog.close()
    
    def __getPatchesList(self, listType, withSummary=False):
        """
        Private method to get a list of patches of a given type.
        
        @param listType type of patches list to get
            (Queues.APPLIED_LIST, Queues.UNAPPLIED_LIST, Queues.SERIES_LIST)
        @param withSummary flag indicating to get a summary as well (boolean)
        @return list of patches (list of string)
        @exception ValueError raised to indicate an invalid patch list type
        """
        patchesList = []
        
        if listType == Queues.APPLIED_LIST:
            args = self.vcs.initCommand("qapplied")
        elif listType == Queues.UNAPPLIED_LIST:
            args = self.vcs.initCommand("qunapplied")
        elif listType == Queues.SERIES_LIST:
            args = self.vcs.initCommand("qseries")
        else:
            raise ValueError("illegal value for listType")
        if withSummary:
            args.append("--summary")
        
        client = self.vcs.getClient()
        output = client.runcommand(args)[0]
        
        for line in output.splitlines():
            if withSummary:
                li = line.strip().split(": ")
                if len(li) == 1:
                    patch, summary = li[0][:-1], ""
                else:
                    patch, summary = li[0], li[1]
                patchesList.append("{0}@@{1}".format(patch, summary))
            else:
                patchesList.append(line.strip())
        
        return patchesList
    
    def __getCurrentPatch(self):
        """
        Private method to get the name of the current patch.
        
        @return name of the current patch (string)
        """
        currentPatch = ""
        
        args = self.vcs.initCommand("qtop")
        
        client = self.vcs.getClient()
        currentPatch = client.runcommand(args)[0].strip()
        
        return currentPatch
    
    def __getCommitMessage(self):
        """
        Private method to get the commit message of the current patch.
        
        @return name of the current patch (string)
        """
        message = ""
        
        args = self.vcs.initCommand("qheader")
        
        client = self.vcs.getClient()
        message = client.runcommand(args)[0]
        
        return message
    
    def getGuardsList(self, allGuards=True):
        """
        Public method to get a list of all guards defined.
        
        @param allGuards flag indicating to get all guards (boolean)
        @return sorted list of guards (list of strings)
        """
        guardsList = []
        
        args = self.vcs.initCommand("qselect")
        if allGuards:
            args.append("--series")
        
        client = self.vcs.getClient()
        output = client.runcommand(args)[0]
        
        for guard in output.splitlines():
            guard = guard.strip()
            if allGuards:
                guard = guard[1:]
            if guard not in guardsList:
                guardsList.append(guard)
        
        return sorted(guardsList)
    
    def hgQueueNewPatch(self):
        """
        Public method to create a new named patch.
        """
        from .HgQueuesNewPatchDialog import HgQueuesNewPatchDialog
        dlg = HgQueuesNewPatchDialog(HgQueuesNewPatchDialog.NEW_MODE)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (name, message,
             (userData, currentUser, userName),
             (dateData, currentDate, dateStr)) = dlg.getData()
            
            args = self.vcs.initCommand("qnew")
            if message != "":
                args.append("--message")
                args.append(message)
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
            args.append(name)
            
            dia = HgDialog(self.tr('New Patch'), self.vcs)
            res = dia.startProcess(args)
            if res:
                dia.exec()
                self.vcs.checkVCSStatus()
    
    def hgQueueRefreshPatch(self, editMessage=False):
        """
        Public method to refresh the current patch.
        
        @param editMessage flag indicating to edit the current
            commit message (boolean)
        """
        args = self.vcs.initCommand("qrefresh")
        
        if editMessage:
            currentMessage = self.__getCommitMessage()
            from .HgQueuesNewPatchDialog import HgQueuesNewPatchDialog
            dlg = HgQueuesNewPatchDialog(HgQueuesNewPatchDialog.REFRESH_MODE,
                                         currentMessage)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                (name, message,
                 (userData, currentUser, userName),
                 (dateData, currentDate, dateStr)) = dlg.getData()
                if message != "" and message != currentMessage:
                    args.append("--message")
                    args.append(message)
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
            else:
                return
        
        dia = HgDialog(self.tr('Update Current Patch'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            self.vcs.checkVCSStatus()
    
    def hgQueueShowPatch(self, name):
        """
        Public method to show the contents of the current patch.
        
        @param name file/directory name (string)
        """
        from ..HgDiffDialog import HgDiffDialog
        self.qdiffDialog = HgDiffDialog(self.vcs)
        self.qdiffDialog.show()
        QApplication.processEvents()
        self.qdiffDialog.start(name, qdiff=True)
    
    def hgQueueShowHeader(self):
        """
        Public method to show the commit message of the current patch.
        """
        from .HgQueuesHeaderDialog import HgQueuesHeaderDialog
        self.qheaderDialog = HgQueuesHeaderDialog(self.vcs)
        self.qheaderDialog.show()
        QApplication.processEvents()
        self.qheaderDialog.start()
    
    def hgQueuePushPopPatches(self, operation, doAll=False, named=False,
                              force=False):
        """
        Public method to push patches onto the stack or pop patches off the
        stack.
        
        @param operation operation type to be performed (Queues.POP,
            Queues.PUSH, Queues.GOTO)
        @param doAll flag indicating to push/pop all (boolean)
        @param named flag indicating to push/pop until a named patch
            is at the top of the stack (boolean)
        @param force flag indicating a forceful pop (boolean)
        @return flag indicating that the project should be reread (boolean)
        @exception ValueError raised to indicate an invalid operation
        """
        if operation == Queues.POP:
            args = self.vcs.initCommand("qpop")
            title = self.tr("Pop Patches")
            listType = Queues.APPLIED_LIST
        elif operation == Queues.PUSH:
            args = self.vcs.initCommand("qpush")
            title = self.tr("Push Patches")
            listType = Queues.UNAPPLIED_LIST
        elif operation == Queues.GOTO:
            args = self.vcs.initCommand("qgoto")
            title = self.tr("Go to Patch")
            listType = Queues.SERIES_LIST
        else:
            raise ValueError("illegal value for operation")
        args.append("-v")
        if force:
            args.append("--force")
        if doAll and operation in (Queues.POP, Queues.PUSH):
            args.append("--all")
        elif named or operation == Queues.GOTO:
            patchnames = self.__getPatchesList(listType)
            if patchnames:
                patch, ok = QInputDialog.getItem(
                    None,
                    self.tr("Select Patch"),
                    self.tr("Select the target patch name:"),
                    patchnames,
                    0, False)
                if ok and patch:
                    args.append(patch)
                else:
                    return False
            else:
                E5MessageBox.information(
                    None,
                    self.tr("Select Patch"),
                    self.tr("""No patches to select from."""))
                return False
        
        dia = HgDialog(title, self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            res = dia.hasAddOrDelete()
            self.vcs.checkVCSStatus()
        return res
    
    def hgQueueListPatches(self):
        """
        Public method to show a list of all patches.
        """
        from .HgQueuesListDialog import HgQueuesListDialog
        self.queuesListDialog = HgQueuesListDialog(self.vcs)
        self.queuesListDialog.show()
        self.queuesListDialog.start()
    
    def hgQueueFinishAppliedPatches(self):
        """
        Public method to finish all applied patches.
        """
        args = self.vcs.initCommand("qfinish")
        args.append("--applied")
        
        dia = HgDialog(self.tr('Finish Applied Patches'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
            self.vcs.checkVCSStatus()
    
    def hgQueueRenamePatch(self):
        """
        Public method to rename the current or a selected patch.
        """
        args = self.vcs.initCommand("qrename")
        patchnames = sorted(self.__getPatchesList(Queues.SERIES_LIST))
        if patchnames:
            currentPatch = self.__getCurrentPatch()
            if currentPatch:
                from .HgQueuesRenamePatchDialog import (
                    HgQueuesRenamePatchDialog
                )
                dlg = HgQueuesRenamePatchDialog(currentPatch, patchnames)
                if dlg.exec() == QDialog.DialogCode.Accepted:
                    newName, selectedPatch = dlg.getData()
                    if selectedPatch:
                        args.append(selectedPatch)
                    args.append(newName)
                    
                    dia = HgDialog(self.tr("Rename Patch"), self.vcs)
                    res = dia.startProcess(args)
                    if res:
                        dia.exec()
    
    def hgQueueDeletePatch(self):
        """
        Public method to delete a selected unapplied patch.
        """
        args = self.vcs.initCommand("qdelete")
        patchnames = sorted(self.__getPatchesList(Queues.UNAPPLIED_LIST))
        if patchnames:
            patch, ok = QInputDialog.getItem(
                None,
                self.tr("Select Patch"),
                self.tr("Select the patch to be deleted:"),
                patchnames,
                0, False)
            if ok and patch:
                args.append(patch)
                
                dia = HgDialog(self.tr("Delete Patch"), self.vcs)
                res = dia.startProcess(args)
                if res:
                    dia.exec()
        else:
            E5MessageBox.information(
                None,
                self.tr("Select Patch"),
                self.tr("""No patches to select from."""))
    
    def hgQueueFoldUnappliedPatches(self):
        """
        Public method to fold patches into the current patch.
        """
        args = self.vcs.initCommand("qfold")
        patchnames = sorted(
            self.__getPatchesList(Queues.UNAPPLIED_LIST, withSummary=True))
        if patchnames:
            from .HgQueuesFoldDialog import HgQueuesFoldDialog
            dlg = HgQueuesFoldDialog(patchnames)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                message, patchesList = dlg.getData()
                if message:
                    args.append("--message")
                    args.append(message)
                if patchesList:
                    args.extend(patchesList)
                    
                    dia = HgDialog(self.tr("Fold Patches"), self.vcs)
                    res = dia.startProcess(args)
                    if res:
                        dia.exec()
                else:
                    E5MessageBox.information(
                        None,
                        self.tr("Fold Patches"),
                        self.tr("""No patches selected."""))
        else:
            E5MessageBox.information(
                None,
                self.tr("Fold Patches"),
                self.tr("""No patches available to be folded."""))
    
    def hgQueueGuardsList(self):
        """
        Public method to list the guards for the current or a named patch.
        """
        patchnames = sorted(self.__getPatchesList(Queues.SERIES_LIST))
        if patchnames:
            from .HgQueuesListGuardsDialog import HgQueuesListGuardsDialog
            self.queuesListGuardsDialog = HgQueuesListGuardsDialog(
                self.vcs, patchnames)
            self.queuesListGuardsDialog.show()
            self.queuesListGuardsDialog.start()
        else:
            E5MessageBox.information(
                None,
                self.tr("List Guards"),
                self.tr("""No patches available to list guards for."""))
    
    def hgQueueGuardsListAll(self):
        """
        Public method to list all guards of all patches.
        """
        from .HgQueuesListAllGuardsDialog import HgQueuesListAllGuardsDialog
        self.queuesListAllGuardsDialog = HgQueuesListAllGuardsDialog(self.vcs)
        self.queuesListAllGuardsDialog.show()
        self.queuesListAllGuardsDialog.start()
    
    def hgQueueGuardsDefine(self):
        """
        Public method to define guards for the current or a named patch.
        """
        patchnames = sorted(self.__getPatchesList(Queues.SERIES_LIST))
        if patchnames:
            from .HgQueuesDefineGuardsDialog import HgQueuesDefineGuardsDialog
            self.queuesDefineGuardsDialog = HgQueuesDefineGuardsDialog(
                self.vcs, self, patchnames)
            self.queuesDefineGuardsDialog.show()
            self.queuesDefineGuardsDialog.start()
        else:
            E5MessageBox.information(
                None,
                self.tr("Define Guards"),
                self.tr("""No patches available to define guards for."""))
    
    def hgQueueGuardsDropAll(self):
        """
        Public method to drop all guards of the current or a named patch.
        """
        patchnames = sorted(
            self.__getPatchesList(Queues.SERIES_LIST))
        if patchnames:
            patch, ok = QInputDialog.getItem(
                None,
                self.tr("Drop All Guards"),
                self.tr("Select the patch to drop guards for"
                        " (leave empty for the current patch):"),
                [""] + patchnames,
                0, False)
            if ok:
                args = self.vcs.initCommand("qguard")
                if patch:
                    args.append(patch)
                args.append("--none")
                
                client = self.vcs.getClient()
                client.runcommand(args)
        else:
            E5MessageBox.information(
                None,
                self.tr("Drop All Guards"),
                self.tr("""No patches available to define guards for."""))
    
    def hgQueueGuardsSetActive(self):
        """
        Public method to set the active guards.
        """
        guardsList = self.getGuardsList()
        if guardsList:
            activeGuardsList = self.getGuardsList(allGuards=False)
            from .HgQueuesGuardsSelectionDialog import (
                HgQueuesGuardsSelectionDialog
            )
            dlg = HgQueuesGuardsSelectionDialog(
                guardsList, activeGuards=activeGuardsList, listOnly=False)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                guards = dlg.getData()
                if guards:
                    args = self.vcs.initCommand("qselect")
                    args.extend(guards)
                    
                    dia = HgDialog(self.tr('Set Active Guards'), self.vcs)
                    res = dia.startProcess(args)
                    if res:
                        dia.exec()
        else:
            E5MessageBox.information(
                None,
                self.tr("Set Active Guards"),
                self.tr("""No guards available to select from."""))
            return
    
    def hgQueueGuardsDeactivate(self):
        """
        Public method to deactivate all active guards.
        """
        args = self.vcs.initCommand("qselect")
        args.append("--none")
        
        dia = HgDialog(self.tr('Deactivate Guards'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
    
    def hgQueueGuardsIdentifyActive(self):
        """
        Public method to list all active guards.
        """
        guardsList = self.getGuardsList(allGuards=False)
        if guardsList:
            from .HgQueuesGuardsSelectionDialog import (
                HgQueuesGuardsSelectionDialog
            )
            dlg = HgQueuesGuardsSelectionDialog(guardsList, listOnly=True)
            dlg.exec()
    
    def hgQueueCreateRenameQueue(self, isCreate):
        """
        Public method to create a new queue or rename the active queue.
        
        @param isCreate flag indicating to create a new queue (boolean)
        """
        if isCreate:
            title = self.tr("Create New Queue")
        else:
            title = self.tr("Rename Active Queue")
        from .HgQueuesQueueManagementDialog import (
            HgQueuesQueueManagementDialog
        )
        dlg = HgQueuesQueueManagementDialog(
            HgQueuesQueueManagementDialog.NAME_INPUT,
            title, False, self.vcs)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            queueName = dlg.getData()
            if queueName:
                args = self.vcs.initCommand("qqueue")
                if isCreate:
                    args.append("--create")
                else:
                    args.append("--rename")
                args.append(queueName)
                
                client = self.vcs.getClient()
                error = client.runcommand(args)[1]
                
                if error:
                    if isCreate:
                        errMsg = self.tr(
                            "Error while creating a new queue.")
                    else:
                        errMsg = self.tr(
                            "Error while renaming the active queue.")
                    E5MessageBox.warning(
                        None,
                        title,
                        """<p>{0}</p><p>{1}</p>""".format(errMsg, error))
                else:
                    if (
                        self.queuesListQueuesDialog is not None and
                        self.queuesListQueuesDialog.isVisible()
                    ):
                        self.queuesListQueuesDialog.refresh()
    
    def hgQueueDeletePurgeActivateQueue(self, operation):
        """
        Public method to delete the reference to a queue and optionally
        remove the patch directory or set the active queue.
        
        @param operation operation to be performed (Queues.QUEUE_DELETE,
            Queues.QUEUE_PURGE, Queues.QUEUE_ACTIVATE)
        @exception ValueError raised to indicate an invalid operation
        """
        if operation == Queues.QUEUE_PURGE:
            title = self.tr("Purge Queue")
        elif operation == Queues.QUEUE_DELETE:
            title = self.tr("Delete Queue")
        elif operation == Queues.QUEUE_ACTIVATE:
            title = self.tr("Activate Queue")
        else:
            raise ValueError("illegal value for operation")
        
        from .HgQueuesQueueManagementDialog import (
            HgQueuesQueueManagementDialog
        )
        dlg = HgQueuesQueueManagementDialog(
            HgQueuesQueueManagementDialog.QUEUE_INPUT,
            title, True, self.vcs)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            queueName = dlg.getData()
            if queueName:
                args = self.vcs.initCommand("qqueue")
                if operation == Queues.QUEUE_PURGE:
                    args.append("--purge")
                elif operation == Queues.QUEUE_DELETE:
                    args.append("--delete")
                args.append(queueName)
                
                client = self.vcs.getClient()
                error = client.runcommand(args)[1]
                
                if error:
                    if operation == Queues.QUEUE_PURGE:
                        errMsg = self.tr("Error while purging the queue.")
                    elif operation == Queues.QUEUE_DELETE:
                        errMsg = self.tr("Error while deleting the queue.")
                    elif operation == Queues.QUEUE_ACTIVATE:
                        errMsg = self.tr(
                            "Error while setting the active queue.")
                    E5MessageBox.warning(
                        None,
                        title,
                        """<p>{0}</p><p>{1}</p>""".format(errMsg, error))
                else:
                    if (
                        self.queuesListQueuesDialog is not None and
                        self.queuesListQueuesDialog.isVisible()
                    ):
                        self.queuesListQueuesDialog.refresh()
    
    def hgQueueListQueues(self):
        """
        Public method to list available queues.
        """
        from .HgQueuesQueueManagementDialog import (
            HgQueuesQueueManagementDialog
        )
        self.queuesListQueuesDialog = HgQueuesQueueManagementDialog(
            HgQueuesQueueManagementDialog.NO_INPUT,
            self.tr("Available Queues"),
            False, self.vcs)
        self.queuesListQueuesDialog.show()
    
    def hgQueueInit(self, name):
        """
        Public method to initialize a new queue repository.
        
        @param name directory name (string)
        """
        args = self.vcs.initCommand("init")
        args.append('--mq')
        args.append(self.vcs.getClient().getRepository())
        # init is not possible with the command server
        dia = HgDialog(
            self.tr('Initializing new queue repository'), self.vcs)
        res = dia.startProcess(args)
        if res:
            dia.exec()
    
    def hgQueueStatus(self, name):
        """
        Public method used to view the status of a queue repository.
        
        @param name directory name (string)
        """
        from ..HgStatusDialog import HgStatusDialog
        self.queueStatusDialog = HgStatusDialog(self.vcs, mq=True)
        self.queueStatusDialog.show()
        self.queueStatusDialog.start(name)
