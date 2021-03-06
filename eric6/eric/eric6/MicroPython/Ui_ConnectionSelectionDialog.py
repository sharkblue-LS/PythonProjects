# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\MicroPython\ConnectionSelectionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectionSelectionDialog(object):
    def setupUi(self, ConnectionSelectionDialog):
        ConnectionSelectionDialog.setObjectName("ConnectionSelectionDialog")
        ConnectionSelectionDialog.resize(400, 108)
        ConnectionSelectionDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(ConnectionSelectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ConnectionSelectionDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.portNameComboBox = QtWidgets.QComboBox(ConnectionSelectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portNameComboBox.sizePolicy().hasHeightForWidth())
        self.portNameComboBox.setSizePolicy(sizePolicy)
        self.portNameComboBox.setObjectName("portNameComboBox")
        self.gridLayout.addWidget(self.portNameComboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(ConnectionSelectionDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.deviceTypeComboBox = QtWidgets.QComboBox(ConnectionSelectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.deviceTypeComboBox.setSizePolicy(sizePolicy)
        self.deviceTypeComboBox.setObjectName("deviceTypeComboBox")
        self.gridLayout.addWidget(self.deviceTypeComboBox, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConnectionSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(ConnectionSelectionDialog)
        self.buttonBox.accepted.connect(ConnectionSelectionDialog.accept)
        self.buttonBox.rejected.connect(ConnectionSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConnectionSelectionDialog)

    def retranslateUi(self, ConnectionSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionSelectionDialog.setWindowTitle(_translate("ConnectionSelectionDialog", "Port and Device Type Selection"))
        self.label.setText(_translate("ConnectionSelectionDialog", "Serial Port Name:"))
        self.portNameComboBox.setToolTip(_translate("ConnectionSelectionDialog", "Select the serial port name to connect"))
        self.label_2.setText(_translate("ConnectionSelectionDialog", "Device Type:"))
        self.deviceTypeComboBox.setToolTip(_translate("ConnectionSelectionDialog", "Select the device type"))
