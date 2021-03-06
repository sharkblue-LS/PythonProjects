# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsMercurial\HgStatusDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgStatusDialog(object):
    def setupUi(self, HgStatusDialog):
        HgStatusDialog.setObjectName("HgStatusDialog")
        HgStatusDialog.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgStatusDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.actionsButton = QtWidgets.QToolButton(HgStatusDialog)
        self.actionsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.actionsButton.setObjectName("actionsButton")
        self.horizontalLayout_2.addWidget(self.actionsButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(HgStatusDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.statusFilterCombo = QtWidgets.QComboBox(HgStatusDialog)
        self.statusFilterCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.statusFilterCombo.setObjectName("statusFilterCombo")
        self.horizontalLayout_2.addWidget(self.statusFilterCombo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.diffSplitter = QtWidgets.QSplitter(HgStatusDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.diffSplitter.sizePolicy().hasHeightForWidth())
        self.diffSplitter.setSizePolicy(sizePolicy)
        self.diffSplitter.setOrientation(QtCore.Qt.Vertical)
        self.diffSplitter.setChildrenCollapsible(False)
        self.diffSplitter.setObjectName("diffSplitter")
        self.statusList = QtWidgets.QTreeWidget(self.diffSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusList.sizePolicy().hasHeightForWidth())
        self.statusList.setSizePolicy(sizePolicy)
        self.statusList.setAlternatingRowColors(True)
        self.statusList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.statusList.setRootIsDecorated(False)
        self.statusList.setObjectName("statusList")
        self.layoutWidget = QtWidgets.QWidget(self.diffSplitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.diffLabel = QtWidgets.QLabel(self.layoutWidget)
        self.diffLabel.setObjectName("diffLabel")
        self.verticalLayout_2.addWidget(self.diffLabel)
        self.diffEdit = QtWidgets.QPlainTextEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diffEdit.sizePolicy().hasHeightForWidth())
        self.diffEdit.setSizePolicy(sizePolicy)
        self.diffEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.diffEdit.setReadOnly(True)
        self.diffEdit.setTabStopWidth(8)
        self.diffEdit.setObjectName("diffEdit")
        self.verticalLayout_2.addWidget(self.diffEdit)
        self.verticalLayout.addWidget(self.diffSplitter)
        self.errorGroup = QtWidgets.QGroupBox(HgStatusDialog)
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
        self.verticalLayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgStatusDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.statusFilterCombo)

        self.retranslateUi(HgStatusDialog)
        QtCore.QMetaObject.connectSlotsByName(HgStatusDialog)
        HgStatusDialog.setTabOrder(self.actionsButton, self.statusFilterCombo)
        HgStatusDialog.setTabOrder(self.statusFilterCombo, self.statusList)
        HgStatusDialog.setTabOrder(self.statusList, self.diffEdit)
        HgStatusDialog.setTabOrder(self.diffEdit, self.errors)

    def retranslateUi(self, HgStatusDialog):
        _translate = QtCore.QCoreApplication.translate
        HgStatusDialog.setWindowTitle(_translate("HgStatusDialog", "Mercurial Status"))
        HgStatusDialog.setWhatsThis(_translate("HgStatusDialog", "<b>Mercurial Status</b>\n"
"<p>This dialog shows the status of the selected file or project.</p>"))
        self.actionsButton.setToolTip(_translate("HgStatusDialog", "Select action from menu"))
        self.label.setText(_translate("HgStatusDialog", "&Filter on Status:"))
        self.statusFilterCombo.setToolTip(_translate("HgStatusDialog", "Select the status of entries to be shown"))
        self.statusList.setSortingEnabled(True)
        self.statusList.headerItem().setText(0, _translate("HgStatusDialog", "Commit"))
        self.statusList.headerItem().setText(1, _translate("HgStatusDialog", "Status"))
        self.statusList.headerItem().setText(2, _translate("HgStatusDialog", "Path"))
        self.diffLabel.setText(_translate("HgStatusDialog", "Differences"))
        self.errorGroup.setTitle(_translate("HgStatusDialog", "Errors"))
