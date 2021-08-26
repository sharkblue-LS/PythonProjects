# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing alternative functions for the QFileDialog static methods
to cope with distributor's usage of KDE wrapper dialogs for Qt file dialogs.
"""

from PyQt5.QtWidgets import QFileDialog

import Globals

Options = QFileDialog.Options
Option = QFileDialog.Option

ShowDirsOnly = QFileDialog.Option.ShowDirsOnly
DontResolveSymlinks = QFileDialog.Option.DontResolveSymlinks
DontConfirmOverwrite = QFileDialog.Option.DontConfirmOverwrite
DontUseNativeDialog = QFileDialog.Option.DontUseNativeDialog
ReadOnly = QFileDialog.Option.ReadOnly
HideNameFilterDetails = QFileDialog.Option.HideNameFilterDetails
DontUseSheet = QFileDialog.Option.DontUseSheet
DontUseCustomDirectoryIcons = QFileDialog.Option.DontUseCustomDirectoryIcons


def __reorderFilter(filterStr, initialFilter=""):
    """
    Private function to reorder the file filter to cope with a KDE issue
    introduced by distributor's usage of KDE file dialogs.
    
    @param filterStr Qt file filter (string)
    @param initialFilter initial filter (string)
    @return the rearranged Qt file filter (string)
    """
    if initialFilter and not Globals.isMacPlatform():
        fileFilters = filterStr.split(';;')
        if len(fileFilters) < 10 and initialFilter in fileFilters:
            fileFilters.remove(initialFilter)
        fileFilters.insert(0, initialFilter)
        return ";;".join(fileFilters)
    else:
        return filterStr


def getOpenFileName(parent=None, caption="", directory="",
                    filterStr="", options=None):
    """
    Module function to get the name of a file for opening it.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param filterStr filter string for the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return name of file to be opened (string)
    """
    if options is None:
        options = QFileDialog.Options()
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    return QFileDialog.getOpenFileName(
        parent, caption, directory, filterStr, "", options)[0]


def getOpenFileNameAndFilter(parent=None, caption="", directory="",
                             filterStr="", initialFilter="",
                             options=None):
    """
    Module function to get the name of a file for opening it and the selected
    file name filter.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param filterStr filter string for the dialog (string)
    @param initialFilter initial filter for the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return name of file to be opened and selected filter (string, string)
    """
    if options is None:
        options = QFileDialog.Options()
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    newfilter = __reorderFilter(filterStr, initialFilter)
    return QFileDialog.getOpenFileName(
        parent, caption, directory, newfilter, initialFilter, options)


def getOpenFileNames(parent=None, caption="", directory="",
                     filterStr="", options=None):
    """
    Module function to get a list of names of files for opening.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param filterStr filter string for the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return list of file names to be opened (list of string)
    """
    if options is None:
        options = QFileDialog.Options()
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    return QFileDialog.getOpenFileNames(
        parent, caption, directory, filterStr, "", options)[0]


def getOpenFileNamesAndFilter(parent=None, caption="", directory="",
                              filterStr="", initialFilter="",
                              options=None):
    """
    Module function to get a list of names of files for opening and the
    selected file name filter.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param filterStr filter string for the dialog (string)
    @param initialFilter initial filter for the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return list of file names to be opened and selected filter
        (list of string, string)
    """
    if options is None:
        options = QFileDialog.Options()
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    newfilter = __reorderFilter(filterStr, initialFilter)
    return QFileDialog.getOpenFileNames(
        parent, caption, directory, newfilter, initialFilter, options)


def getSaveFileName(parent=None, caption="", directory="",
                    filterStr="", options=None):
    """
    Module function to get the name of a file for saving it.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param filterStr filter string for the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return name of file to be saved (string)
    """
    if options is None:
        options = QFileDialog.Options()
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    return QFileDialog.getSaveFileName(
        parent, caption, directory, filterStr, "", options)[0]


def getSaveFileNameAndFilter(parent=None, caption="", directory="",
                             filterStr="", initialFilter="",
                             options=None):
    """
    Module function to get the name of a file for saving it and the selected
    file name filter.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param filterStr filter string for the dialog (string)
    @param initialFilter initial filter for the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return name of file to be saved and selected filter (string, string)
    """
    if options is None:
        options = QFileDialog.Options()
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    newfilter = __reorderFilter(filterStr, initialFilter)
    return QFileDialog.getSaveFileName(
        parent, caption, directory, newfilter, initialFilter, options)


def getExistingDirectory(parent=None, caption="",
                         directory="",
                         options=QFileDialog.Option.ShowDirsOnly):
    """
    Module function to get the name of a directory.
    
    @param parent parent widget of the dialog (QWidget)
    @param caption window title of the dialog (string)
    @param directory working directory of the dialog (string)
    @param options various options for the dialog (QFileDialog.Options)
    @return name of selected directory (string)
    """
    if Globals.isLinuxPlatform():
        options |= QFileDialog.Option.DontUseNativeDialog
    return QFileDialog.getExistingDirectory(parent, caption, directory,
                                            options)
