# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Debugger General configuration page.
"""

import re
import socket

from PyQt5.QtCore import pyqtSlot, Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QLineEdit, QInputDialog
from PyQt5.QtNetwork import QNetworkInterface, QAbstractSocket, QHostAddress

from E5Gui.E5Application import e5App
from E5Gui.E5Completers import E5FileCompleter, E5DirCompleter
from E5Gui import E5MessageBox

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_DebuggerGeneralPage import Ui_DebuggerGeneralPage

import Preferences
import Utilities


class DebuggerGeneralPage(ConfigurationPageBase, Ui_DebuggerGeneralPage):
    """
    Class implementing the Debugger General configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super(DebuggerGeneralPage, self).__init__()
        self.setupUi(self)
        self.setObjectName("DebuggerGeneralPage")
        
        t = self.execLineEdit.whatsThis()
        if t:
            t += Utilities.getPercentReplacementHelp()
            self.execLineEdit.setWhatsThis(t)
        
        try:
            backends = e5App().getObject("DebugServer").getSupportedLanguages()
            for backend in sorted(backends):
                self.passiveDbgBackendCombo.addItem(backend)
        except KeyError:
            self.passiveDbgGroup.setEnabled(False)
        
        t = self.consoleDbgEdit.whatsThis()
        if t:
            t += Utilities.getPercentReplacementHelp()
            self.consoleDbgEdit.setWhatsThis(t)
        
        self.consoleDbgCompleter = E5FileCompleter(self.consoleDbgEdit)
        self.dbgTranslationLocalCompleter = E5DirCompleter(
            self.dbgTranslationLocalEdit)
        
        # set initial values
        interfaces = []
        networkInterfaces = QNetworkInterface.allInterfaces()
        for networkInterface in networkInterfaces:
            addressEntries = networkInterface.addressEntries()
            if len(addressEntries) > 0:
                for addressEntry in addressEntries:
                    if (
                        ":" in addressEntry.ip().toString() and
                        not socket.has_ipv6
                    ):
                        continue    # IPv6 not supported by Python
                    interfaces.append(
                        "{0} ({1})".format(
                            networkInterface.humanReadableName(),
                            addressEntry.ip().toString()))
        self.interfacesCombo.addItems(interfaces)
        interface = Preferences.getDebugger("NetworkInterface")
        if not socket.has_ipv6:
            # IPv6 not supported by Python
            self.all6InterfacesButton.setEnabled(False)
            if interface == "allv6":
                interface = "all"
        if interface == "all":
            self.allInterfacesButton.setChecked(True)
        elif interface == "allv6":
            self.all6InterfacesButton.setChecked(True)
        else:
            self.selectedInterfaceButton.setChecked(True)
            index = -1
            for i in range(len(interfaces)):
                if (
                    re.fullmatch(".*{0}.*".format(interface), interfaces[i])
                ):
                    index = i
                    break
            self.interfacesCombo.setCurrentIndex(index)
        
        self.allowedHostsList.addItems(
            Preferences.getDebugger("AllowedHosts"))
        
        self.remoteDebuggerGroup.setChecked(
            Preferences.getDebugger("RemoteDbgEnabled"))
        self.hostLineEdit.setText(
            Preferences.getDebugger("RemoteHost"))
        self.execLineEdit.setText(
            Preferences.getDebugger("RemoteExecution"))
        
        if self.passiveDbgGroup.isEnabled():
            self.passiveDbgCheckBox.setChecked(
                Preferences.getDebugger("PassiveDbgEnabled"))
            self.passiveDbgPortSpinBox.setValue(
                Preferences.getDebugger("PassiveDbgPort"))
            index = self.passiveDbgBackendCombo.findText(
                Preferences.getDebugger("PassiveDbgType"))
            if index == -1:
                index = 0
            self.passiveDbgBackendCombo.setCurrentIndex(index)
        
        self.debugEnvironReplaceCheckBox.setChecked(
            Preferences.getDebugger("DebugEnvironmentReplace"))
        self.debugEnvironEdit.setText(
            Preferences.getDebugger("DebugEnvironment"))
        self.automaticResetCheckBox.setChecked(
            Preferences.getDebugger("AutomaticReset"))
        self.debugAutoSaveScriptsCheckBox.setChecked(
            Preferences.getDebugger("Autosave"))
        self.consoleDebuggerGroup.setChecked(
            Preferences.getDebugger("ConsoleDbgEnabled"))
        self.consoleDbgEdit.setText(
            Preferences.getDebugger("ConsoleDbgCommand"))
        self.dbgPathTranslationGroup.setChecked(
            Preferences.getDebugger("PathTranslation"))
        self.dbgTranslationRemoteEdit.setText(
            Preferences.getDebugger("PathTranslationRemote"))
        self.dbgTranslationLocalEdit.setText(
            Preferences.getDebugger("PathTranslationLocal"))
        self.multiprocessCheckBox.setChecked(
            Preferences.getDebugger("MultiProcessEnabled"))
        self.debugThreeStateBreakPoint.setChecked(
            Preferences.getDebugger("ThreeStateBreakPoints"))
        self.recentFilesSpinBox.setValue(
            Preferences.getDebugger("RecentNumber"))
        self.exceptionBreakCheckBox.setChecked(
            Preferences.getDebugger("BreakAlways"))
        self.exceptionShellCheckBox.setChecked(
            Preferences.getDebugger("ShowExceptionInShell"))
        self.maxSizeSpinBox.setValue(
            Preferences.getDebugger("MaxVariableSize"))
        # Set the colours for debug viewer backgrounds
        self.previewMdl = PreviewModel()
        self.preView.setModel(self.previewMdl)
        self.colourChanged.connect(self.previewMdl.setColor)
        self.initColour("BgColorNew", self.backgroundNewButton,
                        Preferences.getDebugger, hasAlpha=True)
        self.initColour("BgColorChanged", self.backgroundChangedButton,
                        Preferences.getDebugger, hasAlpha=True)
        
        self.autoViewSourcecodeCheckBox.setChecked(
            Preferences.getDebugger("AutoViewSourceCode"))
    
    def save(self):
        """
        Public slot to save the Debugger General (1) configuration.
        """
        Preferences.setDebugger(
            "RemoteDbgEnabled",
            self.remoteDebuggerGroup.isChecked())
        Preferences.setDebugger(
            "RemoteHost",
            self.hostLineEdit.text())
        Preferences.setDebugger(
            "RemoteExecution",
            self.execLineEdit.text())
        
        Preferences.setDebugger(
            "PassiveDbgEnabled",
            self.passiveDbgCheckBox.isChecked())
        Preferences.setDebugger(
            "PassiveDbgPort",
            self.passiveDbgPortSpinBox.value())
        Preferences.setDebugger(
            "PassiveDbgType",
            self.passiveDbgBackendCombo.currentText())
        
        if self.allInterfacesButton.isChecked():
            Preferences.setDebugger("NetworkInterface", "all")
        elif self.all6InterfacesButton.isChecked():
            Preferences.setDebugger("NetworkInterface", "allv6")
        else:
            interface = self.interfacesCombo.currentText()
            interface = interface.split("(")[1].split(")")[0]
            if not interface:
                Preferences.setDebugger("NetworkInterface", "all")
            else:
                Preferences.setDebugger("NetworkInterface", interface)
        
        allowedHosts = []
        for row in range(self.allowedHostsList.count()):
            allowedHosts.append(self.allowedHostsList.item(row).text())
        Preferences.setDebugger("AllowedHosts", allowedHosts)
        
        Preferences.setDebugger(
            "DebugEnvironmentReplace",
            self.debugEnvironReplaceCheckBox.isChecked())
        Preferences.setDebugger(
            "DebugEnvironment",
            self.debugEnvironEdit.text())
        Preferences.setDebugger(
            "AutomaticReset",
            self.automaticResetCheckBox.isChecked())
        Preferences.setDebugger(
            "Autosave",
            self.debugAutoSaveScriptsCheckBox.isChecked())
        Preferences.setDebugger(
            "ConsoleDbgEnabled",
            self.consoleDebuggerGroup.isChecked())
        Preferences.setDebugger(
            "ConsoleDbgCommand",
            self.consoleDbgEdit.text())
        Preferences.setDebugger(
            "PathTranslation",
            self.dbgPathTranslationGroup.isChecked())
        Preferences.setDebugger(
            "PathTranslationRemote",
            self.dbgTranslationRemoteEdit.text())
        Preferences.setDebugger(
            "PathTranslationLocal",
            self.dbgTranslationLocalEdit.text())
        Preferences.setDebugger(
            "MultiProcessEnabled",
            self.multiprocessCheckBox.isChecked())
        Preferences.setDebugger(
            "ThreeStateBreakPoints",
            self.debugThreeStateBreakPoint.isChecked())
        Preferences.setDebugger(
            "RecentNumber",
            self.recentFilesSpinBox.value())
        Preferences.setDebugger(
            "BreakAlways",
            self.exceptionBreakCheckBox.isChecked())
        Preferences.setDebugger(
            "ShowExceptionInShell",
            self.exceptionShellCheckBox.isChecked())
        Preferences.setDebugger(
            "MaxVariableSize",
            self.maxSizeSpinBox.value())
        # Store background colors for debug viewer
        self.saveColours(Preferences.setDebugger)
        
        Preferences.setDebugger(
            "AutoViewSourceCode",
            self.autoViewSourcecodeCheckBox.isChecked())
        
    def on_allowedHostsList_currentItemChanged(self, current, previous):
        """
        Private method set the state of the edit and delete button.
        
        @param current new current item (QListWidgetItem)
        @param previous previous current item (QListWidgetItem)
        """
        self.editAllowedHostButton.setEnabled(current is not None)
        self.deleteAllowedHostButton.setEnabled(current is not None)
        
    @pyqtSlot()
    def on_addAllowedHostButton_clicked(self):
        """
        Private slot called to add a new allowed host.
        """
        allowedHost, ok = QInputDialog.getText(
            None,
            self.tr("Add allowed host"),
            self.tr("Enter the IP address of an allowed host"),
            QLineEdit.EchoMode.Normal)
        if ok and allowedHost:
            if QHostAddress(allowedHost).protocol() in [
                QAbstractSocket.NetworkLayerProtocol.IPv4Protocol,
                QAbstractSocket.NetworkLayerProtocol.IPv6Protocol
            ]:
                self.allowedHostsList.addItem(allowedHost)
            else:
                E5MessageBox.critical(
                    self,
                    self.tr("Add allowed host"),
                    self.tr(
                        """<p>The entered address <b>{0}</b> is not"""
                        """ a valid IP v4 or IP v6 address."""
                        """ Aborting...</p>""")
                    .format(allowedHost))
        
    @pyqtSlot()
    def on_deleteAllowedHostButton_clicked(self):
        """
        Private slot called to delete an allowed host.
        """
        self.allowedHostsList.takeItem(self.allowedHostsList.currentRow())
        
    @pyqtSlot()
    def on_editAllowedHostButton_clicked(self):
        """
        Private slot called to edit an allowed host.
        """
        allowedHost = self.allowedHostsList.currentItem().text()
        allowedHost, ok = QInputDialog.getText(
            None,
            self.tr("Edit allowed host"),
            self.tr("Enter the IP address of an allowed host"),
            QLineEdit.EchoMode.Normal,
            allowedHost)
        if ok and allowedHost:
            if QHostAddress(allowedHost).protocol() in [
                QAbstractSocket.NetworkLayerProtocol.IPv4Protocol,
                QAbstractSocket.NetworkLayerProtocol.IPv6Protocol
            ]:
                self.allowedHostsList.currentItem().setText(allowedHost)
            else:
                E5MessageBox.critical(
                    self,
                    self.tr("Edit allowed host"),
                    self.tr(
                        """<p>The entered address <b>{0}</b> is not"""
                        """ a valid IP v4 or IP v6 address."""
                        """ Aborting...</p>""")
                    .format(allowedHost))


