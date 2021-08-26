# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing checks for blacklisted imports.
"""

#
# This is a modified version of the one found in the bandit package.
#
# Original Copyright 2016 Hewlett-Packard Development Company, L.P.
#
# SPDX-License-Identifier: Apache-2.0
#

_blacklists = {
    "S401": ([
        'telnetlib'],
        "H"),
    "S402": ([
        'ftplib'],
        "H"),
    "S403": ([
        'pickle',
        'cPickle',
        'dill',
        'shelve'],
        "L"),
    "S404": ([
        'subprocess'],
        "L"),
    "S405": ([
        'xml.etree.cElementTree',
        'xml.etree.ElementTree'],
        "L"),
    "S406": ([
        'xml.sax'],
        "L"),
    "S407": ([
        'xml.dom.expatbuilder'],
        "L"),
    "S408": ([
        'xml.dom.minidom'],
        "L"),
    "S409": ([
        'xml.dom.pulldom'],
        "L"),
    "S410": ([
        'lxml'],
        "L"),
    "S411": ([
        'xmlrpclib'],
        "H"),
    "S412": ([
        'wsgiref.handlers.CGIHandler',
        'twisted.web.twcgi.CGIScript',
        'twisted.web.twcgi.CGIDirectory'],
        "H"),
    "S413": ([
        'Crypto.Cipher',
        'Crypto.Hash',
        'Crypto.IO',
        'Crypto.Protocol',
        'Crypto.PublicKey',
        'Crypto.Random',
        'Crypto.Signature',
        'Crypto.Util'],
        "H"),
}


def getChecks():
    """
    Public method to get a dictionary with checks handled by this module.
    
    @return dictionary containing checker lists containing checker function and
        list of codes
    @rtype dict
    """
    return {
        "Import": [
            (checkBlacklist, tuple(_blacklists.keys())),
        ],
        "ImportFrom": [
            (checkBlacklist, tuple(_blacklists.keys())),
        ],
        "Call": [
            (checkBlacklist, tuple(_blacklists.keys())),
        ],
    }


def checkBlacklist(reportError, context, config):
    """
    Function to check for blacklisted method calls.
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    nodeType = context.node.__class__.__name__

    if nodeType.startswith('Import'):
        prefix = ""
        if nodeType == "ImportFrom":
            if context.node.module is not None:
                prefix = context.node.module + "."

        for code in _blacklists:
            qualnames, severity = _blacklists[code]
            for name in context.node.names:
                for qualname in qualnames:
                    if (prefix + name.name).startswith(qualname):
                        reportError(
                            context.node.lineno - 1,
                            context.node.col_offset,
                            code,
                            severity,
                            "H",
                            name.name
                        )
