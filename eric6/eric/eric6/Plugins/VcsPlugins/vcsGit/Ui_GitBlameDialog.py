# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsGit\GitBlameDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitBlameDialog(object):
    def setupUi(self, GitBlameDialog):
        GitBlameDialog.setObjectName("GitBlameDialog")
        GitBlameDialog.resize(800, 750)
        GitBlameDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(GitBlameDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.blameList = QtWidgets.QTreeWidget(GitBlameDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.blameList.sizePolicy().hasHeightForWidth())
        self.blameList.setSizePolicy(sizePolicy)
        self.blameList.setAlternatingRowColors(True)
        self.blameList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.blameList.setRootIsDecorated(False)
        self.blameList.setItemsExpandable(False)
        self.blameList.setObjectName("blameList")
        self.blameList.header().setStretchLastSection(False)
        self.vboxlayout.addWidget(self.blameList)
        self.errorGroup = QtWidgets.QGroupBox(GitBlameDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout1.addWidget(self.errors)
        self.vboxlayout.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(GitBlameDialog)
        self.inputGroup.setObjectName("inputGroup")
        self.gridlayout = QtWidgets.QGridLayout(self.inputGroup)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = QtWidgets.QLineEdit(self.inputGroup)
        self.input.setObjectName("input")
        self.gridlayout.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self.gridlayout.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.vboxlayout.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitBlameDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(GitBlameDialog)
        QtCore.QMetaObject.connectSlotsByName(GitBlameDialog)
        GitBlameDialog.setTabOrder(self.blameList, self.errors)
        GitBlameDialog.setTabOrder(self.errors, self.input)
        GitBlameDialog.setTabOrder(self.input, self.passwordCheckBox)
        GitBlameDialog.setTabOrder(self.passwordCheckBox, self.sendButton)
        GitBlameDialog.setTabOrder(self.sendButton, self.buttonBox)

    def retranslateUi(self, GitBlameDialog):
        _translate = QtCore.QCoreApplication.translate
        GitBlameDialog.setWindowTitle(_translate("GitBlameDialog", "Git Blame"))
        self.blameList.headerItem().setText(0, _translate("GitBlameDialog", "Commit"))
        self.blameList.headerItem().setText(1, _translate("GitBlameDialog", "Author"))
        self.blameList.headerItem().setText(2, _translate("GitBlameDialog", "Date"))
        self.blameList.headerItem().setText(3, _translate("GitBlameDialog", "Time"))
        self.blameList.headerItem().setText(4, _translate("GitBlameDialog", "Line"))
        self.errorGroup.setTitle(_translate("GitBlameDialog", "Errors"))
        self.inputGroup.setTitle(_translate("GitBlameDialog", "Input"))
        self.sendButton.setToolTip(_translate("GitBlameDialog", "Press to send the input to the git process"))
        self.sendButton.setText(_translate("GitBlameDialog", "&Send"))
        self.sendButton.setShortcut(_translate("GitBlameDialog", "Alt+S"))
        self.input.setToolTip(_translate("GitBlameDialog", "Enter data to be sent to the git process"))
        self.passwordCheckBox.setToolTip(_translate("GitBlameDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("GitBlameDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("GitBlameDialog", "Alt+P"))
