# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\QtPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QtPage(object):
    def setupUi(self, QtPage):
        QtPage.setObjectName("QtPage")
        QtPage.resize(556, 1236)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(QtPage)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.headerLabel = QtWidgets.QLabel(QtPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_10.addWidget(self.headerLabel)
        self.line12 = QtWidgets.QFrame(QtPage)
        self.line12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line12.setObjectName("line12")
        self.verticalLayout_10.addWidget(self.line12)
        self.groupBox_6 = QtWidgets.QGroupBox(QtPage)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TextLabel1_2_2_5 = QtWidgets.QLabel(self.groupBox_3)
        self.TextLabel1_2_2_5.setObjectName("TextLabel1_2_2_5")
        self.verticalLayout.addWidget(self.TextLabel1_2_2_5)
        self.qtTransPicker = E5PathPicker(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qtTransPicker.sizePolicy().hasHeightForWidth())
        self.qtTransPicker.setSizePolicy(sizePolicy)
        self.qtTransPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.qtTransPicker.setObjectName("qtTransPicker")
        self.verticalLayout.addWidget(self.qtTransPicker)
        self.textLabel1_2_4 = QtWidgets.QLabel(self.groupBox_3)
        self.textLabel1_2_4.setWordWrap(True)
        self.textLabel1_2_4.setObjectName("textLabel1_2_4")
        self.verticalLayout.addWidget(self.textLabel1_2_4)
        self.verticalLayout_8.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.qtToolsDirPicker = E5PathPicker(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qtToolsDirPicker.sizePolicy().hasHeightForWidth())
        self.qtToolsDirPicker.setSizePolicy(sizePolicy)
        self.qtToolsDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.qtToolsDirPicker.setObjectName("qtToolsDirPicker")
        self.horizontalLayout.addWidget(self.qtToolsDirPicker)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.qtPrefixEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.qtPrefixEdit.setObjectName("qtPrefixEdit")
        self.horizontalLayout_2.addWidget(self.qtPrefixEdit)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.qtPostfixEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.qtPostfixEdit.setObjectName("qtPostfixEdit")
        self.horizontalLayout_2.addWidget(self.qtPostfixEdit)
        self.qtSampleLabel = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qtSampleLabel.sizePolicy().hasHeightForWidth())
        self.qtSampleLabel.setSizePolicy(sizePolicy)
        self.qtSampleLabel.setObjectName("qtSampleLabel")
        self.horizontalLayout_2.addWidget(self.qtSampleLabel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_8.addWidget(self.groupBox_4)
        self.verticalLayout_10.addWidget(self.groupBox_6)
        self.groupBox_7 = QtWidgets.QGroupBox(QtPage)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label = QtWidgets.QLabel(self.groupBox_5)
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.label)
        self.pyqt5VenvComboBox = QtWidgets.QComboBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt5VenvComboBox.sizePolicy().hasHeightForWidth())
        self.pyqt5VenvComboBox.setSizePolicy(sizePolicy)
        self.pyqt5VenvComboBox.setObjectName("pyqt5VenvComboBox")
        self.horizontalLayout_8.addWidget(self.pyqt5VenvComboBox)
        self.pyqt5VenvDlgButton = QtWidgets.QToolButton(self.groupBox_5)
        self.pyqt5VenvDlgButton.setText("")
        self.pyqt5VenvDlgButton.setObjectName("pyqt5VenvDlgButton")
        self.horizontalLayout_8.addWidget(self.pyqt5VenvDlgButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.pyqtToolsDirPicker = E5PathPicker(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqtToolsDirPicker.sizePolicy().hasHeightForWidth())
        self.pyqtToolsDirPicker.setSizePolicy(sizePolicy)
        self.pyqtToolsDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pyqtToolsDirPicker.setObjectName("pyqtToolsDirPicker")
        self.horizontalLayout_3.addWidget(self.pyqtToolsDirPicker)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.pyuicIndentSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.pyuicIndentSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pyuicIndentSpinBox.setMinimum(2)
        self.pyuicIndentSpinBox.setMaximum(16)
        self.pyuicIndentSpinBox.setProperty("value", 4)
        self.pyuicIndentSpinBox.setObjectName("pyuicIndentSpinBox")
        self.gridLayout.addWidget(self.pyuicIndentSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(448, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.pyuicImportsCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.pyuicImportsCheckBox.setObjectName("pyuicImportsCheckBox")
        self.gridLayout.addWidget(self.pyuicImportsCheckBox, 1, 0, 1, 3)
        self.pyuicExecuteCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.pyuicExecuteCheckBox.setObjectName("pyuicExecuteCheckBox")
        self.gridLayout.addWidget(self.pyuicExecuteCheckBox, 2, 0, 1, 3)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_6.addWidget(self.groupBox_5)
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.groupBox_8)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.pyqt6VenvComboBox = QtWidgets.QComboBox(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt6VenvComboBox.sizePolicy().hasHeightForWidth())
        self.pyqt6VenvComboBox.setSizePolicy(sizePolicy)
        self.pyqt6VenvComboBox.setObjectName("pyqt6VenvComboBox")
        self.horizontalLayout_7.addWidget(self.pyqt6VenvComboBox)
        self.pyqt6VenvDlgButton = QtWidgets.QToolButton(self.groupBox_8)
        self.pyqt6VenvDlgButton.setText("")
        self.pyqt6VenvDlgButton.setObjectName("pyqt6VenvDlgButton")
        self.horizontalLayout_7.addWidget(self.pyqt6VenvDlgButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.groupBox_8)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.pyqt6ToolsDirPicker = E5PathPicker(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt6ToolsDirPicker.sizePolicy().hasHeightForWidth())
        self.pyqt6ToolsDirPicker.setSizePolicy(sizePolicy)
        self.pyqt6ToolsDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pyqt6ToolsDirPicker.setObjectName("pyqt6ToolsDirPicker")
        self.horizontalLayout_4.addWidget(self.pyqt6ToolsDirPicker)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(448, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        self.pyuic6ExecuteCheckBox = QtWidgets.QCheckBox(self.groupBox_9)
        self.pyuic6ExecuteCheckBox.setObjectName("pyuic6ExecuteCheckBox")
        self.gridLayout_3.addWidget(self.pyuic6ExecuteCheckBox, 1, 0, 1, 3)
        self.pyuic6IndentSpinBox = QtWidgets.QSpinBox(self.groupBox_9)
        self.pyuic6IndentSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pyuic6IndentSpinBox.setMinimum(2)
        self.pyuic6IndentSpinBox.setMaximum(16)
        self.pyuic6IndentSpinBox.setProperty("value", 4)
        self.pyuic6IndentSpinBox.setObjectName("pyuic6IndentSpinBox")
        self.gridLayout_3.addWidget(self.pyuic6IndentSpinBox, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_9)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_9)
        self.verticalLayout_6.addWidget(self.groupBox_8)
        self.verticalLayout_10.addWidget(self.groupBox_7)
        self.groupBox_10 = QtWidgets.QGroupBox(QtPage)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pyside2Group = QtWidgets.QGroupBox(self.groupBox_10)
        self.pyside2Group.setObjectName("pyside2Group")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pyside2Group)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.pyside2Group)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.pyside2VenvComboBox = QtWidgets.QComboBox(self.pyside2Group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyside2VenvComboBox.sizePolicy().hasHeightForWidth())
        self.pyside2VenvComboBox.setSizePolicy(sizePolicy)
        self.pyside2VenvComboBox.setObjectName("pyside2VenvComboBox")
        self.horizontalLayout_6.addWidget(self.pyside2VenvComboBox)
        self.pyside2VenvDlgButton = QtWidgets.QToolButton(self.pyside2Group)
        self.pyside2VenvDlgButton.setText("")
        self.pyside2VenvDlgButton.setObjectName("pyside2VenvDlgButton")
        self.horizontalLayout_6.addWidget(self.pyside2VenvDlgButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_7 = QtWidgets.QLabel(self.pyside2Group)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_5.addWidget(self.label_7)
        self.pyside2ToolsDirPicker = E5PathPicker(self.pyside2Group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyside2ToolsDirPicker.sizePolicy().hasHeightForWidth())
        self.pyside2ToolsDirPicker.setSizePolicy(sizePolicy)
        self.pyside2ToolsDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pyside2ToolsDirPicker.setObjectName("pyside2ToolsDirPicker")
        self.horizontalLayout_5.addWidget(self.pyside2ToolsDirPicker)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.groupBox_2 = QtWidgets.QGroupBox(self.pyside2Group)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pyside2uicImportsCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.pyside2uicImportsCheckBox.setObjectName("pyside2uicImportsCheckBox")
        self.gridLayout_2.addWidget(self.pyside2uicImportsCheckBox, 0, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_9.addWidget(self.pyside2Group)
        self.pyside2Group_2 = QtWidgets.QGroupBox(self.groupBox_10)
        self.pyside2Group_2.setObjectName("pyside2Group_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.pyside2Group_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_12 = QtWidgets.QLabel(self.pyside2Group_2)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_9.addWidget(self.label_12)
        self.pyside6VenvComboBox = QtWidgets.QComboBox(self.pyside2Group_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyside6VenvComboBox.sizePolicy().hasHeightForWidth())
        self.pyside6VenvComboBox.setSizePolicy(sizePolicy)
        self.pyside6VenvComboBox.setObjectName("pyside6VenvComboBox")
        self.horizontalLayout_9.addWidget(self.pyside6VenvComboBox)
        self.pyside6VenvDlgButton = QtWidgets.QToolButton(self.pyside2Group_2)
        self.pyside6VenvDlgButton.setText("")
        self.pyside6VenvDlgButton.setObjectName("pyside6VenvDlgButton")
        self.horizontalLayout_9.addWidget(self.pyside6VenvDlgButton)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_13 = QtWidgets.QLabel(self.pyside2Group_2)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_10.addWidget(self.label_13)
        self.pyside6ToolsDirPicker = E5PathPicker(self.pyside2Group_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyside6ToolsDirPicker.sizePolicy().hasHeightForWidth())
        self.pyside6ToolsDirPicker.setSizePolicy(sizePolicy)
        self.pyside6ToolsDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pyside6ToolsDirPicker.setObjectName("pyside6ToolsDirPicker")
        self.horizontalLayout_10.addWidget(self.pyside6ToolsDirPicker)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.groupBox_11 = QtWidgets.QGroupBox(self.pyside2Group_2)
        self.groupBox_11.setObjectName("groupBox_11")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_11)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pyside6uicImportsCheckBox = QtWidgets.QCheckBox(self.groupBox_11)
        self.pyside6uicImportsCheckBox.setObjectName("pyside6uicImportsCheckBox")
        self.gridLayout_4.addWidget(self.pyside6uicImportsCheckBox, 0, 0, 1, 2)
        self.verticalLayout_7.addWidget(self.groupBox_11)
        self.verticalLayout_9.addWidget(self.pyside2Group_2)
        self.verticalLayout_10.addWidget(self.groupBox_10)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem2)

        self.retranslateUi(QtPage)
        QtCore.QMetaObject.connectSlotsByName(QtPage)
        QtPage.setTabOrder(self.qtTransPicker, self.qtToolsDirPicker)
        QtPage.setTabOrder(self.qtToolsDirPicker, self.qtPrefixEdit)
        QtPage.setTabOrder(self.qtPrefixEdit, self.qtPostfixEdit)
        QtPage.setTabOrder(self.qtPostfixEdit, self.pyqt5VenvComboBox)
        QtPage.setTabOrder(self.pyqt5VenvComboBox, self.pyqt5VenvDlgButton)
        QtPage.setTabOrder(self.pyqt5VenvDlgButton, self.pyqtToolsDirPicker)
        QtPage.setTabOrder(self.pyqtToolsDirPicker, self.pyuicIndentSpinBox)
        QtPage.setTabOrder(self.pyuicIndentSpinBox, self.pyuicImportsCheckBox)
        QtPage.setTabOrder(self.pyuicImportsCheckBox, self.pyuicExecuteCheckBox)
        QtPage.setTabOrder(self.pyuicExecuteCheckBox, self.pyqt6VenvComboBox)
        QtPage.setTabOrder(self.pyqt6VenvComboBox, self.pyqt6VenvDlgButton)
        QtPage.setTabOrder(self.pyqt6VenvDlgButton, self.pyqt6ToolsDirPicker)
        QtPage.setTabOrder(self.pyqt6ToolsDirPicker, self.pyuic6IndentSpinBox)
        QtPage.setTabOrder(self.pyuic6IndentSpinBox, self.pyuic6ExecuteCheckBox)
        QtPage.setTabOrder(self.pyuic6ExecuteCheckBox, self.pyside2VenvComboBox)
        QtPage.setTabOrder(self.pyside2VenvComboBox, self.pyside2VenvDlgButton)
        QtPage.setTabOrder(self.pyside2VenvDlgButton, self.pyside2ToolsDirPicker)
        QtPage.setTabOrder(self.pyside2ToolsDirPicker, self.pyside2uicImportsCheckBox)
        QtPage.setTabOrder(self.pyside2uicImportsCheckBox, self.pyside6VenvComboBox)
        QtPage.setTabOrder(self.pyside6VenvComboBox, self.pyside6VenvDlgButton)
        QtPage.setTabOrder(self.pyside6VenvDlgButton, self.pyside6ToolsDirPicker)
        QtPage.setTabOrder(self.pyside6ToolsDirPicker, self.pyside6uicImportsCheckBox)

    def retranslateUi(self, QtPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("QtPage", "<b>Configure Qt</b>"))
        self.groupBox_6.setTitle(_translate("QtPage", "Qt"))
        self.groupBox_3.setTitle(_translate("QtPage", "Qt Translations Directory"))
        self.TextLabel1_2_2_5.setText(_translate("QtPage", "<font color=\"#FF0000\"><b>Note:</b> This setting is activated at the next startup of the application.</font>"))
        self.qtTransPicker.setToolTip(_translate("QtPage", "Enter the path of the Qt translations directory."))
        self.textLabel1_2_4.setText(_translate("QtPage", "<b>Note:</b> Leave this entry empty to use the path compiled into the Qt library."))
        self.groupBox_4.setTitle(_translate("QtPage", "Qt Tools"))
        self.label_4.setText(_translate("QtPage", "Tools Directory:"))
        self.qtToolsDirPicker.setToolTip(_translate("QtPage", "Enter the path of the Qt tools directory, if they are not found."))
        self.label_3.setText(_translate("QtPage", "Qt-Prefix:"))
        self.qtPrefixEdit.setToolTip(_translate("QtPage", "Enter the prefix for the Qt tools name"))
        self.qtPrefixEdit.setWhatsThis(_translate("QtPage", "<b>Qt-Prefix</b>\n"
"<p>Enter a prefix used to determine the Qt tool executable name. It is composed of the prefix, the tool name and the postfix. The executable extension is added automatically on Windows.</p>"))
        self.label_5.setText(_translate("QtPage", "Qt-Postfix:"))
        self.qtPostfixEdit.setToolTip(_translate("QtPage", "Enter the postfix for the Qt tools name"))
        self.qtPostfixEdit.setWhatsThis(_translate("QtPage", "<b>Qt-Postfix</b>\n"
"<p>Enter a postfix used to determine the Qt tool executable name. It is composed of the prefix, the tool name and the postfix. The executable extension is added automatically on Windows.</p>"))
        self.qtSampleLabel.setToolTip(_translate("QtPage", "This gives an example of the complete tool name"))
        self.qtSampleLabel.setText(_translate("QtPage", "designer"))
        self.groupBox_7.setTitle(_translate("QtPage", "PyQt"))
        self.groupBox_5.setTitle(_translate("QtPage", "PyQt 5"))
        self.label.setText(_translate("QtPage", "Virtual Environment:"))
        self.pyqt5VenvComboBox.setToolTip(_translate("QtPage", "Select the virtual environment to be used"))
        self.pyqt5VenvDlgButton.setToolTip(_translate("QtPage", "Press to open the virtual environment manager dialog"))
        self.label_6.setText(_translate("QtPage", "Tools Directory:"))
        self.pyqtToolsDirPicker.setToolTip(_translate("QtPage", "Enter the path of the PyQt 5 tools directory, if they are not found."))
        self.groupBox.setTitle(_translate("QtPage", "pyuic5 Options"))
        self.label_2.setText(_translate("QtPage", "Indent Width:"))
        self.pyuicIndentSpinBox.setToolTip(_translate("QtPage", "Select the indent width (default: 4)"))
        self.pyuicImportsCheckBox.setText(_translate("QtPage", "Generate imports relative to \'.\'"))
        self.pyuicExecuteCheckBox.setToolTip(_translate("QtPage", "Select to generate extra code to test and display the form"))
        self.pyuicExecuteCheckBox.setText(_translate("QtPage", "Generate Extra Test Code"))
        self.groupBox_8.setTitle(_translate("QtPage", "PyQt 6"))
        self.label_10.setText(_translate("QtPage", "Virtual Environment:"))
        self.pyqt6VenvComboBox.setToolTip(_translate("QtPage", "Select the virtual environment to be used"))
        self.pyqt6VenvDlgButton.setToolTip(_translate("QtPage", "Press to open the virtual environment manager dialog"))
        self.label_8.setText(_translate("QtPage", "Tools Directory:"))
        self.pyqt6ToolsDirPicker.setToolTip(_translate("QtPage", "Enter the path of the PyQt 6 tools directory, if they are not found."))
        self.groupBox_9.setTitle(_translate("QtPage", "pyuic6 Options"))
        self.pyuic6ExecuteCheckBox.setToolTip(_translate("QtPage", "Select to generate extra code to test and display the form"))
        self.pyuic6ExecuteCheckBox.setText(_translate("QtPage", "Generate Extra Test Code"))
        self.pyuic6IndentSpinBox.setToolTip(_translate("QtPage", "Select the indent width (default: 4)"))
        self.label_9.setText(_translate("QtPage", "Indent Width:"))
        self.groupBox_10.setTitle(_translate("QtPage", "PySide"))
        self.pyside2Group.setTitle(_translate("QtPage", "PySide2"))
        self.label_11.setText(_translate("QtPage", "Virtual Environment:"))
        self.pyside2VenvComboBox.setToolTip(_translate("QtPage", "Select the virtual environment to be used"))
        self.pyside2VenvDlgButton.setToolTip(_translate("QtPage", "Press to open the virtual environment manager dialog"))
        self.label_7.setText(_translate("QtPage", "Tools Directory:"))
        self.pyside2ToolsDirPicker.setToolTip(_translate("QtPage", "Enter the path of the PySide2 tools directory, if they are not found."))
        self.groupBox_2.setTitle(_translate("QtPage", "pyside2-uic Options"))
        self.pyside2uicImportsCheckBox.setText(_translate("QtPage", "Generate imports relative to \'.\'"))
        self.pyside2Group_2.setTitle(_translate("QtPage", "PySide6"))
        self.label_12.setText(_translate("QtPage", "Virtual Environment:"))
        self.pyside6VenvComboBox.setToolTip(_translate("QtPage", "Select the virtual environment to be used"))
        self.pyside6VenvDlgButton.setToolTip(_translate("QtPage", "Press to open the virtual environment manager dialog"))
        self.label_13.setText(_translate("QtPage", "Tools Directory:"))
        self.pyside6ToolsDirPicker.setToolTip(_translate("QtPage", "Enter the path of the PySide6 tools directory, if they are not found."))
        self.groupBox_11.setTitle(_translate("QtPage", "pyside6-uic Options"))
        self.pyside6uicImportsCheckBox.setText(_translate("QtPage", "Generate imports relative to \'.\'"))
from E5Gui.E5PathPicker import E5PathPicker
