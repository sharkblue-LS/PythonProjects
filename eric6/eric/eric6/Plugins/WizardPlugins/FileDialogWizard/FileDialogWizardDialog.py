# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the file dialog wizard dialog.
"""

import os

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QFileDialog, QButtonGroup
)

from E5Gui.E5Completers import E5FileCompleter, E5DirCompleter

from .Ui_FileDialogWizardDialog import Ui_FileDialogWizardDialog

import Globals


class FileDialogWizardDialog(QDialog, Ui_FileDialogWizardDialog):
    """
    Class implementing the color dialog wizard dialog.
    
    It displays a dialog for entering the parameters for the
    E5FileDialog or QFileDialog code generator.
    """
    def __init__(self, dialogVariant, parent=None):
        """
        Constructor
        
        @param dialogVariant variant of the file dialog to be generated
            (-1 = E5FileDialog, 0 = unknown, 5 = PyQt5)
        @type int
        @param parent parent widget
        @type QWidget
        """
        super(FileDialogWizardDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.eStartWithCompleter = E5FileCompleter(self.eStartWith)
        self.eWorkDirCompleter = E5DirCompleter(self.eWorkDir)
        
        self.__typeButtonsGroup = QButtonGroup(self)
        self.__typeButtonsGroup.setExclusive(True)
        self.__typeButtonsGroup.addButton(self.rOpenFile, 1)
        self.__typeButtonsGroup.addButton(self.rOpenFiles, 2)
        self.__typeButtonsGroup.addButton(self.rSaveFile, 3)
        self.__typeButtonsGroup.addButton(self.rfOpenFile, 11)
        self.__typeButtonsGroup.addButton(self.rfOpenFiles, 12)
        self.__typeButtonsGroup.addButton(self.rfSaveFile, 13)
        self.__typeButtonsGroup.addButton(self.rOpenFileUrl, 21)
        self.__typeButtonsGroup.addButton(self.rOpenFileUrls, 22)
        self.__typeButtonsGroup.addButton(self.rSaveFileUrl, 23)
        self.__typeButtonsGroup.addButton(self.rDirectory, 30)
        self.__typeButtonsGroup.addButton(self.rDirectoryUrl, 31)
        self.__typeButtonsGroup.buttonClicked[int].connect(
            self.__toggleInitialFilterAndResult)
        self.__toggleInitialFilterAndResult(1)
        
        self.__dialogVariant = dialogVariant
        if self.__dialogVariant == -1:
            self.pyqtComboBox.addItems(["eric"])
            self.setWindowTitle(self.tr("E5FileDialog Wizard"))
            self.pyqtComboBox.setCurrentIndex(0)
            self.pyqtComboBox.setEnabled(False)
        else:
            self.pyqtComboBox.addItems(["PyQt5", "PyQt6"])
            self.setWindowTitle(self.tr("QFileDialog Wizard"))
            if self.__dialogVariant == 5:
                self.pyqtComboBox.setCurrentIndex(0)
            elif self.__dialogVariant == 6:
                self.pyqtComboBox.setCurrentIndex(1)
            else:
                self.pyqtComboBox.setCurrentIndex(0)
        
        self.rSaveFile.toggled[bool].connect(self.__toggleConfirmCheckBox)
        self.rfSaveFile.toggled[bool].connect(self.__toggleConfirmCheckBox)
        self.rSaveFileUrl.toggled[bool].connect(self.__toggleConfirmCheckBox)
        self.rDirectory.toggled[bool].connect(self.__toggleGroupsAndTest)
        self.rDirectoryUrl.toggled[bool].connect(self.__toggleGroupsAndTest)
        self.cStartWith.toggled[bool].connect(self.__toggleGroupsAndTest)
        self.cWorkDir.toggled[bool].connect(self.__toggleGroupsAndTest)
        self.cFilters.toggled[bool].connect(self.__toggleGroupsAndTest)
        
        self.bTest = self.buttonBox.addButton(
            self.tr("Test"), QDialogButtonBox.ButtonRole.ActionRole)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __adjustOptions(self, options):
        """
        Private method to adjust the file dialog options.
        
        @param options file dialog options (QFileDialog.Options)
        @return modified options (QFileDialog.Options)
        """
        if Globals.isLinuxPlatform():
            options |= QFileDialog.Option.DontUseNativeDialog
        return options
    
    @pyqtSlot(int)
    def on_pyqtComboBox_currentIndexChanged(self, index):
        """
        Private slot to setup the dialog for the selected PyQt variant.
        
        @param index index of the current item
        @type int
        """
        txt = self.pyqtComboBox.itemText(index)
        self.rfOpenFile.setEnabled(txt == "eric")
        self.rfOpenFiles.setEnabled(txt == "eric")
        self.rfSaveFile.setEnabled(txt == "eric")
        
        self.rOpenFileUrl.setEnabled(txt in ["PyQt5", "PyQt6"])
        self.rOpenFileUrls.setEnabled(txt in ["PyQt5", "PyQt6"])
        self.rSaveFileUrl.setEnabled(txt in ["PyQt5", "PyQt6"])
        self.rDirectoryUrl.setEnabled(txt in ["PyQt5", "PyQt6"])
        
        if txt in ["PyQt5", "PyQt6"]:
            if self.rfOpenFile.isChecked():
                self.rOpenFile.setChecked(True)
            elif self.rfOpenFiles.isChecked():
                self.rOpenFiles.setChecked(True)
            elif self.rfSaveFile.isChecked():
                self.rSaveFile.setChecked(True)
        else:
            if self.rOpenFileUrl.isChecked():
                self.rOpenFile.setChecked(True)
            if self.rOpenFileUrls.isChecked():
                self.rOpenFiles.setChecked(True)
            if self.rSaveFileUrl.isChecked():
                self.rSaveFile.setChecked(True)
            if self.rDirectoryUrl.isChecked():
                self.rDirectory.setChecked(True)
        
        if txt == "eric":
            self.__dialogVariant = -1
        elif txt == "PyQt5":
            self.__dialogVariant = 5
        elif txt == "PyQt6":
            self.__dialogVariant = 6
        else:
            # default is PyQt5
            self.__dialogVariant = 5
        
        self.__toggleInitialFilterAndResult(
            self.__typeButtonsGroup.checkedId())
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.bTest:
            self.on_bTest_clicked()
    
    @pyqtSlot()
    def on_bTest_clicked(self):
        """
        Private method to test the selected options.
        """
        if self.rOpenFile.isChecked() or self.rfOpenFile.isChecked():
            if not self.cSymlinks.isChecked():
                options = QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            else:
                options = QFileDialog.Options()
            options = self.__adjustOptions(options)
            QFileDialog.getOpenFileName(
                None,
                self.eCaption.text(),
                self.eStartWith.text(),
                self.eFilters.text(),
                self.eInitialFilter.text(),
                options)
        elif self.rOpenFileUrl.isChecked():
            if not self.cSymlinks.isChecked():
                options = QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            else:
                options = QFileDialog.Options()
            options = self.__adjustOptions(options)
            try:
                QFileDialog.getOpenFileUrl(
                    None,
                    self.eCaption.text(),
                    QUrl(self.eStartWith.text()),
                    self.eFilters.text(),
                    self.eInitialFilter.text(),
                    options,
                    self.schemesEdit.text().split())
            except TypeError:
                # PyQt5 < 5.13.0 contains an error
                QFileDialog.getOpenFileUrl(
                    None,
                    self.eCaption.text(),
                    self.eStartWith.text(),
                    self.eFilters.text(),
                    self.eInitialFilter.text(),
                    options,
                    self.schemesEdit.text().split())
        elif self.rOpenFiles.isChecked() or self.rfOpenFiles.isChecked():
            if not self.cSymlinks.isChecked():
                options = QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            else:
                options = QFileDialog.Options()
            options = self.__adjustOptions(options)
            QFileDialog.getOpenFileNames(
                None,
                self.eCaption.text(),
                self.eStartWith.text(),
                self.eFilters.text(),
                self.eInitialFilter.text(),
                options)
        elif self.rOpenFileUrls.isChecked():
            if not self.cSymlinks.isChecked():
                options = QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            else:
                options = QFileDialog.Options()
            options = self.__adjustOptions(options)
            try:
                QFileDialog.getOpenFileUrls(
                    None,
                    self.eCaption.text(),
                    QUrl(self.eStartWith.text()),
                    self.eFilters.text(),
                    self.eInitialFilter.text(),
                    options,
                    self.schemesEdit.text().split())
            except TypeError:
                # PyQt5 < 5.13.0 contains an error
                QFileDialog.getOpenFileUrls(
                    None,
                    self.eCaption.text(),
                    self.eStartWith.text(),
                    self.eFilters.text(),
                    self.eInitialFilter.text(),
                    options,
                    self.schemesEdit.text().split())
        elif self.rSaveFile.isChecked() or self.rfSaveFile.isChecked():
            if not self.cSymlinks.isChecked():
                options = QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            else:
                options = QFileDialog.Options()
            options = self.__adjustOptions(options)
            QFileDialog.getSaveFileName(
                None,
                self.eCaption.text(),
                self.eStartWith.text(),
                self.eFilters.text(),
                self.eInitialFilter.text(),
                options)
        elif self.rSaveFileUrl.isChecked():
            if not self.cSymlinks.isChecked():
                options = QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            else:
                options = QFileDialog.Options()
            options = self.__adjustOptions(options)
            try:
                QFileDialog.getSaveFileUrl(
                    None,
                    self.eCaption.text(),
                    QUrl(self.eStartWith.text()),
                    self.eFilters.text(),
                    self.eInitialFilter.text(),
                    options,
                    self.schemesEdit.text().split())
            except TypeError:
                # PyQt5 < 5.13.0 contains an error
                QFileDialog.getSaveFileUrl(
                    None,
                    self.eCaption.text(),
                    self.eStartWith.text(),
                    self.eFilters.text(),
                    self.eInitialFilter.text(),
                    options,
                    self.schemesEdit.text().split())
        elif self.rDirectory.isChecked():
            options = QFileDialog.Options()
            if not self.cSymlinks.isChecked():
                options |= QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            if self.cDirOnly.isChecked():
                options |= QFileDialog.Options(QFileDialog.Option.ShowDirsOnly)
            else:
                options |= QFileDialog.Options(QFileDialog.Option(0))
            options = self.__adjustOptions(options)
            QFileDialog.getExistingDirectory(
                None,
                self.eCaption.text(),
                self.eWorkDir.text(),
                options)
        elif self.rDirectoryUrl.isChecked():
            options = QFileDialog.Options()
            if not self.cSymlinks.isChecked():
                options |= QFileDialog.Options(
                    QFileDialog.Option.DontResolveSymlinks)
            if self.cDirOnly.isChecked():
                options |= QFileDialog.Options(QFileDialog.Option.ShowDirsOnly)
            else:
                options |= QFileDialog.Options(QFileDialog.Option(0))
            options = self.__adjustOptions(options)
            try:
                QFileDialog.getExistingDirectoryUrl(
                    None,
                    self.eCaption.text(),
                    QUrl(self.eWorkDir.text()),
                    options,
                    self.schemesEdit.text().split())
            except TypeError:
                # PyQt5 < 5.13.0 contains an error
                QFileDialog.getExistingDirectoryUrl(
                    None,
                    self.eCaption.text(),
                    self.eWorkDir.text(),
                    options,
                    self.schemesEdit.text().split())
    
    def __toggleConfirmCheckBox(self):
        """
        Private slot to enable/disable the confirmation check box.
        """
        self.cConfirmOverwrite.setEnabled(
            self.rSaveFile.isChecked() or self.rfSaveFile.isChecked() or
            self.rSaveFileUrl.isChecked())
    
    def __toggleGroupsAndTest(self):
        """
        Private slot to enable/disable certain groups and the test button.
        """
        if self.rDirectory.isChecked() or self.rDirectoryUrl.isChecked():
            self.filePropertiesGroup.setEnabled(False)
            self.dirPropertiesGroup.setEnabled(True)
            self.bTest.setDisabled(self.cWorkDir.isChecked())
        else:
            self.filePropertiesGroup.setEnabled(True)
            self.dirPropertiesGroup.setEnabled(False)
            self.bTest.setDisabled(
                self.cStartWith.isChecked() or self.cFilters.isChecked())
    
    def __toggleInitialFilterAndResult(self, checkedId):
        """
        Private slot to enable/disable the initial filter elements and the
        results entries.
        
        @param checkedId id of the clicked button (integer)
        """
        enable = (
            (self.__dialogVariant in (-1, ) and checkedId in [11, 12, 13]) or
            (self.__dialogVariant in (5, 6) and
             checkedId in [1, 2, 3, 21, 22, 23])
        )
        
        self.lInitialFilter.setEnabled(enable)
        self.eInitialFilter.setEnabled(enable)
        self.cInitialFilter.setEnabled(enable)
        
        self.lFilterVariable.setEnabled(enable)
        self.eFilterVariable.setEnabled(enable)
        
        self.urlPropertiesGroup.setEnabled(checkedId in (21, 22, 23, 31))
    
    def getCode(self, indLevel, indString):
        """
        Public method to get the source code for Qt5.
        
        @param indLevel indentation level (int)
        @param indString string used for indentation (space or tab) (string)
        @return generated code (string)
        """
        # calculate our indentation level and the indentation string
        il = indLevel + 1
        istring = il * indString
        estring = os.linesep + indLevel * indString
        
        # now generate the code
        if self.parentSelf.isChecked():
            parent = "self"
        elif self.parentNone.isChecked():
            parent = "None"
        elif self.parentOther.isChecked():
            parent = self.parentEdit.text()
            if parent == "":
                parent = "None"
        
        # prepare the result variables
        nameVariable = self.eNameVariable.text()
        if not nameVariable:
            if self.__typeButtonsGroup.checkedButton() in [
                    self.rOpenFile, self.rfOpenFile,
                    self.rSaveFile, self.rfSaveFile]:
                nameVariable = "fileName"
            elif self.__typeButtonsGroup.checkedButton() in [
                    self.rOpenFiles, self.rfOpenFiles]:
                nameVariable = "fileNames"
            elif self.__typeButtonsGroup.checkedButton() == self.rDirectory:
                nameVariable = "dirName"
            else:
                nameVariable = "res"
        filterVariable = self.eFilterVariable.text()
        if not filterVariable:
            if (
                (self.__dialogVariant in (-1, ) and
                 self.__typeButtonsGroup.checkedButton() in [
                    self.rfOpenFile, self.rfOpenFiles, self.rfSaveFile]) or
                (self.__dialogVariant in (5, 6) and
                 self.__typeButtonsGroup.checkedButton() in [
                    self.rOpenFile, self.rOpenFiles, self.rSaveFile])
            ):
                filterVariable = ", selectedFilter"
            else:
                filterVariable = ""
        else:
            filterVariable = ", " + filterVariable
        
        if self.__dialogVariant == -1:
            dialogType = "E5FileDialog"
            optionStr = ""
        else:
            dialogType = "QFileDialog"
            optionStr = ".Option"
        
        code = '{0}{1} = {2}.'.format(nameVariable, filterVariable, dialogType)
        if (
            self.rOpenFile.isChecked() or
            self.rfOpenFile.isChecked() or
            self.rOpenFileUrl.isChecked()
        ):
            if self.rOpenFile.isChecked():
                code += 'getOpenFileName({0}{1}'.format(os.linesep, istring)
            elif self.rOpenFileUrl.isChecked():
                code += 'getOpenFileUrl({0}{1}'.format(os.linesep, istring)
            else:
                code += 'getOpenFileNameAndFilter({0}{1}'.format(
                    os.linesep, istring)
            code += '{0},{1}{2}'.format(parent, os.linesep, istring)
            if not self.eCaption.text():
                code += '"",{0}{1}'.format(os.linesep, istring)
            else:
                code += 'self.tr("{0}"),{1}{2}'.format(
                    self.eCaption.text(), os.linesep, istring)
            if self.rOpenFileUrl.isChecked():
                if not self.eStartWith.text():
                    code += 'QUrl(),{0}{1}'.format(os.linesep, istring)
                else:
                    if self.cStartWith.isChecked():
                        fmt = '{0},{1}{2}'
                    else:
                        fmt = 'QUrl("{0}"),{1}{2}'
                    code += fmt.format(self.eStartWith.text(), os.linesep,
                                       istring)
            else:
                if not self.eStartWith.text():
                    code += '"",{0}{1}'.format(os.linesep, istring)
                else:
                    if self.cStartWith.isChecked():
                        fmt = '{0},{1}{2}'
                    else:
                        fmt = '"{0}",{1}{2}'
                    code += fmt.format(self.eStartWith.text(), os.linesep,
                                       istring)
            if self.eFilters.text() == "":
                code += '""'
            else:
                if self.cFilters.isChecked():
                    fmt = '{0}'
                else:
                    fmt = 'self.tr("{0}")'
                code += fmt.format(self.eFilters.text())
            if self.rfOpenFile.isChecked() or self.__dialogVariant in (5, 6):
                if self.eInitialFilter.text() == "":
                    initialFilter = "None"
                else:
                    if self.cInitialFilter.isChecked():
                        fmt = '{0}'
                    else:
                        fmt = 'self.tr("{0}")'
                    initialFilter = fmt.format(self.eInitialFilter.text())
                code += ',{0}{1}{2}'.format(os.linesep, istring, initialFilter)
            if not self.cSymlinks.isChecked():
                code += (
                    ',{0}{1}{2}.Options({2}{3}.DontResolveSymlinks)'
                    .format(os.linesep, istring, dialogType, optionStr)
                )
            if self.rOpenFileUrl.isChecked() and bool(self.schemesEdit.text()):
                code += ',{0}{1}{2}'.format(
                    os.linesep, istring, self.__prepareSchemesList())
            code += '){0}'.format(estring)
        elif (
            self.rOpenFiles.isChecked() or
            self.rfOpenFiles.isChecked() or
            self.rOpenFileUrls.isChecked()
        ):
            if self.rOpenFiles.isChecked():
                code += 'getOpenFileNames({0}{1}'.format(os.linesep, istring)
            elif self.rOpenFileUrls.isChecked():
                code += 'getOpenFileUrls({0}{1}'.format(os.linesep, istring)
            else:
                code += 'getOpenFileNamesAndFilter({0}{1}'.format(
                    os.linesep, istring)
            code += '{0},{1}{2}'.format(parent, os.linesep, istring)
            if not self.eCaption.text():
                code += '"",{0}{1}'.format(os.linesep, istring)
            else:
                code += 'self.tr("{0}"),{1}{2}'.format(
                    self.eCaption.text(), os.linesep, istring)
            if self.rOpenFileUrls.isChecked():
                if not self.eStartWith.text():
                    code += 'QUrl(),{0}{1}'.format(os.linesep, istring)
                else:
                    if self.cStartWith.isChecked():
                        fmt = '{0},{1}{2}'
                    else:
                        fmt = 'QUrl("{0}"),{1}{2}'
                    code += fmt.format(self.eStartWith.text(), os.linesep,
                                       istring)
            else:
                if not self.eStartWith.text():
                    code += '"",{0}{1}'.format(os.linesep, istring)
                else:
                    if self.cStartWith.isChecked():
                        fmt = '{0},{1}{2}'
                    else:
                        fmt = '"{0}",{1}{2}'
                    code += fmt.format(self.eStartWith.text(), os.linesep,
                                       istring)
            if not self.eFilters.text():
                code += '""'
            else:
                if self.cFilters.isChecked():
                    fmt = '{0}'
                else:
                    fmt = 'self.tr("{0}")'
                code += fmt.format(self.eFilters.text())
            if self.rfOpenFiles.isChecked() or self.__dialogVariant in (5, 6):
                if self.eInitialFilter.text() == "":
                    initialFilter = "None"
                else:
                    if self.cInitialFilter.isChecked():
                        fmt = '{0}'
                    else:
                        fmt = 'self.tr("{0}")'
                    initialFilter = fmt.format(self.eInitialFilter.text())
                code += ',{0}{1}{2}'.format(os.linesep, istring, initialFilter)
            if not self.cSymlinks.isChecked():
                code += (
                    ',{0}{1}{2}.Options({2}{3}.DontResolveSymlinks)'
                    .format(os.linesep, istring, dialogType, optionStr)
                )
            if (
                self.rOpenFileUrls.isChecked() and
                bool(self.schemesEdit.text())
            ):
                code += ',{0}{1}{2}'.format(
                    os.linesep, istring, self.__prepareSchemesList())
            code += '){0}'.format(estring)
        elif (
            self.rSaveFile.isChecked() or
            self.rfSaveFile.isChecked() or
            self.rSaveFileUrl.isChecked()
        ):
            if self.rSaveFile.isChecked():
                code += 'getSaveFileName({0}{1}'.format(os.linesep, istring)
            elif self.rSaveFileUrl.isChecked():
                code += 'getSaveFileUrl({0}{1}'.format(os.linesep, istring)
            else:
                code += 'getSaveFileNameAndFilter({0}{1}'.format(
                    os.linesep, istring)
            code += '{0},{1}{2}'.format(parent, os.linesep, istring)
            if not self.eCaption.text():
                code += '"",{0}{1}'.format(os.linesep, istring)
            else:
                code += 'self.tr("{0}"),{1}{2}'.format(
                    self.eCaption.text(), os.linesep, istring)
            if self.rSaveFileUrl.isChecked():
                if not self.eStartWith.text():
                    code += 'QUrl(),{0}{1}'.format(os.linesep, istring)
                else:
                    if self.cStartWith.isChecked():
                        fmt = '{0},{1}{2}'
                    else:
                        fmt = 'QUrl("{0}"),{1}{2}'
                    code += fmt.format(self.eStartWith.text(), os.linesep,
                                       istring)
            else:
                if not self.eStartWith.text():
                    code += '"",{0}{1}'.format(os.linesep, istring)
                else:
                    if self.cStartWith.isChecked():
                        fmt = '{0},{1}{2}'
                    else:
                        fmt = '"{0}",{1}{2}'
                    code += fmt.format(self.eStartWith.text(), os.linesep,
                                       istring)
            if not self.eFilters.text():
                code += '""'
            else:
                if self.cFilters.isChecked():
                    fmt = '{0}'
                else:
                    fmt = 'self.tr("{0}")'
                code += fmt.format(self.eFilters.text())
            if self.rfSaveFile.isChecked() or self.__dialogVariant in (5, 6):
                if self.eInitialFilter.text() == "":
                    initialFilter = "None"
                else:
                    if self.cInitialFilter.isChecked():
                        fmt = '{0}'
                    else:
                        fmt = 'self.tr("{0}")'
                    initialFilter = fmt.format(self.eInitialFilter.text())
                code += ',{0}{1}{2}'.format(os.linesep, istring, initialFilter)
            if (
                (not self.cSymlinks.isChecked()) or
                (not self.cConfirmOverwrite.isChecked())
            ):
                code += ',{0}{1}{2}.Options('.format(
                    os.linesep, istring, dialogType)
                if not self.cSymlinks.isChecked():
                    code += '{0}{1}.DontResolveSymlinks'.format(
                        dialogType, optionStr)
                if (
                    (not self.cSymlinks.isChecked()) and
                    (not self.cConfirmOverwrite.isChecked())
                ):
                    code += ' | '
                if not self.cConfirmOverwrite.isChecked():
                    code += '{0}{1}.DontConfirmOverwrite'.format(
                        dialogType, optionStr)
                code += ')'
            if (
                self.rSaveFileUrl.isChecked() and
                bool(self.schemesEdit.text())
            ):
                code += ',{0}{1}{2}'.format(
                    os.linesep, istring, self.__prepareSchemesList())
                            
            code += '){0}'.format(estring)
        elif self.rDirectory.isChecked() or self.rDirectoryUrl.isChecked():
            if self.rDirectory.isChecked():
                code += 'getExistingDirectory({0}{1}'.format(
                    os.linesep, istring)
            else:
                code += 'getExistingDirectoryUrl({0}{1}'.format(
                    os.linesep, istring)
            code += '{0},{1}{2}'.format(parent, os.linesep, istring)
            if not self.eCaption.text():
                code += '"",{0}{1}'.format(os.linesep, istring)
            else:
                code += 'self.tr("{0}"),{1}{2}'.format(
                    self.eCaption.text(), os.linesep, istring)
            if self.rDirectoryUrl.isChecked():
                if not self.eWorkDir.text():
                    code += 'QUrl()'
                else:
                    if self.cWorkDir.isChecked():
                        fmt = '{0}'
                    else:
                        fmt = 'QUrl("{0}")'
                    code += fmt.format(self.eWorkDir.text())
            else:
                if not self.eWorkDir.text():
                    code += '""'
                else:
                    if self.cWorkDir.isChecked():
                        fmt = '{0}'
                    else:
                        fmt = '"{0}"'
                    code += fmt.format(self.eWorkDir.text())
            code += ',{0}{1}{2}.Options('.format(os.linesep, istring,
                                                 dialogType)
            if not self.cSymlinks.isChecked():
                code += '{0}{1}.DontResolveSymlinks | '.format(
                    dialogType, optionStr)
            if self.cDirOnly.isChecked():
                code += '{0}{1}.ShowDirsOnly'.format(
                    dialogType, optionStr)
            else:
                code += '{0}.Option(0)'.format(dialogType)
            code += ')'
            if self.rDirectoryUrl.isChecked():
                code += ',{0}{1}{2}'.format(
                    os.linesep, istring, self.__prepareSchemesList())
            code += '){0}'.format(estring)
            
        return code
    
    def __prepareSchemesList(self):
        """
        Private method to prepare the list of supported schemes.
        
        @return string representation of the supported schemes
        @rtype str
        """
        return repr(self.schemesEdit.text().strip().split())
