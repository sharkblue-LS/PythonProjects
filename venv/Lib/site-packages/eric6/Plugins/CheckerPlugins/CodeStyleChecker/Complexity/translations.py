# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing message translations for the code style plugin messages
(code complexity part).
"""

from PyQt5.QtCore import QCoreApplication

_complexityMessages = {
    "C101": QCoreApplication.translate(
        "ComplexityChecker", "'{0}' is too complex ({1})"),
    "C111": QCoreApplication.translate(
        "ComplexityChecker", "source code line is too complex ({0})"),
    "C112": QCoreApplication.translate(
        "ComplexityChecker",
        "overall source code line complexity is too high ({0})"),
    "C901": QCoreApplication.translate(
        "ComplexityChecker", "{0}: {1}"),
}

_complexityMessagesSampleArgs = {
    "C101": ["foo.bar", "42"],
    "C111": [42],
    "C112": [12.0],
    "C901": ["SyntaxError", "Invalid Syntax"],
}
