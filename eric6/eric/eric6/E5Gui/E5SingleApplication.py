# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the single application server and client.
"""

import os

from E5Gui.E5Application import e5App

from Toolbox.SingleApplication import (
    SingleApplicationClient, SingleApplicationServer
)

import Utilities

###########################################################################
## define some module global stuff
###########################################################################

SAFile = "eric6"

# define the protocol tokens
SAOpenFile = 'OpenFile'
SAOpenProject = 'OpenProject'
SAOpenMultiProject = 'OpenMultiProject'
SAArguments = 'Arguments'


class E5SingleApplicationServer(SingleApplicationServer):
    """
    Class implementing the single application server embedded within the IDE.
    """
    def __init__(self):
        """
        Constructor
        """
        SingleApplicationServer.__init__(self, SAFile)

    def handleCommand(self, command, arguments):
        """
        Public slot to handle the command sent by the client.
        
        @param command command sent by the client
        @type str
        @param arguments list of command arguments
        @type list of str
        """
        if command == SAOpenFile:
            self.__saOpenFile(arguments[0])
            return

        if command == SAOpenProject:
            self.__saOpenProject(arguments[0])
            return

        if command == SAOpenMultiProject:
            self.__saOpenMultiProject(arguments[0])
            return

        if command == SAArguments:
            self.__saArguments(arguments[0])
            return

    def __saOpenFile(self, fname):
        """
        Private method used to handle the "Open File" command.
        
        @param fname filename to be opened (string)
        """
        e5App().getObject("ViewManager").openSourceFile(fname)
        
    def __saOpenProject(self, pfname):
        """
        Private method used to handle the "Open Project" command.
        
        @param pfname filename of the project to be opened (string)
        """
        e5App().getObject("Project").openProject(pfname)
        
    def __saOpenMultiProject(self, pfname):
        """
        Private method used to handle the "Open Multi-Project" command.
        
        @param pfname filename of the multi project to be opened (string)
        """
        e5App().getObject("MultiProject").openMultiProject(pfname)
        
    def __saArguments(self, argsStr):
        """
        Private method used to handle the "Arguments" command.
        
        @param argsStr space delimited list of command args(string)
        """
        e5App().getObject("DebugUI").setArgvHistory(argsStr)


class E5SingleApplicationClient(SingleApplicationClient):
    """
    Class implementing the single application client of the IDE.
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
        
        # holds space delimited list of command args, if any
        argsStr = None
        # flag indicating '--' options was found
        ddseen = False
        
        if Utilities.isWindowsPlatform():
            argChars = ['-', '/']
        else:
            argChars = ['-']
        
        for arg in args:
            if arg == '--' and not ddseen:
                ddseen = True
                continue
                
            if arg[0] in argChars or ddseen:
                if argsStr is None:
                    argsStr = arg
                else:
                    argsStr = "{0} {1}".format(argsStr, arg)
                continue
            
            ext = os.path.splitext(arg)[1]
            ext = os.path.normcase(ext)
            
            if ext in ('.epj', '.e4p'):
                self.__openProject(arg)
            elif ext in ('.emj', '.e4m', '.e5m'):
                self.__openMultiProject(arg)
            else:
                self.__openFile(arg)
        
        # send any args we had
        if argsStr is not None:
            self.__sendArguments(argsStr)
        
        self.disconnect()
        
    def __openFile(self, fname):
        """
        Private method to open a file in the application server.
        
        @param fname name of file to be opened (string)
        """
        self.sendCommand(SAOpenFile, [os.path.abspath(fname)])
        
    def __openProject(self, pfname):
        """
        Private method to open a project in the application server.
        
        @param pfname name of the projectfile to be opened (string)
        """
        self.sendCommand(SAOpenProject, [os.path.abspath(pfname)])
        
    def __openMultiProject(self, pfname):
        """
        Private method to open a project in the application server.
        
        @param pfname name of the projectfile to be opened (string)
        """
        self.sendCommand(SAOpenMultiProject, [os.path.abspath(pfname)])
        
    def __sendArguments(self, argsStr):
        """
        Private method to set the command arguments in the application server.
        
        @param argsStr space delimited list of command args (string)
        """
        self.sendCommand(SAArguments, [argsStr])
