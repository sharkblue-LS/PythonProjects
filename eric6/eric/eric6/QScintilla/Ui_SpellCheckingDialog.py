# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\QScintilla\SpellCheckingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SpellCheckingDialog(object):
    def setupUi(self, SpellCheckingDialog):
        SpellCheckingDialog.setObjectName("SpellCheckingDialog")
        SpellCheckingDialog.resize(696, 366)
        SpellCheckingDialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(SpellCheckingDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(SpellCheckingDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.languageLabel = QtWidgets.QLabel(SpellCheckingDialog)
        self.languageLabel.setText("")
        self.languageLabel.setObjectName("languageLabel")
        self.horizontalLayout.addWidget(self.languageLabel)
        spacerItem1 = QtWidgets.QSpacerItem(328, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.line_2 = QtWidgets.QFrame(SpellCheckingDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(SpellCheckingDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.contextLabel = QtWidgets.QLabel(SpellCheckingDialog)
        self.contextLabel.setFrameShape(QtWidgets.QFrame.Panel)
        self.contextLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.contextLabel.setText("")
        self.contextLabel.setTextFormat(QtCore.Qt.RichText)
        self.contextLabel.setWordWrap(True)
        self.contextLabel.setObjectName("contextLabel")
        self.gridLayout.addWidget(self.contextLabel, 1, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(SpellCheckingDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.changeEdit = QtWidgets.QLineEdit(SpellCheckingDialog)
        self.changeEdit.setObjectName("changeEdit")
        self.gridLayout.addWidget(self.changeEdit, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(SpellCheckingDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
        self.suggestionsList = QtWidgets.QListWidget(SpellCheckingDialog)
        self.suggestionsList.setObjectName("suggestionsList")
        self.gridLayout.addWidget(self.suggestionsList, 4, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ignoreButton = QtWidgets.QPushButton(SpellCheckingDialog)
        self.ignoreButton.setObjectName("ignoreButton")
        self.verticalLayout.addWidget(self.ignoreButton)
        self.ignoreAllButton = QtWidgets.QPushButton(SpellCheckingDialog)
        self.ignoreAllButton.setObjectName("ignoreAllButton")
        self.verticalLayout.addWidget(self.ignoreAllButton)
        self.addButton = QtWidgets.QPushButton(SpellCheckingDialog)
        self.addButton.setObjectName("addButton")
        self.verticalLayout.addWidget(self.addButton)
        self.line = QtWidgets.QFrame(SpellCheckingDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.replaceButton = QtWidgets.QPushButton(SpellCheckingDialog)
        self.replaceButton.setObjectName("replaceButton")
        self.verticalLayout.addWidget(self.replaceButton)
        self.replaceAllButton = QtWidgets.QPushButton(SpellCheckingDialog)
        self.replaceAllButton.setObjectName("replaceAllButton")
        self.verticalLayout.addWidget(self.replaceAllButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(SpellCheckingDialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_2.addWidget(self.line_3, 3, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(SpellCheckingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.label_3.setBuddy(self.changeEdit)
        self.label_4.setBuddy(self.suggestionsList)

        self.retranslateUi(SpellCheckingDialog)
        self.buttonBox.accepted.connect(SpellCheckingDialog.accept)
        self.buttonBox.rejected.connect(SpellCheckingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SpellCheckingDialog)
        SpellCheckingDialog.setTabOrder(self.changeEdit, self.suggestionsList)
        SpellCheckingDialog.setTabOrder(self.suggestionsList, self.ignoreButton)
        SpellCheckingDialog.setTabOrder(self.ignoreButton, self.ignoreAllButton)
        SpellCheckingDialog.setTabOrder(self.ignoreAllButton, self.addButton)
        SpellCheckingDialog.setTabOrder(self.addButton, self.replaceButton)
        SpellCheckingDialog.setTabOrder(self.replaceButton, self.replaceAllButton)
        SpellCheckingDialog.setTabOrder(self.replaceAllButton, self.buttonBox)

    def retranslateUi(self, SpellCheckingDialog):
        _translate = QtCore.QCoreApplication.translate
        SpellCheckingDialog.setWindowTitle(_translate("SpellCheckingDialog", "Check spelling"))
        self.label_2.setText(_translate("SpellCheckingDialog", "Current language:"))
        self.languageLabel.setToolTip(_translate("SpellCheckingDialog", "Shows the language used for spell checking"))
        self.label.setText(_translate("SpellCheckingDialog", "Not found in dictionary"))
        self.contextLabel.setToolTip(_translate("SpellCheckingDialog", "Shows the unrecognized word with some context"))
        self.label_3.setText(_translate("SpellCheckingDialog", "Change &to:"))
        self.label_4.setText(_translate("SpellCheckingDialog", "&Suggestions:"))
        self.ignoreButton.setToolTip(_translate("SpellCheckingDialog", "Press to ignore once"))
        self.ignoreButton.setText(_translate("SpellCheckingDialog", "&Ignore"))
        self.ignoreAllButton.setToolTip(_translate("SpellCheckingDialog", "Press to always ignore"))
        self.ignoreAllButton.setText(_translate("SpellCheckingDialog", "I&gnore All"))
        self.addButton.setToolTip(_translate("SpellCheckingDialog", "Press to add to dictionary"))
        self.addButton.setText(_translate("SpellCheckingDialog", "&Add to dictionary"))
        self.replaceButton.setToolTip(_translate("SpellCheckingDialog", "Press to replace the word"))
        self.replaceButton.setText(_translate("SpellCheckingDialog", "&Replace"))
        self.replaceAllButton.setToolTip(_translate("SpellCheckingDialog", "Press to replace all occurrences"))
        self.replaceAllButton.setText(_translate("SpellCheckingDialog", "Re&place All"))
