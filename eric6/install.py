#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#
# This is the install script for eric.

"""
Installation script for the eric IDE and all eric related tools.
"""

import sys
import os
import re
import compileall
import py_compile
import glob
import shutil
import fnmatch
import subprocess               # secok
import time
import io
import json
import shlex
import datetime
import getpass

# Define the globals.
progName = None
currDir = os.getcwd()
modDir = None
pyModDir = None
platBinDir = None
platBinDirOld = None
distDir = None
apisDir = None
installApis = True
doCleanup = True
doCleanDesktopLinks = False
forceCleanDesktopLinks = False
doCompile = True
yes2All = False
ignorePyqt5Tools = False
cfg = {}
progLanguages = ["Python", "Ruby", "QSS"]
sourceDir = "eric"
eric6SourceDir = os.path.join(sourceDir, "eric6")
configName = 'eric6config.py'
defaultMacAppBundleName = "eric6.app"
defaultMacAppBundlePath = "/Applications"
defaultMacPythonExe = "{0}/Resources/Python.app/Contents/MacOS/Python".format(
    sys.exec_prefix)
if not os.path.exists(defaultMacPythonExe):
    defaultMacPythonExe = ""
macAppBundleName = defaultMacAppBundleName
macAppBundlePath = defaultMacAppBundlePath
macPythonExe = defaultMacPythonExe

createInstallInfoFile = True
installInfoName = "eric6install.json"
installInfo = {}
installCwd = ""

# Define blacklisted versions of the prerequisites
BlackLists = {
    "sip": [],
    "PyQt5": [],
    "QScintilla2": [],
}
PlatformsBlackLists = {
    "windows": {
        "sip": [],
        "PyQt5": [],
        "QScintilla2": [],
    },
    
    "linux": {
        "sip": [],
        "PyQt5": [],
        "QScintilla2": [],
    },
    
    "mac": {
        "sip": [],
        "PyQt5": [],
        "QScintilla2": [],
    },
}


def exit(rcode=0):
    """
    Exit the install script.
    
    @param rcode result code to report back (integer)
    """
    global currDir
    
    print()
    
    if sys.platform.startswith(("win", "cygwin")):
        try:
            input("Press enter to continue...")             # secok
        except (EOFError, SyntaxError):
            pass
    
    os.chdir(currDir)
    
    sys.exit(rcode)


def usage(rcode=2):
    """
    Display a usage message and exit.

    @param rcode the return code passed back to the calling process.
    """
    global progName, modDir, distDir, apisDir
    global macAppBundleName, macAppBundlePath, macPythonExe

    print()
    print("Usage:")
    if sys.platform == "darwin":
        print("    {0} [-chxz] [-a dir] [-b dir] [-d dir] [-f file] [-i dir]"
              " [-m name] [-n path] [-p python] [--no-apis] [--no-info]"
              " [--yes]"
              .format(progName))
    elif sys.platform.startswith(("win", "cygwin")):
        print("    {0} [-chxz] [-a dir] [-b dir] [-d dir] [-f file]"
              " [--clean-desktop] [--no-apis] [--no-info] [--no-tools] [--yes]"
              .format(progName))
    else:
        print("    {0} [-chxz] [-a dir] [-b dir] [-d dir] [-f file] [-i dir]"
              " [--no-apis] [--no-info] [--no-tools] [--yes]"
              .format(progName))
    print("where:")
    print("    -h, --help display this help message")
    print("    -a dir     where the API files will be installed")
    if apisDir:
        print("               (default: {0})".format(apisDir))
    else:
        print("               (no default value)")
    print("    --no-apis  don't install API files")
    print("    -b dir     where the binaries will be installed")
    print("               (default: {0})".format(platBinDir))
    print("    -d dir     where eric python files will be installed")
    print("               (default: {0})".format(modDir))
    print("    -f file    configuration file naming the various installation"
          " paths")
    if not sys.platform.startswith(("win", "cygwin")):
        print("    -i dir     temporary install prefix")
        print("               (default: {0})".format(distDir))
    if sys.platform == "darwin":
        print("    -m name    name of the Mac app bundle")
        print("               (default: {0})".format(macAppBundleName))
        print("    -n path    path of the directory the Mac app bundle will")
        print("               be created in")
        print("               (default: {0})".format(macAppBundlePath))
        print("    -p python  path of the python executable")
        print("               (default: {0})".format(macPythonExe))
    print("    -c         don't cleanup old installation first")
    if sys.platform.startswith(("win", "cygwin")):
        print("    --clean-desktop delete desktop links before installation")
    print("    --no-info  don't create the install info file")
    if sys.platform != "darwin":
        print("    --no-tools don't ask for installation of pyqt5-tools"
              "/qt5-applications")
    print("    -x         don't perform dependency checks (use on your own"
          " risk)")
    print("    -z         don't compile the installed python files")
    print("    --yes      answer 'yes' to all questions")
    print()
    print("The file given to the -f option must be valid Python code"
          " defining a")
    print("dictionary called 'cfg' with the keys 'ericDir', 'ericPixDir',"
          " 'ericIconDir',")
    print("'ericDTDDir', 'ericCSSDir', 'ericStylesDir', 'ericDocDir',"
          " 'ericExamplesDir',")
    print("'ericTranslationsDir', 'ericTemplatesDir', 'ericCodeTemplatesDir',")
    print("'ericOthersDir','bindir', 'mdir' and 'apidir.")
    print("These define the directories for the installation of the various"
          " parts of eric.")

    exit(rcode)


def initGlobals():
    """
    Module function to set the values of globals that need more than a
    simple assignment.
    """
    global platBinDir, modDir, pyModDir, apisDir, platBinDirOld
    
    try:
        import distutils.sysconfig
    except ImportError:
        print("Please install the 'distutils' package first.")
        exit(5)
    
    if sys.platform.startswith(("win", "cygwin")):
        platBinDir = sys.exec_prefix
        if platBinDir.endswith("\\"):
            platBinDir = platBinDir[:-1]
        platBinDirOld = platBinDir
        platBinDir = os.path.join(platBinDir, "Scripts")
        if not os.path.exists(platBinDir):
            platBinDir = platBinDirOld
    else:
        pyBinDir = os.path.normpath(os.path.dirname(sys.executable))
        if os.access(pyBinDir, os.W_OK):
            # install the eric scripts along the python executable
            platBinDir = pyBinDir
        else:
            # install them in the user's bin directory
            platBinDir = os.path.expanduser("~/bin")
        if (
            platBinDir != "/usr/local/bin" and
            os.access("/usr/local/bin", os.W_OK)
        ):
            platBinDirOld = "/usr/local/bin"

    modDir = distutils.sysconfig.get_python_lib(True)
    pyModDir = modDir
    
    pyqtDataDir = os.path.join(modDir, "PyQt5")
    if os.path.exists(os.path.join(pyqtDataDir, "qsci")):
        # it's the installer
        qtDataDir = pyqtDataDir
    elif os.path.exists(os.path.join(pyqtDataDir, "Qt", "qsci")):
        # it's the wheel
        qtDataDir = os.path.join(pyqtDataDir, "Qt")
    else:
        # determine dynamically
        try:
            from PyQt5.QtCore import QLibraryInfo
            qtDataDir = QLibraryInfo.location(QLibraryInfo.DataPath)
        except ImportError:
            qtDataDir = None
    if qtDataDir:
        apisDir = os.path.join(qtDataDir, "qsci", "api")
    else:
        apisDir = None


def copyToFile(name, text):
    """
    Copy a string to a file.

    @param name the name of the file.
    @param text the contents to copy to the file.
    """
    with open(name, "w") as f:
        f.write(text)


def copyDesktopFile(src, dst):
    """
    Modify a desktop file and write it to its destination.
    
    @param src source file name (string)
    @param dst destination file name (string)
    """
    global cfg, platBinDir
    
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = text.replace("@BINDIR@", platBinDir)
    text = text.replace("@MARKER@", "")
    text = text.replace("@PY_MARKER@", "")
    
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(dst, 0o644)


