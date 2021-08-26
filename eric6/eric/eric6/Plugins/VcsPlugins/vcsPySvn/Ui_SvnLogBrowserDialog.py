# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsPySvn\SvnLogBrowserDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SvnLogBrowserDialog(object):
    def setupUi(self, SvnLogBrowserDialog):
        SvnLogBrowserDialog.setObjectName("SvnLogBrowserDialog")
        SvnLogBrowserDialog.resize(700, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(SvnLogBrowserDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = QtWidgets.QLabel(SvnLogBrowserDialog)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.fromDate = QtWidgets.QDateEdit(SvnLogBrowserDialog)
        self.fromDate.setCalendarPopup(True)
        self.fromDate.setObjectName("fromDate")
        self.hboxlayout.addWidget(self.fromDate)
        self.label_2 = QtWidgets.QLabel(SvnLogBrowserDialog)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)
        self.toDate = QtWidgets.QDateEdit(SvnLogBrowserDialog)
        self.toDate.setCalendarPopup(True)
        self.toDate.setObjectName("toDate")
        self.hboxlayout.addWidget(self.toDate)
        self.fieldCombo = QtWidgets.QComboBox(SvnLogBrowserDialog)
        self.fieldCombo.setObjectName("fieldCombo")
        self.fieldCombo.addItem("")
        self.fieldCombo.addItem("")
        self.fieldCombo.addItem("")
        self.hboxlayout.addWidget(self.fieldCombo)
        self.rxEdit = E5ClearableLineEdit(SvnLogBrowserDialog)
        self.rxEdit.setObjectName("rxEdit")
        self.hboxlayout.addWidget(self.rxEdit)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.logTree = QtWidgets.QTreeWidget(SvnLogBrowserDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.logTree.sizePolicy().hasHeightForWidth())
        self.logTree.setSizePolicy(sizePolicy)
        self.logTree.setAlternatingRowColors(True)
        self.logTree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.logTree.setRootIsDecorated(False)
        self.logTree.setItemsExpandable(False)
        self.logTree.setAllColumnsShowFocus(True)
        self.logTree.setObjectName("logTree")
        self.verticalLayout.addWidget(self.logTree)
        self.messageEdit = QtWidgets.QTextEdit(SvnLogBrowserDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.messageEdit.sizePolicy().hasHeightForWidth())
        self.messageEdit.setSizePolicy(sizePolicy)
        self.messageEdit.setReadOnly(True)
        self.messageEdit.setObjectName("messageEdit")
        self.verticalLayout.addWidget(self.messageEdit)
        self.filesTree = QtWidgets.QTreeWidget(SvnLogBrowserDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.filesTree.sizePolicy().hasHeightForWidth())
        self.filesTree.setSizePolicy(sizePolicy)
        self.filesTree.setAlternatingRowColors(True)
        self.filesTree.setRootIsDecorated(False)
        self.filesTree.setItemsExpandable(False)
        self.filesTree.setAllColumnsShowFocus(True)
        self.filesTree.setObjectName("filesTree")
        self.verticalLayout.addWidget(self.filesTree)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.nextButton = QtWidgets.QPushButton(SvnLogBrowserDialog)
        self.nextButton.setObjectName("nextButton")
        self.gridLayout.addWidget(self.nextButton, 0, 0, 1, 1)
        self.limitSpinBox = QtWidgets.QSpinBox(SvnLogBrowserDialog)
        self.limitSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.limitSpinBox.setMinimum(1)
        self.limitSpinBox.setMaximum(10000)
        self.limitSpinBox.setProperty("value", 20)
        self.limitSpinBox.setObjectName("limitSpinBox")
        self.gridLayout.addWidget(self.limitSpinBox, 0, 1, 1, 1)
        self.stopCheckBox = QtWidgets.QCheckBox(SvnLogBrowserDialog)
        self.stopCheckBox.setObjectName("stopCheckBox")
        self.gridLayout.addWidget(self.stopCheckBox, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(SvnLogBrowserDialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 3, 2, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.upButton = QtWidgets.QToolButton(SvnLogBrowserDialog)
        self.upButton.setAutoRepeat(True)
        self.upButton.setObjectName("upButton")
        self.horizontalLayout.addWidget(self.upButton)
        self.downButton = QtWidgets.QToolButton(SvnLogBrowserDialog)
        self.downButton.setAutoRepeat(True)
        self.downButton.setObjectName("downButton")
        self.horizontalLayout.addWidget(self.downButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 4, 1, 1)
        self.diffPreviousButton = QtWidgets.QPushButton(SvnLogBrowserDialog)
        self.diffPreviousButton.setObjectName("diffPreviousButton")
        self.gridLayout.addWidget(self.diffPreviousButton, 0, 5, 1, 1)
        self.diffRevisionsButton = QtWidgets.QPushButton(SvnLogBrowserDialog)
        self.diffRevisionsButton.setObjectName("diffRevisionsButton")
        self.gridLayout.addWidget(self.diffRevisionsButton, 0, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(38, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 7, 1, 1)
        self.sbsCheckBox = QtWidgets.QCheckBox(SvnLogBrowserDialog)
        self.sbsCheckBox.setObjectName("sbsCheckBox")
        self.gridLayout.addWidget(self.sbsCheckBox, 1, 4, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(SvnLogBrowserDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SvnLogBrowserDialog)
        QtCore.QMetaObject.connectSlotsByName(SvnLogBrowserDialog)
        SvnLogBrowserDialog.setTabOrder(self.fromDate, self.toDate)
        SvnLogBrowserDialog.setTabOrder(self.toDate, self.fieldCombo)
        SvnLogBrowserDialog.setTabOrder(self.fieldCombo, self.rxEdit)
        SvnLogBrowserDialog.setTabOrder(self.rxEdit, self.logTree)
        SvnLogBrowserDialog.setTabOrder(self.logTree, self.messageEdit)
        SvnLogBrowserDialog.setTabOrder(self.messageEdit, self.filesTree)
        SvnLogBrowserDialog.setTabOrder(self.filesTree, self.nextButton)
        SvnLogBrowserDialog.setTabOrder(self.nextButton, self.limitSpinBox)
        SvnLogBrowserDialog.setTabOrder(self.limitSpinBox, self.stopCheckBox)
        SvnLogBrowserDialog.setTabOrder(self.stopCheckBox, self.upButton)
        SvnLogBrowserDialog.setTabOrder(self.upButton, self.downButton)
        SvnLogBrowserDialog.setTabOrder(self.downButton, self.diffPreviousButton)
        SvnLogBrowserDialog.setTabOrder(self.diffPreviousButton, self.diffRevisionsButton)
        SvnLogBrowserDialog.setTabOrder(self.diffRevisionsButton, self.sbsCheckBox)

    def retranslateUi(self, SvnLogBrowserDialog):
        _translate = QtCore.QCoreApplication.translate
        SvnLogBrowserDialog.setWindowTitle(_translate("SvnLogBrowserDialog", "Subversion Log"))
        self.label.setText(_translate("SvnLogBrowserDialog", "From:"))
        self.fromDate.setToolTip(_translate("SvnLogBrowserDialog", "Enter the start date"))
        self.label_2.setText(_translate("SvnLogBrowserDialog", "To:"))
        self.toDate.setToolTip(_translate("SvnLogBrowserDialog", "Enter the end date"))
        self.fieldCombo.setToolTip(_translate("SvnLogBrowserDialog", "Select the field to filter on"))
        self.fieldCombo.setItemText(0, _translate("SvnLogBrowserDialog", "Revision"))
        self.fieldCombo.setItemText(1, _translate("SvnLogBrowserDialog", "Author"))
        self.fieldCombo.setItemText(2, _translate("SvnLogBrowserDialog", "Message"))
        self.rxEdit.setToolTip(_translate("SvnLogBrowserDialog", "Enter the regular expression to filter on"))
        self.logTree.setSortingEnabled(True)
        self.logTree.headerItem().setText(0, _translate("SvnLogBrowserDialog", "Revision"))
        self.logTree.headerItem().setText(1, _translate("SvnLogBrowserDialog", "Author"))
        self.logTree.headerItem().setText(2, _translate("SvnLogBrowserDialog", "Date"))
        self.logTree.headerItem().setText(3, _translate("SvnLogBrowserDialog", "Message"))
        self.filesTree.setSortingEnabled(True)
        self.filesTree.headerItem().setText(0, _translate("SvnLogBrowserDialog", "Action"))
        self.filesTree.headerItem().setText(1, _translate("SvnLogBrowserDialog", "Path"))
        self.filesTree.headerItem().setText(2, _translate("SvnLogBrowserDialog", "Copy from"))
        self.filesTree.headerItem().setText(3, _translate("SvnLogBrowserDialog", "Copy from Rev"))
        self.nextButton.setToolTip(_translate("SvnLogBrowserDialog", "Press to get the next bunch of log entries"))
        self.nextButton.setText(_translate("SvnLogBrowserDialog", "&Next"))
        self.limitSpinBox.setToolTip(_translate("SvnLogBrowserDialog", "Enter the limit of entries to fetch"))
        self.stopCheckBox.setToolTip(_translate("SvnLogBrowserDialog", "Select to stop listing log messages at a copy or move"))
        self.stopCheckBox.setText(_translate("SvnLogBrowserDialog", "Stop on Copy/Move"))
        self.upButton.setToolTip(_translate("SvnLogBrowserDialog", "Press to move up in the log list"))
        self.downButton.setToolTip(_translate("SvnLogBrowserDialog", "Press to move down in the log list"))
        self.diffPreviousButton.setToolTip(_translate("SvnLogBrowserDialog", "Press to generate a diff to the previous revision"))
        self.diffPreviousButton.setText(_translate("SvnLogBrowserDialog", "&Diff to Previous"))
        self.diffRevisionsButton.setToolTip(_translate("SvnLogBrowserDialog", "Press to compare two revisions"))
        self.diffRevisionsButton.setText(_translate("SvnLogBrowserDialog", "&Compare Revisions"))
        self.sbsCheckBox.setToolTip(_translate("SvnLogBrowserDialog", "Select to show differences side-by-side"))
        self.sbsCheckBox.setText(_translate("SvnLogBrowserDialog", "Show differences side-by-side"))
from E5Gui.E5LineEdit import E5ClearableLineEdit
