# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\PipInterface\PipDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PipDialog(object):
    def setupUi(self, PipDialog):
        PipDialog.setObjectName("PipDialog")
        PipDialog.resize(600, 500)
        PipDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(PipDialog)
        self.vboxlayout.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.outputGroup = QtWidgets.QGroupBox(PipDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.outputGroup.sizePolicy().hasHeightForWidth())
        self.outputGroup.setSizePolicy(sizePolicy)
        self.outputGroup.setObjectName("outputGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.outputGroup)
        self.vboxlayout1.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.resultbox = QtWidgets.QTextEdit(self.outputGroup)
        self.resultbox.setReadOnly(True)
        self.resultbox.setAcceptRichText(False)
        self.resultbox.setObjectName("resultbox")
        self.vboxlayout1.addWidget(self.resultbox)
        self.vboxlayout.addWidget(self.outputGroup)
        self.errorGroup = QtWidgets.QGroupBox(PipDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout2 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout2.setContentsMargins(11, 11, 11, 11)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout2.addWidget(self.errors)
        self.vboxlayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(PipDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(PipDialog)
        QtCore.QMetaObject.connectSlotsByName(PipDialog)
        PipDialog.setTabOrder(self.resultbox, self.errors)
        PipDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, PipDialog):
        _translate = QtCore.QCoreApplication.translate
        PipDialog.setWindowTitle(_translate("PipDialog", "pip"))
        self.outputGroup.setTitle(_translate("PipDialog", "Output"))
        self.errorGroup.setTitle(_translate("PipDialog", "Errors"))