def copyAppStreamFile(src, dst):
    """
    Modify an appstream file and write it to its destination.
    
    @param src source file name (string)
    @param dst destination file name (string)
    """
    if os.path.exists(os.path.join("eric", "eric6", "UI", "Info.py")):
        # Installing from archive
        from eric.eric6.UI.Info import Version
    elif os.path.exists(os.path.join("eric6", "UI", "Info.py")):
        # Installing from source tree
        from eric6.UI.Info import Version
    else:
        Version = "Unknown"
    
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    
    text = (
        text.replace("@MARKER@", "")
        .replace("@VERSION@", Version.split(None, 1)[0])
        .replace("@DATE@", time.strftime("%Y-%m-%d"))
    )
    
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    os.chmod(dst, 0o644)


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


def createPyWrapper(pydir, wfile, saveDir, isGuiScript=True):
    """
    Create an executable wrapper for a Python script.

    @param pydir the name of the directory where the Python script will
        eventually be installed (string)
    @param wfile the basename of the wrapper (string)
    @param saveDir directory to save the file into (string)
    @param isGuiScript flag indicating a wrapper script for a GUI
        application (boolean)
    @return the platform specific name of the wrapper (string)
    """
    # all kinds of Windows systems
    if sys.platform.startswith(("win", "cygwin")):
        wname = wfile + ".cmd"
        if isGuiScript:
            wrapper = (
                '''@echo off\n'''
                '''start "" "{2}\\pythonw.exe"'''
                ''' "{0}\\{1}.pyw"'''
                ''' %1 %2 %3 %4 %5 %6 %7 %8 %9\n'''.format(
                    pydir, wfile, os.path.dirname(sys.executable))
            )
        else:
            wrapper = (
                '''@"{0}" "{1}\\{2}.py"'''
                ''' %1 %2 %3 %4 %5 %6 %7 %8 %9\n'''.format(
                    sys.executable, pydir, wfile)
            )

    # Mac OS X
    elif sys.platform == "darwin":
        major = sys.version_info.major
        pyexec = "{0}/bin/pythonw{1}".format(sys.exec_prefix, major)
        if not os.path.exists(pyexec):
            pyexec = "{0}/bin/python{1}".format(sys.exec_prefix, major)
        wname = wfile
        wrapper = ('''#!/bin/sh\n'''
                   '''\n'''
                   '''exec "{0}" "{1}/{2}.py" "$@"\n'''
                   .format(pyexec, pydir, wfile))

    # *nix systems
    else:
        wname = wfile
        wrapper = ('''#!/bin/sh\n'''
                   '''\n'''
                   '''exec "{0}" "{1}/{2}.py" "$@"\n'''
                   .format(sys.executable, pydir, wfile))
    
    wname = os.path.join(saveDir, wname)
    copyToFile(wname, wrapper)
    os.chmod(wname, 0o755)                  # secok

    return wname


def copyTree(src, dst, filters, excludeDirs=None, excludePatterns=None):
    """
    Copy Python, translation, documentation, wizards configuration,
    designer template files and DTDs of a directory tree.
    
    @param src name of the source directory
    @param dst name of the destination directory
    @param filters list of filter pattern determining the files to be copied
    @param excludeDirs list of (sub)directories to exclude from copying
    @param excludePatterns list of filter pattern determining the files to
        be skipped
    """
    if excludeDirs is None:
        excludeDirs = []
    if excludePatterns is None:
        excludePatterns = []
    try:
        names = os.listdir(src)
    except OSError:
        # ignore missing directories (most probably the i18n directory)
        return
    
    for name in names:
        skipIt = False
        for excludePattern in excludePatterns:
            if fnmatch.fnmatch(name, excludePattern):
                skipIt = True
                break
        if not skipIt:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            for fileFilter in filters:
                if fnmatch.fnmatch(srcname, fileFilter):
                    if not os.path.isdir(dst):
                        os.makedirs(dst)
                    shutil.copy2(srcname, dstname)
                    os.chmod(dstname, 0o644)
                    break
            else:
                if os.path.isdir(srcname) and srcname not in excludeDirs:
                    copyTree(srcname, dstname, filters,
                             excludePatterns=excludePatterns)


def createGlobalPluginsDir():
    """
    Create the global plugins directory, if it doesn't exist.
    """
    global cfg, distDir
    
    pdir = os.path.join(cfg['mdir'], "eric6plugins")
    fname = os.path.join(pdir, "__init__.py")
    if not os.path.exists(fname):
        if not os.path.exists(pdir):
            os.mkdir(pdir, 0o755)
        with open(fname, "w") as f:
            f.write(
                '''# -*- coding: utf-8 -*-

"""
Package containing the global plugins.
"""
'''
            )
        os.chmod(fname, 0o644)


def cleanupSource(dirName):
    """
    Cleanup the sources directory to get rid of leftover files
    and directories.
    
    @param dirName name of the directory to prune (string)
    """
    # step 1: delete all Ui_*.py files without a corresponding
    #         *.ui file
    dirListing = os.listdir(dirName)
    for formName, sourceName in [
        (f.replace('Ui_', "").replace(".py", ".ui"), f)
            for f in dirListing if fnmatch.fnmatch(f, "Ui_*.py")]:
        if not os.path.exists(os.path.join(dirName, formName)):
            os.remove(os.path.join(dirName, sourceName))
            if os.path.exists(os.path.join(dirName, sourceName + "c")):
                os.remove(os.path.join(dirName, sourceName + "c"))
    
    # step 2: delete the __pycache__ directory and all remaining *.pyc files
    if os.path.exists(os.path.join(dirName, "__pycache__")):
        shutil.rmtree(os.path.join(dirName, "__pycache__"))
    for name in [f for f in os.listdir(dirName)
                 if fnmatch.fnmatch(f, "*.pyc")]:
        os.remove(os.path.join(dirName, name))
    
    # step 3: delete *.orig files
    for name in [f for f in os.listdir(dirName)
                 if fnmatch.fnmatch(f, "*.orig")]:
        os.remove(os.path.join(dirName, name))
    
    # step 4: descent into subdirectories and delete them if empty
    for name in os.listdir(dirName):
        name = os.path.join(dirName, name)
        if os.path.isdir(name):
            cleanupSource(name)
            if len(os.listdir(name)) == 0:
                os.rmdir(name)


