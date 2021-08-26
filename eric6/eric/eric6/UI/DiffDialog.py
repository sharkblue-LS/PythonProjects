# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to compare two files.
"""

import os
import time

from PyQt5.QtCore import QFileInfo, QEvent, pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QApplication, QDialogButtonBox

from E5Gui import E5MessageBox, E5FileDialog
from E5Gui.E5MainWindow import E5MainWindow
from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_DiffDialog import Ui_DiffDialog
from .DiffHighlighter import DiffHighlighter

import Utilities
import Preferences

from difflib import unified_diff, context_diff


class DiffDialog(QWidget, Ui_DiffDialog):
    """
    Class implementing a dialog to compare two files.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(DiffDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.file1Picker.setMode(E5PathPickerModes.OpenFileMode)
        self.file2Picker.setMode(E5PathPickerModes.OpenFileMode)
        
        self.diffButton = self.buttonBox.addButton(
            self.tr("Compare"), QDialogButtonBox.ButtonRole.ActionRole)
        self.diffButton.setToolTip(
            self.tr("Press to perform the comparison of the two files"))
        self.saveButton = self.buttonBox.addButton(
            self.tr("Save"), QDialogButtonBox.ButtonRole.ActionRole)
        self.saveButton.setToolTip(
            self.tr("Save the output to a patch file"))
        self.diffButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.diffButton.setDefault(True)
        
        self.searchWidget.attachTextEdit(self.contents)
        
        self.filename1 = ''
        self.filename2 = ''
        
        self.updateInterval = 20    # update every 20 lines
        
        font = Preferences.getEditorOtherFonts("MonospacedFont")
        self.contents.document().setDefaultFont(font)
        
        self.highlighter = DiffHighlighter(self.contents.document())
        
        # connect some of our widgets explicitly
        self.file1Picker.textChanged.connect(self.__fileChanged)
        self.file2Picker.textChanged.connect(self.__fileChanged)
        
    def show(self, filename=None):
        """
        Public slot to show the dialog.
        
        @param filename name of a file to use as the first file (string)
        """
        if filename:
            self.file1Picker.setText(filename)
        super(DiffDialog, self).show()
        
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.diffButton:
            self.on_diffButton_clicked()
        elif button == self.saveButton:
            self.on_saveButton_clicked()
        
    @pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Private slot to handle the Save button press.
        
        It saves the diff shown in the dialog to a file in the local
        filesystem.
        """
        dname, fname = Utilities.splitPath(self.filename2)
        if fname != '.':
            fname = "{0}.diff".format(self.filename2)
        else:
            fname = dname
            
        fname, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
            self,
            self.tr("Save Diff"),
            fname,
            self.tr("Patch Files (*.diff)"),
            None,
            E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
        
        if not fname:
            return
        
        ext = QFileInfo(fname).suffix()
        if not ext:
            ex = selectedFilter.split("(*")[1].split(")")[0]
            if ex:
                fname += ex
        if QFileInfo(fname).exists():
            res = E5MessageBox.yesNo(
                self,
                self.tr("Save Diff"),
                self.tr("<p>The patch file <b>{0}</b> already exists."
                        " Overwrite it?</p>").format(fname),
                icon=E5MessageBox.Warning)
            if not res:
                return
        fname = Utilities.toNativeSeparators(fname)
        
        txt = self.contents.toPlainText()
        try:
            with open(fname, "w", encoding="utf-8") as f:
                try:
                    f.write(txt)
                except UnicodeError:
                    pass
        except OSError as why:
            E5MessageBox.critical(
                self, self.tr('Save Diff'),
                self.tr(
                    '<p>The patch file <b>{0}</b> could not be saved.<br />'
                    'Reason: {1}</p>').format(fname, str(why)))

    @pyqtSlot()
    def on_diffButton_clicked(self):
        """
        Private slot to handle the Compare button press.
        """
        self.filename1 = Utilities.toNativeSeparators(self.file1Picker.text())
        try:
            filemtime1 = time.ctime(os.stat(self.filename1).st_mtime)
        except OSError:
            filemtime1 = ""
        try:
            with open(self.filename1, "r", encoding="utf-8") as f1:
                lines1 = f1.readlines()
        except OSError:
            E5MessageBox.critical(
                self,
                self.tr("Compare Files"),
                self.tr(
                    """<p>The file <b>{0}</b> could not be read.</p>""")
                .format(self.filename1))
            return

        self.filename2 = Utilities.toNativeSeparators(self.file2Picker.text())
        try:
            filemtime2 = time.ctime(os.stat(self.filename2).st_mtime)
        except OSError:
            filemtime2 = ""
        try:
            with open(self.filename2, "r", encoding="utf-8") as f2:
                lines2 = f2.readlines()
        except OSError:
            E5MessageBox.critical(
                self,
                self.tr("Compare Files"),
                self.tr(
                    """<p>The file <b>{0}</b> could not be read.</p>""")
                .format(self.filename2))
            return
        
        self.contents.clear()
        self.highlighter.regenerateRules()
        self.saveButton.setEnabled(False)
        
        if self.unifiedRadioButton.isChecked():
            self.__generateUnifiedDiff(
                lines1, lines2, self.filename1, self.filename2,
                filemtime1, filemtime2)
        else:
            self.__generateContextDiff(
                lines1, lines2, self.filename1, self.filename2,
                filemtime1, filemtime2)
        
        tc = self.contents.textCursor()
        tc.movePosition(QTextCursor.MoveOperation.Start)
        self.contents.setTextCursor(tc)
        self.contents.ensureCursorVisible()
        
        self.saveButton.setEnabled(True)

    def __appendText(self, txt):
        """
        Private method to append text to the end of the contents pane.
        
        @param txt text to insert (string)
        """
        tc = self.contents.textCursor()
        tc.movePosition(QTextCursor.MoveOperation.End)
        self.contents.setTextCursor(tc)
        self.contents.insertPlainText(txt)
        
    def __generateUnifiedDiff(self, a, b, fromfile, tofile,
                              fromfiledate, tofiledate):
        """
        Private slot to generate a unified diff output.
        
        @param a first sequence of lines (list of strings)
        @param b second sequence of lines (list of strings)
        @param fromfile filename of the first file (string)
        @param tofile filename of the second file (string)
        @param fromfiledate modification time of the first file (string)
        @param tofiledate modification time of the second file (string)
        """
        paras = 0
        for line in unified_diff(a, b, fromfile, tofile,
                                 fromfiledate, tofiledate):
            self.__appendText(line)
            paras += 1
            if not (paras % self.updateInterval):
                QApplication.processEvents()
            
        if paras == 0:
            self.__appendText(self.tr('There is no difference.'))

    def __generateContextDiff(self, a, b, fromfile, tofile,
                              fromfiledate, tofiledate):
        """
        Private slot to generate a context diff output.
        
        @param a first sequence of lines (list of strings)
        @param b second sequence of lines (list of strings)
        @param fromfile filename of the first file (string)
        @param tofile filename of the second file (string)
        @param fromfiledate modification time of the first file (string)
        @param tofiledate modification time of the second file (string)
        """
        paras = 0
        for line in context_diff(a, b, fromfile, tofile,
                                 fromfiledate, tofiledate):
            self.__appendText(line)
            paras += 1
            if not (paras % self.updateInterval):
                QApplication.processEvents()
            
        if paras == 0:
            self.__appendText(self.tr('There is no difference.'))

    def __fileChanged(self):
        """
        Private slot to enable/disable the Compare button.
        """
        if (
            not self.file1Picker.text() or
            not self.file2Picker.text()
        ):
            self.diffButton.setEnabled(False)
        else:
            self.diffButton.setEnabled(True)


class DiffWindow(E5MainWindow):
    """
    Main window class for the standalone dialog.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(DiffWindow, self).__init__(parent)
        
        self.setStyle(Preferences.getUI("Style"),
                      Preferences.getUI("StyleSheet"))
        
        self.cw = DiffDialog(self)
        self.cw.installEventFilter(self)
        size = self.cw.size()
        self.setCentralWidget(self.cw)
        self.resize(size)
    
    def eventFilter(self, obj, event):
        """
        Public method to filter events.
        
        @param obj reference to the object the event is meant for (QObject)
        @param event reference to the event object (QEvent)
        @return flag indicating, whether the event was handled (boolean)
        """
        if event.type() == QEvent.Type.Close:
            QApplication.exit()
            return True
        
        return False
