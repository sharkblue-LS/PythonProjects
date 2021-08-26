# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the output of git blame.
"""

import os
import re

from PyQt5.QtCore import pyqtSlot, QProcess, QTimer, Qt, QCoreApplication
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QHeaderView, QLineEdit, QTreeWidgetItem
)

from E5Gui import E5MessageBox

from .Ui_GitBlameDialog import Ui_GitBlameDialog

import Preferences
from Globals import strToQByteArray


class GitBlameDialog(QDialog, Ui_GitBlameDialog):
    """
    Class implementing a dialog to show the output of git blame.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param parent reference to the parent widget (QWidget)
        """
        super(GitBlameDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.vcs = vcs
        
        self.__blameRe = re.compile(
            r"""\^?([0-9a-fA-F]+)\s+\((.+)\s+(\d{4}-\d{2}-\d{2})\s+"""
            r"""(\d{2}:\d{2}):\d{2}\s+[+-]\d{4}\s+(\d+)\)\s?(.*)""")
        # commit - author - date - time - lineno. - text
        
        self.blameList.headerItem().setText(
            self.blameList.columnCount(), "")
        font = Preferences.getEditorOtherFonts("MonospacedFont")
        self.blameList.setFont(font)
        
        self.process = QProcess()
        self.process.finished.connect(self.__procFinished)
        self.process.readyReadStandardOutput.connect(self.__readStdout)
        self.process.readyReadStandardError.connect(self.__readStderr)
        
        self.show()
        QCoreApplication.processEvents()
    
    def closeEvent(self, e):
        """
        Protected slot implementing a close event handler.
        
        @param e close event (QCloseEvent)
        """
        if (
            self.process is not None and
            self.process.state() != QProcess.ProcessState.NotRunning
        ):
            self.process.terminate()
            QTimer.singleShot(2000, self.process.kill)
            self.process.waitForFinished(3000)
        
        e.accept()
    
    def start(self, fn):
        """
        Public slot to start the blame command.
        
        @param fn filename to show the blame for (string)
        """
        self.blameList.clear()
        
        self.errorGroup.hide()
        self.intercept = False
        self.activateWindow()
        
        dname, fname = self.vcs.splitPath(fn)
        
        # find the root of the repo
        repodir = dname
        while not os.path.isdir(os.path.join(repodir, self.vcs.adminDir)):
            repodir = os.path.dirname(repodir)
            if os.path.splitdrive(repodir)[1] == os.sep:
                return
        
        args = self.vcs.initCommand("blame")
        args.append('--abbrev={0}'.format(
            self.vcs.getPlugin().getPreferences("CommitIdLength")))
        args.append('--date=iso')
        args.append(fn)
        
        self.process.kill()
        self.process.setWorkingDirectory(repodir)
        
        self.process.start('git', args)
        procStarted = self.process.waitForStarted(5000)
        if not procStarted:
            self.inputGroup.setEnabled(False)
            self.inputGroup.hide()
            E5MessageBox.critical(
                self,
                self.tr('Process Generation Error'),
                self.tr(
                    'The process {0} could not be started. '
                    'Ensure, that it is in the search path.'
                ).format('git'))
        else:
            self.inputGroup.setEnabled(True)
            self.inputGroup.show()
    
    def __finish(self):
        """
        Private slot called when the process finished or the user pressed
        the button.
        """
        if (
            self.process is not None and
            self.process.state() != QProcess.ProcessState.NotRunning
        ):
            self.process.terminate()
            QTimer.singleShot(2000, self.process.kill)
            self.process.waitForFinished(3000)
        
        self.inputGroup.setEnabled(False)
        self.inputGroup.hide()
        
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
            self.__finish()
    
    def __procFinished(self, exitCode, exitStatus):
        """
        Private slot connected to the finished signal.
        
        @param exitCode exit code of the process (integer)
        @param exitStatus exit status of the process (QProcess.ExitStatus)
        """
        self.__finish()
    
    def __resizeColumns(self):
        """
        Private method to resize the list columns.
        """
        self.blameList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
    
    def __generateItem(self, commitId, author, date, time, lineno, text):
        """
        Private method to generate a blame item in the annotation list.
        
        @param commitId commit identifier (string)
        @param author author of the change (string)
        @param date date of the change (string)
        @param time time of the change (string)
        @param lineno line number of the change (string)
        @param text name (path) of the tag (string)
        """
        itm = QTreeWidgetItem(
            self.blameList,
            [commitId, author, date, time, lineno, text])
        itm.setTextAlignment(0, Qt.AlignmentFlag.AlignRight)
        itm.setTextAlignment(4, Qt.AlignmentFlag.AlignRight)
    
    def __readStdout(self):
        """
        Private slot to handle the readyReadStdout signal.
        
        It reads the output of the process, formats it and inserts it into
        the annotation list.
        """
        self.process.setReadChannel(QProcess.ProcessChannel.StandardOutput)
        
        while self.process.canReadLine():
            line = str(self.process.readLine(),
                       Preferences.getSystem("IOEncoding"),
                       'replace').strip()
            match = self.__blameRe.match(line)
            commitId, author, date, time, lineno, text = match.groups()
            self.__generateItem(commitId, author, date, time, lineno, text)
    
    def __readStderr(self):
        """
        Private slot to handle the readyReadStderr signal.
        
        It reads the error output of the process and inserts it into the
        error pane.
        """
        if self.process is not None:
            s = str(self.process.readAllStandardError(),
                    Preferences.getSystem("IOEncoding"),
                    'replace')
            
            self.errorGroup.show()
            self.errors.insertPlainText(s)
            self.errors.ensureCursorVisible()
    
    @pyqtSlot()
    def on_sendButton_clicked(self):
        """
        Private slot to send the input to the git process.
        """
        inputTxt = self.input.text()
        inputTxt += os.linesep
        
        if self.passwordCheckBox.isChecked():
            self.errors.insertPlainText(os.linesep)
            self.errors.ensureCursorVisible()
        else:
            self.errors.insertPlainText(inputTxt)
            self.errors.ensureCursorVisible()
        
        self.process.write(strToQByteArray(inputTxt))
        
        self.passwordCheckBox.setChecked(False)
        self.input.clear()
    
    @pyqtSlot()
    def on_input_returnPressed(self):
        """
        Private slot to handle the press of the return key in the input field.
        """
        self.intercept = True
        self.on_sendButton_clicked()
    
    @pyqtSlot(bool)
    def on_passwordCheckBox_toggled(self, checked):
        """
        Private slot to handle the password checkbox toggled.
        
        @param checked flag indicating the status of the check box (boolean)
        """
        if checked:
            self.input.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.input.setEchoMode(QLineEdit.EchoMode.Normal)
    
    def keyPressEvent(self, evt):
        """
        Protected slot to handle a key press event.
        
        @param evt the key press event (QKeyEvent)
        """
        if self.intercept:
            self.intercept = False
            evt.accept()
            return
        super(GitBlameDialog, self).keyPressEvent(evt)
