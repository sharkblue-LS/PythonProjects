# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\EditorKeywordsPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorKeywordsPage(object):
    def setupUi(self, EditorKeywordsPage):
        EditorKeywordsPage.setObjectName("EditorKeywordsPage")
        EditorKeywordsPage.resize(462, 422)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditorKeywordsPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(EditorKeywordsPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line5 = QtWidgets.QFrame(EditorKeywordsPage)
        self.line5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line5.setObjectName("line5")
        self.verticalLayout.addWidget(self.line5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextLabel1_3_3 = QtWidgets.QLabel(EditorKeywordsPage)
        self.TextLabel1_3_3.setToolTip("")
        self.TextLabel1_3_3.setObjectName("TextLabel1_3_3")
        self.horizontalLayout.addWidget(self.TextLabel1_3_3)
        self.languageCombo = QtWidgets.QComboBox(EditorKeywordsPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.languageCombo.sizePolicy().hasHeightForWidth())
        self.languageCombo.setSizePolicy(sizePolicy)
        self.languageCombo.setObjectName("languageCombo")
        self.horizontalLayout.addWidget(self.languageCombo)
        self.label = QtWidgets.QLabel(EditorKeywordsPage)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.setSpinBox = QtWidgets.QSpinBox(EditorKeywordsPage)
        self.setSpinBox.setMinimum(1)
        self.setSpinBox.setMaximum(8)
        self.setSpinBox.setObjectName("setSpinBox")
        self.horizontalLayout.addWidget(self.setSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setDescriptionLabel = QtWidgets.QLabel(EditorKeywordsPage)
        self.setDescriptionLabel.setText("")
        self.setDescriptionLabel.setObjectName("setDescriptionLabel")
        self.verticalLayout.addWidget(self.setDescriptionLabel)
        self.keywordsEdit = QtWidgets.QPlainTextEdit(EditorKeywordsPage)
        self.keywordsEdit.setObjectName("keywordsEdit")
        self.verticalLayout.addWidget(self.keywordsEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.defaultButton = QtWidgets.QPushButton(EditorKeywordsPage)
        self.defaultButton.setObjectName("defaultButton")
        self.horizontalLayout_2.addWidget(self.defaultButton)
        self.allDefaultButton = QtWidgets.QPushButton(EditorKeywordsPage)
        self.allDefaultButton.setObjectName("allDefaultButton")
        self.horizontalLayout_2.addWidget(self.allDefaultButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(EditorKeywordsPage)
        QtCore.QMetaObject.connectSlotsByName(EditorKeywordsPage)
        EditorKeywordsPage.setTabOrder(self.languageCombo, self.setSpinBox)
        EditorKeywordsPage.setTabOrder(self.setSpinBox, self.keywordsEdit)

    def retranslateUi(self, EditorKeywordsPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EditorKeywordsPage", "<b>Configure syntax highlighter keywords</b>"))
        self.TextLabel1_3_3.setText(_translate("EditorKeywordsPage", "Language:"))
        self.languageCombo.setToolTip(_translate("EditorKeywordsPage", "Select the language to be configured."))
        self.label.setText(_translate("EditorKeywordsPage", "Set:"))
        self.keywordsEdit.setToolTip(_translate("EditorKeywordsPage", "Enter the keywords separated by a blank"))
        self.defaultButton.setToolTip(_translate("EditorKeywordsPage", "Press to set the current keyword set to the default value"))
        self.defaultButton.setText(_translate("EditorKeywordsPage", "to Default"))
        self.allDefaultButton.setToolTip(_translate("EditorKeywordsPage", "Press to set all keyword sets of the selected language to default values"))
        self.allDefaultButton.setText(_translate("EditorKeywordsPage", "All to Defaults"))
