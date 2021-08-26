#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Tray.

This is the main Python script that performs the necessary initialization
of the system-tray application. This acts as a quickstarter by providing a
context menu to start the eric IDE and the eric tools.
"""

import sys
import os

SettingsDir = None

sys.path.insert(1, os.path.dirname(__file__))

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        import Globals
        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt5.QtCore import QSettings
        SettingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(SettingsDir):
            os.makedirs(SettingsDir)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, SettingsDir)
        sys.argv.remove(arg)

from Globals import AppInfo

from Toolbox import Startup


def createMainWidget(argv):
    """
    Function to create the main widget.
    
    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from Tools.TrayStarter import TrayStarter
    return TrayStarter(SettingsDir)


def main():
    """
    Main entry point into the application.
    """
    from PyQt5.QtGui import QGuiApplication
    QGuiApplication.setDesktopFileName("eric6_tray.desktop")
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
    ]
    appinfo = AppInfo.makeAppInfo(sys.argv,
                                  "eric Tray",
                                  "",
                                  "Traystarter for eric",
                                  options)
    res = Startup.simpleAppStartup(sys.argv,
                                   appinfo,
                                   createMainWidget,
                                   quitOnLastWindowClosed=False,
                                   raiseIt=False)
    sys.exit(res)

if __name__ == '__main__':
    main()
