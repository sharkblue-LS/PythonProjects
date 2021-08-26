#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the post install logic for 'pip install'.
"""

import sys
import os
import shutil
import sysconfig

######################################################################
## Post installation hooks for Windows below
######################################################################


def createWindowsLinks():
    """
    Create Desktop and Start Menu links.
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


def windowsDesktopEntries():
    """
    Function to generate data for the Windows Desktop links.
    
    @return list of tuples containing the desktop link name,
        the link target and the icon target
    @rtype list of tuples of (str, str, str)
    """
    majorVersion, minorVersion = sys.version_info[:2]
    scriptsDir = sysconfig.get_path("scripts")
    entriesTemplates = [
        ("eric6 (Python {0}.{1}).lnk",
         os.path.join(scriptsDir, "eric6.exe"),
         os.path.join(scriptsDir, "eric6.ico")
         ),
        ("eric6 Browser (Python {0}.{1}).lnk",
         os.path.join(scriptsDir, "eric6_browser.exe"),
         os.path.join(scriptsDir, "ericWeb48.ico")
         ),
    ]
    
    return [
        (e[0].format(majorVersion, minorVersion), e[1], e[2])
        for e in entriesTemplates
    ]


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


def windowsProgramsEntry():
    """
    Function to generate the name of the Start Menu top entry.
    
    @return name of the Start Menu top entry
    @rtype str
    """
    majorVersion, minorVersion = sys.version_info[:2]
    return "eric6 (Python {0}.{1})".format(majorVersion, minorVersion)

######################################################################
## Post installation hooks for Linux below
######################################################################


def copyLinuxMetaData():
    """
    Function to copy the meta data files.
    """
    scriptsDir = sysconfig.get_path("scripts")
    srcDir = os.path.join(os.path.dirname(scriptsDir), "share")
    dstDir = os.path.join(os.path.expanduser("~"), ".local", "share")
    
    for metaDir in ["icons", "appdata", "metainfo"]:
        copyMetaFilesTree(os.path.join(srcDir, metaDir),
                          os.path.join(dstDir, metaDir))
    
    for desktop in ["eric6.desktop", "eric6_browser.desktop"]:
        copyDesktopFile(
            os.path.join(srcDir, "applications", desktop),
            os.path.join(dstDir, "applications", desktop),
            scriptsDir
        )


def copyMetaFilesTree(src, dst):
    """
    Function to copy the files of a directory tree.
    
    @param src name of the source directory
    @param dst name of the destination directory
    """
    try:
        names = os.listdir(src)
    except OSError:
        # ignore missing directories (most probably the i18n directory)
        return
    
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if not os.path.isdir(dst):
            os.makedirs(dst)
        shutil.copy2(srcname, dstname)
        os.chmod(dstname, 0o644)
        
        if os.path.isdir(srcname):
            copyMetaFilesTree(srcname, dstname)


def copyDesktopFile(src, dst, scriptsdir):
    """
    Modify a desktop file and write it to its destination.
    
    @param src source file name (string)
    @param dst destination file name (string)
    @param scriptsdir directory containing the scripts (string)
    """
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = text.replace("@BINDIR@", scriptsdir)
    
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(dst, 0o644)

######################################################################
## Main script below
######################################################################


def main():
    """
    Main script orchestrating the platform dependent post installation tasks.
    """
    if sys.platform.startswith(("win", "cygwin")):
        createWindowsLinks()
    elif sys.platform.startswith("linux"):
        copyLinuxMetaData()
    
    sys.exit(0)


if __name__ == "__main__":
    main()
