# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Project\IdlCompilerOptionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IdlCompilerOptionsDialog(object):
    def setupUi(self, IdlCompilerOptionsDialog):
        IdlCompilerOptionsDialog.setObjectName("IdlCompilerOptionsDialog")
        IdlCompilerOptionsDialog.resize(450, 600)
        IdlCompilerOptionsDialog.setSizeGripEnabled(True)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(IdlCompilerOptionsDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.includeDirectoriesGroup = QtWidgets.QGroupBox(IdlCompilerOptionsDialog)
        self.includeDirectoriesGroup.setObjectName("includeDirectoriesGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.includeDirectoriesGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.idList = QtWidgets.QListWidget(self.includeDirectoriesGroup)
        self.idList.setAlternatingRowColors(True)
        self.idList.setObjectName("idList")
        self.horizontalLayout.addWidget(self.idList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.idAddButton = QtWidgets.QToolButton(self.includeDirectoriesGroup)
        self.idAddButton.setObjectName("idAddButton")
        self.verticalLayout.addWidget(self.idAddButton)
        self.idDeleteButton = QtWidgets.QToolButton(self.includeDirectoriesGroup)
        self.idDeleteButton.setObjectName("idDeleteButton")
        self.verticalLayout.addWidget(self.idDeleteButton)
        self.idEditButton = QtWidgets.QToolButton(self.includeDirectoriesGroup)
        self.idEditButton.setObjectName("idEditButton")
        self.verticalLayout.addWidget(self.idEditButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4.addWidget(self.includeDirectoriesGroup)
        self.groupBox = QtWidgets.QGroupBox(IdlCompilerOptionsDialog)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dnList = QtWidgets.QTreeWidget(self.groupBox)
        self.dnList.setAlternatingRowColors(True)
        self.dnList.setRootIsDecorated(False)
        self.dnList.setItemsExpandable(False)
        self.dnList.setAllColumnsShowFocus(True)
        self.dnList.setObjectName("dnList")
        self.dnList.header().setDefaultSectionSize(150)
        self.dnList.header().setSortIndicatorShown(False)
        self.horizontalLayout_2.addWidget(self.dnList)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dnAddButton = QtWidgets.QToolButton(self.groupBox)
        self.dnAddButton.setObjectName("dnAddButton")
        self.verticalLayout_2.addWidget(self.dnAddButton)
        self.dnDeleteButton = QtWidgets.QToolButton(self.groupBox)
        self.dnDeleteButton.setObjectName("dnDeleteButton")
        self.verticalLayout_2.addWidget(self.dnDeleteButton)
        self.dnEditButton = QtWidgets.QToolButton(self.groupBox)
        self.dnEditButton.setObjectName("dnEditButton")
        self.verticalLayout_2.addWidget(self.dnEditButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(IdlCompilerOptionsDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.unList = QtWidgets.QListWidget(self.groupBox_2)
        self.unList.setAlternatingRowColors(True)
        self.unList.setObjectName("unList")
        self.horizontalLayout_3.addWidget(self.unList)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.unAddButton = QtWidgets.QToolButton(self.groupBox_2)
        self.unAddButton.setObjectName("unAddButton")
        self.verticalLayout_3.addWidget(self.unAddButton)
        self.unDeleteButton = QtWidgets.QToolButton(self.groupBox_2)
        self.unDeleteButton.setObjectName("unDeleteButton")
        self.verticalLayout_3.addWidget(self.unDeleteButton)
        self.unEditButton = QtWidgets.QToolButton(self.groupBox_2)
        self.unEditButton.setObjectName("unEditButton")
        self.verticalLayout_3.addWidget(self.unEditButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(IdlCompilerOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(IdlCompilerOptionsDialog)
        self.buttonBox.accepted.connect(IdlCompilerOptionsDialog.accept)
        self.buttonBox.rejected.connect(IdlCompilerOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IdlCompilerOptionsDialog)
        IdlCompilerOptionsDialog.setTabOrder(self.idList, self.idAddButton)
        IdlCompilerOptionsDialog.setTabOrder(self.idAddButton, self.idDeleteButton)
        IdlCompilerOptionsDialog.setTabOrder(self.idDeleteButton, self.idEditButton)
        IdlCompilerOptionsDialog.setTabOrder(self.idEditButton, self.dnList)
        IdlCompilerOptionsDialog.setTabOrder(self.dnList, self.dnAddButton)
        IdlCompilerOptionsDialog.setTabOrder(self.dnAddButton, self.dnDeleteButton)
        IdlCompilerOptionsDialog.setTabOrder(self.dnDeleteButton, self.dnEditButton)
        IdlCompilerOptionsDialog.setTabOrder(self.dnEditButton, self.unList)
        IdlCompilerOptionsDialog.setTabOrder(self.unList, self.unAddButton)
        IdlCompilerOptionsDialog.setTabOrder(self.unAddButton, self.unDeleteButton)
        IdlCompilerOptionsDialog.setTabOrder(self.unDeleteButton, self.unEditButton)

    def retranslateUi(self, IdlCompilerOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        IdlCompilerOptionsDialog.setWindowTitle(_translate("IdlCompilerOptionsDialog", "IDL Compiler Options"))
        self.includeDirectoriesGroup.setTitle(_translate("IdlCompilerOptionsDialog", "Include Directories (absolute or project relative)"))
        self.idList.setSortingEnabled(True)
        self.idAddButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Add an include directory"))
        self.idDeleteButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Delete an include directory"))
        self.idEditButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Edit an include directory"))
        self.groupBox.setTitle(_translate("IdlCompilerOptionsDialog", "Define Names"))
        self.dnList.setSortingEnabled(False)
        self.dnList.headerItem().setText(0, _translate("IdlCompilerOptionsDialog", "Name"))
        self.dnList.headerItem().setText(1, _translate("IdlCompilerOptionsDialog", "Value"))
        self.dnList.headerItem().setText(2, _translate("IdlCompilerOptionsDialog", " "))
        self.dnAddButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Add a name entry"))
        self.dnDeleteButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Delete a name entry"))
        self.dnEditButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Edit a name entry"))
        self.groupBox_2.setTitle(_translate("IdlCompilerOptionsDialog", "Undefine Names"))
        self.unList.setSortingEnabled(True)
        self.unAddButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Add a name entry"))
        self.unDeleteButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Delete a name entry"))
        self.unEditButton.setToolTip(_translate("IdlCompilerOptionsDialog", "Edit a name entry"))
