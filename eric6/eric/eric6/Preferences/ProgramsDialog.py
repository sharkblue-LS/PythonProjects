# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Programs page.
"""

import os
import re
import sys

from PyQt5.QtCore import pyqtSlot, Qt, QProcess
from PyQt5.QtWidgets import (
    QApplication, QTreeWidgetItem, QHeaderView, QDialog, QDialogButtonBox
)

from E5Gui.E5Application import e5App
from E5Gui.E5OverrideCursor import E5OverrideCursor

from .Ui_ProgramsDialog import Ui_ProgramsDialog

import Preferences
import Utilities


class ProgramsDialog(QDialog, Ui_ProgramsDialog):
    """
    Class implementing the Programs page.
    """
    ToolAvailableRole = Qt.ItemDataRole.UserRole + 1
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        """
        super(ProgramsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName("ProgramsDialog")
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.__hasSearched = False
        
        self.programsList.headerItem().setText(
            self.programsList.columnCount(), "")
        
        self.searchButton = self.buttonBox.addButton(
            self.tr("Search"), QDialogButtonBox.ButtonRole.ActionRole)
        self.searchButton.setToolTip(
            self.tr("Press to search for programs"))
        
        self.showComboBox.addItems([
            self.tr("All Supported Tools"),
            self.tr("Available Tools Only"),
            self.tr("Unavailable Tools Only"),
        ])
        
    def show(self):
        """
        Public slot to show the dialog.
        """
        QDialog.show(self)
        if not self.__hasSearched:
            self.on_programsSearchButton_clicked()
        
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.searchButton:
            self.on_programsSearchButton_clicked()
        
    @pyqtSlot()
    def on_programsSearchButton_clicked(self):
        """
        Private slot to search for all supported/required programs.
        """
        self.programsList.clear()
        header = self.programsList.header()
        header.setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        header.setSortIndicatorShown(False)
        
        with E5OverrideCursor():
            # 1. do the Qt programs
            # 1a. Translation Converter
            exe = (
                Utilities.isWindowsPlatform() and
                "{0}.exe".format(Utilities.generateQtToolName("lrelease")) or
                Utilities.generateQtToolName("lrelease")
            )
            exe = os.path.join(Utilities.getQtBinariesPath(), exe)
            version = self.__createProgramEntry(
                self.tr("Translation Converter (Qt)"), exe, '-version',
                'lrelease', -1)
            # 1b. Qt Designer
            if Utilities.isWindowsPlatform():
                exe = os.path.join(
                    Utilities.getQtBinariesPath(),
                    "{0}.exe".format(Utilities.generateQtToolName("designer")))
            elif Utilities.isMacPlatform():
                exe = Utilities.getQtMacBundle("designer")
            else:
                exe = os.path.join(
                    Utilities.getQtBinariesPath(),
                    Utilities.generateQtToolName("designer"))
            self.__createProgramEntry(
                self.tr("Qt Designer"), exe, version=version)
            # 1c. Qt Linguist
            if Utilities.isWindowsPlatform():
                exe = os.path.join(
                    Utilities.getQtBinariesPath(),
                    "{0}.exe".format(Utilities.generateQtToolName("linguist")))
            elif Utilities.isMacPlatform():
                exe = Utilities.getQtMacBundle("linguist")
            else:
                exe = os.path.join(
                    Utilities.getQtBinariesPath(),
                    Utilities.generateQtToolName("linguist"))
            self.__createProgramEntry(
                self.tr("Qt Linguist"), exe, version=version)
            # 1d. Qt Assistant
            if Utilities.isWindowsPlatform():
                exe = os.path.join(
                    Utilities.getQtBinariesPath(),
                    "{0}.exe".format(
                        Utilities.generateQtToolName("assistant")))
            elif Utilities.isMacPlatform():
                exe = Utilities.getQtMacBundle("assistant")
            else:
                exe = os.path.join(
                    Utilities.getQtBinariesPath(),
                    Utilities.generateQtToolName("assistant"))
            self.__createProgramEntry(
                self.tr("Qt Assistant"), exe, version=version)
            
            # 2. do the PyQt programs
            # 2.1 do the PyQt5 programs
            # 2.1a. Translation Extractor PyQt5
            self.__createProgramEntry(
                self.tr("Translation Extractor (Python, PyQt5)"),
                Utilities.generatePyQtToolPath("pylupdate5"),
                '-version', 'pylupdate', -1)
            # 2.1b. Forms Compiler PyQt5
            self.__createProgramEntry(
                self.tr("Forms Compiler (Python, PyQt5)"),
                Utilities.generatePyQtToolPath("pyuic5", ["py3uic5"]),
                '--version', 'Python User', 4)
            # 2.1c. Resource Compiler PyQt5
            self.__createProgramEntry(
                self.tr("Resource Compiler (Python, PyQt5)"),
                Utilities.generatePyQtToolPath("pyrcc5"),
                '-version', '', -1, versionRe='Resource Compiler|pyrcc5')
            
            # 2.2 do the PyQt6 programs
            # 2.2a. Translation Extractor PyQt6
            self.__createProgramEntry(
                self.tr("Translation Extractor (Python, PyQt6)"),
                Utilities.generatePyQtToolPath("pylupdate6"),
                '--version', versionPosition=0)
            # 2.2b. Forms Compiler PyQt6
            self.__createProgramEntry(
                self.tr("Forms Compiler (Python, PyQt6)"),
                Utilities.generatePyQtToolPath("pyuic6"),
                '--version', versionPosition=0)
            
            # 3. do the PySide programs
            # 3.1 do the PySide2 programs
            # 3.1a. Translation Extractor PySide2
            self.__createProgramEntry(
                self.tr("Translation Extractor (Python, PySide2)"),
                Utilities.generatePySideToolPath("pyside2-lupdate", variant=2),
                '-version', '', -1, versionRe='lupdate')
            # 3.1b. Forms Compiler PySide2
            self.__createProgramEntry(
                self.tr("Forms Compiler (Python, PySide2)"),
                Utilities.generatePySideToolPath("pyside2-uic", variant=2),
                '--version', '', -1, versionRe='uic')
            # 3.1c Resource Compiler PySide2
            self.__createProgramEntry(
                self.tr("Resource Compiler (Python, PySide2)"),
                Utilities.generatePySideToolPath("pyside2-rcc", variant=2),
                '-version', '', -1, versionRe='rcc')
            # 3.2 do the PySide5 programs
            # 3.2a. Translation Extractor PySide6
            self.__createProgramEntry(
                self.tr("Translation Extractor (Python, PySide6)"),
                Utilities.generatePySideToolPath("pyside6-lupdate", variant=6),
                '-version', '', -1, versionRe='lupdate')
            # 3.2b. Forms Compiler PySide6
            self.__createProgramEntry(
                self.tr("Forms Compiler (Python, PySide6)"),
                Utilities.generatePySideToolPath("pyside6-uic", variant=6),
                '--version', '', -1, versionRe='uic')
            # 3.2c Resource Compiler PySide6
            self.__createProgramEntry(
                self.tr("Resource Compiler (Python, PySide6)"),
                Utilities.generatePySideToolPath("pyside6-rcc", variant=6),
                '--version', '', -1, versionRe='rcc')
            
            # 4. do the Conda program(s)
            exe = Preferences.getConda("CondaExecutable")
            if not exe:
                exe = "conda"
                if Utilities.isWindowsPlatform():
                    exe += ".exe"
            self.__createProgramEntry(
                self.tr("conda Manager"), exe, '--version', 'conda', -1)
            
            # 5. do the pip program(s)
            virtualenvManager = e5App().getObject("VirtualEnvManager")
            for venvName in virtualenvManager.getVirtualenvNames():
                interpreter = virtualenvManager.getVirtualenvInterpreter(
                    venvName)
                self.__createProgramEntry(
                    self.tr("PyPI Package Management"), interpreter,
                    '--version', 'pip', 1, exeModule=["-m", "pip"])
            
            # 6. do the CORBA and Protobuf programs
            # 6a. omniORB
            exe = Preferences.getCorba("omniidl")
            if not exe:
                exe = "omniidl"
                if Utilities.isWindowsPlatform():
                    exe += ".exe"
            self.__createProgramEntry(
                self.tr("CORBA IDL Compiler"), exe, '-V', 'omniidl', -1)
            # 6b. protobuf
            exe = Preferences.getProtobuf("protoc")
            if not exe:
                exe = "protoc"
                if Utilities.isWindowsPlatform():
                    exe += ".exe"
            self.__createProgramEntry(
                self.tr("Protobuf Compiler"), exe, '--version', 'libprotoc',
                -1)
            # 6c. grpc
            exe = Preferences.getProtobuf("grpcPython")
            if not exe:
                exe = sys.executable
            self.__createProgramEntry(
                self.tr("gRPC Compiler"), exe, '--version', 'libprotoc', -1,
                exeModule=['-m', 'grpc_tools.protoc'])
            
            # 7. do the spell checking entry
            try:
                import enchant
                try:
                    text = os.path.dirname(enchant.__file__)
                except AttributeError:
                    text = "enchant"
                try:
                    version = enchant.__version__
                except AttributeError:
                    version = self.tr("(unknown)")
            except (ImportError, AttributeError, OSError):
                text = "enchant"
                version = ""
            self.__createEntry(
                self.tr("Spell Checker - PyEnchant"), text, version)
            
            # 8. do the pygments entry
            try:
                import pygments
                try:
                    text = os.path.dirname(pygments.__file__)
                except AttributeError:
                    text = "pygments"
                try:
                    version = pygments.__version__
                except AttributeError:
                    version = self.tr("(unknown)")
            except (ImportError, AttributeError, OSError):
                text = "pygments"
                version = ""
            self.__createEntry(
                self.tr("Source Highlighter - Pygments"), text, version)
            
            # 9. do the MicroPython related entries
            exe = Preferences.getMicroPython("MpyCrossCompiler")
            if not exe:
                exe = "mpy-cross"
            self.__createProgramEntry(
                self.tr("MicroPython - MPY Cross Compiler"), exe, '--version',
                'MicroPython', 1)
            self.__createProgramEntry(
                self.tr("MicroPython - ESP Tool"), sys.executable, 'version',
                'esptool', -1, exeModule=['-m', 'esptool'])
            exe = Preferences.getMicroPython("DfuUtilPath")
            if not exe:
                exe = "dfu-util"
            self.__createProgramEntry(
                self.tr("MicroPython - PyBoard Flasher"), exe, '--version',
                'dfu-util', -1)
            
            # 10. do the plugin related programs
            pm = e5App().getObject("PluginManager")
            for info in pm.getPluginExeDisplayData():
                if info["programEntry"]:
                    if "exeModule" not in info:
                        info["exeModule"] = None
                    if "versionRe" not in info:
                        info["versionRe"] = None
                    self.__createProgramEntry(
                        info["header"],
                        info["exe"],
                        versionCommand=info["versionCommand"],
                        versionStartsWith=info["versionStartsWith"],
                        versionPosition=info["versionPosition"],
                        version=info["version"],
                        versionCleanup=info["versionCleanup"],
                        versionRe=info["versionRe"],
                        exeModule=info["exeModule"],
                    )
                else:
                    self.__createEntry(
                        info["header"],
                        info["text"],
                        info["version"]
                    )
            
            self.programsList.sortByColumn(0, Qt.SortOrder.AscendingOrder)
            self.on_showComboBox_currentIndexChanged(
                self.showComboBox.currentIndex())
        
        self.__hasSearched = True

    def __createProgramEntry(self, description, exe,
                             versionCommand="", versionStartsWith="",
                             versionPosition=None, version="",
                             versionCleanup=None, versionRe=None,
                             exeModule=None):
        """
        Private method to generate a program entry.
        
        @param description descriptive text (string)
        @param exe name of the executable program (string)
        @param versionCommand command line switch to get the version info
            (str). If this is empty, the given version will be shown.
        @param versionStartsWith start of line identifying version info
            (string)
        @param versionPosition index of part containing the version info
            (integer)
        @param version version string to show (string)
        @param versionCleanup tuple of two integers giving string positions
            start and stop for the version string (tuple of integers)
        @param versionRe regexp to determine the line identifying version
            info (string). Takes precedence over versionStartsWith.
        @param exeModule list of command line parameters to execute a module
            with the program given in exe (e.g. to execute a Python module)
            (list of str)
        @return version string of detected or given version (string)
        """
        itmList = self.programsList.findItems(
            description, Qt.MatchFlag.MatchCaseSensitive)
        if itmList:
            itm = itmList[0]
        else:
            itm = QTreeWidgetItem(self.programsList, [description])
        font = itm.font(0)
        font.setBold(True)
        itm.setFont(0, font)
        rememberedExe = exe
        if not exe:
            itm.setText(1, self.tr("(not configured)"))
        else:
            if os.path.isabs(exe):
                if not Utilities.isExecutable(exe):
                    exe = ""
            else:
                exe = Utilities.getExecutablePath(exe)
            if exe:
                available = True
                if versionCommand and versionPosition is not None:
                    proc = QProcess()
                    proc.setProcessChannelMode(
                        QProcess.ProcessChannelMode.MergedChannels)
                    if exeModule:
                        args = exeModule[:] + [versionCommand]
                    else:
                        args = [versionCommand]
                    proc.start(exe, args)
                    finished = proc.waitForFinished(10000)
                    if finished:
                        output = str(proc.readAllStandardOutput(),
                                     Preferences.getSystem("IOEncoding"),
                                     'replace')
                        if (
                            exeModule and
                            exeModule[0] == "-m" and
                            ("ImportError:" in output or
                             "ModuleNotFoundError:" in output or
                             proc.exitCode() != 0)
                        ):
                            version = self.tr("(module not found)")
                            available = False
                        elif not versionStartsWith and not versionRe:
                            # assume output is just one line
                            try:
                                version = (
                                    output.strip().split()[versionPosition]
                                )
                                if versionCleanup:
                                    version = version[
                                        versionCleanup[0]:
                                        versionCleanup[1]
                                    ]
                            except IndexError:
                                version = self.tr("(unknown)")
                                available = False
                        else:
                            if versionRe is None:
                                versionRe = "^{0}".format(
                                    re.escape(versionStartsWith))
                            versionRe = re.compile(versionRe, re.UNICODE)
                            for line in output.splitlines():
                                if versionRe.search(line):
                                    try:
                                        version = line.split()[versionPosition]
                                        if versionCleanup:
                                            version = version[
                                                versionCleanup[0]:
                                                versionCleanup[1]
                                            ]
                                        break
                                    except IndexError:
                                        version = self.tr("(unknown)")
                                        available = False
                            else:
                                version = self.tr("(unknown)")
                                available = False
                    else:
                        version = self.tr("(not executable)")
                        available = False
                if exeModule:
                    citm = QTreeWidgetItem(itm, [
                        "{0} {1}".format(exe, " ".join(exeModule)),
                        version])
                else:
                    citm = QTreeWidgetItem(itm, [exe, version])
                citm.setData(0, self.ToolAvailableRole, available)
                itm.setExpanded(True)
            else:
                if itm.childCount() == 0:
                    itm.setText(1, self.tr("(not found)"))
                else:
                    citm = QTreeWidgetItem(
                        itm, [rememberedExe, self.tr("(not found)")])
                    citm.setData(0, self.ToolAvailableRole, False)
                    itm.setExpanded(True)
        QApplication.processEvents()
        self.programsList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.programsList.header().setStretchLastSection(True)
        return version
        
    def __createEntry(self, description, entryText, entryVersion):
        """
        Private method to generate a program entry.
        
        @param description descriptive text (string)
        @param entryText text to show (string)
        @param entryVersion version string to show (string).
        """
        itm = QTreeWidgetItem(self.programsList, [description])
        font = itm.font(0)
        font.setBold(True)
        itm.setFont(0, font)
        
        if len(entryVersion):
            citm = QTreeWidgetItem(itm, [entryText, entryVersion])
            itm.setExpanded(True)
            citm.setData(0, self.ToolAvailableRole,
                         not entryVersion.startswith("("))
            # assume version starting with '(' is an unavailability
        else:
            itm.setText(1, self.tr("(not found)"))
        QApplication.processEvents()
        self.programsList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.programsList.header().setStretchLastSection(True)
    
    @pyqtSlot(int)
    def on_showComboBox_currentIndexChanged(self, index):
        """
        Private slot to apply the selected show criteria.
        
        @param index index of the show criterium
        @type int
        """
        if index == 0:
            # All Supported Tools
            for topIndex in range(self.programsList.topLevelItemCount()):
                topItem = self.programsList.topLevelItem(topIndex)
                for childIndex in range(topItem.childCount()):
                    topItem.child(childIndex).setHidden(False)
                topItem.setHidden(False)
        else:
            # 1 = Available Tools Only
            # 2 = Unavailable Tools Only
            for topIndex in range(self.programsList.topLevelItemCount()):
                topItem = self.programsList.topLevelItem(topIndex)
                if topItem.childCount() == 0:
                    topItem.setHidden(index == 1)
                else:
                    availabilityList = []
                    for childIndex in range(topItem.childCount()):
                        childItem = topItem.child(childIndex)
                        available = childItem.data(0, self.ToolAvailableRole)
                        if index == 1:
                            childItem.setHidden(not available)
                        else:
                            childItem.setHidden(available)
                        availabilityList.append(available)
                    if index == 1:
                        topItem.setHidden(not any(availabilityList))
                    else:
                        topItem.setHidden(all(availabilityList))
