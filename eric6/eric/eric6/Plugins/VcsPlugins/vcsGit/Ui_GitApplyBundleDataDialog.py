# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsGit\GitApplyBundleDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitApplyBundleDataDialog(object):
    def setupUi(self, GitApplyBundleDataDialog):
        GitApplyBundleDataDialog.setObjectName("GitApplyBundleDataDialog")
        GitApplyBundleDataDialog.resize(400, 94)
        GitApplyBundleDataDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitApplyBundleDataDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(GitApplyBundleDataDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.headCombo = QtWidgets.QComboBox(GitApplyBundleDataDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headCombo.sizePolicy().hasHeightForWidth())
        self.headCombo.setSizePolicy(sizePolicy)
        self.headCombo.setObjectName("headCombo")
        self.gridLayout.addWidget(self.headCombo, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(GitApplyBundleDataDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(GitApplyBundleDataDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.branchCombo.sizePolicy().hasHeightForWidth())
        self.branchCombo.setSizePolicy(sizePolicy)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitApplyBundleDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(GitApplyBundleDataDialog)
        self.buttonBox.accepted.connect(GitApplyBundleDataDialog.accept)
        self.buttonBox.rejected.connect(GitApplyBundleDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GitApplyBundleDataDialog)

    def retranslateUi(self, GitApplyBundleDataDialog):
        _translate = QtCore.QCoreApplication.translate
        GitApplyBundleDataDialog.setWindowTitle(_translate("GitApplyBundleDataDialog", "Git Apply Data"))
        self.label.setText(_translate("GitApplyBundleDataDialog", "Bundle Head:"))
        self.headCombo.setToolTip(_translate("GitApplyBundleDataDialog", "Select a head to apply"))
        self.label_2.setText(_translate("GitApplyBundleDataDialog", "Local Branch:"))
        self.branchCombo.setToolTip(_translate("GitApplyBundleDataDialog", "Enter a local branch"))
