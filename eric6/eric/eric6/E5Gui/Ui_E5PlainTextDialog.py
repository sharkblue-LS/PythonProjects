# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\E5Gui\E5PlainTextDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_E5PlainTextDialog(object):
    def setupUi(self, E5PlainTextDialog):
        E5PlainTextDialog.setObjectName("E5PlainTextDialog")
        E5PlainTextDialog.resize(500, 400)
        E5PlainTextDialog.setWindowTitle("")
        E5PlainTextDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5PlainTextDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QPlainTextEdit(E5PlainTextDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(E5PlainTextDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(E5PlainTextDialog)
        self.buttonBox.accepted.connect(E5PlainTextDialog.accept)
        self.buttonBox.rejected.connect(E5PlainTextDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(E5PlainTextDialog)

    def retranslateUi(self, E5PlainTextDialog):
        pass
