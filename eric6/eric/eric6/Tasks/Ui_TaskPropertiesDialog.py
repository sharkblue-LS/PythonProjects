# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Tasks\TaskPropertiesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TaskPropertiesDialog(object):
    def setupUi(self, TaskPropertiesDialog):
        TaskPropertiesDialog.setObjectName("TaskPropertiesDialog")
        TaskPropertiesDialog.resize(579, 297)
        TaskPropertiesDialog.setSizeGripEnabled(True)
        self.gridlayout = QtWidgets.QGridLayout(TaskPropertiesDialog)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtWidgets.QLabel(TaskPropertiesDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.summaryEdit = QtWidgets.QLineEdit(TaskPropertiesDialog)
        self.summaryEdit.setObjectName("summaryEdit")
        self.gridlayout.addWidget(self.summaryEdit, 0, 1, 1, 3)
        self.textLabel1 = QtWidgets.QLabel(TaskPropertiesDialog)
        self.textLabel1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.textLabel1.setObjectName("textLabel1")
        self.gridlayout.addWidget(self.textLabel1, 1, 0, 1, 1)
        self.descriptionEdit = QtWidgets.QTextEdit(TaskPropertiesDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridlayout.addWidget(self.descriptionEdit, 1, 1, 1, 3)
        self.textLabel2 = QtWidgets.QLabel(TaskPropertiesDialog)
        self.textLabel2.setObjectName("textLabel2")
        self.gridlayout.addWidget(self.textLabel2, 2, 0, 1, 1)
        self.creationLabel = QtWidgets.QLabel(TaskPropertiesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creationLabel.sizePolicy().hasHeightForWidth())
        self.creationLabel.setSizePolicy(sizePolicy)
        self.creationLabel.setObjectName("creationLabel")
        self.gridlayout.addWidget(self.creationLabel, 2, 1, 1, 3)
        self.textLabel4 = QtWidgets.QLabel(TaskPropertiesDialog)
        self.textLabel4.setObjectName("textLabel4")
        self.gridlayout.addWidget(self.textLabel4, 3, 0, 1, 1)
        self.priorityCombo = QtWidgets.QComboBox(TaskPropertiesDialog)
        self.priorityCombo.setObjectName("priorityCombo")
        self.priorityCombo.addItem("")
        self.priorityCombo.addItem("")
        self.priorityCombo.addItem("")
        self.gridlayout.addWidget(self.priorityCombo, 3, 1, 1, 1)
        self.projectCheckBox = QtWidgets.QCheckBox(TaskPropertiesDialog)
        self.projectCheckBox.setObjectName("projectCheckBox")
        self.gridlayout.addWidget(self.projectCheckBox, 3, 2, 1, 1)
        self.completedCheckBox = QtWidgets.QCheckBox(TaskPropertiesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.completedCheckBox.sizePolicy().hasHeightForWidth())
        self.completedCheckBox.setSizePolicy(sizePolicy)
        self.completedCheckBox.setObjectName("completedCheckBox")
        self.gridlayout.addWidget(self.completedCheckBox, 3, 3, 1, 1)
        self.textLabel5 = QtWidgets.QLabel(TaskPropertiesDialog)
        self.textLabel5.setObjectName("textLabel5")
        self.gridlayout.addWidget(self.textLabel5, 4, 0, 1, 1)
        self.filenameEdit = QtWidgets.QLineEdit(TaskPropertiesDialog)
        self.filenameEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.filenameEdit.setReadOnly(True)
        self.filenameEdit.setObjectName("filenameEdit")
        self.gridlayout.addWidget(self.filenameEdit, 4, 1, 1, 3)
        self.textLabel6 = QtWidgets.QLabel(TaskPropertiesDialog)
        self.textLabel6.setObjectName("textLabel6")
        self.gridlayout.addWidget(self.textLabel6, 5, 0, 1, 1)
        self.linenoEdit = QtWidgets.QLineEdit(TaskPropertiesDialog)
        self.linenoEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.linenoEdit.setReadOnly(True)
        self.linenoEdit.setObjectName("linenoEdit")
        self.gridlayout.addWidget(self.linenoEdit, 5, 1, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(TaskPropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 6, 0, 1, 4)
        self.label.setBuddy(self.summaryEdit)
        self.textLabel1.setBuddy(self.descriptionEdit)
        self.textLabel4.setBuddy(self.priorityCombo)

        self.retranslateUi(TaskPropertiesDialog)
        self.priorityCombo.setCurrentIndex(1)
        self.buttonBox.accepted.connect(TaskPropertiesDialog.accept)
        self.buttonBox.rejected.connect(TaskPropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TaskPropertiesDialog)
        TaskPropertiesDialog.setTabOrder(self.summaryEdit, self.descriptionEdit)
        TaskPropertiesDialog.setTabOrder(self.descriptionEdit, self.priorityCombo)
        TaskPropertiesDialog.setTabOrder(self.priorityCombo, self.projectCheckBox)
        TaskPropertiesDialog.setTabOrder(self.projectCheckBox, self.completedCheckBox)
        TaskPropertiesDialog.setTabOrder(self.completedCheckBox, self.buttonBox)

    def retranslateUi(self, TaskPropertiesDialog):
        _translate = QtCore.QCoreApplication.translate
        TaskPropertiesDialog.setWindowTitle(_translate("TaskPropertiesDialog", "Task Properties"))
        self.label.setText(_translate("TaskPropertiesDialog", "&Summary:"))
        self.summaryEdit.setToolTip(_translate("TaskPropertiesDialog", "Enter the task summary"))
        self.textLabel1.setText(_translate("TaskPropertiesDialog", "&Description:"))
        self.descriptionEdit.setToolTip(_translate("TaskPropertiesDialog", "Enter the task description"))
        self.textLabel2.setText(_translate("TaskPropertiesDialog", "Creation Time:"))
        self.textLabel4.setText(_translate("TaskPropertiesDialog", "&Priority:"))
        self.priorityCombo.setToolTip(_translate("TaskPropertiesDialog", "Select the task priority"))
        self.priorityCombo.setItemText(0, _translate("TaskPropertiesDialog", "High"))
        self.priorityCombo.setItemText(1, _translate("TaskPropertiesDialog", "Normal"))
        self.priorityCombo.setItemText(2, _translate("TaskPropertiesDialog", "Low"))
        self.projectCheckBox.setToolTip(_translate("TaskPropertiesDialog", "Select to indicate a task related to the current project"))
        self.projectCheckBox.setText(_translate("TaskPropertiesDialog", "Project &Task"))
        self.completedCheckBox.setToolTip(_translate("TaskPropertiesDialog", "Select to mark this task as completed"))
        self.completedCheckBox.setText(_translate("TaskPropertiesDialog", "T&ask completed"))
        self.textLabel5.setText(_translate("TaskPropertiesDialog", "Filename:"))
        self.textLabel6.setText(_translate("TaskPropertiesDialog", "Line:"))
