# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing various kinds of completers.
"""

import os

from PyQt5.QtCore import QDir, Qt, QStringListModel
from PyQt5.QtWidgets import QCompleter, QFileSystemModel

from Globals import isWindowsPlatform


class E5FileCompleter(QCompleter):
    """
    Class implementing a completer for file names.
    """
    def __init__(self, parent=None,
                 completionMode=QCompleter.CompletionMode.PopupCompletion,
                 showHidden=False):
        """
        Constructor
        
        @param parent parent widget of the completer (QWidget)
        @param completionMode completion mode of the
            completer (QCompleter.CompletionMode)
        @param showHidden flag indicating to show hidden entries as well
            (boolean)
        """
        super(E5FileCompleter, self).__init__(parent)
        self.__model = QFileSystemModel(self)
        if showHidden:
            self.__model.setFilter(QDir.Filters(
                QDir.Filter.Dirs |
                QDir.Filter.Files |
                QDir.Filter.Drives |
                QDir.Filter.AllDirs |
                QDir.Filter.Hidden))
        else:
            self.__model.setFilter(QDir.Filters(
                QDir.Filter.Dirs |
                QDir.Filter.Files |
                QDir.Filter.Drives |
                QDir.Filter.AllDirs))
        self.__model.setRootPath("")
        self.setModel(self.__model)
        self.setCompletionMode(completionMode)
        if isWindowsPlatform():
            self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        if parent:
            parent.setCompleter(self)
    
    def setRootPath(self, path):
        """
        Public method to set the root path of the model.
        
        @param path root path for the model
        @type str
        """
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        self.__model.setRootPath(path)
    
    def rootPath(self):
        """
        Public method to get the root path of the model.
        
        @return root path of the model
        @rtype str
        """
        return self.__model.rootPath()


class E5DirCompleter(QCompleter):
    """
    Class implementing a completer for directory names.
    """
    def __init__(self, parent=None,
                 completionMode=QCompleter.CompletionMode.PopupCompletion,
                 showHidden=False):
        """
        Constructor
        
        @param parent parent widget of the completer (QWidget)
        @param completionMode completion mode of the
            completer (QCompleter.CompletionMode)
        @param showHidden flag indicating to show hidden entries as well
            (boolean)
        """
        super(E5DirCompleter, self).__init__(parent)
        self.__model = QFileSystemModel(self)
        if showHidden:
            self.__model.setFilter(QDir.Filters(
                QDir.Filter.Drives |
                QDir.Filter.AllDirs |
                QDir.Filter.Hidden))
        else:
            self.__model.setFilter(
                QDir.Filters(QDir.Filter.Drives | QDir.Filter.AllDirs))
        self.__model.setRootPath("")
        self.setModel(self.__model)
        self.setCompletionMode(completionMode)
        if isWindowsPlatform():
            self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        if parent:
            parent.setCompleter(self)
    
    def setRootPath(self, path):
        """
        Public method to set the root path of the model.
        
        @param path root path for the model
        @type str
        """
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        self.__model.setRootPath(path)
    
    def rootPath(self):
        """
        Public method to get the root path of the model.
        
        @return root path of the model
        @rtype str
        """
        return self.__model.rootPath()


class E5StringListCompleter(QCompleter):
    """
    Class implementing a completer for string lists.
    """
    def __init__(self, parent=None, strings=None,
                 completionMode=QCompleter.CompletionMode.PopupCompletion):
        """
        Constructor
        
        @param parent parent widget of the completer (QWidget)
        @param strings list of string to load into the completer
            (list of strings)
        @param completionMode completion mode of the
            completer (QCompleter.CompletionMode)
        """
        super(E5StringListCompleter, self).__init__(parent)
        self.__model = QStringListModel(
            [] if strings is None else strings[:],
            parent)
        self.setModel(self.__model)
        self.setCompletionMode(completionMode)
        if parent:
            parent.setCompleter(self)
