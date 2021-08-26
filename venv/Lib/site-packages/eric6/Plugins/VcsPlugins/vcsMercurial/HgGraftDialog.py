# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for a graft session.
"""

from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_HgGraftDialog import Ui_HgGraftDialog


class HgGraftDialog(QDialog, Ui_HgGraftDialog):
    """
    Class implementing a dialog to enter the data for a graft session.
    """
    def __init__(self, vcs, revs=None, parent=None):
        """
        Constructor
        
        @param vcs reference to the VCS object
        @type Hg
        @param revs list of revisions to show in the revisions pane
        @type list of str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HgGraftDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        
        if revs:
            self.revisionsEdit.setPlainText("\n".join(sorted(revs)))
        
        self.noCommitCheckBox.setEnabled(vcs.version >= (4, 7, 0))
       
        self.__updateOk()
    
    def __updateOk(self):
        """
        Private slot to update the state of the OK button.
        """
        enable = self.revisionsEdit.toPlainText() != ""
        if self.userGroup.isChecked():
            enable = (
                enable and
                (self.currentUserCheckBox.isChecked() or
                 self.userEdit.text() != "")
            )
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enable)
    
    @pyqtSlot()
    def on_revisionsEdit_textChanged(self):
        """
        Private slot to react upon changes of revisions.
        """
        self.__updateOk()
    
    @pyqtSlot(bool)
    def on_userGroup_toggled(self, checked):
        """
        Private slot to handle changes of the user group state.
        
        @param checked flag giving the checked state
        @type bool
        """
        self.__updateOk()
    
    @pyqtSlot(bool)
    def on_currentUserCheckBox_toggled(self, checked):
        """
        Private slot to handle changes of the current user state.
        
        @param checked flag giving the checked state
        @type bool
        """
        self.__updateOk()
    
    @pyqtSlot(str)
    def on_userEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the user name.
        
        @param txt text of the edit (string)
        """
        self.__updateOk()
    
    def getData(self):
        """
        Public method to retrieve the entered data.
        
        @return tuple with list of revisions, a tuple giving a
            flag indicating to set the user, a flag indicating to use the
            current user and the user name, another tuple giving a flag
            indicating to set the date, a flag indicating to use the
            current date and the date, a flag indicating to append graft info
            to the log message, a flag indicating a dry-run and a flag
            indicating to not commit the copied changesets
        @rtype tuple of (list of str, (bool, bool, str), (bool, bool, str),
            bool, bool, bool)
        """
        userData = (
            self.userGroup.isChecked(),
            self.currentUserCheckBox.isChecked(),
            self.userEdit.text(),
        )
        
        dateData = (
            self.dateGroup.isChecked(),
            self.currentDateCheckBox.isChecked(),
            self.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm"),
        )
        
        return (
            self.revisionsEdit.toPlainText().strip().splitlines(),
            userData,
            dateData,
            self.logCheckBox.isChecked(),
            self.dryRunCheckBox.isChecked(),
            self.noCommitCheckBox.isChecked(),
        )
