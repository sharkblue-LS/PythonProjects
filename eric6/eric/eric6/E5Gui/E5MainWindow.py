# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a main window class with styling support.
"""

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QStyleFactory, QApplication

from .E5Application import e5App
from . import E5MessageBox


class E5MainWindow(QMainWindow):
    """
    Class implementing a main window with styling support.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(E5MainWindow, self).__init__(parent)
        
        self.defaultStyleName = QApplication.style().objectName()
    
    def setStyle(self, styleName, styleSheetFile):
        """
        Public method to set the style of the interface.
        
        @param styleName name of the style to set (string)
        @param styleSheetFile name of a style sheet file to read to overwrite
            defaults of the given style (string)
        """
        # step 1: set the style
        style = None
        if styleName != "System" and styleName in QStyleFactory.keys():
            style = QStyleFactory.create(styleName)
        if style is None:
            style = QStyleFactory.create(self.defaultStyleName)
        if style is not None:
            QApplication.setStyle(style)
        
        # step 2: set a style sheet
        if styleSheetFile:
            try:
                with open(styleSheetFile, "r", encoding="utf-8") as f:
                    styleSheet = f.read()
            except OSError as msg:
                E5MessageBox.warning(
                    self,
                    QCoreApplication.translate(
                        "E5MainWindow", "Loading Style Sheet"),
                    QCoreApplication.translate(
                        "E5MainWindow",
                        """<p>The Qt Style Sheet file <b>{0}</b> could"""
                        """ not be read.<br>Reason: {1}</p>""")
                    .format(styleSheetFile, str(msg)))
                return
        else:
            styleSheet = ""
        
        e5App().setStyleSheet(styleSheet)
