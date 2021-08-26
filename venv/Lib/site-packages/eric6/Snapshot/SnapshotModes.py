# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the snapshot mode enumeration.
"""

from enum import Enum


class SnapshotModes(Enum):
    """
    Class implementing the snapshot modes.
    """
    Fullscreen = 0
    SelectedScreen = 1
    Rectangle = 2
    Freehand = 3
    Ellipse = 4
    SelectedWindow = 5
