# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the pip packages management widget.
"""

import textwrap
import os
import html.parser

from PyQt5.QtCore import pyqtSlot, Qt, QUrl, QUrlQuery
from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest
from PyQt5.QtWidgets import (
    QWidget, QToolButton, QApplication, QHeaderView, QTreeWidgetItem,
    QMenu, QDialog
)

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox
from E5Gui.E5OverrideCursor import E5OverrideCursor

from .Ui_PipPackagesWidget import Ui_PipPackagesWidget

import UI.PixmapCache
import Globals
import Preferences


class PypiSearchResultsParser(html.parser.HTMLParser):
    """
    Class implementing the parser for the PyPI search result page.
    """
    ClassPrefix = "package-snippet__"
    
    def __init__(self, data):
        """
        Constructor
        
        @param data data to be parsed
        @type str
        """
        super(PypiSearchResultsParser, self).__init__()
        self.__results = []
        self.__activeClass = None
        self.feed(data)
    
    def __getClass(self, attrs):
        """
        Private method to extract the class attribute out of the list of
        attributes.
        
        @param attrs list of tag attributes as (name, value) tuples
        @type list of tuple of (str, str)
        @return value of the 'class' attribute or None
        @rtype str
        """
        for name, value in attrs:
            if name == "class":
                return value
        
        return None
    
    def __getDate(self, attrs):
        """
        Private method to extract the datetime attribute out of the list of
        attributes and process it.
        
        @param attrs list of tag attributes as (name, value) tuples
        @type list of tuple of (str, str)
        @return value of the 'class' attribute or None
        @rtype str
        """
        for name, value in attrs:
            if name == "datetime":
                return value.split("T")[0]
        
        return None
    
    def handle_starttag(self, tag, attrs):
        """
        Public method to process the start tag.
        
        @param tag tag name (all lowercase)
        @type str
        @param attrs list of tag attributes as (name, value) tuples
        @type list of tuple of (str, str)
        """
        if tag == "a" and self.__getClass(attrs) == "package-snippet":
            self.__results.append({})
        
        if tag in ("span", "p"):
            tagClass = self.__getClass(attrs)
            if tagClass in (
                "package-snippet__name", "package-snippet__description",
                "package-snippet__version", "package-snippet__released",
            ):
                self.__activeClass = tagClass
            else:
                self.__activeClass = None
        elif tag == "time":
            attributeName = self.__activeClass.replace(self.ClassPrefix, "")
            self.__results[-1][attributeName] = self.__getDate(attrs)
            self.__activeClass = None
        else:
            self.__activeClass = None
    
    def handle_data(self, data):
        """
        Public method process arbitrary data.
        
        @param data data to be processed
        @type str
        """
        if self.__activeClass is not None:
            attributeName = self.__activeClass.replace(self.ClassPrefix, "")
            self.__results[-1][attributeName] = data
    
    def handle_endtag(self, tag):
        """
        Public method to process the end tag.
        
        @param tag tag name (all lowercase)
        @type str
        """
        self.__activeClass = None
    
    def getResults(self):
        """
        Public method to get the extracted search results.
        
        @return extracted result data
        @rtype list of dict
        """
        return self.__results


class PipPackagesWidget(QWidget, Ui_PipPackagesWidget):
    """
    Class implementing the pip packages management widget.
    """
    ShowProcessGeneralMode = 0
    ShowProcessClassifiersMode = 1
    ShowProcessEntryPointsMode = 2
    ShowProcessFilesListMode = 3
    
    SearchVersionRole = Qt.ItemDataRole.UserRole + 1
    
    def __init__(self, pip, parent=None):
        """
        Constructor
        
        @param pip reference to the global pip interface
        @type Pip
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PipPackagesWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.pipMenuButton.setObjectName(
            "pip_supermenu_button")
        self.pipMenuButton.setIcon(UI.PixmapCache.getIcon("superMenu"))
        self.pipMenuButton.setToolTip(self.tr("pip Menu"))
        self.pipMenuButton.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup)
        self.pipMenuButton.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.pipMenuButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pipMenuButton.setAutoRaise(True)
        self.pipMenuButton.setShowMenuInside(True)
        
        self.refreshButton.setIcon(UI.PixmapCache.getIcon("reload"))
        self.upgradeButton.setIcon(UI.PixmapCache.getIcon("1uparrow"))
        self.upgradeAllButton.setIcon(UI.PixmapCache.getIcon("2uparrow"))
        self.uninstallButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.showPackageDetailsButton.setIcon(UI.PixmapCache.getIcon("info"))
        self.searchToggleButton.setIcon(UI.PixmapCache.getIcon("find"))
        self.searchButton.setIcon(UI.PixmapCache.getIcon("findNext"))
        self.installButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.installUserSiteButton.setIcon(UI.PixmapCache.getIcon("addUser"))
        self.showDetailsButton.setIcon(UI.PixmapCache.getIcon("info"))
        
        self.__pip = pip
        
        self.packagesList.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder)
        
        self.__infoLabels = {
            "name": self.tr("Name:"),
            "version": self.tr("Version:"),
            "location": self.tr("Location:"),
            "requires": self.tr("Requires:"),
            "summary": self.tr("Summary:"),
            "home-page": self.tr("Homepage:"),
            "author": self.tr("Author:"),
            "author-email": self.tr("Author Email:"),
            "license": self.tr("License:"),
            "metadata-version": self.tr("Metadata Version:"),
            "installer": self.tr("Installer:"),
            "classifiers": self.tr("Classifiers:"),
            "entry-points": self.tr("Entry Points:"),
            "files": self.tr("Files:"),
        }
        self.infoWidget.setHeaderLabels(["Key", "Value"])
        
        venvManager = e5App().getObject("VirtualEnvManager")
        venvManager.virtualEnvironmentAdded.connect(
            self.on_refreshButton_clicked)
        venvManager.virtualEnvironmentRemoved.connect(
            self.on_refreshButton_clicked)
        
        project = e5App().getObject("Project")
        project.projectOpened.connect(
            self.on_refreshButton_clicked)
        project.projectClosed.connect(
            self.on_refreshButton_clicked)
        
        self.__initPipMenu()
        self.__populateEnvironments()
        self.__updateActionButtons()
        
        self.statusLabel.hide()
        self.searchWidget.hide()
        
        self.__queryName = []
        self.__querySummary = []
        
        self.__replies = []
        
        self.__packageDetailsDialog = None
    
    def __populateEnvironments(self):
        """
        Private method to get a list of environments and populate the selector.
        """
        self.environmentsComboBox.addItem("")
        projectVenv = self.__pip.getProjectEnvironmentString()
        if projectVenv:
            self.environmentsComboBox.addItem(projectVenv)
        self.environmentsComboBox.addItems(
            self.__pip.getVirtualenvNames(
                noRemote=True,
                noConda=Preferences.getPip("ExcludeCondaEnvironments")
            )
        )
    
    def __isPipAvailable(self):
        """
        Private method to check, if the pip package is available for the
        selected environment.
        
        @return flag indicating availability
        @rtype bool
        """
        available = False
        
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            available = (
                len(self.packagesList.findItems(
                    "pip",
                    Qt.MatchFlag.MatchExactly |
                    Qt.MatchFlag.MatchCaseSensitive)) == 1
            )
        
        return available
    
    def __availablePipVersion(self):
        """
        Private method to get the pip version of the selected environment.
        
        @return tuple containing the version number or tuple with all zeros
            in case pip is not available
        @rtype tuple of int
        """
        pipVersionTuple = (0, 0, 0)
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            pipList = self.packagesList.findItems(
                "pip",
                Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchCaseSensitive
            )
            if len(pipList) > 0:
                pipVersionTuple = Globals.versionToTuple(pipList[0].text(1))
        
        return pipVersionTuple
    
    def getPip(self):
        """
        Public method to get a reference to the pip interface object.
        
        @return reference to the pip interface object
        @rtype Pip
        """
        return self.__pip
    
    #######################################################################
    ## Slots handling widget signals below
    #######################################################################
    
    def __selectedUpdateableItems(self):
        """
        Private method to get a list of selected items that can be updated.
        
        @return list of selected items that can be updated
        @rtype list of QTreeWidgetItem
        """
        return [
            itm for itm in self.packagesList.selectedItems()
            if bool(itm.text(2))
        ]
    
    def __allUpdateableItems(self):
        """
        Private method to get a list of all items that can be updated.
        
        @return list of all items that can be updated
        @rtype list of QTreeWidgetItem
        """
        updateableItems = []
        for index in range(self.packagesList.topLevelItemCount()):
            itm = self.packagesList.topLevelItem(index)
            if itm.text(2):
                updateableItems.append(itm)
        
        return updateableItems
    
    def __updateActionButtons(self):
        """
        Private method to set the state of the action buttons.
        """
        if self.__isPipAvailable():
            self.upgradeButton.setEnabled(
                bool(self.__selectedUpdateableItems()))
            self.uninstallButton.setEnabled(
                bool(self.packagesList.selectedItems()))
            self.upgradeAllButton.setEnabled(
                bool(self.__allUpdateableItems()))
            self.showPackageDetailsButton.setEnabled(
                len(self.packagesList.selectedItems()) == 1)
        else:
            self.upgradeButton.setEnabled(False)
            self.uninstallButton.setEnabled(False)
            self.upgradeAllButton.setEnabled(False)
            self.showPackageDetailsButton.setEnabled(False)
    
    def __refreshPackagesList(self):
        """
        Private method to referesh the packages list.
        """
        self.packagesList.clear()
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            interpreter = self.__pip.getVirtualenvInterpreter(venvName)
            if interpreter:
                self.statusLabel.show()
                self.statusLabel.setText(
                    self.tr("Getting installed packages..."))
                
                with E5OverrideCursor():
                    # 1. populate with installed packages
                    self.packagesList.setUpdatesEnabled(False)
                    installedPackages = self.__pip.getInstalledPackages(
                        venvName,
                        localPackages=self.localCheckBox.isChecked(),
                        notRequired=self.notRequiredCheckBox.isChecked(),
                        usersite=self.userCheckBox.isChecked(),
                    )
                    for package, version in installedPackages:
                        QTreeWidgetItem(self.packagesList, [package, version])
                    self.packagesList.setUpdatesEnabled(True)
                    self.statusLabel.setText(
                        self.tr("Getting outdated packages..."))
                    QApplication.processEvents()
                    
                    # 2. update with update information
                    self.packagesList.setUpdatesEnabled(False)
                    outdatedPackages = self.__pip.getOutdatedPackages(
                        venvName,
                        localPackages=self.localCheckBox.isChecked(),
                        notRequired=self.notRequiredCheckBox.isChecked(),
                        usersite=self.userCheckBox.isChecked(),
                    )
                    for package, _version, latest in outdatedPackages:
                        items = self.packagesList.findItems(
                            package,
                            Qt.MatchFlag.MatchExactly |
                            Qt.MatchFlag.MatchCaseSensitive
                        )
                        if items:
                            itm = items[0]
                            itm.setText(2, latest)
                    
                    self.packagesList.sortItems(0, Qt.SortOrder.AscendingOrder)
                    for col in range(self.packagesList.columnCount()):
                        self.packagesList.resizeColumnToContents(col)
                    self.packagesList.setUpdatesEnabled(True)
                self.statusLabel.hide()
        
        self.__updateActionButtons()
        self.__updateSearchActionButtons()
        self.__updateSearchButton()
    
    @pyqtSlot(int)
    def on_environmentsComboBox_currentIndexChanged(self, index):
        """
        Private slot handling the selection of a Python environment.
        
        @param index index of the selected Python environment
        @type int
        """
        self.__refreshPackagesList()
    
    @pyqtSlot(bool)
    def on_localCheckBox_clicked(self, checked):
        """
        Private slot handling the switching of the local mode.
        
        @param checked state of the local check box
        @type bool
        """
        self.__refreshPackagesList()
    
    @pyqtSlot(bool)
    def on_notRequiredCheckBox_clicked(self, checked):
        """
        Private slot handling the switching of the 'not required' mode.
        
        @param checked state of the 'not required' check box
        @type bool
        """
        self.__refreshPackagesList()
    
    @pyqtSlot(bool)
    def on_userCheckBox_clicked(self, checked):
        """
        Private slot handling the switching of the 'user-site' mode.
        
        @param checked state of the 'user-site' check box
        @type bool
        """
        self.__refreshPackagesList()
    
    @pyqtSlot()
    def on_packagesList_itemSelectionChanged(self):
        """
        Private slot handling the selection of a package.
        """
        self.infoWidget.clear()
        
        if len(self.packagesList.selectedItems()) == 1:
            itm = self.packagesList.selectedItems()[0]
            
            environment = self.environmentsComboBox.currentText()
            interpreter = self.__pip.getVirtualenvInterpreter(environment)
            if not interpreter:
                return
            
            args = ["-m", "pip", "show"]
            if self.verboseCheckBox.isChecked():
                args.append("--verbose")
            if self.installedFilesCheckBox.isChecked():
                args.append("--files")
            args.append(itm.text(0))
            
            with E5OverrideCursor():
                success, output = self.__pip.runProcess(args, interpreter)
                
                if success and output:
                    mode = self.ShowProcessGeneralMode
                    for line in output.splitlines():
                        line = line.rstrip()
                        if line != "---":
                            if mode != self.ShowProcessGeneralMode:
                                if line[0] == " ":
                                    QTreeWidgetItem(
                                        self.infoWidget,
                                        [" ", line.strip()])
                                else:
                                    mode = self.ShowProcessGeneralMode
                            if mode == self.ShowProcessGeneralMode:
                                try:
                                    label, info = line.split(": ", 1)
                                except ValueError:
                                    label = line[:-1]
                                    info = ""
                                label = label.lower()
                                if label in self.__infoLabels:
                                    QTreeWidgetItem(
                                        self.infoWidget,
                                        [self.__infoLabels[label], info])
                                if label == "files":
                                    mode = self.ShowProcessFilesListMode
                                elif label == "classifiers":
                                    mode = self.ShowProcessClassifiersMode
                                elif label == "entry-points":
                                    mode = self.ShowProcessEntryPointsMode
                    self.infoWidget.scrollToTop()
                
                header = self.infoWidget.header()
                header.setStretchLastSection(False)
                header.resizeSections(QHeaderView.ResizeMode.ResizeToContents)
                if (
                    header.sectionSize(0) + header.sectionSize(1) <
                    header.width()
                ):
                    header.setStretchLastSection(True)
        
        self.__updateActionButtons()
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_packagesList_itemActivated(self, item, column):
        """
        Private slot reacting on a package item activation.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column activated column
        @type int
        """
        packageName = item.text(0)
        upgradable = bool(item.text(2))
        if column == 1:
            # show details for installed version
            packageVersion = item.text(1)
        else:
            # show details for available version or installed one
            if item.text(2):
                packageVersion = item.text(2)
            else:
                packageVersion = item.text(1)
        
        self.__showPackageDetails(packageName, packageVersion,
                                  upgradable=upgradable)
    
    @pyqtSlot(bool)
    def on_verboseCheckBox_clicked(self, checked):
        """
        Private slot to handle a change of the verbose package information
        checkbox.
        
        @param checked state of the checkbox
        @type bool
        """
        self.on_packagesList_itemSelectionChanged()
    
    @pyqtSlot(bool)
    def on_installedFilesCheckBox_clicked(self, checked):
        """
        Private slot to handle a change of the installed files information
        checkbox.
        
        @param checked state of the checkbox
        @type bool
        """
        self.on_packagesList_itemSelectionChanged()
    
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """
        Private slot to refresh the display.
        """
        currentEnvironment = self.environmentsComboBox.currentText()
        self.environmentsComboBox.clear()
        self.packagesList.clear()
        
        with E5OverrideCursor():
            self.__populateEnvironments()
            
            index = self.environmentsComboBox.findText(
                currentEnvironment,
                Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchCaseSensitive
            )
            if index != -1:
                self.environmentsComboBox.setCurrentIndex(index)
        
        self.__updateActionButtons()
    
    @pyqtSlot()
    def on_upgradeButton_clicked(self):
        """
        Private slot to upgrade selected packages of the selected environment.
        """
        packages = [itm.text(0) for itm in self.__selectedUpdateableItems()]
        if packages:
            self.executeUpgradePackages(packages)
    
    @pyqtSlot()
    def on_upgradeAllButton_clicked(self):
        """
        Private slot to upgrade all packages of the selected environment.
        """
        packages = [itm.text(0) for itm in self.__allUpdateableItems()]
        if packages:
            self.executeUpgradePackages(packages)
    
    @pyqtSlot()
    def on_uninstallButton_clicked(self):
        """
        Private slot to remove selected packages of the selected environment.
        """
        packages = [itm.text(0) for itm in self.packagesList.selectedItems()]
        self.executeUninstallPackages(packages)
    
    def executeUninstallPackages(self, packages):
        """
        Public method to uninstall the given list of packages.
        
        @param packages list of package names to be uninstalled
        @type list of str
        """
        if packages:
            ok = self.__pip.uninstallPackages(
                packages,
                venvName=self.environmentsComboBox.currentText())
            if ok:
                self.on_refreshButton_clicked()
    
    def executeUpgradePackages(self, packages):
        """
        Public method to execute the pip upgrade command.
        
        @param packages list of package names to be upgraded
        @type list of str
        """
        ok = self.__pip.upgradePackages(
            packages, venvName=self.environmentsComboBox.currentText(),
            userSite=self.userCheckBox.isChecked())
        if ok:
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def on_showPackageDetailsButton_clicked(self):
        """
        Private slot to show information for the selected package.
        """
        item = self.packagesList.selectedItems()[0]
        if item:
            packageName = item.text(0)
            upgradable = bool(item.text(2))
            # show details for available version or installed one
            if item.text(2):
                packageVersion = item.text(2)
            else:
                packageVersion = item.text(1)
            
            self.__showPackageDetails(packageName, packageVersion,
                                      upgradable=upgradable)
    
    #######################################################################
    ## Search widget related methods below
    #######################################################################
    
    def __updateSearchActionButtons(self):
        """
        Private method to update the action button states of the search widget.
        """
        installEnable = (
            len(self.searchResultList.selectedItems()) > 0 and
            self.environmentsComboBox.currentIndex() > 0 and
            self.__isPipAvailable()
        )
        self.installButton.setEnabled(installEnable)
        self.installUserSiteButton.setEnabled(installEnable)
        
        self.showDetailsButton.setEnabled(
            len(self.searchResultList.selectedItems()) == 1 and
            self.__isPipAvailable()
        )
    
    def __updateSearchButton(self):
        """
        Private method to update the state of the search button.
        """
        self.searchButton.setEnabled(
            bool(self.searchEditName.text()) and
            self.__isPipAvailable()
        )
    
    @pyqtSlot(bool)
    def on_searchToggleButton_toggled(self, checked):
        """
        Private slot to togle the search widget.
        
        @param checked state of the search widget button
        @type bool
        """
        self.searchWidget.setVisible(checked)
        
        if checked:
            self.searchEditName.setFocus(Qt.FocusReason.OtherFocusReason)
            self.searchEditName.selectAll()
            
            self.__updateSearchActionButtons()
            self.__updateSearchButton()
    
    @pyqtSlot(str)
    def on_searchEditName_textChanged(self, txt):
        """
        Private slot handling a change of the search term.
        
        @param txt search term
        @type str
        """
        self.__updateSearchButton()
    
    @pyqtSlot()
    def on_searchEditName_returnPressed(self):
        """
        Private slot initiating a search via a press of the Return key.
        """
        if (
            bool(self.searchEditName.text()) and
            self.__isPipAvailable()
        ):
            self.__search()
    
    @pyqtSlot()
    def on_searchButton_clicked(self):
        """
        Private slot handling a press of the search button.
        """
        self.__search()
    
    @pyqtSlot()
    def on_searchResultList_itemSelectionChanged(self):
        """
        Private slot handling changes of the search result selection.
        """
        self.__updateSearchActionButtons()
    
    def __search(self):
        """
        Private method to perform the search by calling the PyPI search URL.
        """
        self.searchResultList.clear()
        self.searchInfoLabel.clear()
        
        self.searchButton.setEnabled(False)
        
        searchTerm = self.searchEditName.text().strip()
        searchTerm = bytes(QUrl.toPercentEncoding(searchTerm)).decode()
        urlQuery = QUrlQuery()
        urlQuery.addQueryItem("q", searchTerm)
        url = QUrl(self.__pip.getIndexUrlSearch())
        url.setQuery(urlQuery)
        
        request = QNetworkRequest(QUrl(url))
        request.setAttribute(
            QNetworkRequest.Attribute.CacheLoadControlAttribute,
            QNetworkRequest.CacheLoadControl.AlwaysNetwork)
        reply = self.__pip.getNetworkAccessManager().get(request)
        reply.finished.connect(
            lambda: self.__searchResponse(reply))
        self.__replies.append(reply)
    
    def __searchResponse(self, reply):
        """
        Private method to extract the search result data from the response.
        
        @param reply reference to the reply object containing the data
        @type QNetworkReply
        """
        if reply in self.__replies:
            self.__replies.remove(reply)
        
        urlQuery = QUrlQuery(reply.url())
        searchTerm = urlQuery.queryItemValue("q")
        
        if reply.error() != QNetworkReply.NetworkError.NoError:
            E5MessageBox.warning(
                None,
                self.tr("Search PyPI"),
                self.tr(
                    "<p>Received an error while searching for <b>{0}</b>.</p>"
                    "<p>Error: {1}</p>"
                ).format(searchTerm, reply.errorString())
            )
            reply.deleteLater()
            return
        
        data = bytes(reply.readAll()).decode()
        reply.deleteLater()
        
        results = PypiSearchResultsParser(data).getResults()
        if results:
            if len(results) < 20:
                msg = self.tr("%n package(s) found.", "", len(results))
            else:
                msg = self.tr("Showing first 20 packages found.")
            self.searchInfoLabel.setText(msg)
        else:
            E5MessageBox.warning(
                self,
                self.tr("Search PyPI"),
                self.tr("""<p>There were no results for <b>{0}</b>.</p>"""))
            self.searchInfoLabel.setText(
                self.tr("""<p>There were no results for <b>{0}</b>.</p>"""))
        
        wrapper = textwrap.TextWrapper(width=80)
        for result in results:
            try:
                description = "\n".join([
                    wrapper.fill(line) for line in
                    result['description'].strip().splitlines()
                ])
            except KeyError:
                description = ""
            itm = QTreeWidgetItem(
                self.searchResultList, [
                    result['name'].strip(),
                    result['version'],
                    result["released"].strip(),
                    description,
                ])
            itm.setData(0, self.SearchVersionRole, result['version'])
        
        header = self.searchResultList.header()
        header.setStretchLastSection(False)
        header.resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        headerSize = 0
        for col in range(header.count()):
            headerSize += header.sectionSize(col)
        if headerSize < header.width():
            header.setStretchLastSection(True)
        
        self.__finishSearch()
    
    def __finishSearch(self):
        """
        Private slot performing the search finishing actions.
        """
        self.__updateSearchActionButtons()
        self.__updateSearchButton()
        
        self.searchEditName.setFocus(Qt.FocusReason.OtherFocusReason)
    
    @pyqtSlot()
    def on_installButton_clicked(self):
        """
        Private slot to handle pressing the Install button..
        """
        packages = [
            itm.text(0).strip()
            for itm in self.searchResultList.selectedItems()
        ]
        self.executeInstallPackages(packages)
    
    @pyqtSlot()
    def on_installUserSiteButton_clicked(self):
        """
        Private slot to handle pressing the Install to User-Site button..
        """
        packages = [
            itm.text(0).strip()
            for itm in self.searchResultList.selectedItems()
        ]
        self.executeInstallPackages(packages, userSite=True)
    
    def executeInstallPackages(self, packages, userSite=False):
        """
        Public method to install the given list of packages.
        
        @param packages list of package names to be installed
        @type list of str
        @param userSite flag indicating to install to the user directory
        @type bool
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName and packages:
            self.__pip.installPackages(packages, venvName=venvName,
                                       userSite=userSite)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def on_showDetailsButton_clicked(self):
        """
        Private slot to handle pressing the Show Details button.
        """
        self.__showSearchedDetails()
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_searchResultList_itemActivated(self, item, column):
        """
        Private slot reacting on an search result item activation.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column activated column
        @type int
        """
        self.__showSearchedDetails(item)
    
    def __showSearchedDetails(self, item=None):
        """
        Private slot to show details about the selected search result package.
        
        @param item reference to the search result item to show details for
        @type QTreeWidgetItem
        """
        self.showDetailsButton.setEnabled(False)
        
        if not item:
            item = self.searchResultList.selectedItems()[0]
        
        packageVersion = item.data(0, self.SearchVersionRole)
        packageName = item.text(0)
        
        self.__showPackageDetails(packageName, packageVersion,
                                  installable=True)
    
    def __showPackageDetails(self, packageName, packageVersion,
                             upgradable=False, installable=False):
        """
        Private method to populate the package details dialog.
        
        @param packageName name of the package to show details for
        @type str
        @param packageVersion version of the package
        @type str
        @param upgradable flag indicating that the package may be upgraded
            (defaults to False)
        @type bool (optional)
        @param installable flag indicating that the package may be installed
            (defaults to False)
        @type bool (optional)
        """
        with E5OverrideCursor():
            packageData = self.__pip.getPackageDetails(
                packageName, packageVersion)
        
        if packageData:
            from .PipPackageDetailsDialog import PipPackageDetailsDialog
            
            self.showDetailsButton.setEnabled(True)
            
            if installable:
                buttonsMode = PipPackageDetailsDialog.ButtonInstall
            elif upgradable:
                buttonsMode = (
                    PipPackageDetailsDialog.ButtonRemove |
                    PipPackageDetailsDialog.ButtonUpgrade
                )
            else:
                buttonsMode = PipPackageDetailsDialog.ButtonRemove
            
            if self.__packageDetailsDialog is not None:
                self.__packageDetailsDialog.close()
            
            self.__packageDetailsDialog = (
                PipPackageDetailsDialog(packageData, buttonsMode=buttonsMode,
                                        parent=self)
            )
            self.__packageDetailsDialog.show()
        else:
            E5MessageBox.warning(
                self,
                self.tr("Search PyPI"),
                self.tr("""<p>No package details info for <b>{0}</b>"""
                        """ available.</p>""").format(packageName))
    
    #######################################################################
    ## Menu related methods below
    #######################################################################
        
    def __initPipMenu(self):
        """
        Private method to create the super menu and attach it to the super
        menu button.
        """
        self.__pipMenu = QMenu()
        self.__installPipAct = self.__pipMenu.addAction(
            self.tr("Install Pip"),
            self.__installPip)
        self.__installPipUserAct = self.__pipMenu.addAction(
            self.tr("Install Pip to User-Site"),
            self.__installPipUser)
        self.__repairPipAct = self.__pipMenu.addAction(
            self.tr("Repair Pip"),
            self.__repairPip)
        self.__pipMenu.addSeparator()
        self.__installPackagesAct = self.__pipMenu.addAction(
            self.tr("Install Packages"),
            self.__installPackages)
        self.__installLocalPackageAct = self.__pipMenu.addAction(
            self.tr("Install Local Package"),
            self.__installLocalPackage)
        self.__pipMenu.addSeparator()
        self.__installRequirementsAct = self.__pipMenu.addAction(
            self.tr("Install Requirements"),
            self.__installRequirements)
        self.__reinstallPackagesAct = self.__pipMenu.addAction(
            self.tr("Re-Install Selected Packages"),
            self.__reinstallPackages)
        self.__uninstallRequirementsAct = self.__pipMenu.addAction(
            self.tr("Uninstall Requirements"),
            self.__uninstallRequirements)
        self.__generateRequirementsAct = self.__pipMenu.addAction(
            self.tr("Generate Requirements..."),
            self.__generateRequirements)
        self.__pipMenu.addSeparator()
        self.__cacheInfoAct = self.__pipMenu.addAction(
            self.tr("Show Cache Info..."),
            self.__showCacheInfo)
        self.__cacheShowListAct = self.__pipMenu.addAction(
            self.tr("Show Cached Files..."),
            self.__showCacheList)
        self.__cacheRemoveAct = self.__pipMenu.addAction(
            self.tr("Remove Cached Files..."),
            self.__removeCachedFiles)
        self.__cachePurgeAct = self.__pipMenu.addAction(
            self.tr("Purge Cache..."),
            self.__purgeCache)
        self.__pipMenu.addSeparator()
        # editUserConfigAct
        self.__pipMenu.addAction(
            self.tr("Edit User Configuration..."),
            self.__editUserConfiguration)
        self.__editVirtualenvConfigAct = self.__pipMenu.addAction(
            self.tr("Edit Environment Configuration..."),
            self.__editVirtualenvConfiguration)
        self.__pipMenu.addSeparator()
        # pipConfigAct
        self.__pipMenu.addAction(
            self.tr("Configure..."),
            self.__pipConfigure)

        self.__pipMenu.aboutToShow.connect(self.__aboutToShowPipMenu)
        
        self.pipMenuButton.setMenu(self.__pipMenu)
    
    def __aboutToShowPipMenu(self):
        """
        Private slot to set the action enabled status.
        """
        enable = bool(self.environmentsComboBox.currentText())
        enablePip = self.__isPipAvailable()
        enablePipCache = self.__availablePipVersion() >= (20, 1, 0)
        
        self.__installPipAct.setEnabled(not enablePip)
        self.__installPipUserAct.setEnabled(not enablePip)
        self.__repairPipAct.setEnabled(enablePip)
        
        self.__installPackagesAct.setEnabled(enablePip)
        self.__installLocalPackageAct.setEnabled(enablePip)
        self.__reinstallPackagesAct.setEnabled(enablePip)
        
        self.__installRequirementsAct.setEnabled(enablePip)
        self.__uninstallRequirementsAct.setEnabled(enablePip)
        self.__generateRequirementsAct.setEnabled(enablePip)
        
        self.__cacheInfoAct.setEnabled(enablePipCache)
        self.__cacheShowListAct.setEnabled(enablePipCache)
        self.__cacheRemoveAct.setEnabled(enablePipCache)
        self.__cachePurgeAct.setEnabled(enablePipCache)
        
        self.__editVirtualenvConfigAct.setEnabled(enable)
    
    @pyqtSlot()
    def __installPip(self):
        """
        Private slot to install pip into the selected environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.installPip(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __installPipUser(self):
        """
        Private slot to install pip into the user site for the selected
        environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.installPip(venvName, userSite=True)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __repairPip(self):
        """
        Private slot to repair the pip installation of the selected
        environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.repairPip(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __installPackages(self):
        """
        Private slot to install packages to be given by the user.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            from .PipPackagesInputDialog import PipPackagesInputDialog
            dlg = PipPackagesInputDialog(self, self.tr("Install Packages"))
            if dlg.exec() == QDialog.DialogCode.Accepted:
                packages, user = dlg.getData()
                self.executeInstallPackages(packages, userSite=user)
    
    @pyqtSlot()
    def __installLocalPackage(self):
        """
        Private slot to install a package available on local storage.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            from .PipFileSelectionDialog import PipFileSelectionDialog
            dlg = PipFileSelectionDialog(self, "package")
            if dlg.exec() == QDialog.DialogCode.Accepted:
                package, user = dlg.getData()
                if package and os.path.exists(package):
                    self.executeInstallPackages([package], userSite=user)
    
    @pyqtSlot()
    def __reinstallPackages(self):
        """
        Private slot to force a re-installation of the selected packages.
        """
        packages = [itm.text(0) for itm in self.packagesList.selectedItems()]
        venvName = self.environmentsComboBox.currentText()
        if venvName and packages:
            self.__pip.installPackages(packages, venvName=venvName,
                                       forceReinstall=True)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __installRequirements(self):
        """
        Private slot to install packages as given in a requirements file.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.installRequirements(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __uninstallRequirements(self):
        """
        Private slot to uninstall packages as given in a requirements file.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.uninstallRequirements(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __generateRequirements(self):
        """
        Private slot to generate the contents for a requirements file.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            from .PipFreezeDialog import PipFreezeDialog
            self.__freezeDialog = PipFreezeDialog(self.__pip, self)
            self.__freezeDialog.show()
            self.__freezeDialog.start(venvName)
    
    @pyqtSlot()
    def __editUserConfiguration(self):
        """
        Private slot to edit the user configuration.
        """
        self.__editConfiguration()
    
    @pyqtSlot()
    def __editVirtualenvConfiguration(self):
        """
        Private slot to edit the configuration of the selected environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__editConfiguration(venvName=venvName)
    
    def __editConfiguration(self, venvName=""):
        """
        Private method to edit a configuration.
        
        @param venvName name of the environment to act upon
        @type str
        """
        from QScintilla.MiniEditor import MiniEditor
        if venvName:
            cfgFile = self.__pip.getVirtualenvConfig(venvName)
            if not cfgFile:
                return
        else:
            cfgFile = self.__pip.getUserConfig()
        cfgDir = os.path.dirname(cfgFile)
        if not cfgDir:
            E5MessageBox.critical(
                None,
                self.tr("Edit Configuration"),
                self.tr("""No valid configuration path determined."""
                        """ Aborting"""))
            return
        
        try:
            if not os.path.isdir(cfgDir):
                os.makedirs(cfgDir)
        except OSError:
            E5MessageBox.critical(
                None,
                self.tr("Edit Configuration"),
                self.tr("""No valid configuration path determined."""
                        """ Aborting"""))
            return
        
        if not os.path.exists(cfgFile):
            try:
                with open(cfgFile, "w") as f:
                    f.write("[global]\n")
            except OSError:
                # ignore these
                pass
        
        # check, if the destination is writeable
        if not os.access(cfgFile, os.W_OK):
            E5MessageBox.critical(
                None,
                self.tr("Edit Configuration"),
                self.tr("""No valid configuration path determined."""
                        """ Aborting"""))
            return
        
        self.__editor = MiniEditor(cfgFile, "Properties")
        self.__editor.show()
 
    def __pipConfigure(self):
        """
        Private slot to open the configuration page.
        """
        e5App().getObject("UserInterface").showPreferences("pipPage")
    
    @pyqtSlot()
    def __showCacheInfo(self):
        """
        Private slot to show information about the cache.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.showCacheInfo(venvName)
    
    @pyqtSlot()
    def __showCacheList(self):
        """
        Private slot to show a list of cached files.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.cacheList(venvName)
    
    @pyqtSlot()
    def __removeCachedFiles(self):
        """
        Private slot to remove files from the pip cache.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.cacheRemove(venvName)
    
    @pyqtSlot()
    def __purgeCache(self):
        """
        Private slot to empty the pip cache.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.cachePurge(venvName)
