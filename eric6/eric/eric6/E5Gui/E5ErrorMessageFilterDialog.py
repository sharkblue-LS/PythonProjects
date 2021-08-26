# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to manage the list of messages to be ignored.
"""

from PyQt5.QtWidgets import QDialog

from .Ui_E5ErrorMessageFilterDialog import Ui_E5ErrorMessageFilterDialog


class E5ErrorMessageFilterDialog(QDialog, Ui_E5ErrorMessageFilterDialog):
    """
    Class implementing a dialog to manage the list of messages to be ignored.
    """
    def __init__(self, messageFilters, parent=None):
        """
        Constructor
        
        @param messageFilters list of message filters to be edited
        @type list of str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5ErrorMessageFilterDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.filtersEditWidget.setList(messageFilters)
        self.filtersEditWidget.setListWhatsThis(self.tr(
            "<b>Error Message Filters</b>"
            "<p>This list shows the configured message filters used to"
            " suppress error messages from within Qt.</p>"
            "<p>A default list of message filters is added to this"
            " user list.</p>"
        ))
    
    def getFilters(self):
        """
        Public method to get the list of message filters.
        
        @return error message filters (list of strings)
        """
        return self.filtersEditWidget.getList()
