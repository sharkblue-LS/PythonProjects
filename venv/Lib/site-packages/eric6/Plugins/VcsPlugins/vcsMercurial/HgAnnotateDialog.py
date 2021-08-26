# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the output of the hg annotate command.
"""

import re

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QHeaderView, QTreeWidgetItem
)

from .Ui_HgAnnotateDialog import Ui_HgAnnotateDialog

import Preferences


class HgAnnotateDialog(QDialog, Ui_HgAnnotateDialog):
    """
    Class implementing a dialog to show the output of the hg annotate command.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param parent parent widget (QWidget)
        """
        super(HgAnnotateDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.vcs = vcs
        self.__hgClient = vcs.getClient()
        
        self.__annotateRe = re.compile(
            r"""(.+)\s+(\d+)\s+([0-9a-fA-F]+)\s+([0-9-]+)\s+(.+)""")
        
        self.annotateList.headerItem().setText(
            self.annotateList.columnCount(), "")
        font = Preferences.getEditorOtherFonts("MonospacedFont")
        self.annotateList.setFont(font)
        
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
    
    def start(self, fn):
        """
        Public slot to start the annotate command.
        
        @param fn filename to show the annotation for (string)
        """
        self.annotateList.clear()
        self.errorGroup.hide()
        self.intercept = False
        self.activateWindow()
        self.lineno = 1
        
        args = self.vcs.initCommand("annotate")
        args.append('--follow')
        args.append('--user')
        args.append('--date')
        args.append('--number')
        args.append('--changeset')
        args.append('--quiet')
        args.append(fn)
        
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
        
        self.__resizeColumns()
    
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
    
    def __resizeColumns(self):
        """
        Private method to resize the list columns.
        """
        self.annotateList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
    
    def __generateItem(self, revision, changeset, author, date, text):
        """
        Private method to generate an annotate item in the annotation list.
        
        @param revision revision string (string)
        @param changeset changeset string (string)
        @param author author of the change (string)
        @param date date of the change (string)
        @param text text of the change (string)
        """
        itm = QTreeWidgetItem(
            self.annotateList,
            [revision, changeset, author, date, "{0:d}".format(self.lineno),
             text])
        self.lineno += 1
        itm.setTextAlignment(0, Qt.AlignmentFlag.AlignRight)
        itm.setTextAlignment(4, Qt.AlignmentFlag.AlignRight)
    
    def __processOutputLine(self, line):
        """
        Private method to process the lines of output.
        
        @param line output line to be processed (string)
        """
        try:
            info, text = line.split(": ", 1)
        except ValueError:
            info = line[:-2]
            text = ""
        match = self.__annotateRe.match(info)
        author, rev, changeset, date, file = match.groups()
        self.__generateItem(rev.strip(), changeset.strip(), author.strip(),
                            date.strip(), text)
    
    def __showError(self, out):
        """
        Private slot to show some error.
        
        @param out error to be shown (string)
        """
        self.errorGroup.show()
        self.errors.insertPlainText(out)
        self.errors.ensureCursorVisible()
