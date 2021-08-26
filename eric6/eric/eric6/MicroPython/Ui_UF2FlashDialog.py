# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\MicroPython\UF2FlashDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UF2FlashDialog(object):
    def setupUi(self, UF2FlashDialog):
        UF2FlashDialog.setObjectName("UF2FlashDialog")
        UF2FlashDialog.resize(600, 600)
        UF2FlashDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(UF2FlashDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(UF2FlashDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.devicesComboBox = QtWidgets.QComboBox(UF2FlashDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesComboBox.sizePolicy().hasHeightForWidth())
        self.devicesComboBox.setSizePolicy(sizePolicy)
        self.devicesComboBox.setObjectName("devicesComboBox")
        self.gridLayout.addWidget(self.devicesComboBox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(UF2FlashDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.firmwarePicker = E5PathPicker(UF2FlashDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firmwarePicker.sizePolicy().hasHeightForWidth())
        self.firmwarePicker.setSizePolicy(sizePolicy)
        self.firmwarePicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.firmwarePicker.setObjectName("firmwarePicker")
        self.gridLayout.addWidget(self.firmwarePicker, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(UF2FlashDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.bootPicker = E5PathPicker(UF2FlashDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bootPicker.sizePolicy().hasHeightForWidth())
        self.bootPicker.setSizePolicy(sizePolicy)
        self.bootPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.bootPicker.setObjectName("bootPicker")
        self.gridLayout.addWidget(self.bootPicker, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.flashButton = QtWidgets.QPushButton(UF2FlashDialog)
        self.flashButton.setObjectName("flashButton")
        self.verticalLayout_2.addWidget(self.flashButton)
        self.infoFrame = QtWidgets.QFrame(UF2FlashDialog)
        self.infoFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.infoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.infoFrame.setObjectName("infoFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.infoFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.infoLabel = QtWidgets.QLabel(self.infoFrame)
        self.infoLabel.setText("")
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.infoEdit = QtWidgets.QTextEdit(self.infoFrame)
        self.infoEdit.setReadOnly(False)
        self.infoEdit.setObjectName("infoEdit")
        self.verticalLayout.addWidget(self.infoEdit)
        self.verticalLayout_2.addWidget(self.infoFrame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refreshButton = QtWidgets.QPushButton(UF2FlashDialog)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(UF2FlashDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(UF2FlashDialog)
        self.buttonBox.accepted.connect(UF2FlashDialog.accept)
        self.buttonBox.rejected.connect(UF2FlashDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UF2FlashDialog)
        UF2FlashDialog.setTabOrder(self.devicesComboBox, self.firmwarePicker)
        UF2FlashDialog.setTabOrder(self.firmwarePicker, self.bootPicker)
        UF2FlashDialog.setTabOrder(self.bootPicker, self.flashButton)
        UF2FlashDialog.setTabOrder(self.flashButton, self.infoEdit)
        UF2FlashDialog.setTabOrder(self.infoEdit, self.refreshButton)

    def retranslateUi(self, UF2FlashDialog):
        _translate = QtCore.QCoreApplication.translate
        UF2FlashDialog.setWindowTitle(_translate("UF2FlashDialog", "Flash UF2 Device"))
        self.label.setText(_translate("UF2FlashDialog", "Detected Devices:"))
        self.devicesComboBox.setToolTip(_translate("UF2FlashDialog", "Select the device to be flashed"))
        self.label_3.setText(_translate("UF2FlashDialog", "MicroPython:"))
        self.firmwarePicker.setToolTip(_translate("UF2FlashDialog", "Enter the path of the MicroPython / CircuitPython firmware file"))
        self.label_2.setText(_translate("UF2FlashDialog", "\'Boot\' Path:"))
        self.bootPicker.setToolTip(_translate("UF2FlashDialog", "Enter the path of the bootloader volume"))
        self.flashButton.setText(_translate("UF2FlashDialog", "Flash MicroPython / CircuitPython"))
        self.refreshButton.setText(_translate("UF2FlashDialog", "Refresh"))
from E5Gui.E5PathPicker import E5PathPicker