# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\DocumentationPlugins\Ericdoc\EricdocConfigDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EricdocConfigDialog(object):
    def setupUi(self, EricdocConfigDialog):
        EricdocConfigDialog.setObjectName("EricdocConfigDialog")
        EricdocConfigDialog.resize(554, 550)
        EricdocConfigDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(EricdocConfigDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabWidget = QtWidgets.QTabWidget(EricdocConfigDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.generalTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.TextLabel6 = QtWidgets.QLabel(self.generalTab)
        self.TextLabel6.setObjectName("TextLabel6")
        self.horizontalLayout_2.addWidget(self.TextLabel6)
        self.outputDirPicker = E5PathPicker(self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputDirPicker.sizePolicy().hasHeightForWidth())
        self.outputDirPicker.setSizePolicy(sizePolicy)
        self.outputDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.outputDirPicker.setObjectName("outputDirPicker")
        self.horizontalLayout_2.addWidget(self.outputDirPicker)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1_3 = QtWidgets.QLabel(self.generalTab)
        self.textLabel1_3.setObjectName("textLabel1_3")
        self.hboxlayout.addWidget(self.textLabel1_3)
        self.sourceExtEdit = QtWidgets.QLineEdit(self.generalTab)
        self.sourceExtEdit.setObjectName("sourceExtEdit")
        self.hboxlayout.addWidget(self.sourceExtEdit)
        self.verticalLayout_2.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.recursionCheckBox = QtWidgets.QCheckBox(self.generalTab)
        self.recursionCheckBox.setObjectName("recursionCheckBox")
        self.hboxlayout1.addWidget(self.recursionCheckBox)
        self.noindexCheckBox = QtWidgets.QCheckBox(self.generalTab)
        self.noindexCheckBox.setObjectName("noindexCheckBox")
        self.hboxlayout1.addWidget(self.noindexCheckBox)
        spacerItem = QtWidgets.QSpacerItem(145, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.hboxlayout1)
        self.hboxlayout2 = QtWidgets.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")
        self.noemptyCheckBox = QtWidgets.QCheckBox(self.generalTab)
        self.noemptyCheckBox.setObjectName("noemptyCheckBox")
        self.hboxlayout2.addWidget(self.noemptyCheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.hboxlayout2)
        self.hboxlayout3 = QtWidgets.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")
        self.label = QtWidgets.QLabel(self.generalTab)
        self.label.setObjectName("label")
        self.hboxlayout3.addWidget(self.label)
        self.excludeFilesEdit = QtWidgets.QLineEdit(self.generalTab)
        self.excludeFilesEdit.setObjectName("excludeFilesEdit")
        self.hboxlayout3.addWidget(self.excludeFilesEdit)
        self.verticalLayout_2.addLayout(self.hboxlayout3)
        self.groupBox = QtWidgets.QGroupBox(self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.addButton = QtWidgets.QPushButton(self.groupBox)
        self.addButton.setObjectName("addButton")
        self.gridLayout_2.addWidget(self.addButton, 1, 1, 1, 1)
        self.deleteButton = QtWidgets.QPushButton(self.groupBox)
        self.deleteButton.setObjectName("deleteButton")
        self.gridLayout_2.addWidget(self.deleteButton, 1, 0, 1, 1)
        self.ignoreDirsList = QtWidgets.QListWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.ignoreDirsList.sizePolicy().hasHeightForWidth())
        self.ignoreDirsList.setSizePolicy(sizePolicy)
        self.ignoreDirsList.setAlternatingRowColors(True)
        self.ignoreDirsList.setObjectName("ignoreDirsList")
        self.gridLayout_2.addWidget(self.ignoreDirsList, 0, 0, 1, 3)
        self.ignoreDirPicker = E5PathPicker(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ignoreDirPicker.sizePolicy().hasHeightForWidth())
        self.ignoreDirPicker.setSizePolicy(sizePolicy)
        self.ignoreDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ignoreDirPicker.setObjectName("ignoreDirPicker")
        self.gridLayout_2.addWidget(self.ignoreDirPicker, 1, 2, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tabWidget.addTab(self.generalTab, "")
        self.styleTab = QtWidgets.QWidget()
        self.styleTab.setObjectName("styleTab")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.styleTab)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.groupBox_3 = QtWidgets.QGroupBox(self.styleTab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cssPicker = E5PathPicker(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cssPicker.sizePolicy().hasHeightForWidth())
        self.cssPicker.setSizePolicy(sizePolicy)
        self.cssPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.cssPicker.setObjectName("cssPicker")
        self.verticalLayout_3.addWidget(self.cssPicker)
        self.vboxlayout1.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.styleTab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName("gridlayout")
        self.cfBgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.cfBgButton.setObjectName("cfBgButton")
        self.gridlayout.addWidget(self.cfBgButton, 3, 1, 1, 1)
        self.cfFgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.cfFgButton.setObjectName("cfFgButton")
        self.gridlayout.addWidget(self.cfFgButton, 3, 0, 1, 1)
        self.l2BgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.l2BgButton.setObjectName("l2BgButton")
        self.gridlayout.addWidget(self.l2BgButton, 2, 1, 1, 1)
        self.l2FgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.l2FgButton.setObjectName("l2FgButton")
        self.gridlayout.addWidget(self.l2FgButton, 2, 0, 1, 1)
        self.l1BgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.l1BgButton.setObjectName("l1BgButton")
        self.gridlayout.addWidget(self.l1BgButton, 1, 1, 1, 1)
        self.l1FgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.l1FgButton.setObjectName("l1FgButton")
        self.gridlayout.addWidget(self.l1FgButton, 1, 0, 1, 1)
        self.bodyBgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.bodyBgButton.setObjectName("bodyBgButton")
        self.gridlayout.addWidget(self.bodyBgButton, 0, 1, 1, 1)
        self.bodyFgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.bodyFgButton.setObjectName("bodyFgButton")
        self.gridlayout.addWidget(self.bodyFgButton, 0, 0, 1, 1)
        self.linkFgButton = QtWidgets.QPushButton(self.groupBox_2)
        self.linkFgButton.setObjectName("linkFgButton")
        self.gridlayout.addWidget(self.linkFgButton, 4, 0, 1, 1)
        self.sample = QtWidgets.QTextEdit(self.groupBox_2)
        self.sample.setReadOnly(True)
        self.sample.setObjectName("sample")
        self.gridlayout.addWidget(self.sample, 5, 0, 1, 2)
        self.vboxlayout1.addWidget(self.groupBox_2)
        self.tabWidget.addTab(self.styleTab, "")
        self.qtHelpTab = QtWidgets.QWidget()
        self.qtHelpTab.setObjectName("qtHelpTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.qtHelpTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.qtHelpGroup = QtWidgets.QGroupBox(self.qtHelpTab)
        self.qtHelpGroup.setCheckable(True)
        self.qtHelpGroup.setChecked(False)
        self.qtHelpGroup.setObjectName("qtHelpGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.qtHelpGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.TextLabel6_2 = QtWidgets.QLabel(self.qtHelpGroup)
        self.TextLabel6_2.setObjectName("TextLabel6_2")
        self.gridLayout.addWidget(self.TextLabel6_2, 0, 0, 1, 1)
        self.qtHelpDirPicker = E5PathPicker(self.qtHelpGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qtHelpDirPicker.sizePolicy().hasHeightForWidth())
        self.qtHelpDirPicker.setSizePolicy(sizePolicy)
        self.qtHelpDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.qtHelpDirPicker.setObjectName("qtHelpDirPicker")
        self.gridLayout.addWidget(self.qtHelpDirPicker, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.qtHelpGroup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.qtHelpNamespaceEdit = QtWidgets.QLineEdit(self.qtHelpGroup)
        self.qtHelpNamespaceEdit.setObjectName("qtHelpNamespaceEdit")
        self.gridLayout.addWidget(self.qtHelpNamespaceEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.qtHelpGroup)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.qtHelpFolderEdit = QtWidgets.QLineEdit(self.qtHelpGroup)
        self.qtHelpFolderEdit.setObjectName("qtHelpFolderEdit")
        self.gridLayout.addWidget(self.qtHelpFolderEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.qtHelpGroup)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.qtHelpFilterNameEdit = QtWidgets.QLineEdit(self.qtHelpGroup)
        self.qtHelpFilterNameEdit.setObjectName("qtHelpFilterNameEdit")
        self.gridLayout.addWidget(self.qtHelpFilterNameEdit, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.qtHelpGroup)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.qtHelpFilterAttributesEdit = QtWidgets.QLineEdit(self.qtHelpGroup)
        self.qtHelpFilterAttributesEdit.setObjectName("qtHelpFilterAttributesEdit")
        self.gridLayout.addWidget(self.qtHelpFilterAttributesEdit, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.qtHelpGroup)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.qtHelpTitleEdit = QtWidgets.QLineEdit(self.qtHelpGroup)
        self.qtHelpTitleEdit.setObjectName("qtHelpTitleEdit")
        self.gridLayout.addWidget(self.qtHelpTitleEdit, 5, 1, 1, 1)
        self.qtHelpGenerateCollectionCheckBox = QtWidgets.QCheckBox(self.qtHelpGroup)
        self.qtHelpGenerateCollectionCheckBox.setObjectName("qtHelpGenerateCollectionCheckBox")
        self.gridLayout.addWidget(self.qtHelpGenerateCollectionCheckBox, 6, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 271, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 2)
        self.verticalLayout.addWidget(self.qtHelpGroup)
        self.tabWidget.addTab(self.qtHelpTab, "")
        self.vboxlayout.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(EricdocConfigDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(EricdocConfigDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(EricdocConfigDialog.accept)
        self.buttonBox.rejected.connect(EricdocConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EricdocConfigDialog)
        EricdocConfigDialog.setTabOrder(self.tabWidget, self.outputDirPicker)
        EricdocConfigDialog.setTabOrder(self.outputDirPicker, self.sourceExtEdit)
        EricdocConfigDialog.setTabOrder(self.sourceExtEdit, self.recursionCheckBox)
        EricdocConfigDialog.setTabOrder(self.recursionCheckBox, self.noindexCheckBox)
        EricdocConfigDialog.setTabOrder(self.noindexCheckBox, self.noemptyCheckBox)
        EricdocConfigDialog.setTabOrder(self.noemptyCheckBox, self.excludeFilesEdit)
        EricdocConfigDialog.setTabOrder(self.excludeFilesEdit, self.ignoreDirsList)
        EricdocConfigDialog.setTabOrder(self.ignoreDirsList, self.ignoreDirPicker)
        EricdocConfigDialog.setTabOrder(self.ignoreDirPicker, self.addButton)
        EricdocConfigDialog.setTabOrder(self.addButton, self.deleteButton)
        EricdocConfigDialog.setTabOrder(self.deleteButton, self.cssPicker)
        EricdocConfigDialog.setTabOrder(self.cssPicker, self.bodyFgButton)
        EricdocConfigDialog.setTabOrder(self.bodyFgButton, self.bodyBgButton)
        EricdocConfigDialog.setTabOrder(self.bodyBgButton, self.l1FgButton)
        EricdocConfigDialog.setTabOrder(self.l1FgButton, self.l1BgButton)
        EricdocConfigDialog.setTabOrder(self.l1BgButton, self.l2FgButton)
        EricdocConfigDialog.setTabOrder(self.l2FgButton, self.l2BgButton)
        EricdocConfigDialog.setTabOrder(self.l2BgButton, self.cfFgButton)
        EricdocConfigDialog.setTabOrder(self.cfFgButton, self.cfBgButton)
        EricdocConfigDialog.setTabOrder(self.cfBgButton, self.linkFgButton)
        EricdocConfigDialog.setTabOrder(self.linkFgButton, self.sample)
        EricdocConfigDialog.setTabOrder(self.sample, self.qtHelpGroup)
        EricdocConfigDialog.setTabOrder(self.qtHelpGroup, self.qtHelpDirPicker)
        EricdocConfigDialog.setTabOrder(self.qtHelpDirPicker, self.qtHelpNamespaceEdit)
        EricdocConfigDialog.setTabOrder(self.qtHelpNamespaceEdit, self.qtHelpFolderEdit)
        EricdocConfigDialog.setTabOrder(self.qtHelpFolderEdit, self.qtHelpFilterNameEdit)
        EricdocConfigDialog.setTabOrder(self.qtHelpFilterNameEdit, self.qtHelpFilterAttributesEdit)
        EricdocConfigDialog.setTabOrder(self.qtHelpFilterAttributesEdit, self.qtHelpTitleEdit)
        EricdocConfigDialog.setTabOrder(self.qtHelpTitleEdit, self.qtHelpGenerateCollectionCheckBox)

    def retranslateUi(self, EricdocConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        EricdocConfigDialog.setWindowTitle(_translate("EricdocConfigDialog", "Ericdoc Configuration"))
        self.TextLabel6.setText(_translate("EricdocConfigDialog", "Output Directory:"))
        self.outputDirPicker.setToolTip(_translate("EricdocConfigDialog", "Enter an output directory"))
        self.textLabel1_3.setText(_translate("EricdocConfigDialog", "Additional source extensions:"))
        self.sourceExtEdit.setToolTip(_translate("EricdocConfigDialog", "Enter additional source extensions separated by a comma"))
        self.recursionCheckBox.setToolTip(_translate("EricdocConfigDialog", "Select to recurse into subdirectories"))
        self.recursionCheckBox.setText(_translate("EricdocConfigDialog", "Recurse into subdirectories"))
        self.noindexCheckBox.setToolTip(_translate("EricdocConfigDialog", "Select, if no index files should be generated"))
        self.noindexCheckBox.setText(_translate("EricdocConfigDialog", "Don\'t generate index files"))
        self.noemptyCheckBox.setToolTip(_translate("EricdocConfigDialog", "Select to exclude empty modules"))
        self.noemptyCheckBox.setText(_translate("EricdocConfigDialog", "Don\'t include empty modules"))
        self.label.setText(_translate("EricdocConfigDialog", "Exclude Files:"))
        self.excludeFilesEdit.setToolTip(_translate("EricdocConfigDialog", "Enter filename patterns of files to be excluded separated by a comma"))
        self.groupBox.setTitle(_translate("EricdocConfigDialog", "Exclude Directories"))
        self.addButton.setToolTip(_translate("EricdocConfigDialog", "Press to add the entered directory to the list"))
        self.addButton.setText(_translate("EricdocConfigDialog", "Add"))
        self.deleteButton.setToolTip(_translate("EricdocConfigDialog", "Press to delete the selected directory from the list"))
        self.deleteButton.setText(_translate("EricdocConfigDialog", "Delete"))
        self.ignoreDirsList.setToolTip(_translate("EricdocConfigDialog", "List of directory basenames to be ignored"))
        self.ignoreDirPicker.setToolTip(_translate("EricdocConfigDialog", "Enter a directory basename to be ignored"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("EricdocConfigDialog", "General"))
        self.groupBox_3.setTitle(_translate("EricdocConfigDialog", "Style Sheet"))
        self.cssPicker.setToolTip(_translate("EricdocConfigDialog", "Enter the filename of a CSS style sheet. Leave empty to use the colors defined below."))
        self.groupBox_2.setTitle(_translate("EricdocConfigDialog", "Colors"))
        self.cfBgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the class and function header background color."))
        self.cfBgButton.setText(_translate("EricdocConfigDialog", "Class/Function Header Background"))
        self.cfFgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the class and function header foreground color."))
        self.cfFgButton.setText(_translate("EricdocConfigDialog", "Class/Function Header Foreground"))
        self.l2BgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the level 2 header background color."))
        self.l2BgButton.setText(_translate("EricdocConfigDialog", "Level 2 Header Background"))
        self.l2FgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the level 2 header foreground color."))
        self.l2FgButton.setText(_translate("EricdocConfigDialog", "Level 2 Header Foreground"))
        self.l1BgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the level 1 header background color."))
        self.l1BgButton.setText(_translate("EricdocConfigDialog", "Level 1 Header Background"))
        self.l1FgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the level 1 header foreground color."))
        self.l1FgButton.setText(_translate("EricdocConfigDialog", "Level 1 Header Foreground"))
        self.bodyBgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the body background color."))
        self.bodyBgButton.setText(_translate("EricdocConfigDialog", "Body Background"))
        self.bodyFgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the body foreground color."))
        self.bodyFgButton.setText(_translate("EricdocConfigDialog", "Body Foreground"))
        self.linkFgButton.setToolTip(_translate("EricdocConfigDialog", "Press to select the foreground color of links."))
        self.linkFgButton.setText(_translate("EricdocConfigDialog", "Links"))
        self.sample.setToolTip(_translate("EricdocConfigDialog", "This shows an example of the selected colors."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.styleTab), _translate("EricdocConfigDialog", "Style"))
        self.qtHelpGroup.setTitle(_translate("EricdocConfigDialog", "Generate QtHelp Files"))
        self.TextLabel6_2.setText(_translate("EricdocConfigDialog", "Output Directory:"))
        self.qtHelpDirPicker.setToolTip(_translate("EricdocConfigDialog", "Enter an output directory"))
        self.label_2.setText(_translate("EricdocConfigDialog", "Namespace:"))
        self.qtHelpNamespaceEdit.setToolTip(_translate("EricdocConfigDialog", "Enter the namespace"))
        self.label_3.setText(_translate("EricdocConfigDialog", "Virtual Folder:"))
        self.qtHelpFolderEdit.setToolTip(_translate("EricdocConfigDialog", "Enter the name of the virtual folder (must not contain \'/\')"))
        self.label_4.setText(_translate("EricdocConfigDialog", "Filter Name:"))
        self.qtHelpFilterNameEdit.setToolTip(_translate("EricdocConfigDialog", "Enter the name of the custom filter"))
        self.label_5.setText(_translate("EricdocConfigDialog", "Filter Attributes:"))
        self.qtHelpFilterAttributesEdit.setToolTip(_translate("EricdocConfigDialog", "Enter the filter attributes separated by \':\'"))
        self.label_6.setText(_translate("EricdocConfigDialog", "Title:"))
        self.qtHelpTitleEdit.setToolTip(_translate("EricdocConfigDialog", "Enter a short title for the top entry"))
        self.qtHelpGenerateCollectionCheckBox.setToolTip(_translate("EricdocConfigDialog", "Select to generate the QtHelp collection files"))
        self.qtHelpGenerateCollectionCheckBox.setText(_translate("EricdocConfigDialog", "Generate QtHelp collection files"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.qtHelpTab), _translate("EricdocConfigDialog", "QtHelp"))
from E5Gui.E5PathPicker import E5PathPicker
