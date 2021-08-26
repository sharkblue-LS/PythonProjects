# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module defining the different Python types and their display strings.
"""

from PyQt5.QtCore import QT_TRANSLATE_NOOP

# Variable type definitions
ConfigVarTypeDispStrings = {
    '__': QT_TRANSLATE_NOOP('Variable Types', 'Hidden Attributes'),
    'NoneType': QT_TRANSLATE_NOOP('Variable Types', 'None'),
    'type': QT_TRANSLATE_NOOP('Variable Types', 'Type'),
    'bool': QT_TRANSLATE_NOOP('Variable Types', 'Boolean'),
    'int': QT_TRANSLATE_NOOP('Variable Types', 'Integer'),
    'long': QT_TRANSLATE_NOOP('Variable Types', 'Long Integer'),
    'float': QT_TRANSLATE_NOOP('Variable Types', 'Float'),
    'complex': QT_TRANSLATE_NOOP('Variable Types', 'Complex'),
    'str': QT_TRANSLATE_NOOP('Variable Types', 'String'),
    'tuple': QT_TRANSLATE_NOOP('Variable Types', 'Tuple'),
    'list': QT_TRANSLATE_NOOP('Variable Types', 'List/Array'),
    'dict': QT_TRANSLATE_NOOP('Variable Types', 'Dictionary/Hash/Map'),
    'dict-proxy': QT_TRANSLATE_NOOP('Variable Types', 'Dictionary Proxy'),
    'set': QT_TRANSLATE_NOOP('Variable Types', 'Set'),
    'frozenset': QT_TRANSLATE_NOOP('Variable Types', 'Frozen Set'),
    'file': QT_TRANSLATE_NOOP('Variable Types', 'File'),
    'xrange': QT_TRANSLATE_NOOP('Variable Types', 'X Range'),
    'slice': QT_TRANSLATE_NOOP('Variable Types', 'Slice'),
    'buffer': QT_TRANSLATE_NOOP('Variable Types', 'Buffer'),
    'class': QT_TRANSLATE_NOOP('Variable Types', 'Class'),
    'instance': QT_TRANSLATE_NOOP('Variable Types', 'Class Instance'),
    'method': QT_TRANSLATE_NOOP('Variable Types', 'Class Method'),
    'property': QT_TRANSLATE_NOOP('Variable Types', 'Class Property'),
    'generator': QT_TRANSLATE_NOOP('Variable Types', 'Generator'),
    'function': QT_TRANSLATE_NOOP('Variable Types', 'Function'),
    'builtin_function_or_method':
        QT_TRANSLATE_NOOP('Variable Types', 'Builtin Function'),
    'code': QT_TRANSLATE_NOOP('Variable Types', 'Code'),
    'module': QT_TRANSLATE_NOOP('Variable Types', 'Module'),
    'ellipsis': QT_TRANSLATE_NOOP('Variable Types', 'Ellipsis'),
    'traceback': QT_TRANSLATE_NOOP('Variable Types', 'Traceback'),
    'frame': QT_TRANSLATE_NOOP('Variable Types', 'Frame'),
    'bytes': QT_TRANSLATE_NOOP('Variable Types', 'Bytes'),
    "special_attributes": QT_TRANSLATE_NOOP(
        'Variable Types', "Special Attributes"),
}
