# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the output of the svn proplist command
process.
"""

import os

import pysvn

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QWidget, QHeaderView, QApplication, QDialogButtonBox, QTreeWidgetItem
)

from E5Utilities.E5MutexLocker import E5MutexLocker

from .SvnDialogMixin import SvnDialogMixin
from .Ui_SvnPropListDialog import Ui_SvnPropListDialog


class SvnPropListDialog(QWidget, SvnDialogMixin, Ui_SvnPropListDialog):
    """
    Class implementing a dialog to show the output of the svn proplist command
    process.
    """
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param parent parent widget (QWidget)
        """
        super(SvnPropListDialog, self).__init__(parent)
        self.setupUi(self)
        SvnDialogMixin.__init__(self)
        
        self.refreshButton = self.buttonBox.addButton(
            self.tr("Refresh"), QDialogButtonBox.ButtonRole.ActionRole)
        self.refreshButton.setToolTip(
            self.tr("Press to refresh the properties display"))
        self.refreshButton.setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.vcs = vcs
        
        self.propsList.headerItem().setText(self.propsList.columnCount(), "")
        self.propsList.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder)
        
        self.client = self.vcs.getClient()
        self.client.callback_cancel = self._clientCancelCallback
        self.client.callback_get_login = self._clientLoginCallback
        self.client.callback_ssl_server_trust_prompt = (
            self._clientSslServerTrustPromptCallback
        )
        
    def __resort(self):
        """
        Private method to resort the tree.
        """
        self.propsList.sortItems(
            self.propsList.sortColumn(),
            self.propsList.header().sortIndicatorOrder())
        
    def __resizeColumns(self):
        """
        Private method to resize the list columns.
        """
        self.propsList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.propsList.header().setStretchLastSection(True)
        
    def __generateItem(self, path, propName, propValue):
        """
        Private method to generate a properties item in the properties list.
        
        @param path file/directory name the property applies to (string)
        @param propName name of the property (string)
        @param propValue value of the property (string)
        """
        QTreeWidgetItem(self.propsList, [path, propName, propValue])
        
    def start(self, fn, recursive=False):
        """
        Public slot to start the svn status command.
        
        @param fn filename(s) (string or list of strings)
        @param recursive flag indicating a recursive list is requested
        """
        self.errorGroup.hide()
        
        self.propsList.clear()
        
        self.__args = fn
        self.__recursive = recursive
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        self.refreshButton.setEnabled(False)
        
        QApplication.processEvents()
        self.propsFound = False
        if isinstance(fn, list):
            dname, fnames = self.vcs.splitPathList(fn)
        else:
            dname, fname = self.vcs.splitPath(fn)
            fnames = [fname]
        
        cwd = os.getcwd()
        os.chdir(dname)
        with E5MutexLocker(self.vcs.vcsExecutionMutex):
            try:
                for name in fnames:
                    proplist = self.client.proplist(name, recurse=recursive)
                    counter = 0
                    for path, prop in proplist:
                        for propName, propVal in list(prop.items()):
                            self.__generateItem(path, propName, propVal)
                            self.propsFound = True
                        counter += 1
                        if counter == 30:
                            # check for cancel every 30 items
                            counter = 0
                            if self._clientCancelCallback():
                                break
                    if self._clientCancelCallback():
                        break
            except pysvn.ClientError as e:
                self.__showError(e.args[0])
        
        self.__finish()
        os.chdir(cwd)
        
    def __finish(self):
        """
        Private slot called when the process finished or the user pressed the
        button.
        """
        if not self.propsFound:
            self.__generateItem("", self.tr("None"), "")
        
        self.__resort()
        self.__resizeColumns()
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        
        self.refreshButton.setEnabled(True)
        
        self._cancel()
        
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.__finish()
        elif button == self.refreshButton:
            self.on_refreshButton_clicked()
        
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """
        Private slot to refresh the status display.
        """
        self.start(self.__args, recursive=self.__recursive)
        
    def __showError(self, msg):
        """
        Private slot to show an error message.
        
        @param msg error message to show (string)
        """
        self.errorGroup.show()
        self.errors.insertPlainText(msg)
        self.errors.ensureCursorVisible()
