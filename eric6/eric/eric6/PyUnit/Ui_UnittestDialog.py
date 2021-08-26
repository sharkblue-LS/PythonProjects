# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\PyUnit\UnittestDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UnittestDialog(object):
    def setupUi(self, UnittestDialog):
        UnittestDialog.setObjectName("UnittestDialog")
        UnittestDialog.resize(650, 700)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(UnittestDialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabWidget = QtWidgets.QTabWidget(UnittestDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.parametersTab = QtWidgets.QWidget()
        self.parametersTab.setObjectName("parametersTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.parametersTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.parametersTab)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.discoverCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.discoverCheckBox.setObjectName("discoverCheckBox")
        self.gridLayout.addWidget(self.discoverCheckBox, 0, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.discoveryPicker = E5ComboPathPicker(self.groupBox)
        self.discoveryPicker.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discoveryPicker.sizePolicy().hasHeightForWidth())
        self.discoveryPicker.setSizePolicy(sizePolicy)
        self.discoveryPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.discoveryPicker.setObjectName("discoveryPicker")
        self.gridLayout.addWidget(self.discoveryPicker, 1, 1, 1, 1)
        self.testsuiteLabel = QtWidgets.QLabel(self.groupBox)
        self.testsuiteLabel.setObjectName("testsuiteLabel")
        self.gridLayout.addWidget(self.testsuiteLabel, 2, 0, 1, 1)
        self.testsuitePicker = E5ComboPathPicker(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testsuitePicker.sizePolicy().hasHeightForWidth())
        self.testsuitePicker.setSizePolicy(sizePolicy)
        self.testsuitePicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.testsuitePicker.setObjectName("testsuitePicker")
        self.gridLayout.addWidget(self.testsuitePicker, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.testComboBox = QtWidgets.QComboBox(self.groupBox)
        self.testComboBox.setEditable(True)
        self.testComboBox.setObjectName("testComboBox")
        self.gridLayout.addWidget(self.testComboBox, 3, 1, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.optionsGroup = QtWidgets.QGroupBox(self.parametersTab)
        self.optionsGroup.setObjectName("optionsGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.optionsGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.venvLabel = QtWidgets.QLabel(self.optionsGroup)
        self.venvLabel.setObjectName("venvLabel")
        self.horizontalLayout_3.addWidget(self.venvLabel)
        self.venvComboBox = QtWidgets.QComboBox(self.optionsGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.venvComboBox.sizePolicy().hasHeightForWidth())
        self.venvComboBox.setSizePolicy(sizePolicy)
        self.venvComboBox.setObjectName("venvComboBox")
        self.horizontalLayout_3.addWidget(self.venvComboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.coverageCheckBox = QtWidgets.QCheckBox(self.optionsGroup)
        self.coverageCheckBox.setObjectName("coverageCheckBox")
        self.gridLayout_2.addWidget(self.coverageCheckBox, 0, 0, 1, 1)
        self.coverageEraseCheckBox = QtWidgets.QCheckBox(self.optionsGroup)
        self.coverageEraseCheckBox.setEnabled(False)
        self.coverageEraseCheckBox.setObjectName("coverageEraseCheckBox")
        self.gridLayout_2.addWidget(self.coverageEraseCheckBox, 0, 1, 1, 1)
        self.failfastCheckBox = QtWidgets.QCheckBox(self.optionsGroup)
        self.failfastCheckBox.setObjectName("failfastCheckBox")
        self.gridLayout_2.addWidget(self.failfastCheckBox, 1, 0, 1, 1)
        self.debuggerCheckBox = QtWidgets.QCheckBox(self.optionsGroup)
        self.debuggerCheckBox.setObjectName("debuggerCheckBox")
        self.gridLayout_2.addWidget(self.debuggerCheckBox, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout_6.addWidget(self.optionsGroup)
        self.discoveryGroup = QtWidgets.QGroupBox(self.parametersTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.discoveryGroup.sizePolicy().hasHeightForWidth())
        self.discoveryGroup.setSizePolicy(sizePolicy)
        self.discoveryGroup.setObjectName("discoveryGroup")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.discoveryGroup)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.discoveryList = QtWidgets.QTreeWidget(self.discoveryGroup)
        self.discoveryList.setAlternatingRowColors(True)
        self.discoveryList.setHeaderHidden(True)
        self.discoveryList.setExpandsOnDoubleClick(False)
        self.discoveryList.setObjectName("discoveryList")
        self.discoveryList.headerItem().setText(0, "1")
        self.verticalLayout_3.addWidget(self.discoveryList)
        self.verticalLayout_6.addWidget(self.discoveryGroup)
        self.tabWidget.addTab(self.parametersTab, "")
        self.resultsTab = QtWidgets.QWidget()
        self.resultsTab.setObjectName("resultsTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.resultsTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.progressGroupBox = QtWidgets.QGroupBox(self.resultsTab)
        self.progressGroupBox.setObjectName("progressGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.progressGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self._8 = QtWidgets.QHBoxLayout()
        self._8.setObjectName("_8")
        self.progressTextLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressTextLabel.setObjectName("progressTextLabel")
        self._8.addWidget(self.progressTextLabel)
        spacerItem = QtWidgets.QSpacerItem(371, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._8.addItem(spacerItem)
        self.progressLed = E5Led(self.progressGroupBox)
        self.progressLed.setObjectName("progressLed")
        self._8.addWidget(self.progressLed)
        self.verticalLayout.addLayout(self._8)
        self.progressProgressBar = QtWidgets.QProgressBar(self.progressGroupBox)
        self.progressProgressBar.setProperty("value", 0)
        self.progressProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressProgressBar.setObjectName("progressProgressBar")
        self.verticalLayout.addWidget(self.progressProgressBar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressCounterRunLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterRunLabel.setObjectName("progressCounterRunLabel")
        self.horizontalLayout_2.addWidget(self.progressCounterRunLabel)
        self.progressCounterRunCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterRunCount.setText("0")
        self.progressCounterRunCount.setObjectName("progressCounterRunCount")
        self.horizontalLayout_2.addWidget(self.progressCounterRunCount)
        self.progressCounterRemLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterRemLabel.setObjectName("progressCounterRemLabel")
        self.horizontalLayout_2.addWidget(self.progressCounterRemLabel)
        self.progressCounterRemCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterRemCount.setText("0")
        self.progressCounterRemCount.setObjectName("progressCounterRemCount")
        self.horizontalLayout_2.addWidget(self.progressCounterRemCount)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressCounterFailureLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterFailureLabel.setObjectName("progressCounterFailureLabel")
        self.horizontalLayout.addWidget(self.progressCounterFailureLabel)
        self.progressCounterFailureCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterFailureCount.setText("0")
        self.progressCounterFailureCount.setObjectName("progressCounterFailureCount")
        self.horizontalLayout.addWidget(self.progressCounterFailureCount)
        self.progressCounterErrorLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterErrorLabel.setObjectName("progressCounterErrorLabel")
        self.horizontalLayout.addWidget(self.progressCounterErrorLabel)
        self.progressCounterErrorCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterErrorCount.setText("0")
        self.progressCounterErrorCount.setObjectName("progressCounterErrorCount")
        self.horizontalLayout.addWidget(self.progressCounterErrorCount)
        self.progressCounterSkippedLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterSkippedLabel.setObjectName("progressCounterSkippedLabel")
        self.horizontalLayout.addWidget(self.progressCounterSkippedLabel)
        self.progressCounterSkippedCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterSkippedCount.setText("0")
        self.progressCounterSkippedCount.setObjectName("progressCounterSkippedCount")
        self.horizontalLayout.addWidget(self.progressCounterSkippedCount)
        self.progressCounterExpectedFailureLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterExpectedFailureLabel.setObjectName("progressCounterExpectedFailureLabel")
        self.horizontalLayout.addWidget(self.progressCounterExpectedFailureLabel)
        self.progressCounterExpectedFailureCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterExpectedFailureCount.setText("0")
        self.progressCounterExpectedFailureCount.setObjectName("progressCounterExpectedFailureCount")
        self.horizontalLayout.addWidget(self.progressCounterExpectedFailureCount)
        self.progressCounterUnexpectedSuccessLabel = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterUnexpectedSuccessLabel.setObjectName("progressCounterUnexpectedSuccessLabel")
        self.horizontalLayout.addWidget(self.progressCounterUnexpectedSuccessLabel)
        self.progressCounterUnexpectedSuccessCount = QtWidgets.QLabel(self.progressGroupBox)
        self.progressCounterUnexpectedSuccessCount.setText("0")
        self.progressCounterUnexpectedSuccessCount.setObjectName("progressCounterUnexpectedSuccessCount")
        self.horizontalLayout.addWidget(self.progressCounterUnexpectedSuccessCount)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.progressGroupBox)
        self.textLabel1 = QtWidgets.QLabel(self.resultsTab)
        self.textLabel1.setObjectName("textLabel1")
        self.verticalLayout_4.addWidget(self.textLabel1)
        self.testsListWidget = QtWidgets.QListWidget(self.resultsTab)
        self.testsListWidget.setObjectName("testsListWidget")
        self.verticalLayout_4.addWidget(self.testsListWidget)
        self.listboxLabel = QtWidgets.QLabel(self.resultsTab)
        self.listboxLabel.setObjectName("listboxLabel")
        self.verticalLayout_4.addWidget(self.listboxLabel)
        self.errorsListWidget = QtWidgets.QListWidget(self.resultsTab)
        self.errorsListWidget.setObjectName("errorsListWidget")
        self.verticalLayout_4.addWidget(self.errorsListWidget)
        self.tabWidget.addTab(self.resultsTab, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(UnittestDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_5.addWidget(self.buttonBox)
        self._3 = QtWidgets.QHBoxLayout()
        self._3.setObjectName("_3")
        self.sbLabel = QtWidgets.QLabel(UnittestDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbLabel.sizePolicy().hasHeightForWidth())
        self.sbLabel.setSizePolicy(sizePolicy)
        self.sbLabel.setObjectName("sbLabel")
        self._3.addWidget(self.sbLabel)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._3.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self._3)
        self.label_3.setBuddy(self.discoveryPicker)
        self.testsuiteLabel.setBuddy(self.testsuitePicker)
        self.label.setBuddy(self.testComboBox)
        self.venvLabel.setBuddy(self.venvComboBox)

        self.retranslateUi(UnittestDialog)
        self.tabWidget.setCurrentIndex(0)
        self.coverageCheckBox.toggled['bool'].connect(self.coverageEraseCheckBox.setEnabled)
        self.buttonBox.accepted.connect(UnittestDialog.close)
        self.buttonBox.rejected.connect(UnittestDialog.close)
        self.discoverCheckBox.toggled['bool'].connect(self.discoveryPicker.setEnabled)
        self.discoverCheckBox.toggled['bool'].connect(self.testsuitePicker.setDisabled)
        self.discoverCheckBox.toggled['bool'].connect(self.testComboBox.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(UnittestDialog)
        UnittestDialog.setTabOrder(self.tabWidget, self.discoverCheckBox)
        UnittestDialog.setTabOrder(self.discoverCheckBox, self.testsuitePicker)
        UnittestDialog.setTabOrder(self.testsuitePicker, self.discoveryPicker)
        UnittestDialog.setTabOrder(self.discoveryPicker, self.testComboBox)
        UnittestDialog.setTabOrder(self.testComboBox, self.venvComboBox)
        UnittestDialog.setTabOrder(self.venvComboBox, self.coverageCheckBox)
        UnittestDialog.setTabOrder(self.coverageCheckBox, self.coverageEraseCheckBox)
        UnittestDialog.setTabOrder(self.coverageEraseCheckBox, self.failfastCheckBox)
        UnittestDialog.setTabOrder(self.failfastCheckBox, self.debuggerCheckBox)
        UnittestDialog.setTabOrder(self.debuggerCheckBox, self.discoveryList)
        UnittestDialog.setTabOrder(self.discoveryList, self.testsListWidget)
        UnittestDialog.setTabOrder(self.testsListWidget, self.errorsListWidget)

    def retranslateUi(self, UnittestDialog):
        _translate = QtCore.QCoreApplication.translate
        UnittestDialog.setWindowTitle(_translate("UnittestDialog", "Unittest"))
        self.groupBox.setTitle(_translate("UnittestDialog", "Test Parameters"))
        self.discoverCheckBox.setToolTip(_translate("UnittestDialog", "Select to discover tests automatically"))
        self.discoverCheckBox.setText(_translate("UnittestDialog", "&Discover tests (test modules must be importable)"))
        self.label_3.setText(_translate("UnittestDialog", "Discovery &Start:"))
        self.discoveryPicker.setToolTip(_translate("UnittestDialog", "Enter name of the directory at which to start the test file discovery"))
        self.discoveryPicker.setWhatsThis(_translate("UnittestDialog", "<b>Discovery Start</b>\n"
"<p>Enter name of the directory at which to start the test file discovery.\n"
"Note that all test modules must be importable from this directory.</p>"))
        self.testsuiteLabel.setText(_translate("UnittestDialog", "Test &Filename:"))
        self.testsuitePicker.setToolTip(_translate("UnittestDialog", "Enter name of file defining the testsuite"))
        self.testsuitePicker.setWhatsThis(_translate("UnittestDialog", "<b>Testsuite</b>\n"
"<p>Enter the name of the file defining the testsuite.\n"
"It should have a method with a name given below. If no name is given, the suite() method will be tried. If no such method can be\n"
"found, the module will be inspected for proper test\n"
"cases.</p>"))
        self.label.setText(_translate("UnittestDialog", "&Test Name:"))
        self.testComboBox.setToolTip(_translate("UnittestDialog", "Enter the test name. Leave empty to use the default name \"suite\"."))
        self.testComboBox.setWhatsThis(_translate("UnittestDialog", "<b>Testname</b><p>Enter the name of the test to be performed. This name must follow the rules given by Python\'s unittest module. If this field is empty, the default name of \"suite\" will be used.</p>"))
        self.optionsGroup.setTitle(_translate("UnittestDialog", "Run Parameters"))
        self.venvLabel.setText(_translate("UnittestDialog", "&Virtual Environment:"))
        self.venvComboBox.setToolTip(_translate("UnittestDialog", "Select the virtual environment to be used"))
        self.venvComboBox.setWhatsThis(_translate("UnittestDialog", "<b>Virtual Environment</b>\\n<p>Enter the virtual environment to be used. Leave it empty to use the default environment, i.e. the one configured globally or per project.</p>"))
        self.coverageCheckBox.setToolTip(_translate("UnittestDialog", "Select whether coverage data should be collected"))
        self.coverageCheckBox.setText(_translate("UnittestDialog", "C&ollect coverage data"))
        self.coverageEraseCheckBox.setToolTip(_translate("UnittestDialog", "Select whether old coverage data should be erased"))
        self.coverageEraseCheckBox.setText(_translate("UnittestDialog", "&Erase coverage data"))
        self.failfastCheckBox.setToolTip(_translate("UnittestDialog", "Select to stop the test run on the first error or failure"))
        self.failfastCheckBox.setText(_translate("UnittestDialog", "Stop on First Error or Failure"))
        self.debuggerCheckBox.setToolTip(_translate("UnittestDialog", "Select to run the unittest with debugger support enabled"))
        self.debuggerCheckBox.setText(_translate("UnittestDialog", "Run with Debugger"))
        self.discoveryGroup.setTitle(_translate("UnittestDialog", "Discovery Results"))
        self.discoveryList.setSortingEnabled(True)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.parametersTab), _translate("UnittestDialog", "Parameters"))
        self.progressGroupBox.setTitle(_translate("UnittestDialog", "Progress"))
        self.progressTextLabel.setText(_translate("UnittestDialog", "Progress:"))
        self.progressProgressBar.setFormat(_translate("UnittestDialog", "%v/%m Tests"))
        self.progressCounterRunLabel.setText(_translate("UnittestDialog", "Run:"))
        self.progressCounterRunCount.setToolTip(_translate("UnittestDialog", "Number of tests run"))
        self.progressCounterRemLabel.setText(_translate("UnittestDialog", "Remaining:"))
        self.progressCounterRemCount.setToolTip(_translate("UnittestDialog", "Number of tests to be run"))
        self.progressCounterFailureLabel.setText(_translate("UnittestDialog", "Failures:"))
        self.progressCounterFailureCount.setToolTip(_translate("UnittestDialog", "Number of test failures"))
        self.progressCounterErrorLabel.setText(_translate("UnittestDialog", "Errors:"))
        self.progressCounterErrorCount.setToolTip(_translate("UnittestDialog", "Number of test errors"))
        self.progressCounterSkippedLabel.setText(_translate("UnittestDialog", "Skipped:"))
        self.progressCounterSkippedCount.setToolTip(_translate("UnittestDialog", "Number of tests skipped"))
        self.progressCounterExpectedFailureLabel.setText(_translate("UnittestDialog", "Expected Failures:"))
        self.progressCounterExpectedFailureCount.setToolTip(_translate("UnittestDialog", "Number of tests with expected failure"))
        self.progressCounterUnexpectedSuccessLabel.setText(_translate("UnittestDialog", "Unexpected Successes:"))
        self.progressCounterUnexpectedSuccessCount.setToolTip(_translate("UnittestDialog", "Number of tests with unexpected success"))
        self.textLabel1.setText(_translate("UnittestDialog", "Tests performed:"))
        self.listboxLabel.setText(_translate("UnittestDialog", "Failures and errors:"))
        self.errorsListWidget.setToolTip(_translate("UnittestDialog", "Failures and Errors list"))
        self.errorsListWidget.setWhatsThis(_translate("UnittestDialog", "<b>Failures and Errors list</b>\n"
"<p>This list shows all failed and errored tests.\n"
"Double clicking on an entry will show the respective traceback.</p>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resultsTab), _translate("UnittestDialog", "Results"))
        self.sbLabel.setText(_translate("UnittestDialog", "Idle"))
from E5Gui.E5Led import E5Led
from E5Gui.E5PathPicker import E5ComboPathPicker
