# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\HexEditorPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HexEditorPage(object):
    def setupUi(self, HexEditorPage):
        HexEditorPage.setObjectName("HexEditorPage")
        HexEditorPage.resize(519, 664)
        self.verticalLayout = QtWidgets.QVBoxLayout(HexEditorPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(HexEditorPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line14 = QtWidgets.QFrame(HexEditorPage)
        self.line14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line14.setObjectName("line14")
        self.verticalLayout.addWidget(self.line14)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.readOnlyCheckBox = QtWidgets.QCheckBox(HexEditorPage)
        self.readOnlyCheckBox.setObjectName("readOnlyCheckBox")
        self.horizontalLayout_4.addWidget(self.readOnlyCheckBox)
        self.overwriteCheckBox = QtWidgets.QCheckBox(HexEditorPage)
        self.overwriteCheckBox.setObjectName("overwriteCheckBox")
        self.horizontalLayout_4.addWidget(self.overwriteCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.groupBox_3 = QtWidgets.QGroupBox(HexEditorPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.addressAreaCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.addressAreaCheckBox.setObjectName("addressAreaCheckBox")
        self.gridLayout_2.addWidget(self.addressAreaCheckBox, 0, 0, 1, 4)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1_20 = QtWidgets.QLabel(self.groupBox_3)
        self.textLabel1_20.setObjectName("textLabel1_20")
        self.hboxlayout.addWidget(self.textLabel1_20)
        self.addressAreaWidthSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.addressAreaWidthSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.addressAreaWidthSpinBox.setMinimum(2)
        self.addressAreaWidthSpinBox.setMaximum(12)
        self.addressAreaWidthSpinBox.setSingleStep(2)
        self.addressAreaWidthSpinBox.setProperty("value", 4)
        self.addressAreaWidthSpinBox.setObjectName("addressAreaWidthSpinBox")
        self.hboxlayout.addWidget(self.addressAreaWidthSpinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.hboxlayout, 1, 0, 1, 4)
        self.TextLabel1_3_4 = QtWidgets.QLabel(self.groupBox_3)
        self.TextLabel1_3_4.setObjectName("TextLabel1_3_4")
        self.gridLayout_2.addWidget(self.TextLabel1_3_4, 2, 0, 1, 1)
        self.addressAreaForeGroundButton = QtWidgets.QPushButton(self.groupBox_3)
        self.addressAreaForeGroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.addressAreaForeGroundButton.setText("")
        self.addressAreaForeGroundButton.setObjectName("addressAreaForeGroundButton")
        self.gridLayout_2.addWidget(self.addressAreaForeGroundButton, 2, 1, 1, 1)
        self.TextLabel1_3_2_4 = QtWidgets.QLabel(self.groupBox_3)
        self.TextLabel1_3_2_4.setObjectName("TextLabel1_3_2_4")
        self.gridLayout_2.addWidget(self.TextLabel1_3_2_4, 2, 2, 1, 1)
        self.addressAreaBackGroundButton = QtWidgets.QPushButton(self.groupBox_3)
        self.addressAreaBackGroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.addressAreaBackGroundButton.setText("")
        self.addressAreaBackGroundButton.setObjectName("addressAreaBackGroundButton")
        self.gridLayout_2.addWidget(self.addressAreaBackGroundButton, 2, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(HexEditorPage)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.asciiAreaCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.asciiAreaCheckBox.setObjectName("asciiAreaCheckBox")
        self.horizontalLayout_3.addWidget(self.asciiAreaCheckBox)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.groupBox = QtWidgets.QGroupBox(HexEditorPage)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.highlightingCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.highlightingCheckBox.setObjectName("highlightingCheckBox")
        self.gridLayout.addWidget(self.highlightingCheckBox, 0, 0, 1, 4)
        self.TextLabel1_3_2 = QtWidgets.QLabel(self.groupBox)
        self.TextLabel1_3_2.setObjectName("TextLabel1_3_2")
        self.gridLayout.addWidget(self.TextLabel1_3_2, 1, 0, 1, 1)
        self.highlightingForeGroundButton = QtWidgets.QPushButton(self.groupBox)
        self.highlightingForeGroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.highlightingForeGroundButton.setText("")
        self.highlightingForeGroundButton.setObjectName("highlightingForeGroundButton")
        self.gridLayout.addWidget(self.highlightingForeGroundButton, 1, 1, 1, 1)
        self.TextLabel1_3_2_2 = QtWidgets.QLabel(self.groupBox)
        self.TextLabel1_3_2_2.setObjectName("TextLabel1_3_2_2")
        self.gridLayout.addWidget(self.TextLabel1_3_2_2, 1, 2, 1, 1)
        self.highlightingBackGroundButton = QtWidgets.QPushButton(self.groupBox)
        self.highlightingBackGroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.highlightingBackGroundButton.setText("")
        self.highlightingBackGroundButton.setObjectName("highlightingBackGroundButton")
        self.gridLayout.addWidget(self.highlightingBackGroundButton, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(HexEditorPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.TextLabel1_3_3 = QtWidgets.QLabel(self.groupBox_2)
        self.TextLabel1_3_3.setObjectName("TextLabel1_3_3")
        self.horizontalLayout_2.addWidget(self.TextLabel1_3_3)
        self.selectionForeGroundButton = QtWidgets.QPushButton(self.groupBox_2)
        self.selectionForeGroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.selectionForeGroundButton.setText("")
        self.selectionForeGroundButton.setObjectName("selectionForeGroundButton")
        self.horizontalLayout_2.addWidget(self.selectionForeGroundButton)
        self.TextLabel1_3_2_3 = QtWidgets.QLabel(self.groupBox_2)
        self.TextLabel1_3_2_3.setObjectName("TextLabel1_3_2_3")
        self.horizontalLayout_2.addWidget(self.TextLabel1_3_2_3)
        self.selectionBackGroundButton = QtWidgets.QPushButton(self.groupBox_2)
        self.selectionBackGroundButton.setMinimumSize(QtCore.QSize(100, 0))
        self.selectionBackGroundButton.setText("")
        self.selectionBackGroundButton.setObjectName("selectionBackGroundButton")
        self.horizontalLayout_2.addWidget(self.selectionBackGroundButton)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_5 = QtWidgets.QGroupBox(HexEditorPage)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.monospacedFontButton = QtWidgets.QPushButton(self.groupBox_5)
        self.monospacedFontButton.setObjectName("monospacedFontButton")
        self.horizontalLayout.addWidget(self.monospacedFontButton)
        self.monospacedFontSample = QtWidgets.QLineEdit(self.groupBox_5)
        self.monospacedFontSample.setFocusPolicy(QtCore.Qt.NoFocus)
        self.monospacedFontSample.setText("01 23 45 67 89 ab cd ef 70 81 92 a3 b4 c5 d6 e7 f9")
        self.monospacedFontSample.setAlignment(QtCore.Qt.AlignHCenter)
        self.monospacedFontSample.setReadOnly(True)
        self.monospacedFontSample.setObjectName("monospacedFontSample")
        self.horizontalLayout.addWidget(self.monospacedFontSample)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_7 = QtWidgets.QGroupBox(HexEditorPage)
        self.groupBox_7.setObjectName("groupBox_7")
        self._2 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self._2.setObjectName("_2")
        self.label = QtWidgets.QLabel(self.groupBox_7)
        self.label.setObjectName("label")
        self._2.addWidget(self.label)
        self.recentFilesSpinBox = QtWidgets.QSpinBox(self.groupBox_7)
        self.recentFilesSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.recentFilesSpinBox.setMinimum(5)
        self.recentFilesSpinBox.setMaximum(50)
        self.recentFilesSpinBox.setObjectName("recentFilesSpinBox")
        self._2.addWidget(self.recentFilesSpinBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.groupBox_7)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(HexEditorPage)
        QtCore.QMetaObject.connectSlotsByName(HexEditorPage)
        HexEditorPage.setTabOrder(self.readOnlyCheckBox, self.overwriteCheckBox)
        HexEditorPage.setTabOrder(self.overwriteCheckBox, self.addressAreaCheckBox)
        HexEditorPage.setTabOrder(self.addressAreaCheckBox, self.addressAreaWidthSpinBox)
        HexEditorPage.setTabOrder(self.addressAreaWidthSpinBox, self.addressAreaForeGroundButton)
        HexEditorPage.setTabOrder(self.addressAreaForeGroundButton, self.addressAreaBackGroundButton)
        HexEditorPage.setTabOrder(self.addressAreaBackGroundButton, self.asciiAreaCheckBox)
        HexEditorPage.setTabOrder(self.asciiAreaCheckBox, self.highlightingCheckBox)
        HexEditorPage.setTabOrder(self.highlightingCheckBox, self.highlightingForeGroundButton)
        HexEditorPage.setTabOrder(self.highlightingForeGroundButton, self.highlightingBackGroundButton)
        HexEditorPage.setTabOrder(self.highlightingBackGroundButton, self.selectionForeGroundButton)
        HexEditorPage.setTabOrder(self.selectionForeGroundButton, self.selectionBackGroundButton)
        HexEditorPage.setTabOrder(self.selectionBackGroundButton, self.monospacedFontButton)

    def retranslateUi(self, HexEditorPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("HexEditorPage", "<b>Configure Hex Editor</b>"))
        self.readOnlyCheckBox.setToolTip(_translate("HexEditorPage", "Select whether files shall be opened in read only mode"))
        self.readOnlyCheckBox.setText(_translate("HexEditorPage", "Open files \'read only\'"))
        self.overwriteCheckBox.setToolTip(_translate("HexEditorPage", "Select whether the editor shall be started in Overwrite mode"))
        self.overwriteCheckBox.setText(_translate("HexEditorPage", "Overwrite data"))
        self.groupBox_3.setTitle(_translate("HexEditorPage", "Address Area"))
        self.addressAreaCheckBox.setToolTip(_translate("HexEditorPage", "Select whether the address area shall be shown"))
        self.addressAreaCheckBox.setText(_translate("HexEditorPage", "Show Address Area"))
        self.textLabel1_20.setText(_translate("HexEditorPage", "Address Area Width:"))
        self.addressAreaWidthSpinBox.setToolTip(_translate("HexEditorPage", "Enter the width of the address area in characters"))
        self.addressAreaWidthSpinBox.setSuffix(_translate("HexEditorPage", " Chars"))
        self.TextLabel1_3_4.setText(_translate("HexEditorPage", "Foreground:"))
        self.addressAreaForeGroundButton.setToolTip(_translate("HexEditorPage", "Select the foreground color of the address area"))
        self.TextLabel1_3_2_4.setText(_translate("HexEditorPage", "Background:"))
        self.addressAreaBackGroundButton.setToolTip(_translate("HexEditorPage", "Select the background color of the address area"))
        self.groupBox_4.setTitle(_translate("HexEditorPage", "ASCII Area"))
        self.asciiAreaCheckBox.setToolTip(_translate("HexEditorPage", "Select whether the ASCII area shall be shown"))
        self.asciiAreaCheckBox.setText(_translate("HexEditorPage", "Show ASCII Area"))
        self.groupBox.setTitle(_translate("HexEditorPage", "Highlighting"))
        self.highlightingCheckBox.setToolTip(_translate("HexEditorPage", "Select whether changed data shall be highlighted"))
        self.highlightingCheckBox.setText(_translate("HexEditorPage", "Highlight Changed Data"))
        self.TextLabel1_3_2.setText(_translate("HexEditorPage", "Foreground:"))
        self.highlightingForeGroundButton.setToolTip(_translate("HexEditorPage", "Select the foreground color for highlighted data"))
        self.TextLabel1_3_2_2.setText(_translate("HexEditorPage", "Background:"))
        self.highlightingBackGroundButton.setToolTip(_translate("HexEditorPage", "Select the background color for highlighted data"))
        self.groupBox_2.setTitle(_translate("HexEditorPage", "Selection"))
        self.TextLabel1_3_3.setText(_translate("HexEditorPage", "Foreground:"))
        self.selectionForeGroundButton.setToolTip(_translate("HexEditorPage", "Select the foreground color of the selection"))
        self.TextLabel1_3_2_3.setText(_translate("HexEditorPage", "Background:"))
        self.selectionBackGroundButton.setToolTip(_translate("HexEditorPage", "Select the background color of the selection"))
        self.groupBox_5.setTitle(_translate("HexEditorPage", "Font"))
        self.monospacedFontButton.setToolTip(_translate("HexEditorPage", "Press to select the font to be used (this must be a monospaced font)"))
        self.monospacedFontButton.setText(_translate("HexEditorPage", "Monospaced Font"))
        self.groupBox_7.setTitle(_translate("HexEditorPage", "Recent Files"))
        self.label.setText(_translate("HexEditorPage", "Number of recent files:"))
        self.recentFilesSpinBox.setToolTip(_translate("HexEditorPage", "Enter the number of recent files to remember"))
