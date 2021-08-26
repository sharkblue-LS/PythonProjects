#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Python IDE.

This is the main Python script that performs the necessary initialization
of the IDE and starts the Qt event loop.
"""

import sys
import os

originalPathString = os.getenv("PATH")

# generate list of arguments to be remembered for a restart
restartArgsList = ["--no-splash", "--plugin", "--debug", "--config",
                   "--settings", "--disable-crash", "--disable-plugin"]
restartArgs = [arg for arg in sys.argv[1:]
               if arg.split("=", 1)[0] in restartArgsList]

sys.path.insert(1, os.path.dirname(__file__))

try:
    try:
        from PyQt5 import sip       # __IGNORE_EXCEPTION__
    except ImportError:
        import sip
    sip.setdestroyonexit(False)
except AttributeError:
    pass

import traceback
import time
import logging
import io

try:
    from PyQt5.QtCore import qWarning, QLibraryInfo, QTimer, QCoreApplication
except ImportError:
    try:
        from tkinter import messagebox
    except ImportError:
        sys.exit(100)
    messagebox.showerror(
        "eric6 Error",
        "PyQt could not be imported. Please make sure"
        " it is installed and accessible.")
    sys.exit(100)

try:
    from PyQt5 import QtWebEngineWidgets    # __IGNORE_WARNING__
except ImportError:
    pass

# some global variables needed to start the application
args = None
mainWindow = None
splash = None
inMainLoop = None
app = None

if "--debug" in sys.argv:
    del sys.argv[sys.argv.index("--debug")]
    logging.basicConfig(level=logging.DEBUG)

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        import Globals
        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt5.QtCore import QSettings
        settingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(settingsDir):
            os.makedirs(settingsDir)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, settingsDir)
        sys.argv.remove(arg)

# make Third-Party package available as a packages repository
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "ThirdParty", "Pygments"))
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "ThirdParty", "Jasy"))
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "ThirdParty", "EditorConfig"))
sys.path.insert(2, os.path.join(os.path.dirname(__file__),
                                "DebugClients", "Python"))

from E5Gui.E5Application import E5Application


def handleSingleApplication(ddindex):
    """
    Global function to handle the single application mode.
    
    @param ddindex index of a '--' option in the options list
    """
    from E5Gui.E5SingleApplication import E5SingleApplicationClient
    
    client = E5SingleApplicationClient()
    res = client.connect()
    if res > 0:
        if (
            "--no-splash" in sys.argv and
            sys.argv.index("--no-splash") < ddindex
        ):
            sys.argv.remove("--no-splash")
            ddindex -= 1
        if "--no-open" in sys.argv and sys.argv.index("--no-open") < ddindex:
            sys.argv.remove("--no-open")
            ddindex -= 1
        if "--no-crash" in sys.argv and sys.argv.index("--no-crash") < ddindex:
            sys.argv.remove("--no-crash")
        if (
            "--disable-crash" in sys.argv and
            sys.argv.index("--disable-crash") < ddindex
        ):
            sys.argv.remove("--disable-crash")
            ddindex -= 1
        if "--debug" in sys.argv and sys.argv.index("--debug") < ddindex:
            sys.argv.remove("--debug")
            ddindex -= 1
        for arg in sys.argv:
            if (
                arg.startswith("--config=") and
                sys.argv.index(arg) < ddindex
            ):
                sys.argv.remove(arg)
                ddindex -= 1
                break
        for arg in sys.argv:
            if (
                arg.startswith("--plugin=") and
                sys.argv.index(arg) < ddindex
            ):
                sys.argv.remove(arg)
                ddindex -= 1
                break
        for arg in sys.argv[:]:
            if (
                arg.startswith("--disable-plugin=") and
                sys.argv.index(arg) < ddindex
            ):
                sys.argv.remove(arg)
                ddindex -= 1
        
        if len(sys.argv) > 1:
            client.processArgs(sys.argv[1:])
        sys.exit(0)
    elif res < 0:
        print("eric6: {0}".format(client.errstr()))
        # __IGNORE_WARNING_M801__
        sys.exit(res)


def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    from UI.Info import BugAddress
    import Utilities
    import Globals
    
    separator = '-' * 80
    logFile = os.path.join(Globals.getConfigDir(), "eric6_error.log")
    notice = (
        """An unhandled exception occurred. Please report the problem\n"""
        """using the error reporting dialog or via email to <{0}>.\n"""
        """A log has been written to "{1}".\n\nError information:\n""".format(
            BugAddress, logFile)
    )
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    
    versionInfo = "\n{0}\n{1}".format(
        separator, Utilities.generateVersionInfo())
    pluginVersionInfo = Utilities.generatePluginsVersionInfo()
    if pluginVersionInfo:
        versionInfo += "\n{0}\n{1}".format(separator, pluginVersionInfo)
    distroInfo = Utilities.generateDistroInfo()
    if distroInfo:
        versionInfo += "\n{0}\n{1}".format(separator, distroInfo)
    
    if isinstance(excType, str):
        tbinfo = tracebackobj
    else:
        tbinfofile = io.StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
    errmsg = '{0}: \n{1}'.format(str(excType), str(excValue))
    sections = ['', separator, timeString, separator, errmsg, separator,
                tbinfo]
    msg = '\n'.join(sections)
    try:
        with open(logFile, "w", encoding="utf-8") as f:
            f.write(msg)
            f.write(versionInfo)
    except OSError:
        pass
    
    if inMainLoop is None:
        warning = notice + msg + versionInfo
        print(warning)                          # __IGNORE_WARNING_M801__
    else:
        warning = notice + msg + versionInfo
        # Escape &<> otherwise it's not visible in the error dialog
        warning = (
            warning
            .replace("&", "&amp;")
            .replace(">", "&gt;")
            .replace("<", "&lt;")
        )
        qWarning(warning)


def uiStartUp():
    """
    Global function to finalize the start up of the main UI.
    
    Note: It is activated by a zero timeout single-shot timer.
    """
    global args, mainWindow, splash
    
    if splash:
        splash.finish(mainWindow)
        del splash
    
    mainWindow.checkForErrorLog()
    mainWindow.processArgs(args)
    mainWindow.processInstallInfoFile()
    mainWindow.checkProjectsWorkspace()
    mainWindow.checkConfigurationStatus()
    mainWindow.performVersionCheck(False)
    mainWindow.checkPluginUpdatesAvailable()
    mainWindow.autoConnectIrc()


def main():
    """
    Main entry point into the application.
    """
    from Globals import AppInfo
    import Globals
    
    global app, args, mainWindow, splash, restartArgs, inMainLoop
    
    sys.excepthook = excepthook
    
    from PyQt5.QtGui import QGuiApplication
    QGuiApplication.setDesktopFileName("eric6.desktop")
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--debug", "activate debugging output to the console"),
        ("--no-splash", "don't show the splash screen"),
        ("--no-open",
         "don't open anything at startup except that given in command"),
        ("--no-crash", "don't check for a crash session file on startup"),
        ("--disable-crash", "disable the support for crash sessions"),
        ("--disable-plugin=<plug-in name>",
         "disable the given plug-in (may be repeated)"),
        ("--plugin=plugin-file",
         "load the given plugin file (plugin development)"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
        ("--start-file", "load the most recently opened file"),
        ("--start-multi", "load the most recently opened multi-project"),
        ("--start-project", "load the most recently opened project"),
        ("--start-session", "load the global session file"),
        ("--",
         "indicate that there are options for the program to be debugged"),
        ("",
         "(everything after that is considered arguments for this program)")
    ]
    appinfo = AppInfo.makeAppInfo(sys.argv,
                                  "Eric6",
                                  "[project | files... [--] [debug-options]]",
                                  "A Python IDE",
                                  options)
    
    if "__PYVENV_LAUNCHER__" in os.environ:
        del os.environ["__PYVENV_LAUNCHER__"]
    
    # make sure our executable directory (i.e. that of the used Python
    # interpreter) is included in the executable search path
    pathList = os.environ["PATH"].split(os.pathsep)
    exeDir = os.path.dirname(sys.executable)
    if exeDir not in pathList:
        pathList.insert(0, exeDir)
    os.environ["PATH"] = os.pathsep.join(pathList)
    
    from Toolbox import Startup
    # set the library paths for plugins
    Startup.setLibraryPaths()

    app = E5Application(sys.argv)
    ddindex = Startup.handleArgs(sys.argv, appinfo)
    
    logging.debug("Importing Preferences")
    import Preferences
    
    if Preferences.getUI("SingleApplicationMode"):
        handleSingleApplication(ddindex)
    
    # set the search path for icons
    Startup.initializeResourceSearchPath(app)
    
    # generate and show a splash window, if not suppressed
    from UI.SplashScreen import SplashScreen, NoneSplashScreen
    if "--no-splash" in sys.argv and sys.argv.index("--no-splash") < ddindex:
        sys.argv.remove("--no-splash")
        ddindex -= 1
        splash = NoneSplashScreen()
    elif not Preferences.getUI("ShowSplash"):
        splash = NoneSplashScreen()
    else:
        splash = SplashScreen()
    QCoreApplication.processEvents()

    # modify the executable search path for the PyQt5 installer
    if Globals.isWindowsPlatform():
        pyqtDataDir = Globals.getPyQt5ModulesDirectory()
        if os.path.exists(os.path.join(pyqtDataDir, "bin")):
            path = os.path.join(pyqtDataDir, "bin")
        else:
            path = pyqtDataDir
        os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    
    pluginFile = None
    noopen = False
    nocrash = False
    disablecrash = False
    disabledPlugins = []
    if "--no-open" in sys.argv and sys.argv.index("--no-open") < ddindex:
        sys.argv.remove("--no-open")
        ddindex -= 1
        noopen = True
    if "--no-crash" in sys.argv and sys.argv.index("--no-crash") < ddindex:
        sys.argv.remove("--no-crash")
        ddindex -= 1
        nocrash = True
    if (
        "--disable-crash" in sys.argv and
        sys.argv.index("--disable-crash") < ddindex
    ):
        sys.argv.remove("--disable-crash")
        ddindex -= 1
        disablecrash = True
    for arg in sys.argv[:]:
        if (
            arg.startswith("--disable-plugin=") and
            sys.argv.index(arg) < ddindex
        ):
            # extract the plug-in name
            pluginName = arg.replace("--disable-plugin=", "")
            sys.argv.remove(arg)
            ddindex -= 1
            disabledPlugins.append(pluginName)
    for arg in sys.argv:
        if arg.startswith("--plugin=") and sys.argv.index(arg) < ddindex:
            # extract the plugin development option
            pluginFile = arg.replace("--plugin=", "").replace('"', "")
            sys.argv.remove(arg)
            ddindex -= 1
            pluginFile = os.path.expanduser(pluginFile)
            pluginFile = os.path.abspath(pluginFile)
            break
    
    # is there a set of filenames or options on the command line,
    # if so, pass them to the UI
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    
    # get the Qt translations directory
    qtTransDir = Preferences.getQtTranslationsDir()
    if not qtTransDir:
        qtTransDir = QLibraryInfo.location(
            QLibraryInfo.LibraryLocation.TranslationsPath)
    
    # Load translation files and install them
    loc = Startup.loadTranslators(qtTransDir, app, ("qscintilla",))
    
    # Initialize SSL stuff
    from E5Network.E5SslUtilities import initSSL
    initSSL()
    
    splash.showMessage(QCoreApplication.translate("eric6", "Starting..."))
    # We can only import these after creating the E5Application because they
    # make Qt calls that need the E5Application to exist.
    from UI.UserInterface import UserInterface

    splash.showMessage(
        QCoreApplication.translate("eric6", "Generating Main Window..."))
    mainWindow = UserInterface(app, loc, splash, pluginFile, disabledPlugins,
                               noopen, nocrash, disablecrash, restartArgs,
                               originalPathString)
    app.lastWindowClosed.connect(app.quit)
    mainWindow.show()
    
    QTimer.singleShot(0, uiStartUp)
    
    # generate a graphical error handler
    from E5Gui import E5ErrorMessage
    eMsg = E5ErrorMessage.qtHandler()
    eMsg.setMinimumSize(600, 400)
    
    # start the event loop
    inMainLoop = True
    res = app.exec()
    logging.debug("Shutting down, result %d", res)
    logging.shutdown()
    sys.exit(res)

if __name__ == '__main__':
    main()
