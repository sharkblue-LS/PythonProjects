# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\Feeds\FeedsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FeedsDialog(object):
    def setupUi(self, FeedsDialog):
        FeedsDialog.setObjectName("FeedsDialog")
        FeedsDialog.resize(352, 94)
        FeedsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(FeedsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.iconLabel = QtWidgets.QLabel(FeedsDialog)
        self.iconLabel.setText("")
        self.iconLabel.setObjectName("iconLabel")
        self.horizontalLayout.addWidget(self.iconLabel)
        self.label = QtWidgets.QLabel(FeedsDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.feedsLayout = QtWidgets.QGridLayout()
        self.feedsLayout.setObjectName("feedsLayout")
        self.verticalLayout.addLayout(self.feedsLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(FeedsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FeedsDialog)
        self.buttonBox.accepted.connect(FeedsDialog.accept)
        self.buttonBox.rejected.connect(FeedsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FeedsDialog)

    def retranslateUi(self, FeedsDialog):
        _translate = QtCore.QCoreApplication.translate
        FeedsDialog.setWindowTitle(_translate("FeedsDialog", "Add Feed"))
        self.label.setText(_translate("FeedsDialog", "Add Feeds from this site"))