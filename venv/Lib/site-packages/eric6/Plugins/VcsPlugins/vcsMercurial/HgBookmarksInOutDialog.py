# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show a list of incoming or outgoing bookmarks.
"""

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QHeaderView, QTreeWidgetItem
)

from .Ui_HgBookmarksInOutDialog import Ui_HgBookmarksInOutDialog


class HgBookmarksInOutDialog(QDialog, Ui_HgBookmarksInOutDialog):
    """
    Class implementing a dialog to show a list of incoming or outgoing
    bookmarks.
    """
    INCOMING = 0
    OUTGOING = 1
    
    def __init__(self, vcs, mode, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param mode mode of the dialog (HgBookmarksInOutDialog.INCOMING,
            HgBookmarksInOutDialog.OUTGOING)
        @param parent reference to the parent widget (QWidget)
        @exception ValueError raised to indicate an invalid dialog mode
        """
        super(HgBookmarksInOutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        if mode not in [self.INCOMING, self.OUTGOING]:
            raise ValueError("Bad value for mode")
        if mode == self.INCOMING:
            self.setWindowTitle(self.tr("Mercurial Incoming Bookmarks"))
        elif mode == self.OUTGOING:
            self.setWindowTitle(self.tr("Mercurial Outgoing Bookmarks"))
        
        self.vcs = vcs
        self.mode = mode
        self.__hgClient = vcs.getClient()
        
        self.bookmarksList.headerItem().setText(
            self.bookmarksList.columnCount(), "")
        self.bookmarksList.header().setSortIndicator(
            3, Qt.SortOrder.AscendingOrder)
        
        self.show()
        QCoreApplication.processEvents()
    
    def closeEvent(self, e):
        """
        Protected slot implementing a close event handler.
        
        @param e close event (QCloseEvent)
        """
        if self.__hgClient.isExecuting():
            self.__hgClient.cancel()
        
        e.accept()
    
    def start(self):
        """
        Public slot to start the bookmarks command.
        
        @exception ValueError raised to indicate an invalid dialog mode
        """
        self.errorGroup.hide()
        
        self.intercept = False
        self.activateWindow()
        
        if self.mode == self.INCOMING:
            args = self.vcs.initCommand("incoming")
        elif self.mode == self.OUTGOING:
            args = self.vcs.initCommand("outgoing")
        else:
            raise ValueError("Bad value for mode")
        args.append('--bookmarks')
        
        out, err = self.__hgClient.runcommand(args)
        if err:
            self.__showError(err)
        if out:
            for line in out.splitlines():
                self.__processOutputLine(line)
                if self.__hgClient.wasCanceled():
                    break
        self.__finish()
    
    def __finish(self):
        """
        Private slot called when the process finished or the user pressed
        the button.
        """
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setFocus(
                Qt.FocusReason.OtherFocusReason)
        
        if self.bookmarksList.topLevelItemCount() == 0:
            # no bookmarks defined
            self.__generateItem(self.tr("no bookmarks found"), "")
        self.__resizeColumns()
        self.__resort()
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            if self.__hgClient:
                self.__hgClient.cancel()
            else:
                self.__finish()
    
    def __resort(self):
        """
        Private method to resort the tree.
        """
        self.bookmarksList.sortItems(
            self.bookmarksList.sortColumn(),
            self.bookmarksList.header().sortIndicatorOrder())
    
    def __resizeColumns(self):
        """
        Private method to resize the list columns.
        """
        self.bookmarksList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.bookmarksList.header().setStretchLastSection(True)
    
    def __generateItem(self, changeset, name):
        """
        Private method to generate a bookmark item in the bookmarks list.
        
        @param changeset changeset of the bookmark (string)
        @param name name of the bookmark (string)
        """
        QTreeWidgetItem(self.bookmarksList, [
            name,
            changeset])
    
    def __processOutputLine(self, line):
        """
        Private method to process the lines of output.
        
        @param line output line to be processed (string)
        """
        if line.startswith(" "):
            li = line.strip().split()
            changeset = li[-1]
            del li[-1]
            name = " ".join(li)
            self.__generateItem(changeset, name)
    
    def __showError(self, out):
        """
        Private slot to show some error.
        
        @param out error to be shown (string)
        """
        self.errorGroup.show()
        self.errors.insertPlainText(out)
        self.errors.ensureCursorVisible()
