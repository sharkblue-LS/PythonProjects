# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\PipInterface\PipPackageDetailsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PipPackageDetailsDialog(object):
    def setupUi(self, PipPackageDetailsDialog):
        PipPackageDetailsDialog.setObjectName("PipPackageDetailsDialog")
        PipPackageDetailsDialog.resize(800, 700)
        PipPackageDetailsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(PipPackageDetailsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.packageNameLabel = QtWidgets.QLabel(PipPackageDetailsDialog)
        self.packageNameLabel.setObjectName("packageNameLabel")
        self.verticalLayout.addWidget(self.packageNameLabel)
        self.infoWidget = QtWidgets.QTabWidget(PipPackageDetailsDialog)
        self.infoWidget.setObjectName("infoWidget")
        self.details = QtWidgets.QWidget()
        self.details.setObjectName("details")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.details)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.details)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.details)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.licenseLabel = QtWidgets.QLabel(self.details)
        self.licenseLabel.setObjectName("licenseLabel")
        self.gridLayout_2.addWidget(self.licenseLabel, 4, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.details)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 8, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.details)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.authorLabel = QtWidgets.QLabel(self.details)
        self.authorLabel.setObjectName("authorLabel")
        self.gridLayout_2.addWidget(self.authorLabel, 2, 1, 1, 1)
        self.releaseUrlLabel = QtWidgets.QLabel(self.details)
        self.releaseUrlLabel.setOpenExternalLinks(True)
        self.releaseUrlLabel.setObjectName("releaseUrlLabel")
        self.gridLayout_2.addWidget(self.releaseUrlLabel, 8, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.details)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.details)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.details)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 9, 0, 1, 1)
        self.authorEmailLabel = QtWidgets.QLabel(self.details)
        self.authorEmailLabel.setOpenExternalLinks(True)
        self.authorEmailLabel.setObjectName("authorEmailLabel")
        self.gridLayout_2.addWidget(self.authorEmailLabel, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.details)
        self.label_16.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 10, 0, 1, 1)
        self.homePageLabel = QtWidgets.QLabel(self.details)
        self.homePageLabel.setOpenExternalLinks(True)
        self.homePageLabel.setObjectName("homePageLabel")
        self.gridLayout_2.addWidget(self.homePageLabel, 6, 1, 1, 1)
        self.classifiersList = QtWidgets.QListWidget(self.details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.classifiersList.sizePolicy().hasHeightForWidth())
        self.classifiersList.setSizePolicy(sizePolicy)
        self.classifiersList.setAlternatingRowColors(True)
        self.classifiersList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.classifiersList.setObjectName("classifiersList")
        self.gridLayout_2.addWidget(self.classifiersList, 10, 1, 1, 1)
        self.packageUrlLabel = QtWidgets.QLabel(self.details)
        self.packageUrlLabel.setOpenExternalLinks(True)
        self.packageUrlLabel.setObjectName("packageUrlLabel")
        self.gridLayout_2.addWidget(self.packageUrlLabel, 7, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.details)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 7, 0, 1, 1)
        self.platformLabel = QtWidgets.QLabel(self.details)
        self.platformLabel.setObjectName("platformLabel")
        self.gridLayout_2.addWidget(self.platformLabel, 5, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.details)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.details)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 5, 0, 1, 1)
        self.descriptionEdit = QtWidgets.QPlainTextEdit(self.details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.descriptionEdit.sizePolicy().hasHeightForWidth())
        self.descriptionEdit.setSizePolicy(sizePolicy)
        self.descriptionEdit.setTabChangesFocus(True)
        self.descriptionEdit.setReadOnly(True)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridLayout_2.addWidget(self.descriptionEdit, 1, 1, 1, 1)
        self.summaryLabel = QtWidgets.QLabel(self.details)
        self.summaryLabel.setWordWrap(True)
        self.summaryLabel.setObjectName("summaryLabel")
        self.gridLayout_2.addWidget(self.summaryLabel, 0, 1, 1, 1)
        self.docsUrlLabel = QtWidgets.QLabel(self.details)
        self.docsUrlLabel.setOpenExternalLinks(True)
        self.docsUrlLabel.setObjectName("docsUrlLabel")
        self.gridLayout_2.addWidget(self.docsUrlLabel, 9, 1, 1, 1)
        self.infoWidget.addTab(self.details, "")
        self.urls = QtWidgets.QWidget()
        self.urls.setObjectName("urls")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.urls)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.downloadUrlsList = QtWidgets.QTreeWidget(self.urls)
        self.downloadUrlsList.setAlternatingRowColors(True)
        self.downloadUrlsList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.downloadUrlsList.setRootIsDecorated(False)
        self.downloadUrlsList.setItemsExpandable(False)
        self.downloadUrlsList.setObjectName("downloadUrlsList")
        self.downloadUrlsList.header().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.downloadUrlsList)
        self.infoWidget.addTab(self.urls, "")
        self.requires = QtWidgets.QWidget()
        self.requires.setObjectName("requires")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.requires)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.requires)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_17 = QtWidgets.QLabel(self.groupBox)
        self.label_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 0, 0, 1, 1)
        self.requiredPackagesList = QtWidgets.QListWidget(self.groupBox)
        self.requiredPackagesList.setAlternatingRowColors(True)
        self.requiredPackagesList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.requiredPackagesList.setObjectName("requiredPackagesList")
        self.gridLayout_4.addWidget(self.requiredPackagesList, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox)
        self.label_18.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 1, 0, 1, 1)
        self.requiredDistributionsList = QtWidgets.QListWidget(self.groupBox)
        self.requiredDistributionsList.setAlternatingRowColors(True)
        self.requiredDistributionsList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.requiredDistributionsList.setObjectName("requiredDistributionsList")
        self.gridLayout_4.addWidget(self.requiredDistributionsList, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.requires)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_20 = QtWidgets.QLabel(self.groupBox_2)
        self.label_20.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 0, 0, 1, 1)
        self.providedPackagesList = QtWidgets.QListWidget(self.groupBox_2)
        self.providedPackagesList.setAlternatingRowColors(True)
        self.providedPackagesList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.providedPackagesList.setObjectName("providedPackagesList")
        self.gridLayout_3.addWidget(self.providedPackagesList, 0, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_2)
        self.label_19.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 1, 0, 1, 1)
        self.providedDistributionsList = QtWidgets.QListWidget(self.groupBox_2)
        self.providedDistributionsList.setAlternatingRowColors(True)
        self.providedDistributionsList.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.providedDistributionsList.setObjectName("providedDistributionsList")
        self.gridLayout_3.addWidget(self.providedDistributionsList, 1, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.infoWidget.addTab(self.requires, "")
        self.verticalLayout.addWidget(self.infoWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(PipPackageDetailsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PipPackageDetailsDialog)
        self.infoWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(PipPackageDetailsDialog.accept)
        self.buttonBox.rejected.connect(PipPackageDetailsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PipPackageDetailsDialog)
        PipPackageDetailsDialog.setTabOrder(self.infoWidget, self.descriptionEdit)
        PipPackageDetailsDialog.setTabOrder(self.descriptionEdit, self.classifiersList)
        PipPackageDetailsDialog.setTabOrder(self.classifiersList, self.downloadUrlsList)
        PipPackageDetailsDialog.setTabOrder(self.downloadUrlsList, self.requiredPackagesList)
        PipPackageDetailsDialog.setTabOrder(self.requiredPackagesList, self.requiredDistributionsList)
        PipPackageDetailsDialog.setTabOrder(self.requiredDistributionsList, self.providedPackagesList)
        PipPackageDetailsDialog.setTabOrder(self.providedPackagesList, self.providedDistributionsList)

    def retranslateUi(self, PipPackageDetailsDialog):
        _translate = QtCore.QCoreApplication.translate
        PipPackageDetailsDialog.setWindowTitle(_translate("PipPackageDetailsDialog", "Package Details"))
        self.label_4.setText(_translate("PipPackageDetailsDialog", "Author:"))
        self.label.setText(_translate("PipPackageDetailsDialog", "Summary:"))
        self.label_10.setText(_translate("PipPackageDetailsDialog", "Release URL:"))
        self.label_3.setText(_translate("PipPackageDetailsDialog", "Description:"))
        self.label_8.setText(_translate("PipPackageDetailsDialog", "Home Page:"))
        self.label_6.setText(_translate("PipPackageDetailsDialog", "License:"))
        self.label_11.setText(_translate("PipPackageDetailsDialog", "Documentation URL:"))
        self.label_16.setText(_translate("PipPackageDetailsDialog", "Classifiers:"))
        self.classifiersList.setSortingEnabled(True)
        self.label_9.setText(_translate("PipPackageDetailsDialog", "Package URL:"))
        self.label_5.setText(_translate("PipPackageDetailsDialog", "Author Email:"))
        self.label_7.setText(_translate("PipPackageDetailsDialog", "Platform:"))
        self.infoWidget.setTabText(self.infoWidget.indexOf(self.details), _translate("PipPackageDetailsDialog", "Details"))
        self.infoWidget.setTabToolTip(self.infoWidget.indexOf(self.details), _translate("PipPackageDetailsDialog", "Lists package informations"))
        self.downloadUrlsList.headerItem().setText(0, _translate("PipPackageDetailsDialog", "File"))
        self.downloadUrlsList.headerItem().setText(1, _translate("PipPackageDetailsDialog", "Type"))
        self.downloadUrlsList.headerItem().setText(2, _translate("PipPackageDetailsDialog", "Py Version"))
        self.downloadUrlsList.headerItem().setText(3, _translate("PipPackageDetailsDialog", "Uploaded on"))
        self.downloadUrlsList.headerItem().setText(4, _translate("PipPackageDetailsDialog", "Size"))
        self.infoWidget.setTabText(self.infoWidget.indexOf(self.urls), _translate("PipPackageDetailsDialog", "Download URLs"))
        self.infoWidget.setTabToolTip(self.infoWidget.indexOf(self.urls), _translate("PipPackageDetailsDialog", "Lists the download URLs"))
        self.groupBox.setTitle(_translate("PipPackageDetailsDialog", "Requires"))
        self.label_17.setText(_translate("PipPackageDetailsDialog", "Required Packages:"))
        self.requiredPackagesList.setSortingEnabled(True)
        self.label_18.setText(_translate("PipPackageDetailsDialog", "Required Distributions:"))
        self.requiredDistributionsList.setSortingEnabled(True)
        self.groupBox_2.setTitle(_translate("PipPackageDetailsDialog", "Provides"))
        self.label_20.setText(_translate("PipPackageDetailsDialog", "Provided Packages:"))
        self.providedPackagesList.setSortingEnabled(True)
        self.label_19.setText(_translate("PipPackageDetailsDialog", "Provided Distributions:"))
        self.providedDistributionsList.setSortingEnabled(True)
        self.infoWidget.setTabText(self.infoWidget.indexOf(self.requires), _translate("PipPackageDetailsDialog", "Requires/Provides"))
        self.infoWidget.setTabToolTip(self.infoWidget.indexOf(self.requires), _translate("PipPackageDetailsDialog", "Lists required and provided packages"))
