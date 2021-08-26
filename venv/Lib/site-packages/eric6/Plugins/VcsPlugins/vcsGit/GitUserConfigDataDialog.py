# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter some user data.
"""

from PyQt5.QtWidgets import QDialog

from .Ui_GitUserConfigDataDialog import Ui_GitUserConfigDataDialog


class GitUserConfigDataDialog(QDialog, Ui_GitUserConfigDataDialog):
    """
    Class implementing a dialog to enter some user data.
    """
    def __init__(self, version=(0, 0), parent=None):
        """
        Constructor
        
        @param version Git version info (tuple of two integers)
        @param parent reference to the parent widget (QWidget)
        """
        super(GitUserConfigDataDialog, self).__init__(parent)
        self.setupUi(self)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def getData(self):
        """
        Public method to retrieve the entered data.
        
        @return tuple with user's first name, last name and email address
            (tuple of three strings)
        """
        return (
            self.firstNameEdit.text(),
            self.lastNameEdit.text(),
            self.emailEdit.text(),
        )
