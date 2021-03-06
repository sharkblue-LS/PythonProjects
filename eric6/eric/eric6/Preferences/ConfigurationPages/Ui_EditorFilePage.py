# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\EditorFilePage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorFilePage(object):
    def setupUi(self, EditorFilePage):
        EditorFilePage.setObjectName("EditorFilePage")
        EditorFilePage.resize(600, 1621)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(EditorFilePage)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.headerLabel = QtWidgets.QLabel(EditorFilePage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_5.addWidget(self.headerLabel)
        self.line2 = QtWidgets.QFrame(EditorFilePage)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setObjectName("line2")
        self.verticalLayout_5.addWidget(self.line2)
        self.groupBox_3 = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.clearBreakpointsCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.clearBreakpointsCheckBox.setObjectName("clearBreakpointsCheckBox")
        self.hboxlayout.addWidget(self.clearBreakpointsCheckBox)
        self.automaticReopenCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.automaticReopenCheckBox.setObjectName("automaticReopenCheckBox")
        self.hboxlayout.addWidget(self.automaticReopenCheckBox)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)
        self.warnFilesizeSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.warnFilesizeSpinBox.setMinimum(1)
        self.warnFilesizeSpinBox.setMaximum(16384)
        self.warnFilesizeSpinBox.setSingleStep(16)
        self.warnFilesizeSpinBox.setProperty("value", 1024)
        self.warnFilesizeSpinBox.setObjectName("warnFilesizeSpinBox")
        self.hboxlayout1.addWidget(self.warnFilesizeSpinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        self.groupBox_5 = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_5)
        self.groupBox_8.setObjectName("groupBox_8")
        self._12 = QtWidgets.QHBoxLayout(self.groupBox_8)
        self._12.setObjectName("_12")
        self.lfRadioButton = QtWidgets.QRadioButton(self.groupBox_8)
        self.lfRadioButton.setObjectName("lfRadioButton")
        self._12.addWidget(self.lfRadioButton)
        self.crRadioButton = QtWidgets.QRadioButton(self.groupBox_8)
        self.crRadioButton.setObjectName("crRadioButton")
        self._12.addWidget(self.crRadioButton)
        self.crlfRadioButton = QtWidgets.QRadioButton(self.groupBox_8)
        self.crlfRadioButton.setObjectName("crlfRadioButton")
        self._12.addWidget(self.crlfRadioButton)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.automaticEolConversionCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.automaticEolConversionCheckBox.setObjectName("automaticEolConversionCheckBox")
        self.verticalLayout.addWidget(self.automaticEolConversionCheckBox)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.insertFinalNewlineCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.insertFinalNewlineCheckBox.setObjectName("insertFinalNewlineCheckBox")
        self.verticalLayout_3.addWidget(self.insertFinalNewlineCheckBox)
        self.stripWhitespaceCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.stripWhitespaceCheckBox.setObjectName("stripWhitespaceCheckBox")
        self.verticalLayout_3.addWidget(self.stripWhitespaceCheckBox)
        self.createBackupFileCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.createBackupFileCheckBox.setObjectName("createBackupFileCheckBox")
        self.verticalLayout_3.addWidget(self.createBackupFileCheckBox)
        self.hboxlayout2 = QtWidgets.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")
        self.TextLabel13_3_3 = QtWidgets.QLabel(self.groupBox_4)
        self.TextLabel13_3_3.setObjectName("TextLabel13_3_3")
        self.hboxlayout2.addWidget(self.TextLabel13_3_3)
        self.autosaveSlider = QtWidgets.QSlider(self.groupBox_4)
        self.autosaveSlider.setMinimum(0)
        self.autosaveSlider.setMaximum(30)
        self.autosaveSlider.setProperty("value", 5)
        self.autosaveSlider.setOrientation(QtCore.Qt.Horizontal)
        self.autosaveSlider.setTickInterval(1)
        self.autosaveSlider.setObjectName("autosaveSlider")
        self.hboxlayout2.addWidget(self.autosaveSlider)
        self.autosaveLCD = QtWidgets.QLCDNumber(self.groupBox_4)
        self.autosaveLCD.setDigitCount(2)
        self.autosaveLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.autosaveLCD.setProperty("value", 5.0)
        self.autosaveLCD.setObjectName("autosaveLCD")
        self.hboxlayout2.addWidget(self.autosaveLCD)
        self.verticalLayout_3.addLayout(self.hboxlayout2)
        self.verticalLayout_5.addWidget(self.groupBox_4)
        self.groupBox = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.advEncodingCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.advEncodingCheckBox.setObjectName("advEncodingCheckBox")
        self.gridLayout.addWidget(self.advEncodingCheckBox, 0, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.defaultEncodingComboBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defaultEncodingComboBox.sizePolicy().hasHeightForWidth())
        self.defaultEncodingComboBox.setSizePolicy(sizePolicy)
        self.defaultEncodingComboBox.setObjectName("defaultEncodingComboBox")
        self.gridLayout.addWidget(self.defaultEncodingComboBox, 1, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName("gridlayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.openFilesFilterComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.openFilesFilterComboBox.setObjectName("openFilesFilterComboBox")
        self.gridlayout.addWidget(self.openFilesFilterComboBox, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.saveFilesFilterComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.saveFilesFilterComboBox.setObjectName("saveFilesFilterComboBox")
        self.gridlayout.addWidget(self.saveFilesFilterComboBox, 1, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_2)
        self.groupBox_6 = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_6)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openFiltersButton = QtWidgets.QRadioButton(self.groupBox_6)
        self.openFiltersButton.setChecked(True)
        self.openFiltersButton.setObjectName("openFiltersButton")
        self.horizontalLayout.addWidget(self.openFiltersButton)
        self.savFiltersButton = QtWidgets.QRadioButton(self.groupBox_6)
        self.savFiltersButton.setObjectName("savFiltersButton")
        self.horizontalLayout.addWidget(self.savFiltersButton)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.fileFiltersList = QtWidgets.QListWidget(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileFiltersList.sizePolicy().hasHeightForWidth())
        self.fileFiltersList.setSizePolicy(sizePolicy)
        self.fileFiltersList.setMinimumSize(QtCore.QSize(0, 200))
        self.fileFiltersList.setAlternatingRowColors(True)
        self.fileFiltersList.setObjectName("fileFiltersList")
        self.gridLayout_2.addWidget(self.fileFiltersList, 2, 0, 4, 1)
        self.addFileFilterButton = QtWidgets.QPushButton(self.groupBox_6)
        self.addFileFilterButton.setObjectName("addFileFilterButton")
        self.gridLayout_2.addWidget(self.addFileFilterButton, 2, 1, 1, 1)
        self.editFileFilterButton = QtWidgets.QPushButton(self.groupBox_6)
        self.editFileFilterButton.setEnabled(False)
        self.editFileFilterButton.setObjectName("editFileFilterButton")
        self.gridLayout_2.addWidget(self.editFileFilterButton, 3, 1, 1, 1)
        self.deleteFileFilterButton = QtWidgets.QPushButton(self.groupBox_6)
        self.deleteFileFilterButton.setEnabled(False)
        self.deleteFileFilterButton.setObjectName("deleteFileFilterButton")
        self.gridLayout_2.addWidget(self.deleteFileFilterButton, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 5, 1, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_6)
        self.groupBox_7 = QtWidgets.QGroupBox(EditorFilePage)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox_7)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.previewRefreshTimeoutSpinBox = QtWidgets.QSpinBox(self.groupBox_7)
        self.previewRefreshTimeoutSpinBox.setMinimum(500)
        self.previewRefreshTimeoutSpinBox.setMaximum(5000)
        self.previewRefreshTimeoutSpinBox.setSingleStep(500)
        self.previewRefreshTimeoutSpinBox.setObjectName("previewRefreshTimeoutSpinBox")
        self.horizontalLayout_5.addWidget(self.previewRefreshTimeoutSpinBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_12.setObjectName("groupBox_12")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.groupBox_12)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_3.addWidget(self.label_12)
        self.previewHtmlExtensionsEdit = QtWidgets.QLineEdit(self.groupBox_12)
        self.previewHtmlExtensionsEdit.setObjectName("previewHtmlExtensionsEdit")
        self.horizontalLayout_3.addWidget(self.previewHtmlExtensionsEdit)
        self.verticalLayout_4.addWidget(self.groupBox_12)
        self.groupBox_11 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_11.setObjectName("groupBox_11")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_11)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.groupBox_11)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.previewMarkdownExtensionsEdit = QtWidgets.QLineEdit(self.groupBox_11)
        self.previewMarkdownExtensionsEdit.setObjectName("previewMarkdownExtensionsEdit")
        self.gridLayout_4.addWidget(self.previewMarkdownExtensionsEdit, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_11)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)
        self.previewMarkdownHTMLFormatComboBox = QtWidgets.QComboBox(self.groupBox_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewMarkdownHTMLFormatComboBox.sizePolicy().hasHeightForWidth())
        self.previewMarkdownHTMLFormatComboBox.setSizePolicy(sizePolicy)
        self.previewMarkdownHTMLFormatComboBox.setObjectName("previewMarkdownHTMLFormatComboBox")
        self.gridLayout_4.addWidget(self.previewMarkdownHTMLFormatComboBox, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_4)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.previewMarkdownNLtoBreakCheckBox = QtWidgets.QCheckBox(self.groupBox_11)
        self.previewMarkdownNLtoBreakCheckBox.setObjectName("previewMarkdownNLtoBreakCheckBox")
        self.gridLayout_5.addWidget(self.previewMarkdownNLtoBreakCheckBox, 0, 0, 1, 1)
        self.previewMarkdownMathJaxCheckBox = QtWidgets.QCheckBox(self.groupBox_11)
        self.previewMarkdownMathJaxCheckBox.setObjectName("previewMarkdownMathJaxCheckBox")
        self.gridLayout_5.addWidget(self.previewMarkdownMathJaxCheckBox, 1, 0, 1, 1)
        self.previewMarkdownMermaidCheckBox = QtWidgets.QCheckBox(self.groupBox_11)
        self.previewMarkdownMermaidCheckBox.setObjectName("previewMarkdownMermaidCheckBox")
        self.gridLayout_5.addWidget(self.previewMarkdownMermaidCheckBox, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.previewMarkdownPyMdownCheckBox = QtWidgets.QCheckBox(self.groupBox_11)
        self.previewMarkdownPyMdownCheckBox.setObjectName("previewMarkdownPyMdownCheckBox")
        self.horizontalLayout_6.addWidget(self.previewMarkdownPyMdownCheckBox)
        self.previewMarkdownPyMdownInstallPushButton = QtWidgets.QPushButton(self.groupBox_11)
        self.previewMarkdownPyMdownInstallPushButton.setObjectName("previewMarkdownPyMdownInstallPushButton")
        self.horizontalLayout_6.addWidget(self.previewMarkdownPyMdownInstallPushButton)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.verticalLayout_4.addWidget(self.groupBox_11)
        self.groupBox_10 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_10.setObjectName("groupBox_10")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_10)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.previewRestExtensionsEdit = QtWidgets.QLineEdit(self.groupBox_10)
        self.previewRestExtensionsEdit.setObjectName("previewRestExtensionsEdit")
        self.gridLayout_3.addWidget(self.previewRestExtensionsEdit, 0, 1, 1, 1)
        self.previewRestSphinxCheckBox = QtWidgets.QCheckBox(self.groupBox_10)
        self.previewRestSphinxCheckBox.setObjectName("previewRestSphinxCheckBox")
        self.gridLayout_3.addWidget(self.previewRestSphinxCheckBox, 1, 0, 1, 2)
        self.groupBox_13 = QtWidgets.QGroupBox(self.groupBox_10)
        self.groupBox_13.setObjectName("groupBox_13")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_13)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.groupBox_13)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.previewRestDocutilsHTMLFormatComboBox = QtWidgets.QComboBox(self.groupBox_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewRestDocutilsHTMLFormatComboBox.sizePolicy().hasHeightForWidth())
        self.previewRestDocutilsHTMLFormatComboBox.setSizePolicy(sizePolicy)
        self.previewRestDocutilsHTMLFormatComboBox.setObjectName("previewRestDocutilsHTMLFormatComboBox")
        self.horizontalLayout_4.addWidget(self.previewRestDocutilsHTMLFormatComboBox)
        self.gridLayout_3.addWidget(self.groupBox_13, 2, 0, 1, 2)
        self.verticalLayout_4.addWidget(self.groupBox_10)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.groupBox_9)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.previewQssExtensionsEdit = QtWidgets.QLineEdit(self.groupBox_9)
        self.previewQssExtensionsEdit.setObjectName("previewQssExtensionsEdit")
        self.horizontalLayout_2.addWidget(self.previewQssExtensionsEdit)
        self.verticalLayout_4.addWidget(self.groupBox_9)
        self.verticalLayout_5.addWidget(self.groupBox_7)

        self.retranslateUi(EditorFilePage)
        self.autosaveSlider.valueChanged['int'].connect(self.autosaveLCD.display)
        QtCore.QMetaObject.connectSlotsByName(EditorFilePage)
        EditorFilePage.setTabOrder(self.clearBreakpointsCheckBox, self.automaticReopenCheckBox)
        EditorFilePage.setTabOrder(self.automaticReopenCheckBox, self.warnFilesizeSpinBox)
        EditorFilePage.setTabOrder(self.warnFilesizeSpinBox, self.lfRadioButton)
        EditorFilePage.setTabOrder(self.lfRadioButton, self.crRadioButton)
        EditorFilePage.setTabOrder(self.crRadioButton, self.crlfRadioButton)
        EditorFilePage.setTabOrder(self.crlfRadioButton, self.automaticEolConversionCheckBox)
        EditorFilePage.setTabOrder(self.automaticEolConversionCheckBox, self.insertFinalNewlineCheckBox)
        EditorFilePage.setTabOrder(self.insertFinalNewlineCheckBox, self.stripWhitespaceCheckBox)
        EditorFilePage.setTabOrder(self.stripWhitespaceCheckBox, self.createBackupFileCheckBox)
        EditorFilePage.setTabOrder(self.createBackupFileCheckBox, self.autosaveSlider)
        EditorFilePage.setTabOrder(self.autosaveSlider, self.advEncodingCheckBox)
        EditorFilePage.setTabOrder(self.advEncodingCheckBox, self.defaultEncodingComboBox)
        EditorFilePage.setTabOrder(self.defaultEncodingComboBox, self.openFilesFilterComboBox)
        EditorFilePage.setTabOrder(self.openFilesFilterComboBox, self.saveFilesFilterComboBox)
        EditorFilePage.setTabOrder(self.saveFilesFilterComboBox, self.openFiltersButton)
        EditorFilePage.setTabOrder(self.openFiltersButton, self.savFiltersButton)
        EditorFilePage.setTabOrder(self.savFiltersButton, self.fileFiltersList)
        EditorFilePage.setTabOrder(self.fileFiltersList, self.addFileFilterButton)
        EditorFilePage.setTabOrder(self.addFileFilterButton, self.editFileFilterButton)
        EditorFilePage.setTabOrder(self.editFileFilterButton, self.deleteFileFilterButton)
        EditorFilePage.setTabOrder(self.deleteFileFilterButton, self.previewRefreshTimeoutSpinBox)
        EditorFilePage.setTabOrder(self.previewRefreshTimeoutSpinBox, self.previewHtmlExtensionsEdit)
        EditorFilePage.setTabOrder(self.previewHtmlExtensionsEdit, self.previewMarkdownExtensionsEdit)
        EditorFilePage.setTabOrder(self.previewMarkdownExtensionsEdit, self.previewMarkdownHTMLFormatComboBox)
        EditorFilePage.setTabOrder(self.previewMarkdownHTMLFormatComboBox, self.previewMarkdownNLtoBreakCheckBox)
        EditorFilePage.setTabOrder(self.previewMarkdownNLtoBreakCheckBox, self.previewMarkdownMathJaxCheckBox)
        EditorFilePage.setTabOrder(self.previewMarkdownMathJaxCheckBox, self.previewMarkdownMermaidCheckBox)
        EditorFilePage.setTabOrder(self.previewMarkdownMermaidCheckBox, self.previewMarkdownPyMdownCheckBox)
        EditorFilePage.setTabOrder(self.previewMarkdownPyMdownCheckBox, self.previewMarkdownPyMdownInstallPushButton)
        EditorFilePage.setTabOrder(self.previewMarkdownPyMdownInstallPushButton, self.previewRestExtensionsEdit)
        EditorFilePage.setTabOrder(self.previewRestExtensionsEdit, self.previewRestSphinxCheckBox)
        EditorFilePage.setTabOrder(self.previewRestSphinxCheckBox, self.previewRestDocutilsHTMLFormatComboBox)
        EditorFilePage.setTabOrder(self.previewRestDocutilsHTMLFormatComboBox, self.previewQssExtensionsEdit)

    def retranslateUi(self, EditorFilePage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorFilePage", "<b>Configure file handling settings</b>"))
        self.groupBox_3.setTitle(_translate("EditorFilePage", "Open && Close"))
        self.clearBreakpointsCheckBox.setToolTip(_translate("EditorFilePage", "Select, whether breakpoint belonging to an editor should be cleared, when the editor is closed"))
        self.clearBreakpointsCheckBox.setText(_translate("EditorFilePage", "Clear Breakpoints upon closing"))
        self.automaticReopenCheckBox.setToolTip(_translate("EditorFilePage", "Select to reread the file automatically, if it was changed externally"))
        self.automaticReopenCheckBox.setText(_translate("EditorFilePage", "Reread automatically when changed externally"))
        self.label.setText(_translate("EditorFilePage", "Warn, if file is greater than"))
        self.warnFilesizeSpinBox.setToolTip(_translate("EditorFilePage", "Enter the filesize, a warning dialog should be shown."))
        self.warnFilesizeSpinBox.setSuffix(_translate("EditorFilePage", " KB"))
        self.groupBox_5.setTitle(_translate("EditorFilePage", "End of Line"))
        self.groupBox_8.setTitle(_translate("EditorFilePage", "End of Line Characters"))
        self.lfRadioButton.setToolTip(_translate("EditorFilePage", "Select Unix type end of line"))
        self.lfRadioButton.setText(_translate("EditorFilePage", "Unix"))
        self.crRadioButton.setToolTip(_translate("EditorFilePage", "Select Macintosh type end of line"))
        self.crRadioButton.setText(_translate("EditorFilePage", "Macintosh"))
        self.crlfRadioButton.setToolTip(_translate("EditorFilePage", "Select Windows type end of line"))
        self.crlfRadioButton.setText(_translate("EditorFilePage", "Windows/DOS"))
        self.automaticEolConversionCheckBox.setToolTip(_translate("EditorFilePage", "Select whether the eol type should be converted upon opening the file."))
        self.automaticEolConversionCheckBox.setText(_translate("EditorFilePage", "Automatic End of Line Conversion"))
        self.groupBox_4.setTitle(_translate("EditorFilePage", "Save"))
        self.insertFinalNewlineCheckBox.setToolTip(_translate("EditorFilePage", "Select to insert a final newline if none is there"))
        self.insertFinalNewlineCheckBox.setText(_translate("EditorFilePage", "Insert final newline upon save"))
        self.stripWhitespaceCheckBox.setToolTip(_translate("EditorFilePage", "Select, whether trailing whitespace should be removed upon save"))
        self.stripWhitespaceCheckBox.setText(_translate("EditorFilePage", "Strip trailing whitespace upon save"))
        self.createBackupFileCheckBox.setToolTip(_translate("EditorFilePage", "Select, whether a backup file shall be generated upon save"))
        self.createBackupFileCheckBox.setText(_translate("EditorFilePage", "Create backup file upon save"))
        self.TextLabel13_3_3.setText(_translate("EditorFilePage", "Autosave interval:"))
        self.autosaveSlider.setToolTip(_translate("EditorFilePage", "Move to set the autosave interval in minutes (0 to disable)"))
        self.autosaveLCD.setToolTip(_translate("EditorFilePage", "Displays the selected autosave interval."))
        self.groupBox.setTitle(_translate("EditorFilePage", "Encoding"))
        self.advEncodingCheckBox.setToolTip(_translate("EditorFilePage", "Select to use the advanced encoding detection "))
        self.advEncodingCheckBox.setWhatsThis(_translate("EditorFilePage", "<b>Advanced encoding detection</b>\n"
"<p>Select to use the advanced encoding detection based on the &quot;universal character encoding detector&quot; from <a href=\"http://chardet.feedparser.org\">http://chardet.feedparser.org</a>.</p>"))
        self.advEncodingCheckBox.setText(_translate("EditorFilePage", "Use advanced encoding detection"))
        self.label_4.setText(_translate("EditorFilePage", "Default Encoding:"))
        self.defaultEncodingComboBox.setToolTip(_translate("EditorFilePage", "Select the string encoding to be used."))
        self.groupBox_2.setTitle(_translate("EditorFilePage", "Default File Filters"))
        self.label_2.setText(_translate("EditorFilePage", "Open Files:"))
        self.label_3.setText(_translate("EditorFilePage", "Save Files:"))
        self.groupBox_6.setTitle(_translate("EditorFilePage", "Additional File Filters"))
        self.label_5.setText(_translate("EditorFilePage", "<b>Note:</b> Save file filters must contain one wildcard pattern only."))
        self.openFiltersButton.setToolTip(_translate("EditorFilePage", "Select to edit the open file filters"))
        self.openFiltersButton.setText(_translate("EditorFilePage", "Open Files"))
        self.savFiltersButton.setToolTip(_translate("EditorFilePage", "Select to edit the save file filters"))
        self.savFiltersButton.setText(_translate("EditorFilePage", "Save Files"))
        self.fileFiltersList.setSortingEnabled(True)
        self.addFileFilterButton.setText(_translate("EditorFilePage", "Add..."))
        self.editFileFilterButton.setText(_translate("EditorFilePage", "Edit..."))
        self.deleteFileFilterButton.setText(_translate("EditorFilePage", "Delete"))
        self.groupBox_7.setTitle(_translate("EditorFilePage", "File Preview"))
        self.label_8.setText(_translate("EditorFilePage", "Refresh Timeout:"))
        self.previewRefreshTimeoutSpinBox.setToolTip(_translate("EditorFilePage", "Enter the timeout in milliseconds until the preview is refreshed"))
        self.previewRefreshTimeoutSpinBox.setSuffix(_translate("EditorFilePage", " ms"))
        self.groupBox_12.setTitle(_translate("EditorFilePage", "HTML Files"))
        self.label_12.setText(_translate("EditorFilePage", "File Extensions:"))
        self.previewHtmlExtensionsEdit.setToolTip(_translate("EditorFilePage", "Enter the filename extensions of HTML files that may be previewed (separated by a space)"))
        self.groupBox_11.setTitle(_translate("EditorFilePage", "Markdown Files"))
        self.label_11.setText(_translate("EditorFilePage", "File Extensions:"))
        self.previewMarkdownExtensionsEdit.setToolTip(_translate("EditorFilePage", "Enter the filename extensions of Markdown files that may be previewed (separated by a space)"))
        self.label_6.setText(_translate("EditorFilePage", "HTML Format:"))
        self.previewMarkdownHTMLFormatComboBox.setToolTip(_translate("EditorFilePage", "Select the HTML format to be generated"))
        self.previewMarkdownNLtoBreakCheckBox.setToolTip(_translate("EditorFilePage", "Select this to convert a new line character to an HTML &lt;br/&gt; tag."))
        self.previewMarkdownNLtoBreakCheckBox.setText(_translate("EditorFilePage", "Convert New Line to HTML Break"))
        self.previewMarkdownMathJaxCheckBox.setToolTip(_translate("EditorFilePage", "Select to enable Math support using MathJax"))
        self.previewMarkdownMathJaxCheckBox.setText(_translate("EditorFilePage", "Enable Math support"))
        self.previewMarkdownMermaidCheckBox.setToolTip(_translate("EditorFilePage", "Select to enable Graph support using Mermaid"))
        self.previewMarkdownMermaidCheckBox.setText(_translate("EditorFilePage", "Enable Graph support"))
        self.previewMarkdownPyMdownCheckBox.setToolTip(_translate("EditorFilePage", "Select to enable the use of the PyMdown extensions"))
        self.previewMarkdownPyMdownCheckBox.setWhatsThis(_translate("EditorFilePage", "<b>Enable PyMdown Extensions</b>\n"
"<p>Select this entry to enable the use of the PyMdown extensions. These have to be installed with <code>pip install pymdown-extensions</code>.</p>"))
        self.previewMarkdownPyMdownCheckBox.setText(_translate("EditorFilePage", "Enable PyMdown Extensions"))
        self.previewMarkdownPyMdownInstallPushButton.setToolTip(_translate("EditorFilePage", "Press to install the PyMdown extensions"))
        self.previewMarkdownPyMdownInstallPushButton.setText(_translate("EditorFilePage", "Install PyMdown Extensions"))
        self.groupBox_10.setTitle(_translate("EditorFilePage", "ReST Files"))
        self.label_9.setText(_translate("EditorFilePage", "File Extensions:"))
        self.previewRestExtensionsEdit.setToolTip(_translate("EditorFilePage", "Enter the filename extensions of ReStructuredText files that may be previewed (separated by a space)"))
        self.previewRestSphinxCheckBox.setToolTip(_translate("EditorFilePage", "Select to use \'sphinx\' to generate the ReST preview"))
        self.previewRestSphinxCheckBox.setText(_translate("EditorFilePage", "Use \'sphinx\' for ReST preview"))
        self.groupBox_13.setTitle(_translate("EditorFilePage", "Docutils"))
        self.label_7.setText(_translate("EditorFilePage", "HTML Format:"))
        self.previewRestDocutilsHTMLFormatComboBox.setToolTip(_translate("EditorFilePage", "Select the HTML format to be generated"))
        self.groupBox_9.setTitle(_translate("EditorFilePage", "QSS Files"))
        self.label_10.setText(_translate("EditorFilePage", "File Extensions:"))
        self.previewQssExtensionsEdit.setToolTip(_translate("EditorFilePage", "Enter the filename extensions of Qt Stylesheet files that may be previewed (separated by a space)"))
