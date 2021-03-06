# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\MicroPython\EspBackupRestoreFirmwareDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EspBackupRestoreFirmwareDialog(object):
    def setupUi(self, EspBackupRestoreFirmwareDialog):
        EspBackupRestoreFirmwareDialog.setObjectName("EspBackupRestoreFirmwareDialog")
        EspBackupRestoreFirmwareDialog.resize(500, 166)
        EspBackupRestoreFirmwareDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EspBackupRestoreFirmwareDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(EspBackupRestoreFirmwareDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.espComboBox = QtWidgets.QComboBox(EspBackupRestoreFirmwareDialog)
        self.espComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.espComboBox.setObjectName("espComboBox")
        self.gridLayout.addWidget(self.espComboBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(268, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(EspBackupRestoreFirmwareDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.sizeComboBox = QtWidgets.QComboBox(EspBackupRestoreFirmwareDialog)
        self.sizeComboBox.setObjectName("sizeComboBox")
        self.gridLayout.addWidget(self.sizeComboBox, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(EspBackupRestoreFirmwareDialog)
        self.label_3.setToolTip("")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.modeComboBox = QtWidgets.QComboBox(EspBackupRestoreFirmwareDialog)
        self.modeComboBox.setObjectName("modeComboBox")
        self.gridLayout.addWidget(self.modeComboBox, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(EspBackupRestoreFirmwareDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.firmwarePicker = E5PathPicker(EspBackupRestoreFirmwareDialog)
        self.firmwarePicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.firmwarePicker.setObjectName("firmwarePicker")
        self.gridLayout.addWidget(self.firmwarePicker, 3, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(EspBackupRestoreFirmwareDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EspBackupRestoreFirmwareDialog)
        self.buttonBox.accepted.connect(EspBackupRestoreFirmwareDialog.accept)
        self.buttonBox.rejected.connect(EspBackupRestoreFirmwareDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EspBackupRestoreFirmwareDialog)

    def retranslateUi(self, EspBackupRestoreFirmwareDialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("EspBackupRestoreFirmwareDialog", "ESP Chip Type:"))
        self.espComboBox.setToolTip(_translate("EspBackupRestoreFirmwareDialog", "Select the ESP chip type"))
        self.label_2.setText(_translate("EspBackupRestoreFirmwareDialog", "Firmware Size:"))
        self.sizeComboBox.setToolTip(_translate("EspBackupRestoreFirmwareDialog", "Select the firmware size"))
        self.label_3.setText(_translate("EspBackupRestoreFirmwareDialog", "Flashmode:"))
        self.modeComboBox.setToolTip(_translate("EspBackupRestoreFirmwareDialog", "Select the flash mode"))
        self.label_4.setText(_translate("EspBackupRestoreFirmwareDialog", "Firmware:"))
        self.firmwarePicker.setToolTip(_translate("EspBackupRestoreFirmwareDialog", "Enter the path of the firmware file"))
from E5Gui.E5PathPicker import E5PathPicker
