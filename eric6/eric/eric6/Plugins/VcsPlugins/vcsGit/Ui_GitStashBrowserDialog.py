# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsGit\GitStashBrowserDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GitStashBrowserDialog(object):
    def setupUi(self, GitStashBrowserDialog):
        GitStashBrowserDialog.setObjectName("GitStashBrowserDialog")
        GitStashBrowserDialog.resize(650, 574)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(GitStashBrowserDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stashList = QtWidgets.QTreeWidget(GitStashBrowserDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.stashList.sizePolicy().hasHeightForWidth())
        self.stashList.setSizePolicy(sizePolicy)
        self.stashList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.stashList.setAlternatingRowColors(True)
        self.stashList.setRootIsDecorated(False)
        self.stashList.setItemsExpandable(False)
        self.stashList.setObjectName("stashList")
        self.verticalLayout_2.addWidget(self.stashList)
        self.groupBox = QtWidgets.QGroupBox(GitStashBrowserDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.statisticsList = QtWidgets.QTreeWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.statisticsList.sizePolicy().hasHeightForWidth())
        self.statisticsList.setSizePolicy(sizePolicy)
        self.statisticsList.setAlternatingRowColors(True)
        self.statisticsList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.statisticsList.setRootIsDecorated(False)
        self.statisticsList.setItemsExpandable(False)
        self.statisticsList.setObjectName("statisticsList")
        self.verticalLayout.addWidget(self.statisticsList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filesLabel = QtWidgets.QLabel(self.groupBox)
        self.filesLabel.setText("")
        self.filesLabel.setObjectName("filesLabel")
        self.horizontalLayout.addWidget(self.filesLabel)
        self.insertionsLabel = QtWidgets.QLabel(self.groupBox)
        self.insertionsLabel.setText("")
        self.insertionsLabel.setObjectName("insertionsLabel")
        self.horizontalLayout.addWidget(self.insertionsLabel)
        self.deletionsLabel = QtWidgets.QLabel(self.groupBox)
        self.deletionsLabel.setText("")
        self.deletionsLabel.setObjectName("deletionsLabel")
        self.horizontalLayout.addWidget(self.deletionsLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.errorGroup = QtWidgets.QGroupBox(GitStashBrowserDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout.addWidget(self.errors)
        self.verticalLayout_2.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(GitStashBrowserDialog)
        self.inputGroup.setObjectName("inputGroup")
        self._2 = QtWidgets.QGridLayout(self.inputGroup)
        self._2.setObjectName("_2")
        spacerItem = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._2.addItem(spacerItem, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self._2.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = QtWidgets.QLineEdit(self.inputGroup)
        self.input.setObjectName("input")
        self._2.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self._2.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(GitStashBrowserDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.buttonBox.raise_()
        self.stashList.raise_()
        self.errorGroup.raise_()
        self.inputGroup.raise_()
        self.groupBox.raise_()

        self.retranslateUi(GitStashBrowserDialog)
        QtCore.QMetaObject.connectSlotsByName(GitStashBrowserDialog)
        GitStashBrowserDialog.setTabOrder(self.stashList, self.statisticsList)
        GitStashBrowserDialog.setTabOrder(self.statisticsList, self.errors)
        GitStashBrowserDialog.setTabOrder(self.errors, self.input)
        GitStashBrowserDialog.setTabOrder(self.input, self.passwordCheckBox)
        GitStashBrowserDialog.setTabOrder(self.passwordCheckBox, self.sendButton)
        GitStashBrowserDialog.setTabOrder(self.sendButton, self.buttonBox)

    def retranslateUi(self, GitStashBrowserDialog):
        _translate = QtCore.QCoreApplication.translate
        GitStashBrowserDialog.setWindowTitle(_translate("GitStashBrowserDialog", "Git Stash Browser"))
        self.stashList.setSortingEnabled(True)
        self.stashList.headerItem().setText(0, _translate("GitStashBrowserDialog", "Name"))
        self.stashList.headerItem().setText(1, _translate("GitStashBrowserDialog", "Date"))
        self.stashList.headerItem().setText(2, _translate("GitStashBrowserDialog", "Message"))
        self.groupBox.setTitle(_translate("GitStashBrowserDialog", "Statistics"))
        self.statisticsList.headerItem().setText(0, _translate("GitStashBrowserDialog", "File"))
        self.statisticsList.headerItem().setText(1, _translate("GitStashBrowserDialog", "Changes"))
        self.statisticsList.headerItem().setText(2, _translate("GitStashBrowserDialog", "Lines added"))
        self.statisticsList.headerItem().setText(3, _translate("GitStashBrowserDialog", "Lines deleted"))
        self.errorGroup.setTitle(_translate("GitStashBrowserDialog", "Errors"))
        self.errors.setWhatsThis(_translate("GitStashBrowserDialog", "<b>Git stash errors</b><p>This shows possible error messages of the git stash command.</p>"))
        self.inputGroup.setTitle(_translate("GitStashBrowserDialog", "Input"))
        self.sendButton.setToolTip(_translate("GitStashBrowserDialog", "Press to send the input to the git process"))
        self.sendButton.setText(_translate("GitStashBrowserDialog", "&Send"))
        self.sendButton.setShortcut(_translate("GitStashBrowserDialog", "Alt+S"))
        self.input.setToolTip(_translate("GitStashBrowserDialog", "Enter data to be sent to the git process"))
        self.passwordCheckBox.setToolTip(_translate("GitStashBrowserDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("GitStashBrowserDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("GitStashBrowserDialog", "Alt+P"))
