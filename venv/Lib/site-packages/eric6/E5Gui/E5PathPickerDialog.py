# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter a file system path using a file picker.
"""

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

from .E5PathPicker import E5PathPicker, E5PathPickerModes


class E5PathPickerDialog(QDialog):
    """
    Class implementing a dialog to enter a file system path using a file
    picker.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5PathPickerDialog, self).__init__(parent)
        
        self.setMinimumWidth(400)
        
        self.__layout = QVBoxLayout(self)
        
        self.__label = QLabel(self)
        self.__label.setWordWrap(True)
        
        self.__pathPicker = E5PathPicker(self)
        self.__buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Ok, self)
        
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__pathPicker)
        self.__layout.addWidget(self.__buttonBox)
        
        self.__buttonBox.accepted.connect(self.accept)
        self.__buttonBox.rejected.connect(self.reject)
    
    def setLabelText(self, text):
        """
        Public method to set the label text.
        
        @param text label text
        @type str
        """
        self.__label.setText(text)
    
    def setTitle(self, title):
        """
        Public method to set the window title.
        
        @param title window title
        @type str
        """
        self.setWindowTitle(title)
        self.__pathPicker.setWindowTitle(title)
    
    def setPickerMode(self, mode):
        """
        Public method to set the mode of the path picker.
        
        @param mode picker mode
        @type E5PathPickerModes
        """
        self.__pathPicker.setMode(mode)
    
    def setPickerPath(self, path):
        """
        Public method to set the path of the path picker.
        
        @param path path to be set
        @type str
        """
        self.__pathPicker.setPath(path)
    
    def setDefaultDirectory(self, directory):
        """
        Public method to set the default directory of the path picker.
        
        @param directory default directory
        @type str
        """
        self.__pathPicker.setDefaultDirectory(directory)
    
    def setPickerFilters(self, filters):
        """
        Public method to set the filters of the path picker.
        
        Note: Multiple filters must be separated by ';;'.
        
        @param filters string containing the file filters
        @type str
        """
        self.__pathPicker.setFilters(filters)
    
    def getPath(self):
        """
        Public method to get the current path.
        
        @return current path
        @rtype str
        """
        return self.__pathPicker.path()


def getPath(parent, title, label, mode=E5PathPickerModes.OpenFileMode,
            path="", defaultDirectory="", filters=None):
    """
    Function to get a file or directory path from the user.
    
    @param parent reference to the parent widget
    @type QWidget
    @param title title of the dialog
    @type str
    @param label text to be shown above the path picker
    @type str
    @param mode mode of the path picker
    @type E5PathPickerModes
    @param path initial path to be shown
    @type str
    @param defaultDirectory default directory of the path picker selection
        dialog
    @type str
    @param filters list of file filters
    @type list of str
    @return tuple containing the entered path and a flag indicating that the
        user pressed the OK button
    @rtype tuple of (str, bool)
    """
    # step 1: setup of the dialog
    dlg = E5PathPickerDialog(parent)
    if title:
        dlg.setTitle(title)
    if label:
        dlg.setLabelText(label)
    dlg.setPickerMode(mode)
    if path:
        dlg.setPickerPath(path)
    if defaultDirectory:
        dlg.setDefaultDirectory(defaultDirectory)
    if filters is not None and len(filters) > 0:
        dlg.setPickerFilters(";;".join(filters))
    
    # step 2: show the dialog and get the result
    if dlg.exec() == QDialog.DialogCode.Accepted:
        ok = True
        path = dlg.getPath().strip()
    else:
        ok = False
        path = ""
    
    # step 3: return the result
    return path, ok
