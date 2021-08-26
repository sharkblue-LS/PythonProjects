# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\WebBrowser\Sync\SyncCheckPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SyncCheckPage(object):
    def setupUi(self, SyncCheckPage):
        SyncCheckPage.setObjectName("SyncCheckPage")
        SyncCheckPage.resize(650, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(SyncCheckPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(SyncCheckPage)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.handlerLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.handlerLabel.sizePolicy().hasHeightForWidth())
        self.handlerLabel.setSizePolicy(sizePolicy)
        self.handlerLabel.setText("handler")
        self.handlerLabel.setObjectName("handlerLabel")
        self.gridLayout.addWidget(self.handlerLabel, 0, 1, 1, 1)
        self.infoLabel = QtWidgets.QLabel(self.groupBox)
        self.infoLabel.setText("Host:")
        self.infoLabel.setObjectName("infoLabel")
        self.gridLayout.addWidget(self.infoLabel, 1, 0, 1, 1)
        self.infoDataLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoDataLabel.sizePolicy().hasHeightForWidth())
        self.infoDataLabel.setSizePolicy(sizePolicy)
        self.infoDataLabel.setText("host")
        self.infoDataLabel.setObjectName("infoDataLabel")
        self.gridLayout.addWidget(self.infoDataLabel, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(SyncCheckPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.bookmarkLabel = E5AnimatedLabel(self.groupBox_2)
        self.bookmarkLabel.setObjectName("bookmarkLabel")
        self.gridLayout_2.addWidget(self.bookmarkLabel, 0, 1, 1, 1)
        self.bookmarkMsgLabel = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarkMsgLabel.sizePolicy().hasHeightForWidth())
        self.bookmarkMsgLabel.setSizePolicy(sizePolicy)
        self.bookmarkMsgLabel.setWordWrap(True)
        self.bookmarkMsgLabel.setObjectName("bookmarkMsgLabel")
        self.gridLayout_2.addWidget(self.bookmarkMsgLabel, 0, 2, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.historyLabel = E5AnimatedLabel(self.groupBox_2)
        self.historyLabel.setObjectName("historyLabel")
        self.gridLayout_2.addWidget(self.historyLabel, 1, 1, 1, 1)
        self.historyMsgLabel = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.historyMsgLabel.sizePolicy().hasHeightForWidth())
        self.historyMsgLabel.setSizePolicy(sizePolicy)
        self.historyMsgLabel.setWordWrap(True)
        self.historyMsgLabel.setObjectName("historyMsgLabel")
        self.gridLayout_2.addWidget(self.historyMsgLabel, 1, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.passwordsLabel = E5AnimatedLabel(self.groupBox_2)
        self.passwordsLabel.setObjectName("passwordsLabel")
        self.gridLayout_2.addWidget(self.passwordsLabel, 2, 1, 1, 1)
        self.passwordsMsgLabel = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordsMsgLabel.sizePolicy().hasHeightForWidth())
        self.passwordsMsgLabel.setSizePolicy(sizePolicy)
        self.passwordsMsgLabel.setWordWrap(True)
        self.passwordsMsgLabel.setObjectName("passwordsMsgLabel")
        self.gridLayout_2.addWidget(self.passwordsMsgLabel, 2, 2, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.userAgentsLabel = E5AnimatedLabel(self.groupBox_2)
        self.userAgentsLabel.setObjectName("userAgentsLabel")
        self.gridLayout_2.addWidget(self.userAgentsLabel, 3, 1, 1, 1)
        self.userAgentsMsgLabel = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userAgentsMsgLabel.sizePolicy().hasHeightForWidth())
        self.userAgentsMsgLabel.setSizePolicy(sizePolicy)
        self.userAgentsMsgLabel.setWordWrap(True)
        self.userAgentsMsgLabel.setObjectName("userAgentsMsgLabel")
        self.gridLayout_2.addWidget(self.userAgentsMsgLabel, 3, 2, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.speedDialLabel = E5AnimatedLabel(self.groupBox_2)
        self.speedDialLabel.setObjectName("speedDialLabel")
        self.gridLayout_2.addWidget(self.speedDialLabel, 4, 1, 1, 2)
        self.speedDialMsgLabel = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speedDialMsgLabel.sizePolicy().hasHeightForWidth())
        self.speedDialMsgLabel.setSizePolicy(sizePolicy)
        self.speedDialMsgLabel.setWordWrap(True)
        self.speedDialMsgLabel.setObjectName("speedDialMsgLabel")
        self.gridLayout_2.addWidget(self.speedDialMsgLabel, 4, 3, 1, 1)
        self.syncErrorLabel = QtWidgets.QLabel(self.groupBox_2)
        self.syncErrorLabel.setWordWrap(True)
        self.syncErrorLabel.setObjectName("syncErrorLabel")
        self.gridLayout_2.addWidget(self.syncErrorLabel, 5, 0, 1, 4)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 81, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(SyncCheckPage)
        QtCore.QMetaObject.connectSlotsByName(SyncCheckPage)

    def retranslateUi(self, SyncCheckPage):
        _translate = QtCore.QCoreApplication.translate
        SyncCheckPage.setTitle(_translate("SyncCheckPage", "Synchronization status"))
        SyncCheckPage.setSubTitle(_translate("SyncCheckPage", "This page shows the status of the current synchronization process."))
        self.groupBox.setTitle(_translate("SyncCheckPage", "Synchronization Data"))
        self.label.setText(_translate("SyncCheckPage", "Sync Handler:"))
        self.groupBox_2.setTitle(_translate("SyncCheckPage", "Synchronization Status"))
        self.label_3.setText(_translate("SyncCheckPage", "Bookmarks:"))
        self.label_4.setText(_translate("SyncCheckPage", "History:"))
        self.label_5.setText(_translate("SyncCheckPage", "Passwords:"))
        self.label_6.setText(_translate("SyncCheckPage", "User Agent Settings:"))
        self.label_7.setText(_translate("SyncCheckPage", "Speed Dial Settings:"))
from E5Gui.E5AnimatedLabel import E5AnimatedLabel
