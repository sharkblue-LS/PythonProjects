# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\Download\DownloadItem.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DownloadItem(object):
    def setupUi(self, DownloadItem):
        DownloadItem.setObjectName("DownloadItem")
        DownloadItem.resize(397, 93)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DownloadItem.sizePolicy().hasHeightForWidth())
        DownloadItem.setSizePolicy(sizePolicy)
        DownloadItem.setWindowTitle("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(DownloadItem)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileIcon = QtWidgets.QLabel(DownloadItem)
        self.fileIcon.setObjectName("fileIcon")
        self.horizontalLayout.addWidget(self.fileIcon)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.datetimeLabel = QtWidgets.QLabel(DownloadItem)
        self.datetimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.datetimeLabel.setWordWrap(True)
        self.datetimeLabel.setObjectName("datetimeLabel")
        self.verticalLayout.addWidget(self.datetimeLabel)
        self.filenameLabel = QtWidgets.QLabel(DownloadItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filenameLabel.sizePolicy().hasHeightForWidth())
        self.filenameLabel.setSizePolicy(sizePolicy)
        self.filenameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.filenameLabel.setWordWrap(True)
        self.filenameLabel.setObjectName("filenameLabel")
        self.verticalLayout.addWidget(self.filenameLabel)
        self.progressBar = QtWidgets.QProgressBar(DownloadItem)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.infoLabel = QtWidgets.QLabel(DownloadItem)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setText("Info")
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setObjectName("infoLabel")
        self.verticalLayout.addWidget(self.infoLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.pauseButton = QtWidgets.QToolButton(DownloadItem)
        self.pauseButton.setText("")
        self.pauseButton.setCheckable(True)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout.addWidget(self.pauseButton)
        self.stopButton = QtWidgets.QToolButton(DownloadItem)
        self.stopButton.setText("")
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.openButton = QtWidgets.QToolButton(DownloadItem)
        self.openButton.setText("")
        self.openButton.setObjectName("openButton")
        self.horizontalLayout.addWidget(self.openButton)

        self.retranslateUi(DownloadItem)
        QtCore.QMetaObject.connectSlotsByName(DownloadItem)
        DownloadItem.setTabOrder(self.pauseButton, self.stopButton)
        DownloadItem.setTabOrder(self.stopButton, self.openButton)

    def retranslateUi(self, DownloadItem):
        _translate = QtCore.QCoreApplication.translate
        self.fileIcon.setText(_translate("DownloadItem", "Icon"))
        self.datetimeLabel.setText(_translate("DownloadItem", "Date and Time"))
        self.filenameLabel.setText(_translate("DownloadItem", "Filename"))
        self.pauseButton.setToolTip(_translate("DownloadItem", "Press to pause the download"))
        self.stopButton.setToolTip(_translate("DownloadItem", "Press to cancel the download"))
        self.openButton.setToolTip(_translate("DownloadItem", "Press to open the downloaded file"))
