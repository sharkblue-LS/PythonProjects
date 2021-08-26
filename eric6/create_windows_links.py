#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#
# This is the install script for eric.

"""
Installation script for the eric IDE and all eric related tools.
"""

import os
import sys

from eric6config import getConfig


def main(argv):
    """
    Create Desktop and Start Menu links.
    
    @param argv list of command line arguments
    @type list of str
    """
    regPath = (
        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" +
        "\\User Shell Folders"
    )
    
    # 1. create desktop shortcuts
    regName = "Desktop"
    desktopFolder = os.path.normpath(
        os.path.expandvars(getWinregEntry(regName, regPath)))
    for linkName, targetPath, iconPath in windowsDesktopEntries():
        linkPath = os.path.join(desktopFolder, linkName)
        createWindowsShortcut(linkPath, targetPath, iconPath)
    
    # 2. create start menu entry and shortcuts
    regName = "Programs"
    programsEntry = getWinregEntry(regName, regPath)
    if programsEntry:
        programsFolder = os.path.normpath(os.path.expandvars(programsEntry))
        eric6EntryPath = os.path.join(programsFolder, windowsProgramsEntry())
        if not os.path.exists(eric6EntryPath):
            try:
                os.makedirs(eric6EntryPath)
            except OSError:
                # maybe restrictions prohibited link creation
                return
        
        for linkName, targetPath, iconPath in windowsDesktopEntries():
            linkPath = os.path.join(eric6EntryPath, linkName)
            createWindowsShortcut(linkPath, targetPath, iconPath)


def getWinregEntry(name, path):
    """
    Function to get an entry from the Windows Registry.
    
    @param name variable name
    @type str
    @param path registry path of the variable
    @type str
    @return value of requested registry variable
    @rtype any
    """
    try:
        import winreg
    except ImportError:
        return None
    
    try:
        registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0,
                                     winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(registryKey, name)
        winreg.CloseKey(registryKey)
        return value
    except WindowsError:
        return None


def createWindowsShortcut(linkPath, targetPath, iconPath):
    """
    Create Windows shortcut.
    
    @param linkPath path of the shortcut file
    @type str
    @param targetPath path the shortcut shall point to
    @type str
    @param iconPath path of the icon file
    @type str
    """
    from win32com.client import Dispatch
    from pywintypes import com_error
    
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(linkPath)
        shortcut.Targetpath = targetPath
        shortcut.WorkingDirectory = os.path.dirname(targetPath)
        shortcut.IconLocation = iconPath
        shortcut.save()
    except com_error:
        # maybe restrictions prohibited link creation
        pass


def windowsDesktopNames():
    """
    Function to generate the link names for the Windows Desktop.
    
    @return list of desktop link names
    @rtype list of str
    """
    return [e[0] for e in windowsDesktopEntries()]


def windowsDesktopEntries():
    """
    Function to generate data for the Windows Desktop links.
    
    @return list of tuples containing the desktop link name,
        the link target and the icon target
    @rtype list of tuples of (str, str, str)
    """
    majorVersion, minorVersion = sys.version_info[:2]
    entriesTemplates = [
        ("eric6 (Python {0}.{1}).lnk",
         os.path.join(getConfig("bindir"), "eric6.cmd"),
         os.path.join(getConfig("ericPixDir"), "eric6.ico")),
        ("eric6 Browser (Python {0}.{1}).lnk",
         os.path.join(getConfig("bindir"), "eric6_browser.cmd"),
         os.path.join(getConfig("ericPixDir"), "ericWeb48.ico")),
    ]
    
    return [
        (e[0].format(majorVersion, minorVersion), e[1], e[2])
        for e in entriesTemplates
    ]


def windowsProgramsEntry():
    """
    Function to generate the name of the Start Menu top entry.
    
    @return name of the Start Menu top entry
    @rtype str
    """
    majorVersion, minorVersion = sys.version_info[:2]
    return "eric6 (Python {0}.{1})".format(majorVersion, minorVersion)
    
    
if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit:
        raise
    except Exception:
        print("""An internal error occured.  Please report all the output"""
              """ of the program,\nincluding the following traceback, to"""
              """ eric-bugs@eric-ide.python-projects.org.\n""")
        raise

#
# eflag: noqa = M801
