# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\VirusTotal\VirusTotalDomainReportDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VirusTotalDomainReportDialog(object):
    def setupUi(self, VirusTotalDomainReportDialog):
        VirusTotalDomainReportDialog.setObjectName("VirusTotalDomainReportDialog")
        VirusTotalDomainReportDialog.resize(900, 700)
        VirusTotalDomainReportDialog.setSizeGripEnabled(True)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(VirusTotalDomainReportDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.headerPixmap = QtWidgets.QLabel(VirusTotalDomainReportDialog)
        self.headerPixmap.setObjectName("headerPixmap")
        self.horizontalLayout_4.addWidget(self.headerPixmap)
        self.headerLabel = QtWidgets.QLabel(VirusTotalDomainReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerLabel.sizePolicy().hasHeightForWidth())
        self.headerLabel.setSizePolicy(sizePolicy)
        self.headerLabel.setObjectName("headerLabel")
        self.horizontalLayout_4.addWidget(self.headerLabel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.line9_3 = QtWidgets.QFrame(VirusTotalDomainReportDialog)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setObjectName("line9_3")
        self.verticalLayout_4.addWidget(self.line9_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(VirusTotalDomainReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setText("BitDefender:")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.bdLabel = QtWidgets.QLabel(self.groupBox)
        self.bdLabel.setText("")
        self.bdLabel.setObjectName("bdLabel")
        self.gridLayout.addWidget(self.bdLabel, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setText("TrendMicro:")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.tmLabel = QtWidgets.QLabel(self.groupBox)
        self.tmLabel.setText("")
        self.tmLabel.setObjectName("tmLabel")
        self.gridLayout.addWidget(self.tmLabel, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setText("Websense ThreatSeeker:")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.wtsLabel = QtWidgets.QLabel(self.groupBox)
        self.wtsLabel.setText("")
        self.wtsLabel.setObjectName("wtsLabel")
        self.gridLayout.addWidget(self.wtsLabel, 2, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(690, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.whoisButton = QtWidgets.QPushButton(VirusTotalDomainReportDialog)
        self.whoisButton.setObjectName("whoisButton")
        self.horizontalLayout_3.addWidget(self.whoisButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.resolutionsGroup = QtWidgets.QGroupBox(VirusTotalDomainReportDialog)
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
        self.horizontalLayout_2.addWidget(self.resolutionsGroup)
        self.subdomainsGroup = QtWidgets.QGroupBox(VirusTotalDomainReportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.subdomainsGroup.sizePolicy().hasHeightForWidth())
        self.subdomainsGroup.setSizePolicy(sizePolicy)
        self.subdomainsGroup.setObjectName("subdomainsGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.subdomainsGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.subdomainsList = QtWidgets.QListWidget(self.subdomainsGroup)
        self.subdomainsList.setAlternatingRowColors(True)
        self.subdomainsList.setObjectName("subdomainsList")
        self.verticalLayout.addWidget(self.subdomainsList)
        self.horizontalLayout_2.addWidget(self.subdomainsGroup)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.detectedUrlsGroup = QtWidgets.QGroupBox(VirusTotalDomainReportDialog)
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
        self.verticalLayout_4.addWidget(self.detectedUrlsGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(VirusTotalDomainReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.retranslateUi(VirusTotalDomainReportDialog)
        self.buttonBox.accepted.connect(VirusTotalDomainReportDialog.accept)
        self.buttonBox.rejected.connect(VirusTotalDomainReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VirusTotalDomainReportDialog)
        VirusTotalDomainReportDialog.setTabOrder(self.whoisButton, self.resolutionsList)
        VirusTotalDomainReportDialog.setTabOrder(self.resolutionsList, self.subdomainsList)
        VirusTotalDomainReportDialog.setTabOrder(self.subdomainsList, self.urlsList)

    def retranslateUi(self, VirusTotalDomainReportDialog):
        _translate = QtCore.QCoreApplication.translate
        VirusTotalDomainReportDialog.setWindowTitle(_translate("VirusTotalDomainReportDialog", "Domain Report"))
        self.groupBox.setTitle(_translate("VirusTotalDomainReportDialog", "Categorizations"))
        self.whoisButton.setText(_translate("VirusTotalDomainReportDialog", "Whois"))
        self.resolutionsGroup.setTitle(_translate("VirusTotalDomainReportDialog", "Resolutions"))
        self.resolutionsList.setSortingEnabled(True)
        self.resolutionsList.headerItem().setText(0, _translate("VirusTotalDomainReportDialog", "IP-Address"))
        self.resolutionsList.headerItem().setText(1, _translate("VirusTotalDomainReportDialog", "Resolved Date"))
        self.subdomainsGroup.setTitle(_translate("VirusTotalDomainReportDialog", "Subdomains"))
        self.subdomainsList.setSortingEnabled(True)
        self.detectedUrlsGroup.setTitle(_translate("VirusTotalDomainReportDialog", "Detected URLs"))
        self.urlsList.setSortingEnabled(True)
        self.urlsList.headerItem().setText(0, _translate("VirusTotalDomainReportDialog", "URL"))
        self.urlsList.headerItem().setText(1, _translate("VirusTotalDomainReportDialog", "Scan Result"))
        self.urlsList.headerItem().setText(2, _translate("VirusTotalDomainReportDialog", "Scan Date"))
