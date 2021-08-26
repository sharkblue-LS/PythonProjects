# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a splashscreen for eric.
"""

import os.path
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QSplashScreen

from eric6config import getConfig


class SplashScreen(QSplashScreen):
    """
    Class implementing a splashscreen for eric.
    """
    def __init__(self):
        """
        Constructor
        """
        ericPic = QPixmap(
            os.path.join(getConfig('ericPixDir'), 'ericSplash.png'))
        self.labelAlignment = Qt.Alignment(
            Qt.AlignmentFlag.AlignBottom |
            Qt.AlignmentFlag.AlignRight |
            Qt.AlignmentFlag.AlignAbsolute
        )
        super(SplashScreen, self).__init__(ericPic)
        self.show()
        QApplication.flush()
        
    def showMessage(self, msg):
        """
        Public method to show a message in the bottom part of the splashscreen.
        
        @param msg message to be shown (string)
        """
        logging.debug(msg)
        super(SplashScreen, self).showMessage(
            msg, self.labelAlignment, QColor(Qt.GlobalColor.white))
        QApplication.processEvents()
        
    def clearMessage(self):
        """
        Public method to clear the message shown.
        """
        super(SplashScreen, self).clearMessage()
        QApplication.processEvents()


class NoneSplashScreen(object):
    """
    Class implementing a "None" splashscreen for eric.
    
    This class implements the same interface as the real splashscreen,
    but simply does nothing.
    """
    def __init__(self):
        """
        Constructor
        """
        pass
        
    def showMessage(self, msg):
        """
        Public method to show a message in the bottom part of the splashscreen.
        
        @param msg message to be shown (string)
        """
        logging.debug(msg)
        
    def clearMessage(self):
        """
        Public method to clear the message shown.
        """
        pass
        
    def finish(self, widget):
        """
        Public method to finish the splash screen.
        
        @param widget widget to wait for (QWidget)
        """
        pass
