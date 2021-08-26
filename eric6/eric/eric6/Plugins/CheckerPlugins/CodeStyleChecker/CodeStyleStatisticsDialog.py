# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog showing statistical data for the last code
style checker run.
"""

import textwrap

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

from .translations import getTranslatedMessage

from .Ui_CodeStyleStatisticsDialog import Ui_CodeStyleStatisticsDialog

import UI.PixmapCache


class CodeStyleStatisticsDialog(QDialog, Ui_CodeStyleStatisticsDialog):
    """
    Class implementing a dialog showing statistical data for the last
    code style checker run.
    """
    def __init__(self, statistics, parent=None):
        """
        Constructor
        
        @param statistics dictionary with the statistical data
        @param parent reference to the parent widget (QWidget)
        """
        super(CodeStyleStatisticsDialog, self).__init__(parent)
        self.setupUi(self)
        
        stats = statistics.copy()
        filesCount = stats["_FilesCount"]
        filesIssues = stats["_FilesIssues"]
        fixesCount = stats["_IssuesFixed"]
        ignoresCount = stats["_IgnoredErrors"]
        securityOk = stats["_SecurityOK"]
        del stats["_FilesCount"]
        del stats["_FilesIssues"]
        del stats["_IssuesFixed"]
        del stats["_IgnoredErrors"]
        del stats["_SecurityOK"]
        
        totalIssues = 0
        
        textWrapper = textwrap.TextWrapper(width=80)
        
        for code in sorted(stats.keys()):
            message = getTranslatedMessage(code, [], example=True)
            if message is None:
                continue
            
            self.__createItem(stats[code], code,
                              "\n".join(textWrapper.wrap(message)))
            totalIssues += stats[code]
        
        self.totalIssues.setText(
            self.tr("%n issue(s) found", "", totalIssues))
        self.ignoredIssues.setText(
            self.tr("%n issue(s) ignored", "", ignoresCount))
        self.fixedIssues.setText(
            self.tr("%n issue(s) fixed", "", fixesCount))
        self.filesChecked.setText(
            self.tr("%n file(s) checked", "", filesCount))
        self.filesIssues.setText(
            self.tr("%n file(s) with issues found", "", filesIssues))
        self.securityOk.setText(
            self.tr("%n security issue(s) acknowledged", "", securityOk))
        
        self.statisticsList.resizeColumnToContents(0)
        self.statisticsList.resizeColumnToContents(1)
    
    def __createItem(self, count, code, message):
        """
        Private method to create an entry in the result list.
        
        @param count occurrences of the issue (integer)
        @param code of a code style issue message (string)
        @param message code style issue message to be shown (string)
        """
        itm = QTreeWidgetItem(self.statisticsList, [
            "{0:6d}".format(count), code, message])
        if code.startswith(("W", "C", "M")):
            itm.setIcon(1, UI.PixmapCache.getIcon("warning"))
        elif code.startswith("E"):
            itm.setIcon(1, UI.PixmapCache.getIcon("syntaxError"))
        elif code.startswith("N"):
            itm.setIcon(1, UI.PixmapCache.getIcon("namingError"))
        elif code.startswith("D"):
            itm.setIcon(1, UI.PixmapCache.getIcon("docstringError"))
        elif code.startswith("S"):
            itm.setIcon(1, UI.PixmapCache.getIcon("securityLow"))
        elif code.startswith("P"):
            itm.setIcon(1, UI.PixmapCache.getIcon("dirClosed"))
        
        itm.setTextAlignment(
            0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        itm.setTextAlignment(
            1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
