# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsGit\GitCommandDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitCommandDialog(object):
    def setupUi(self, GitCommandDialog):
        GitCommandDialog.setObjectName("GitCommandDialog")
        GitCommandDialog.resize(628, 99)
        GitCommandDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitCommandDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.textLabel1 = QtWidgets.QLabel(GitCommandDialog)
        self.textLabel1.setObjectName("textLabel1")
        self.gridLayout.addWidget(self.textLabel1, 0, 0, 1, 1)
        self.commandCombo = QtWidgets.QComboBox(GitCommandDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandCombo.sizePolicy().hasHeightForWidth())
        self.commandCombo.setSizePolicy(sizePolicy)
        self.commandCombo.setEditable(True)
        self.commandCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.commandCombo.setDuplicatesEnabled(False)
        self.commandCombo.setObjectName("commandCombo")
        self.gridLayout.addWidget(self.commandCombo, 0, 1, 1, 1)
        self.textLabel3 = QtWidgets.QLabel(GitCommandDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textLabel3.sizePolicy().hasHeightForWidth())
        self.textLabel3.setSizePolicy(sizePolicy)
        self.textLabel3.setObjectName("textLabel3")
        self.gridLayout.addWidget(self.textLabel3, 1, 0, 1, 1)
        self.projectDirLabel = QtWidgets.QLabel(GitCommandDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectDirLabel.sizePolicy().hasHeightForWidth())
        self.projectDirLabel.setSizePolicy(sizePolicy)
        self.projectDirLabel.setObjectName("projectDirLabel")
        self.gridLayout.addWidget(self.projectDirLabel, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitCommandDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(GitCommandDialog)
        self.buttonBox.accepted.connect(GitCommandDialog.accept)
        self.buttonBox.rejected.connect(GitCommandDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitCommandDialog)
        GitCommandDialog.setTabOrder(self.commandCombo, self.buttonBox)

    def retranslateUi(self, GitCommandDialog):
        _translate = QtCore.QCoreApplication.translate
        GitCommandDialog.setWindowTitle(_translate("GitCommandDialog", "Git Command"))
        self.textLabel1.setText(_translate("GitCommandDialog", "Git Command:"))
        self.commandCombo.setToolTip(_translate("GitCommandDialog", "Enter the Git command to be executed with all necessary parameters"))
        self.commandCombo.setWhatsThis(_translate("GitCommandDialog", "<b>Git Command</b>\n"
"<p>Enter the Git command to be executed including all necessary \n"
"parameters. If a parameter of the commandline includes a space you have to \n"
"surround this parameter by single or double quotes. Do not include the name \n"
"of the Git client executable (i.e. git).</p>"))
        self.textLabel3.setText(_translate("GitCommandDialog", "Project Directory:"))
        self.projectDirLabel.setToolTip(_translate("GitCommandDialog", "This shows the root directory of the current project."))
        self.projectDirLabel.setText(_translate("GitCommandDialog", "project directory"))
