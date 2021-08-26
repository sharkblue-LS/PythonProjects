# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a check for use of insecure md4, md5, or sha1 hash
functions in hashlib.new().
"""

#
# This is a modified version of the one found in the bandit package.
#
# Original Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# SPDX-License-Identifier: Apache-2.0
#

from Security.SecurityDefaults import SecurityDefaults


def getChecks():
    """
    Public method to get a dictionary with checks handled by this module.
    
    @return dictionary containing checker lists containing checker function and
        list of codes
    @rtype dict
    """
    return {
        "Call": [
            (checkHashlibNew, ("S331",)),
        ],
    }


def checkHashlibNew(reportError, context, config):
    """
    Function to check for use of insecure md4, md5, or sha1 hash functions
    in hashlib.new().
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    if config and "insecure_hashes" in config:
        insecureHashes = [h.lower() for h in config["insecure_hashes"]]
    else:
        insecureHashes = SecurityDefaults["insecure_hashes"]
    
    if isinstance(context.callFunctionNameQual, str):
        qualnameList = context.callFunctionNameQual.split('.')
        func = qualnameList[-1]
        if 'hashlib' in qualnameList and func == 'new':
            args = context.callArgs
            keywords = context.callKeywords
            name = args[0] if args else keywords['name']
            if (
                isinstance(name, str) and
                name.lower() in insecureHashes
            ):
                reportError(
                    context.node.lineno - 1,
                    context.node.col_offset,
                    "S331",
                    "M",
                    "H",
                    name.upper()
                )
