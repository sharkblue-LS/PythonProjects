# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the label to show some SSL info (if available).
"""

from PyQt5.QtCore import Qt

from E5Gui.E5ClickableLabel import E5ClickableLabel


class SslLabel(E5ClickableLabel):
    """
    Class implementing the label to show some SSL info (if available).
    """
    okStyle = "QLabel { color : white; background-color : green; }"
    nokStyle = "QLabel { color : white; background-color : red; }"
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(SslLabel, self).__init__(parent)
        
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    def setValidity(self, valid):
        """
        Public method to set the validity indication.
        
        @param valid flag indicating the certificate validity (boolean)
        """
        if valid:
            self.setStyleSheet(SslLabel.okStyle)
        else:
            self.setStyleSheet(SslLabel.nokStyle)
