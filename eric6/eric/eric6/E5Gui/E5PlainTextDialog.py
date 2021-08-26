# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show some plain text.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from .Ui_E5PlainTextDialog import Ui_E5PlainTextDialog


class E5PlainTextDialog(QDialog, Ui_E5PlainTextDialog):
    """
    Class implementing a dialog to show some plain text.
    """
    def __init__(self, title="", text="", parent=None):
        """
        Constructor
        
        @param title title of the window
        @type str
        @param text text to be shown
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5PlainTextDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.copyButton = self.buttonBox.addButton(
            self.tr("Copy to Clipboard"),
            QDialogButtonBox.ButtonRole.ActionRole)
        self.copyButton.clicked.connect(self.on_copyButton_clicked)
        
        self.setWindowTitle(title)
        self.textEdit.setPlainText(text)
    
    @pyqtSlot()
    def on_copyButton_clicked(self):
        """
        Private slot to copy the text to the clipboard.
        """
        txt = self.textEdit.toPlainText()
        cb = QGuiApplication.clipboard()
        cb.setText(txt)