def cleanUp():
    """
    Uninstall the old eric files.
    """
    global platBinDir, platBinDirOld
    
    try:
        from eric6config import getConfig
    except ImportError:
        # eric wasn't installed previously
        return
    except SyntaxError:
        # an incomplete or old config file was found
        return
    
    global pyModDir, progLanguages
    
    # Remove the menu entry for Linux systems
    if sys.platform.startswith("linux"):
        cleanUpLinuxSpecifics()
    # Remove the Desktop and Start Menu entries for Windows systems
    elif sys.platform.startswith(("win", "cygwin")):
        cleanUpWindowsLinks()
    
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
        dirs = [platBinDir, getConfig('bindir')]
        if platBinDirOld:
            dirs.append(platBinDirOld)
        for rem_wname in rem_wnames:
            for d in dirs:
                for rwname in wrapperNames(d, rem_wname):
                    if os.path.exists(rwname):
                        os.remove(rwname)
        
        # Cleanup our config file(s)
        for name in ['eric6config.py', 'eric6config.pyc', 'eric6.pth']:
            e6cfile = os.path.join(pyModDir, name)
            if os.path.exists(e6cfile):
                os.remove(e6cfile)
            e6cfile = os.path.join(pyModDir, "__pycache__", name)
            path, ext = os.path.splitext(e6cfile)
            for f in glob.glob("{0}.*{1}".format(path, ext)):
                os.remove(f)
            
        # Cleanup the install directories
        for name in ['ericExamplesDir', 'ericDocDir', 'ericDTDDir',
                     'ericCSSDir', 'ericIconDir', 'ericPixDir',
                     'ericTemplatesDir', 'ericCodeTemplatesDir',
                     'ericOthersDir', 'ericStylesDir', 'ericDir']:
            if os.path.exists(getConfig(name)):
                shutil.rmtree(getConfig(name), True)
        
        # Cleanup translations
        for name in glob.glob(
                os.path.join(getConfig('ericTranslationsDir'), 'eric6_*.qm')):
            if os.path.exists(name):
                os.remove(name)
        
        # Cleanup API files
        try:
            apidir = getConfig('apidir')
            for progLanguage in progLanguages:
                for name in getConfig('apis'):
                    apiname = os.path.join(apidir, progLanguage.lower(), name)
                    if os.path.exists(apiname):
                        os.remove(apiname)
                for apiname in glob.glob(
                        os.path.join(apidir, progLanguage.lower(), "*.bas")):
                    if os.path.basename(apiname) != "eric6.bas":
                        os.remove(apiname)
        except AttributeError:
            pass
        
        if sys.platform == "darwin":
            # delete the Mac app bundle
            cleanUpMacAppBundle()
    except OSError as msg:
        sys.stderr.write(
            'Error: {0}\nTry install with admin rights.\n'.format(msg))
        exit(7)


