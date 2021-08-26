# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing checks for potentially hardcoded passwords.
"""

#
# This is a modified version of the one found in the bandit package.
#
# Original Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# SPDX-License-Identifier: Apache-2.0
#

import ast
import re

import AstUtilities

RE_WORDS = "(pas+wo?r?d|pass(phrase)?|pwd|token|secrete?|ken+wort|geheim)"
RE_CANDIDATES = re.compile(
    '(^{0}$|_{0}_|^{0}_|_{0}$)'.format(RE_WORDS),
    re.IGNORECASE
)


def getChecks():
    """
    Public method to get a dictionary with checks handled by this module.
    
    @return dictionary containing checker lists containing checker function and
        list of codes
    @rtype dict
    """
    return {
        "Str": [
            (checkHardcodedPasswordAsString, ("S105",)),
        ],
        "Call": [
            (checkHardcodedPasswordAsFunctionArg, ("S106",)),
        ],
        "FunctionDef": [
            (checkHardcodedPasswordAsDefault, ("S107",)),
        ],
    }


def checkHardcodedPasswordAsString(reportError, context, config):
    """
    Function to check for use of hardcoded password strings.
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    node = context.node
    if isinstance(node._securityParent, ast.Assign):
        # looks for "candidate='some_string'"
        for targ in node._securityParent.targets:
            if isinstance(targ, ast.Name) and RE_CANDIDATES.search(targ.id):
                reportError(
                    context.node.lineno - 1,
                    context.node.col_offset,
                    "S105",
                    "L",
                    "M",
                    node.s
                )
    
    elif (
        isinstance(node._securityParent, ast.Index) and
        RE_CANDIDATES.search(node.s)
    ):
        # looks for "dict[candidate]='some_string'"
        # assign -> subscript -> index -> string
        assign = node._securityParent._securityParent._securityParent
        if (
            isinstance(assign, ast.Assign) and
            AstUtilities.isString(assign.value)
        ):
            reportError(
                context.node.lineno - 1,
                context.node.col_offset,
                "S105",
                "L",
                "M",
                assign.value.s
            )
    
    elif isinstance(node._securityParent, ast.Compare):
        # looks for "candidate == 'some_string'"
        comp = node._securityParent
        if isinstance(comp.left, ast.Name):
            if RE_CANDIDATES.search(comp.left.id):
                if AstUtilities.isString(comp.comparators[0]):
                    reportError(
                        context.node.lineno - 1,
                        context.node.col_offset,
                        "S105",
                        "L",
                        "M",
                        comp.comparators[0].s
                    )


def checkHardcodedPasswordAsFunctionArg(reportError, context, config):
    """
    Function to check for use of hard-coded password function arguments.
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    # looks for "function(candidate='some_string')"
    for kw in context.node.keywords:
        if AstUtilities.isString(kw.value) and RE_CANDIDATES.search(kw.arg):
            reportError(
                context.node.lineno - 1,
                context.node.col_offset,
                "S106",
                "L",
                "M",
                kw.value.s
            )


def checkHardcodedPasswordAsDefault(reportError, context, config):
    """
    Function to check for use of hard-coded password argument defaults.
    
    @param reportError function to be used to report errors
    @type func
    @param context security context object
    @type SecurityContext
    @param config dictionary with configuration data
    @type dict
    """
    # looks for "def function(candidate='some_string')"
    
    # this pads the list of default values with "None" if nothing is given
    defs = [None] * (len(context.node.args.args) -
                     len(context.node.args.defaults))
    defs.extend(context.node.args.defaults)
    
    # go through all (param, value)s and look for candidates
    for key, val in zip(context.node.args.args, defs):
        if isinstance(key, ast.Name) or isinstance(key, ast.arg):
            if AstUtilities.isString(val) and RE_CANDIDATES.search(key.arg):
                reportError(
                    context.node.lineno - 1,
                    context.node.col_offset,
                    "S107",
                    "L",
                    "M",
                    val.s
                )
