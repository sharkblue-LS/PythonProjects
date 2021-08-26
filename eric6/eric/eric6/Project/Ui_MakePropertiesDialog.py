# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Project\MakePropertiesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MakePropertiesDialog(object):
    def setupUi(self, MakePropertiesDialog):
        MakePropertiesDialog.setObjectName("MakePropertiesDialog")
        MakePropertiesDialog.resize(600, 266)
        MakePropertiesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(MakePropertiesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MakePropertiesDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.makePicker = E5PathPicker(MakePropertiesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.makePicker.sizePolicy().hasHeightForWidth())
        self.makePicker.setSizePolicy(sizePolicy)
        self.makePicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.makePicker.setObjectName("makePicker")
        self.verticalLayout.addWidget(self.makePicker)
        self.label_2 = QtWidgets.QLabel(MakePropertiesDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.makefilePicker = E5PathPicker(MakePropertiesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.makefilePicker.sizePolicy().hasHeightForWidth())
        self.makefilePicker.setSizePolicy(sizePolicy)
        self.makefilePicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.makefilePicker.setObjectName("makefilePicker")
        self.verticalLayout.addWidget(self.makefilePicker)
        self.label_3 = QtWidgets.QLabel(MakePropertiesDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.makeTargetEdit = E5ClearableLineEdit(MakePropertiesDialog)
        self.makeTargetEdit.setObjectName("makeTargetEdit")
        self.verticalLayout.addWidget(self.makeTargetEdit)
        self.label_4 = QtWidgets.QLabel(MakePropertiesDialog)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.makeParametersEdit = E5ClearableLineEdit(MakePropertiesDialog)
        self.makeParametersEdit.setObjectName("makeParametersEdit")
        self.verticalLayout.addWidget(self.makeParametersEdit)
        self.testOnlyCheckBox = QtWidgets.QCheckBox(MakePropertiesDialog)
        self.testOnlyCheckBox.setObjectName("testOnlyCheckBox")
        self.verticalLayout.addWidget(self.testOnlyCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(MakePropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MakePropertiesDialog)
        self.buttonBox.accepted.connect(MakePropertiesDialog.accept)
        self.buttonBox.rejected.connect(MakePropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MakePropertiesDialog)

    def retranslateUi(self, MakePropertiesDialog):
        _translate = QtCore.QCoreApplication.translate
        MakePropertiesDialog.setWindowTitle(_translate("MakePropertiesDialog", "Make Properties"))
        self.label.setText(_translate("MakePropertiesDialog", "\'make\' Executable (leave empty to use global \'make\'):"))
        self.makePicker.setToolTip(_translate("MakePropertiesDialog", "Enter the executable name of the make utility"))
        self.label_2.setText(_translate("MakePropertiesDialog", "\'makefile\' path or directory (without file name \'makefile\' will be used):"))
        self.makefilePicker.setToolTip(_translate("MakePropertiesDialog", "Enter the name and/or path of the makefile"))
        self.label_3.setText(_translate("MakePropertiesDialog", "Make Target:"))
        self.makeTargetEdit.setToolTip(_translate("MakePropertiesDialog", "Enter the make target to be built"))
        self.label_4.setText(_translate("MakePropertiesDialog", "Make Command Parameters (enclose parameters containing spaces in \"\"):"))
        self.makeParametersEdit.setToolTip(_translate("MakePropertiesDialog", "Enter the command parameters for make"))
        self.testOnlyCheckBox.setToolTip(_translate("MakePropertiesDialog", "Select to just test for changes needing a make run"))
        self.testOnlyCheckBox.setText(_translate("MakePropertiesDialog", "Test for changes only when run automatically"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
from E5Gui.E5PathPicker import E5PathPicker