def cleanUpLinuxSpecifics():
    """
    Clean up Linux specific files.
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


def cleanUpMacAppBundle():
    """
    Uninstall the macOS application bundle.
    """
    from eric6config import getConfig
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


def cleanUpWindowsLinks():
    """
    Clean up the Desktop and Start Menu entries for Windows.
    """
    global doCleanDesktopLinks, forceCleanDesktopLinks
    
    try:
        from pywintypes import com_error        # __IGNORE_WARNING__
    except ImportError:
        # links were not created by install.py
        return
    
    regPath = (
        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" +
        "\\User Shell Folders"
    )
    
    if doCleanDesktopLinks or forceCleanDesktopLinks:
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


def shutilCopy(src, dst, perm=0o644):
    """
    Wrapper function around shutil.copy() to ensure the permissions.
    
    @param src source file name (string)
    @param dst destination file name or directory name (string)
    @param perm permissions to be set (integer)
    """
    shutil.copy(src, dst)
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    os.chmod(dst, perm)


def installEric():
    """
    Actually perform the installation steps.
    
    @return result code (integer)
    """
    global distDir, doCleanup, cfg, progLanguages, sourceDir, configName
    global installApis
    
    # Create the platform specific wrappers.
    scriptsDir = "install_scripts"
    if not os.path.isdir(scriptsDir):
        os.mkdir(scriptsDir)
    wnames = []
    for name in ["eric6_api", "eric6_doc"]:
        wnames.append(createPyWrapper(cfg['ericDir'], name, scriptsDir, False))
    for name in ["eric6_compare", "eric6_configure", "eric6_diff",
                 "eric6_editor", "eric6_hexeditor", "eric6_iconeditor",
                 "eric6_plugininstall", "eric6_pluginrepository",
                 "eric6_pluginuninstall", "eric6_qregularexpression",
                 "eric6_re", "eric6_snap", "eric6_sqlbrowser", "eric6_tray",
                 "eric6_trpreviewer", "eric6_uipreviewer", "eric6_unittest",
                 "eric6_browser", "eric6_shell", "eric6"]:
        wnames.append(createPyWrapper(cfg['ericDir'], name, scriptsDir))
    
    # set install prefix, if not None
    if distDir:
        for key in list(cfg.keys()):
            cfg[key] = os.path.normpath(
                os.path.join(distDir, cfg[key].lstrip(os.sep)))
    
    try:
        # Install the files
        # make the install directories
        for key in cfg.keys():
            if cfg[key] and not os.path.isdir(cfg[key]):
                os.makedirs(cfg[key])
        
        # copy the eric config file
        if distDir:
            shutilCopy(configName, cfg['mdir'])
            if os.path.exists(configName + 'c'):
                shutilCopy(configName + 'c', cfg['mdir'])
        else:
            shutilCopy(configName, modDir)
            if os.path.exists(configName + 'c'):
                shutilCopy(configName + 'c', modDir)
        
        # copy the various parts of eric
        copyTree(
            eric6SourceDir, cfg['ericDir'],
            ['*.py', '*.pyc', '*.pyo', '*.pyw'],
            [os.path.join(sourceDir, "Examples"),
             os.path.join(sourceDir, ".ropeproject")],
            excludePatterns=["eric6config.py*"])
        copyTree(
            os.path.join(eric6SourceDir, "Plugins"),
            os.path.join(cfg['ericDir'], "Plugins"),
            ['*.svgz', '*.svg', '*.png', '*.style', '*.tmpl', '*.txt'])
        copyTree(
            os.path.join(eric6SourceDir, "Documentation"),
            cfg['ericDocDir'],
            ['*.html', '*.qch'])
        copyTree(
            os.path.join(eric6SourceDir, "CSSs"),
            cfg['ericCSSDir'],
            ['*.css'])
        copyTree(
            os.path.join(eric6SourceDir, "Styles"),
            cfg['ericStylesDir'],
            ['*.qss', '*.e4h', '*.e6h', '*.ehj'])
        copyTree(
            os.path.join(eric6SourceDir, "i18n"),
            cfg['ericTranslationsDir'],
            ['*.qm'])
        copyTree(
            os.path.join(eric6SourceDir, "icons"),
            cfg['ericIconDir'],
            ['*.svgz', '*.svg', '*.png', 'LICENSE*.*', 'readme.txt'])
        copyTree(
            os.path.join(eric6SourceDir, "pixmaps"),
            cfg['ericPixDir'],
            ['*.svgz', '*.svg', '*.png', '*.xpm', '*.ico', '*.gif'])
        copyTree(
            os.path.join(eric6SourceDir, "DesignerTemplates"),
            cfg['ericTemplatesDir'],
            ['*.tmpl'])
        copyTree(
            os.path.join(eric6SourceDir, "CodeTemplates"),
            cfg['ericCodeTemplatesDir'],
            ['*.tmpl'])
        
        # copy some data files needed at various places
        copyTree(
            os.path.join(eric6SourceDir, "E5Network", "data"),
            os.path.join(cfg['ericDir'], "E5Network", "data"),
            ['*.dat', '*.txt'])
        copyTree(
            os.path.join(eric6SourceDir, "IconEditor", "cursors"),
            os.path.join(cfg['ericDir'], "IconEditor", "cursors"),
            ['*.xpm'])
        copyTree(
            os.path.join(eric6SourceDir, "UI", "data"),
            os.path.join(cfg['ericDir'], "UI", "data"),
            ['*.css'])
        copyTree(
            os.path.join(eric6SourceDir, "WebBrowser"),
            os.path.join(cfg['ericDir'], "WebBrowser"),
            ['*.xbel', '*.xml', '*.html', '*.png', '*.gif', '*.js'])
        
        # copy the wrappers
        for wname in wnames:
            shutilCopy(wname, cfg['bindir'], perm=0o755)
            os.remove(wname)
        shutil.rmtree(scriptsDir)
        
        # copy the license file
        shutilCopy(os.path.join(sourceDir, "docs", "LICENSE.GPL3"),
                   cfg['ericDir'])
        
        # create the global plugins directory
        createGlobalPluginsDir()
        
    except OSError as msg:
        sys.stderr.write(
            'Error: {0}\nTry install with admin rights.\n'.format(msg))
        return(7)
    
    # copy some text files to the doc area
    for name in ["LICENSE.GPL3", "THANKS", "changelog"]:
        try:
            shutilCopy(os.path.join(sourceDir, "docs", name),
                       cfg['ericDocDir'])
        except OSError:
            print("Could not install '{0}'.".format(
                os.path.join(sourceDir, "docs", name)))
    for name in glob.glob(os.path.join(sourceDir, 'docs', 'README*.*')):
        try:
            shutilCopy(name, cfg['ericDocDir'])
        except OSError:
            print("Could not install '{0}'.".format(name))
   
    # copy some more stuff
    for name in ('default.ekj', 'default_Mac.ekj',
                 'default.e4k', 'default_Mac.e4k'):
        try:
            shutilCopy(os.path.join(sourceDir, "others", name),
                       cfg['ericOthersDir'])
        except OSError:
            print("Could not install '{0}'.".format(
                os.path.join(sourceDir, "others", name)))
    
    # install the API file
    if installApis:
        for progLanguage in progLanguages:
            apidir = os.path.join(cfg['apidir'], progLanguage.lower())
            print("Installing {0} API files to '{1}'.".format(
                progLanguage, apidir))
            if not os.path.exists(apidir):
                os.makedirs(apidir)
            for apiName in glob.glob(os.path.join(eric6SourceDir, "APIs",
                                                  progLanguage, "*.api")):
                try:
                    shutilCopy(apiName, apidir)
                except OSError:
                    print("Could not install '{0}' (no permission)."
                          .format(apiName))
            for apiName in glob.glob(os.path.join(eric6SourceDir, "APIs",
                                                  progLanguage, "*.bas")):
                try:
                    shutilCopy(apiName, apidir)
                except OSError:
                    print("Could not install '{0}' (no permission)."
                          .format(apiName))
            if progLanguage == "Python":
                # copy Python3 API files to the same destination
                for apiName in glob.glob(os.path.join(eric6SourceDir, "APIs",
                                                      "Python3", "*.api")):
                    try:
                        shutilCopy(apiName, apidir)
                    except OSError:
                        print("Could not install '{0}' (no permission)."
                              .format(apiName))
                for apiName in glob.glob(os.path.join(eric6SourceDir, "APIs",
                                                      "Python3", "*.bas")):
                    if os.path.exists(os.path.join(
                        apidir, os.path.basename(
                            apiName.replace(".bas", ".api")))):
                        try:
                            shutilCopy(apiName, apidir)
                        except OSError:
                            print("Could not install '{0}' (no permission)."
                                  .format(apiName))
                
                # copy MicroPython API files to the same destination
                for apiName in glob.glob(os.path.join(eric6SourceDir, "APIs",
                                                      "MicroPython", "*.api")):
                    try:
                        shutilCopy(apiName, apidir)
                    except OSError:
                        print("Could not install '{0}' (no permission)."
                              .format(apiName))
                for apiName in glob.glob(os.path.join(eric6SourceDir, "APIs",
                                                      "MicroPython", "*.bas")):
                    if os.path.exists(os.path.join(
                        apidir, os.path.basename(
                            apiName.replace(".bas", ".api")))):
                        try:
                            shutilCopy(apiName, apidir)
                        except OSError:
                            print("Could not install '{0}' (no permission)."
                                  .format(apiName))
    
    # Create menu entry for Linux systems
    if sys.platform.startswith("linux"):
        createLinuxSpecifics()
    
    # Create Desktop and Start Menu entries for Windows systems
    elif sys.platform.startswith(("win", "cygwin")):
        createWindowsLinks()
    
    # Create a Mac application bundle
    elif sys.platform == "darwin":
        createMacAppBundle(cfg['ericDir'])
    
    return 0


def createLinuxSpecifics():
    """
    Install Linux specific files.
    """
    global distDir, sourceDir
    
    if distDir:
        dst = os.path.normpath(os.path.join(distDir, "usr/share/pixmaps"))
        if not os.path.exists(dst):
            os.makedirs(dst)
        shutilCopy(
            os.path.join(eric6SourceDir, "pixmaps", "eric_icon.png"),
            os.path.join(dst, "eric.png"))
        shutilCopy(
            os.path.join(eric6SourceDir, "pixmaps", "ericWeb48_icon.png"),
            os.path.join(dst, "ericWeb.png"))
        dst = os.path.normpath(
            os.path.join(distDir, "usr/share/applications"))
        if not os.path.exists(dst):
            os.makedirs(dst)
        copyDesktopFile(os.path.join(sourceDir, "linux", "eric6.desktop.in"),
                        os.path.join(dst, "eric6.desktop"))
        copyDesktopFile(
            os.path.join(sourceDir, "linux", "eric6_browser.desktop.in"),
            os.path.join(dst, "eric6_browser.desktop"))
        dst = os.path.normpath(
            os.path.join(distDir, "usr/share/metainfo"))
        if not os.path.exists(dst):
            os.makedirs(dst)
        copyAppStreamFile(
            os.path.join(sourceDir, "linux", "eric6.appdata.xml.in"),
            os.path.join(dst, "eric6.appdata.xml"))
    elif os.getuid() == 0:
        shutilCopy(
            os.path.join(eric6SourceDir, "pixmaps", "eric_icon.png"),
            "/usr/share/pixmaps/eric.png")
        copyDesktopFile(
            os.path.join(sourceDir, "linux", "eric6.desktop.in"),
            "/usr/share/applications/eric6.desktop")
        if os.path.exists("/usr/share/metainfo"):
            copyAppStreamFile(
                os.path.join(sourceDir, "linux", "eric6.appdata.xml.in"),
                "/usr/share/metainfo/eric6.appdata.xml")
        elif os.path.exists("/usr/share/appdata"):
            copyAppStreamFile(
                os.path.join(sourceDir, "linux", "eric6.appdata.xml.in"),
                "/usr/share/appdata/eric6.appdata.xml")
        shutilCopy(
            os.path.join(eric6SourceDir, "pixmaps", "ericWeb48_icon.png"),
            "/usr/share/pixmaps/ericWeb.png")
        copyDesktopFile(
            os.path.join(sourceDir, "linux", "eric6_browser.desktop.in"),
            "/usr/share/applications/eric6_browser.desktop")
    elif os.getuid() >= 1000:
        # it is assumed, that user ids start at 1000
        localPath = os.path.join(os.path.expanduser("~"),
                                 ".local", "share")
        # create directories first
        for directory in [os.path.join(localPath, name)
                          for name in ("pixmaps", "applications",
                                       "metainfo", "appdata")]:
            if not os.path.isdir(directory):
                os.makedirs(directory)
        # now copy the files
        shutilCopy(
            os.path.join(eric6SourceDir, "pixmaps", "eric_icon.png"),
            os.path.join(localPath, "pixmaps", "eric.png"))
        copyDesktopFile(
            os.path.join(sourceDir, "linux", "eric6.desktop.in"),
            os.path.join(localPath, "applications", "eric6.desktop"))
        copyAppStreamFile(
            os.path.join(sourceDir, "linux", "eric6.appdata.xml.in"),
            os.path.join(localPath, "metainfo", "eric6.appdata.xml"))
        copyAppStreamFile(
            os.path.join(sourceDir, "linux", "eric6.appdata.xml.in"),
            os.path.join(localPath, "appdata", "eric6.appdata.xml"))
        shutilCopy(
            os.path.join(eric6SourceDir, "pixmaps", "ericWeb48_icon.png"),
            os.path.join(localPath, "pixmaps", "ericWeb.png"))
        copyDesktopFile(
            os.path.join(sourceDir, "linux", "eric6_browser.desktop.in"),
            os.path.join(localPath, "applications", "eric6_browser.desktop"))


def createWindowsLinks():
    """
    Create Desktop and Start Menu links.
    """
    try:
        # check, if pywin32 is available
        from win32com.client import Dispatch    # __IGNORE_WARNING__
    except ImportError:
        installed = pipInstall(
            "pywin32",
            "\nThe Python package 'pywin32' could not be imported."
        )
        if installed:
            # create the links via an external script to get around some
            # startup magic done by pywin32.pth
            args = [
                sys.executable,
                os.path.join(os.path.dirname(__file__),
                             "create_windows_links.py"),
            ]
            subprocess.call(args)               # secok
        else:
            print(
                "\nThe Python package 'pywin32' is not installed. Desktop and"
                " Start Menu entries will not be created."
            )
        return
    
    regPath = (
        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" +
        "\\User Shell Folders"
    )
    
    # 1. create desktop shortcuts
    regName = "Desktop"
    desktopEntry = getWinregEntry(regName, regPath)
    if desktopEntry:
        desktopFolder = os.path.normpath(os.path.expandvars(desktopEntry))
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


def createMacAppBundle(pydir):
    """
    Create a Mac application bundle.

    @param pydir the name of the directory where the Python script will
        eventually be installed
    @type str
    """
    global cfg, macAppBundleName, macPythonExe, macAppBundlePath
    
    directories = {
        "contents": "{0}/{1}/Contents/".format(
            macAppBundlePath, macAppBundleName),
        "exe": "{0}/{1}/Contents/MacOS".format(
            macAppBundlePath, macAppBundleName),
        "icns": "{0}/{1}/Contents/Resources".format(
            macAppBundlePath, macAppBundleName)
    }
    for directory in directories.values():
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    if macPythonExe == defaultMacPythonExe and macPythonExe:
        starter = os.path.join(directories["exe"], "eric")
        os.symlink(macPythonExe, starter)
    else:
        starter = "python{0}".format(sys.version_info.major)
    
    wname = os.path.join(directories["exe"], "eric6")
    
    # determine entry for DYLD_FRAMEWORK_PATH
    dyldLine = ""
    try:
        from PyQt5.QtCore import QLibraryInfo
        qtLibraryDir = QLibraryInfo.location(QLibraryInfo.LibrariesPath)
    except ImportError:
        qtLibraryDir = ""
    if qtLibraryDir:
        dyldLine = "DYLD_FRAMEWORK_PATH={0}\n".format(qtLibraryDir)
    
    # determine entry for PATH
    pathLine = ""
    path = os.getenv("PATH", "")
    if path:
        pybin = os.path.join(sys.exec_prefix, "bin")
        pathlist = path.split(os.pathsep)
        pathlist_n = [pybin]
        for path_ in pathlist:
            if path_ and path_ not in pathlist_n:
                pathlist_n.append(path_)
        pathLine = "PATH={0}\n".format(os.pathsep.join(pathlist_n))
    
    # create the wrapper script
    wrapper = ('''#!/bin/sh\n'''
               '''\n'''
               '''{0}'''
               '''{1}'''
               '''exec "{2}" "{3}/{4}.py" "$@"\n'''
               .format(pathLine, dyldLine, starter, pydir, "eric6"))
    copyToFile(wname, wrapper)
    os.chmod(wname, 0o755)                  # secok
    
    shutilCopy(os.path.join(eric6SourceDir, "pixmaps", "eric_2.icns"),
               os.path.join(directories["icns"], "eric.icns"))
    
    if os.path.exists(os.path.join("eric", "eric6", "UI", "Info.py")):
        # Installing from archive
        from eric.eric6.UI.Info import Version, CopyrightShort
    elif os.path.exists(os.path.join("eric6", "UI", "Info.py")):
        # Installing from source tree
        from eric6.UI.Info import Version, CopyrightShort
    else:
        Version = "Unknown"
        CopyrightShort = "(c) 2002 - 2021 Detlev Offenbach"
    
    copyToFile(
        os.path.join(directories["contents"], "Info.plist"),
        '''<?xml version="1.0" encoding="UTF-8"?>\n'''
        '''<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"\n'''
        '''          "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'''
        '''<plist version="1.0">\n'''
        '''<dict>\n'''
        '''    <key>CFBundleExecutable</key>\n'''
        '''    <string>eric6</string>\n'''
        '''    <key>CFBundleIconFile</key>\n'''
        '''    <string>eric.icns</string>\n'''
        '''    <key>CFBundleInfoDictionaryVersion</key>\n'''
        '''    <string>{1}</string>\n'''
        '''    <key>CFBundleName</key>\n'''
        '''    <string>{0}</string>\n'''
        '''    <key>CFBundleDisplayName</key>\n'''
        '''    <string>{0}</string>\n'''
        '''    <key>CFBundlePackageType</key>\n'''
        '''    <string>APPL</string>\n'''
        '''    <key>CFBundleSignature</key>\n'''
        '''    <string>ERIC-IDE</string>\n'''
        '''    <key>CFBundleVersion</key>\n'''
        '''    <string>{1}</string>\n'''
        '''    <key>CFBundleGetInfoString</key>\n'''
        '''    <string>{1}, {2}</string>\n'''
        '''    <key>CFBundleIdentifier</key>\n'''
        '''    <string>org.python-projects.eric-ide</string>\n'''
        '''    <key>NSRequiresAquaSystemAppearance</key>\n'''
        '''    <string>false</string>\n'''
        '''</dict>\n'''
        '''</plist>\n'''.format(
            macAppBundleName.replace(".app", ""),
            Version.split(None, 1)[0],
            CopyrightShort))


def createInstallConfig():
    """
    Create the installation config dictionary.
    """
    global modDir, platBinDir, cfg, apisDir, installApis
        
    ericdir = os.path.join(modDir, "eric6")
    cfg = {
        'ericDir': ericdir,
        'ericPixDir': os.path.join(ericdir, "pixmaps"),
        'ericIconDir': os.path.join(ericdir, "icons"),
        'ericDTDDir': os.path.join(ericdir, "DTDs"),
        'ericCSSDir': os.path.join(ericdir, "CSSs"),
        'ericStylesDir': os.path.join(ericdir, "Styles"),
        'ericDocDir': os.path.join(ericdir, "Documentation"),
        'ericExamplesDir': os.path.join(ericdir, "Examples"),
        'ericTranslationsDir': os.path.join(ericdir, "i18n"),
        'ericTemplatesDir': os.path.join(ericdir, "DesignerTemplates"),
        'ericCodeTemplatesDir': os.path.join(ericdir, 'CodeTemplates'),
        'ericOthersDir': ericdir,
        'bindir': platBinDir,
        'mdir': modDir,
    }
    if installApis:
        if apisDir:
            cfg['apidir'] = apisDir
        else:
            cfg['apidir'] = os.path.join(ericdir, "api")
    else:
        cfg['apidir'] = ""
configLength = 15
    

def createConfig():
    """
    Create a config file with the respective config entries.
    """
    global cfg, macAppBundlePath, configName
    
    apis = []
    if installApis:
        for progLanguage in progLanguages:
            for apiName in sorted(
                glob.glob(os.path.join(eric6SourceDir, "APIs", progLanguage,
                                       "*.api"))):
                apis.append(os.path.basename(apiName))
            if progLanguage == "Python":
                # treat Python3 API files the same as Python API files
                for apiName in sorted(
                    glob.glob(os.path.join(eric6SourceDir, "APIs", "Python3",
                                           "*.api"))):
                    apis.append(os.path.basename(apiName))
                
                # treat MicroPython API files the same as Python API files
                for apiName in sorted(
                    glob.glob(os.path.join(eric6SourceDir, "APIs",
                                           "MicroPython", "*.api"))):
                    apis.append(os.path.basename(apiName))
    
    if sys.platform == "darwin":
        macConfig = (
            """    'macAppBundlePath': r'{0}',\n"""
            """    'macAppBundleName': r'{1}',\n"""
        ).format(macAppBundlePath, macAppBundleName)
    else:
        macConfig = ""
    config = (
        """# -*- coding: utf-8 -*-\n"""
        """#\n"""
        """# This module contains the configuration of the individual eric"""
        """ installation\n"""
        """#\n"""
        """\n"""
        """_pkg_config = {{\n"""
        """    'ericDir': r'{0}',\n"""
        """    'ericPixDir': r'{1}',\n"""
        """    'ericIconDir': r'{2}',\n"""
        """    'ericDTDDir': r'{3}',\n"""
        """    'ericCSSDir': r'{4}',\n"""
        """    'ericStylesDir': r'{5}',\n"""
        """    'ericDocDir': r'{6}',\n"""
        """    'ericExamplesDir': r'{7}',\n"""
        """    'ericTranslationsDir': r'{8}',\n"""
        """    'ericTemplatesDir': r'{9}',\n"""
        """    'ericCodeTemplatesDir': r'{10}',\n"""
        """    'ericOthersDir': r'{11}',\n"""
        """    'bindir': r'{12}',\n"""
        """    'mdir': r'{13}',\n"""
        """    'apidir': r'{14}',\n"""
        """    'apis': {15},\n"""
        """{16}"""
        """}}\n"""
        """\n"""
        """def getConfig(name):\n"""
        """    '''\n"""
        """    Module function to get a configuration value.\n"""
        """\n"""
        """    @param name name of the configuration value"""
        """    @type str\n"""
        """    @exception AttributeError raised to indicate an invalid"""
        """ config entry\n"""
        """    '''\n"""
        """    try:\n"""
        """        return _pkg_config[name]\n"""
        """    except KeyError:\n"""
        """        pass\n"""
        """\n"""
        """    raise AttributeError(\n"""
        """        '"{{0}}" is not a valid configuration value'"""
        """.format(name))\n"""
    ).format(
        cfg['ericDir'], cfg['ericPixDir'], cfg['ericIconDir'],
        cfg['ericDTDDir'], cfg['ericCSSDir'],
        cfg['ericStylesDir'], cfg['ericDocDir'],
        cfg['ericExamplesDir'], cfg['ericTranslationsDir'],
        cfg['ericTemplatesDir'],
        cfg['ericCodeTemplatesDir'], cfg['ericOthersDir'],
        cfg['bindir'], cfg['mdir'],
        cfg['apidir'], sorted(apis),
        macConfig,
    )
    copyToFile(configName, config)


