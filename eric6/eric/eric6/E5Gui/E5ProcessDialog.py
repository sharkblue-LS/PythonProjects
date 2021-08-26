# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog starting a process and showing its output.
"""

import os
import re

from PyQt5.QtCore import (
    QProcess, QTimer, pyqtSlot, Qt, QCoreApplication, QProcessEnvironment
)
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit

from E5Gui import E5MessageBox

from .Ui_E5ProcessDialog import Ui_E5ProcessDialog

from Globals import strToQByteArray
import Preferences


class E5ProcessDialog(QDialog, Ui_E5ProcessDialog):
    """
    Class implementing a dialog starting a process and showing its output.
    
    It starts a QProcess and displays a dialog that
    shows the output of the process. The dialog is modal,
    which causes a synchronized execution of the process.
    """
    def __init__(self, outputTitle="", windowTitle="", showProgress=False,
                 parent=None):
        """
        Constructor
        
        @param outputTitle title for the output group
        @type str
        @param windowTitle title of the dialog
        @type str
        @param showProgress flag indicating to show a progress bar
        @type bool
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5ProcessDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        font = Preferences.getEditorOtherFonts("MonospacedFont")
        self.resultbox.setFontFamily(font.family())
        self.resultbox.setFontPointSize(font.pointSize())
        self.errors.setFontFamily(font.family())
        self.errors.setFontPointSize(font.pointSize())
        
        if windowTitle:
            self.setWindowTitle(windowTitle)
        if outputTitle:
            self.outputGroup.setTitle(outputTitle)
        self.__showProgress = showProgress
        self.progressBar.setVisible(self.__showProgress)
        
        self.__process = None
        self.__progressRe = re.compile(r"""(\d{1,3})\s*%""")
        
        self.show()
        QCoreApplication.processEvents()
    
    def __finish(self):
        """
        Private slot called when the process finished or the user pressed
        the button.
        """
        if (
            self.__process is not None and
            self.__process.state() != QProcess.ProcessState.NotRunning
        ):
            self.__process.terminate()
            QTimer.singleShot(2000, self.__process.kill)
            self.__process.waitForFinished(3000)
        
        self.inputGroup.setEnabled(False)
        self.inputGroup.hide()
        
        self.__process = None
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setFocus(
            Qt.FocusReason.OtherFocusReason)
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked
        @type QAbstractButton
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.statusLabel.setText(self.tr("Process canceled."))
            self.__finish()
    
    def __procFinished(self, exitCode, exitStatus):
        """
        Private slot connected to the finished signal.
        
        @param exitCode exit code of the process
        @type int
        @param exitStatus exit status of the process
        @type QProcess.ExitStatus
        """
        self.__normal = (
            (exitStatus == QProcess.ExitStatus.NormalExit) and
            (exitCode == 0)
        )
        if self.__normal:
            self.statusLabel.setText(self.tr("Process finished successfully."))
        elif exitStatus == QProcess.ExitStatus.CrashExit:
            self.statusLabel.setText(self.tr("Process crashed."))
        else:
            self.statusLabel.setText(
                self.tr("Process finished with exit code {0}")
                .format(exitCode))
        self.__finish()
    
    def startProcess(self, program, args, workingDir=None, showArgs=True,
                     environment=None):
        """
        Public slot used to start the process.
        
        @param program path of the program to be executed
        @type str
        @param args list of arguments for the process
        @type list of str
        @param workingDir working directory for the process
        @type str
        @param showArgs flag indicating to show the arguments
        @type bool
        @param environment dictionary of environment settings to add
            or change for the process
        @type dict
        @return flag indicating a successful start of the process
        @rtype bool
        """
        self.errorGroup.hide()
        self.__normal = False
        self.__intercept = False
        
        if environment is None:
            environment = {}
        
        if showArgs:
            self.resultbox.append(program + ' ' + ' '.join(args))
            self.resultbox.append('')
        
        self.__process = QProcess()
        if environment:
            env = QProcessEnvironment.systemEnvironment()
            for key, value in environment.items():
                env.insert(key, value)
            self.__process.setProcessEnvironment(env)
        
        self.__process.finished.connect(self.__procFinished)
        self.__process.readyReadStandardOutput.connect(self.__readStdout)
        self.__process.readyReadStandardError.connect(self.__readStderr)
        
        if workingDir:
            self.__process.setWorkingDirectory(workingDir)
        
        self.__process.start(program, args)
        procStarted = self.__process.waitForStarted(10000)
        if not procStarted:
            self.buttonBox.setFocus()
            self.inputGroup.setEnabled(False)
            E5MessageBox.critical(
                self,
                self.tr('Process Generation Error'),
                self.tr(
                    '<p>The process <b>{0}</b> could not be started.</p>'
                ).format(program))
        else:
            self.inputGroup.setEnabled(True)
            self.inputGroup.show()
        
        return procStarted
    
    def normalExit(self):
        """
        Public method to check for a normal process termination.
        
        @return flag indicating normal process termination
        @rtype bool
        """
        return self.__normal
    
    def normalExitWithoutErrors(self):
        """
        Public method to check for a normal process termination without
        error messages.
        
        @return flag indicating normal process termination
        @rtype bool
        """
        return self.__normal and self.errors.toPlainText() == ""
    
    def __readStdout(self):
        """
        Private slot to handle the readyReadStandardOutput signal.
        
        It reads the output of the process and inserts it into the
        output pane.
        """
        if self.__process is not None:
            s = str(self.__process.readAllStandardOutput(),
                    Preferences.getSystem("IOEncoding"),
                    'replace')
            if self.__showProgress:
                match = self.__progressRe.search(s)
                if match:
                    progress = int(match.group(1))
                    self.progressBar.setValue(progress)
                    if not s.endswith("\n"):
                        s = s + "\n"
            self.resultbox.insertPlainText(s)
            self.resultbox.ensureCursorVisible()
            
            QCoreApplication.processEvents()
    
    def __readStderr(self):
        """
        Private slot to handle the readyReadStandardError signal.
        
        It reads the error output of the process and inserts it into the
        error pane.
        """
        if self.__process is not None:
            s = str(self.__process.readAllStandardError(),
                    Preferences.getSystem("IOEncoding"),
                    'replace')
            
            self.errorGroup.show()
            self.errors.insertPlainText(s)
            self.errors.ensureCursorVisible()
            
            QCoreApplication.processEvents()
    
    def on_passwordCheckBox_toggled(self, isOn):
        """
        Private slot to handle the password checkbox toggled.
        
        @param isOn flag indicating the status of the check box
        @type bool
        """
        if isOn:
            self.input.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.input.setEchoMode(QLineEdit.EchoMode.Normal)
    
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
        
        self.__process.write(strToQByteArray(inputTxt))
        
        self.passwordCheckBox.setChecked(False)
        self.input.clear()
    
    def on_input_returnPressed(self):
        """
        Private slot to handle the press of the return key in the input field.
        """
        self.__intercept = True
        self.on_sendButton_clicked()
    
    def keyPressEvent(self, evt):
        """
        Protected slot to handle a key press event.
        
        @param evt the key press event (QKeyEvent)
        """
        if self.__intercept:
            self.__intercept = False
            evt.accept()
            return
        
        super(E5ProcessDialog, self).keyPressEvent(evt)
