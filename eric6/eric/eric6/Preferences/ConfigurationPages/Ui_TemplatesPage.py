# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\TemplatesPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TemplatesPage(object):
    def setupUi(self, TemplatesPage):
        TemplatesPage.setObjectName("TemplatesPage")
        TemplatesPage.resize(414, 478)
        self.verticalLayout = QtWidgets.QVBoxLayout(TemplatesPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(TemplatesPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line11_2_2_2_2_2 = QtWidgets.QFrame(TemplatesPage)
        self.line11_2_2_2_2_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line11_2_2_2_2_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line11_2_2_2_2_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line11_2_2_2_2_2.setObjectName("line11_2_2_2_2_2")
        self.verticalLayout.addWidget(self.line11_2_2_2_2_2)
        self.groupBox = QtWidgets.QGroupBox(TemplatesPage)
        self.groupBox.setObjectName("groupBox")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.vboxlayout.setObjectName("vboxlayout")
        self.templatesAutoOpenGroupsCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.templatesAutoOpenGroupsCheckBox.setObjectName("templatesAutoOpenGroupsCheckBox")
        self.vboxlayout.addWidget(self.templatesAutoOpenGroupsCheckBox)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(TemplatesPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1_19 = QtWidgets.QLabel(self.groupBox_2)
        self.textLabel1_19.setObjectName("textLabel1_19")
        self.hboxlayout.addWidget(self.textLabel1_19)
        self.templatesSeparatorCharEdit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.templatesSeparatorCharEdit.sizePolicy().hasHeightForWidth())
        self.templatesSeparatorCharEdit.setSizePolicy(sizePolicy)
        self.templatesSeparatorCharEdit.setMaxLength(1)
        self.templatesSeparatorCharEdit.setObjectName("templatesSeparatorCharEdit")
        self.hboxlayout.addWidget(self.templatesSeparatorCharEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.vboxlayout2 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.templatesMultiDialogButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.templatesMultiDialogButton.setObjectName("templatesMultiDialogButton")
        self.vboxlayout2.addWidget(self.templatesMultiDialogButton)
        self.templatesSingleDialogButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.templatesSingleDialogButton.setObjectName("templatesSingleDialogButton")
        self.vboxlayout2.addWidget(self.templatesSingleDialogButton)
        self.vboxlayout1.addWidget(self.groupBox_3)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(TemplatesPage)
        self.groupBox_4.setObjectName("groupBox_4")
        self.vboxlayout3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.vboxlayout3.setObjectName("vboxlayout3")
        self.templatesToolTipCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.templatesToolTipCheckBox.setObjectName("templatesToolTipCheckBox")
        self.vboxlayout3.addWidget(self.templatesToolTipCheckBox)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox_5 = QtWidgets.QGroupBox(TemplatesPage)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName("gridLayout")
        self.editorFontButton = QtWidgets.QPushButton(self.groupBox_5)
        self.editorFontButton.setObjectName("editorFontButton")
        self.gridLayout.addWidget(self.editorFontButton, 0, 0, 1, 1)
        self.editorFontSample = QtWidgets.QLineEdit(self.groupBox_5)
        self.editorFontSample.setFocusPolicy(QtCore.Qt.NoFocus)
        self.editorFontSample.setAlignment(QtCore.Qt.AlignHCenter)
        self.editorFontSample.setReadOnly(True)
        self.editorFontSample.setObjectName("editorFontSample")
        self.gridLayout.addWidget(self.editorFontSample, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_5)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(TemplatesPage)
        QtCore.QMetaObject.connectSlotsByName(TemplatesPage)
        TemplatesPage.setTabOrder(self.templatesAutoOpenGroupsCheckBox, self.templatesSeparatorCharEdit)
        TemplatesPage.setTabOrder(self.templatesSeparatorCharEdit, self.templatesMultiDialogButton)
        TemplatesPage.setTabOrder(self.templatesMultiDialogButton, self.templatesSingleDialogButton)
        TemplatesPage.setTabOrder(self.templatesSingleDialogButton, self.templatesToolTipCheckBox)

    def retranslateUi(self, TemplatesPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("TemplatesPage", "<b>Configure Templates</b>"))
        self.groupBox.setTitle(_translate("TemplatesPage", "Groups"))
        self.templatesAutoOpenGroupsCheckBox.setToolTip(_translate("TemplatesPage", "Select, if groups having entries should be opened automatically"))
        self.templatesAutoOpenGroupsCheckBox.setText(_translate("TemplatesPage", "Expand groups automatically"))
        self.groupBox_2.setTitle(_translate("TemplatesPage", "Variables"))
        self.textLabel1_19.setText(_translate("TemplatesPage", "Separator:"))
        self.templatesSeparatorCharEdit.setToolTip(_translate("TemplatesPage", "Enter the character that encloses variables"))
        self.groupBox_3.setTitle(_translate("TemplatesPage", "Input method for variables"))
        self.templatesMultiDialogButton.setToolTip(_translate("TemplatesPage", "Select, if a new dialog should be opened for every template variable"))
        self.templatesMultiDialogButton.setText(_translate("TemplatesPage", "One dialog per template variable"))
        self.templatesSingleDialogButton.setToolTip(_translate("TemplatesPage", "Select, if only one dialog for all template variables should be shown"))
        self.templatesSingleDialogButton.setText(_translate("TemplatesPage", "One dialog for all template variables"))
        self.groupBox_4.setTitle(_translate("TemplatesPage", "Tooltips"))
        self.templatesToolTipCheckBox.setToolTip(_translate("TemplatesPage", "Select, if the template text should be shown in a tooltip"))
        self.templatesToolTipCheckBox.setText(_translate("TemplatesPage", "Show template text in tooltip"))
        self.groupBox_5.setTitle(_translate("TemplatesPage", "Template Editor"))
        self.editorFontButton.setToolTip(_translate("TemplatesPage", "Press to select the font to be used for the code editor"))
        self.editorFontButton.setText(_translate("TemplatesPage", "Editor Font"))
        self.editorFontSample.setText(_translate("TemplatesPage", "Template Code Editor"))
