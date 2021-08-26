# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the variables filter dialog.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem

from Debugger.Config import ConfigVarTypeDispStrings
import Preferences

from .Ui_VariablesFilterDialog import Ui_VariablesFilterDialog


class VariablesFilterDialog(QDialog, Ui_VariablesFilterDialog):
    """
    Class implementing the variables filter dialog.
    
    It opens a dialog window for the configuration of the variables type
    filter to be applied during a debugging session.
    """
    def __init__(self, parent=None, name=None, modal=False):
        """
        Constructor
        
        @param parent parent widget of this dialog (QWidget)
        @param name name of this dialog (string)
        @param modal flag to indicate a modal dialog (boolean)
        """
        super(VariablesFilterDialog, self).__init__(parent)
        if name:
            self.setObjectName(name)
        self.setModal(modal)
        self.setupUi(self)

        self.defaultButton = self.buttonBox.addButton(
            self.tr("Save Default"), QDialogButtonBox.ButtonRole.ActionRole)
        
        #populate the list widgets and set the default selection
        for widget in self.localsList, self.globalsList:
            for varType, varTypeStr in ConfigVarTypeDispStrings.items():
                itm = QListWidgetItem(self.tr(varTypeStr), widget)
                itm.setData(Qt.ItemDataRole.UserRole, varType)
                itm.setFlags(Qt.ItemFlag.ItemIsEnabled |
                             Qt.ItemFlag.ItemIsUserCheckable)
                itm.setCheckState(Qt.CheckState.Unchecked)
                widget.addItem(itm)
        
        lDefaultFilter, gDefaultFilter = Preferences.getVarFilters()
        self.setSelection(lDefaultFilter, gDefaultFilter)

    def getSelection(self):
        """
        Public slot to retrieve the current selections.
        
        @return tuple of lists containing the variable filters. The first list
            is the locals variables filter, the second the globals variables
            filter.
        @rtype tuple of (list of str, list of str)
        """
        lList = []
        for row in range(self.localsList.count()):
            itm = self.localsList.item(row)
            if itm.checkState() == Qt.CheckState.Unchecked:
                lList.append(itm.data(Qt.ItemDataRole.UserRole))
        
        gList = []
        for row in range(self.globalsList.count()):
            itm = self.globalsList.item(row)
            if itm.checkState() == Qt.CheckState.Unchecked:
                gList.append(itm.data(Qt.ItemDataRole.UserRole))
        return (lList, gList)
    
    def setSelection(self, lList, gList):
        """
        Public slot to set the current selection.
        
        @param lList local variables filter
        @type list of str
        @param gList global variables filter
        @type list of str
        """
        for row in range(self.localsList.count()):
            itm = self.localsList.item(row)
            if itm.data(Qt.ItemDataRole.UserRole) in lList:
                itm.setCheckState(Qt.CheckState.Unchecked)
            else:
                itm.setCheckState(Qt.CheckState.Checked)
        
        for row in range(self.globalsList.count()):
            itm = self.globalsList.item(row)
            if itm.data(Qt.ItemDataRole.UserRole) in gList:
                itm.setCheckState(Qt.CheckState.Unchecked)
            else:
                itm.setCheckState(Qt.CheckState.Checked)

    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.defaultButton:
            Preferences.setVarFilters(self.getSelection())
