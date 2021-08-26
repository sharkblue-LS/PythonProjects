#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#
# This is the uninstall script for eric.
#

"""
Uninstallation script for the eric IDE and all eric related tools.
"""

import sys
import os
import shutil
import glob
import distutils.sysconfig

# Define the globals.
progName = None
currDir = os.getcwd()
pyModDir = None
progLanguages = ["Python", "Ruby", "QSS"]
defaultMacAppBundleName = "eric6.app"
defaultMacAppBundlePath = "/Applications"
settingsNameOrganization = "Eric6"
settingsNameGlobal = "eric6"


def exit(rcode=0):
    """
    Exit the uninstall script.
    
    @param rcode result code to report back (integer)
    """
    global currDir
    
    # restore the local eric6config.py
    if os.path.exists("eric6config.py.orig"):
        if os.path.exists("eric6config.py"):
            os.remove("eric6config.py")
        os.rename("eric6config.py.orig", "eric6config.py")
    
    if sys.platform.startswith(("win", "cygwin")):
        try:
            input("Press enter to continue...")         # secok
        except (EOFError, SyntaxError):
            pass
    
    os.chdir(currDir)
    
    sys.exit(rcode)

# get a local eric6config.py out of the way
if os.path.exists("eric6config.py"):
    os.rename("eric6config.py", "eric6config.py.orig")
try:
    from eric6config import getConfig
except ImportError:
    print("The eric IDE doesn't seem to be installed. Aborting.")
    exit(1)
except SyntaxError:
    # an incomplete or old config file was found
    print("The eric IDE seems to be installed incompletely. Aborting.")
    exit(1)


def usage(rcode=2):
    """
    Display a usage message and exit.

    @param rcode return code passed back to the calling process (integer)
    """
    global progName

    print("Usage:")
    print("    {0} [-h]".format(progName))
    print("where:")
    print("    -h             display this help message")

    exit(rcode)


def initGlobals():
    """
    Set the values of globals that need more than a simple assignment.
    """
    global pyModDir

    pyModDir = distutils.sysconfig.get_python_lib(True)


def wrapperNames(dname, wfile):
    """
    Create the platform specific names for the wrapper script.
    
    @param dname name of the directory to place the wrapper into
    @param wfile basename (without extension) of the wrapper script
    @return the names of the wrapper scripts
    """
    if sys.platform.startswith(("win", "cygwin")):
        wnames = (dname + "\\" + wfile + ".cmd",
                  dname + "\\" + wfile + ".bat")
    else:
        wnames = (dname + "/" + wfile, )

    return wnames


def uninstallEric():
    """
    Uninstall the eric files.
    """
    global pyModDir
    
    # Remove the menu entry for Linux systems
    if sys.platform.startswith("linux"):
        uninstallLinuxSpecifics()
    # Remove the Desktop and Start Menu entries for Windows systems
    elif sys.platform.startswith(("win", "cygwin")):
        uninstallWindowsLinks()
    
    # Remove the wrapper scripts
    rem_wnames = [
        "eric6_api", "eric6_compare",
        "eric6_configure", "eric6_diff",
        "eric6_doc", "eric6_qregularexpression",
        "eric6_qregexp", "eric6_re",
        "eric6_trpreviewer", "eric6_uipreviewer",
        "eric6_unittest", "eric6",
        "eric6_tray", "eric6_editor",
        "eric6_plugininstall", "eric6_pluginuninstall",
        "eric6_pluginrepository", "eric6_sqlbrowser",
        "eric6_iconeditor", "eric6_snap", "eric6_hexeditor",
        "eric6_browser", "eric6_shell",
        # from Python2 era
        "eric6_webbrowser",
    ]
    
    try:
        for rem_wname in rem_wnames:
            for rwname in wrapperNames(getConfig('bindir'), rem_wname):
                if os.path.exists(rwname):
                    os.remove(rwname)
        
        # Cleanup our config file(s)
        for name in ['eric6config.py', 'eric6config.pyc', 'eric6.pth']:
            e5cfile = os.path.join(pyModDir, name)
            if os.path.exists(e5cfile):
                os.remove(e5cfile)
            e5cfile = os.path.join(pyModDir, "__pycache__", name)
            path, ext = os.path.splitext(e5cfile)
            for f in glob.glob("{0}.*{1}".format(path, ext)):
                os.remove(f)
        
        # Cleanup the install directories
        for name in ['ericExamplesDir', 'ericDocDir', 'ericDTDDir',
                     'ericCSSDir', 'ericIconDir', 'ericPixDir',
                     'ericTemplatesDir', 'ericCodeTemplatesDir',
                     'ericOthersDir', 'ericStylesDir', 'ericDir']:
            dirpath = getConfig(name)
            if os.path.exists(dirpath):
                shutil.rmtree(dirpath, True)
        
        # Cleanup translations
        for name in glob.glob(
                os.path.join(getConfig('ericTranslationsDir'), 'eric6_*.qm')):
            if os.path.exists(name):
                os.remove(name)
        
        # Cleanup API files
        apidir = getConfig('apidir')
        if apidir:
            for progLanguage in progLanguages:
                for name in getConfig('apis'):
                    apiname = os.path.join(apidir, progLanguage.lower(), name)
                    if os.path.exists(apiname):
                        os.remove(apiname)
                for apiname in glob.glob(
                        os.path.join(apidir, progLanguage.lower(), "*.bas")):
                    if os.path.basename(apiname) != "eric6.bas":
                        os.remove(apiname)
        
        if sys.platform == "darwin":
            # delete the Mac app bundle
            uninstallMacAppBundle()
        
        # remove plug-in directories
        removePluginDirectories()
        
        # remove the eric data directory
        removeDataDirectory()
        
        # remove the eric configuration directory
        removeConfigurationData()
        
        print("\nUninstallation completed")
    except OSError as msg:
        sys.stderr.write(
            'Error: {0}\nTry uninstall with admin rights.\n'.format(msg))
        exit(7)


