# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Project\RccCompilerOptionsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RccCompilerOptionsDialog(object):
    def setupUi(self, RccCompilerOptionsDialog):
        RccCompilerOptionsDialog.setObjectName("RccCompilerOptionsDialog")
        RccCompilerOptionsDialog.resize(500, 219)
        RccCompilerOptionsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(RccCompilerOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(RccCompilerOptionsDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.thresholdSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.thresholdSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.thresholdSpinBox.setSpecialValueText("")
        self.thresholdSpinBox.setMinimum(0)
        self.thresholdSpinBox.setMaximum(100)
        self.thresholdSpinBox.setSingleStep(5)
        self.thresholdSpinBox.setProperty("value", 70)
        self.thresholdSpinBox.setObjectName("thresholdSpinBox")
        self.gridLayout.addWidget(self.thresholdSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(253, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.compressionSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.compressionSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.compressionSpinBox.setMinimum(0)
        self.compressionSpinBox.setMaximum(9)
        self.compressionSpinBox.setObjectName("compressionSpinBox")
        self.gridLayout.addWidget(self.compressionSpinBox, 1, 1, 1, 1)
        self.disableCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.disableCheckBox.setObjectName("disableCheckBox")
        self.gridLayout.addWidget(self.disableCheckBox, 2, 0, 1, 2)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(RccCompilerOptionsDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.rootEdit = E5ClearableLineEdit(RccCompilerOptionsDialog)
        self.rootEdit.setObjectName("rootEdit")
        self.horizontalLayout.addWidget(self.rootEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(RccCompilerOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RccCompilerOptionsDialog)
        self.buttonBox.accepted.connect(RccCompilerOptionsDialog.accept)
        self.buttonBox.rejected.connect(RccCompilerOptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RccCompilerOptionsDialog)
        RccCompilerOptionsDialog.setTabOrder(self.thresholdSpinBox, self.compressionSpinBox)
        RccCompilerOptionsDialog.setTabOrder(self.compressionSpinBox, self.disableCheckBox)
        RccCompilerOptionsDialog.setTabOrder(self.disableCheckBox, self.rootEdit)

    def retranslateUi(self, RccCompilerOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        RccCompilerOptionsDialog.setWindowTitle(_translate("RccCompilerOptionsDialog", "rcc Compiler Options"))
        self.groupBox.setTitle(_translate("RccCompilerOptionsDialog", "Compression Parameters"))
        self.label_2.setText(_translate("RccCompilerOptionsDialog", "Threshold:"))
        self.thresholdSpinBox.setToolTip(_translate("RccCompilerOptionsDialog", "Select the compression threshold (default: 70%)"))
        self.thresholdSpinBox.setSuffix(_translate("RccCompilerOptionsDialog", "%"))
        self.label_3.setText(_translate("RccCompilerOptionsDialog", "Compression Level:"))
        self.compressionSpinBox.setToolTip(_translate("RccCompilerOptionsDialog", "Select the compression level (default: use zlib default value)"))
        self.compressionSpinBox.setSpecialValueText(_translate("RccCompilerOptionsDialog", "default"))
        self.disableCheckBox.setText(_translate("RccCompilerOptionsDialog", "Disable Compression"))
        self.label.setText(_translate("RccCompilerOptionsDialog", "Access Path Prefix:"))
        self.rootEdit.setToolTip(_translate("RccCompilerOptionsDialog", "Enter the prefix for the resource access path"))
from E5Gui.E5LineEdit import E5ClearableLineEdit