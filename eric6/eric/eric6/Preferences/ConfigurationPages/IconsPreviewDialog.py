# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to preview the contents of an icon directory.
"""

import os.path

from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QListWidgetItem, QDialog

from .Ui_IconsPreviewDialog import Ui_IconsPreviewDialog


class IconsPreviewDialog(QDialog, Ui_IconsPreviewDialog):
    """
    Class implementing a dialog to preview the contents of an icon directory.
    """
    def __init__(self, directories, parent=None):
        """
        Constructor
        
        @param directories list of directories to be shown
        @type list of str
        @param parent parent widget
        @type QWidget
        """
        super(IconsPreviewDialog, self).__init__(parent)
        self.setupUi(self)
        
        palette = self.iconView.palette()
        self.__baseBrush = palette.brush(QPalette.ColorRole.Base)
        self.__textBrush = palette.brush(QPalette.ColorRole.Text)
        self.__inverted = False
        
        self.directoryCombo.addItems(sorted(directories))
    
    @pyqtSlot(str)
    def on_directoryCombo_currentTextChanged(self, dirName):
        """
        Private slot to show the icons of the selected icon directory.
        
        @param dirName selected icon directory
        @type str
        """
        self.iconView.clear()
        directory = QDir(dirName)
        for icon in directory.entryList(["*.svg", "*.svgz", "*.png"]):
            itm = QListWidgetItem(
                QIcon(os.path.join(dirName, icon)),
                icon, self.iconView)
            if self.__inverted:
                itm.setForeground(self.__baseBrush)
            else:
                itm.setForeground(self.__textBrush)
    
    @pyqtSlot(bool)
    def on_invertButton_toggled(self, checked):
        """
        Private slot to show the icons on an inverted background.
        
        @param checked state of the button
        @type bool
        """
        self.__inverted = checked
        
        palette = self.iconView.palette()
        if self.__inverted:
            palette.setBrush(QPalette.ColorRole.Base, self.__textBrush)
            palette.setBrush(QPalette.ColorRole.Text, self.__baseBrush)
        else:
            palette.setBrush(QPalette.ColorRole.Base, self.__baseBrush)
            palette.setBrush(QPalette.ColorRole.Text, self.__textBrush)
        self.iconView.viewport().setPalette(palette)
        
        self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """
        Private slot to refresh the view.
        """
        currentDirectory = self.directoryCombo.currentText()
        self.on_directoryCombo_currentTextChanged(currentDirectory)
