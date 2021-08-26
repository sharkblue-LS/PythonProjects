# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a check for the use of 'exec'.
"""

#
# This is a modified version of the one found in the bandit package.
#
# Original Copyright 2014 Hewlett-Packard Development Company, L.P.
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
            (checkExecUsed, ("S102",)),
        ],
    }


def checkExecUsed(reportError, context, config):
    """
    Function to check for the use of 'exec'.
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    if context.callFunctionNameQual == 'exec':
        reportError(
            context.node.lineno - 1,
            context.node.col_offset,
            "S102",
            "M",
            "H"
        )
