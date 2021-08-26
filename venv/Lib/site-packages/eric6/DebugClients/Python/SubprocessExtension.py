# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a function to patch subprocess.Popen to support debugging
of the process.
"""

import os
import shlex

from DebugUtilities import isPythonProgram, patchArguments

_debugClient = None


def patchSubprocess(module, debugClient):
    """
    Function to patch the subprocess module.
    
    @param module reference to the imported module to be patched
    @type module
    @param debugClient reference to the debug client object
    @type DebugClient
    """     # __IGNORE_WARNING_D234__
    global _debugClient
    
    class PopenWrapper(module.Popen):
        """
        Wrapper class for subprocess.Popen.
        """
        def __init__(self, arguments, *args, **kwargs):
            """
            Constructor
            
            @param arguments command line arguments for the new process
            @type list of str or str
            @param args constructor arguments of Popen
            @type list
            @param kwargs constructor keyword only arguments of Popen
            @type dict
            """
            if (
                _debugClient.debugging and
                _debugClient.multiprocessSupport and
                isinstance(arguments, (str, list))
            ):
                if isinstance(arguments, str):
                    # convert to arguments list
                    arguments = shlex.split(arguments)
                else:
                    # create a copy of the arguments
                    arguments = arguments[:]
                ok = isPythonProgram(arguments[0])
                if ok:
                    scriptName = os.path.basename(arguments[0])
                    if not _debugClient.skipMultiProcessDebugging(scriptName):
                        arguments = patchArguments(
                            _debugClient, arguments, noRedirect=True
                        )
            
            super(PopenWrapper, self).__init__(arguments, *args, **kwargs)
    
    _debugClient = debugClient
    module.Popen = PopenWrapper
