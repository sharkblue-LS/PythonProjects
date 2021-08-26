# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsMercurial\HgConflictsListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgConflictsListDialog(object):
    def setupUi(self, HgConflictsListDialog):
        HgConflictsListDialog.setObjectName("HgConflictsListDialog")
        HgConflictsListDialog.resize(650, 450)
        HgConflictsListDialog.setProperty("sizeGripEnabled", True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgConflictsListDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.conflictsList = QtWidgets.QTreeWidget(HgConflictsListDialog)
        self.conflictsList.setAlternatingRowColors(True)
        self.conflictsList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.conflictsList.setRootIsDecorated(False)
        self.conflictsList.setItemsExpandable(False)
        self.conflictsList.setObjectName("conflictsList")
        self.verticalLayout.addWidget(self.conflictsList)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.resolvedButton = QtWidgets.QPushButton(HgConflictsListDialog)
        self.resolvedButton.setObjectName("resolvedButton")
        self.horizontalLayout.addWidget(self.resolvedButton)
        self.unresolvedButton = QtWidgets.QPushButton(HgConflictsListDialog)
        self.unresolvedButton.setObjectName("unresolvedButton")
        self.horizontalLayout.addWidget(self.unresolvedButton)
        self.line = QtWidgets.QFrame(HgConflictsListDialog)
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.reMergeButton = QtWidgets.QPushButton(HgConflictsListDialog)
        self.reMergeButton.setObjectName("reMergeButton")
        self.horizontalLayout.addWidget(self.reMergeButton)
        self.editButton = QtWidgets.QPushButton(HgConflictsListDialog)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.errorGroup = QtWidgets.QGroupBox(HgConflictsListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgConflictsListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgConflictsListDialog)
        QtCore.QMetaObject.connectSlotsByName(HgConflictsListDialog)
        HgConflictsListDialog.setTabOrder(self.conflictsList, self.resolvedButton)
        HgConflictsListDialog.setTabOrder(self.resolvedButton, self.unresolvedButton)
        HgConflictsListDialog.setTabOrder(self.unresolvedButton, self.reMergeButton)
        HgConflictsListDialog.setTabOrder(self.reMergeButton, self.editButton)
        HgConflictsListDialog.setTabOrder(self.editButton, self.errors)
        HgConflictsListDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, HgConflictsListDialog):
        _translate = QtCore.QCoreApplication.translate
        HgConflictsListDialog.setWindowTitle(_translate("HgConflictsListDialog", "Mercurial Conflicts"))
        self.conflictsList.setWhatsThis(_translate("HgConflictsListDialog", "<b>Conflicts List</b>\\n<p>This shows a list of files  which had or still have conflicts.</p>"))
        self.conflictsList.setSortingEnabled(True)
        self.conflictsList.headerItem().setText(0, _translate("HgConflictsListDialog", "Status"))
        self.conflictsList.headerItem().setText(1, _translate("HgConflictsListDialog", "Name"))
        self.resolvedButton.setToolTip(_translate("HgConflictsListDialog", "Press to mark the selected entries as \'resolved\'"))
        self.resolvedButton.setText(_translate("HgConflictsListDialog", "Resolved"))
        self.unresolvedButton.setToolTip(_translate("HgConflictsListDialog", "Press to mark the selected entries as \'unresolved\'"))
        self.unresolvedButton.setText(_translate("HgConflictsListDialog", "Unresolved"))
        self.reMergeButton.setToolTip(_translate("HgConflictsListDialog", "Press to re-merge the selected entries"))
        self.reMergeButton.setText(_translate("HgConflictsListDialog", "Re-Merge"))
        self.editButton.setToolTip(_translate("HgConflictsListDialog", "Press to edit the selected entry"))
        self.editButton.setText(_translate("HgConflictsListDialog", "Edit"))
        self.errorGroup.setTitle(_translate("HgConflictsListDialog", "Errors"))
