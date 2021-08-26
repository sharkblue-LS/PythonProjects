# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a starter for the system tray.
"""

import sys
import os

from PyQt5.QtCore import QProcess, QSettings, QFileInfo
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QDialog, QApplication

from E5Gui import E5MessageBox
from E5Gui.E5Application import e5App

import Globals
import UI.PixmapCache
from UI.Info import Version, Program

import Utilities
import Preferences

from eric6config import getConfig


class TrayStarter(QSystemTrayIcon):
    """
    Class implementing a starter for the system tray.
    """
    def __init__(self, settingsDir):
        """
        Constructor
        
        @param settingsDir directory to be used for the settings files
        @type str
        """
        super(TrayStarter, self).__init__(
            UI.PixmapCache.getIcon(
                Preferences.getTrayStarter("TrayStarterIcon")))
        
        self.settingsDir = settingsDir
        
        self.maxMenuFilePathLen = 75
        
        self.rsettings = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            Globals.settingsNameOrganization,
            Globals.settingsNameRecent)
        
        self.recentProjects = []
        self.__loadRecentProjects()
        self.recentMultiProjects = []
        self.__loadRecentMultiProjects()
        self.recentFiles = []
        self.__loadRecentFiles()
        
        self.activated.connect(self.__activated)
        
        self.__menu = QMenu(self.tr("eric tray starter"))
        
        self.recentProjectsMenu = QMenu(
            self.tr('Recent Projects'), self.__menu)
        self.recentProjectsMenu.aboutToShow.connect(
            self.__showRecentProjectsMenu)
        self.recentProjectsMenu.triggered.connect(self.__openRecent)
        
        self.recentMultiProjectsMenu = QMenu(
            self.tr('Recent Multiprojects'), self.__menu)
        self.recentMultiProjectsMenu.aboutToShow.connect(
            self.__showRecentMultiProjectsMenu)
        self.recentMultiProjectsMenu.triggered.connect(self.__openRecent)
        
        self.recentFilesMenu = QMenu(self.tr('Recent Files'), self.__menu)
        self.recentFilesMenu.aboutToShow.connect(self.__showRecentFilesMenu)
        self.recentFilesMenu.triggered.connect(self.__openRecent)
        
        act = self.__menu.addAction(
            self.tr("eric tray starter"), self.__about)
        font = act.font()
        font.setBold(True)
        act.setFont(font)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            self.tr("Show Versions"), self.__showVersions)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            self.tr("QRegularExpression editor"),
            self.__startQRegularExpression)
        self.__menu.addAction(
            self.tr("Python re editor"), self.__startPyRe)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("uiPreviewer"),
            self.tr("UI Previewer"), self.__startUIPreviewer)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("trPreviewer"),
            self.tr("Translations Previewer"), self.__startTRPreviewer)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("unittest"),
            self.tr("Unittest"), self.__startUnittest)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("diffFiles"),
            self.tr("Compare Files"), self.__startDiff)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("compareFiles"),
            self.tr("Compare Files side by side"), self.__startCompare)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("sqlBrowser"),
            self.tr("SQL Browser"), self.__startSqlBrowser)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("ericSnap"),
            self.tr("Snapshot"), self.__startSnapshot)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("iconEditor"),
            self.tr("Icon Editor"), self.__startIconEditor)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("pluginInstall"),
            self.tr("Install Plugin"), self.__startPluginInstall)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("pluginUninstall"),
            self.tr("Uninstall Plugin"), self.__startPluginUninstall)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("pluginRepository"),
            self.tr("Plugin Repository"), self.__startPluginRepository)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("configure"),
            self.tr('Preferences'), self.__startPreferences)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("editor"),
            self.tr("eric Mini Editor"), self.__startMiniEditor)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("hexEditor"),
            self.tr("eric Hex Editor"), self.__startHexEditor)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("shell"),
            self.tr("eric Shell Window"), self.__startShell)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("ericWeb"),
            self.tr("eric Web Browser"), self.__startWebBrowser)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("ericWeb"),
            self.tr("eric Web Browser (with QtHelp)"),
            self.__startWebBrowserQtHelp)
        self.__menu.addAction(
            UI.PixmapCache.getIcon("ericWeb"),
            self.tr("eric Web Browser (Private Mode)"),
            self.__startWebBrowserPrivate)
        self.__menu.addSeparator()
        
        # recent files
        self.menuRecentFilesAct = self.__menu.addMenu(self.recentFilesMenu)
        # recent multi projects
        self.menuRecentMultiProjectsAct = self.__menu.addMenu(
            self.recentMultiProjectsMenu)
        # recent projects
        self.menuRecentProjectsAct = self.__menu.addMenu(
            self.recentProjectsMenu)
        self.__menu.addSeparator()
        
        self.__menu.addAction(
            UI.PixmapCache.getIcon("erict"),
            self.tr("eric IDE"), self.__startEric)
        self.__menu.addSeparator()
         
        self.__menu.addAction(
            UI.PixmapCache.getIcon("configure"),
            self.tr('Configure Tray Starter'), self.__showPreferences)
        self.__menu.addSeparator()
       
        self.__menu.addAction(
            UI.PixmapCache.getIcon("exit"),
            self.tr('Quit'), e5App().quit)
    
    def __loadRecentProjects(self):
        """
        Private method to load the recently opened project filenames.
        """
        rp = self.rsettings.value(Globals.recentNameProject)
        if rp is not None:
            for f in rp:
                if QFileInfo(f).exists():
                    self.recentProjects.append(f)
    
    def __loadRecentMultiProjects(self):
        """
        Private method to load the recently opened multi project filenames.
        """
        rmp = self.rsettings.value(Globals.recentNameMultiProject)
        if rmp is not None:
            for f in rmp:
                if QFileInfo(f).exists():
                    self.recentMultiProjects.append(f)
    
    def __loadRecentFiles(self):
        """
        Private method to load the recently opened filenames.
        """
        rf = self.rsettings.value(Globals.recentNameFiles)
        if rf is not None:
            for f in rf:
                if QFileInfo(f).exists():
                    self.recentFiles.append(f)
    
    def __activated(self, reason):
        """
        Private slot to handle the activated signal.
        
        @param reason reason code of the signal
            (QSystemTrayIcon.ActivationReason)
        """
        if (
            reason == QSystemTrayIcon.ActivationReason.Context or
            reason == QSystemTrayIcon.ActivationReason.MiddleClick
        ):
            self.__showContextMenu()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.__startEric()
    
    def __showContextMenu(self):
        """
        Private slot to show the context menu.
        """
        self.menuRecentProjectsAct.setEnabled(len(self.recentProjects) > 0)
        self.menuRecentMultiProjectsAct.setEnabled(
            len(self.recentMultiProjects) > 0)
        self.menuRecentFilesAct.setEnabled(len(self.recentFiles) > 0)
        
        pos = QCursor.pos()
        x = pos.x() - self.__menu.sizeHint().width()
        pos.setX(x > 0 and x or 0)
        y = pos.y() - self.__menu.sizeHint().height()
        pos.setY(y > 0 and y or 0)
        self.__menu.popup(pos)
    
    def __startProc(self, applName, *applArgs):
        """
        Private method to start an eric application.
        
        @param applName name of the eric application script (string)
        @param *applArgs variable list of application arguments
        """
        proc = QProcess()
        applPath = os.path.join(getConfig("ericDir"), applName)
        
        args = []
        args.append(applPath)
        args.append("--config={0}".format(Utilities.getConfigDir()))
        if self.settingsDir:
            args.append("--settings={0}".format(self.settingsDir))
        for arg in applArgs:
            args.append(arg)
        
        if (
            not os.path.isfile(applPath) or
            not proc.startDetached(sys.executable, args)
        ):
            E5MessageBox.critical(
                self,
                self.tr('Process Generation Error'),
                self.tr(
                    '<p>Could not start the process.<br>'
                    'Ensure that it is available as <b>{0}</b>.</p>'
                ).format(applPath),
                self.tr('OK'))
    
    def __startMiniEditor(self):
        """
        Private slot to start the eric Mini Editor.
        """
        self.__startProc("eric6_editor.py")
    
    def __startEric(self):
        """
        Private slot to start the eric IDE.
        """
        self.__startProc("eric6.py")

    def __startPreferences(self):
        """
        Private slot to start the eric configuration dialog.
        """
        self.__startProc("eric6_configure.py")

    def __startPluginInstall(self):
        """
        Private slot to start the eric plugin installation dialog.
        """
        self.__startProc("eric6_plugininstall.py")

    def __startPluginUninstall(self):
        """
        Private slot to start the eric plugin uninstallation dialog.
        """
        self.__startProc("eric6_pluginuninstall.py")

    def __startPluginRepository(self):
        """
        Private slot to start the eric plugin repository dialog.
        """
        self.__startProc("eric6_pluginrepository.py")

    def __startWebBrowser(self):
        """
        Private slot to start the eric web browser.
        """
        variant = Globals.getWebBrowserSupport()
        if variant == "QtWebEngine":
            self.__startProc("eric6_browser.py")

    def __startWebBrowserQtHelp(self):
        """
        Private slot to start the eric web browser with QtHelp support.
        """
        variant = Globals.getWebBrowserSupport()
        if variant == "QtWebEngine":
            self.__startProc("eric6_browser.py", "--qthelp")

    def __startWebBrowserPrivate(self):
        """
        Private slot to start the eric web browser in private mode.
        """
        variant = Globals.getWebBrowserSupport()
        if variant == "QtWebEngine":
            self.__startProc("eric6_browser.py", "--private")

    def __startUIPreviewer(self):
        """
        Private slot to start the eric UI previewer.
        """
        self.__startProc("eric6_uipreviewer.py")

    def __startTRPreviewer(self):
        """
        Private slot to start the eric translations previewer.
        """
        self.__startProc("eric6_trpreviewer.py")

    def __startUnittest(self):
        """
        Private slot to start the eric unittest dialog.
        """
        self.__startProc("eric6_unittest.py")

    def __startDiff(self):
        """
        Private slot to start the eric diff dialog.
        """
        self.__startProc("eric6_diff.py")

    def __startCompare(self):
        """
        Private slot to start the eric compare dialog.
        """
        self.__startProc("eric6_compare.py")
    
    def __startSqlBrowser(self):
        """
        Private slot to start the eric sql browser dialog.
        """
        self.__startProc("eric6_sqlbrowser.py")

    def __startIconEditor(self):
        """
        Private slot to start the eric icon editor dialog.
        """
        self.__startProc("eric6_iconeditor.py")

    def __startSnapshot(self):
        """
        Private slot to start the eric snapshot dialog.
        """
        self.__startProc("eric6_snap.py")

    def __startQRegularExpression(self):
        """
        Private slot to start the eric QRegularExpression editor dialog.
        """
        self.__startProc("eric6_qregularexpression.py")

    def __startPyRe(self):
        """
        Private slot to start the eric Python re editor dialog.
        """
        self.__startProc("eric6_re.py")
    
    def __startHexEditor(self):
        """
        Private slot to start the eric hex editor dialog.
        """
        self.__startProc("eric6_hexeditor.py")
    
    def __startShell(self):
        """
        Private slot to start the eric Shell window.
        """
        self.__startProc("eric6_shell.py")

    def __showRecentProjectsMenu(self):
        """
        Private method to set up the recent projects menu.
        """
        self.recentProjects = []
        self.rsettings.sync()
        self.__loadRecentProjects()
        
        self.recentProjectsMenu.clear()
        
        idx = 1
        for rp in self.recentProjects:
            if idx < 10:
                formatStr = '&{0:d}. {1}'
            else:
                formatStr = '{0:d}. {1}'
            act = self.recentProjectsMenu.addAction(
                formatStr.format(
                    idx, Utilities.compactPath(rp, self.maxMenuFilePathLen)))
            act.setData(rp)
            idx += 1
    
    def __showRecentMultiProjectsMenu(self):
        """
        Private method to set up the recent multi projects menu.
        """
        self.recentMultiProjects = []
        self.rsettings.sync()
        self.__loadRecentMultiProjects()
        
        self.recentMultiProjectsMenu.clear()
        
        idx = 1
        for rmp in self.recentMultiProjects:
            if idx < 10:
                formatStr = '&{0:d}. {1}'
            else:
                formatStr = '{0:d}. {1}'
            act = self.recentMultiProjectsMenu.addAction(
                formatStr.format(
                    idx, Utilities.compactPath(rmp, self.maxMenuFilePathLen)))
            act.setData(rmp)
            idx += 1
    
    def __showRecentFilesMenu(self):
        """
        Private method to set up the recent files menu.
        """
        self.recentFiles = []
        self.rsettings.sync()
        self.__loadRecentFiles()
        
        self.recentFilesMenu.clear()
        
        idx = 1
        for rf in self.recentFiles:
            if idx < 10:
                formatStr = '&{0:d}. {1}'
            else:
                formatStr = '{0:d}. {1}'
            act = self.recentFilesMenu.addAction(
                formatStr.format(
                    idx, Utilities.compactPath(rf, self.maxMenuFilePathLen)))
            act.setData(rf)
            idx += 1
    
    def __openRecent(self, act):
        """
        Private method to open a project or file from the list of recently
        opened projects or files.
        
        @param act reference to the action that triggered (QAction)
        """
        filename = act.data()
        if filename:
            self.__startProc(
                "eric6.py",
                filename)
    
    def __showPreferences(self):
        """
        Private slot to set the preferences.
        """
        from Preferences.ConfigurationDialog import ConfigurationDialog
        dlg = ConfigurationDialog(
            None, 'Configuration', True, fromEric=True,
            displayMode=ConfigurationDialog.TrayStarterMode)
        dlg.preferencesChanged.connect(self.preferencesChanged)
        dlg.show()
        dlg.showConfigurationPageByName("trayStarterPage")
        dlg.exec()
        QApplication.processEvents()
        if dlg.result() == QDialog.DialogCode.Accepted:
            dlg.setPreferences()
            Preferences.syncPreferences()
            self.preferencesChanged()
    
    def preferencesChanged(self):
        """
        Public slot to handle a change of preferences.
        """
        self.setIcon(
            UI.PixmapCache.getIcon(
                Preferences.getTrayStarter("TrayStarterIcon")))

    def __about(self):
        """
        Private slot to handle the About dialog.
        """
        from Plugins.AboutPlugin.AboutDialog import AboutDialog
        dlg = AboutDialog()
        dlg.exec()
    
    def __showVersions(self):
        """
        Private slot to handle the Versions dialog.
        """
        from PyQt5.QtCore import qVersion, PYQT_VERSION_STR
        from PyQt5.Qsci import QSCINTILLA_VERSION_STR
        
        try:
            try:
                from PyQt5 import sip
            except ImportError:
                import sip
            sip_version_str = sip.SIP_VERSION_STR
        except (ImportError, AttributeError):
            sip_version_str = "sip version not available"
        
        versionText = self.tr(
            """<h3>Version Numbers</h3>"""
            """<table>""")
        versionText += (
            """<tr><td><b>Python</b></td><td>{0}</td></tr>"""
            .format(sys.version.split()[0])
        )
        versionText += (
            """<tr><td><b>Qt</b></td><td>{0}</td></tr>"""
            .format(qVersion())
        )
        versionText += (
            """<tr><td><b>PyQt</b></td><td>{0}</td></tr>"""
            .format(PYQT_VERSION_STR)
        )
        versionText += (
            """<tr><td><b>sip</b></td><td>{0}</td></tr>"""
            .format(sip_version_str)
        )
        versionText += (
            """<tr><td><b>QScintilla</b></td><td>{0}</td></tr>"""
            .format(QSCINTILLA_VERSION_STR)
        )
        try:
            from WebBrowser.Tools import WebBrowserTools
            chromeVersion = WebBrowserTools.getWebEngineVersions()[0]
            versionText += (
                """<tr><td><b>WebEngine</b></td><td>{0}</td></tr>"""
                .format(chromeVersion)
            )
        except ImportError:
            pass
        versionText += (
            """<tr><td><b>{0}</b></td><td>{1}</td></tr>"""
            .format(Program, Version)
        )
        versionText += self.tr("""</table>""")
        
        E5MessageBox.about(None, Program, versionText)
