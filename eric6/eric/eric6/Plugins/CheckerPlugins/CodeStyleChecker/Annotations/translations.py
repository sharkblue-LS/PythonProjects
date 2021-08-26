# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#


"""
Module implementing message translations for the code style plugin messages
(code annotations part).
"""

from PyQt5.QtCore import QCoreApplication

_annotationsMessages = {
    "A001": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing type annotation for function argument '{0}'"),
    "A002": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing type annotation for '*{0}'"),
    "A003": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing type annotation for '**{0}'"),
    "A101": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing type annotation for 'self' in method"),
    "A102": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing type annotation for 'cls' in classmethod"),
    "A201": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing return type annotation for public function"),
    "A202": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing return type annotation for protected function"),
    "A203": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing return type annotation for private function"),
    "A204": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing return type annotation for special method"),
    "A205": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing return type annotation for staticmethod"),
    "A206": QCoreApplication.translate(
        "AnnotationsChecker",
        "missing return type annotation for classmethod"),
    
    "A881": QCoreApplication.translate(
        "AnnotationsChecker",
        "type annotation coverage of {0}% is too low"),
    
    "A891": QCoreApplication.translate(
        "AnnotationsChecker",
        "type annotation is too complex ({0} > {1})"),
    
    "A999": QCoreApplication.translate(
        "AnnotationsChecker",
        "{0}: {1}"),
}

_annotationsMessagesSampleArgs = {
    "A001": ["arg1"],
    "A002": ["args"],
    "A003": ["kwargs"],
    "A881": [60],
    "A891": [5, 3],
    "A999": ["SyntaxError", "Invalid Syntax"],
}