def uninstallWindowsLinks():
    """
    Clean up the Desktop and Start Menu entries for Windows.
    """
    try:
        from pywintypes import com_error        # __IGNORE_WARNING__
    except ImportError:
        # links were not created by install.py
        return
    
    regPath = (
        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" +
        "\\User Shell Folders"
    )
    
    # 1. cleanup desktop links
    regName = "Desktop"
    desktopEntry = getWinregEntry(regName, regPath)
    if desktopEntry:
        desktopFolder = os.path.normpath(os.path.expandvars(desktopEntry))
        for linkName in windowsDesktopNames():
            linkPath = os.path.join(desktopFolder, linkName)
            if os.path.exists(linkPath):
                try:
                    os.remove(linkPath)
                except OSError:
                    # maybe restrictions prohibited link removal
                    print("Could not remove '{0}'.".format(linkPath))
    
    # 2. cleanup start menu entry
    regName = "Programs"
    programsEntry = getWinregEntry(regName, regPath)
    if programsEntry:
        programsFolder = os.path.normpath(os.path.expandvars(programsEntry))
        eric6EntryPath = os.path.join(programsFolder, windowsProgramsEntry())
        if os.path.exists(eric6EntryPath):
            try:
                shutil.rmtree(eric6EntryPath)
            except OSError:
                # maybe restrictions prohibited link removal
                print("Could not remove '{0}'.".format(eric6EntryPath))


def uninstallLinuxSpecifics():
    """
    Uninstall Linux specific files.
    """
    if os.getuid() == 0:
        for name in ["/usr/share/pixmaps/eric.png",
                     "/usr/share/pixmaps/ericWeb.png"]:
            if os.path.exists(name):
                os.remove(name)
        for name in [
            "/usr/share/applications/eric6.desktop",
            "/usr/share/appdata/eric6.appdata.xml",
            "/usr/share/metainfo/eric6.appdata.xml",
            "/usr/share/applications/eric6_browser.desktop",
            "/usr/share/pixmaps/eric.png",
            "/usr/share/pixmaps/ericWeb.png",
            # from Python2 era
            "/usr/share/applications/eric6_webbrowser.desktop",
        ]:
            if os.path.exists(name):
                os.remove(name)
    elif os.getuid() >= 1000:
        # it is assumed that user ids start at 1000
        for name in ["~/.local/share/pixmaps/eric.png",
                     "~/.local/share/pixmaps/ericWeb.png"]:
            path = os.path.expanduser(name)
            if os.path.exists(path):
                os.remove(path)
        for name in [
            "~/.local/share/applications/eric6.desktop",
            "~/.local/share/appdata/eric6.appdata.xml",
            "~/.local/share/metainfo/eric6.appdata.xml",
            "~/.local/share/applications/eric6_browser.desktop",
            "~/.local/share/pixmaps/eric.png",
            "~/.local/share/pixmaps/ericWeb.png",
            # from Python2 era
            "/usr/share/applications/eric6_webbrowser.desktop",
        ]:
            path = os.path.expanduser(name)
            if os.path.exists(path):
                os.remove(path)


