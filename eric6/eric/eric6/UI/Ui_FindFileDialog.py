# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\UI\FindFileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FindFileDialog(object):
    def setupUi(self, FindFileDialog):
        FindFileDialog.setObjectName("FindFileDialog")
        FindFileDialog.resize(600, 800)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(FindFileDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.TextLabel1 = QtWidgets.QLabel(FindFileDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.gridLayout_3.addWidget(self.TextLabel1, 0, 0, 1, 1)
        self.findtextCombo = QtWidgets.QComboBox(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findtextCombo.sizePolicy().hasHeightForWidth())
        self.findtextCombo.setSizePolicy(sizePolicy)
        self.findtextCombo.setEditable(True)
        self.findtextCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.findtextCombo.setDuplicatesEnabled(False)
        self.findtextCombo.setObjectName("findtextCombo")
        self.gridLayout_3.addWidget(self.findtextCombo, 0, 1, 1, 1)
        self.replaceLabel = QtWidgets.QLabel(FindFileDialog)
        self.replaceLabel.setObjectName("replaceLabel")
        self.gridLayout_3.addWidget(self.replaceLabel, 1, 0, 1, 1)
        self.replacetextCombo = QtWidgets.QComboBox(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.replacetextCombo.sizePolicy().hasHeightForWidth())
        self.replacetextCombo.setSizePolicy(sizePolicy)
        self.replacetextCombo.setEditable(True)
        self.replacetextCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.replacetextCombo.setDuplicatesEnabled(False)
        self.replacetextCombo.setObjectName("replacetextCombo")
        self.gridLayout_3.addWidget(self.replacetextCombo, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.caseCheckBox = QtWidgets.QCheckBox(FindFileDialog)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.horizontalLayout_2.addWidget(self.caseCheckBox)
        self.wordCheckBox = QtWidgets.QCheckBox(FindFileDialog)
        self.wordCheckBox.setObjectName("wordCheckBox")
        self.horizontalLayout_2.addWidget(self.wordCheckBox)
        self.regexpCheckBox = QtWidgets.QCheckBox(FindFileDialog)
        self.regexpCheckBox.setObjectName("regexpCheckBox")
        self.horizontalLayout_2.addWidget(self.regexpCheckBox)
        self.feelLikeCheckBox = QtWidgets.QCheckBox(FindFileDialog)
        self.feelLikeCheckBox.setObjectName("feelLikeCheckBox")
        self.horizontalLayout_2.addWidget(self.feelLikeCheckBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(FindFileDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.sourcesCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.sourcesCheckBox.setChecked(True)
        self.sourcesCheckBox.setObjectName("sourcesCheckBox")
        self.gridLayout.addWidget(self.sourcesCheckBox, 0, 0, 1, 1)
        self.interfacesCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.interfacesCheckBox.setObjectName("interfacesCheckBox")
        self.gridLayout.addWidget(self.interfacesCheckBox, 0, 1, 1, 1)
        self.formsCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.formsCheckBox.setObjectName("formsCheckBox")
        self.gridLayout.addWidget(self.formsCheckBox, 1, 0, 1, 1)
        self.protocolsCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.protocolsCheckBox.setObjectName("protocolsCheckBox")
        self.gridLayout.addWidget(self.protocolsCheckBox, 1, 1, 1, 1)
        self.resourcesCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.resourcesCheckBox.setObjectName("resourcesCheckBox")
        self.gridLayout.addWidget(self.resourcesCheckBox, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filterCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.filterCheckBox.setObjectName("filterCheckBox")
        self.horizontalLayout.addWidget(self.filterCheckBox)
        self.filterEdit = QtWidgets.QLineEdit(self.groupBox)
        self.filterEdit.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterEdit.sizePolicy().hasHeightForWidth())
        self.filterEdit.setSizePolicy(sizePolicy)
        self.filterEdit.setObjectName("filterEdit")
        self.horizontalLayout.addWidget(self.filterEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 2)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.projectButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.projectButton.setChecked(True)
        self.projectButton.setObjectName("projectButton")
        self.horizontalLayout_3.addWidget(self.projectButton)
        self.dirButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.dirButton.setObjectName("dirButton")
        self.horizontalLayout_3.addWidget(self.dirButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.dirPicker = E5ComboPathPicker(self.groupBox_2)
        self.dirPicker.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dirPicker.sizePolicy().hasHeightForWidth())
        self.dirPicker.setSizePolicy(sizePolicy)
        self.dirPicker.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.dirPicker.setObjectName("dirPicker")
        self.verticalLayout.addWidget(self.dirPicker)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.openFilesButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.openFilesButton.setObjectName("openFilesButton")
        self.horizontalLayout_5.addWidget(self.openFilesButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.excludeHiddenCheckBox = QtWidgets.QCheckBox(FindFileDialog)
        self.excludeHiddenCheckBox.setChecked(True)
        self.excludeHiddenCheckBox.setObjectName("excludeHiddenCheckBox")
        self.verticalLayout_2.addWidget(self.excludeHiddenCheckBox)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.findProgressLabel = E5SqueezeLabelPath(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findProgressLabel.sizePolicy().hasHeightForWidth())
        self.findProgressLabel.setSizePolicy(sizePolicy)
        self.findProgressLabel.setText("")
        self.findProgressLabel.setObjectName("findProgressLabel")
        self.verticalLayout_3.addWidget(self.findProgressLabel)
        self.findProgress = QtWidgets.QProgressBar(FindFileDialog)
        self.findProgress.setProperty("value", 0)
        self.findProgress.setOrientation(QtCore.Qt.Horizontal)
        self.findProgress.setObjectName("findProgress")
        self.verticalLayout_3.addWidget(self.findProgress)
        self.findList = QtWidgets.QTreeWidget(FindFileDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.findList.sizePolicy().hasHeightForWidth())
        self.findList.setSizePolicy(sizePolicy)
        self.findList.setAlternatingRowColors(True)
        self.findList.setColumnCount(2)
        self.findList.setObjectName("findList")
        self.verticalLayout_3.addWidget(self.findList)
        self.replaceButton = QtWidgets.QPushButton(FindFileDialog)
        self.replaceButton.setObjectName("replaceButton")
        self.verticalLayout_3.addWidget(self.replaceButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(FindFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.TextLabel1.setBuddy(self.findtextCombo)
        self.replaceLabel.setBuddy(self.findtextCombo)

        self.retranslateUi(FindFileDialog)
        self.buttonBox.rejected.connect(FindFileDialog.close)
        self.filterCheckBox.toggled['bool'].connect(self.filterEdit.setEnabled)
        self.dirButton.toggled['bool'].connect(self.dirPicker.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(FindFileDialog)
        FindFileDialog.setTabOrder(self.findtextCombo, self.replacetextCombo)
        FindFileDialog.setTabOrder(self.replacetextCombo, self.caseCheckBox)
        FindFileDialog.setTabOrder(self.caseCheckBox, self.wordCheckBox)
        FindFileDialog.setTabOrder(self.wordCheckBox, self.regexpCheckBox)
        FindFileDialog.setTabOrder(self.regexpCheckBox, self.feelLikeCheckBox)
        FindFileDialog.setTabOrder(self.feelLikeCheckBox, self.sourcesCheckBox)
        FindFileDialog.setTabOrder(self.sourcesCheckBox, self.formsCheckBox)
        FindFileDialog.setTabOrder(self.formsCheckBox, self.resourcesCheckBox)
        FindFileDialog.setTabOrder(self.resourcesCheckBox, self.interfacesCheckBox)
        FindFileDialog.setTabOrder(self.interfacesCheckBox, self.protocolsCheckBox)
        FindFileDialog.setTabOrder(self.protocolsCheckBox, self.filterCheckBox)
        FindFileDialog.setTabOrder(self.filterCheckBox, self.filterEdit)
        FindFileDialog.setTabOrder(self.filterEdit, self.projectButton)
        FindFileDialog.setTabOrder(self.projectButton, self.dirButton)
        FindFileDialog.setTabOrder(self.dirButton, self.dirPicker)
        FindFileDialog.setTabOrder(self.dirPicker, self.openFilesButton)
        FindFileDialog.setTabOrder(self.openFilesButton, self.excludeHiddenCheckBox)
        FindFileDialog.setTabOrder(self.excludeHiddenCheckBox, self.findList)
        FindFileDialog.setTabOrder(self.findList, self.replaceButton)

    def retranslateUi(self, FindFileDialog):
        _translate = QtCore.QCoreApplication.translate
        FindFileDialog.setWindowTitle(_translate("FindFileDialog", "Find in Files"))
        self.TextLabel1.setText(_translate("FindFileDialog", "Find &text:"))
        self.findtextCombo.setToolTip(_translate("FindFileDialog", "Enter the search text or regular expression"))
        self.replaceLabel.setText(_translate("FindFileDialog", "Replace te&xt:"))
        self.replacetextCombo.setToolTip(_translate("FindFileDialog", "Enter the replacement text or regular expression"))
        self.caseCheckBox.setToolTip(_translate("FindFileDialog", "Select to match case sensitive"))
        self.caseCheckBox.setText(_translate("FindFileDialog", "&Match upper/lower case"))
        self.wordCheckBox.setToolTip(_translate("FindFileDialog", "Select to match whole words only"))
        self.wordCheckBox.setText(_translate("FindFileDialog", "Whole &word"))
        self.regexpCheckBox.setToolTip(_translate("FindFileDialog", "Select if the searchtext is a regular expression"))
        self.regexpCheckBox.setText(_translate("FindFileDialog", "Regular &Expression"))
        self.feelLikeCheckBox.setToolTip(_translate("FindFileDialog", "Select to open the first occurence automatically"))
        self.feelLikeCheckBox.setText(_translate("FindFileDialog", "Feeling Like"))
        self.groupBox.setTitle(_translate("FindFileDialog", "File type"))
        self.sourcesCheckBox.setToolTip(_translate("FindFileDialog", "Search in source files"))
        self.sourcesCheckBox.setText(_translate("FindFileDialog", "&Sources"))
        self.interfacesCheckBox.setToolTip(_translate("FindFileDialog", "Search in interfaces"))
        self.interfacesCheckBox.setText(_translate("FindFileDialog", "&Interfaces"))
        self.formsCheckBox.setToolTip(_translate("FindFileDialog", "Search in forms"))
        self.formsCheckBox.setText(_translate("FindFileDialog", "&Forms"))
        self.protocolsCheckBox.setToolTip(_translate("FindFileDialog", "Search in protocols"))
        self.protocolsCheckBox.setText(_translate("FindFileDialog", "&Protocols"))
        self.resourcesCheckBox.setToolTip(_translate("FindFileDialog", "Search in resources"))
        self.resourcesCheckBox.setText(_translate("FindFileDialog", "&Resources"))
        self.filterCheckBox.setToolTip(_translate("FindFileDialog", "Select to filter the files by a given filename pattern"))
        self.filterCheckBox.setText(_translate("FindFileDialog", "Fi&lter"))
        self.filterEdit.setToolTip(_translate("FindFileDialog", "Enter the filename wildcards separated by \';\'"))
        self.groupBox_2.setTitle(_translate("FindFileDialog", "Find in"))
        self.projectButton.setToolTip(_translate("FindFileDialog", "Search in files of the current project"))
        self.projectButton.setText(_translate("FindFileDialog", "&Project"))
        self.dirButton.setToolTip(_translate("FindFileDialog", "Search in files of a directory tree to be entered below"))
        self.dirButton.setText(_translate("FindFileDialog", "&Directory tree"))
        self.dirPicker.setToolTip(_translate("FindFileDialog", "Enter the directory to search in"))
        self.openFilesButton.setToolTip(_translate("FindFileDialog", "Search in open files only "))
        self.openFilesButton.setText(_translate("FindFileDialog", "&Open files only"))
        self.excludeHiddenCheckBox.setToolTip(_translate("FindFileDialog", "Select to exclude hidden files and directories when searching a directory tree."))
        self.excludeHiddenCheckBox.setText(_translate("FindFileDialog", "Exclude hidden files and directories"))
        self.findProgress.setToolTip(_translate("FindFileDialog", "Shows the progress of the search action"))
        self.findProgress.setFormat(_translate("FindFileDialog", "%v/%m Files"))
        self.findList.setSortingEnabled(True)
        self.findList.headerItem().setText(0, _translate("FindFileDialog", "File/Line"))
        self.findList.headerItem().setText(1, _translate("FindFileDialog", "Text"))
        self.replaceButton.setToolTip(_translate("FindFileDialog", "Press to apply the selected replacements"))
        self.replaceButton.setText(_translate("FindFileDialog", "Replace"))
from E5Gui.E5PathPicker import E5ComboPathPicker
from E5Gui.E5SqueezeLabels import E5SqueezeLabelPath
