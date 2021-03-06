# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\CondaInterface\CondaInfoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CondaInfoDialog(object):
    def setupUi(self, CondaInfoDialog):
        CondaInfoDialog.setObjectName("CondaInfoDialog")
        CondaInfoDialog.resize(650, 746)
        CondaInfoDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CondaInfoDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.iconLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.iconLabel.setText("icon")
        self.iconLabel.setObjectName("iconLabel")
        self.horizontalLayout.addWidget(self.iconLabel)
        self.label = QtWidgets.QLabel(CondaInfoDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.condaVersionLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.condaVersionLabel.setObjectName("condaVersionLabel")
        self.gridLayout.addWidget(self.condaVersionLabel, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.condaBuildVersionLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.condaBuildVersionLabel.setObjectName("condaBuildVersionLabel")
        self.gridLayout.addWidget(self.condaBuildVersionLabel, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.pythonVersionLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.pythonVersionLabel.setObjectName("pythonVersionLabel")
        self.gridLayout.addWidget(self.pythonVersionLabel, 3, 1, 1, 1)
        self.activeEnvironmentLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.activeEnvironmentLabel.setObjectName("activeEnvironmentLabel")
        self.gridLayout.addWidget(self.activeEnvironmentLabel, 4, 0, 1, 1)
        self.activeEnvironmentEdit = QtWidgets.QLineEdit(CondaInfoDialog)
        self.activeEnvironmentEdit.setObjectName("activeEnvironmentEdit")
        self.gridLayout.addWidget(self.activeEnvironmentEdit, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.userConfigEdit = QtWidgets.QLineEdit(CondaInfoDialog)
        self.userConfigEdit.setObjectName("userConfigEdit")
        self.gridLayout.addWidget(self.userConfigEdit, 5, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 6, 0, 1, 1)
        self.systemConfigEdit = QtWidgets.QLineEdit(CondaInfoDialog)
        self.systemConfigEdit.setObjectName("systemConfigEdit")
        self.gridLayout.addWidget(self.systemConfigEdit, 6, 1, 1, 1)
        self.configurationsLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.configurationsLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.configurationsLabel.setObjectName("configurationsLabel")
        self.gridLayout.addWidget(self.configurationsLabel, 7, 0, 1, 1)
        self.configurationsEdit = QtWidgets.QPlainTextEdit(CondaInfoDialog)
        self.configurationsEdit.setObjectName("configurationsEdit")
        self.gridLayout.addWidget(self.configurationsEdit, 7, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)
        self.baseEnvironmentEdit = QtWidgets.QLineEdit(CondaInfoDialog)
        self.baseEnvironmentEdit.setObjectName("baseEnvironmentEdit")
        self.gridLayout.addWidget(self.baseEnvironmentEdit, 8, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)
        self.channelsEdit = QtWidgets.QPlainTextEdit(CondaInfoDialog)
        self.channelsEdit.setObjectName("channelsEdit")
        self.gridLayout.addWidget(self.channelsEdit, 9, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 10, 0, 1, 1)
        self.cachesEdit = QtWidgets.QPlainTextEdit(CondaInfoDialog)
        self.cachesEdit.setObjectName("cachesEdit")
        self.gridLayout.addWidget(self.cachesEdit, 10, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 11, 0, 1, 1)
        self.envDirsEdit = QtWidgets.QPlainTextEdit(CondaInfoDialog)
        self.envDirsEdit.setObjectName("envDirsEdit")
        self.gridLayout.addWidget(self.envDirsEdit, 11, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 12, 0, 1, 1)
        self.platformLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.platformLabel.setObjectName("platformLabel")
        self.gridLayout.addWidget(self.platformLabel, 12, 1, 1, 1)
        self.useragentLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.useragentLabel.setObjectName("useragentLabel")
        self.gridLayout.addWidget(self.useragentLabel, 13, 0, 1, 1)
        self.useragentEdit = QtWidgets.QLineEdit(CondaInfoDialog)
        self.useragentEdit.setObjectName("useragentEdit")
        self.gridLayout.addWidget(self.useragentEdit, 13, 1, 1, 1)
        self.uidGidLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.uidGidLabel.setObjectName("uidGidLabel")
        self.gridLayout.addWidget(self.uidGidLabel, 14, 0, 1, 1)
        self.uidGidDataLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.uidGidDataLabel.setObjectName("uidGidDataLabel")
        self.gridLayout.addWidget(self.uidGidDataLabel, 14, 1, 1, 1)
        self.netrcLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.netrcLabel.setObjectName("netrcLabel")
        self.gridLayout.addWidget(self.netrcLabel, 15, 0, 1, 1)
        self.netrcEdit = QtWidgets.QLineEdit(CondaInfoDialog)
        self.netrcEdit.setObjectName("netrcEdit")
        self.gridLayout.addWidget(self.netrcEdit, 15, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 16, 0, 1, 1)
        self.offlineCheckBox = QtWidgets.QCheckBox(CondaInfoDialog)
        self.offlineCheckBox.setText("")
        self.offlineCheckBox.setObjectName("offlineCheckBox")
        self.gridLayout.addWidget(self.offlineCheckBox, 16, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(CondaInfoDialog)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 0, 1, 1)
        self.condaEnvVersionLabel = QtWidgets.QLabel(CondaInfoDialog)
        self.condaEnvVersionLabel.setObjectName("condaEnvVersionLabel")
        self.gridLayout.addWidget(self.condaEnvVersionLabel, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(CondaInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CondaInfoDialog)
        self.buttonBox.accepted.connect(CondaInfoDialog.accept)
        self.buttonBox.rejected.connect(CondaInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CondaInfoDialog)

    def retranslateUi(self, CondaInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        CondaInfoDialog.setWindowTitle(_translate("CondaInfoDialog", "Conda Information"))
        self.label.setText(_translate("CondaInfoDialog", "<h2>Conda Information</h2>"))
        self.label_3.setText(_translate("CondaInfoDialog", "conda Version:"))
        self.label_4.setText(_translate("CondaInfoDialog", "conda-build Version:"))
        self.label_5.setText(_translate("CondaInfoDialog", "python Version:"))
        self.activeEnvironmentLabel.setText(_translate("CondaInfoDialog", "Active Environment:"))
        self.label_6.setText(_translate("CondaInfoDialog", "User Configuration:"))
        self.label_17.setText(_translate("CondaInfoDialog", "System Configuration:"))
        self.configurationsLabel.setText(_translate("CondaInfoDialog", "Populated Configurations:"))
        self.label_8.setText(_translate("CondaInfoDialog", "Base Environment:"))
        self.label_9.setText(_translate("CondaInfoDialog", "Channel URLs:"))
        self.label_10.setText(_translate("CondaInfoDialog", "Package Cache:"))
        self.label_11.setText(_translate("CondaInfoDialog", "Environment Directories:"))
        self.label_12.setText(_translate("CondaInfoDialog", "Platform:"))
        self.useragentLabel.setText(_translate("CondaInfoDialog", "User-Agent:"))
        self.uidGidLabel.setText(_translate("CondaInfoDialog", "UID:GID:"))
        self.netrcLabel.setText(_translate("CondaInfoDialog", "netrc File:"))
        self.label_16.setText(_translate("CondaInfoDialog", "Offline Mode:"))
        self.label_18.setText(_translate("CondaInfoDialog", "conda-env Version:"))
