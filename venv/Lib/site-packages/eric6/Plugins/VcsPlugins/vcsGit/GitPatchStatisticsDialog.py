# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show some patch file statistics.
"""

import os

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QHeaderView

from E5Gui import E5MessageBox

from .Ui_GitPatchStatisticsDialog import Ui_GitPatchStatisticsDialog

import Preferences


class GitPatchStatisticsDialog(QDialog, Ui_GitPatchStatisticsDialog):
    """
    Class implementing a dialog to show some patch file statistics.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the VCS object (Git)
        @param parent reference to the parent widget (QWidget)
        """
        super(GitPatchStatisticsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.__vcs = vcs
        
        self.changesTreeWidget.headerItem().setText(
            self.changesTreeWidget.columnCount(), "")
        self.changesTreeWidget.header().setSortIndicator(
            2, Qt.SortOrder.AscendingOrder)
    
    def start(self, projectDir, patchCheckData):
        """
        Public method to start the statistics process.
        
        @param projectDir directory name of the project (string)
        @param patchCheckData tuple of data as returned by the
            GitPatchFilesDialog.getData() method
        """
        self.__patchCheckData = patchCheckData
        
        self.changesTreeWidget.clear()
        self.summaryEdit.clear()
        
        # find the root of the repo
        repodir = projectDir
        while not os.path.isdir(os.path.join(repodir, self.__vcs.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        from .GitPatchFilesDialog import GitPatchFilesDialog
        dlg = GitPatchFilesDialog(repodir, patchCheckData)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            patchFilesList, stripCount, inaccurateEof, recount = dlg.getData()
            self.__patchCheckData = (patchFilesList, stripCount,
                                     inaccurateEof, recount)
            if patchFilesList:
                process = QProcess()
                process.setWorkingDirectory(repodir)
                
                # step 1: get the statistics
                args = self.__vcs.initCommand("apply")
                args.append("--numstat")
                if inaccurateEof:
                    args.append("--inaccurate-eof")
                if recount:
                    args.append("--recount")
                args.append("-p{0}".format(stripCount))
                args.extend(patchFilesList)
                
                process.start('git', args)
                procStarted = process.waitForStarted(5000)
                if not procStarted:
                    E5MessageBox.critical(
                        self,
                        self.tr('Process Generation Error'),
                        self.tr(
                            'The process {0} could not be started. '
                            'Ensure, that it is in the search path.'
                        ).format('git'))
                    return
                else:
                    finished = process.waitForFinished(30000)
                    if finished and process.exitCode() == 0:
                        output = str(process.readAllStandardOutput(),
                                     Preferences.getSystem("IOEncoding"),
                                     'replace')
                        for line in output.splitlines():
                            self.__createStatisticsItem(line)
                
                # step 2: get the summary
                args = self.__vcs.initCommand("apply")
                args.append("--summary")
                if inaccurateEof:
                    args.append("--inaccurate-eof")
                if recount:
                    args.append("--recount")
                args.append("-p{0}".format(stripCount))
                args.extend(patchFilesList)
                
                process.start('git', args)
                procStarted = process.waitForStarted(5000)
                if not procStarted:
                    E5MessageBox.critical(
                        self,
                        self.tr('Process Generation Error'),
                        self.tr(
                            'The process {0} could not be started. '
                            'Ensure, that it is in the search path.'
                        ).format('git'))
                    return
                else:
                    finished = process.waitForFinished(30000)
                    if finished and process.exitCode() == 0:
                        output = str(process.readAllStandardOutput(),
                                     Preferences.getSystem("IOEncoding"),
                                     'replace')
                        for line in output.splitlines():
                            self.summaryEdit.appendPlainText(line.strip())
    
    def __createStatisticsItem(self, line):
        """
        Private method to create a file statistics entry.
        
        @param line string with file statistics data (string)
        """
        insertions, deletions, filename = line.strip().split(None, 2)
        itm = QTreeWidgetItem(self.changesTreeWidget,
                              [insertions, deletions, filename])
        itm.setTextAlignment(0, Qt.AlignmentFlag.AlignRight)
        itm.setTextAlignment(1, Qt.AlignmentFlag.AlignRight)
    
    def __resizeColumns(self):
        """
        Private method to resize the list columns.
        """
        self.changesTreeWidget.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.changesTreeWidget.header().setStretchLastSection(True)
    
    def getData(self):
        """
        Public method to get the data used to generate the statistics.
        
        @return tuple of list of patch files, strip count, flag indicating
            that the patch has inaccurate end-of-file marker and a flag
            indicating to not trust the line count information
            (list of string, integer, boolean, boolean)
        """
        return self.__patchCheckData
