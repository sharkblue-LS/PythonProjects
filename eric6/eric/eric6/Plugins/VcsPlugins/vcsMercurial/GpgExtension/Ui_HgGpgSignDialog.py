# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsMercurial\GpgExtension\HgGpgSignDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgGpgSignDialog(object):
    def setupUi(self, HgGpgSignDialog):
        HgGpgSignDialog.setObjectName("HgGpgSignDialog")
        HgGpgSignDialog.resize(400, 518)
        HgGpgSignDialog.setWindowTitle("")
        HgGpgSignDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(HgGpgSignDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(HgGpgSignDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.numberButton = QtWidgets.QRadioButton(self.groupBox)
        self.numberButton.setObjectName("numberButton")
        self.gridLayout.addWidget(self.numberButton, 0, 0, 1, 1)
        self.numberSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.numberSpinBox.setEnabled(False)
        self.numberSpinBox.setAlignment(QtCore.Qt.AlignRight)
        self.numberSpinBox.setMaximum(999999999)
        self.numberSpinBox.setObjectName("numberSpinBox")
        self.gridLayout.addWidget(self.numberSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.idButton = QtWidgets.QRadioButton(self.groupBox)
        self.idButton.setObjectName("idButton")
        self.gridLayout.addWidget(self.idButton, 1, 0, 1, 1)
        self.idEdit = QtWidgets.QLineEdit(self.groupBox)
        self.idEdit.setEnabled(False)
        self.idEdit.setObjectName("idEdit")
        self.gridLayout.addWidget(self.idEdit, 1, 1, 1, 2)
        self.tagButton = QtWidgets.QRadioButton(self.groupBox)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 2, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(self.groupBox)
        self.tagCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagCombo.sizePolicy().hasHeightForWidth())
        self.tagCombo.setSizePolicy(sizePolicy)
        self.tagCombo.setEditable(True)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout.addWidget(self.tagCombo, 2, 1, 1, 2)
        self.branchButton = QtWidgets.QRadioButton(self.groupBox)
        self.branchButton.setObjectName("branchButton")
        self.gridLayout.addWidget(self.branchButton, 3, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(self.groupBox)
        self.branchCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.branchCombo.sizePolicy().hasHeightForWidth())
        self.branchCombo.setSizePolicy(sizePolicy)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 3, 1, 1, 2)
        self.bookmarkButton = QtWidgets.QRadioButton(self.groupBox)
        self.bookmarkButton.setObjectName("bookmarkButton")
        self.gridLayout.addWidget(self.bookmarkButton, 4, 0, 1, 1)
        self.bookmarkCombo = QtWidgets.QComboBox(self.groupBox)
        self.bookmarkCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarkCombo.sizePolicy().hasHeightForWidth())
        self.bookmarkCombo.setSizePolicy(sizePolicy)
        self.bookmarkCombo.setEditable(True)
        self.bookmarkCombo.setObjectName("bookmarkCombo")
        self.gridLayout.addWidget(self.bookmarkCombo, 4, 1, 1, 2)
        self.tipButton = QtWidgets.QRadioButton(self.groupBox)
        self.tipButton.setChecked(True)
        self.tipButton.setObjectName("tipButton")
        self.gridLayout.addWidget(self.tipButton, 5, 0, 1, 3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(HgGpgSignDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nocommitCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.nocommitCheckBox.setObjectName("nocommitCheckBox")
        self.verticalLayout.addWidget(self.nocommitCheckBox)
        self.messageEdit = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.messageEdit.setTabChangesFocus(True)
        self.messageEdit.setObjectName("messageEdit")
        self.verticalLayout.addWidget(self.messageEdit)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(HgGpgSignDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.keyEdit = QtWidgets.QLineEdit(HgGpgSignDialog)
        self.keyEdit.setObjectName("keyEdit")
        self.gridLayout_2.addWidget(self.keyEdit, 0, 1, 1, 1)
        self.localCheckBox = QtWidgets.QCheckBox(HgGpgSignDialog)
        self.localCheckBox.setObjectName("localCheckBox")
        self.gridLayout_2.addWidget(self.localCheckBox, 1, 0, 1, 2)
        self.forceCheckBox = QtWidgets.QCheckBox(HgGpgSignDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.gridLayout_2.addWidget(self.forceCheckBox, 2, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgGpgSignDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(HgGpgSignDialog)
        self.buttonBox.accepted.connect(HgGpgSignDialog.accept)
        self.buttonBox.rejected.connect(HgGpgSignDialog.reject)
        self.numberButton.toggled['bool'].connect(self.numberSpinBox.setEnabled)
        self.idButton.toggled['bool'].connect(self.idEdit.setEnabled)
        self.tagButton.toggled['bool'].connect(self.tagCombo.setEnabled)
        self.branchButton.toggled['bool'].connect(self.branchCombo.setEnabled)
        self.bookmarkButton.toggled['bool'].connect(self.bookmarkCombo.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(HgGpgSignDialog)
        HgGpgSignDialog.setTabOrder(self.numberButton, self.numberSpinBox)
        HgGpgSignDialog.setTabOrder(self.numberSpinBox, self.idButton)
        HgGpgSignDialog.setTabOrder(self.idButton, self.idEdit)
        HgGpgSignDialog.setTabOrder(self.idEdit, self.tagButton)
        HgGpgSignDialog.setTabOrder(self.tagButton, self.tagCombo)
        HgGpgSignDialog.setTabOrder(self.tagCombo, self.branchButton)
        HgGpgSignDialog.setTabOrder(self.branchButton, self.branchCombo)
        HgGpgSignDialog.setTabOrder(self.branchCombo, self.bookmarkButton)
        HgGpgSignDialog.setTabOrder(self.bookmarkButton, self.bookmarkCombo)
        HgGpgSignDialog.setTabOrder(self.bookmarkCombo, self.tipButton)
        HgGpgSignDialog.setTabOrder(self.tipButton, self.nocommitCheckBox)
        HgGpgSignDialog.setTabOrder(self.nocommitCheckBox, self.messageEdit)
        HgGpgSignDialog.setTabOrder(self.messageEdit, self.keyEdit)
        HgGpgSignDialog.setTabOrder(self.keyEdit, self.localCheckBox)
        HgGpgSignDialog.setTabOrder(self.localCheckBox, self.forceCheckBox)
        HgGpgSignDialog.setTabOrder(self.forceCheckBox, self.buttonBox)

    def retranslateUi(self, HgGpgSignDialog):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox.setTitle(_translate("HgGpgSignDialog", "Revision"))
        self.numberButton.setToolTip(_translate("HgGpgSignDialog", "Select to specify a revision by number"))
        self.numberButton.setText(_translate("HgGpgSignDialog", "Number"))
        self.numberSpinBox.setToolTip(_translate("HgGpgSignDialog", "Enter a revision number"))
        self.idButton.setToolTip(_translate("HgGpgSignDialog", "Select to specify a revision by changeset id"))
        self.idButton.setText(_translate("HgGpgSignDialog", "Id:"))
        self.idEdit.setToolTip(_translate("HgGpgSignDialog", "Enter a changeset id"))
        self.tagButton.setToolTip(_translate("HgGpgSignDialog", "Select to specify a revision by a tag"))
        self.tagButton.setText(_translate("HgGpgSignDialog", "Tag:"))
        self.tagCombo.setToolTip(_translate("HgGpgSignDialog", "Enter a tag name"))
        self.branchButton.setToolTip(_translate("HgGpgSignDialog", "Select to specify a revision by a branch"))
        self.branchButton.setText(_translate("HgGpgSignDialog", "Branch:"))
        self.branchCombo.setToolTip(_translate("HgGpgSignDialog", "Enter a branch name"))
        self.bookmarkButton.setToolTip(_translate("HgGpgSignDialog", "Select to specify a revision by a bookmark"))
        self.bookmarkButton.setText(_translate("HgGpgSignDialog", "Bookmark:"))
        self.bookmarkCombo.setToolTip(_translate("HgGpgSignDialog", "Enter a bookmark name"))
        self.tipButton.setToolTip(_translate("HgGpgSignDialog", "Select tip revision of repository"))
        self.tipButton.setText(_translate("HgGpgSignDialog", "Parent"))
        self.groupBox_2.setTitle(_translate("HgGpgSignDialog", "Commit Message"))
        self.nocommitCheckBox.setToolTip(_translate("HgGpgSignDialog", "Select to not commit the signature"))
        self.nocommitCheckBox.setText(_translate("HgGpgSignDialog", "Do Not Commit"))
        self.messageEdit.setToolTip(_translate("HgGpgSignDialog", "Enter a commit message (leave empty to use default)"))
        self.label.setText(_translate("HgGpgSignDialog", "Key-ID:"))
        self.keyEdit.setToolTip(_translate("HgGpgSignDialog", "Enter the ID of the key to be used"))
        self.localCheckBox.setToolTip(_translate("HgGpgSignDialog", "Select to make the signature local"))
        self.localCheckBox.setText(_translate("HgGpgSignDialog", "Local Signature"))
        self.forceCheckBox.setToolTip(_translate("HgGpgSignDialog", "Select to sign even if the signature file is modified"))
        self.forceCheckBox.setText(_translate("HgGpgSignDialog", "Force Signature"))
