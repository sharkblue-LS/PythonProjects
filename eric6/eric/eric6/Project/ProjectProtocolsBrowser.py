# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the a class used to display the protocols (protobuf) part
of the project.
"""

import os
import glob
import sys

from PyQt5.QtCore import QThread, pyqtSignal, QProcess
from PyQt5.QtWidgets import QDialog, QApplication, QMenu

from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox
from E5Gui.E5ProgressDialog import E5ProgressDialog

from .ProjectBrowserModel import (
    ProjectBrowserFileItem, ProjectBrowserSimpleDirectoryItem,
    ProjectBrowserDirectoryItem, ProjectBrowserProtocolsType
)
from .ProjectBaseBrowser import ProjectBaseBrowser

from UI.BrowserModel import (
    BrowserFileItem, BrowserClassItem, BrowserMethodItem,
    BrowserClassAttributeItem
)
import UI.PixmapCache
from UI.NotificationWidget import NotificationTypes

import Preferences
import Utilities


class ProjectProtocolsBrowser(ProjectBaseBrowser):
    """
    A class used to display the protocols (protobuf) part of the project.
    
    @signal appendStdout(str) emitted after something was received from
        a QProcess on stdout
    @signal appendStderr(str) emitted after something was received from
        a QProcess on stderr
    @signal showMenu(str, QMenu) emitted when a menu is about to be shown.
        The name of the menu and a reference to the menu are given.
    """
    appendStdout = pyqtSignal(str)
    appendStderr = pyqtSignal(str)
    showMenu = pyqtSignal(str, QMenu)
    
    def __init__(self, project, parent=None):
        """
        Constructor
        
        @param project reference to the project object
        @type Project
        @param parent parent widget of this browser
        @type QWidget
        """
        ProjectBaseBrowser.__init__(self, project,
                                    ProjectBrowserProtocolsType, parent)
        
        self.selectedItemsFilter = [ProjectBrowserFileItem,
                                    ProjectBrowserSimpleDirectoryItem]
        
        self.setWindowTitle(self.tr('Protocols (protobuf)'))
        
        self.setWhatsThis(self.tr(
            """<b>Project Protocols Browser</b>"""
            """<p>This allows to easily see all protocols (protobuf files)"""
            """ contained in the current project. Several actions can be"""
            """ executed via the context menu.</p>"""
        ))
        
        project.prepareRepopulateItem.connect(self._prepareRepopulateItem)
        project.completeRepopulateItem.connect(self._completeRepopulateItem)
    
    def _createPopupMenus(self):
        """
        Protected overloaded method to generate the popup menu.
        """
        self.menuActions = []
        self.multiMenuActions = []
        self.dirMenuActions = []
        self.dirMultiMenuActions = []
        
        self.sourceMenu = QMenu(self)
        self.sourceMenu.addAction(
            self.tr('Compile protocol'), self.__compileProtocol)
        self.sourceMenu.addAction(
            self.tr('Compile all protocols'),
            self.__compileAllProtocols)
        self.sourceMenu.addSeparator()
        self.sourceMenu.addAction(
            self.tr('Compile protocol as gRPC'),
            lambda: self.__compileProtocol(grpc=True))
        self.sourceMenu.addAction(
            self.tr('Compile all protocols as gRPC'),
            lambda: self.__compileAllProtocols(grpc=True))
        self.sourceMenu.addSeparator()
        self.sourceMenu.addAction(self.tr('Open'), self._openItem)
        self.sourceMenu.addSeparator()
        act = self.sourceMenu.addAction(
            self.tr('Rename file'), self._renameFile)
        self.menuActions.append(act)
        act = self.sourceMenu.addAction(
            self.tr('Remove from project'), self._removeFile)
        self.menuActions.append(act)
        act = self.sourceMenu.addAction(
            self.tr('Delete'), self.__deleteFile)
        self.menuActions.append(act)
        self.sourceMenu.addSeparator()
        self.sourceMenu.addAction(
            self.tr('Add protocols...'), self.__addProtocolFiles)
        self.sourceMenu.addAction(
            self.tr('Add protocols directory...'),
            self.__addProtocolsDirectory)
        self.sourceMenu.addSeparator()
        self.sourceMenu.addAction(
            self.tr('Copy Path to Clipboard'), self._copyToClipboard)
        self.sourceMenu.addSeparator()
        self.sourceMenu.addAction(
            self.tr('Expand all directories'), self._expandAllDirs)
        self.sourceMenu.addAction(
            self.tr('Collapse all directories'), self._collapseAllDirs)
        self.sourceMenu.addSeparator()
        self.sourceMenu.addAction(self.tr('Configure...'), self._configure)
        self.sourceMenu.addAction(
            self.tr('Configure Protobuf...'), self.__configureProtobuf)

        self.menu = QMenu(self)
        self.menu.addAction(
            self.tr('Compile protocol'), self.__compileProtocol)
        self.menu.addAction(
            self.tr('Compile all protocols'),
            self.__compileAllProtocols)
        self.menu.addSeparator()
        self.menu.addAction(
            self.tr('Compile protocol as gRPC'),
            lambda: self.__compileProtocol(grpc=True))
        self.menu.addAction(
            self.tr('Compile all protocols as gRPC'),
            lambda: self.__compileAllProtocols(grpc=True))
        self.menu.addSeparator()
        self.menu.addAction(self.tr('Open'), self._openItem)
        self.menu.addSeparator()
        self.menu.addAction(
            self.tr('Add protocols...'), self.__addProtocolFiles)
        self.menu.addAction(
            self.tr('Add protocols directory...'),
            self.__addProtocolsDirectory)
        self.menu.addSeparator()
        self.menu.addAction(
            self.tr('Expand all directories'), self._expandAllDirs)
        self.menu.addAction(
            self.tr('Collapse all directories'), self._collapseAllDirs)
        self.menu.addSeparator()
        self.menu.addAction(self.tr('Configure...'), self._configure)
        self.menu.addAction(
            self.tr('Configure Protobuf...'), self.__configureProtobuf)

        self.backMenu = QMenu(self)
        self.backMenu.addAction(
            self.tr('Compile all protocols'),
            self.__compileAllProtocols)
        self.backMenu.addSeparator()
        self.backMenu.addAction(
            self.tr('Compile all protocols as gRPC'),
            lambda: self.__compileAllProtocols(grpc=True))
        self.backMenu.addSeparator()
        self.backMenu.addAction(
            self.tr('Add protocols...'), self.project.addProtoFiles)
        self.backMenu.addAction(
            self.tr('Add protocols directory...'), self.project.addProtoDir)
        self.backMenu.addSeparator()
        self.backMenu.addAction(
            self.tr('Expand all directories'), self._expandAllDirs)
        self.backMenu.addAction(
            self.tr('Collapse all directories'), self._collapseAllDirs)
        self.backMenu.addSeparator()
        self.backMenu.addAction(self.tr('Configure...'), self._configure)
        self.backMenu.addAction(
            self.tr('Configure Protobuf...'), self.__configureProtobuf)
        self.backMenu.setEnabled(False)

        # create the menu for multiple selected files
        self.multiMenu = QMenu(self)
        self.multiMenu.addAction(
            self.tr('Compile protocols'),
            self.__compileSelectedProtocols)
        self.multiMenu.addSeparator()
        self.multiMenu.addAction(
            self.tr('Compile protocols as gRPC'),
            lambda: self.__compileSelectedProtocols(grpc=True))
        self.multiMenu.addSeparator()
        self.multiMenu.addAction(self.tr('Open'), self._openItem)
        self.multiMenu.addSeparator()
        act = self.multiMenu.addAction(
            self.tr('Remove from project'), self._removeFile)
        self.multiMenuActions.append(act)
        act = self.multiMenu.addAction(
            self.tr('Delete'), self.__deleteFile)
        self.multiMenuActions.append(act)
        self.multiMenu.addSeparator()
        self.multiMenu.addAction(
            self.tr('Expand all directories'), self._expandAllDirs)
        self.multiMenu.addAction(
            self.tr('Collapse all directories'), self._collapseAllDirs)
        self.multiMenu.addSeparator()
        self.multiMenu.addAction(self.tr('Configure...'), self._configure)
        self.multiMenu.addAction(
            self.tr('Configure Protobuf...'), self.__configureProtobuf)

        self.dirMenu = QMenu(self)
        self.dirMenu.addAction(
            self.tr('Compile all protocols'),
            self.__compileAllProtocols)
        self.dirMenu.addSeparator()
        self.dirMenu.addAction(
            self.tr('Compile all protocols as gRPC'),
            lambda: self.__compileAllProtocols(grpc=True))
        act = self.dirMenu.addAction(
            self.tr('Remove from project'), self._removeFile)
        self.dirMenuActions.append(act)
        act = self.dirMenu.addAction(
            self.tr('Delete'), self._deleteDirectory)
        self.dirMenuActions.append(act)
        self.dirMenu.addSeparator()
        self.dirMenu.addAction(
            self.tr('Add protocols...'), self.__addProtocolFiles)
        self.dirMenu.addAction(
            self.tr('Add protocols directory...'),
            self.__addProtocolsDirectory)
        self.dirMenu.addSeparator()
        self.dirMenu.addAction(
            self.tr('Copy Path to Clipboard'), self._copyToClipboard)
        self.dirMenu.addSeparator()
        self.dirMenu.addAction(
            self.tr('Expand all directories'), self._expandAllDirs)
        self.dirMenu.addAction(
            self.tr('Collapse all directories'), self._collapseAllDirs)
        self.dirMenu.addSeparator()
        self.dirMenu.addAction(self.tr('Configure...'), self._configure)
        self.dirMenu.addAction(
            self.tr('Configure Protobuf...'), self.__configureProtobuf)
        
        self.dirMultiMenu = QMenu(self)
        self.dirMultiMenu.addAction(
            self.tr('Compile all protocols'),
            self.__compileAllProtocols)
        self.dirMultiMenu.addSeparator()
        self.dirMultiMenu.addAction(
            self.tr('Compile all protocols as gRPC'),
            lambda: self.__compileAllProtocols(grpc=True))
        self.dirMultiMenu.addAction(
            self.tr('Add protocols...'), self.project.addProtoFiles)
        self.dirMultiMenu.addAction(
            self.tr('Add protocols directory...'), self.project.addProtoDir)
        self.dirMultiMenu.addSeparator()
        self.dirMultiMenu.addAction(
            self.tr('Expand all directories'), self._expandAllDirs)
        self.dirMultiMenu.addAction(
            self.tr('Collapse all directories'), self._collapseAllDirs)
        self.dirMultiMenu.addSeparator()
        self.dirMultiMenu.addAction(
            self.tr('Configure...'), self._configure)
        self.dirMultiMenu.addAction(self.tr('Configure Protobuf...'),
                                    self.__configureProtobuf)
        
        self.sourceMenu.aboutToShow.connect(self.__showContextMenu)
        self.multiMenu.aboutToShow.connect(self.__showContextMenuMulti)
        self.dirMenu.aboutToShow.connect(self.__showContextMenuDir)
        self.dirMultiMenu.aboutToShow.connect(self.__showContextMenuDirMulti)
        self.backMenu.aboutToShow.connect(self.__showContextMenuBack)
        self.mainMenu = self.sourceMenu
        
    def _contextMenuRequested(self, coord):
        """
        Protected slot to show the context menu.
        
        @param coord the position of the mouse pointer (QPoint)
        """
        if not self.project.isOpen():
            return
        
        try:
            categories = self.getSelectedItemsCountCategorized(
                [ProjectBrowserFileItem, BrowserClassItem,
                 BrowserMethodItem, ProjectBrowserSimpleDirectoryItem])
            cnt = categories["sum"]
            if cnt <= 1:
                index = self.indexAt(coord)
                if index.isValid():
                    self._selectSingleItem(index)
                    categories = self.getSelectedItemsCountCategorized(
                        [ProjectBrowserFileItem, BrowserClassItem,
                         BrowserMethodItem, ProjectBrowserSimpleDirectoryItem])
                    cnt = categories["sum"]
            
            bfcnt = categories[str(ProjectBrowserFileItem)]
            cmcnt = (
                categories[str(BrowserClassItem)] +
                categories[str(BrowserMethodItem)]
            )
            sdcnt = categories[str(ProjectBrowserSimpleDirectoryItem)]
            if cnt > 1 and cnt == bfcnt:
                self.multiMenu.popup(self.mapToGlobal(coord))
            elif cnt > 1 and cnt == sdcnt:
                self.dirMultiMenu.popup(self.mapToGlobal(coord))
            else:
                index = self.indexAt(coord)
                if cnt == 1 and index.isValid():
                    if bfcnt == 1 or cmcnt == 1:
                        itm = self.model().item(index)
                        if isinstance(itm, ProjectBrowserFileItem):
                            self.sourceMenu.popup(self.mapToGlobal(coord))
                        elif isinstance(
                            itm,
                            (BrowserClassItem, BrowserMethodItem)
                        ):
                            self.menu.popup(self.mapToGlobal(coord))
                        else:
                            self.backMenu.popup(self.mapToGlobal(coord))
                    elif sdcnt == 1:
                        self.dirMenu.popup(self.mapToGlobal(coord))
                    else:
                        self.backMenu.popup(self.mapToGlobal(coord))
                else:
                    self.backMenu.popup(self.mapToGlobal(coord))
        except Exception:           # secok
            pass
        
    def __showContextMenu(self):
        """
        Private slot called by the menu aboutToShow signal.
        """
        ProjectBaseBrowser._showContextMenu(self, self.menu)
        
        self.showMenu.emit("Main", self.menu)
        
    def __showContextMenuMulti(self):
        """
        Private slot called by the multiMenu aboutToShow signal.
        """
        ProjectBaseBrowser._showContextMenuMulti(self, self.multiMenu)
        
        self.showMenu.emit("MainMulti", self.multiMenu)
        
    def __showContextMenuDir(self):
        """
        Private slot called by the dirMenu aboutToShow signal.
        """
        ProjectBaseBrowser._showContextMenuDir(self, self.dirMenu)
        
        self.showMenu.emit("MainDir", self.dirMenu)
        
    def __showContextMenuDirMulti(self):
        """
        Private slot called by the dirMultiMenu aboutToShow signal.
        """
        ProjectBaseBrowser._showContextMenuDirMulti(self, self.dirMultiMenu)
        
        self.showMenu.emit("MainDirMulti", self.dirMultiMenu)
        
    def __showContextMenuBack(self):
        """
        Private slot called by the backMenu aboutToShow signal.
        """
        ProjectBaseBrowser._showContextMenuBack(self, self.backMenu)
        
        self.showMenu.emit("MainBack", self.backMenu)
        
    def _openItem(self):
        """
        Protected slot to handle the open popup menu entry.
        """
        itmList = self.getSelectedItems(
            [BrowserFileItem, BrowserClassItem, BrowserMethodItem,
             BrowserClassAttributeItem])
        
        for itm in itmList:
            if isinstance(itm, BrowserFileItem):
                self.sourceFile[str].emit(itm.fileName())
            elif isinstance(itm, BrowserClassItem):
                self.sourceFile[str, int].emit(
                    itm.fileName(), itm.classObject().lineno)
            elif isinstance(itm, BrowserMethodItem):
                self.sourceFile[str, int].emit(
                    itm.fileName(), itm.functionObject().lineno)
            elif isinstance(itm, BrowserClassAttributeItem):
                self.sourceFile[str, int].emit(
                    itm.fileName(), itm.attributeObject().lineno)
        
    def __addProtocolFiles(self):
        """
        Private method to add protocol files to the project.
        """
        itm = self.model().item(self.currentIndex())
        if isinstance(
            itm,
            (ProjectBrowserFileItem, BrowserClassItem, BrowserMethodItem)
        ):
            dn = os.path.dirname(itm.fileName())
        elif isinstance(
            itm,
            (ProjectBrowserSimpleDirectoryItem, ProjectBrowserDirectoryItem)
        ):
            dn = itm.dirName()
        else:
            dn = None
        self.project.addFiles('protocol', dn)
        
    def __addProtocolsDirectory(self):
        """
        Private method to add protocol files of a directory to the project.
        """
        itm = self.model().item(self.currentIndex())
        if isinstance(
            itm,
            (ProjectBrowserFileItem, BrowserClassItem, BrowserMethodItem)
        ):
            dn = os.path.dirname(itm.fileName())
        elif isinstance(
            itm,
            (ProjectBrowserSimpleDirectoryItem, ProjectBrowserDirectoryItem)
        ):
            dn = itm.dirName()
        else:
            dn = None
        self.project.addDirectory('protocol', dn)
        
    def __deleteFile(self):
        """
        Private method to delete files from the project.
        """
        itmList = self.getSelectedItems()
        
        files = []
        fullNames = []
        for itm in itmList:
            fn2 = itm.fileName()
            fullNames.append(fn2)
            fn = self.project.getRelativePath(fn2)
            files.append(fn)
        
        from UI.DeleteFilesConfirmationDialog import (
            DeleteFilesConfirmationDialog
        )
        dlg = DeleteFilesConfirmationDialog(
            self.parent(),
            self.tr("Delete Protocols"),
            self.tr("Do you really want to delete these protocol files from"
                    " the project?"),
            files)
        
        if dlg.exec() == QDialog.DialogCode.Accepted:
            for fn2, fn in zip(fullNames, files):
                self.closeSourceWindow.emit(fn2)
                self.project.deleteFile(fn)
    
    ###########################################################################
    ##  Methods to handle the various compile commands
    ###########################################################################
    
    def __getCompilerCommand(self, grpc):
        """
        Private method to get the compiler command.
        
        @param grpc flag indicating to get a gRPC command
        @type bool
        @return tuple giving the executable and its parameter list
        @rtype tuple of (str, list of str)
        """
        exe = None
        exeArgs = []
        
        if grpc:
            exe = Preferences.getProtobuf("grpcPython")
            if exe == "":
                exe = sys.executable
            exeArgs = ['-m', 'grpc_tools.protoc']
        else:
            exe = Preferences.getProtobuf("protoc")
            if exe == "":
                exe = (
                    Utilities.isWindowsPlatform() and
                    "protoc.exe" or "protoc"
                )
            if not Utilities.isinpath(exe):
                exe = None
        
        return exe, exeArgs
    
    def __readStdout(self):
        """
        Private slot to handle the readyReadStandardOutput signal of the
        protoc process.
        """
        if self.compileProc is None:
            return
        
        ioEncoding = Preferences.getSystem("IOEncoding")
        
        self.compileProc.setReadChannel(QProcess.ProcessChannel.StandardOutput)
        while self.compileProc and self.compileProc.canReadLine():
            s = 'protoc: '
            output = str(self.compileProc.readLine(), ioEncoding, 'replace')
            s += output
            self.appendStdout.emit(s)
        
    def __readStderr(self):
        """
        Private slot to handle the readyReadStandardError signal of the
        protoc process.
        """
        if self.compileProc is None:
            return
        
        ioEncoding = Preferences.getSystem("IOEncoding")
        
        self.compileProc.setReadChannel(QProcess.ProcessChannel.StandardError)
        while self.compileProc and self.compileProc.canReadLine():
            s = 'protoc: '
            error = str(self.compileProc.readLine(), ioEncoding, 'replace')
            s += error
            self.appendStderr.emit(s)
        
    def __compileProtoDone(self, exitCode, exitStatus, grpc):
        """
        Private slot to handle the finished signal of the protoc process.
        
        @param exitCode exit code of the process
        @type int
        @param exitStatus exit status of the process
        @type QProcess.ExitStatus
        @param grpc flag indicating to compile as gRPC files
        @type bool
        """
        self.__compileRunning = False
        ui = e5App().getObject("UserInterface")
        if exitStatus == QProcess.ExitStatus.NormalExit and exitCode == 0:
            path = os.path.dirname(self.__protoFile)
            fileList = glob.glob(os.path.join(path, "*_pb2.py"))
            if grpc:
                fileList += glob.glob(os.path.join(path, "*_pb2_grpc.py"))
            for file in fileList:
                self.project.appendFile(file)
            if grpc:
                icon = UI.PixmapCache.getPixmap("gRPC48")
            else:
                icon = UI.PixmapCache.getPixmap("protobuf48")
            ui.showNotification(
                icon,
                self.tr("Protocol Compilation"),
                self.tr(
                    "The compilation of the protocol file was"
                    " successful."))
        else:
            if grpc:
                icon = UI.PixmapCache.getPixmap("gRPC48")
            else:
                icon = UI.PixmapCache.getPixmap("protobuf48")
            ui.showNotification(
                icon,
                self.tr("Protocol Compilation"),
                self.tr(
                    "The compilation of the protocol file failed."),
                kind=NotificationTypes.Critical,
                timeout=0)
        self.compileProc = None
        
    def __compileProto(self, fn, noDialog=False, progress=None, grpc=False):
        """
        Private method to compile a .proto file to Python.

        @param fn filename of the .proto file to be compiled
        @type str
        @param noDialog flag indicating silent operations
        @type bool
        @param progress reference to the progress dialog
        @type E5ProgressDialog
        @param grpc flag indicating to compile as gRPC files
        @type bool
        @return reference to the compile process
        @rtype QProcess
        """
        exe, exeArgs = self.__getCompilerCommand(grpc)
        if exe:
            self.compileProc = QProcess()
            args = []
            
            fn = os.path.join(self.project.ppath, fn)
            self.__protoFile = fn
            
            srcPath = os.path.dirname(fn)
            args.append("--proto_path={0}".format(srcPath))
            args.append("--python_out={0}".format(srcPath))
            if grpc:
                args.append("--grpc_python_out={0}".format(srcPath))
            args.append(fn)
            
            self.compileProc.finished.connect(
                lambda c, s: self.__compileProtoDone(c, s, grpc))
            self.compileProc.readyReadStandardOutput.connect(self.__readStdout)
            self.compileProc.readyReadStandardError.connect(self.__readStderr)
            
            self.noDialog = noDialog
            self.compileProc.start(exe, exeArgs + args)
            procStarted = self.compileProc.waitForStarted(5000)
            if procStarted:
                self.__compileRunning = True
                return self.compileProc
            else:
                self.__compileRunning = False
                if progress is not None:
                    progress.cancel()
                E5MessageBox.critical(
                    self,
                    self.tr('Process Generation Error'),
                    self.tr(
                        '<p>Could not start {0}.<br>'
                        'Ensure that it is in the search path.</p>'
                    ).format(exe))
                return None
        else:
            E5MessageBox.critical(
                self,
                self.tr('Compiler Invalid'),
                self.tr('The configured compiler is invalid.'))
            return None
        
    def __compileProtocol(self, grpc=False):
        """
        Private method to compile a protocol to Python.
        
        @param grpc flag indicating to compile as gRPC files
        @type bool
        """
        if self.__getCompilerCommand(grpc)[0] is not None:
            itm = self.model().item(self.currentIndex())
            fn2 = itm.fileName()
            fn = self.project.getRelativePath(fn2)
            self.__compileProto(fn, grpc=grpc)
        
    def __compileAllProtocols(self, grpc=False):
        """
        Private method to compile all protocols to Python.
        
        @param grpc flag indicating to compile as gRPC files
        @type bool
        """
        if self.__getCompilerCommand(grpc)[0] is not None:
            numProtos = len(self.project.pdata["PROTOCOLS"])
            progress = E5ProgressDialog(
                self.tr("Compiling Protocols..."),
                self.tr("Abort"), 0, numProtos,
                self.tr("%v/%m Protocols"), self)
            progress.setModal(True)
            progress.setMinimumDuration(0)
            progress.setWindowTitle(self.tr("Protocols"))
            i = 0
            
            for fn in self.project.pdata["PROTOCOLS"]:
                progress.setValue(i)
                if progress.wasCanceled():
                    break
                proc = self.__compileProto(fn, True, progress, grpc=grpc)
                if proc is not None:
                    while proc.state() == QProcess.ProcessState.Running:
                        QApplication.processEvents()
                        QThread.msleep(300)
                        QApplication.processEvents()
                else:
                    break
                i += 1
            
            progress.setValue(numProtos)
        
    def __compileSelectedProtocols(self, grpc=False):
        """
        Private method to compile selected protocols to Python.
        
        @param grpc flag indicating to compile as gRPC files
        @type bool
        """
        if self.__getCompilerCommand(grpc)[0] is not None:
            items = self.getSelectedItems()
            
            files = [self.project.getRelativePath(itm.fileName())
                     for itm in items]
            numProtos = len(files)
            progress = E5ProgressDialog(
                self.tr("Compiling Protocols..."),
                self.tr("Abort"), 0, numProtos,
                self.tr("%v/%m Protocols"), self)
            progress.setModal(True)
            progress.setMinimumDuration(0)
            progress.setWindowTitle(self.tr("Protocols"))
            i = 0
            
            for fn in files:
                progress.setValue(i)
                if progress.wasCanceled():
                    break
                proc = self.__compileProto(fn, True, progress, grpc=grpc)
                if proc is not None:
                    while proc.state() == QProcess.ProcessState.Running:
                        QApplication.processEvents()
                        QThread.msleep(300)
                        QApplication.processEvents()
                else:
                    break
                i += 1
                
            progress.setValue(numProtos)
        
    def __configureProtobuf(self):
        """
        Private method to open the configuration dialog.
        """
        e5App().getObject("UserInterface").showPreferences("protobufPage")
