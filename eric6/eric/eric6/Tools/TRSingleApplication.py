# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the single application server and client.
"""

import os

from PyQt5.QtCore import pyqtSignal

from Toolbox.SingleApplication import (
    SingleApplicationClient, SingleApplicationServer
)

###########################################################################
## define some module global stuff
###########################################################################

SAFile = "eric6_trpreviewer"

# define the protocol tokens
SALoadForm = 'LoadForm'
SALoadTranslation = 'LoadTranslation'


class TRSingleApplicationServer(SingleApplicationServer):
    """
    Class implementing the single application server embedded within the
    Translations Previewer.
    
    @signal loadForm(str) emitted to load a form file
    @signal loadTranslation(str, bool) emitted to load a translation file
    """
    loadForm = pyqtSignal(str)
    loadTranslation = pyqtSignal(str, bool)
    
    def __init__(self, parent):
        """
        Constructor
        
        @param parent parent widget (QWidget)
        """
        SingleApplicationServer.__init__(self, SAFile)
        
        self.parent = parent

    def handleCommand(self, command, arguments):
        """
        Public slot to handle the command sent by the client.
        
        @param command command sent by the client
        @type str
        @param arguments list of command arguments
        @type list of str
        """
        if command == SALoadForm:
            self.__saLoadForm(arguments)

        elif command == SALoadTranslation:
            self.__saLoadTranslation(arguments)

    def __saLoadForm(self, fnames):
        """
        Private method used to handle the "Load Form" command.
        
        @param fnames filenames of the forms to be loaded (list of strings)
        """
        for fname in fnames:
            self.loadForm.emit(fname)
        
    def __saLoadTranslation(self, fnames):
        """
        Private method used to handle the "Load Translation" command.
        
        @param fnames filenames of the translations to be loaded
            (list of strings)
        """
        first = True
        for fname in fnames:
            self.loadTranslation.emit(fname, first)
            first = False


class TRSingleApplicationClient(SingleApplicationClient):
    """
    Class implementing the single application client of the Translations
    Previewer.
    """
    def __init__(self):
        """
        Constructor
        """
        SingleApplicationClient.__init__(self, SAFile)
        
    def processArgs(self, args):
        """
        Public method to process the command line args passed to the UI.
        
        @param args list of files to open
        """
        # no args, return
        if args is None:
            return
        
        uiFiles = []
        qmFiles = []
        
        for arg in args:
            ext = os.path.splitext(arg)[1]
            ext = ext.lower()
            
            if ext == '.ui':
                uiFiles.append(arg)
            elif ext == '.qm':
                qmFiles.append(arg)
        
        self.sendCommand(SALoadForm, uiFiles)
        self.sendCommand(SALoadTranslation, qmFiles)
        
        self.disconnect()
