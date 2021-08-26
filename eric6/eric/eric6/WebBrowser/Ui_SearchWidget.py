# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\SearchWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchWidget(object):
    def setupUi(self, SearchWidget):
        SearchWidget.setObjectName("SearchWidget")
        SearchWidget.resize(747, 26)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SearchWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.closeButton = QtWidgets.QToolButton(SearchWidget)
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.label = QtWidgets.QLabel(SearchWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.findtextCombo = QtWidgets.QComboBox(SearchWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findtextCombo.sizePolicy().hasHeightForWidth())
        self.findtextCombo.setSizePolicy(sizePolicy)
        self.findtextCombo.setEditable(True)
        self.findtextCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.findtextCombo.setDuplicatesEnabled(False)
        self.findtextCombo.setObjectName("findtextCombo")
        self.horizontalLayout_2.addWidget(self.findtextCombo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.findPrevButton = QtWidgets.QToolButton(SearchWidget)
        self.findPrevButton.setObjectName("findPrevButton")
        self.horizontalLayout.addWidget(self.findPrevButton)
        self.findNextButton = QtWidgets.QToolButton(SearchWidget)
        self.findNextButton.setObjectName("findNextButton")
        self.horizontalLayout.addWidget(self.findNextButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.caseCheckBox = QtWidgets.QCheckBox(SearchWidget)
        self.caseCheckBox.setObjectName("caseCheckBox")
        self.horizontalLayout_2.addWidget(self.caseCheckBox)
        self.infoLine = QtWidgets.QFrame(SearchWidget)
        self.infoLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.infoLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.infoLine.setObjectName("infoLine")
        self.horizontalLayout_2.addWidget(self.infoLine)
        self.infoLabel = QtWidgets.QLabel(SearchWidget)
        self.infoLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.infoLabel.setText("")
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout_2.addWidget(self.infoLabel)

        self.retranslateUi(SearchWidget)
        QtCore.QMetaObject.connectSlotsByName(SearchWidget)
        SearchWidget.setTabOrder(self.findtextCombo, self.caseCheckBox)
        SearchWidget.setTabOrder(self.caseCheckBox, self.findNextButton)
        SearchWidget.setTabOrder(self.findNextButton, self.findPrevButton)
        SearchWidget.setTabOrder(self.findPrevButton, self.closeButton)

    def retranslateUi(self, SearchWidget):
        _translate = QtCore.QCoreApplication.translate
        SearchWidget.setWindowTitle(_translate("SearchWidget", "Find"))
        self.closeButton.setToolTip(_translate("SearchWidget", "Press to close the window"))
        self.label.setText(_translate("SearchWidget", "Find:"))
        self.findPrevButton.setToolTip(_translate("SearchWidget", "Press to find the previous occurrence"))
        self.findNextButton.setToolTip(_translate("SearchWidget", "Press to find the next occurrence"))
        self.caseCheckBox.setText(_translate("SearchWidget", "Match case"))
