# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\VirusTotal\VirusTotalIpReportDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VirusTotalIpReportDialog(object):
    def setupUi(self, VirusTotalIpReportDialog):
        VirusTotalIpReportDialog.setObjectName("VirusTotalIpReportDialog")
        VirusTotalIpReportDialog.resize(800, 600)
        VirusTotalIpReportDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(VirusTotalIpReportDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.headerPixmap = QtWidgets.QLabel(VirusTotalIpReportDialog)
        self.headerPixmap.setObjectName("headerPixmap")
        self.horizontalLayout_4.addWidget(self.headerPixmap)
        self.headerLabel = QtWidgets.QLabel(VirusTotalIpReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerLabel.sizePolicy().hasHeightForWidth())
        self.headerLabel.setSizePolicy(sizePolicy)
        self.headerLabel.setObjectName("headerLabel")
        self.horizontalLayout_4.addWidget(self.headerLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.line9_3 = QtWidgets.QFrame(VirusTotalIpReportDialog)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setObjectName("line9_3")
        self.verticalLayout.addWidget(self.line9_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(VirusTotalIpReportDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ownerLabel = QtWidgets.QLabel(VirusTotalIpReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ownerLabel.sizePolicy().hasHeightForWidth())
        self.ownerLabel.setSizePolicy(sizePolicy)
        self.ownerLabel.setText("")
        self.ownerLabel.setObjectName("ownerLabel")
        self.horizontalLayout.addWidget(self.ownerLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.resolutionsGroup = QtWidgets.QGroupBox(VirusTotalIpReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.resolutionsGroup.sizePolicy().hasHeightForWidth())
        self.resolutionsGroup.setSizePolicy(sizePolicy)
        self.resolutionsGroup.setObjectName("resolutionsGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.resolutionsGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.resolutionsList = QtWidgets.QTreeWidget(self.resolutionsGroup)
        self.resolutionsList.setAlternatingRowColors(True)
        self.resolutionsList.setRootIsDecorated(False)
        self.resolutionsList.setAllColumnsShowFocus(True)
        self.resolutionsList.setObjectName("resolutionsList")
        self.verticalLayout_2.addWidget(self.resolutionsList)
        self.verticalLayout.addWidget(self.resolutionsGroup)
        self.detectedUrlsGroup = QtWidgets.QGroupBox(VirusTotalIpReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.detectedUrlsGroup.sizePolicy().hasHeightForWidth())
        self.detectedUrlsGroup.setSizePolicy(sizePolicy)
        self.detectedUrlsGroup.setObjectName("detectedUrlsGroup")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.detectedUrlsGroup)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.urlsList = QtWidgets.QTreeWidget(self.detectedUrlsGroup)
        self.urlsList.setAlternatingRowColors(True)
        self.urlsList.setRootIsDecorated(False)
        self.urlsList.setAllColumnsShowFocus(True)
        self.urlsList.setObjectName("urlsList")
        self.verticalLayout_3.addWidget(self.urlsList)
        self.verticalLayout.addWidget(self.detectedUrlsGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(VirusTotalIpReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(VirusTotalIpReportDialog)
        self.buttonBox.accepted.connect(VirusTotalIpReportDialog.accept)
        self.buttonBox.rejected.connect(VirusTotalIpReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VirusTotalIpReportDialog)

    def retranslateUi(self, VirusTotalIpReportDialog):
        _translate = QtCore.QCoreApplication.translate
        VirusTotalIpReportDialog.setWindowTitle(_translate("VirusTotalIpReportDialog", "IP Address Report"))
        self.label.setText(_translate("VirusTotalIpReportDialog", "Owner:"))
        self.resolutionsGroup.setTitle(_translate("VirusTotalIpReportDialog", "Resolutions"))
        self.resolutionsList.setSortingEnabled(True)
        self.resolutionsList.headerItem().setText(0, _translate("VirusTotalIpReportDialog", "Hostname"))
        self.resolutionsList.headerItem().setText(1, _translate("VirusTotalIpReportDialog", "Resolved Date"))
        self.detectedUrlsGroup.setTitle(_translate("VirusTotalIpReportDialog", "Detected URLs"))
        self.urlsList.setSortingEnabled(True)
        self.urlsList.headerItem().setText(0, _translate("VirusTotalIpReportDialog", "URL"))
        self.urlsList.headerItem().setText(1, _translate("VirusTotalIpReportDialog", "Scan Result"))
        self.urlsList.headerItem().setText(2, _translate("VirusTotalIpReportDialog", "Scan Date"))
