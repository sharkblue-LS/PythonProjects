# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\PipPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PipPage(object):
    def setupUi(self, PipPage):
        PipPage.setObjectName("PipPage")
        PipPage.resize(402, 247)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(PipPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headerLabel = QtWidgets.QLabel(PipPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.line9_3 = QtWidgets.QFrame(PipPage)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setObjectName("line9_3")
        self.verticalLayout_3.addWidget(self.line9_3)
        self.groupBox_2 = QtWidgets.QGroupBox(PipPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.indexEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.indexEdit.setObjectName("indexEdit")
        self.verticalLayout.addWidget(self.indexEdit)
        self.indexLabel = QtWidgets.QLabel(self.groupBox_2)
        self.indexLabel.setText("")
        self.indexLabel.setOpenExternalLinks(True)
        self.indexLabel.setObjectName("indexLabel")
        self.verticalLayout.addWidget(self.indexLabel)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(PipPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.noCondaCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.noCondaCheckBox.setObjectName("noCondaCheckBox")
        self.verticalLayout_2.addWidget(self.noCondaCheckBox)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 234, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        self.retranslateUi(PipPage)
        QtCore.QMetaObject.connectSlotsByName(PipPage)

    def retranslateUi(self, PipPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("PipPage", "<b>Configure pip</b>"))
        self.groupBox_2.setTitle(_translate("PipPage", "Index URL"))
        self.indexEdit.setToolTip(_translate("PipPage", "Enter the URL of the package index or leave empty to use the default"))
        self.groupBox.setTitle(_translate("PipPage", "Environment"))
        self.noCondaCheckBox.setToolTip(_translate("PipPage", "Select to exclude conda managed environments"))
        self.noCondaCheckBox.setText(_translate("PipPage", "Don\'t show \'Conda\' environments"))