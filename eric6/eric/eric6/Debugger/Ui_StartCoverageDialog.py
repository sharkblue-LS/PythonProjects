# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Debugger\StartCoverageDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StartCoverageDialog(object):
    def setupUi(self, StartCoverageDialog):
        StartCoverageDialog.setObjectName("StartCoverageDialog")
        StartCoverageDialog.resize(550, 303)
        StartCoverageDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(StartCoverageDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.TextLabel2 = QtWidgets.QLabel(StartCoverageDialog)
        self.TextLabel2.setObjectName("TextLabel2")
        self.gridLayout_3.addWidget(self.TextLabel2, 2, 0, 1, 1)
        self.TextLabel1 = QtWidgets.QLabel(StartCoverageDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.gridLayout_3.addWidget(self.TextLabel1, 1, 0, 1, 1)
        self.cmdlineCombo = QtWidgets.QComboBox(StartCoverageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdlineCombo.sizePolicy().hasHeightForWidth())
        self.cmdlineCombo.setSizePolicy(sizePolicy)
        self.cmdlineCombo.setEditable(True)
        self.cmdlineCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.cmdlineCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.cmdlineCombo.setDuplicatesEnabled(False)
        self.cmdlineCombo.setObjectName("cmdlineCombo")
        self.gridLayout_3.addWidget(self.cmdlineCombo, 1, 1, 1, 1)
        self.environmentCombo = QtWidgets.QComboBox(StartCoverageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.environmentCombo.sizePolicy().hasHeightForWidth())
        self.environmentCombo.setSizePolicy(sizePolicy)
        self.environmentCombo.setEditable(True)
        self.environmentCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.environmentCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.environmentCombo.setDuplicatesEnabled(False)
        self.environmentCombo.setObjectName("environmentCombo")
        self.gridLayout_3.addWidget(self.environmentCombo, 3, 1, 1, 1)
        self.workdirPicker = E5ComboPathPicker(StartCoverageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workdirPicker.sizePolicy().hasHeightForWidth())
        self.workdirPicker.setSizePolicy(sizePolicy)
        self.workdirPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.workdirPicker.setObjectName("workdirPicker")
        self.gridLayout_3.addWidget(self.workdirPicker, 2, 1, 1, 1)
        self.venvComboBox = QtWidgets.QComboBox(StartCoverageDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.venvComboBox.sizePolicy().hasHeightForWidth())
        self.venvComboBox.setSizePolicy(sizePolicy)
        self.venvComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.venvComboBox.setObjectName("venvComboBox")
        self.gridLayout_3.addWidget(self.venvComboBox, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(StartCoverageDialog)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.textLabel1 = QtWidgets.QLabel(StartCoverageDialog)
        self.textLabel1.setObjectName("textLabel1")
        self.gridLayout_3.addWidget(self.textLabel1, 3, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.globalOverrideGroup = QtWidgets.QGroupBox(StartCoverageDialog)
        self.globalOverrideGroup.setCheckable(True)
        self.globalOverrideGroup.setChecked(False)
        self.globalOverrideGroup.setObjectName("globalOverrideGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.globalOverrideGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.redirectCheckBox = QtWidgets.QCheckBox(self.globalOverrideGroup)
        self.redirectCheckBox.setObjectName("redirectCheckBox")
        self.verticalLayout.addWidget(self.redirectCheckBox)
        self.verticalLayout_2.addWidget(self.globalOverrideGroup)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.exceptionCheckBox = QtWidgets.QCheckBox(StartCoverageDialog)
        self.exceptionCheckBox.setChecked(True)
        self.exceptionCheckBox.setObjectName("exceptionCheckBox")
        self.gridLayout_2.addWidget(self.exceptionCheckBox, 0, 0, 1, 1)
        self.clearShellCheckBox = QtWidgets.QCheckBox(StartCoverageDialog)
        self.clearShellCheckBox.setChecked(True)
        self.clearShellCheckBox.setObjectName("clearShellCheckBox")
        self.gridLayout_2.addWidget(self.clearShellCheckBox, 0, 1, 1, 1)
        self.consoleCheckBox = QtWidgets.QCheckBox(StartCoverageDialog)
        self.consoleCheckBox.setObjectName("consoleCheckBox")
        self.gridLayout_2.addWidget(self.consoleCheckBox, 1, 0, 1, 1)
        self.eraseCheckBox = QtWidgets.QCheckBox(StartCoverageDialog)
        self.eraseCheckBox.setObjectName("eraseCheckBox")
        self.gridLayout_2.addWidget(self.eraseCheckBox, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(StartCoverageDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.TextLabel2.setBuddy(self.workdirPicker)
        self.TextLabel1.setBuddy(self.cmdlineCombo)
        self.label.setBuddy(self.venvComboBox)
        self.textLabel1.setBuddy(self.environmentCombo)

        self.retranslateUi(StartCoverageDialog)
        self.buttonBox.accepted.connect(StartCoverageDialog.accept)
        self.buttonBox.rejected.connect(StartCoverageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StartCoverageDialog)
        StartCoverageDialog.setTabOrder(self.venvComboBox, self.cmdlineCombo)
        StartCoverageDialog.setTabOrder(self.cmdlineCombo, self.workdirPicker)
        StartCoverageDialog.setTabOrder(self.workdirPicker, self.environmentCombo)
        StartCoverageDialog.setTabOrder(self.environmentCombo, self.globalOverrideGroup)
        StartCoverageDialog.setTabOrder(self.globalOverrideGroup, self.redirectCheckBox)
        StartCoverageDialog.setTabOrder(self.redirectCheckBox, self.exceptionCheckBox)
        StartCoverageDialog.setTabOrder(self.exceptionCheckBox, self.clearShellCheckBox)
        StartCoverageDialog.setTabOrder(self.clearShellCheckBox, self.consoleCheckBox)
        StartCoverageDialog.setTabOrder(self.consoleCheckBox, self.eraseCheckBox)

    def retranslateUi(self, StartCoverageDialog):
        _translate = QtCore.QCoreApplication.translate
        StartCoverageDialog.setWindowTitle(_translate("StartCoverageDialog", "Start coverage run"))
        self.TextLabel2.setText(_translate("StartCoverageDialog", "Working directory:"))
        self.TextLabel1.setText(_translate("StartCoverageDialog", "Script Parameters:"))
        self.cmdlineCombo.setToolTip(_translate("StartCoverageDialog", "Enter the commandline parameters"))
        self.cmdlineCombo.setWhatsThis(_translate("StartCoverageDialog", "<b>Commandline</b>\n"
"<p>Enter the commandline parameters in this field.</p>"))
        self.environmentCombo.setToolTip(_translate("StartCoverageDialog", "Enter the environment variables to be set."))
        self.environmentCombo.setWhatsThis(_translate("StartCoverageDialog", "<b>Environment Variables</b>\n"
"<p>Enter the environment variables to be set for the program. The individual settings must be separated by whitespace and be given in the form \'var=value\'. In order to add to an environment variable, enter it in the form \'var+=value\'. To delete an environment variable, append a \'-\' to the variable name.</p>\n"
"<p>Example: var1=1 var2=\"hello world\" var3+=\":/tmp\" var4-</p>"))
        self.workdirPicker.setToolTip(_translate("StartCoverageDialog", "Enter the working directory"))
        self.workdirPicker.setWhatsThis(_translate("StartCoverageDialog", "<b>Working directory</b>\n"
"<p>Enter the working directory of the application to be debugged. Leave it empty to set the working directory to the executable directory.</p>"))
        self.venvComboBox.setToolTip(_translate("StartCoverageDialog", "Select the virtual environment to be used"))
        self.venvComboBox.setWhatsThis(_translate("StartCoverageDialog", "<b>Virtual Environment</b>\n"
"<p>Enter the virtual environment to be used. Leave it empty to use the default environment, i.e. the one configured globally or per project.</p>"))
        self.label.setText(_translate("StartCoverageDialog", "Virtual Environment:"))
        self.textLabel1.setText(_translate("StartCoverageDialog", "Environment Variables:"))
        self.globalOverrideGroup.setTitle(_translate("StartCoverageDialog", "Override Global Configuration"))
        self.redirectCheckBox.setToolTip(_translate("StartCoverageDialog", "Select, to redirect stdin, stdout and stderr of the program being debugged to the eric IDE"))
        self.redirectCheckBox.setText(_translate("StartCoverageDialog", "Redirect stdin/stdout/stderr"))
        self.exceptionCheckBox.setToolTip(_translate("StartCoverageDialog", "Uncheck to disable exception reporting"))
        self.exceptionCheckBox.setWhatsThis(_translate("StartCoverageDialog", "<b>Report exceptions</b>\n"
"<p>Uncheck this in order to disable exception reporting.</p>"))
        self.exceptionCheckBox.setText(_translate("StartCoverageDialog", "Report exceptions"))
        self.exceptionCheckBox.setShortcut(_translate("StartCoverageDialog", "Alt+E"))
        self.clearShellCheckBox.setToolTip(_translate("StartCoverageDialog", "Select to clear the display of the interpreter window"))
        self.clearShellCheckBox.setWhatsThis(_translate("StartCoverageDialog", "<b>Clear interpreter window</b><p>This clears the display of the interpreter window before starting the debug client.</p>"))
        self.clearShellCheckBox.setText(_translate("StartCoverageDialog", "Clear interpreter window"))
        self.consoleCheckBox.setToolTip(_translate("StartCoverageDialog", "Select to start the debugger in a console window"))
        self.consoleCheckBox.setWhatsThis(_translate("StartCoverageDialog", "<b>Start in console</b>\n"
"<p>Select to start the debugger in a console window. The console command has to be configured on the Debugger-&gt;General page</p>"))
        self.consoleCheckBox.setText(_translate("StartCoverageDialog", "Start in console"))
        self.eraseCheckBox.setToolTip(_translate("StartCoverageDialog", "Select this to erase the collected coverage information"))
        self.eraseCheckBox.setWhatsThis(_translate("StartCoverageDialog", "<b>Erase coverage information</b>\n"
"<p>Select this to erase the collected coverage information before the next coverage run.</p>"))
        self.eraseCheckBox.setText(_translate("StartCoverageDialog", "Erase coverage information"))
        self.eraseCheckBox.setShortcut(_translate("StartCoverageDialog", "Alt+C"))
from E5Gui.E5PathPicker import E5ComboPathPicker
