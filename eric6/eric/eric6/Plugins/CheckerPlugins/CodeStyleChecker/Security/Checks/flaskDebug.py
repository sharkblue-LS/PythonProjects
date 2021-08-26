# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing checks for running a flask application with enabled debug.
"""

#
# This is a modified version of the one found in the bandit package.
#
# Original Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# SPDX-License-Identifier: Apache-2.0
#


def getChecks():
    """
    Public method to get a dictionary with checks handled by this module.
    
    @return dictionary containing checker lists containing checker function and
        list of codes
    @rtype dict
    """
    return {
        "Call": [
            (checkFlaskDebug, ("S201",)),
        ],
    }


def checkFlaskDebug(reportError, context, config):
    """
    Function to check for a flask app being run with debug.
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    if context.isModuleImportedLike('flask'):
        if context.callFunctionNameQual.endswith('.run'):
            if context.checkCallArgValue('debug', 'True'):
                reportError(
                    context.node.lineno - 1,
                    context.node.col_offset,
                    "S201",
                    "L",
                    "M"
                )