def uninstallMacAppBundle():
    """
    Uninstall the macOS application bundle.
    """
    if os.path.exists("/Developer/Applications/Eric6"):
        shutil.rmtree("/Developer/Applications/Eric6")
    try:
        macAppBundlePath = getConfig("macAppBundlePath")
        macAppBundleName = getConfig("macAppBundleName")
    except AttributeError:
        macAppBundlePath = defaultMacAppBundlePath
        macAppBundleName = defaultMacAppBundleName
    for bundlePath in [os.path.join(defaultMacAppBundlePath,
                                    macAppBundleName),
                       os.path.join(macAppBundlePath,
                                    macAppBundleName),
                       ]:
        if os.path.exists(bundlePath):
            shutil.rmtree(bundlePath)


def removePluginDirectories():
    """
    Remove the plug-in directories.
    """
    pathsToRemove = []
    
    globalPluginsDir = os.path.join(getConfig('mdir'), "eric6plugins")
    if os.path.exists(globalPluginsDir):
        pathsToRemove.append(globalPluginsDir)
    
    localPluginsDir = os.path.join(getConfigDir(), "eric6plugins")
    if os.path.exists(localPluginsDir):
        pathsToRemove.append(localPluginsDir)
    
    if pathsToRemove:
        print("Found these plug-in directories")
        for path in pathsToRemove:
            print("  - {0}".format(path))
        answer = "c"
        while answer not in ["y", "Y", "n", "N", ""]:
            answer = input("Shall these directories be removed (y/N)? ")
            # secok
        if answer in ["y", "Y"]:
            for path in pathsToRemove:
                shutil.rmtree(path)


def removeDataDirectory():
    """
    Remove the eric data directory.
    """
    cfg = getConfigDir()
    if os.path.exists(cfg):
        print("Found the eric data directory")
        print("  - {0}".format(cfg))
        answer = "c"
        while answer not in ["y", "Y", "n", "N", ""]:
            answer = input("Shall this directory be removed (y/N)? ")
            # secok
        if answer in ["y", "Y"]:
            shutil.rmtree(cfg)


def removeConfigurationData():
    """
    Remove the eric configuration directory.
    """
    try:
        from PyQt5.QtCore import QSettings
    except ImportError:
        print("No PyQt variant installed. The configuration directory")
        print("cannot be determined. You have to remove it manually.\n")
        return
    
    settings = QSettings(QSettings.IniFormat, QSettings.UserScope,
                         settingsNameOrganization, settingsNameGlobal)
    settingsDir = os.path.dirname(settings.fileName())
    if os.path.exists(settingsDir):
        print("Found the eric configuration directory")
        print("  - {0}".format(settingsDir))
        answer = "c"
        while answer not in ["y", "Y", "n", "N", ""]:
            answer = input("Shall this directory be removed (y/N)? ")
            # secok
        if answer in ["y", "Y"]:
            shutil.rmtree(settingsDir)


def getConfigDir():
    """
    Module function to get the name of the directory storing the config data.
    
    @return directory name of the config dir (string)
    """
    cdn = ".eric6"
    return os.path.join(os.path.expanduser("~"), cdn)


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
    # From http://stackoverflow.com/a/35286642
    import winreg
    try:
        registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0,
                                     winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(registryKey, name)
        winreg.CloseKey(registryKey)
        return value
    except WindowsError:
        return None


def windowsDesktopNames():
    """
    Function to generate the link names for the Windows Desktop.
    
    @return list of desktop link names
    @rtype list of str
    """
    majorVersion, minorVersion = sys.version_info[:2]
    linkTemplates = [
        "eric6 (Python {0}.{1}).lnk",
        "eric6 Browser (Python {0}.{1}).lnk",
    ]
    
    return [ll.format(majorVersion, minorVersion) for ll in linkTemplates]


def windowsProgramsEntry():
    """
    Function to generate the name of the Start Menu top entry.
    
    @return name of the Start Menu top entry
    @rtype str
    """
    majorVersion, minorVersion = sys.version_info[:2]
    return "eric6 (Python {0}.{1})".format(majorVersion, minorVersion)


def main(argv):
    """
    The main function of the script.

    @param argv list of command line arguments
    """
    import getopt

    initGlobals()

    # Parse the command line.
    global progName
    progName = os.path.basename(argv[0])

    try:
        optlist, args = getopt.getopt(argv[1:], "hy")
    except getopt.GetoptError:
        usage()

    global platBinDir

    for opt, _arg in optlist:
        if opt == "-h":
            usage(0)
    
    print("\nUninstalling eric ...")
    uninstallEric()
    print("\nUninstallation complete.")
    print()
    
    exit(0)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit:
        raise
    except Exception:
        print("""An internal error occured.  Please report all the output of"""
              """ the program,\n"""
              """including the following traceback, to"""
              """ eric-bugs@eric-ide.python-projects.org.\n""")
        raise

#
# eflag: noqa = M801
