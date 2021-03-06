# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\Preferences\ConfigurationPages\NetworkPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NetworkPage(object):
    def setupUi(self, NetworkPage):
        NetworkPage.setObjectName("NetworkPage")
        NetworkPage.resize(589, 1051)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(NetworkPage)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.headerLabel = QtWidgets.QLabel(NetworkPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_7.addWidget(self.headerLabel)
        self.line9_3 = QtWidgets.QFrame(NetworkPage)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line9_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line9_3.setObjectName("line9_3")
        self.verticalLayout_7.addWidget(self.line9_3)
        self.groupBox_2 = QtWidgets.QGroupBox(NetworkPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.downloadDirPicker = E5PathPicker(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downloadDirPicker.sizePolicy().hasHeightForWidth())
        self.downloadDirPicker.setSizePolicy(sizePolicy)
        self.downloadDirPicker.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.downloadDirPicker.setObjectName("downloadDirPicker")
        self.horizontalLayout.addWidget(self.downloadDirPicker)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.requestFilenameCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.requestFilenameCheckBox.setObjectName("requestFilenameCheckBox")
        self.verticalLayout_6.addWidget(self.requestFilenameCheckBox)
        self.cleanupGroup = QtWidgets.QGroupBox(self.groupBox_2)
        self.cleanupGroup.setObjectName("cleanupGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.cleanupGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cleanupNeverButton = QtWidgets.QRadioButton(self.cleanupGroup)
        self.cleanupNeverButton.setObjectName("cleanupNeverButton")
        self.verticalLayout_2.addWidget(self.cleanupNeverButton)
        self.cleanupExitButton = QtWidgets.QRadioButton(self.cleanupGroup)
        self.cleanupExitButton.setObjectName("cleanupExitButton")
        self.verticalLayout_2.addWidget(self.cleanupExitButton)
        self.cleanupSuccessfulButton = QtWidgets.QRadioButton(self.cleanupGroup)
        self.cleanupSuccessfulButton.setObjectName("cleanupSuccessfulButton")
        self.verticalLayout_2.addWidget(self.cleanupSuccessfulButton)
        self.verticalLayout_6.addWidget(self.cleanupGroup)
        self.displayGroup = QtWidgets.QGroupBox(self.groupBox_2)
        self.displayGroup.setObjectName("displayGroup")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.displayGroup)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.openOnStartCheckBox = QtWidgets.QCheckBox(self.displayGroup)
        self.openOnStartCheckBox.setObjectName("openOnStartCheckBox")
        self.verticalLayout_3.addWidget(self.openOnStartCheckBox)
        self.closeOnFinishedCheckBox = QtWidgets.QCheckBox(self.displayGroup)
        self.closeOnFinishedCheckBox.setObjectName("closeOnFinishedCheckBox")
        self.verticalLayout_3.addWidget(self.closeOnFinishedCheckBox)
        self.verticalLayout_6.addWidget(self.displayGroup)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.proxyGroup = QtWidgets.QGroupBox(NetworkPage)
        self.proxyGroup.setCheckable(False)
        self.proxyGroup.setChecked(False)
        self.proxyGroup.setObjectName("proxyGroup")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.proxyGroup)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.noProxyButton = QtWidgets.QRadioButton(self.proxyGroup)
        self.noProxyButton.setChecked(True)
        self.noProxyButton.setObjectName("noProxyButton")
        self.verticalLayout_4.addWidget(self.noProxyButton)
        self.systemProxyButton = QtWidgets.QRadioButton(self.proxyGroup)
        self.systemProxyButton.setObjectName("systemProxyButton")
        self.verticalLayout_4.addWidget(self.systemProxyButton)
        self.manualProxyButton = QtWidgets.QRadioButton(self.proxyGroup)
        self.manualProxyButton.setChecked(False)
        self.manualProxyButton.setObjectName("manualProxyButton")
        self.verticalLayout_4.addWidget(self.manualProxyButton)
        self.groupBox = QtWidgets.QGroupBox(self.proxyGroup)
        self.groupBox.setEnabled(False)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_13 = QtWidgets.QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 0, 0, 1, 1)
        self.httpProxyHostEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.httpProxyHostEdit.setObjectName("httpProxyHostEdit")
        self.gridLayout_2.addWidget(self.httpProxyHostEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_6)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
        self.httpProxyPortSpin = QtWidgets.QSpinBox(self.groupBox_6)
        self.httpProxyPortSpin.setAlignment(QtCore.Qt.AlignRight)
        self.httpProxyPortSpin.setMinimum(1)
        self.httpProxyPortSpin.setMaximum(65535)
        self.httpProxyPortSpin.setProperty("value", 80)
        self.httpProxyPortSpin.setObjectName("httpProxyPortSpin")
        self.gridLayout_2.addWidget(self.httpProxyPortSpin, 0, 3, 1, 1)
        self.httpProxyForAllCheckBox = QtWidgets.QCheckBox(self.groupBox_6)
        self.httpProxyForAllCheckBox.setObjectName("httpProxyForAllCheckBox")
        self.gridLayout_2.addWidget(self.httpProxyForAllCheckBox, 1, 0, 1, 4)
        self.verticalLayout.addWidget(self.groupBox_6)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_12 = QtWidgets.QLabel(self.groupBox_5)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        self.httpsProxyHostEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.httpsProxyHostEdit.setObjectName("httpsProxyHostEdit")
        self.horizontalLayout_2.addWidget(self.httpsProxyHostEdit)
        self.label_5 = QtWidgets.QLabel(self.groupBox_5)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.httpsProxyPortSpin = QtWidgets.QSpinBox(self.groupBox_5)
        self.httpsProxyPortSpin.setAlignment(QtCore.Qt.AlignRight)
        self.httpsProxyPortSpin.setMinimum(1)
        self.httpsProxyPortSpin.setMaximum(65535)
        self.httpsProxyPortSpin.setProperty("value", 443)
        self.httpsProxyPortSpin.setObjectName("httpsProxyPortSpin")
        self.horizontalLayout_2.addWidget(self.httpsProxyPortSpin)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.ftpProxyTypeCombo = QtWidgets.QComboBox(self.groupBox_4)
        self.ftpProxyTypeCombo.setObjectName("ftpProxyTypeCombo")
        self.gridLayout.addWidget(self.ftpProxyTypeCombo, 0, 1, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.ftpProxyHostEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.ftpProxyHostEdit.setObjectName("ftpProxyHostEdit")
        self.gridLayout.addWidget(self.ftpProxyHostEdit, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.ftpProxyPortSpin = QtWidgets.QSpinBox(self.groupBox_4)
        self.ftpProxyPortSpin.setAlignment(QtCore.Qt.AlignRight)
        self.ftpProxyPortSpin.setMinimum(1)
        self.ftpProxyPortSpin.setMaximum(65535)
        self.ftpProxyPortSpin.setProperty("value", 21)
        self.ftpProxyPortSpin.setObjectName("ftpProxyPortSpin")
        self.gridLayout.addWidget(self.ftpProxyPortSpin, 1, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)
        self.ftpProxyUserEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.ftpProxyUserEdit.setObjectName("ftpProxyUserEdit")
        self.gridLayout.addWidget(self.ftpProxyUserEdit, 2, 1, 1, 3)
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.ftpProxyPasswordEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.ftpProxyPasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ftpProxyPasswordEdit.setObjectName("ftpProxyPasswordEdit")
        self.gridLayout.addWidget(self.ftpProxyPasswordEdit, 3, 1, 1, 3)
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.ftpProxyAccountEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.ftpProxyAccountEdit.setObjectName("ftpProxyAccountEdit")
        self.gridLayout.addWidget(self.ftpProxyAccountEdit, 4, 1, 1, 3)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.proxyGroup)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.exceptionsEdit = QtWidgets.QLineEdit(self.proxyGroup)
        self.exceptionsEdit.setObjectName("exceptionsEdit")
        self.horizontalLayout_3.addWidget(self.exceptionsEdit)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.clearProxyPasswordsButton = QtWidgets.QPushButton(self.proxyGroup)
        self.clearProxyPasswordsButton.setObjectName("clearProxyPasswordsButton")
        self.verticalLayout_4.addWidget(self.clearProxyPasswordsButton)
        self.verticalLayout_7.addWidget(self.proxyGroup)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)

        self.retranslateUi(NetworkPage)
        self.manualProxyButton.toggled['bool'].connect(self.groupBox.setEnabled)
        self.httpProxyForAllCheckBox.toggled['bool'].connect(self.groupBox_5.setDisabled)
        self.httpProxyForAllCheckBox.toggled['bool'].connect(self.groupBox_4.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(NetworkPage)
        NetworkPage.setTabOrder(self.downloadDirPicker, self.requestFilenameCheckBox)
        NetworkPage.setTabOrder(self.requestFilenameCheckBox, self.cleanupNeverButton)
        NetworkPage.setTabOrder(self.cleanupNeverButton, self.cleanupExitButton)
        NetworkPage.setTabOrder(self.cleanupExitButton, self.cleanupSuccessfulButton)
        NetworkPage.setTabOrder(self.cleanupSuccessfulButton, self.openOnStartCheckBox)
        NetworkPage.setTabOrder(self.openOnStartCheckBox, self.closeOnFinishedCheckBox)
        NetworkPage.setTabOrder(self.closeOnFinishedCheckBox, self.noProxyButton)
        NetworkPage.setTabOrder(self.noProxyButton, self.systemProxyButton)
        NetworkPage.setTabOrder(self.systemProxyButton, self.manualProxyButton)
        NetworkPage.setTabOrder(self.manualProxyButton, self.httpProxyHostEdit)
        NetworkPage.setTabOrder(self.httpProxyHostEdit, self.httpProxyPortSpin)
        NetworkPage.setTabOrder(self.httpProxyPortSpin, self.httpProxyForAllCheckBox)
        NetworkPage.setTabOrder(self.httpProxyForAllCheckBox, self.httpsProxyHostEdit)
        NetworkPage.setTabOrder(self.httpsProxyHostEdit, self.httpsProxyPortSpin)
        NetworkPage.setTabOrder(self.httpsProxyPortSpin, self.ftpProxyTypeCombo)
        NetworkPage.setTabOrder(self.ftpProxyTypeCombo, self.ftpProxyHostEdit)
        NetworkPage.setTabOrder(self.ftpProxyHostEdit, self.ftpProxyPortSpin)
        NetworkPage.setTabOrder(self.ftpProxyPortSpin, self.ftpProxyUserEdit)
        NetworkPage.setTabOrder(self.ftpProxyUserEdit, self.ftpProxyPasswordEdit)
        NetworkPage.setTabOrder(self.ftpProxyPasswordEdit, self.ftpProxyAccountEdit)
        NetworkPage.setTabOrder(self.ftpProxyAccountEdit, self.exceptionsEdit)
        NetworkPage.setTabOrder(self.exceptionsEdit, self.clearProxyPasswordsButton)

    def retranslateUi(self, NetworkPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("NetworkPage", "<b>Configure Network</b>"))
        self.groupBox_2.setTitle(_translate("NetworkPage", "Downloads"))
        self.label_6.setText(_translate("NetworkPage", "Download directory:"))
        self.downloadDirPicker.setToolTip(_translate("NetworkPage", "Enter the download directory (leave empty to use the default location)"))
        self.requestFilenameCheckBox.setToolTip(_translate("NetworkPage", "Select to ask the user for a download filename"))
        self.requestFilenameCheckBox.setText(_translate("NetworkPage", "Request name of downloaded file"))
        self.cleanupGroup.setTitle(_translate("NetworkPage", "Download Manager Cleanup Policy"))
        self.cleanupNeverButton.setToolTip(_translate("NetworkPage", "Select to never cleanup automatically"))
        self.cleanupNeverButton.setText(_translate("NetworkPage", "Never"))
        self.cleanupExitButton.setToolTip(_translate("NetworkPage", "Select to cleanup upon exiting"))
        self.cleanupExitButton.setText(_translate("NetworkPage", "When exiting the application"))
        self.cleanupSuccessfulButton.setToolTip(_translate("NetworkPage", "Select to cleanup after a successful download"))
        self.cleanupSuccessfulButton.setText(_translate("NetworkPage", "When download finished successfully"))
        self.displayGroup.setTitle(_translate("NetworkPage", "Download Manager Display Policy"))
        self.openOnStartCheckBox.setToolTip(_translate("NetworkPage", "Select to open the download manager dialog when starting a download"))
        self.openOnStartCheckBox.setText(_translate("NetworkPage", "Open when starting download"))
        self.closeOnFinishedCheckBox.setToolTip(_translate("NetworkPage", "Select to close the download manager dialog when the last download is finished"))
        self.closeOnFinishedCheckBox.setText(_translate("NetworkPage", "Close when downloads finished"))
        self.proxyGroup.setToolTip(_translate("NetworkPage", "Select to use a web proxy"))
        self.proxyGroup.setTitle(_translate("NetworkPage", "Network Proxy"))
        self.noProxyButton.setToolTip(_translate("NetworkPage", "Select to not use a network proxy"))
        self.noProxyButton.setText(_translate("NetworkPage", "Do not use proxy"))
        self.systemProxyButton.setToolTip(_translate("NetworkPage", "Select to use the system proxy configuration"))
        self.systemProxyButton.setText(_translate("NetworkPage", "Use system proxy configuration"))
        self.manualProxyButton.setToolTip(_translate("NetworkPage", "Select to use an application specific proxy configuration"))
        self.manualProxyButton.setText(_translate("NetworkPage", "Manual proxy configuration:"))
        self.groupBox.setTitle(_translate("NetworkPage", "Manual proxy settings"))
        self.groupBox_6.setTitle(_translate("NetworkPage", "HTTP-Proxy"))
        self.label_13.setText(_translate("NetworkPage", "Hostname:"))
        self.httpProxyHostEdit.setToolTip(_translate("NetworkPage", "Enter the name of the HTTP proxy host"))
        self.label_2.setText(_translate("NetworkPage", "Port:"))
        self.httpProxyPortSpin.setToolTip(_translate("NetworkPage", "Enter the HTTP proxy port"))
        self.httpProxyForAllCheckBox.setToolTip(_translate("NetworkPage", "Select to use the HTTP proxy for all"))
        self.httpProxyForAllCheckBox.setText(_translate("NetworkPage", "Use this proxy for all protocols"))
        self.groupBox_5.setTitle(_translate("NetworkPage", "HTTPS-Proxy"))
        self.label_12.setText(_translate("NetworkPage", "Hostname:"))
        self.httpsProxyHostEdit.setToolTip(_translate("NetworkPage", "Enter the name of the HTTPS proxy host"))
        self.label_5.setText(_translate("NetworkPage", "Port:"))
        self.httpsProxyPortSpin.setToolTip(_translate("NetworkPage", "Enter the HTTPS proxy port"))
        self.groupBox_4.setTitle(_translate("NetworkPage", "FTP-Proxy"))
        self.label_8.setText(_translate("NetworkPage", "Proxy Type:"))
        self.ftpProxyTypeCombo.setToolTip(_translate("NetworkPage", "Select the type of the FTP proxy"))
        self.label_3.setText(_translate("NetworkPage", "Hostname:"))
        self.ftpProxyHostEdit.setToolTip(_translate("NetworkPage", "Enter the name of the FTP proxy host"))
        self.label_7.setText(_translate("NetworkPage", "Port:"))
        self.ftpProxyPortSpin.setToolTip(_translate("NetworkPage", "Enter the FTP proxy port"))
        self.label_9.setText(_translate("NetworkPage", "User Name:"))
        self.ftpProxyUserEdit.setToolTip(_translate("NetworkPage", "Enter the user name for the proxy authentication"))
        self.label_10.setText(_translate("NetworkPage", "Password:"))
        self.ftpProxyPasswordEdit.setToolTip(_translate("NetworkPage", "Enter the password for the proxy authentication"))
        self.label_11.setText(_translate("NetworkPage", "Account:"))
        self.ftpProxyAccountEdit.setToolTip(_translate("NetworkPage", "Enter the account info for the proxy authentication"))
        self.label.setText(_translate("NetworkPage", "Exceptions:"))
        self.exceptionsEdit.setToolTip(_translate("NetworkPage", "Enter host names or IP-addresses for which the proxy is to be circumvented separated by \',\' (wildcards * or ? may be used)"))
        self.clearProxyPasswordsButton.setToolTip(_translate("NetworkPage", "Press to clear the saved passwords for the Http(s) proxy"))
        self.clearProxyPasswordsButton.setText(_translate("NetworkPage", "Clear HTTP(S) Proxy Passwords"))
from E5Gui.E5PathPicker import E5PathPicker
