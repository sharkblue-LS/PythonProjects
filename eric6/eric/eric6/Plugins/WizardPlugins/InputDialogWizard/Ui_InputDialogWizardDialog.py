# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\WizardPlugins\InputDialogWizard\InputDialogWizardDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InputDialogWizardDialog(object):
    def setupUi(self, InputDialogWizardDialog):
        InputDialogWizardDialog.setObjectName("InputDialogWizardDialog")
        InputDialogWizardDialog.resize(501, 684)
        InputDialogWizardDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(InputDialogWizardDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(InputDialogWizardDialog)
        self.groupBox.setObjectName("groupBox")
        self.hboxlayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.hboxlayout.setObjectName("hboxlayout")
        self.rText = QtWidgets.QRadioButton(self.groupBox)
        self.rText.setChecked(True)
        self.rText.setObjectName("rText")
        self.hboxlayout.addWidget(self.rText)
        self.rInteger = QtWidgets.QRadioButton(self.groupBox)
        self.rInteger.setObjectName("rInteger")
        self.hboxlayout.addWidget(self.rInteger)
        self.rDouble = QtWidgets.QRadioButton(self.groupBox)
        self.rDouble.setObjectName("rDouble")
        self.hboxlayout.addWidget(self.rDouble)
        self.rItem = QtWidgets.QRadioButton(self.groupBox)
        self.rItem.setObjectName("rItem")
        self.hboxlayout.addWidget(self.rItem)
        self.verticalLayout.addWidget(self.groupBox)
        self.label = QtWidgets.QLabel(InputDialogWizardDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.eResultVar = QtWidgets.QLineEdit(InputDialogWizardDialog)
        self.eResultVar.setObjectName("eResultVar")
        self.verticalLayout.addWidget(self.eResultVar)
        self.TextLabel1 = QtWidgets.QLabel(InputDialogWizardDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.verticalLayout.addWidget(self.TextLabel1)
        self.eCaption = QtWidgets.QLineEdit(InputDialogWizardDialog)
        self.eCaption.setObjectName("eCaption")
        self.verticalLayout.addWidget(self.eCaption)
        self.TextLabel2 = QtWidgets.QLabel(InputDialogWizardDialog)
        self.TextLabel2.setObjectName("TextLabel2")
        self.verticalLayout.addWidget(self.TextLabel2)
        self.eLabel = QtWidgets.QLineEdit(InputDialogWizardDialog)
        self.eLabel.setObjectName("eLabel")
        self.verticalLayout.addWidget(self.eLabel)
        self.parentGroup = QtWidgets.QGroupBox(InputDialogWizardDialog)
        self.parentGroup.setObjectName("parentGroup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.parentGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.parentSelf = QtWidgets.QRadioButton(self.parentGroup)
        self.parentSelf.setChecked(True)
        self.parentSelf.setObjectName("parentSelf")
        self.gridLayout_3.addWidget(self.parentSelf, 0, 0, 1, 1)
        self.parentNone = QtWidgets.QRadioButton(self.parentGroup)
        self.parentNone.setObjectName("parentNone")
        self.gridLayout_3.addWidget(self.parentNone, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.parentOther = QtWidgets.QRadioButton(self.parentGroup)
        self.parentOther.setObjectName("parentOther")
        self.horizontalLayout_2.addWidget(self.parentOther)
        self.parentEdit = QtWidgets.QLineEdit(self.parentGroup)
        self.parentEdit.setEnabled(False)
        self.parentEdit.setObjectName("parentEdit")
        self.horizontalLayout_2.addWidget(self.parentEdit)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.parentGroup)
        self.groupBox_2 = QtWidgets.QGroupBox(InputDialogWizardDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.vboxlayout.setObjectName("vboxlayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.hboxlayout1 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.rEchoNormal = QtWidgets.QRadioButton(self.groupBox_3)
        self.rEchoNormal.setChecked(True)
        self.rEchoNormal.setObjectName("rEchoNormal")
        self.hboxlayout1.addWidget(self.rEchoNormal)
        self.rEchoNoEcho = QtWidgets.QRadioButton(self.groupBox_3)
        self.rEchoNoEcho.setObjectName("rEchoNoEcho")
        self.hboxlayout1.addWidget(self.rEchoNoEcho)
        self.rEchoPassword = QtWidgets.QRadioButton(self.groupBox_3)
        self.rEchoPassword.setObjectName("rEchoPassword")
        self.hboxlayout1.addWidget(self.rEchoPassword)
        self.vboxlayout.addWidget(self.groupBox_3)
        self.TextLabel3 = QtWidgets.QLabel(self.groupBox_2)
        self.TextLabel3.setObjectName("TextLabel3")
        self.vboxlayout.addWidget(self.TextLabel3)
        self.eTextDefault = QtWidgets.QLineEdit(self.groupBox_2)
        self.eTextDefault.setObjectName("eTextDefault")
        self.vboxlayout.addWidget(self.eTextDefault)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(InputDialogWizardDialog)
        self.groupBox_4.setEnabled(False)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridlayout.setObjectName("gridlayout")
        self.sIntStep = QtWidgets.QSpinBox(self.groupBox_4)
        self.sIntStep.setMinimum(-2147483647)
        self.sIntStep.setMaximum(2147483647)
        self.sIntStep.setProperty("value", 1)
        self.sIntStep.setObjectName("sIntStep")
        self.gridlayout.addWidget(self.sIntStep, 1, 3, 1, 1)
        self.sIntTo = QtWidgets.QSpinBox(self.groupBox_4)
        self.sIntTo.setMinimum(-2147483647)
        self.sIntTo.setMaximum(2147483647)
        self.sIntTo.setProperty("value", 2147483647)
        self.sIntTo.setObjectName("sIntTo")
        self.gridlayout.addWidget(self.sIntTo, 1, 2, 1, 1)
        self.sIntFrom = QtWidgets.QSpinBox(self.groupBox_4)
        self.sIntFrom.setMinimum(-2147483647)
        self.sIntFrom.setMaximum(2147483647)
        self.sIntFrom.setProperty("value", -2147483647)
        self.sIntFrom.setObjectName("sIntFrom")
        self.gridlayout.addWidget(self.sIntFrom, 1, 1, 1, 1)
        self.sIntDefault = QtWidgets.QSpinBox(self.groupBox_4)
        self.sIntDefault.setMinimum(-2147483647)
        self.sIntDefault.setMaximum(2147483647)
        self.sIntDefault.setObjectName("sIntDefault")
        self.gridlayout.addWidget(self.sIntDefault, 1, 0, 1, 1)
        self.TextLabel4_4 = QtWidgets.QLabel(self.groupBox_4)
        self.TextLabel4_4.setObjectName("TextLabel4_4")
        self.gridlayout.addWidget(self.TextLabel4_4, 0, 3, 1, 1)
        self.TextLabel4_3 = QtWidgets.QLabel(self.groupBox_4)
        self.TextLabel4_3.setObjectName("TextLabel4_3")
        self.gridlayout.addWidget(self.TextLabel4_3, 0, 2, 1, 1)
        self.TextLabel4_2 = QtWidgets.QLabel(self.groupBox_4)
        self.TextLabel4_2.setObjectName("TextLabel4_2")
        self.gridlayout.addWidget(self.TextLabel4_2, 0, 1, 1, 1)
        self.TextLabel4 = QtWidgets.QLabel(self.groupBox_4)
        self.TextLabel4.setObjectName("TextLabel4")
        self.gridlayout.addWidget(self.TextLabel4, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(InputDialogWizardDialog)
        self.groupBox_5.setEnabled(False)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridlayout1 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridlayout1.setObjectName("gridlayout1")
        self.sDoubleDecimals = QtWidgets.QSpinBox(self.groupBox_5)
        self.sDoubleDecimals.setMinimum(-2147483647)
        self.sDoubleDecimals.setMaximum(2147483647)
        self.sDoubleDecimals.setProperty("value", 1)
        self.sDoubleDecimals.setObjectName("sDoubleDecimals")
        self.gridlayout1.addWidget(self.sDoubleDecimals, 1, 3, 1, 1)
        self.eDoubleTo = QtWidgets.QLineEdit(self.groupBox_5)
        self.eDoubleTo.setObjectName("eDoubleTo")
        self.gridlayout1.addWidget(self.eDoubleTo, 1, 2, 1, 1)
        self.eDoubleFrom = QtWidgets.QLineEdit(self.groupBox_5)
        self.eDoubleFrom.setObjectName("eDoubleFrom")
        self.gridlayout1.addWidget(self.eDoubleFrom, 1, 1, 1, 1)
        self.eDoubleDefault = QtWidgets.QLineEdit(self.groupBox_5)
        self.eDoubleDefault.setObjectName("eDoubleDefault")
        self.gridlayout1.addWidget(self.eDoubleDefault, 1, 0, 1, 1)
        self.TextLabel5 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel5.setObjectName("TextLabel5")
        self.gridlayout1.addWidget(self.TextLabel5, 0, 0, 1, 1)
        self.TextLabel6 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel6.setObjectName("TextLabel6")
        self.gridlayout1.addWidget(self.TextLabel6, 0, 1, 1, 1)
        self.TextLabel7 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel7.setObjectName("TextLabel7")
        self.gridlayout1.addWidget(self.TextLabel7, 0, 2, 1, 1)
        self.TextLabel8 = QtWidgets.QLabel(self.groupBox_5)
        self.TextLabel8.setObjectName("TextLabel8")
        self.gridlayout1.addWidget(self.TextLabel8, 0, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(InputDialogWizardDialog)
        self.groupBox_6.setEnabled(False)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridlayout2 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridlayout2.setObjectName("gridlayout2")
        self.cEditable = QtWidgets.QCheckBox(self.groupBox_6)
        self.cEditable.setChecked(True)
        self.cEditable.setObjectName("cEditable")
        self.gridlayout2.addWidget(self.cEditable, 1, 2, 1, 1)
        self.sCurrentItem = QtWidgets.QSpinBox(self.groupBox_6)
        self.sCurrentItem.setObjectName("sCurrentItem")
        self.gridlayout2.addWidget(self.sCurrentItem, 1, 1, 1, 1)
        self.eVariable = QtWidgets.QLineEdit(self.groupBox_6)
        self.eVariable.setObjectName("eVariable")
        self.gridlayout2.addWidget(self.eVariable, 1, 0, 1, 1)
        self.TextLabel10 = QtWidgets.QLabel(self.groupBox_6)
        self.TextLabel10.setObjectName("TextLabel10")
        self.gridlayout2.addWidget(self.TextLabel10, 0, 1, 1, 1)
        self.TextLabel9 = QtWidgets.QLabel(self.groupBox_6)
        self.TextLabel9.setObjectName("TextLabel9")
        self.gridlayout2.addWidget(self.TextLabel9, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_6)
        self.buttonBox = QtWidgets.QDialogButtonBox(InputDialogWizardDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(InputDialogWizardDialog)
        self.rText.toggled['bool'].connect(self.groupBox_2.setEnabled)
        self.rInteger.toggled['bool'].connect(self.groupBox_4.setEnabled)
        self.rDouble.toggled['bool'].connect(self.groupBox_5.setEnabled)
        self.rItem.toggled['bool'].connect(self.groupBox_6.setEnabled)
        self.buttonBox.accepted.connect(InputDialogWizardDialog.accept)
        self.buttonBox.rejected.connect(InputDialogWizardDialog.reject)
        self.parentOther.toggled['bool'].connect(self.parentEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(InputDialogWizardDialog)
        InputDialogWizardDialog.setTabOrder(self.rText, self.rInteger)
        InputDialogWizardDialog.setTabOrder(self.rInteger, self.rDouble)
        InputDialogWizardDialog.setTabOrder(self.rDouble, self.rItem)
        InputDialogWizardDialog.setTabOrder(self.rItem, self.eResultVar)
        InputDialogWizardDialog.setTabOrder(self.eResultVar, self.eCaption)
        InputDialogWizardDialog.setTabOrder(self.eCaption, self.eLabel)
        InputDialogWizardDialog.setTabOrder(self.eLabel, self.parentSelf)
        InputDialogWizardDialog.setTabOrder(self.parentSelf, self.parentNone)
        InputDialogWizardDialog.setTabOrder(self.parentNone, self.parentOther)
        InputDialogWizardDialog.setTabOrder(self.parentOther, self.parentEdit)
        InputDialogWizardDialog.setTabOrder(self.parentEdit, self.rEchoNormal)
        InputDialogWizardDialog.setTabOrder(self.rEchoNormal, self.rEchoNoEcho)
        InputDialogWizardDialog.setTabOrder(self.rEchoNoEcho, self.rEchoPassword)
        InputDialogWizardDialog.setTabOrder(self.rEchoPassword, self.eTextDefault)
        InputDialogWizardDialog.setTabOrder(self.eTextDefault, self.sIntDefault)
        InputDialogWizardDialog.setTabOrder(self.sIntDefault, self.sIntFrom)
        InputDialogWizardDialog.setTabOrder(self.sIntFrom, self.sIntTo)
        InputDialogWizardDialog.setTabOrder(self.sIntTo, self.sIntStep)
        InputDialogWizardDialog.setTabOrder(self.sIntStep, self.eDoubleDefault)
        InputDialogWizardDialog.setTabOrder(self.eDoubleDefault, self.eDoubleFrom)
        InputDialogWizardDialog.setTabOrder(self.eDoubleFrom, self.eDoubleTo)
        InputDialogWizardDialog.setTabOrder(self.eDoubleTo, self.sDoubleDecimals)
        InputDialogWizardDialog.setTabOrder(self.sDoubleDecimals, self.eVariable)
        InputDialogWizardDialog.setTabOrder(self.eVariable, self.sCurrentItem)
        InputDialogWizardDialog.setTabOrder(self.sCurrentItem, self.cEditable)
        InputDialogWizardDialog.setTabOrder(self.cEditable, self.buttonBox)

    def retranslateUi(self, InputDialogWizardDialog):
        _translate = QtCore.QCoreApplication.translate
        InputDialogWizardDialog.setWindowTitle(_translate("InputDialogWizardDialog", "QInputDialog Wizard"))
        self.groupBox.setTitle(_translate("InputDialogWizardDialog", "Type"))
        self.rText.setText(_translate("InputDialogWizardDialog", "Text"))
        self.rInteger.setText(_translate("InputDialogWizardDialog", "Integer"))
        self.rDouble.setText(_translate("InputDialogWizardDialog", "Double"))
        self.rItem.setText(_translate("InputDialogWizardDialog", "Item"))
        self.label.setText(_translate("InputDialogWizardDialog", "Result:"))
        self.eResultVar.setToolTip(_translate("InputDialogWizardDialog", "Enter the result variable name"))
        self.TextLabel1.setText(_translate("InputDialogWizardDialog", "Title"))
        self.TextLabel2.setText(_translate("InputDialogWizardDialog", "Label"))
        self.parentGroup.setTitle(_translate("InputDialogWizardDialog", "Parent"))
        self.parentSelf.setToolTip(_translate("InputDialogWizardDialog", "Select \"self\" as parent"))
        self.parentSelf.setText(_translate("InputDialogWizardDialog", "self"))
        self.parentNone.setToolTip(_translate("InputDialogWizardDialog", "Select \"None\" as parent"))
        self.parentNone.setText(_translate("InputDialogWizardDialog", "None"))
        self.parentOther.setToolTip(_translate("InputDialogWizardDialog", "Select to enter a parent expression"))
        self.parentOther.setText(_translate("InputDialogWizardDialog", "Expression:"))
        self.parentEdit.setToolTip(_translate("InputDialogWizardDialog", "Enter the parent expression"))
        self.groupBox_2.setTitle(_translate("InputDialogWizardDialog", "Text"))
        self.groupBox_3.setTitle(_translate("InputDialogWizardDialog", "Echo Mode"))
        self.rEchoNormal.setText(_translate("InputDialogWizardDialog", "Normal"))
        self.rEchoNoEcho.setText(_translate("InputDialogWizardDialog", "No Echo"))
        self.rEchoPassword.setText(_translate("InputDialogWizardDialog", "Password"))
        self.TextLabel3.setText(_translate("InputDialogWizardDialog", "Default"))
        self.groupBox_4.setTitle(_translate("InputDialogWizardDialog", "Integer"))
        self.TextLabel4_4.setText(_translate("InputDialogWizardDialog", "Step"))
        self.TextLabel4_3.setText(_translate("InputDialogWizardDialog", "To"))
        self.TextLabel4_2.setText(_translate("InputDialogWizardDialog", "From"))
        self.TextLabel4.setText(_translate("InputDialogWizardDialog", "Default"))
        self.groupBox_5.setTitle(_translate("InputDialogWizardDialog", "Double"))
        self.eDoubleTo.setText(_translate("InputDialogWizardDialog", "2147483647"))
        self.eDoubleFrom.setText(_translate("InputDialogWizardDialog", "-2147483647"))
        self.eDoubleDefault.setText(_translate("InputDialogWizardDialog", "0"))
        self.TextLabel5.setText(_translate("InputDialogWizardDialog", "Default"))
        self.TextLabel6.setText(_translate("InputDialogWizardDialog", "From"))
        self.TextLabel7.setText(_translate("InputDialogWizardDialog", "To"))
        self.TextLabel8.setText(_translate("InputDialogWizardDialog", "Decimals"))
        self.groupBox_6.setTitle(_translate("InputDialogWizardDialog", "Item"))
        self.cEditable.setText(_translate("InputDialogWizardDialog", "Editable"))
        self.TextLabel10.setText(_translate("InputDialogWizardDialog", "Current Item"))
        self.TextLabel9.setText(_translate("InputDialogWizardDialog", "String List Variable"))
