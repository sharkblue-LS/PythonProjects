# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\EditorExportersPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorExportersPage(object):
    def setupUi(self, EditorExportersPage):
        EditorExportersPage.setObjectName("EditorExportersPage")
        EditorExportersPage.resize(537, 435)
        EditorExportersPage.setWindowTitle("")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(EditorExportersPage)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.headerLabel = QtWidgets.QLabel(EditorExportersPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_10.addWidget(self.headerLabel)
        self.line1 = QtWidgets.QFrame(EditorExportersPage)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setObjectName("line1")
        self.verticalLayout_10.addWidget(self.line1)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.TextLabel1_3 = QtWidgets.QLabel(EditorExportersPage)
        self.TextLabel1_3.setObjectName("TextLabel1_3")
        self.hboxlayout.addWidget(self.TextLabel1_3)
        self.exportersCombo = QtWidgets.QComboBox(EditorExportersPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportersCombo.sizePolicy().hasHeightForWidth())
        self.exportersCombo.setSizePolicy(sizePolicy)
        self.exportersCombo.setObjectName("exportersCombo")
        self.hboxlayout.addWidget(self.exportersCombo)
        self.verticalLayout_10.addLayout(self.hboxlayout)
        self.stackedWidget = QtWidgets.QStackedWidget(EditorExportersPage)
        self.stackedWidget.setObjectName("stackedWidget")
        self.emptyPage = QtWidgets.QWidget()
        self.emptyPage.setObjectName("emptyPage")
        self.stackedWidget.addWidget(self.emptyPage)
        self.htmlPage = QtWidgets.QWidget()
        self.htmlPage.setObjectName("htmlPage")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.htmlPage)
        self.verticalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.htmlPage)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.htmlWysiwygCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.htmlWysiwygCheckBox.setObjectName("htmlWysiwygCheckBox")
        self.verticalLayout_3.addWidget(self.htmlWysiwygCheckBox)
        self.htmlFoldingCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.htmlFoldingCheckBox.setObjectName("htmlFoldingCheckBox")
        self.verticalLayout_3.addWidget(self.htmlFoldingCheckBox)
        self.htmlStylesCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.htmlStylesCheckBox.setObjectName("htmlStylesCheckBox")
        self.verticalLayout_3.addWidget(self.htmlStylesCheckBox)
        self.htmlTitleCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.htmlTitleCheckBox.setObjectName("htmlTitleCheckBox")
        self.verticalLayout_3.addWidget(self.htmlTitleCheckBox)
        self.htmlTabsCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.htmlTabsCheckBox.setObjectName("htmlTabsCheckBox")
        self.verticalLayout_3.addWidget(self.htmlTabsCheckBox)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(507, 21, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.stackedWidget.addWidget(self.htmlPage)
        self.odtPage = QtWidgets.QWidget()
        self.odtPage.setObjectName("odtPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.odtPage)
        self.verticalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.odtPage)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.odtWysiwygCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.odtWysiwygCheckBox.setObjectName("odtWysiwygCheckBox")
        self.verticalLayout.addWidget(self.odtWysiwygCheckBox)
        self.odtStylesCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.odtStylesCheckBox.setObjectName("odtStylesCheckBox")
        self.verticalLayout.addWidget(self.odtStylesCheckBox)
        self.odtTabsCheckBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.odtTabsCheckBox.setObjectName("odtTabsCheckBox")
        self.verticalLayout.addWidget(self.odtTabsCheckBox)
        self.verticalLayout_2.addWidget(self.groupBox_3)
        spacerItem1 = QtWidgets.QSpacerItem(498, 136, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.odtPage)
        self.pdfPage = QtWidgets.QWidget()
        self.pdfPage.setObjectName("pdfPage")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.pdfPage)
        self.verticalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_4 = QtWidgets.QGroupBox(self.pdfPage)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pdfMagnificationSlider = QtWidgets.QSlider(self.groupBox_4)
        self.pdfMagnificationSlider.setMaximum(20)
        self.pdfMagnificationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.pdfMagnificationSlider.setObjectName("pdfMagnificationSlider")
        self.gridLayout.addWidget(self.pdfMagnificationSlider, 0, 1, 1, 1)
        self.pdfMagnificationLCD = QtWidgets.QLCDNumber(self.groupBox_4)
        self.pdfMagnificationLCD.setDigitCount(2)
        self.pdfMagnificationLCD.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.pdfMagnificationLCD.setObjectName("pdfMagnificationLCD")
        self.gridLayout.addWidget(self.pdfMagnificationLCD, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pdfFontCombo = QtWidgets.QComboBox(self.groupBox_4)
        self.pdfFontCombo.setObjectName("pdfFontCombo")
        self.gridLayout.addWidget(self.pdfFontCombo, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.pdfPageSizeCombo = QtWidgets.QComboBox(self.groupBox_4)
        self.pdfPageSizeCombo.setObjectName("pdfPageSizeCombo")
        self.gridLayout.addWidget(self.pdfPageSizeCombo, 2, 1, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox.setObjectName("groupBox")
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")
        self.pdfMarginTopSpin = QtWidgets.QSpinBox(self.groupBox)
        self.pdfMarginTopSpin.setMaximum(288)
        self.pdfMarginTopSpin.setObjectName("pdfMarginTopSpin")
        self.gridlayout.addWidget(self.pdfMarginTopSpin, 0, 1, 1, 1)
        self.pdfMarginLeftSpin = QtWidgets.QSpinBox(self.groupBox)
        self.pdfMarginLeftSpin.setMaximum(288)
        self.pdfMarginLeftSpin.setObjectName("pdfMarginLeftSpin")
        self.gridlayout.addWidget(self.pdfMarginLeftSpin, 1, 0, 1, 1)
        self.pdfMarginRightSpin = QtWidgets.QSpinBox(self.groupBox)
        self.pdfMarginRightSpin.setMaximum(288)
        self.pdfMarginRightSpin.setObjectName("pdfMarginRightSpin")
        self.gridlayout.addWidget(self.pdfMarginRightSpin, 1, 2, 1, 1)
        self.pdfMarginBottomSpin = QtWidgets.QSpinBox(self.groupBox)
        self.pdfMarginBottomSpin.setMaximum(288)
        self.pdfMarginBottomSpin.setObjectName("pdfMarginBottomSpin")
        self.gridlayout.addWidget(self.pdfMarginBottomSpin, 2, 1, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 3)
        self.verticalLayout_5.addWidget(self.groupBox_4)
        spacerItem3 = QtWidgets.QSpacerItem(20, 21, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.stackedWidget.addWidget(self.pdfPage)
        self.rtfPage = QtWidgets.QWidget()
        self.rtfPage.setObjectName("rtfPage")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.rtfPage)
        self.verticalLayout_7.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_5 = QtWidgets.QGroupBox(self.rtfPage)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.rtfWysiwygCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.rtfWysiwygCheckBox.setObjectName("rtfWysiwygCheckBox")
        self.verticalLayout_6.addWidget(self.rtfWysiwygCheckBox)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.rtfFontButton = QtWidgets.QPushButton(self.groupBox_5)
        self.rtfFontButton.setObjectName("rtfFontButton")
        self.hboxlayout1.addWidget(self.rtfFontButton)
        self.rtfFontSample = QtWidgets.QLineEdit(self.groupBox_5)
        self.rtfFontSample.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rtfFontSample.setAlignment(QtCore.Qt.AlignHCenter)
        self.rtfFontSample.setReadOnly(True)
        self.rtfFontSample.setObjectName("rtfFontSample")
        self.hboxlayout1.addWidget(self.rtfFontSample)
        self.verticalLayout_6.addLayout(self.hboxlayout1)
        self.rtfTabsCheckBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.rtfTabsCheckBox.setObjectName("rtfTabsCheckBox")
        self.verticalLayout_6.addWidget(self.rtfTabsCheckBox)
        self.verticalLayout_7.addWidget(self.groupBox_5)
        spacerItem4 = QtWidgets.QSpacerItem(451, 21, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem4)
        self.stackedWidget.addWidget(self.rtfPage)
        self.texPage = QtWidgets.QWidget()
        self.texPage.setObjectName("texPage")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.texPage)
        self.verticalLayout_9.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_6 = QtWidgets.QGroupBox(self.texPage)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.texStylesCheckBox = QtWidgets.QCheckBox(self.groupBox_6)
        self.texStylesCheckBox.setObjectName("texStylesCheckBox")
        self.verticalLayout_8.addWidget(self.texStylesCheckBox)
        self.texTitleCheckBox = QtWidgets.QCheckBox(self.groupBox_6)
        self.texTitleCheckBox.setObjectName("texTitleCheckBox")
        self.verticalLayout_8.addWidget(self.texTitleCheckBox)
        self.verticalLayout_9.addWidget(self.groupBox_6)
        spacerItem5 = QtWidgets.QSpacerItem(507, 21, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem5)
        self.stackedWidget.addWidget(self.texPage)
        self.verticalLayout_10.addWidget(self.stackedWidget)
        spacerItem6 = QtWidgets.QSpacerItem(519, 21, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem6)

        self.retranslateUi(EditorExportersPage)
        self.stackedWidget.setCurrentIndex(0)
        self.rtfWysiwygCheckBox.toggled['bool'].connect(self.rtfFontButton.setDisabled)
        self.rtfWysiwygCheckBox.toggled['bool'].connect(self.rtfFontSample.setDisabled)
        self.pdfMagnificationSlider.sliderMoved['int'].connect(self.pdfMagnificationLCD.display)
        self.pdfMagnificationSlider.valueChanged['int'].connect(self.pdfMagnificationLCD.display)
        QtCore.QMetaObject.connectSlotsByName(EditorExportersPage)
        EditorExportersPage.setTabOrder(self.exportersCombo, self.htmlWysiwygCheckBox)
        EditorExportersPage.setTabOrder(self.htmlWysiwygCheckBox, self.htmlFoldingCheckBox)
        EditorExportersPage.setTabOrder(self.htmlFoldingCheckBox, self.htmlStylesCheckBox)
        EditorExportersPage.setTabOrder(self.htmlStylesCheckBox, self.htmlTitleCheckBox)
        EditorExportersPage.setTabOrder(self.htmlTitleCheckBox, self.htmlTabsCheckBox)
        EditorExportersPage.setTabOrder(self.htmlTabsCheckBox, self.odtWysiwygCheckBox)
        EditorExportersPage.setTabOrder(self.odtWysiwygCheckBox, self.odtStylesCheckBox)
        EditorExportersPage.setTabOrder(self.odtStylesCheckBox, self.odtTabsCheckBox)
        EditorExportersPage.setTabOrder(self.odtTabsCheckBox, self.pdfMagnificationSlider)
        EditorExportersPage.setTabOrder(self.pdfMagnificationSlider, self.pdfFontCombo)
        EditorExportersPage.setTabOrder(self.pdfFontCombo, self.pdfPageSizeCombo)
        EditorExportersPage.setTabOrder(self.pdfPageSizeCombo, self.pdfMarginTopSpin)
        EditorExportersPage.setTabOrder(self.pdfMarginTopSpin, self.pdfMarginLeftSpin)
        EditorExportersPage.setTabOrder(self.pdfMarginLeftSpin, self.pdfMarginRightSpin)
        EditorExportersPage.setTabOrder(self.pdfMarginRightSpin, self.pdfMarginBottomSpin)
        EditorExportersPage.setTabOrder(self.pdfMarginBottomSpin, self.rtfWysiwygCheckBox)
        EditorExportersPage.setTabOrder(self.rtfWysiwygCheckBox, self.rtfFontButton)
        EditorExportersPage.setTabOrder(self.rtfFontButton, self.rtfTabsCheckBox)
        EditorExportersPage.setTabOrder(self.rtfTabsCheckBox, self.texStylesCheckBox)
        EditorExportersPage.setTabOrder(self.texStylesCheckBox, self.texTitleCheckBox)

    def retranslateUi(self, EditorExportersPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorExportersPage", "<b>Configure exporters</b>"))
        self.TextLabel1_3.setText(_translate("EditorExportersPage", "Exporter Type:"))
        self.exportersCombo.setToolTip(_translate("EditorExportersPage", "Select the exporter to be configured."))
        self.htmlWysiwygCheckBox.setToolTip(_translate("EditorExportersPage", "Select to export in WYSIWYG mode"))
        self.htmlWysiwygCheckBox.setText(_translate("EditorExportersPage", "Use WYSIWYG mode"))
        self.htmlFoldingCheckBox.setToolTip(_translate("EditorExportersPage", "Select to include folding functionality"))
        self.htmlFoldingCheckBox.setText(_translate("EditorExportersPage", "Include folding functionality"))
        self.htmlStylesCheckBox.setToolTip(_translate("EditorExportersPage", "Select to include only used styles"))
        self.htmlStylesCheckBox.setText(_translate("EditorExportersPage", "Include only used styles"))
        self.htmlTitleCheckBox.setToolTip(_translate("EditorExportersPage", "Select to use the full pathname as the document title"))
        self.htmlTitleCheckBox.setText(_translate("EditorExportersPage", "Use full pathname as document title"))
        self.htmlTabsCheckBox.setToolTip(_translate("EditorExportersPage", "Select to use tabs in the generated file"))
        self.htmlTabsCheckBox.setText(_translate("EditorExportersPage", "Use tabs"))
        self.odtWysiwygCheckBox.setToolTip(_translate("EditorExportersPage", "Select to export in WYSIWYG mode"))
        self.odtWysiwygCheckBox.setText(_translate("EditorExportersPage", "Use WYSIWYG mode"))
        self.odtStylesCheckBox.setToolTip(_translate("EditorExportersPage", "Select to include only used styles"))
        self.odtStylesCheckBox.setText(_translate("EditorExportersPage", "Include only used styles"))
        self.odtTabsCheckBox.setToolTip(_translate("EditorExportersPage", "Select to use tabs in the generated file"))
        self.odtTabsCheckBox.setText(_translate("EditorExportersPage", "Use tabs"))
        self.label.setText(_translate("EditorExportersPage", "Magnification:"))
        self.pdfMagnificationSlider.setToolTip(_translate("EditorExportersPage", "Select the magnification value to be added to the font sizes of the styles"))
        self.pdfMagnificationLCD.setToolTip(_translate("EditorExportersPage", "Displays the selected magnification value"))
        self.label_2.setText(_translate("EditorExportersPage", "Font:"))
        self.pdfFontCombo.setToolTip(_translate("EditorExportersPage", "Select the font from the list"))
        self.label_3.setText(_translate("EditorExportersPage", "Pagesize:"))
        self.pdfPageSizeCombo.setToolTip(_translate("EditorExportersPage", "Select the page size from the list"))
        self.groupBox.setTitle(_translate("EditorExportersPage", "Margins"))
        self.pdfMarginTopSpin.setToolTip(_translate("EditorExportersPage", "Select the top margin in points (72 pt == 1\")"))
        self.pdfMarginLeftSpin.setToolTip(_translate("EditorExportersPage", "Select the left margin in points (72 pt == 1\")"))
        self.pdfMarginRightSpin.setToolTip(_translate("EditorExportersPage", "Select the right margin in points (72 pt == 1\")"))
        self.pdfMarginBottomSpin.setToolTip(_translate("EditorExportersPage", "Select the bottom margin in points (72 pt == 1\")"))
        self.rtfWysiwygCheckBox.setToolTip(_translate("EditorExportersPage", "Select to export in WYSIWYG mode"))
        self.rtfWysiwygCheckBox.setText(_translate("EditorExportersPage", "Use WYSIWYG mode"))
        self.rtfFontButton.setToolTip(_translate("EditorExportersPage", "Press to select the font for the RTF export"))
        self.rtfFontButton.setText(_translate("EditorExportersPage", "Select Font"))
        self.rtfFontSample.setText(_translate("EditorExportersPage", "Font for RTF export"))
        self.rtfTabsCheckBox.setToolTip(_translate("EditorExportersPage", "Select to use tabs in the generated file"))
        self.rtfTabsCheckBox.setText(_translate("EditorExportersPage", "Use tabs"))
        self.texStylesCheckBox.setToolTip(_translate("EditorExportersPage", "Select to include only used styles"))
        self.texStylesCheckBox.setText(_translate("EditorExportersPage", "Include only used styles"))
        self.texTitleCheckBox.setToolTip(_translate("EditorExportersPage", "Select to use the full pathname as the document title"))
        self.texTitleCheckBox.setText(_translate("EditorExportersPage", "Use full pathname as document title"))