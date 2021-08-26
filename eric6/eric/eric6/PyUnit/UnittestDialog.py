# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the UI to the pyunit package.
"""

import unittest
import sys
import time
import re
import os

from PyQt5.QtCore import pyqtSignal, QEvent, Qt, pyqtSlot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QDialog, QApplication, QDialogButtonBox, QListWidgetItem,
    QComboBox, QTreeWidgetItem
)

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox
from E5Gui.E5MainWindow import E5MainWindow
from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_UnittestDialog import Ui_UnittestDialog

import UI.PixmapCache

import Preferences


class UnittestDialog(QWidget, Ui_UnittestDialog):
    """
    Class implementing the UI to the pyunit package.
    
    @signal unittestFile(str, int, bool) emitted to show the source of a
        unittest file
    @signal unittestStopped() emitted after a unit test was run
    """
    unittestFile = pyqtSignal(str, int, bool)
    unittestStopped = pyqtSignal()
    
    TestCaseNameRole = Qt.ItemDataRole.UserRole
    TestCaseFileRole = Qt.ItemDataRole.UserRole + 1
    
    ErrorsInfoRole = Qt.ItemDataRole.UserRole
    
    SkippedColorDarkTheme = QColor("#00aaff")
    FailedExpectedColorDarkTheme = QColor("#ccaaff")
    SucceededUnexpectedColorDarkTheme = QColor("#ff99dd")
    SkippedColorLightTheme = QColor("#0000ff")
    FailedExpectedColorLightTheme = QColor("#7700bb")
    SucceededUnexpectedColorLightTheme = QColor("#ff0000")
    
    def __init__(self, prog=None, dbs=None, ui=None, parent=None, name=None):
        """
        Constructor
        
        @param prog filename of the program to open
        @type str
        @param dbs reference to the debug server object. It is an indication
            whether we were called from within the eric IDE.
        @type DebugServer
        @param ui reference to the UI object
        @type UserInterface
        @param parent parent widget of this dialog
        @type QWidget
        @param name name of this dialog
        @type str
        """
        super(UnittestDialog, self).__init__(parent)
        if name:
            self.setObjectName(name)
        self.setupUi(self)
        
        self.testsuitePicker.setMode(E5PathPickerModes.OpenFileMode)
        self.testsuitePicker.setInsertPolicy(
            QComboBox.InsertPolicy.InsertAtTop)
        self.testsuitePicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        
        self.discoveryPicker.setMode(E5PathPickerModes.DirectoryMode)
        self.discoveryPicker.setInsertPolicy(
            QComboBox.InsertPolicy.InsertAtTop)
        self.discoveryPicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        
        self.discoverButton = self.buttonBox.addButton(
            self.tr("Discover"), QDialogButtonBox.ButtonRole.ActionRole)
        self.discoverButton.setToolTip(self.tr(
            "Discover tests"))
        self.discoverButton.setWhatsThis(self.tr(
            """<b>Discover</b>"""
            """<p>This button starts a discovery of available tests.</p>"""))
        self.startButton = self.buttonBox.addButton(
            self.tr("Start"), QDialogButtonBox.ButtonRole.ActionRole)
        self.startButton.setToolTip(self.tr(
            "Start the selected testsuite"))
        self.startButton.setWhatsThis(self.tr(
            """<b>Start Test</b>"""
            """<p>This button starts the selected testsuite.</p>"""))
        self.startFailedButton = self.buttonBox.addButton(
            self.tr("Rerun Failed"), QDialogButtonBox.ButtonRole.ActionRole)
        self.startFailedButton.setToolTip(
            self.tr("Reruns failed tests of the selected testsuite"))
        self.startFailedButton.setWhatsThis(self.tr(
            """<b>Rerun Failed</b>"""
            """<p>This button reruns all failed tests of the selected"""
            """ testsuite.</p>"""))
        self.stopButton = self.buttonBox.addButton(
            self.tr("Stop"), QDialogButtonBox.ButtonRole.ActionRole)
        self.stopButton.setToolTip(self.tr("Stop the running unittest"))
        self.stopButton.setWhatsThis(self.tr(
            """<b>Stop Test</b>"""
            """<p>This button stops a running unittest.</p>"""))
        self.discoverButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.startButton.setDefault(True)
        self.startFailedButton.setEnabled(False)
        
        self.__dbs = dbs
        self.__forProject = False
        
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowFlags(
                Qt.WindowType.WindowContextHelpButtonHint))
        self.setWindowIcon(UI.PixmapCache.getIcon("eric"))
        self.setWindowTitle(self.tr("Unittest"))
        if dbs:
            self.ui = ui
            
            self.debuggerCheckBox.setChecked(True)
            
            # virtual environment manager is only used in the integrated
            # variant
            self.__venvManager = e5App().getObject("VirtualEnvManager")
            self.__populateVenvComboBox()
            self.__venvManager.virtualEnvironmentAdded.connect(
                self.__populateVenvComboBox)
            self.__venvManager.virtualEnvironmentRemoved.connect(
                self.__populateVenvComboBox)
            self.__venvManager.virtualEnvironmentChanged.connect(
                self.__populateVenvComboBox)
        else:
            self.__venvManager = None
            self.debuggerCheckBox.setVisible(False)
        self.venvComboBox.setVisible(bool(self.__venvManager))
        self.venvLabel.setVisible(bool(self.__venvManager))
        
        self.__setProgressColor("green")
        self.progressLed.setDarkFactor(150)
        self.progressLed.off()
        
        self.discoverHistory = []
        self.fileHistory = []
        self.testNameHistory = []
        self.running = False
        self.savedModulelist = None
        self.savedSysPath = sys.path
        self.savedCwd = os.getcwd()
        if prog:
            self.insertProg(prog)
        
        self.rxPatterns = [
            self.tr("^Failure: "),
            self.tr("^Error: "),
            # These are for untranslated/partially translated situations
            "^Failure: ",
            "^Error: ",
        ]
        
        self.__failedTests = []
        
        # now connect the debug server signals if called from the eric IDE
        if self.__dbs:
            self.__dbs.utDiscovered.connect(self.__UTDiscovered)
            self.__dbs.utPrepared.connect(self.__UTPrepared)
            self.__dbs.utFinished.connect(self.__setStoppedMode)
            self.__dbs.utStartTest.connect(self.testStarted)
            self.__dbs.utStopTest.connect(self.testFinished)
            self.__dbs.utTestFailed.connect(self.testFailed)
            self.__dbs.utTestErrored.connect(self.testErrored)
            self.__dbs.utTestSkipped.connect(self.testSkipped)
            self.__dbs.utTestFailedExpected.connect(self.testFailedExpected)
            self.__dbs.utTestSucceededUnexpected.connect(
                self.testSucceededUnexpected)
        
        self.__editors = []
    
    def keyPressEvent(self, evt):
        """
        Protected slot to handle key press events.
        
        @param evt key press event to handle (QKeyEvent)
        """
        if evt.key() == Qt.Key.Key_Escape and self.__dbs:
            self.close()
    
    def __populateVenvComboBox(self):
        """
        Private method to (re-)populate the virtual environments selector.
        """
        currentText = self.venvComboBox.currentText()
        self.venvComboBox.clear()
        self.venvComboBox.addItem("")
        self.venvComboBox.addItems(
            sorted(self.__venvManager.getVirtualenvNames()))
        index = self.venvComboBox.findText(currentText)
        if index < 0:
            index = 0
        self.venvComboBox.setCurrentIndex(index)
    
    def __setProgressColor(self, color):
        """
        Private methode to set the color of the progress color label.
        
        @param color colour to be shown (string)
        """
        self.progressLed.setColor(QColor(color))
    
    def setProjectMode(self, forProject):
        """
        Public method to set the project mode of the dialog.
        
        @param forProject flag indicating to run for the open project
        @type bool
        """
        self.__forProject = forProject
        if forProject:
            project = e5App().getObject("Project")
            if project.isOpen():
                self.insertDiscovery(project.getProjectPath())
            else:
                self.insertDiscovery("")
        else:
            self.insertDiscovery("")
        
        self.discoveryList.clear()
        self.tabWidget.setCurrentIndex(0)
    
    def insertDiscovery(self, start):
        """
        Public slot to insert the discovery start directory into the
        discoveryPicker object.
        
        @param start start directory name to be inserted
        @type str
        """
        # prepend the given directory to the discovery picker
        if start is None:
            start = ""
        if start in self.discoverHistory:
            self.discoverHistory.remove(start)
        self.discoverHistory.insert(0, start)
        self.discoveryPicker.clear()
        self.discoveryPicker.addItems(self.discoverHistory)
    
    def insertProg(self, prog):
        """
        Public slot to insert the filename prog into the testsuitePicker
        object.
        
        @param prog filename to be inserted (string)
        """
        # prepend the selected file to the testsuite picker
        if prog is None:
            prog = ""
        if prog in self.fileHistory:
            self.fileHistory.remove(prog)
        self.fileHistory.insert(0, prog)
        self.testsuitePicker.clear()
        self.testsuitePicker.addItems(self.fileHistory)
    
    def insertTestName(self, testName):
        """
        Public slot to insert a test name into the testComboBox object.
        
        @param testName name of the test to be inserted (string)
        """
        # prepend the selected file to the testsuite combobox
        if testName is None:
            testName = ""
        if testName in self.testNameHistory:
            self.testNameHistory.remove(testName)
        self.testNameHistory.insert(0, testName)
        self.testComboBox.clear()
        self.testComboBox.addItems(self.testNameHistory)
    
    @pyqtSlot()
    def on_testsuitePicker_aboutToShowPathPickerDialog(self):
        """
        Private slot called before the test suite selection dialog is shown.
        """
        if self.__dbs:
            py3Extensions = ' '.join(
                ["*{0}".format(ext)
                 for ext in self.__dbs.getExtensions('Python3')]
            )
            fileFilter = self.tr(
                "Python3 Files ({0});;All Files (*)"
            ).format(py3Extensions)
        else:
            fileFilter = self.tr("Python Files (*.py);;All Files (*)")
        self.testsuitePicker.setFilters(fileFilter)
        
        defaultDirectory = Preferences.getMultiProject("Workspace")
        if not defaultDirectory:
            defaultDirectory = os.path.expanduser("~")
        if self.__dbs:
            project = e5App().getObject("Project")
            if self.__forProject and project.isOpen():
                defaultDirectory = project.getProjectPath()
        self.testsuitePicker.setDefaultDirectory(defaultDirectory)
    
    @pyqtSlot(str)
    def on_testsuitePicker_pathSelected(self, suite):
        """
        Private slot called after a test suite has been selected.
        
        @param suite file name of the test suite
        @type str
        """
        self.insertProg(suite)
    
    @pyqtSlot(str)
    def on_testsuitePicker_editTextChanged(self, path):
        """
        Private slot handling changes of the test suite path.
        
        @param path path of the test suite file
        @type str
        """
        self.startFailedButton.setEnabled(False)
    
    @pyqtSlot(bool)
    def on_discoverCheckBox_toggled(self, checked):
        """
        Private slot handling state changes of the 'discover' checkbox.
        
        @param checked state of the checkbox
        @type bool
        """
        self.discoverButton.setEnabled(checked)
        self.discoveryList.clear()
        
        if not bool(self.discoveryPicker.currentText()):
            if self.__forProject:
                project = e5App().getObject("Project")
                if project.isOpen():
                    self.insertDiscovery(project.getProjectPath())
                    return
            
            self.insertDiscovery(Preferences.getMultiProject("Workspace"))
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.discoverButton:
            self.__discover()
        elif button == self.startButton:
            self.startTests()
        elif button == self.stopButton:
            self.__stopTests()
        elif button == self.startFailedButton:
            self.startTests(failedOnly=True)
    
    @pyqtSlot()
    def __discover(self):
        """
        Private slot to discover unit test but don't run them.
        """
        if self.running:
            return
        
        self.discoveryList.clear()
        
        discoveryStart = self.discoveryPicker.currentText()
        self.sbLabel.setText(self.tr("Discovering Tests"))
        QApplication.processEvents()
        
        self.testName = self.tr("Unittest with auto-discovery")
        if self.__dbs:
            venvName = self.venvComboBox.currentText()
            
            # we are cooperating with the eric IDE
            project = e5App().getObject("Project")
            if self.__forProject:
                mainScript = project.getMainScript(True)
                clientType = project.getProjectLanguage()
                if mainScript:
                    workdir = os.path.dirname(os.path.abspath(mainScript))
                else:
                    workdir = project.getProjectPath()
                sysPath = [workdir]
                if not discoveryStart:
                    discoveryStart = workdir
            else:
                if not discoveryStart:
                    E5MessageBox.critical(
                        self,
                        self.tr("Unittest"),
                        self.tr("You must enter a start directory for"
                                " auto-discovery."))
                    return
                
                workdir = ""
                clientType = "Python3"
                sysPath = []
            self.__dbs.remoteUTDiscover(clientType, self.__forProject,
                                        venvName, sysPath, workdir,
                                        discoveryStart)
        else:
            # we are running as an application
            if not discoveryStart:
                E5MessageBox.critical(
                    self,
                    self.tr("Unittest"),
                    self.tr("You must enter a start directory for"
                            " auto-discovery."))
                return
            
            if discoveryStart:
                sys.path = (
                    [os.path.abspath(discoveryStart)] +
                    self.savedSysPath
                )
            
            # clean up list of imported modules to force a reimport upon
            # running the test
            if self.savedModulelist:
                for modname in list(sys.modules.keys()):
                    if modname not in self.savedModulelist:
                        # delete it
                        del(sys.modules[modname])
            self.savedModulelist = sys.modules.copy()
            
            # now try to discover the testsuite
            os.chdir(discoveryStart)
            try:
                testLoader = unittest.TestLoader()
                test = testLoader.discover(discoveryStart)
                if hasattr(testLoader, "errors") and bool(testLoader.errors):
                    E5MessageBox.critical(
                        self,
                        self.tr("Unittest"),
                        self.tr(
                            "<p>Unable to discover tests.</p>"
                            "<p>{0}</p>"
                        ).format("<br/>".join(testLoader.errors)
                                 .replace("\n", "<br/>"))
                    )
                    self.sbLabel.clear()
                else:
                    testsList = self.__assembleTestCasesList(
                        test, discoveryStart)
                    self.__populateDiscoveryResults(testsList)
                    self.sbLabel.setText(
                        self.tr("Discovered %n Test(s)", "",
                                len(testsList)))
                    self.tabWidget.setCurrentIndex(0)
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                E5MessageBox.critical(
                    self,
                    self.tr("Unittest"),
                    self.tr(
                        "<p>Unable to discover tests.</p>"
                        "<p>{0}<br/>{1}</p>")
                    .format(str(exc_type),
                            str(exc_value).replace("\n", "<br/>"))
                )
                self.sbLabel.clear()
            
            sys.path = self.savedSysPath
    
    def __assembleTestCasesList(self, suite, start):
        """
        Private method to assemble a list of test cases included in a test
        suite.
        
        @param suite test suite to be inspected
        @type unittest.TestSuite
        @param start name of directory discovery was started at
        @type str
        @return list of tuples containing the test case ID, a short description
            and the path of the test file name
        @rtype list of tuples of (str, str, str)
        """
        testCases = []
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                testCases.extend(self.__assembleTestCasesList(test, start))
            else:
                testId = test.id()
                if (
                    "ModuleImportFailure" not in testId and
                    "LoadTestsFailure" not in testId and
                    "_FailedTest" not in testId
                ):
                    filename = os.path.join(
                        start,
                        test.__module__.replace(".", os.sep) + ".py")
                    testCases.append(
                        (test.id(), test.shortDescription(), filename)
                    )
        return testCases
    
    def __findDiscoveryItem(self, modulePath):
        """
        Private method to find an item given the module path.
        
        @param modulePath path of the module in dotted notation
        @type str
        @return reference to the item or None
        @rtype QTreeWidgetItem or None
        """
        itm = self.discoveryList.topLevelItem(0)
        while itm is not None:
            if itm.data(0, UnittestDialog.TestCaseNameRole) == modulePath:
                return itm
            itm = self.discoveryList.itemBelow(itm)
        
        return None
    
    def __populateDiscoveryResults(self, tests):
        """
        Private method to populate the test discovery results list.
        
        @param tests list of tuples containing the discovery results
        @type list of tuples of (str, str, str)
        """
        for test, _testDescription, filename in tests:
            testPath = test.split(".")
            pitm = None
            for index in range(1, len(testPath) + 1):
                modulePath = ".".join(testPath[:index])
                itm = self.__findDiscoveryItem(modulePath)
                if itm is not None:
                    pitm = itm
                else:
                    if pitm is None:
                        itm = QTreeWidgetItem(self.discoveryList,
                                              [testPath[index - 1]])
                    else:
                        itm = QTreeWidgetItem(pitm,
                                              [testPath[index - 1]])
                        pitm.setExpanded(True)
                    itm.setFlags(Qt.ItemFlag.ItemIsUserCheckable |
                                 Qt.ItemFlag.ItemIsEnabled)
                    itm.setCheckState(0, Qt.CheckState.Unchecked)
                    itm.setData(0, UnittestDialog.TestCaseNameRole, modulePath)
                    if (
                        os.path.splitext(os.path.basename(filename))[0] ==
                        itm.text(0)
                    ):
                        itm.setData(0, UnittestDialog.TestCaseFileRole,
                                    filename)
                    elif pitm:
                        fn = pitm.data(0, UnittestDialog.TestCaseFileRole)
                        if fn:
                            itm.setData(0, UnittestDialog.TestCaseFileRole, fn)
                    pitm = itm
    
    def __selectedTestCases(self, parent=None):
        """
        Private method to assemble the list of selected test cases and suites.
        
        @param parent reference to the parent item
        @type QTreeWidgetItem
        @return list of selected test cases
        @rtype list of str
        """
        selectedTests = []
        if parent is None:
            # top level
            for index in range(self.discoveryList.topLevelItemCount()):
                itm = self.discoveryList.topLevelItem(index)
                if itm.checkState(0) == Qt.CheckState.Checked:
                    selectedTests.append(
                        itm.data(0, UnittestDialog.TestCaseNameRole))
                    # ignore children because they are included implicitly
                elif itm.childCount():
                    # recursively check children
                    selectedTests.extend(self.__selectedTestCases(itm))
        
        else:
            # parent item with children
            for index in range(parent.childCount()):
                itm = parent.child(index)
                if itm.checkState(0) == Qt.CheckState.Checked:
                    selectedTests.append(
                        itm.data(0, UnittestDialog.TestCaseNameRole))
                    # ignore children because they are included implicitly
                elif itm.childCount():
                    # recursively check children
                    selectedTests.extend(self.__selectedTestCases(itm))
        
        return selectedTests
    
    def __UTDiscovered(self, testCases, exc_type, exc_value):
        """
        Private slot to handle the utDiscovered signal.
        
        If the unittest suite was loaded successfully, we ask the
        client to run the test suite.
        
        @param testCases list of detected test cases
        @type str
        @param exc_type exception type occured during discovery
        @type str
        @param exc_value value of exception occured during discovery
        @type str
        """
        if testCases:
            self.__populateDiscoveryResults(testCases)
            self.sbLabel.setText(
                self.tr("Discovered %n Test(s)", "",
                        len(testCases)))
            self.tabWidget.setCurrentIndex(0)
        else:
            E5MessageBox.critical(
                self,
                self.tr("Unittest"),
                self.tr("<p>Unable to discover tests.</p>"
                        "<p>{0}<br/>{1}</p>")
                .format(exc_type, exc_value.replace("\n", "<br/>"))
            )
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_discoveryList_itemChanged(self, item, column):
        """
        Private slot handling the user checking or unchecking an item.

        @param item reference to the item
        @type QTreeWidgetItem
        @param column changed column
        @type int
        """
        if column == 0:
            for index in range(item.childCount()):
                item.child(index).setCheckState(0, item.checkState(0))

    @pyqtSlot(QTreeWidgetItem, int)
    def on_discoveryList_itemDoubleClicked(self, item, column):
        """
        Private slot handling the user double clicking an item.
        
        @param item reference to the item
        @type QTreeWidgetItem
        @param column column of the double click
        @type int
        """
        if item:
            filename = item.data(0, UnittestDialog.TestCaseFileRole)
            if filename:
                if self.__dbs:
                    # running as part of eric IDE
                    self.unittestFile.emit(filename, 1, False)
                else:
                    self.__openEditor(filename, 1)
    
    @pyqtSlot()
    def startTests(self, failedOnly=False):
        """
        Public slot to start the test.
        
        @param failedOnly flag indicating to run only failed tests (boolean)
        """
        if self.running:
            return
        
        discover = self.discoverCheckBox.isChecked()
        if discover:
            discoveryStart = self.discoveryPicker.currentText()
            testFileName = ""
            testName = ""
        else:
            discoveryStart = ""
            testFileName = self.testsuitePicker.currentText()
            testName = self.testComboBox.currentText()
            if testName:
                self.insertTestName(testName)
            if testFileName and not testName:
                testName = "suite"
        
        if not discover and not testFileName and not testName:
            E5MessageBox.critical(
                self,
                self.tr("Unittest"),
                self.tr("You must select auto-discovery or enter a test suite"
                        " file or a dotted test name."))
            return
        
        # prepend the selected file to the testsuite combobox
        self.insertProg(testFileName)
        self.sbLabel.setText(self.tr("Preparing Testsuite"))
        QApplication.processEvents()
        
        if discover:
            self.testName = self.tr("Unittest with auto-discovery")
        else:
            # build the module name from the filename without extension
            if testFileName:
                self.testName = os.path.splitext(
                    os.path.basename(testFileName))[0]
            elif testName:
                self.testName = testName
            else:
                self.testName = self.tr("<Unnamed Test>")
        
        if failedOnly:
            testCases = []
        else:
            testCases = self.__selectedTestCases()
        
            if not testCases and self.discoveryList.topLevelItemCount():
                ok = E5MessageBox.yesNo(
                    self,
                    self.tr("Unittest"),
                    self.tr("""No test case has been selected. Shall all"""
                            """ test cases be run?"""))
                if not ok:
                    return
        
        if self.__dbs:
            venvName = self.venvComboBox.currentText()
            
            # we are cooperating with the eric IDE
            project = e5App().getObject("Project")
            if self.__forProject:
                mainScript = project.getMainScript(True)
                clientType = project.getProjectLanguage()
                if mainScript:
                    workdir = os.path.dirname(os.path.abspath(mainScript))
                    coverageFile = os.path.splitext(mainScript)[0]
                else:
                    workdir = project.getProjectPath()
                    coverageFile = os.path.join(discoveryStart, "unittest")
                sysPath = [workdir]
                if discover and not discoveryStart:
                    discoveryStart = workdir
            else:
                if discover:
                    if not discoveryStart:
                        E5MessageBox.critical(
                            self,
                            self.tr("Unittest"),
                            self.tr("You must enter a start directory for"
                                    " auto-discovery."))
                        return
                    
                    coverageFile = os.path.join(discoveryStart, "unittest")
                    workdir = ""
                    clientType = "Python3"
                elif testFileName:
                    mainScript = os.path.abspath(testFileName)
                    workdir = os.path.dirname(mainScript)
                    clientType = "Python3"
                    coverageFile = os.path.splitext(mainScript)[0]
                else:
                    coverageFile = os.path.abspath("unittest")
                    workdir = ""
                    clientType = "Python3"
                sysPath = []
            if failedOnly and self.__failedTests:
                failed = self.__failedTests[:]
                if discover:
                    workdir = discoveryStart
                    discover = False
            else:
                failed = []
            self.__failedTests = []
            self.__dbs.remoteUTPrepare(
                testFileName, self.testName, testName, failed,
                self.coverageCheckBox.isChecked(), coverageFile,
                self.coverageEraseCheckBox.isChecked(), clientType=clientType,
                forProject=self.__forProject, workdir=workdir,
                venvName=venvName, syspath=sysPath,
                discover=discover, discoveryStart=discoveryStart,
                testCases=testCases, debug=self.debuggerCheckBox.isChecked())
        else:
            # we are running as an application
            if discover and not discoveryStart:
                E5MessageBox.critical(
                    self,
                    self.tr("Unittest"),
                    self.tr("You must enter a start directory for"
                            " auto-discovery."))
                return
            
            if testFileName:
                sys.path = (
                    [os.path.dirname(os.path.abspath(testFileName))] +
                    self.savedSysPath
                )
            elif discoveryStart:
                sys.path = (
                    [os.path.abspath(discoveryStart)] +
                    self.savedSysPath
                )
            
            # clean up list of imported modules to force a reimport upon
            # running the test
            if self.savedModulelist:
                for modname in list(sys.modules.keys()):
                    if modname not in self.savedModulelist:
                        # delete it
                        del(sys.modules[modname])
            self.savedModulelist = sys.modules.copy()
            
            os.chdir(self.savedCwd)
            
            # now try to generate the testsuite
            try:
                testLoader = unittest.TestLoader()
                if failedOnly and self.__failedTests:
                    failed = self.__failedTests[:]
                    if discover:
                        os.chdir(discoveryStart)
                        discover = False
                else:
                    failed = []
                if discover:
                    if testCases:
                        test = testLoader.loadTestsFromNames(testCases)
                    else:
                        test = testLoader.discover(discoveryStart)
                else:
                    if testFileName:
                        module = __import__(self.testName)
                    else:
                        module = None
                    if failedOnly and self.__failedTests:
                        if module:
                            failed = [t.split(".", 1)[1]
                                      for t in self.__failedTests]
                        else:
                            failed = self.__failedTests[:]
                        test = testLoader.loadTestsFromNames(
                            failed, module)
                    else:
                        test = testLoader.loadTestsFromName(
                            testName, module)
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                E5MessageBox.critical(
                    self,
                    self.tr("Unittest"),
                    self.tr(
                        "<p>Unable to run test <b>{0}</b>.</p>"
                        "<p>{1}<br/>{2}</p>")
                    .format(self.testName, str(exc_type),
                            str(exc_value).replace("\n", "<br/>"))
                )
                return
                
            # now set up the coverage stuff
            if self.coverageCheckBox.isChecked():
                if discover:
                    covname = os.path.join(discoveryStart, "unittest")
                elif testFileName:
                    covname = os.path.splitext(
                        os.path.abspath(testFileName))[0]
                else:
                    covname = "unittest"
                
                from DebugClients.Python.coverage import coverage
                cover = coverage(data_file="{0}.coverage".format(covname))
                if self.coverageEraseCheckBox.isChecked():
                    cover.erase()
            else:
                cover = None
            
            self.testResult = QtTestResult(
                self, self.failfastCheckBox.isChecked())
            self.totalTests = test.countTestCases()
            self.__failedTests = []
            self.__setRunningMode()
            if cover:
                cover.start()
            test.run(self.testResult)
            if cover:
                cover.stop()
                cover.save()
            self.__setStoppedMode()
            sys.path = self.savedSysPath
    
    def __UTPrepared(self, nrTests, exc_type, exc_value):
        """
        Private slot to handle the utPrepared signal.
        
        If the unittest suite was loaded successfully, we ask the
        client to run the test suite.
        
        @param nrTests number of tests contained in the test suite (integer)
        @param exc_type type of exception occured during preparation (string)
        @param exc_value value of exception occured during preparation (string)
        """
        if nrTests == 0:
            E5MessageBox.critical(
                self,
                self.tr("Unittest"),
                self.tr(
                    "<p>Unable to run test <b>{0}</b>.</p>"
                    "<p>{1}<br/>{2}</p>")
                .format(self.testName, exc_type,
                        exc_value.replace("\n", "<br/>"))
            )
            return
        
        self.totalTests = nrTests
        self.__setRunningMode()
        self.__dbs.remoteUTRun(debug=self.debuggerCheckBox.isChecked(),
                               failfast=self.failfastCheckBox.isChecked())
    
    @pyqtSlot()
    def __stopTests(self):
        """
        Private slot to stop the test.
        """
        if self.__dbs:
            self.__dbs.remoteUTStop()
        elif self.testResult:
            self.testResult.stop()
    
    def on_errorsListWidget_currentTextChanged(self, text):
        """
        Private slot to handle the highlighted signal.
        
        @param text current text (string)
        """
        if text:
            for pattern in self.rxPatterns:
                text = re.sub(pattern, "", text)
            
            foundItems = self.testsListWidget.findItems(
                text, Qt.MatchFlags(Qt.MatchFlag.MatchExactly))
            if len(foundItems) > 0:
                itm = foundItems[0]
                self.testsListWidget.setCurrentItem(itm)
                self.testsListWidget.scrollToItem(itm)
    
    def __setRunningMode(self):
        """
        Private method to set the GUI in running mode.
        """
        self.running = True
        self.tabWidget.setCurrentIndex(1)
        
        # reset counters and error infos
        self.runCount = 0
        self.failCount = 0
        self.errorCount = 0
        self.skippedCount = 0
        self.expectedFailureCount = 0
        self.unexpectedSuccessCount = 0
        self.remainingCount = self.totalTests
        
        # reset the GUI
        self.progressCounterRunCount.setText(str(self.runCount))
        self.progressCounterRemCount.setText(str(self.remainingCount))
        self.progressCounterFailureCount.setText(str(self.failCount))
        self.progressCounterErrorCount.setText(str(self.errorCount))
        self.progressCounterSkippedCount.setText(str(self.skippedCount))
        self.progressCounterExpectedFailureCount.setText(
            str(self.expectedFailureCount))
        self.progressCounterUnexpectedSuccessCount.setText(
            str(self.unexpectedSuccessCount))
        
        self.errorsListWidget.clear()
        self.testsListWidget.clear()
        
        self.progressProgressBar.setRange(0, self.totalTests)
        self.__setProgressColor("green")
        self.progressProgressBar.reset()
        
        self.stopButton.setEnabled(True)
        self.startButton.setEnabled(False)
        self.startFailedButton.setEnabled(False)
        self.stopButton.setDefault(True)
        
        self.sbLabel.setText(self.tr("Running"))
        self.progressLed.on()
        QApplication.processEvents()
        
        self.startTime = time.time()
    
    def __setStoppedMode(self):
        """
        Private method to set the GUI in stopped mode.
        """
        self.stopTime = time.time()
        self.timeTaken = float(self.stopTime - self.startTime)
        self.running = False
        
        failedAvailable = bool(self.__failedTests)
        self.startButton.setEnabled(True)
        self.startFailedButton.setEnabled(failedAvailable)
        self.stopButton.setEnabled(False)
        if failedAvailable:
            self.startFailedButton.setDefault(True)
            self.startButton.setDefault(False)
        else:
            self.startFailedButton.setDefault(False)
            self.startButton.setDefault(True)
        self.sbLabel.setText(
            self.tr("Ran %n test(s) in {0:.3f}s", "", self.runCount)
            .format(self.timeTaken))
        self.progressLed.off()
        
        self.unittestStopped.emit()
        
        self.raise_()
        self.activateWindow()
    
    def testFailed(self, test, exc, testId):
        """
        Public method called if a test fails.
        
        @param test name of the test (string)
        @param exc string representation of the exception (string)
        @param testId id of the test (string)
        """
        self.failCount += 1
        self.progressCounterFailureCount.setText(str(self.failCount))
        itm = QListWidgetItem(self.tr("Failure: {0}").format(test))
        itm.setData(UnittestDialog.ErrorsInfoRole, (test, exc))
        self.errorsListWidget.insertItem(0, itm)
        self.__failedTests.append(testId)
    
    def testErrored(self, test, exc, testId):
        """
        Public method called if a test errors.
        
        @param test name of the test (string)
        @param exc string representation of the exception (string)
        @param testId id of the test (string)
        """
        self.errorCount += 1
        self.progressCounterErrorCount.setText(str(self.errorCount))
        itm = QListWidgetItem(self.tr("Error: {0}").format(test))
        itm.setData(UnittestDialog.ErrorsInfoRole, (test, exc))
        self.errorsListWidget.insertItem(0, itm)
        self.__failedTests.append(testId)
    
    def testSkipped(self, test, reason, testId):
        """
        Public method called if a test was skipped.
        
        @param test name of the test (string)
        @param reason reason for skipping the test (string)
        @param testId id of the test (string)
        """
        self.skippedCount += 1
        self.progressCounterSkippedCount.setText(str(self.skippedCount))
        itm = QListWidgetItem(self.tr("    Skipped: {0}").format(reason))
        if e5App().usesDarkPalette():
            itm.setForeground(self.SkippedColorDarkTheme)
        else:
            itm.setForeground(self.SkippedColorLightTheme)
        self.testsListWidget.insertItem(1, itm)
    
    def testFailedExpected(self, test, exc, testId):
        """
        Public method called if a test fails as expected.
        
        @param test name of the test (string)
        @param exc string representation of the exception (string)
        @param testId id of the test (string)
        """
        self.expectedFailureCount += 1
        self.progressCounterExpectedFailureCount.setText(
            str(self.expectedFailureCount))
        itm = QListWidgetItem(self.tr("    Expected Failure"))
        if e5App().usesDarkPalette():
            itm.setForeground(self.FailedExpectedColorDarkTheme)
        else:
            itm.setForeground(self.FailedExpectedColorLightTheme)
        self.testsListWidget.insertItem(1, itm)
    
    def testSucceededUnexpected(self, test, testId):
        """
        Public method called if a test succeeds unexpectedly.
        
        @param test name of the test (string)
        @param testId id of the test (string)
        """
        self.unexpectedSuccessCount += 1
        self.progressCounterUnexpectedSuccessCount.setText(
            str(self.unexpectedSuccessCount))
        itm = QListWidgetItem(self.tr("    Unexpected Success"))
        if e5App().usesDarkPalette():
            itm.setForeground(self.SucceededUnexpectedColorDarkTheme)
        else:
            itm.setForeground(self.SucceededUnexpectedColorLightTheme)
        self.testsListWidget.insertItem(1, itm)
    
    def testStarted(self, test, doc):
        """
        Public method called if a test is about to be run.
        
        @param test name of the started test (string)
        @param doc documentation of the started test (string)
        """
        if doc:
            self.testsListWidget.insertItem(0, "    {0}".format(doc))
        self.testsListWidget.insertItem(0, test)
        if self.__dbs is None:
            QApplication.processEvents()
    
    def testFinished(self):
        """
        Public method called if a test has finished.
        
        <b>Note</b>: It is also called if it has already failed or errored.
        """
        # update the counters
        self.remainingCount -= 1
        self.runCount += 1
        self.progressCounterRunCount.setText(str(self.runCount))
        self.progressCounterRemCount.setText(str(self.remainingCount))
        
        # update the progressbar
        if self.errorCount:
            self.__setProgressColor("red")
        elif self.failCount:
            self.__setProgressColor("orange")
        self.progressProgressBar.setValue(self.runCount)
    
    def on_errorsListWidget_itemDoubleClicked(self, lbitem):
        """
        Private slot called by doubleclicking an errorlist entry.
        
        It will popup a dialog showing the stacktrace.
        If called from eric, an additional button is displayed
        to show the python source in an eric source viewer (in
        erics main window.
        
        @param lbitem the listbox item that was double clicked
        """
        self.errListIndex = self.errorsListWidget.row(lbitem)
        text = lbitem.text()
        self.on_errorsListWidget_currentTextChanged(text)
        
        # get the error info
        test, tracebackText = lbitem.data(UnittestDialog.ErrorsInfoRole)
        
        # now build the dialog
        from .Ui_UnittestStacktraceDialog import Ui_UnittestStacktraceDialog
        self.dlg = QDialog(self)
        ui = Ui_UnittestStacktraceDialog()
        ui.setupUi(self.dlg)
        self.dlg.traceback = ui.traceback
        
        ui.showButton = ui.buttonBox.addButton(
            self.tr("Show Source"), QDialogButtonBox.ButtonRole.ActionRole)
        ui.showButton.clicked.connect(self.__showSource)
        
        ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        
        self.dlg.setWindowTitle(text)
        ui.testLabel.setText(test)
        ui.traceback.setPlainText(tracebackText)
        
        # and now fire it up
        self.dlg.show()
        self.dlg.exec()
    
    def __showSource(self):
        """
        Private slot to show the source of a traceback in an eric editor.
        """
        # get the error info
        tracebackLines = self.dlg.traceback.toPlainText().splitlines()
        # find the last entry matching the pattern
        for index in range(len(tracebackLines) - 1, -1, -1):
            fmatch = re.search(r'File "(.*?)", line (\d*?),.*',
                               tracebackLines[index])
            if fmatch:
                break
        if fmatch:
            fn, ln = fmatch.group(1, 2)
            if self.__dbs:
                # running as part of eric IDE
                self.unittestFile.emit(fn, int(ln), True)
            else:
                self.__openEditor(fn, int(ln))
    
    def hasFailedTests(self):
        """
        Public method to check, if there are failed tests from the last run.
        
        @return flag indicating the presence of failed tests (boolean)
        """
        return bool(self.__failedTests)
    
    def __openEditor(self, filename, linenumber):
        """
        Private method to open an editor window for the given file.
        
        Note: This method opens an editor window when the unittest dialog
        is called as a standalone application.
        
        @param filename path of the file to be opened
        @type str
        @param linenumber line number to place the cursor at
        @type int
        """
        from QScintilla.MiniEditor import MiniEditor
        editor = MiniEditor(filename, "Python3", self)
        editor.gotoLine(linenumber)
        editor.show()
        
        self.__editors.append(editor)
    
    def closeEvent(self, event):
        """
        Protected method to handle the close event.
        
        @param event close event
        @type QCloseEvent
        """
        event.accept()
        
        for editor in self.__editors:
            try:
                editor.close()
            except Exception:           # secok
                # ignore all exceptions
                pass


class QtTestResult(unittest.TestResult):
    """
    A TestResult derivative to work with a graphical GUI.
    
    For more details see pyunit.py of the standard Python distribution.
    """
    def __init__(self, parent, failfast):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type UnittestDialog
        @param failfast flag indicating to stop at the first error
        @type bool
        """
        super(QtTestResult, self).__init__()
        self.parent = parent
        self.failfast = failfast
    
    def addFailure(self, test, err):
        """
        Public method called if a test failed.
        
        @param test reference to the test object
        @param err error traceback
        """
        super(QtTestResult, self).addFailure(test, err)
        tracebackLines = self._exc_info_to_string(err, test)
        self.parent.testFailed(str(test), tracebackLines, test.id())
    
    def addError(self, test, err):
        """
        Public method called if a test errored.
        
        @param test reference to the test object
        @param err error traceback
        """
        super(QtTestResult, self).addError(test, err)
        tracebackLines = self._exc_info_to_string(err, test)
        self.parent.testErrored(str(test), tracebackLines, test.id())
    
    def addSkip(self, test, reason):
        """
        Public method called if a test was skipped.
        
        @param test reference to the test object
        @param reason reason for skipping the test (string)
        """
        super(QtTestResult, self).addSkip(test, reason)
        self.parent.testSkipped(str(test), reason, test.id())
    
    def addExpectedFailure(self, test, err):
        """
        Public method called if a test failed expected.
        
        @param test reference to the test object
        @param err error traceback
        """
        super(QtTestResult, self).addExpectedFailure(test, err)
        tracebackLines = self._exc_info_to_string(err, test)
        self.parent.testFailedExpected(str(test), tracebackLines, test.id())
    
    def addUnexpectedSuccess(self, test):
        """
        Public method called if a test succeeded expectedly.
        
        @param test reference to the test object
        """
        super(QtTestResult, self).addUnexpectedSuccess(test)
        self.parent.testSucceededUnexpected(str(test), test.id())
    
    def startTest(self, test):
        """
        Public method called at the start of a test.
        
        @param test Reference to the test object
        """
        super(QtTestResult, self).startTest(test)
        self.parent.testStarted(str(test), test.shortDescription())

    def stopTest(self, test):
        """
        Public method called at the end of a test.
        
        @param test Reference to the test object
        """
        super(QtTestResult, self).stopTest(test)
        self.parent.testFinished()


class UnittestWindow(E5MainWindow):
    """
    Main window class for the standalone dialog.
    """
    def __init__(self, prog=None, parent=None):
        """
        Constructor
        
        @param prog filename of the program to open
        @param parent reference to the parent widget (QWidget)
        """
        super(UnittestWindow, self).__init__(parent)
        self.cw = UnittestDialog(prog, parent=self)
        self.cw.installEventFilter(self)
        size = self.cw.size()
        self.setCentralWidget(self.cw)
        self.resize(size)
        
        self.setStyle(Preferences.getUI("Style"),
                      Preferences.getUI("StyleSheet"))
        
        self.cw.buttonBox.accepted.connect(self.close)
        self.cw.buttonBox.rejected.connect(self.close)
    
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
