# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsGit\GitStashDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitStashDataDialog(object):
    def setupUi(self, GitStashDataDialog):
        GitStashDataDialog.setObjectName("GitStashDataDialog")
        GitStashDataDialog.resize(500, 238)
        GitStashDataDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitStashDataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(GitStashDataDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.messageEdit = QtWidgets.QLineEdit(GitStashDataDialog)
        self.messageEdit.setObjectName("messageEdit")
        self.gridLayout.addWidget(self.messageEdit, 0, 1, 1, 1)
        self.keepCheckBox = QtWidgets.QCheckBox(GitStashDataDialog)
        self.keepCheckBox.setObjectName("keepCheckBox")
        self.gridLayout.addWidget(self.keepCheckBox, 1, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(GitStashDataDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.noneRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.noneRadioButton.setChecked(True)
        self.noneRadioButton.setObjectName("noneRadioButton")
        self.verticalLayout.addWidget(self.noneRadioButton)
        self.untrackedRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.untrackedRadioButton.setObjectName("untrackedRadioButton")
        self.verticalLayout.addWidget(self.untrackedRadioButton)
        self.allRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.allRadioButton.setObjectName("allRadioButton")
        self.verticalLayout.addWidget(self.allRadioButton)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitStashDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(GitStashDataDialog)
        self.buttonBox.accepted.connect(GitStashDataDialog.accept)
        self.buttonBox.rejected.connect(GitStashDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitStashDataDialog)
        GitStashDataDialog.setTabOrder(self.messageEdit, self.keepCheckBox)
        GitStashDataDialog.setTabOrder(self.keepCheckBox, self.noneRadioButton)
        GitStashDataDialog.setTabOrder(self.noneRadioButton, self.untrackedRadioButton)
        GitStashDataDialog.setTabOrder(self.untrackedRadioButton, self.allRadioButton)

    def retranslateUi(self, GitStashDataDialog):
        _translate = QtCore.QCoreApplication.translate
        GitStashDataDialog.setWindowTitle(_translate("GitStashDataDialog", "Git Stash"))
        self.label_3.setText(_translate("GitStashDataDialog", "Message:"))
        self.messageEdit.setToolTip(_translate("GitStashDataDialog", "Enter a message for the stash"))
        self.keepCheckBox.setText(_translate("GitStashDataDialog", "Keep changes in staging area"))
        self.groupBox.setTitle(_translate("GitStashDataDialog", "Untracked/Ignored Files"))
        self.noneRadioButton.setToolTip(_translate("GitStashDataDialog", "Select to not stash untracked or ignored files"))
        self.noneRadioButton.setText(_translate("GitStashDataDialog", "Don\'t stash untracked or ignored files"))
        self.untrackedRadioButton.setToolTip(_translate("GitStashDataDialog", "Select to stash untracked files"))
        self.untrackedRadioButton.setText(_translate("GitStashDataDialog", "Stash untracked files"))
        self.allRadioButton.setToolTip(_translate("GitStashDataDialog", "Select to stash untracked and ignored files"))
        self.allRadioButton.setText(_translate("GitStashDataDialog", "Stash untracked and ignored files"))
