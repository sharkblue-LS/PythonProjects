# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\WizardPlugins\EricPluginWizard\PluginWizardDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginWizardDialog(object):
    def setupUi(self, PluginWizardDialog):
        PluginWizardDialog.setObjectName("PluginWizardDialog")
        PluginWizardDialog.resize(700, 600)
        PluginWizardDialog.setSizeGripEnabled(True)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(PluginWizardDialog)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.dataTabWidget = QtWidgets.QTabWidget(PluginWizardDialog)
        self.dataTabWidget.setObjectName("dataTabWidget")
        self.headerTab = QtWidgets.QWidget()
        self.headerTab.setObjectName("headerTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.headerTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.headerTab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(self.headerTab)
        self.nameEdit.setMaxLength(55)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.headerTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.versionEdit = QtWidgets.QLineEdit(self.headerTab)
        self.versionEdit.setMaxLength(10)
        self.versionEdit.setObjectName("versionEdit")
        self.gridLayout.addWidget(self.versionEdit, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.headerTab)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.authorEdit = QtWidgets.QLineEdit(self.headerTab)
        self.authorEdit.setMaxLength(55)
        self.authorEdit.setObjectName("authorEdit")
        self.gridLayout.addWidget(self.authorEdit, 2, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.headerTab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.authorEmailEdit = QtWidgets.QLineEdit(self.headerTab)
        self.authorEmailEdit.setInputMask("")
        self.authorEmailEdit.setMaxLength(55)
        self.authorEmailEdit.setObjectName("authorEmailEdit")
        self.gridLayout.addWidget(self.authorEmailEdit, 3, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.headerTab)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.classNameEdit = QtWidgets.QLineEdit(self.headerTab)
        self.classNameEdit.setMaxLength(55)
        self.classNameEdit.setObjectName("classNameEdit")
        self.gridLayout.addWidget(self.classNameEdit, 4, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.headerTab)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.packageNameEdit = QtWidgets.QLineEdit(self.headerTab)
        self.packageNameEdit.setMaxLength(55)
        self.packageNameEdit.setObjectName("packageNameEdit")
        self.gridLayout.addWidget(self.packageNameEdit, 5, 1, 1, 1)
        self.createPackageCheckBox = QtWidgets.QCheckBox(self.headerTab)
        self.createPackageCheckBox.setChecked(True)
        self.createPackageCheckBox.setObjectName("createPackageCheckBox")
        self.gridLayout.addWidget(self.createPackageCheckBox, 5, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.headerTab)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.shortDescriptionEdit = QtWidgets.QLineEdit(self.headerTab)
        self.shortDescriptionEdit.setMaxLength(55)
        self.shortDescriptionEdit.setObjectName("shortDescriptionEdit")
        self.gridLayout.addWidget(self.shortDescriptionEdit, 6, 1, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.headerTab)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.longDescriptionEdit = QtWidgets.QPlainTextEdit(self.headerTab)
        self.longDescriptionEdit.setTabChangesFocus(True)
        self.longDescriptionEdit.setObjectName("longDescriptionEdit")
        self.gridLayout.addWidget(self.longDescriptionEdit, 7, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.autoActivateCheckBox = QtWidgets.QCheckBox(self.headerTab)
        self.autoActivateCheckBox.setChecked(True)
        self.autoActivateCheckBox.setObjectName("autoActivateCheckBox")
        self.gridLayout_2.addWidget(self.autoActivateCheckBox, 0, 0, 1, 1)
        self.deactivateableCheckBox = QtWidgets.QCheckBox(self.headerTab)
        self.deactivateableCheckBox.setChecked(True)
        self.deactivateableCheckBox.setObjectName("deactivateableCheckBox")
        self.gridLayout_2.addWidget(self.deactivateableCheckBox, 0, 1, 1, 1)
        self.restartCheckBox = QtWidgets.QCheckBox(self.headerTab)
        self.restartCheckBox.setObjectName("restartCheckBox")
        self.gridLayout_2.addWidget(self.restartCheckBox, 1, 0, 1, 1)
        self.python2CheckBox = QtWidgets.QCheckBox(self.headerTab)
        self.python2CheckBox.setChecked(True)
        self.python2CheckBox.setObjectName("python2CheckBox")
        self.gridLayout_2.addWidget(self.python2CheckBox, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.ondemandFrame = QtWidgets.QFrame(self.headerTab)
        self.ondemandFrame.setEnabled(False)
        self.ondemandFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ondemandFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ondemandFrame.setObjectName("ondemandFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.ondemandFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_10 = QtWidgets.QLabel(self.ondemandFrame)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)
        self.pluginTypeCombo = QtWidgets.QComboBox(self.ondemandFrame)
        self.pluginTypeCombo.setObjectName("pluginTypeCombo")
        self.gridLayout_4.addWidget(self.pluginTypeCombo, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(406, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.ondemandFrame)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)
        self.pluginTypeNameEdit = QtWidgets.QLineEdit(self.ondemandFrame)
        self.pluginTypeNameEdit.setMaxLength(55)
        self.pluginTypeNameEdit.setObjectName("pluginTypeNameEdit")
        self.gridLayout_4.addWidget(self.pluginTypeNameEdit, 1, 1, 1, 2)
        self.verticalLayout.addWidget(self.ondemandFrame)
        self.dataTabWidget.addTab(self.headerTab, "")
        self.configTab = QtWidgets.QWidget()
        self.configTab.setObjectName("configTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.configTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.configurationGroup = QtWidgets.QGroupBox(self.configTab)
        self.configurationGroup.setCheckable(True)
        self.configurationGroup.setChecked(False)
        self.configurationGroup.setObjectName("configurationGroup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.configurationGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_9 = QtWidgets.QLabel(self.configurationGroup)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.preferencesKeyEdit = QtWidgets.QLineEdit(self.configurationGroup)
        self.preferencesKeyEdit.setMaxLength(55)
        self.preferencesKeyEdit.setObjectName("preferencesKeyEdit")
        self.gridLayout_3.addWidget(self.preferencesKeyEdit, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 416, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.configurationGroup)
        self.dataTabWidget.addTab(self.configTab, "")
        self.variousTab = QtWidgets.QWidget()
        self.variousTab.setObjectName("variousTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.variousTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pixmapCheckBox = QtWidgets.QCheckBox(self.variousTab)
        self.pixmapCheckBox.setObjectName("pixmapCheckBox")
        self.verticalLayout_4.addWidget(self.pixmapCheckBox)
        self.moduleSetupCheckBox = QtWidgets.QCheckBox(self.variousTab)
        self.moduleSetupCheckBox.setObjectName("moduleSetupCheckBox")
        self.verticalLayout_4.addWidget(self.moduleSetupCheckBox)
        self.exeGroup = QtWidgets.QGroupBox(self.variousTab)
        self.exeGroup.setCheckable(True)
        self.exeGroup.setChecked(False)
        self.exeGroup.setObjectName("exeGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.exeGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.exeRadioButton = QtWidgets.QRadioButton(self.exeGroup)
        self.exeRadioButton.setChecked(True)
        self.exeRadioButton.setObjectName("exeRadioButton")
        self.verticalLayout_2.addWidget(self.exeRadioButton)
        self.exeInfoRadioButton = QtWidgets.QRadioButton(self.exeGroup)
        self.exeInfoRadioButton.setObjectName("exeInfoRadioButton")
        self.verticalLayout_2.addWidget(self.exeInfoRadioButton)
        self.exeListRadioButton = QtWidgets.QRadioButton(self.exeGroup)
        self.exeListRadioButton.setObjectName("exeListRadioButton")
        self.verticalLayout_2.addWidget(self.exeListRadioButton)
        self.verticalLayout_4.addWidget(self.exeGroup)
        self.apiFilesCheckBox = QtWidgets.QCheckBox(self.variousTab)
        self.apiFilesCheckBox.setObjectName("apiFilesCheckBox")
        self.verticalLayout_4.addWidget(self.apiFilesCheckBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 377, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.dataTabWidget.addTab(self.variousTab, "")
        self.verticalLayout_5.addWidget(self.dataTabWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.projectButton = QtWidgets.QPushButton(PluginWizardDialog)
        self.projectButton.setObjectName("projectButton")
        self.horizontalLayout.addWidget(self.projectButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.buttonBox = QtWidgets.QDialogButtonBox(PluginWizardDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.retranslateUi(PluginWizardDialog)
        self.dataTabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(PluginWizardDialog.accept)
        self.buttonBox.rejected.connect(PluginWizardDialog.reject)
        self.autoActivateCheckBox.toggled['bool'].connect(self.ondemandFrame.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(PluginWizardDialog)
        PluginWizardDialog.setTabOrder(self.projectButton, self.dataTabWidget)
        PluginWizardDialog.setTabOrder(self.dataTabWidget, self.nameEdit)
        PluginWizardDialog.setTabOrder(self.nameEdit, self.versionEdit)
        PluginWizardDialog.setTabOrder(self.versionEdit, self.authorEdit)
        PluginWizardDialog.setTabOrder(self.authorEdit, self.authorEmailEdit)
        PluginWizardDialog.setTabOrder(self.authorEmailEdit, self.classNameEdit)
        PluginWizardDialog.setTabOrder(self.classNameEdit, self.packageNameEdit)
        PluginWizardDialog.setTabOrder(self.packageNameEdit, self.createPackageCheckBox)
        PluginWizardDialog.setTabOrder(self.createPackageCheckBox, self.shortDescriptionEdit)
        PluginWizardDialog.setTabOrder(self.shortDescriptionEdit, self.longDescriptionEdit)
        PluginWizardDialog.setTabOrder(self.longDescriptionEdit, self.autoActivateCheckBox)
        PluginWizardDialog.setTabOrder(self.autoActivateCheckBox, self.deactivateableCheckBox)
        PluginWizardDialog.setTabOrder(self.deactivateableCheckBox, self.restartCheckBox)
        PluginWizardDialog.setTabOrder(self.restartCheckBox, self.python2CheckBox)
        PluginWizardDialog.setTabOrder(self.python2CheckBox, self.pluginTypeCombo)
        PluginWizardDialog.setTabOrder(self.pluginTypeCombo, self.pluginTypeNameEdit)
        PluginWizardDialog.setTabOrder(self.pluginTypeNameEdit, self.configurationGroup)
        PluginWizardDialog.setTabOrder(self.configurationGroup, self.preferencesKeyEdit)
        PluginWizardDialog.setTabOrder(self.preferencesKeyEdit, self.pixmapCheckBox)
        PluginWizardDialog.setTabOrder(self.pixmapCheckBox, self.moduleSetupCheckBox)
        PluginWizardDialog.setTabOrder(self.moduleSetupCheckBox, self.exeGroup)
        PluginWizardDialog.setTabOrder(self.exeGroup, self.exeRadioButton)
        PluginWizardDialog.setTabOrder(self.exeRadioButton, self.exeInfoRadioButton)
        PluginWizardDialog.setTabOrder(self.exeInfoRadioButton, self.exeListRadioButton)
        PluginWizardDialog.setTabOrder(self.exeListRadioButton, self.apiFilesCheckBox)

    def retranslateUi(self, PluginWizardDialog):
        _translate = QtCore.QCoreApplication.translate
        PluginWizardDialog.setWindowTitle(_translate("PluginWizardDialog", "eric Plug-in Wizard"))
        self.label.setText(_translate("PluginWizardDialog", "Plug-in Name:"))
        self.nameEdit.setToolTip(_translate("PluginWizardDialog", "Enter the plug-in name"))
        self.label_2.setText(_translate("PluginWizardDialog", "Version:"))
        self.versionEdit.setToolTip(_translate("PluginWizardDialog", "Enter the version number in the form \'major.minor[.patch[.sub]]\'"))
        self.label_3.setText(_translate("PluginWizardDialog", "Author:"))
        self.authorEdit.setToolTip(_translate("PluginWizardDialog", "Enter the author\'s name"))
        self.label_4.setText(_translate("PluginWizardDialog", "Author Email:"))
        self.authorEmailEdit.setToolTip(_translate("PluginWizardDialog", "Enter the author\'s email address"))
        self.label_5.setText(_translate("PluginWizardDialog", "Class Name:"))
        self.classNameEdit.setToolTip(_translate("PluginWizardDialog", "Enter the name of the plug-in class"))
        self.label_6.setText(_translate("PluginWizardDialog", "Package Name:"))
        self.packageNameEdit.setToolTip(_translate("PluginWizardDialog", "Enter the name of the plug-in package"))
        self.createPackageCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to create the entered package"))
        self.createPackageCheckBox.setText(_translate("PluginWizardDialog", "Create Package"))
        self.label_7.setText(_translate("PluginWizardDialog", "Short Description:"))
        self.shortDescriptionEdit.setToolTip(_translate("PluginWizardDialog", "Enter the short description"))
        self.label_8.setText(_translate("PluginWizardDialog", "Long Description:"))
        self.longDescriptionEdit.setToolTip(_translate("PluginWizardDialog", "Enter the long description"))
        self.autoActivateCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to activate the plug-in automatically"))
        self.autoActivateCheckBox.setText(_translate("PluginWizardDialog", "Activate Automatically"))
        self.deactivateableCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to allow the plug-in to be deactivated"))
        self.deactivateableCheckBox.setText(_translate("PluginWizardDialog", "Can be deactivated"))
        self.restartCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to indicate a restart is needed when updated"))
        self.restartCheckBox.setText(_translate("PluginWizardDialog", "Needs Restart"))
        self.python2CheckBox.setToolTip(_translate("PluginWizardDialog", "Select to indicate Python 2 compatibility"))
        self.python2CheckBox.setText(_translate("PluginWizardDialog", "Python 2 compatible"))
        self.label_10.setText(_translate("PluginWizardDialog", "Plug-in Type:"))
        self.pluginTypeCombo.setToolTip(_translate("PluginWizardDialog", "Select the plug-in type"))
        self.label_11.setText(_translate("PluginWizardDialog", "Plug-in Type Name:"))
        self.pluginTypeNameEdit.setToolTip(_translate("PluginWizardDialog", "Enter the plug-in type name"))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.headerTab), _translate("PluginWizardDialog", "Header"))
        self.configurationGroup.setToolTip(_translate("PluginWizardDialog", "Select to indicate that the plug-in has configurable data"))
        self.configurationGroup.setTitle(_translate("PluginWizardDialog", "Is configurable"))
        self.label_9.setText(_translate("PluginWizardDialog", "Preferences Key:"))
        self.preferencesKeyEdit.setToolTip(_translate("PluginWizardDialog", "Enter the preferences key"))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.configTab), _translate("PluginWizardDialog", "Configuration"))
        self.pixmapCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to create a \'previewPix()\' function skeleton"))
        self.pixmapCheckBox.setText(_translate("PluginWizardDialog", "Include \'previewPix()\' function"))
        self.moduleSetupCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to create a \'moduleSetup()\' function skeleton"))
        self.moduleSetupCheckBox.setText(_translate("PluginWizardDialog", "Include \'moduleSetup()\' function"))
        self.exeGroup.setTitle(_translate("PluginWizardDialog", "Include an \'exeDisplayData\' function"))
        self.exeRadioButton.setToolTip(_translate("PluginWizardDialog", "Select to create an \'exeDisplayData()\' function skeleton"))
        self.exeRadioButton.setText(_translate("PluginWizardDialog", "\'exeDisplayData()\' function returning program data to determine version information"))
        self.exeInfoRadioButton.setToolTip(_translate("PluginWizardDialog", "Select to create an \'exeDisplayData()\' function skeleton returning version info"))
        self.exeInfoRadioButton.setText(_translate("PluginWizardDialog", "\'exeDisplayData()\' function returning version information"))
        self.exeListRadioButton.setToolTip(_translate("PluginWizardDialog", "Select to create an \'exeDisplayDataList()\' function skeleton"))
        self.exeListRadioButton.setText(_translate("PluginWizardDialog", "\'exeDisplayDataList()\' function"))
        self.apiFilesCheckBox.setToolTip(_translate("PluginWizardDialog", "Select to create an \'apiFiles()\' function skeleton"))
        self.apiFilesCheckBox.setText(_translate("PluginWizardDialog", "Include \'apiFiles()\' function"))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.variousTab), _translate("PluginWizardDialog", "Various"))
        self.projectButton.setToolTip(_translate("PluginWizardDialog", "Press to populate entry fields from project data"))
        self.projectButton.setText(_translate("PluginWizardDialog", "Populate from Project"))
