# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the name-value pair to define a variable
for the IDL compiler.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_IdlCompilerDefineNameDialog import Ui_IdlCompilerDefineNameDialog


class IdlCompilerDefineNameDialog(QDialog, Ui_IdlCompilerDefineNameDialog):
    """
    Class implementing a dialog to enter the name-value pair to define a
    variable for the IDL compiler.
    """
    def __init__(self, name="", value="", parent=None):
        """
        Constructor
        
        @param name name of the variable
        @type str
        @param value value of the variable
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(IdlCompilerDefineNameDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.nameEdit.setText(name)
        self.valueEdit.setText(value)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
        
        self.__updateOkButton()
    
    def __updateOkButton(self):
        """
        Private slot to update the enable state of the OK button.
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(self.nameEdit.text()))
    
    @pyqtSlot(str)
    def on_nameEdit_textChanged(self, txt):
        """
        Private slot to handle changes of the name.
        
        @param txt current text of the name edit
        @type str
        """
        self.__updateOkButton()
    
    def getData(self):
        """
        Public method to get the entered data.
        
        @return tuple containing the variable name and value
        @rtype tuple of (str, str)
        """
        return (
            self.nameEdit.text().strip(),
            self.valueEdit.text().strip(),
        )