def createInstallInfo():
    """
    Record information about the way eric was installed.
    """
    global createInstallInfoFile, installInfo, installCwd, cfg
    
    if createInstallInfoFile:
        installDateTime = datetime.datetime.now(tz=None)
        try:
            installInfo["sudo"] = os.getuid() == 0
        except AttributeError:
            installInfo["sudo"] = False
        installInfo["user"] = getpass.getuser()
        installInfo["exe"] = sys.executable
        installInfo["argv"] = " ".join(shlex.quote(a) for a in sys.argv[:])
        installInfo["install_cwd"] = installCwd
        installInfo["eric"] = cfg["ericDir"]
        installInfo["virtualenv"] = installInfo["eric"].startswith(
            os.path.expanduser("~"))
        installInfo["installed"] = True
        installInfo["installed_on"] = installDateTime.strftime(
            "%Y-%m-%d %H:%M:%S")
        installInfo["guessed"] = False
        installInfo["edited"] = False
        installInfo["pip"] = False
        installInfo["remarks"] = ""
        installInfo["install_cwd_edited"] = False
        installInfo["exe_edited"] = False
        installInfo["argv_edited"] = False
        installInfo["eric_edited"] = False


def pipInstall(packageName, message):
    """
    Install the given package via pip.
    
    @param packageName name of the package to be installed
    @type str
    @param message message to be shown to the user
    @type str
    @return flag indicating a successful installation
    @rtype bool
    """
    global yes2All
    
    ok = False
    if yes2All:
        answer = "y"
    else:
        print("{0}\n\nShall '{1}' be installed using pip? (Y/n)"
              .format(message, packageName), end=" ")
        answer = input()                            # secok
    if answer in ("", "Y", "y"):
        exitCode = subprocess.call(                 # secok
            [sys.executable, "-m", "pip", "install", packageName])
        ok = (exitCode == 0)
    
    return ok


