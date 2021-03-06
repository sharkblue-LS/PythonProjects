# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\VirtualEnv\VirtualenvManagerDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VirtualenvManagerDialog(object):
    def setupUi(self, VirtualenvManagerDialog):
        VirtualenvManagerDialog.setObjectName("VirtualenvManagerDialog")
        VirtualenvManagerDialog.resize(700, 500)
        VirtualenvManagerDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(VirtualenvManagerDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.venvList = QtWidgets.QTreeWidget(VirtualenvManagerDialog)
        self.venvList.setAlternatingRowColors(True)
        self.venvList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.venvList.setRootIsDecorated(False)
        self.venvList.setItemsExpandable(False)
        self.venvList.setAllColumnsShowFocus(True)
        self.venvList.setObjectName("venvList")
        self.gridLayout.addWidget(self.venvList, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.addButton.setAutoDefault(False)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.newButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.newButton.setAutoDefault(False)
        self.newButton.setObjectName("newButton")
        self.verticalLayout.addWidget(self.newButton)
        self.line_6 = QtWidgets.QFrame(VirtualenvManagerDialog)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout.addWidget(self.line_6)
        self.editButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.editButton.setObjectName("editButton")
        self.verticalLayout.addWidget(self.editButton)
        self.line_3 = QtWidgets.QFrame(VirtualenvManagerDialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.removeButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.removeButton.setAutoDefault(False)
        self.removeButton.setObjectName("removeButton")
        self.verticalLayout.addWidget(self.removeButton)
        self.removeAllButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.removeAllButton.setAutoDefault(False)
        self.removeAllButton.setObjectName("removeAllButton")
        self.verticalLayout.addWidget(self.removeAllButton)
        self.line_4 = QtWidgets.QFrame(VirtualenvManagerDialog)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.deleteButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.deleteButton.setAutoDefault(False)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        self.deleteAllButton = QtWidgets.QPushButton(VirtualenvManagerDialog)
        self.deleteAllButton.setAutoDefault(False)
        self.deleteAllButton.setObjectName("deleteAllButton")
        self.verticalLayout.addWidget(self.deleteAllButton)
        spacerItem = QtWidgets.QSpacerItem(20, 228, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(VirtualenvManagerDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.envBaseDirectoryPicker = E5PathPicker(VirtualenvManagerDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.envBaseDirectoryPicker.sizePolicy().hasHeightForWidth())
        self.envBaseDirectoryPicker.setSizePolicy(sizePolicy)
        self.envBaseDirectoryPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.envBaseDirectoryPicker.setObjectName("envBaseDirectoryPicker")
        self.horizontalLayout.addWidget(self.envBaseDirectoryPicker)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(VirtualenvManagerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(VirtualenvManagerDialog)
        self.buttonBox.accepted.connect(VirtualenvManagerDialog.accept)
        self.buttonBox.rejected.connect(VirtualenvManagerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VirtualenvManagerDialog)
        VirtualenvManagerDialog.setTabOrder(self.venvList, self.addButton)
        VirtualenvManagerDialog.setTabOrder(self.addButton, self.newButton)
        VirtualenvManagerDialog.setTabOrder(self.newButton, self.editButton)
        VirtualenvManagerDialog.setTabOrder(self.editButton, self.removeButton)
        VirtualenvManagerDialog.setTabOrder(self.removeButton, self.removeAllButton)
        VirtualenvManagerDialog.setTabOrder(self.removeAllButton, self.deleteButton)
        VirtualenvManagerDialog.setTabOrder(self.deleteButton, self.deleteAllButton)

    def retranslateUi(self, VirtualenvManagerDialog):
        _translate = QtCore.QCoreApplication.translate
        VirtualenvManagerDialog.setWindowTitle(_translate("VirtualenvManagerDialog", "Manage Virtual Environments"))
        self.venvList.setSortingEnabled(True)
        self.venvList.headerItem().setText(0, _translate("VirtualenvManagerDialog", "Name"))
        self.venvList.headerItem().setText(1, _translate("VirtualenvManagerDialog", "Directory"))
        self.venvList.headerItem().setText(2, _translate("VirtualenvManagerDialog", "Interpreter"))
        self.addButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to add an existing virtual environment"))
        self.addButton.setText(_translate("VirtualenvManagerDialog", "Add..."))
        self.newButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to create a new virtual environment"))
        self.newButton.setText(_translate("VirtualenvManagerDialog", "New..."))
        self.editButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to edit the selected virtual environment"))
        self.editButton.setText(_translate("VirtualenvManagerDialog", "Edit..."))
        self.removeButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to remove the selected virtual environments"))
        self.removeButton.setText(_translate("VirtualenvManagerDialog", "Remove"))
        self.removeAllButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to remove all virtual environments"))
        self.removeAllButton.setText(_translate("VirtualenvManagerDialog", "Remove All"))
        self.deleteButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to remove the selected virtual environments and delete them"))
        self.deleteButton.setText(_translate("VirtualenvManagerDialog", "Delete"))
        self.deleteAllButton.setToolTip(_translate("VirtualenvManagerDialog", "Press to remove all virtual environments and delete them"))
        self.deleteAllButton.setText(_translate("VirtualenvManagerDialog", "Delete All"))
        self.label_2.setText(_translate("VirtualenvManagerDialog", "Base Directory:"))
        self.envBaseDirectoryPicker.setToolTip(_translate("VirtualenvManagerDialog", "Enter the base directory of the virtual environments"))
from E5Gui.E5PathPicker import E5PathPicker