class PreviewModel(QAbstractItemModel):
    """
    Class to show an example of the selected background colours for the debug
    viewer.
    """
    def __init__(self):
        """
        Constructor
        """
        super(PreviewModel, self).__init__()
        self.bgColorNew = QBrush(QColor('#FFFFFF'))
        self.bgColorChanged = QBrush(QColor('#FFFFFF'))
    
    def setColor(self, key, bgcolour):
        """
        Public slot to update the background colour indexed by key.
        
        @param key the name of background
        @type str
        @param bgcolour the new background colour
        @type QColor
        """
        if key == 'BgColorNew':
            self.bgColorNew = QBrush(bgcolour)
        else:
            self.bgColorChanged = QBrush(bgcolour)
        
        # Force update of preview view
        idxStart = self.index(0, 0, QModelIndex())
        idxEnd = self.index(0, 2, QModelIndex())
        self.dataChanged.emit(idxStart, idxEnd)
    
    def index(self, row, column, parent=QModelIndex()):
        """
        Public Qt slot to get the index of item at row:column of parent.
        
        @param row number of rows
        @type int
        @param column number of columns
        @type int
        @param parent the model parent
        @type QModelIndex
        @return new model index for child
        @rtype QModelIndex
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        return self.createIndex(row, column, None)
    
    def parent(self, child):
        """
        Public Qt slot to get the parent of the given child.
        
        @param child the model child node
        @type QModelIndex
        @return new model index for parent
        @rtype QModelIndex
        """
        return QModelIndex()
    
    def columnCount(self, parent=QModelIndex()):
        """
        Public Qt slot to get the column count.
        
        @param parent the model parent
        @type QModelIndex
        @return number of columns
        @rtype int
        """
        return 1
    
    def rowCount(self, parent=QModelIndex()):
        """
        Public Qt slot to get the row count.
        
        @param parent the model parent
        @type QModelIndex
        @return number of rows
        @rtype int
        """
        return 4
    
    def flags(self, index):
        """
        Public Qt slot to get the item flags.
        
        @param index of item
        @type QModelIndex
        @return item flags
        @rtype QtCore.Qt.ItemFlag
        """
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        Public Qt slot get the role data of item.
        
        @param index the model index
        @type QModelIndex
        @param role the requested data role
        @type QtCore.Qt.ItemDataRole
        @return role data of item
        @rtype str, QBrush or None
        """
        if role == Qt.ItemDataRole.DisplayRole:
            return self.tr("Variable Name")
        elif role == Qt.ItemDataRole.BackgroundRole:
            if index.row() >= 2:
                return self.bgColorChanged
            else:
                return self.bgColorNew
        
        return None


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    return DebuggerGeneralPage()

#
# eflag: noqa = M822
