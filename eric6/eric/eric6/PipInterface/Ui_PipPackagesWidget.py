# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eric\eric6\PipInterface\PipPackagesWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PipPackagesWidget(object):
    def setupUi(self, PipPackagesWidget):
        PipPackagesWidget.setObjectName("PipPackagesWidget")
        PipPackagesWidget.resize(503, 700)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(PipPackagesWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.baseWidget = QtWidgets.QWidget(PipPackagesWidget)
        self.baseWidget.setObjectName("baseWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.baseWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.environmentsComboBox = QtWidgets.QComboBox(self.baseWidget)
        self.environmentsComboBox.setObjectName("environmentsComboBox")
        self.horizontalLayout.addWidget(self.environmentsComboBox)
        self.pipMenuButton = E5ToolButton(self.baseWidget)
        self.pipMenuButton.setObjectName("pipMenuButton")
        self.horizontalLayout.addWidget(self.pipMenuButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.localCheckBox = QtWidgets.QCheckBox(self.baseWidget)
        self.localCheckBox.setChecked(True)
        self.localCheckBox.setObjectName("localCheckBox")
        self.gridLayout_2.addWidget(self.localCheckBox, 0, 0, 1, 1)
        self.notRequiredCheckBox = QtWidgets.QCheckBox(self.baseWidget)
        self.notRequiredCheckBox.setObjectName("notRequiredCheckBox")
        self.gridLayout_2.addWidget(self.notRequiredCheckBox, 0, 1, 1, 1)
        self.userCheckBox = QtWidgets.QCheckBox(self.baseWidget)
        self.userCheckBox.setObjectName("userCheckBox")
        self.gridLayout_2.addWidget(self.userCheckBox, 1, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.statusLabel = QtWidgets.QLabel(self.baseWidget)
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout_4.addWidget(self.statusLabel)
        self.splitter = QtWidgets.QSplitter(self.baseWidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.packagesList = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.packagesList.sizePolicy().hasHeightForWidth())
        self.packagesList.setSizePolicy(sizePolicy)
        self.packagesList.setAlternatingRowColors(True)
        self.packagesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.packagesList.setRootIsDecorated(False)
        self.packagesList.setItemsExpandable(False)
        self.packagesList.setObjectName("packagesList")
        self.packagesList.header().setDefaultSectionSize(150)
        self.widget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verboseCheckBox = QtWidgets.QCheckBox(self.widget)
        self.verboseCheckBox.setObjectName("verboseCheckBox")
        self.horizontalLayout_7.addWidget(self.verboseCheckBox)
        self.installedFilesCheckBox = QtWidgets.QCheckBox(self.widget)
        self.installedFilesCheckBox.setObjectName("installedFilesCheckBox")
        self.horizontalLayout_7.addWidget(self.installedFilesCheckBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.infoWidget = QtWidgets.QTreeWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy)
        self.infoWidget.setAlternatingRowColors(True)
        self.infoWidget.setRootIsDecorated(False)
        self.infoWidget.setItemsExpandable(False)
        self.infoWidget.setAllColumnsShowFocus(True)
        self.infoWidget.setWordWrap(True)
        self.infoWidget.setColumnCount(2)
        self.infoWidget.setObjectName("infoWidget")
        self.infoWidget.headerItem().setText(0, "1")
        self.infoWidget.headerItem().setText(1, "2")
        self.infoWidget.header().setVisible(False)
        self.infoWidget.header().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.infoWidget)
        self.verticalLayout_4.addWidget(self.splitter)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.refreshButton = QtWidgets.QToolButton(self.baseWidget)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_2.addWidget(self.refreshButton)
        self.upgradeButton = QtWidgets.QToolButton(self.baseWidget)
        self.upgradeButton.setObjectName("upgradeButton")
        self.horizontalLayout_2.addWidget(self.upgradeButton)
        self.upgradeAllButton = QtWidgets.QToolButton(self.baseWidget)
        self.upgradeAllButton.setObjectName("upgradeAllButton")
        self.horizontalLayout_2.addWidget(self.upgradeAllButton)
        self.uninstallButton = QtWidgets.QToolButton(self.baseWidget)
        self.uninstallButton.setObjectName("uninstallButton")
        self.horizontalLayout_2.addWidget(self.uninstallButton)
        self.showPackageDetailsButton = QtWidgets.QToolButton(self.baseWidget)
        self.showPackageDetailsButton.setObjectName("showPackageDetailsButton")
        self.horizontalLayout_2.addWidget(self.showPackageDetailsButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.searchToggleButton = QtWidgets.QToolButton(self.baseWidget)
        self.searchToggleButton.setCheckable(True)
        self.searchToggleButton.setObjectName("searchToggleButton")
        self.horizontalLayout_2.addWidget(self.searchToggleButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.baseWidget)
        self.searchWidget = QtWidgets.QWidget(PipPackagesWidget)
        self.searchWidget.setObjectName("searchWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.searchWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.searchButton = QtWidgets.QToolButton(self.searchWidget)
        self.searchButton.setEnabled(False)
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 0, 2, 2, 1)
        self.label = QtWidgets.QLabel(self.searchWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.searchEditName = QtWidgets.QLineEdit(self.searchWidget)
        self.searchEditName.setObjectName("searchEditName")
        self.gridLayout.addWidget(self.searchEditName, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.searchOptionsWidget = QtWidgets.QWidget(self.searchWidget)
        self.searchOptionsWidget.setObjectName("searchOptionsWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.searchOptionsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addWidget(self.searchOptionsWidget)
        self.searchResultList = QtWidgets.QTreeWidget(self.searchWidget)
        self.searchResultList.setAlternatingRowColors(True)
        self.searchResultList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.searchResultList.setRootIsDecorated(False)
        self.searchResultList.setItemsExpandable(False)
        self.searchResultList.setAllColumnsShowFocus(True)
        self.searchResultList.setWordWrap(True)
        self.searchResultList.setObjectName("searchResultList")
        self.verticalLayout_2.addWidget(self.searchResultList)
        self.searchInfoLabel = QtWidgets.QLabel(self.searchWidget)
        self.searchInfoLabel.setObjectName("searchInfoLabel")
        self.verticalLayout_2.addWidget(self.searchInfoLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.installButton = QtWidgets.QToolButton(self.searchWidget)
        self.installButton.setObjectName("installButton")
        self.horizontalLayout_3.addWidget(self.installButton)
        self.installUserSiteButton = QtWidgets.QToolButton(self.searchWidget)
        self.installUserSiteButton.setObjectName("installUserSiteButton")
        self.horizontalLayout_3.addWidget(self.installUserSiteButton)
        self.showDetailsButton = QtWidgets.QToolButton(self.searchWidget)
        self.showDetailsButton.setObjectName("showDetailsButton")
        self.horizontalLayout_3.addWidget(self.showDetailsButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addWidget(self.searchWidget)

        self.retranslateUi(PipPackagesWidget)
        QtCore.QMetaObject.connectSlotsByName(PipPackagesWidget)
        PipPackagesWidget.setTabOrder(self.environmentsComboBox, self.pipMenuButton)
        PipPackagesWidget.setTabOrder(self.pipMenuButton, self.localCheckBox)
        PipPackagesWidget.setTabOrder(self.localCheckBox, self.notRequiredCheckBox)
        PipPackagesWidget.setTabOrder(self.notRequiredCheckBox, self.userCheckBox)
        PipPackagesWidget.setTabOrder(self.userCheckBox, self.packagesList)
        PipPackagesWidget.setTabOrder(self.packagesList, self.verboseCheckBox)
        PipPackagesWidget.setTabOrder(self.verboseCheckBox, self.installedFilesCheckBox)
        PipPackagesWidget.setTabOrder(self.installedFilesCheckBox, self.infoWidget)
        PipPackagesWidget.setTabOrder(self.infoWidget, self.refreshButton)
        PipPackagesWidget.setTabOrder(self.refreshButton, self.upgradeButton)
        PipPackagesWidget.setTabOrder(self.upgradeButton, self.upgradeAllButton)
        PipPackagesWidget.setTabOrder(self.upgradeAllButton, self.uninstallButton)
        PipPackagesWidget.setTabOrder(self.uninstallButton, self.showPackageDetailsButton)
        PipPackagesWidget.setTabOrder(self.showPackageDetailsButton, self.searchToggleButton)
        PipPackagesWidget.setTabOrder(self.searchToggleButton, self.searchEditName)
        PipPackagesWidget.setTabOrder(self.searchEditName, self.searchButton)
        PipPackagesWidget.setTabOrder(self.searchButton, self.searchResultList)
        PipPackagesWidget.setTabOrder(self.searchResultList, self.installButton)
        PipPackagesWidget.setTabOrder(self.installButton, self.installUserSiteButton)
        PipPackagesWidget.setTabOrder(self.installUserSiteButton, self.showDetailsButton)

    def retranslateUi(self, PipPackagesWidget):
        _translate = QtCore.QCoreApplication.translate
        self.localCheckBox.setToolTip(_translate("PipPackagesWidget", "Select to show only locally-installed packages"))
        self.localCheckBox.setText(_translate("PipPackagesWidget", "Local packages only"))
        self.notRequiredCheckBox.setToolTip(_translate("PipPackagesWidget", "Select to list packages that are not dependencies of installed packages"))
        self.notRequiredCheckBox.setText(_translate("PipPackagesWidget", "Not required Packages"))
        self.userCheckBox.setToolTip(_translate("PipPackagesWidget", "Select to show only packages installed to the user-site"))
        self.userCheckBox.setText(_translate("PipPackagesWidget", "User-Site only"))
        self.packagesList.setSortingEnabled(True)
        self.packagesList.headerItem().setText(0, _translate("PipPackagesWidget", "Package"))
        self.packagesList.headerItem().setText(1, _translate("PipPackagesWidget", "Installed Version"))
        self.packagesList.headerItem().setText(2, _translate("PipPackagesWidget", "Available Version"))
        self.verboseCheckBox.setToolTip(_translate("PipPackagesWidget", "Select to show verbose package information"))
        self.verboseCheckBox.setText(_translate("PipPackagesWidget", "Verbose Information"))
        self.installedFilesCheckBox.setToolTip(_translate("PipPackagesWidget", "Select to show information about installed files"))
        self.installedFilesCheckBox.setText(_translate("PipPackagesWidget", "Installed Files"))
        self.refreshButton.setToolTip(_translate("PipPackagesWidget", "Press to refresh the lists"))
        self.upgradeButton.setToolTip(_translate("PipPackagesWidget", "Press to upgrade the selected packages"))
        self.upgradeAllButton.setToolTip(_translate("PipPackagesWidget", "Press to upgrade all listed packages"))
        self.uninstallButton.setToolTip(_translate("PipPackagesWidget", "Press to uninstall the selected package"))
        self.showPackageDetailsButton.setToolTip(_translate("PipPackagesWidget", "Press to show details for the selected entry"))
        self.searchToggleButton.setToolTip(_translate("PipPackagesWidget", "Toggle to show or hide the search window"))
        self.searchButton.setToolTip(_translate("PipPackagesWidget", "Press to start the search"))
        self.label.setText(_translate("PipPackagesWidget", "Package"))
        self.searchEditName.setToolTip(_translate("PipPackagesWidget", "Enter the search term for the package name"))
        self.searchEditName.setPlaceholderText(_translate("PipPackagesWidget", "Enter search term"))
        self.searchResultList.headerItem().setText(0, _translate("PipPackagesWidget", "Package"))
        self.searchResultList.headerItem().setText(1, _translate("PipPackagesWidget", "Version"))
        self.searchResultList.headerItem().setText(2, _translate("PipPackagesWidget", "Released"))
        self.searchResultList.headerItem().setText(3, _translate("PipPackagesWidget", "Description"))
        self.installButton.setToolTip(_translate("PipPackagesWidget", "Press to install the selected package"))
        self.installUserSiteButton.setToolTip(_translate("PipPackagesWidget", "Press to install the selected package to the user site"))
        self.showDetailsButton.setToolTip(_translate("PipPackagesWidget", "Press to show details for the selected entry"))
from E5Gui.E5ToolButton import E5ToolButton
