# -*- coding: utf-8 -*-

# Copyright (c) 2005 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module defining type strings for the different Python types.
"""


SpecialAttributes = (
    "__bases__", "__class__", "__dict__", "__doc__", "__mro__", "__name__",
    "__qualname__",
)
BatchSize = 200
ConfigQtNames = (
    'PyQt5.', 'PyQt6.', 'PySide2.', 'PySide6.', 'Shiboken.EnumType'
)
ConfigKnownQtTypes = (
    '.QChar', '.QByteArray', '.QString', '.QStringList', '.QPoint', '.QPointF',
    '.QRect', '.QRectF', '.QSize', '.QSizeF', '.QColor', '.QDate', '.QTime',
    '.QDateTime', '.QDir', '.QFile', '.QFont', '.QUrl', '.QModelIndex',
    '.QRegExp', '.QRegularExpression', '.QAction', '.QKeySequence',
    '.QDomAttr', '.QDomCharacterData', '.QDomComment', '.QDomDocument',
    '.QDomElement', '.QDomText', '.QHostAddress', '.EnumType'
)
