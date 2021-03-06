# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Plugins\VcsPlugins\vcsMercurial\QueuesExtension\HgQueuesListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HgQueuesListDialog(object):
    def setupUi(self, HgQueuesListDialog):
        HgQueuesListDialog.setObjectName("HgQueuesListDialog")
        HgQueuesListDialog.resize(634, 494)
        HgQueuesListDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(HgQueuesListDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.patchesList = QtWidgets.QTreeWidget(HgQueuesListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.patchesList.sizePolicy().hasHeightForWidth())
        self.patchesList.setSizePolicy(sizePolicy)
        self.patchesList.setAlternatingRowColors(True)
        self.patchesList.setRootIsDecorated(False)
        self.patchesList.setItemsExpandable(False)
        self.patchesList.setObjectName("patchesList")
        self.patchesList.headerItem().setText(0, "#")
        self.patchesList.headerItem().setTextAlignment(0, QtCore.Qt.AlignLeading|QtCore.Qt.AlignVCenter)
        self.vboxlayout.addWidget(self.patchesList)
        self.errorGroup = QtWidgets.QGroupBox(HgQueuesListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.errors = QtWidgets.QTextEdit(self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout1.addWidget(self.errors)
        self.vboxlayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(HgQueuesListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(HgQueuesListDialog)
        QtCore.QMetaObject.connectSlotsByName(HgQueuesListDialog)
        HgQueuesListDialog.setTabOrder(self.patchesList, self.errors)
        HgQueuesListDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, HgQueuesListDialog):
        _translate = QtCore.QCoreApplication.translate
        HgQueuesListDialog.setWindowTitle(_translate("HgQueuesListDialog", "List of Patches"))
        HgQueuesListDialog.setWhatsThis(_translate("HgQueuesListDialog", "<b>List of Patches</b>\n"
"<p>This dialog shows a list of applied and unapplied patches.</p>"))
        self.patchesList.setWhatsThis(_translate("HgQueuesListDialog", "<b>Patches List</b>\n"
"<p>This shows a list of applied and unapplied patches.</p>"))
        self.patchesList.headerItem().setText(1, _translate("HgQueuesListDialog", "Name"))
        self.patchesList.headerItem().setText(2, _translate("HgQueuesListDialog", "Status"))
        self.patchesList.headerItem().setText(3, _translate("HgQueuesListDialog", "Summary"))
        self.errorGroup.setTitle(_translate("HgQueuesListDialog", "Errors"))
