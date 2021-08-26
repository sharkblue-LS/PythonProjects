# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\EditorLanguageTabIndentOverrideDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditorLanguageTabIndentOverrideDialog(object):
    def setupUi(self, EditorLanguageTabIndentOverrideDialog):
        EditorLanguageTabIndentOverrideDialog.setObjectName("EditorLanguageTabIndentOverrideDialog")
        EditorLanguageTabIndentOverrideDialog.resize(400, 145)
        EditorLanguageTabIndentOverrideDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(EditorLanguageTabIndentOverrideDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(EditorLanguageTabIndentOverrideDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.languageComboBox = QtWidgets.QComboBox(EditorLanguageTabIndentOverrideDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.languageComboBox.sizePolicy().hasHeightForWidth())
        self.languageComboBox.setSizePolicy(sizePolicy)
        self.languageComboBox.setObjectName("languageComboBox")
        self.gridLayout.addWidget(self.languageComboBox, 0, 1, 1, 2)
        self.pygmentsLabel = QtWidgets.QLabel(EditorLanguageTabIndentOverrideDialog)
        self.pygmentsLabel.setObjectName("pygmentsLabel")
        self.gridLayout.addWidget(self.pygmentsLabel, 1, 0, 1, 1)
        self.pygmentsLexerCombo = QtWidgets.QComboBox(EditorLanguageTabIndentOverrideDialog)
        self.pygmentsLexerCombo.setObjectName("pygmentsLexerCombo")
        self.gridLayout.addWidget(self.pygmentsLexerCombo, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(EditorLanguageTabIndentOverrideDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.tabWidthSpinBox = QtWidgets.QSpinBox(EditorLanguageTabIndentOverrideDialog)
        self.tabWidthSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tabWidthSpinBox.setMinimum(1)
        self.tabWidthSpinBox.setMaximum(20)
        self.tabWidthSpinBox.setObjectName("tabWidthSpinBox")
        self.gridLayout.addWidget(self.tabWidthSpinBox, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(208, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.TextLabel13_2_3 = QtWidgets.QLabel(EditorLanguageTabIndentOverrideDialog)
        self.TextLabel13_2_3.setObjectName("TextLabel13_2_3")
        self.gridLayout.addWidget(self.TextLabel13_2_3, 3, 0, 1, 1)
        self.indentWidthSpinBox = QtWidgets.QSpinBox(EditorLanguageTabIndentOverrideDialog)
        self.indentWidthSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.indentWidthSpinBox.setMinimum(1)
        self.indentWidthSpinBox.setMaximum(20)
        self.indentWidthSpinBox.setObjectName("indentWidthSpinBox")
        self.gridLayout.addWidget(self.indentWidthSpinBox, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(208, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(EditorLanguageTabIndentOverrideDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)

        self.retranslateUi(EditorLanguageTabIndentOverrideDialog)
        self.buttonBox.accepted.connect(EditorLanguageTabIndentOverrideDialog.accept)
        self.buttonBox.rejected.connect(EditorLanguageTabIndentOverrideDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EditorLanguageTabIndentOverrideDialog)
        EditorLanguageTabIndentOverrideDialog.setTabOrder(self.languageComboBox, self.pygmentsLexerCombo)
        EditorLanguageTabIndentOverrideDialog.setTabOrder(self.pygmentsLexerCombo, self.tabWidthSpinBox)
        EditorLanguageTabIndentOverrideDialog.setTabOrder(self.tabWidthSpinBox, self.indentWidthSpinBox)

    def retranslateUi(self, EditorLanguageTabIndentOverrideDialog):
        _translate = QtCore.QCoreApplication.translate
        EditorLanguageTabIndentOverrideDialog.setWindowTitle(_translate("EditorLanguageTabIndentOverrideDialog", "Tab and Indent Override"))
        self.label.setText(_translate("EditorLanguageTabIndentOverrideDialog", "Lexer Language:"))
        self.languageComboBox.setToolTip(_translate("EditorLanguageTabIndentOverrideDialog", "Select the lexer language to override"))
        self.pygmentsLabel.setText(_translate("EditorLanguageTabIndentOverrideDialog", "Alternative Lexer:"))
        self.pygmentsLexerCombo.setToolTip(_translate("EditorLanguageTabIndentOverrideDialog", "Select the alternative lexer to override"))
        self.label_2.setText(_translate("EditorLanguageTabIndentOverrideDialog", "Tab Width:"))
        self.tabWidthSpinBox.setToolTip(_translate("EditorLanguageTabIndentOverrideDialog", "Enter the tab width"))
        self.TextLabel13_2_3.setText(_translate("EditorLanguageTabIndentOverrideDialog", "Indentation width:"))
        self.indentWidthSpinBox.setToolTip(_translate("EditorLanguageTabIndentOverrideDialog", "Enter the indentation width"))