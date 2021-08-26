#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric SQL Browser.

This is the main Python script that performs the necessary initialization
of the SQL browser and starts the Qt event loop.
"""

import sys
import os

sys.path.insert(1, os.path.dirname(__file__))

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

from Globals import AppInfo

from Toolbox import Startup


def createMainWidget(argv):
    """
    Function to create the main widget.
    
    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from SqlBrowser.SqlBrowser import SqlBrowser
    
    if len(argv) > 1:
        connections = argv[1:]
    else:
        connections = []
    
    browser = SqlBrowser(connections)
    return browser


def main():
    """
    Main entry point into the application.
    """
    from PyQt5.QtGui import QGuiApplication
    QGuiApplication.setDesktopFileName("eric6_sqlbrowser.desktop")
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
    ]
    appinfo = AppInfo.makeAppInfo(sys.argv,
                                  "eric SQL Browser",
                                  "connection",
                                  "SQL browser",
                                  options)
    res = Startup.simpleAppStartup(sys.argv,
                                   appinfo,
                                   createMainWidget)
    sys.exit(res)

if __name__ == '__main__':
    main()
