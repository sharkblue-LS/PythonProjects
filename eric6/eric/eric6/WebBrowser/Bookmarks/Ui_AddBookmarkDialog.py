# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\Bookmarks\AddBookmarkDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddBookmarkDialog(object):
    def setupUi(self, AddBookmarkDialog):
        AddBookmarkDialog.setObjectName("AddBookmarkDialog")
        AddBookmarkDialog.resize(500, 230)
        AddBookmarkDialog.setMinimumSize(QtCore.QSize(500, 0))
        AddBookmarkDialog.setMaximumSize(QtCore.QSize(500, 250))
        AddBookmarkDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(AddBookmarkDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(AddBookmarkDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.nameEdit = E5LineEdit(AddBookmarkDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.addressLabel = QtWidgets.QLabel(AddBookmarkDialog)
        self.addressLabel.setObjectName("addressLabel")
        self.gridLayout.addWidget(self.addressLabel, 1, 0, 1, 1)
        self.addressEdit = E5LineEdit(AddBookmarkDialog)
        self.addressEdit.setObjectName("addressEdit")
        self.gridLayout.addWidget(self.addressEdit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AddBookmarkDialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.descriptionEdit = QtWidgets.QPlainTextEdit(AddBookmarkDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridLayout.addWidget(self.descriptionEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(AddBookmarkDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.locationCombo = QtWidgets.QComboBox(AddBookmarkDialog)
        self.locationCombo.setObjectName("locationCombo")
        self.gridLayout.addWidget(self.locationCombo, 3, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddBookmarkDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.retranslateUi(AddBookmarkDialog)
        self.buttonBox.accepted.connect(AddBookmarkDialog.accept)
        self.buttonBox.rejected.connect(AddBookmarkDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddBookmarkDialog)
        AddBookmarkDialog.setTabOrder(self.nameEdit, self.addressEdit)
        AddBookmarkDialog.setTabOrder(self.addressEdit, self.descriptionEdit)
        AddBookmarkDialog.setTabOrder(self.descriptionEdit, self.locationCombo)
        AddBookmarkDialog.setTabOrder(self.locationCombo, self.buttonBox)

    def retranslateUi(self, AddBookmarkDialog):
        _translate = QtCore.QCoreApplication.translate
        AddBookmarkDialog.setWindowTitle(_translate("AddBookmarkDialog", "Add Bookmark"))
        self.label_2.setText(_translate("AddBookmarkDialog", "Name:"))
        self.nameEdit.setToolTip(_translate("AddBookmarkDialog", "Enter the name"))
        self.addressLabel.setText(_translate("AddBookmarkDialog", "Address:"))
        self.addressEdit.setToolTip(_translate("AddBookmarkDialog", "Enter the address"))
        self.label.setText(_translate("AddBookmarkDialog", "Description:"))
        self.descriptionEdit.setToolTip(_translate("AddBookmarkDialog", "Enter a description"))
        self.label_4.setText(_translate("AddBookmarkDialog", "Folder:"))
from E5Gui.E5LineEdit import E5LineEdit
