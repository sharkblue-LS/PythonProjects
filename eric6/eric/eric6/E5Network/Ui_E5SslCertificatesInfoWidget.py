# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\E5Network\E5SslCertificatesInfoWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_E5SslCertificatesInfoWidget(object):
    def setupUi(self, E5SslCertificatesInfoWidget):
        E5SslCertificatesInfoWidget.setObjectName("E5SslCertificatesInfoWidget")
        E5SslCertificatesInfoWidget.resize(500, 455)
        self.verticalLayout = QtWidgets.QVBoxLayout(E5SslCertificatesInfoWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_17 = QtWidgets.QLabel(E5SslCertificatesInfoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.verticalLayout.addWidget(self.label_17)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chainLabel = QtWidgets.QLabel(E5SslCertificatesInfoWidget)
        self.chainLabel.setObjectName("chainLabel")
        self.horizontalLayout.addWidget(self.chainLabel)
        self.chainComboBox = QtWidgets.QComboBox(E5SslCertificatesInfoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chainComboBox.sizePolicy().hasHeightForWidth())
        self.chainComboBox.setSizePolicy(sizePolicy)
        self.chainComboBox.setObjectName("chainComboBox")
        self.horizontalLayout.addWidget(self.chainComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.blacklistedLabel = QtWidgets.QLabel(E5SslCertificatesInfoWidget)
        self.blacklistedLabel.setObjectName("blacklistedLabel")
        self.verticalLayout.addWidget(self.blacklistedLabel)
        self.groupBox = QtWidgets.QGroupBox(E5SslCertificatesInfoWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.subjectCommonNameLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectCommonNameLabel.sizePolicy().hasHeightForWidth())
        self.subjectCommonNameLabel.setSizePolicy(sizePolicy)
        self.subjectCommonNameLabel.setText("")
        self.subjectCommonNameLabel.setObjectName("subjectCommonNameLabel")
        self.gridLayout.addWidget(self.subjectCommonNameLabel, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.subjectOrganizationLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectOrganizationLabel.sizePolicy().hasHeightForWidth())
        self.subjectOrganizationLabel.setSizePolicy(sizePolicy)
        self.subjectOrganizationLabel.setText("")
        self.subjectOrganizationLabel.setObjectName("subjectOrganizationLabel")
        self.gridLayout.addWidget(self.subjectOrganizationLabel, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.subjectOrganizationalUnitLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectOrganizationalUnitLabel.sizePolicy().hasHeightForWidth())
        self.subjectOrganizationalUnitLabel.setSizePolicy(sizePolicy)
        self.subjectOrganizationalUnitLabel.setText("")
        self.subjectOrganizationalUnitLabel.setObjectName("subjectOrganizationalUnitLabel")
        self.gridLayout.addWidget(self.subjectOrganizationalUnitLabel, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.serialNumberLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serialNumberLabel.sizePolicy().hasHeightForWidth())
        self.serialNumberLabel.setSizePolicy(sizePolicy)
        self.serialNumberLabel.setText("")
        self.serialNumberLabel.setObjectName("serialNumberLabel")
        self.gridLayout.addWidget(self.serialNumberLabel, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.issuerCommonNameLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.issuerCommonNameLabel.sizePolicy().hasHeightForWidth())
        self.issuerCommonNameLabel.setSizePolicy(sizePolicy)
        self.issuerCommonNameLabel.setText("")
        self.issuerCommonNameLabel.setObjectName("issuerCommonNameLabel")
        self.gridLayout.addWidget(self.issuerCommonNameLabel, 7, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)
        self.issuerOrganizationLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.issuerOrganizationLabel.sizePolicy().hasHeightForWidth())
        self.issuerOrganizationLabel.setSizePolicy(sizePolicy)
        self.issuerOrganizationLabel.setText("")
        self.issuerOrganizationLabel.setObjectName("issuerOrganizationLabel")
        self.gridLayout.addWidget(self.issuerOrganizationLabel, 8, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 9, 0, 1, 1)
        self.issuerOrganizationalUnitLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.issuerOrganizationalUnitLabel.sizePolicy().hasHeightForWidth())
        self.issuerOrganizationalUnitLabel.setSizePolicy(sizePolicy)
        self.issuerOrganizationalUnitLabel.setText("")
        self.issuerOrganizationalUnitLabel.setObjectName("issuerOrganizationalUnitLabel")
        self.gridLayout.addWidget(self.issuerOrganizationalUnitLabel, 9, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 9, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 11, 0, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 12, 0, 1, 1)
        self.effectiveLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.effectiveLabel.sizePolicy().hasHeightForWidth())
        self.effectiveLabel.setSizePolicy(sizePolicy)
        self.effectiveLabel.setText("")
        self.effectiveLabel.setObjectName("effectiveLabel")
        self.gridLayout.addWidget(self.effectiveLabel, 12, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 13, 0, 1, 1)
        self.expiresLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expiresLabel.sizePolicy().hasHeightForWidth())
        self.expiresLabel.setSizePolicy(sizePolicy)
        self.expiresLabel.setText("")
        self.expiresLabel.setObjectName("expiresLabel")
        self.gridLayout.addWidget(self.expiresLabel, 13, 1, 1, 1)
        self.expiredLabel = QtWidgets.QLabel(self.groupBox)
        self.expiredLabel.setObjectName("expiredLabel")
        self.gridLayout.addWidget(self.expiredLabel, 14, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 15, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 16, 0, 1, 2)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 17, 0, 1, 1)
        self.sha1Label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sha1Label.sizePolicy().hasHeightForWidth())
        self.sha1Label.setSizePolicy(sizePolicy)
        self.sha1Label.setText("")
        self.sha1Label.setObjectName("sha1Label")
        self.gridLayout.addWidget(self.sha1Label, 17, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 18, 0, 1, 1)
        self.md5Label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.md5Label.sizePolicy().hasHeightForWidth())
        self.md5Label.setSizePolicy(sizePolicy)
        self.md5Label.setText("")
        self.md5Label.setObjectName("md5Label")
        self.gridLayout.addWidget(self.md5Label, 18, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(E5SslCertificatesInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(E5SslCertificatesInfoWidget)

    def retranslateUi(self, E5SslCertificatesInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        self.label_17.setText(_translate("E5SslCertificatesInfoWidget", "<h2>Certificate Information</h2>"))
        self.chainLabel.setText(_translate("E5SslCertificatesInfoWidget", "Certificate Chain:"))
        self.blacklistedLabel.setText(_translate("E5SslCertificatesInfoWidget", "This certificated has been blacklisted."))
        self.label.setText(_translate("E5SslCertificatesInfoWidget", "<b>Issued for:</b>"))
        self.label_2.setText(_translate("E5SslCertificatesInfoWidget", "Common Name (CN):"))
        self.label_3.setText(_translate("E5SslCertificatesInfoWidget", "Organization (O):"))
        self.label_4.setText(_translate("E5SslCertificatesInfoWidget", "Organizational Unit (OU):"))
        self.label_5.setText(_translate("E5SslCertificatesInfoWidget", "Serialnumber:"))
        self.label_6.setText(_translate("E5SslCertificatesInfoWidget", "<b>Issued by:</b>"))
        self.label_9.setText(_translate("E5SslCertificatesInfoWidget", "Common Name (CN):"))
        self.label_8.setText(_translate("E5SslCertificatesInfoWidget", "Organization (O):"))
        self.label_7.setText(_translate("E5SslCertificatesInfoWidget", "Organizational Unit (OU):"))
        self.label_10.setText(_translate("E5SslCertificatesInfoWidget", "<b>Validity:</b>"))
        self.label_11.setText(_translate("E5SslCertificatesInfoWidget", "Issued on:"))
        self.label_12.setText(_translate("E5SslCertificatesInfoWidget", "Expires on:"))
        self.expiredLabel.setText(_translate("E5SslCertificatesInfoWidget", "This certificate is not valid yet or has expired."))
        self.label_13.setText(_translate("E5SslCertificatesInfoWidget", "<b>Fingerprints:</b>"))
        self.label_14.setText(_translate("E5SslCertificatesInfoWidget", "SHA1-Fingerprint:"))
        self.label_15.setText(_translate("E5SslCertificatesInfoWidget", "MD5-Fingerprint:"))
