#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric QRegularExpression.

This is the main Python script that performs the necessary initialization
of the QRegularExpression wizard module and starts the Qt event loop. This is
a standalone version of the integrated QRegularExpression wizard.
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
    from Plugins.WizardPlugins.QRegularExpressionWizard import (
        QRegularExpressionWizardDialog
    )
    return QRegularExpressionWizardDialog.QRegularExpressionWizardWindow()


def main():
    """
    Main entry point into the application.
    """
    from PyQt5.QtGui import QGuiApplication
    QGuiApplication.setDesktopFileName("eric6_qregularexpression.desktop")
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
    ]
    appinfo = AppInfo.makeAppInfo(
        sys.argv,
        "eric QRegularExpression",
        "",
        "Regexp editor for Qt's QRegularExpression class",
        options)
    res = Startup.simpleAppStartup(sys.argv,
                                   appinfo,
                                   createMainWidget)
    sys.exit(res)

if __name__ == '__main__':
    main()
