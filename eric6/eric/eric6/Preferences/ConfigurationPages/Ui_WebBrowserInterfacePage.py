# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\WebBrowserInterfacePage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WebBrowserInterfacePage(object):
    def setupUi(self, WebBrowserInterfacePage):
        WebBrowserInterfacePage.setObjectName("WebBrowserInterfacePage")
        WebBrowserInterfacePage.resize(555, 133)
        self.verticalLayout = QtWidgets.QVBoxLayout(WebBrowserInterfacePage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(WebBrowserInterfacePage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line9 = QtWidgets.QFrame(WebBrowserInterfacePage)
        self.line9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9.setObjectName("line9")
        self.verticalLayout.addWidget(self.line9)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(WebBrowserInterfacePage)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.styleComboBox = QtWidgets.QComboBox(WebBrowserInterfacePage)
        self.styleComboBox.setObjectName("styleComboBox")
        self.gridLayout.addWidget(self.styleComboBox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(WebBrowserInterfacePage)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.styleSheetPicker = E5PathPicker(WebBrowserInterfacePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.styleSheetPicker.sizePolicy().hasHeightForWidth())
        self.styleSheetPicker.setSizePolicy(sizePolicy)
        self.styleSheetPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.styleSheetPicker.setObjectName("styleSheetPicker")
        self.gridLayout.addWidget(self.styleSheetPicker, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(537, 41, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(WebBrowserInterfacePage)
        QtCore.QMetaObject.connectSlotsByName(WebBrowserInterfacePage)

    def retranslateUi(self, WebBrowserInterfacePage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("WebBrowserInterfacePage", "<b>Configure User Interface</b>"))
        self.label_2.setText(_translate("WebBrowserInterfacePage", "Style:"))
        self.styleComboBox.setToolTip(_translate("WebBrowserInterfacePage", "Select the interface style"))
        self.label_3.setText(_translate("WebBrowserInterfacePage", "Style Sheet:"))
        self.styleSheetPicker.setToolTip(_translate("WebBrowserInterfacePage", "Enter the path of the style sheet file"))
from E5Gui.E5PathPicker import E5PathPicker
