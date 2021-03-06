# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\CondaPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CondaPage(object):
    def setupUi(self, CondaPage):
        CondaPage.setObjectName("CondaPage")
        CondaPage.resize(585, 165)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CondaPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headerLabel = QtWidgets.QLabel(CondaPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_2.addWidget(self.headerLabel)
        self.line13 = QtWidgets.QFrame(CondaPage)
        self.line13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line13.setObjectName("line13")
        self.verticalLayout_2.addWidget(self.line13)
        self.groupBox = QtWidgets.QGroupBox(CondaPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.condaExePicker = E5PathPicker(self.groupBox)
        self.condaExePicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.condaExePicker.setObjectName("condaExePicker")
        self.verticalLayout.addWidget(self.condaExePicker)
        self.textLabel1_4 = QtWidgets.QLabel(self.groupBox)
        self.textLabel1_4.setObjectName("textLabel1_4")
        self.verticalLayout.addWidget(self.textLabel1_4)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 292, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(CondaPage)
        QtCore.QMetaObject.connectSlotsByName(CondaPage)

    def retranslateUi(self, CondaPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("CondaPage", "<b>Configure \"conda\" support</b>"))
        self.groupBox.setTitle(_translate("CondaPage", "conda Executable"))
        self.condaExePicker.setToolTip(_translate("CondaPage", "Enter the path to the conda executable."))
        self.textLabel1_4.setText(_translate("CondaPage", "<b>Note:</b> Leave this entry empty to use the default value (conda or conda.exe)."))
from E5Gui.E5PathPicker import E5PathPicker