def isPipOutdated():
    """
    Check, if pip is outdated.
    
    @return flag indicating an outdated pip
    @rtype bool
    """
    try:
        pipOut = subprocess.check_output([          # secok
            sys.executable, "-m", "pip", "list", "--outdated",
            "--format=json"
        ])
        pipOut = pipOut.decode()
    except (OSError, subprocess.CalledProcessError):
        pipOut = "[]"       # default empty list
    try:
        jsonList = json.loads(pipOut)
    except Exception:
        jsonList = []
    for package in jsonList:
        if isinstance(package, dict) and package["name"] == "pip":
            print("'pip' is outdated (installed {0}, available {1})".format(
                package["version"], package["latest_version"]
            ))
            return True
    
    return False


def updatePip():
    """
    Update the installed pip package.
    """
    global yes2All
    
    if yes2All:
        answer = "y"
    else:
        print("Shall 'pip' be updated (recommended)? (Y/n)", end=" ")
        answer = input()            # secok
    if answer in ("", "Y", "y"):
        subprocess.call(            # secok
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"])


def doDependancyChecks():
    """
    Perform some dependency checks.
    """
    try:
        isSudo = os.getuid() == 0
    except AttributeError:
        isSudo = False
    
    print('Checking dependencies')
    
    # update pip first even if we don't need to install anything
    if not isSudo and isPipOutdated():
        updatePip()
        print("\n")
    
    # perform dependency checks
    print("Python Version: {0:d}.{1:d}.{2:d}".format(*sys.version_info[:3]))
    if sys.version_info < (3, 6, 0):
        print('Sorry, you must have Python 3.6.0 or higher.')
        exit(5)
    
    try:
        import xml.etree            # __IGNORE_WARNING__
    except ImportError:
        print('Your Python installation is missing the XML module.')
        print('Please install it and try again.')
        exit(5)
    
    try:
        from PyQt5.QtCore import qVersion
    except ImportError as msg:
        installed = not isSudo and pipInstall(
            "PyQt5>=5.12.1,<5.15.2",
            "'PyQt5' could not be detected.\nError: {0}".format(msg)
        )
        if installed:
            # try to import it again
            try:
                from PyQt5.QtCore import qVersion
            except ImportError as msg:
                print('Sorry, please install PyQt5.')
                print('Error: {0}'.format(msg))
                exit(1)
        else:
            print('Sorry, please install PyQt5.')
            print('Error: {0}'.format(msg))
            exit(1)
    print("Found PyQt5")
    
    try:
        pyuic = "pyuic5"
        from PyQt5 import uic      # __IGNORE_WARNING__
    except ImportError as msg:
        print("Sorry, {0} is not installed.".format(pyuic))
        print('Error: {0}'.format(msg))
        exit(1)
    print("Found {0}".format(pyuic))
    
    try:
        from PyQt5 import QtWebEngineWidgets    # __IGNORE_WARNING__
    except ImportError as msg:
        from PyQt5.QtCore import PYQT_VERSION
        if PYQT_VERSION >= 0x050c00:
            # PyQt 5.12 separated QtWebEngine into a separate wheel
            if isSudo:
                print("Optional 'PyQtWebEngine' could not be detected.")
            else:
                pipInstall(
                    "PyQtWebEngine>=5.12.1,<5.15.2",
                    "Optional 'PyQtWebEngine' could not be detected.\n"
                    "Error: {0}".format(msg)
                )
    
    try:
        from PyQt5 import QtChart    # __IGNORE_WARNING__
    except ImportError as msg:
        if isSudo:
            print("Optional 'PyQtChart' could not be detected.")
        else:
            pipInstall(
                "PyQtChart>=5.12.1,<5.15.2",
                "Optional 'PyQtChart' could not be detected.\n"
                "Error: {0}".format(msg)
            )
    
    try:
        from PyQt5 import Qsci      # __IGNORE_WARNING__
    except ImportError as msg:
        installed = not isSudo and pipInstall(
            "QScintilla",
            "'QScintilla' could not be detected.\nError: {0}".format(msg)
        )
        if installed:
            # try to import it again
            try:
                from PyQt5 import Qsci      # __IGNORE_WARNING__
                message = None
            except ImportError as msg:
                message = str(msg)
        else:
            message = "QScintilla could not be installed."
        if message:
            print("Sorry, please install QScintilla2 and")
            print("its PyQt5 wrapper.")
            print('Error: {0}'.format(message))
            exit(1)
    print("Found QScintilla2")
    
    impModulesList = [
        "PyQt5.QtGui", "PyQt5.QtNetwork", "PyQt5.QtPrintSupport",
        "PyQt5.QtSql", "PyQt5.QtSvg", "PyQt5.QtWidgets",
    ]
    altModulesList = [
        # Tuple with alternatives, flag indicating it's ok to not be
        # available (e.g. for 32-Bit Windows)
        (("PyQt5.QtWebEngineWidgets", ), sys.maxsize <= 2**32),
    ]
    optionalModulesList = {
        # key is pip project name
        # value is tuple of package name, pip install constraint
        "PyYAML": ("yaml", ""),
        "toml": ("toml", ""),
    }
    # dict with tuples of package name and install constraint
    if sys.platform != "darwin" and not ignorePyqt5Tools:
        optionalModulesList["qt5-applications"] = ("qt5_applications",
                                                   "<5.15.2")
    
    # check mandatory modules
    modulesOK = True
    for impModule in impModulesList:
        name = impModule.split(".")[1]
        try:
            __import__(impModule)
            print("Found", name)
        except ImportError as msg:
            print('Sorry, please install {0}.'.format(name))
            print('Error: {0}'.format(msg))
            modulesOK = False
    if not modulesOK:
        exit(1)
    # check mandatory modules with alternatives
    if altModulesList:
        altModulesOK = True
        for altModules, forcedOk in altModulesList:
            modulesOK = False
            for altModule in altModules:
                name = altModule.split(".")[1]
                try:
                    __import__(altModule)
                    print("Found", name)
                    modulesOK = True
                    break
                except ImportError:
                    pass
            if not modulesOK and not forcedOk:
                altModulesOK = False
                print('Sorry, please install {0}.'
                      .format(" or ".join(altModules)))
        if not altModulesOK:
            exit(1)
    # check optional modules
    for optPackage in optionalModulesList:
        try:
            __import__(optionalModulesList[optPackage][0])
            print("Found", optPackage)
        except ImportError as msg:
            if isSudo:
                print("Optional '{0}' could not be detected."
                      .format(optPackage))
            else:
                pipInstall(
                    optPackage + optionalModulesList[optPackage][1],
                    "Optional '{0}' could not be detected.\n"
                    "Error: {1}".format(optPackage, msg)
                )
    
    # determine the platform dependent black list
    if sys.platform.startswith(("win", "cygwin")):
        PlatformBlackLists = PlatformsBlackLists["windows"]
    elif sys.platform.startswith("linux"):
        PlatformBlackLists = PlatformsBlackLists["linux"]
    else:
        PlatformBlackLists = PlatformsBlackLists["mac"]
    
    # check version of Qt
    qtMajor = int(qVersion().split('.')[0])
    qtMinor = int(qVersion().split('.')[1])
    print("Qt Version: {0}".format(qVersion().strip()))
    if qtMajor == 5 and qtMinor < 12:
        print('Sorry, you must have Qt version 5.12.0 or better.')
        exit(2)
    
    # check version of sip
    try:
        try:
            from PyQt5 import sip
        except ImportError:
            import sip
        sipVersion = sip.SIP_VERSION_STR
        print("sip Version:", sipVersion.strip())
        # always assume, that snapshots or dev versions are new enough
        if "snapshot" not in sipVersion and "dev" not in sipVersion:
            while sipVersion.count('.') < 2:
                sipVersion += '.0'
            (major, minor, pat) = sipVersion.split('.')
            major = int(major)
            minor = int(minor)
            pat = int(pat)
            if (
                major < 4 or
                (major == 4 and minor < 14) or
                (major == 4 and minor == 14 and pat < 2)
            ):
                print('Sorry, you must have sip 4.14.2 or higher or'
                      ' a recent snapshot release.')
                exit(3)
            # check for blacklisted versions
            for vers in BlackLists["sip"] + PlatformBlackLists["sip"]:
                if vers == sipVersion:
                    print(
                        'Sorry, sip version {0} is not compatible with eric.'
                        .format(vers))
                    print('Please install another version.')
                    exit(3)
    except (ImportError, AttributeError):
        pass
    
    # check version of PyQt
    from PyQt5.QtCore import PYQT_VERSION_STR
    pyqtVersion = PYQT_VERSION_STR
    print("PyQt Version:", pyqtVersion.strip())
    # always assume, that snapshots or dev versions are new enough
    if "snapshot" not in pyqtVersion and "dev" not in pyqtVersion:
        while pyqtVersion.count('.') < 2:
            pyqtVersion += '.0'
        (major, minor, pat) = pyqtVersion.split('.')
        major = int(major)
        minor = int(minor)
        pat = int(pat)
        if major == 5 and minor < 12:
            print('Sorry, you must have PyQt 5.12.0 or better or'
                  ' a recent snapshot release.')
            exit(4)
        # check for blacklisted versions
        for vers in BlackLists["PyQt5"] + PlatformBlackLists["PyQt5"]:
            if vers == pyqtVersion:
                print('Sorry, PyQt version {0} is not compatible with eric.'
                      .format(vers))
                print('Please install another version.')
                exit(4)
    
    # check version of QScintilla
    from PyQt5.Qsci import QSCINTILLA_VERSION_STR
    scintillaVersion = QSCINTILLA_VERSION_STR
    print("QScintilla Version:", QSCINTILLA_VERSION_STR.strip())
    # always assume, that snapshots or dev versions are new enough
    if "snapshot" not in scintillaVersion and "dev" not in scintillaVersion:
        while scintillaVersion.count('.') < 2:
            scintillaVersion += '.0'
        (major, minor, pat) = scintillaVersion.split('.')
        major = int(major)
        minor = int(minor)
        pat = int(pat)
        if (
            major < 2 or
            (major == 2 and minor < 11) or
            (major == 2 and minor == 11 and pat < 1)
        ):
            print('Sorry, you must have QScintilla 2.11.1 or higher or'
                  ' a recent snapshot release.')
            exit(5)
        # check for blacklisted versions
        for vers in (
            BlackLists["QScintilla2"] +
            PlatformBlackLists["QScintilla2"]
        ):
            if vers == scintillaVersion:
                print(
                    'Sorry, QScintilla2 version {0} is not compatible with'
                    ' eric.'.format(vers))
                print('Please install another version.')
                exit(5)
    
    # print version info for additional modules
    try:
        print("PyQtChart:", QtChart.PYQT_CHART_VERSION_STR)
    except (NameError, AttributeError):
        pass
    try:
        from PyQt5 import QtWebEngine
        print("PyQtWebEngine.", QtWebEngine.PYQT_WEBENGINE_VERSION_STR)
    except (ImportError, AttributeError):
        pass
    
    print("All dependencies ok.")
    print()


def __pyName(py_dir, py_file):
    """
    Local function to create the Python source file name for the compiled
    .ui file.
    
    @param py_dir suggested name of the directory (string)
    @param py_file suggested name for the compile source file (string)
    @return tuple of directory name (string) and source file name (string)
    """
    return py_dir, "Ui_{0}".format(py_file)


def compileUiFiles():
    """
    Compile the .ui files to Python sources.
    """
    from PyQt5.uic import compileUiDir
    compileUiDir(eric6SourceDir, True, __pyName)


def prepareInfoFile(fileName):
    """
    Function to prepare an Info.py file when installing from source.
    
    @param fileName name of the Python file containing the info (string)
    """
    if not fileName:
        return
    
    try:
        os.rename(fileName, fileName + ".orig")
    except OSError:
        pass
    try:
        hgOut = subprocess.check_output(["hg", "identify", "-i"])   # secok
        hgOut = hgOut.decode()
    except (OSError, subprocess.CalledProcessError):
        hgOut = ""
    if hgOut:
        hgOut = hgOut.strip()
        if hgOut.endswith("+"):
            hgOut = hgOut[:-1]
        with open(fileName + ".orig", "r", encoding="utf-8") as f:
            text = f.read()
        text = (
            text.replace("@@REVISION@@", hgOut)
            .replace("@@VERSION@@", "rev_" + hgOut)
        )
        copyToFile(fileName, text)
    else:
        shutil.copy(fileName + ".orig", fileName)


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
    global cfg
    
    majorVersion, minorVersion = sys.version_info[:2]
    entriesTemplates = [
        ("eric6 (Python {0}.{1}).lnk",
         os.path.join(cfg["bindir"], "eric6.cmd"),
         os.path.join(cfg["ericPixDir"], "eric6.ico")),
        ("eric6 Browser (Python {0}.{1}).lnk",
         os.path.join(cfg["bindir"], "eric6_browse.cmd"),
         os.path.join(cfg["ericPixDir"], "ericWeb48.ico")),
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


def main(argv):
    """
    The main function of the script.

    @param argv list of command line arguments
    @type list of str
    """
    import getopt

    # Parse the command line.
    global progName, modDir, doCleanup, doCompile, distDir, cfg, apisDir
    global sourceDir, eric6SourceDir, configName
    global macAppBundlePath, macAppBundleName, macPythonExe
    global installApis, doCleanDesktopLinks, yes2All
    global createInstallInfoFile, installCwd
    global ignorePyqt5Tools
    
    if sys.version_info < (3, 6, 0) or sys.version_info > (3, 99, 99):
        print('Sorry, eric requires at least Python 3.6 for running.')
        exit(5)
    
    progName = os.path.basename(argv[0])
    
    installCwd = os.getcwd()
    
    if os.path.dirname(argv[0]):
        os.chdir(os.path.dirname(argv[0]))
    
    initGlobals()

    try:
        if sys.platform.startswith(("win", "cygwin")):
            optlist, args = getopt.getopt(
                argv[1:], "chxza:b:d:f:",
                ["help", "no-apis", "no-info", "no-tools", "yes"])
        elif sys.platform == "darwin":
            optlist, args = getopt.getopt(
                argv[1:], "chxza:b:d:f:i:m:n:p:",
                ["help", "no-apis", "no-info", "yes"])
        else:
            optlist, args = getopt.getopt(
                argv[1:], "chxza:b:d:f:i:",
                ["help", "no-apis", "no-info", "no-tools", "yes"])
    except getopt.GetoptError as err:
        print(err)
        usage()

    global platBinDir
    
    depChecks = True

    for opt, arg in optlist:
        if opt in ["-h", "--help"]:
            usage(0)
        elif opt == "-a":
            apisDir = arg
        elif opt == "-b":
            platBinDir = arg
        elif opt == "-d":
            modDir = arg
        elif opt == "-i":
            distDir = os.path.normpath(arg)
        elif opt == "-x":
            depChecks = False
        elif opt == "-c":
            doCleanup = False
        elif opt == "-z":
            doCompile = False
        elif opt == "-f":
            try:
                exec(compile(open(arg).read(), arg, 'exec'), globals())
                # secok
                if len(cfg) != configLength:
                    print("The configuration dictionary in '{0}' is incorrect."
                          " Aborting".format(arg))
                    exit(6)
            except Exception:
                cfg = {}
        elif opt == "-m":
            macAppBundleName = arg
        elif opt == "-n":
            macAppBundlePath = arg
        elif opt == "-p":
            macPythonExe = arg
        elif opt == "--no-apis":
            installApis = False
        elif opt == "--clean-desktop":
            doCleanDesktopLinks = True
        elif opt == "--yes":
            yes2All = True
        elif opt == "--no-tools":
            ignorePyqt5Tools = True
        elif opt == "--no-info":
            createInstallInfoFile = False
    
    infoName = ""
    installFromSource = not os.path.isdir(sourceDir)
    
    # check dependencies
    if depChecks:
        doDependancyChecks()
    
    # cleanup source if installing from source
    if installFromSource:
        print("Cleaning up source ...")
        sourceDir = os.path.abspath("..")
        eric6SourceDir = os.path.join(sourceDir, "eric6")
        cleanupSource(eric6SourceDir)
        print()
    
    if installFromSource:
        sourceDir = os.path.abspath("..")
        eric6SourceDir = os.path.join(sourceDir, "eric6")
        configName = os.path.join(eric6SourceDir, "eric6config.py")
        if os.path.exists(os.path.join(sourceDir, ".hg")):
            # we are installing from source with repo
            infoName = os.path.join(eric6SourceDir, "UI", "Info.py")
            prepareInfoFile(infoName)
    
    if len(cfg) == 0:
        createInstallConfig()
    
    # get rid of development config file, if it exists
    try:
        if installFromSource:
            os.rename(configName, configName + ".orig")
            configNameC = configName + 'c'
            if os.path.exists(configNameC):
                os.remove(configNameC)
        os.remove(configName)
    except OSError:
        pass
    
    # cleanup old installation
    print("Cleaning up old installation ...")
    try:
        if doCleanup:
            if distDir:
                shutil.rmtree(distDir, True)
            else:
                cleanUp()
    except OSError as msg:
        sys.stderr.write('Error: {0}\nTry install as root.\n'.format(msg))
        exit(7)

    # Create a config file and delete the default one
    print("\nCreating configuration file ...")
    createConfig()

    createInstallInfo()
    
    # Compile .ui files
    print("\nCompiling user interface files ...")
    # step 1: remove old Ui_*.py files
    for root, _, files in os.walk(sourceDir):
        for file in [f for f in files if fnmatch.fnmatch(f, 'Ui_*.py')]:
            os.remove(os.path.join(root, file))
    # step 2: compile the forms
    compileUiFiles()
    
    if doCompile:
        print("\nCompiling source files ...")
        skipRe = re.compile(r"DebugClients[\\/]Python[\\/]")
        sys.stdout = io.StringIO()
        if distDir:
            compileall.compile_dir(
                eric6SourceDir,
                ddir=os.path.join(distDir, modDir, cfg['ericDir']),
                rx=skipRe,
                quiet=True)
            py_compile.compile(
                configName,
                dfile=os.path.join(distDir, modDir, "eric6config.py"))
        else:
            compileall.compile_dir(
                eric6SourceDir,
                ddir=os.path.join(modDir, cfg['ericDir']),
                rx=skipRe,
                quiet=True)
            py_compile.compile(configName,
                               dfile=os.path.join(modDir, "eric6config.py"))
        sys.stdout = sys.__stdout__
    print("\nInstalling eric ...")
    res = installEric()
    
    if createInstallInfoFile:
        with open(os.path.join(cfg["ericDir"],
                               installInfoName), "w") as installInfoFile:
            json.dump(installInfo, installInfoFile, indent=2)
    
    # do some cleanup
    try:
        if installFromSource:
            os.remove(configName)
            configNameC = configName + 'c'
            if os.path.exists(configNameC):
                os.remove(configNameC)
            os.rename(configName + ".orig", configName)
    except OSError:
        pass
    try:
        if installFromSource and infoName:
            os.remove(infoName)
            infoNameC = infoName + 'c'
            if os.path.exists(infoNameC):
                os.remove(infoNameC)
            os.rename(infoName + ".orig", infoName)
    except OSError:
        pass
    
    print("\nInstallation complete.")
    print()
    
    exit(res)
    
    
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
