# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsGit\GitBranchPushDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitBranchPushDialog(object):
    def setupUi(self, GitBranchPushDialog):
        GitBranchPushDialog.setObjectName("GitBranchPushDialog")
        GitBranchPushDialog.resize(497, 107)
        GitBranchPushDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitBranchPushDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(GitBranchPushDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.branchComboBox = QtWidgets.QComboBox(GitBranchPushDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.branchComboBox.sizePolicy().hasHeightForWidth())
        self.branchComboBox.setSizePolicy(sizePolicy)
        self.branchComboBox.setObjectName("branchComboBox")
        self.gridLayout.addWidget(self.branchComboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(GitBranchPushDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.remoteComboBox = QtWidgets.QComboBox(GitBranchPushDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remoteComboBox.sizePolicy().hasHeightForWidth())
        self.remoteComboBox.setSizePolicy(sizePolicy)
        self.remoteComboBox.setObjectName("remoteComboBox")
        self.gridLayout.addWidget(self.remoteComboBox, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitBranchPushDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(GitBranchPushDialog)
        self.buttonBox.accepted.connect(GitBranchPushDialog.accept)
        self.buttonBox.rejected.connect(GitBranchPushDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitBranchPushDialog)
        GitBranchPushDialog.setTabOrder(self.branchComboBox, self.remoteComboBox)

    def retranslateUi(self, GitBranchPushDialog):
        _translate = QtCore.QCoreApplication.translate
        GitBranchPushDialog.setWindowTitle(_translate("GitBranchPushDialog", "Git Push Branch"))
        self.label.setText(_translate("GitBranchPushDialog", "Branch Name:"))
        self.branchComboBox.setToolTip(_translate("GitBranchPushDialog", "Select the branch"))
        self.label_2.setText(_translate("GitBranchPushDialog", "Remote Name:"))
        self.remoteComboBox.setToolTip(_translate("GitBranchPushDialog", "Select the remote repository"))
