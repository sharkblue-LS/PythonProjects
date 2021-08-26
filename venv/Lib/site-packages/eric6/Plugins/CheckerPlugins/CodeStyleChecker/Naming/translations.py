# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing message translations for the code style plugin messages
(miscellaneous part).
"""

from PyQt5.QtCore import QCoreApplication

_namingStyleMessages = {
    "N801": QCoreApplication.translate(
        "NamingStyleChecker",
        "class names should use CapWords convention"),
    "N802": QCoreApplication.translate(
        "NamingStyleChecker",
        "function name should be lowercase"),
    "N803": QCoreApplication.translate(
        "NamingStyleChecker",
        "argument name should be lowercase"),
    "N804": QCoreApplication.translate(
        "NamingStyleChecker",
        "first argument of a class method should be named 'cls'"),
    "N805": QCoreApplication.translate(
        "NamingStyleChecker",
        "first argument of a method should be named 'self'"),
    "N806": QCoreApplication.translate(
        "NamingStyleChecker",
        "first argument of a static method should not be named"
        " 'self' or 'cls"),
    "N807": QCoreApplication.translate(
        "NamingStyleChecker",
        "module names should be lowercase"),
    "N808": QCoreApplication.translate(
        "NamingStyleChecker",
        "package names should be lowercase"),
    "N811": QCoreApplication.translate(
        "NamingStyleChecker",
        "constant imported as non constant"),
    "N812": QCoreApplication.translate(
        "NamingStyleChecker",
        "lowercase imported as non lowercase"),
    "N813": QCoreApplication.translate(
        "NamingStyleChecker",
        "camelcase imported as lowercase"),
    "N814": QCoreApplication.translate(
        "NamingStyleChecker",
        "camelcase imported as constant"),
    "N821": QCoreApplication.translate(
        "NamingStyleChecker",
        "variable in function should be lowercase"),
    "N831": QCoreApplication.translate(
        "NamingStyleChecker",
        "names 'l', 'O' and 'I' should be avoided"),
}
