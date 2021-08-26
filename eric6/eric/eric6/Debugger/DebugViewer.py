# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a widget containing various debug related views.

The views avaliable are:
<ul>
  <li>selector showing all connected debugger backends with associated
      threads</li>
  <li>variables viewer for global variables for the selected debug client</li>
  <li>variables viewer for local variables for the selected debug client</li>
  <li>call stack viewer for the selected debug client</li>
  <li>call trace viewer</li>
  <li>viewer for breakpoints</li>
  <li>viewer for watch expressions</li>
  <li>viewer for exceptions</li>
  <li>viewer for a code disassembly for an exception<li>
</ul>
"""

import os

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy, QPushButton,
    QComboBox, QLabel, QTreeWidget, QTreeWidgetItem, QHeaderView, QSplitter
)

import UI.PixmapCache
import Preferences

from E5Gui.E5TabWidget import E5TabWidget


class DebugViewer(QWidget):
    """
    Class implementing a widget containing various debug related views.
    
    The individual tabs contain the interpreter shell (optional),
    the filesystem browser (optional), the two variables viewers
    (global and local), a breakpoint viewer, a watch expression viewer and
    the exception logger. Additionally a list of all threads is shown.
    
    @signal sourceFile(string, int) emitted to open a source file at a line
    @signal preferencesChanged() emitted to react on changed preferences
    """
    sourceFile = pyqtSignal(str, int)
    preferencesChanged = pyqtSignal()
    
    ThreadIdRole = Qt.ItemDataRole.UserRole + 1
    DebuggerStateRole = Qt.ItemDataRole.UserRole + 2
    
    # Map debug state to icon name
    StateIcon = {
        "broken": "break",
        "exception": "exceptions",
        "running": "mediaPlaybackStart",
        "syntax": "syntaxError22",
    }
    
    # Map debug state to user message
    StateMessage = {
        "broken": QCoreApplication.translate(
            "DebugViewer", "waiting at breakpoint"),
        "exception": QCoreApplication.translate(
            "DebugViewer", "waiting at exception"),
        "running": QCoreApplication.translate(
            "DebugViewer", "running"),
        "syntax": QCoreApplication.translate(
            "DebugViewer", "syntax error"),
    }
    
    def __init__(self, debugServer, parent=None):
        """
        Constructor
        
        @param debugServer reference to the debug server object
        @type DebugServer
        @param parent parent widget
        @type QWidget
        """
        super(DebugViewer, self).__init__(parent)
        
        self.debugServer = debugServer
        self.debugUI = None
        
        self.setWindowIcon(UI.PixmapCache.getIcon("eric"))
        
        self.__mainLayout = QVBoxLayout()
        self.__mainLayout.setContentsMargins(0, 3, 0, 0)
        self.setLayout(self.__mainLayout)
        
        self.__mainSplitter = QSplitter(Qt.Orientation.Vertical, self)
        self.__mainLayout.addWidget(self.__mainSplitter)
        
        # add the viewer showing the connected debug backends
        self.__debuggersWidget = QWidget()
        self.__debuggersLayout = QVBoxLayout(self.__debuggersWidget)
        self.__debuggersLayout.setContentsMargins(0, 0, 0, 0)
        self.__debuggersLayout.addWidget(
            QLabel(self.tr("Debuggers and Threads:")))
        self.__debuggersList = QTreeWidget()
        self.__debuggersList.setHeaderLabels(
            [self.tr("ID"), self.tr("State"), ""])
        self.__debuggersList.header().setStretchLastSection(True)
        self.__debuggersList.setSortingEnabled(True)
        self.__debuggersList.setRootIsDecorated(True)
        self.__debuggersList.setAlternatingRowColors(True)
        self.__debuggersLayout.addWidget(self.__debuggersList)
        self.__mainSplitter.addWidget(self.__debuggersWidget)
        
        self.__debuggersList.currentItemChanged.connect(
            self.__debuggerSelected)
        
        # add the tab widget containing various debug related views
        self.__tabWidget = E5TabWidget()
        self.__mainSplitter.addWidget(self.__tabWidget)
        
        from .VariablesViewer import VariablesViewer
        # add the global variables viewer
        self.glvWidget = QWidget()
        self.glvWidgetVLayout = QVBoxLayout(self.glvWidget)
        self.glvWidgetVLayout.setContentsMargins(0, 0, 0, 0)
        self.glvWidgetVLayout.setSpacing(3)
        self.glvWidget.setLayout(self.glvWidgetVLayout)
        
        self.globalsViewer = VariablesViewer(self, True, self.glvWidget)
        self.glvWidgetVLayout.addWidget(self.globalsViewer)
        
        self.glvWidgetHLayout = QHBoxLayout()
        self.glvWidgetHLayout.setContentsMargins(3, 3, 3, 3)
        
        self.globalsFilterEdit = QLineEdit(self.glvWidget)
        self.globalsFilterEdit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.glvWidgetHLayout.addWidget(self.globalsFilterEdit)
        self.globalsFilterEdit.setToolTip(
            self.tr("Enter regular expression patterns separated by ';'"
                    " to define variable filters. "))
        self.globalsFilterEdit.setWhatsThis(
            self.tr("Enter regular expression patterns separated by ';'"
                    " to define variable filters. All variables and"
                    " class attributes matched by one of the expressions"
                    " are not shown in the list above."))
        
        self.setGlobalsFilterButton = QPushButton(
            self.tr('Set'), self.glvWidget)
        self.glvWidgetHLayout.addWidget(self.setGlobalsFilterButton)
        self.glvWidgetVLayout.addLayout(self.glvWidgetHLayout)
        
        index = self.__tabWidget.addTab(
            self.glvWidget,
            UI.PixmapCache.getIcon("globalVariables"), '')
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows the list of global variables and their values."))
        
        self.setGlobalsFilterButton.clicked.connect(
            self.setGlobalsFilter)
        self.globalsFilterEdit.returnPressed.connect(self.setGlobalsFilter)
        
        # add the local variables viewer
        self.lvWidget = QWidget()
        self.lvWidgetVLayout = QVBoxLayout(self.lvWidget)
        self.lvWidgetVLayout.setContentsMargins(0, 0, 0, 0)
        self.lvWidgetVLayout.setSpacing(3)
        self.lvWidget.setLayout(self.lvWidgetVLayout)
        
        self.lvWidgetHLayout1 = QHBoxLayout()
        self.lvWidgetHLayout1.setContentsMargins(3, 3, 3, 3)
        
        self.stackComboBox = QComboBox(self.lvWidget)
        self.stackComboBox.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.lvWidgetHLayout1.addWidget(self.stackComboBox)

        self.sourceButton = QPushButton(self.tr('Source'), self.lvWidget)
        self.lvWidgetHLayout1.addWidget(self.sourceButton)
        self.sourceButton.setEnabled(False)
        self.lvWidgetVLayout.addLayout(self.lvWidgetHLayout1)

        self.localsViewer = VariablesViewer(self, False, self.lvWidget)
        self.lvWidgetVLayout.addWidget(self.localsViewer)
        
        self.lvWidgetHLayout2 = QHBoxLayout()
        self.lvWidgetHLayout2.setContentsMargins(3, 3, 3, 3)
        
        self.localsFilterEdit = QLineEdit(self.lvWidget)
        self.localsFilterEdit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.lvWidgetHLayout2.addWidget(self.localsFilterEdit)
        self.localsFilterEdit.setToolTip(
            self.tr(
                "Enter regular expression patterns separated by ';' to define "
                "variable filters. "))
        self.localsFilterEdit.setWhatsThis(
            self.tr(
                "Enter regular expression patterns separated by ';' to define "
                "variable filters. All variables and class attributes matched"
                " by one of the expressions are not shown in the list above."))
        
        self.setLocalsFilterButton = QPushButton(
            self.tr('Set'), self.lvWidget)
        self.lvWidgetHLayout2.addWidget(self.setLocalsFilterButton)
        self.lvWidgetVLayout.addLayout(self.lvWidgetHLayout2)
        
        index = self.__tabWidget.addTab(
            self.lvWidget,
            UI.PixmapCache.getIcon("localVariables"), '')
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows the list of local variables and their values."))
        
        self.sourceButton.clicked.connect(self.__showSource)
        self.stackComboBox.currentIndexChanged[int].connect(
            self.__frameSelected)
        self.setLocalsFilterButton.clicked.connect(self.setLocalsFilter)
        self.localsFilterEdit.returnPressed.connect(self.setLocalsFilter)
        
        self.preferencesChanged.connect(self.handlePreferencesChanged)
        self.preferencesChanged.connect(self.globalsViewer.preferencesChanged)
        self.preferencesChanged.connect(self.localsViewer.preferencesChanged)
        
        from .CallStackViewer import CallStackViewer
        # add the call stack viewer
        self.callStackViewer = CallStackViewer(self.debugServer)
        index = self.__tabWidget.addTab(
            self.callStackViewer,
            UI.PixmapCache.getIcon("callStack"), "")
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows the current call stack."))
        self.callStackViewer.sourceFile.connect(self.sourceFile)
        self.callStackViewer.frameSelected.connect(
            self.__callStackFrameSelected)
        
        from .CallTraceViewer import CallTraceViewer
        # add the call trace viewer
        self.callTraceViewer = CallTraceViewer(self.debugServer, self)
        index = self.__tabWidget.addTab(
            self.callTraceViewer,
            UI.PixmapCache.getIcon("callTrace"), "")
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows a trace of the program flow."))
        self.callTraceViewer.sourceFile.connect(self.sourceFile)
        
        from .BreakPointViewer import BreakPointViewer
        # add the breakpoint viewer
        self.breakpointViewer = BreakPointViewer()
        self.breakpointViewer.setModel(self.debugServer.getBreakPointModel())
        index = self.__tabWidget.addTab(
            self.breakpointViewer,
            UI.PixmapCache.getIcon("breakpoints"), '')
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows a list of defined breakpoints."))
        self.breakpointViewer.sourceFile.connect(self.sourceFile)
        
        from .WatchPointViewer import WatchPointViewer
        # add the watch expression viewer
        self.watchpointViewer = WatchPointViewer()
        self.watchpointViewer.setModel(self.debugServer.getWatchPointModel())
        index = self.__tabWidget.addTab(
            self.watchpointViewer,
            UI.PixmapCache.getIcon("watchpoints"), '')
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows a list of defined watchpoints."))
        
        from .ExceptionLogger import ExceptionLogger
        # add the exception logger
        self.exceptionLogger = ExceptionLogger()
        index = self.__tabWidget.addTab(
            self.exceptionLogger,
            UI.PixmapCache.getIcon("exceptions"), '')
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows a list of raised exceptions."))
        
        from UI.PythonDisViewer import PythonDisViewer, PythonDisViewerModes
        # add the Python disassembly viewer
        self.disassemblyViewer = PythonDisViewer(
            None, mode=PythonDisViewerModes.TracebackMode)
        index = self.__tabWidget.addTab(
            self.disassemblyViewer,
            UI.PixmapCache.getIcon("disassembly"), '')
        self.__tabWidget.setTabToolTip(
            index,
            self.tr("Shows a code disassembly in case of an exception."))
        
        self.__tabWidget.setCurrentWidget(self.glvWidget)
        
        self.__doDebuggersListUpdate = True
        
        self.__mainSplitter.setSizes([100, 700])
        
        self.currentStack = None
        self.framenr = 0
        
        self.__autoViewSource = Preferences.getDebugger("AutoViewSourceCode")
        self.sourceButton.setVisible(not self.__autoViewSource)
        
        # connect some debug server signals
        self.debugServer.clientStack.connect(
            self.handleClientStack)
        self.debugServer.clientThreadList.connect(
            self.__addThreadList)
        self.debugServer.clientDebuggerId.connect(
            self.__clientDebuggerId)
        self.debugServer.passiveDebugStarted.connect(
            self.handleDebuggingStarted)
        self.debugServer.clientLine.connect(
            self.__clientLine)
        self.debugServer.clientSyntaxError.connect(
            self.__clientSyntaxError)
        self.debugServer.clientException.connect(
            self.__clientException)
        self.debugServer.clientExit.connect(
            self.__clientExit)
        self.debugServer.clientDisconnected.connect(
            self.__removeDebugger)
        
        self.debugServer.clientException.connect(
            self.exceptionLogger.addException)
        self.debugServer.passiveDebugStarted.connect(
            self.exceptionLogger.debuggingStarted)
        
        self.debugServer.clientLine.connect(
            self.breakpointViewer.highlightBreakpoint)
    
    def handlePreferencesChanged(self):
        """
        Public slot to handle the preferencesChanged signal.
        """
        self.__autoViewSource = Preferences.getDebugger("AutoViewSourceCode")
        self.sourceButton.setVisible(not self.__autoViewSource)
        
    def setDebugger(self, debugUI):
        """
        Public method to set a reference to the Debug UI.
        
        @param debugUI reference to the DebugUI object
        @type DebugUI
        """
        self.debugUI = debugUI
        self.callStackViewer.setDebugger(debugUI)
        
        # connect some debugUI signals
        self.debugUI.clientStack.connect(self.handleClientStack)
        self.debugUI.debuggingStarted.connect(
            self.exceptionLogger.debuggingStarted)
        self.debugUI.debuggingStarted.connect(
            self.handleDebuggingStarted)
    
    def handleResetUI(self, fullReset):
        """
        Public method to reset the viewer.
        
        @param fullReset flag indicating a full reset is required
        @type bool
        """
        self.globalsViewer.handleResetUI()
        self.localsViewer.handleResetUI()
        self.setGlobalsFilter()
        self.setLocalsFilter()
        self.sourceButton.setEnabled(False)
        self.currentStack = None
        self.stackComboBox.clear()
        self.__tabWidget.setCurrentWidget(self.glvWidget)
        self.breakpointViewer.handleResetUI()
        if fullReset:
            self.__debuggersList.clear()
        self.disassemblyViewer.clear()
        
    def initCallStackViewer(self, projectMode):
        """
        Public method to initialize the call stack viewer.
        
        @param projectMode flag indicating to enable the project mode
        @type bool
        """
        self.callStackViewer.clear()
        self.callStackViewer.setProjectMode(projectMode)
        
    def isCallTraceEnabled(self):
        """
        Public method to get the state of the call trace function.
        
        @return flag indicating the state of the call trace function
        @rtype bool
        """
        return self.callTraceViewer.isCallTraceEnabled()
        
    def clearCallTrace(self):
        """
        Public method to clear the recorded call trace.
        """
        self.callTraceViewer.clear()
        
    def setCallTraceToProjectMode(self, enabled):
        """
        Public slot to set the call trace viewer to project mode.
        
        In project mode the call trace info is shown with project relative
        path names.
        
        @param enabled flag indicating to enable the project mode
        @type bool
        """
        self.callTraceViewer.setProjectMode(enabled)
        
    def showVariables(self, vlist, showGlobals):
        """
        Public method to show the variables in the respective window.
        
        @param vlist list of variables to display
        @type list
        @param showGlobals flag indicating global/local state
        @type bool
        """
        if showGlobals:
            self.globalsViewer.showVariables(vlist, self.framenr)
        else:
            self.localsViewer.showVariables(vlist, self.framenr)
            
    def showVariable(self, vlist, showGlobals):
        """
        Public method to show the variables in the respective window.
        
        @param vlist list of variables to display
        @type list
        @param showGlobals flag indicating global/local state
        @type bool
        """
        if showGlobals:
            self.globalsViewer.showVariable(vlist)
        else:
            self.localsViewer.showVariable(vlist)
            
    def showVariablesTab(self, showGlobals):
        """
        Public method to make a variables tab visible.
        
        @param showGlobals flag indicating global/local state
        @type bool
        """
        if showGlobals:
            self.__tabWidget.setCurrentWidget(self.glvWidget)
        else:
            self.__tabWidget.setCurrentWidget(self.lvWidget)
        
    def handleClientStack(self, stack, debuggerId):
        """
        Public slot to show the call stack of the program being debugged.
        
        @param stack list of tuples with call stack data (file name,
            line number, function name, formatted argument/values list)
        @type list of tuples of (str, str, str, str)
        @param debuggerId ID of the debugger backend
        @type str
        """
        if debuggerId == self.getSelectedDebuggerId():
            block = self.stackComboBox.blockSignals(True)
            self.framenr = 0
            self.stackComboBox.clear()
            self.currentStack = stack
            self.sourceButton.setEnabled(len(stack) > 0)
            for s in stack:
                # just show base filename to make it readable
                s = (os.path.basename(s[0]), s[1], s[2])
                self.stackComboBox.addItem('{0}:{1}:{2}'.format(*s))
            self.stackComboBox.blockSignals(block)
    
    def __clientLine(self, fn, line, debuggerId, threadName):
        """
        Private method to handle a change to the current line.
        
        @param fn filename
        @type str
        @param line linenumber
        @type int
        @param debuggerId ID of the debugger backend
        @type str
        @param threadName name of the thread signaling the event
        @type str
        """
        self.__setDebuggerIconAndState(debuggerId, "broken")
        self.__setThreadIconAndState(debuggerId, threadName, "broken")
        if debuggerId != self.getSelectedDebuggerId():
            self.__setCurrentDebugger(debuggerId)
    
    @pyqtSlot(str, int, str, bool, str)
    def __clientExit(self, program, status, message, quiet, debuggerId):
        """
        Private method to handle the debugged program terminating.
        
        @param program name of the exited program
        @type str
        @param status exit code of the debugged program
        @type int
        @param message exit message of the debugged program
        @type str
        @param quiet flag indicating to suppress exit info display
        @type bool
        @param debuggerId ID of the debugger backend
        @type str
        """
        if not self.isOnlyDebugger():
            if debuggerId == self.getSelectedDebuggerId():
                # the current client has exited
                self.globalsViewer.handleResetUI()
                self.localsViewer.handleResetUI()
                self.setGlobalsFilter()
                self.setLocalsFilter()
                self.sourceButton.setEnabled(False)
                self.currentStack = None
                self.stackComboBox.clear()
            
            self.__removeDebugger(debuggerId)
    
    def __clientSyntaxError(self, message, filename, lineNo, characterNo,
                            debuggerId, threadName):
        """
        Private method to handle a syntax error in the debugged program.
        
        @param message message of the syntax error
        @type str
        @param filename translated filename of the syntax error position
        @type str
        @param lineNo line number of the syntax error position
        @type int
        @param characterNo character number of the syntax error position
        @type int
        @param debuggerId ID of the debugger backend
        @type str
        @param threadName name of the thread signaling the event
        @type str
        """
        self.__setDebuggerIconAndState(debuggerId, "syntax")
        self.__setThreadIconAndState(debuggerId, threadName, "syntax")
    
    def __clientException(self, exceptionType, exceptionMessage, stackTrace,
                          debuggerId, threadName):
        """
        Private method to handle an exception of the debugged program.
        
        @param exceptionType type of exception raised
        @type str
        @param exceptionMessage message given by the exception
        @type (str
        @param stackTrace list of stack entries
        @type list of str
        @param debuggerId ID of the debugger backend
        @type str
        @param threadName name of the thread signaling the event
        @type str
        """
        self.__setDebuggerIconAndState(debuggerId, "exception")
        self.__setThreadIconAndState(debuggerId, threadName, "exception")
    
    def setVariablesFilter(self, globalsFilter, localsFilter):
        """
        Public slot to set the local variables filter.
        
        @param globalsFilter filter list for global variable types
        @type list of str
        @param localsFilter filter list for local variable types
        @type list of str
        """
        self.__globalsFilter = globalsFilter
        self.__localsFilter = localsFilter
        
    def __showSource(self):
        """
        Private slot to handle the source button press to show the selected
        file.
        """
        index = self.stackComboBox.currentIndex()
        if index > -1 and self.currentStack:
            s = self.currentStack[index]
            self.sourceFile.emit(s[0], int(s[1]))
        
    def __frameSelected(self, frmnr):
        """
        Private slot to handle the selection of a new stack frame number.
        
        @param frmnr frame number (0 is the current frame)
        @type int
        """
        if frmnr >= 0:
            self.framenr = frmnr
            if self.debugServer.isDebugging():
                self.debugServer.remoteClientVariables(
                    self.getSelectedDebuggerId(), 0, self.__localsFilter,
                    frmnr)
            
            if self.__autoViewSource:
                self.__showSource()
        
    def setGlobalsFilter(self):
        """
        Public slot to set the global variable filter.
        """
        if self.debugServer.isDebugging():
            filterStr = self.globalsFilterEdit.text()
            self.debugServer.remoteClientSetFilter(
                self.getSelectedDebuggerId(), 1, filterStr)
            self.debugServer.remoteClientVariables(
                self.getSelectedDebuggerId(), 2, self.__globalsFilter)
        
    def setLocalsFilter(self):
        """
        Public slot to set the local variable filter.
        """
        if self.debugServer.isDebugging():
            filterStr = self.localsFilterEdit.text()
            self.debugServer.remoteClientSetFilter(
                self.getSelectedDebuggerId(), 0, filterStr)
            if self.currentStack:
                self.debugServer.remoteClientVariables(
                    self.getSelectedDebuggerId(), 0, self.__localsFilter,
                    self.framenr)
        
    def handleDebuggingStarted(self):
        """
        Public slot to handle the start of a debugging session.
        
        This slot sets the variables filter expressions.
        """
        self.setGlobalsFilter()
        self.setLocalsFilter()
        self.showVariablesTab(False)
        
        self.disassemblyViewer.clear()
        
    def currentWidget(self):
        """
        Public method to get a reference to the current widget.
        
        @return reference to the current widget
        @rtype QWidget
        """
        return self.__tabWidget.currentWidget()
        
    def setCurrentWidget(self, widget):
        """
        Public slot to set the current page based on the given widget.
        
        @param widget reference to the widget
        @type QWidget
        """
        self.__tabWidget.setCurrentWidget(widget)
    
    def __callStackFrameSelected(self, frameNo):
        """
        Private slot to handle the selection of a call stack entry of the
        call stack viewer.
        
        @param frameNo frame number (index) of the selected entry
        @type int
        """
        if frameNo >= 0:
            self.stackComboBox.setCurrentIndex(frameNo)
    
    def __debuggerSelected(self, current, previous):
        """
        Private slot to handle the selection of a debugger backend in the
        debuggers list.
        
        @param current reference to the new current item
        @type QTreeWidgetItem
        @param previous reference to the previous current item
        @type QTreeWidgetItem
        """
        if current is not None and self.__doDebuggersListUpdate:
            if current.parent() is None:
                # it is a debugger item
                debuggerId = current.text(0)
                self.globalsViewer.handleResetUI()
                self.localsViewer.handleResetUI()
                self.currentStack = None
                self.stackComboBox.clear()
                self.callStackViewer.clear()
                
                self.debugServer.remoteSetThread(debuggerId, -1)
                self.__showSource()
            else:
                # it is a thread item
                tid = current.data(0, self.ThreadIdRole)
                self.debugServer.remoteSetThread(
                    self.getSelectedDebuggerId(), tid)
    
    def __clientDebuggerId(self, debuggerId):
        """
        Private slot to receive the ID of a newly connected debugger backend.
        
        @param debuggerId ID of a newly connected debugger backend
        @type str
        """
        itm = QTreeWidgetItem(self.__debuggersList, [debuggerId])
        if self.__debuggersList.topLevelItemCount() > 1:
            self.debugUI.showNotification(
                self.tr("<p>Debugger with ID <b>{0}</b> has been connected."
                        "</p>")
                .format(debuggerId))
        
        self.__debuggersList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        
        if self.__debuggersList.topLevelItemCount() == 1:
            # it is the only item, select it as the current one
            self.__debuggersList.setCurrentItem(itm)
    
    def __setCurrentDebugger(self, debuggerId):
        """
        Private method to set the current debugger based on the given ID.
        
        @param debuggerId ID of the debugger to set as current debugger
        @type str
        """
        debuggerItems = self.__debuggersList.findItems(
            debuggerId, Qt.MatchFlag.MatchExactly)
        if debuggerItems:
            debuggerItem = debuggerItems[0]
            currentItem = self.__debuggersList.currentItem()
            if currentItem is debuggerItem:
                # nothing to do
                return
            
            if currentItem:
                currentParent = currentItem.parent()
            else:
                currentParent = None
            if currentParent is None:
                # current is a debugger item
                self.__debuggersList.setCurrentItem(debuggerItem)
            elif currentParent is debuggerItem:
                # nothing to do
                return
            else:
                self.__debuggersList.setCurrentItem(debuggerItem)
    
    def isOnlyDebugger(self):
        """
        Public method to test, if only one debugger is connected.
        
        @return flag indicating that only one debugger is connected
        @rtype bool
        """
        return self.__debuggersList.topLevelItemCount() == 1
    
    def getSelectedDebuggerId(self):
        """
        Public method to get the currently selected debugger ID.
        
        @return selected debugger ID
        @rtype str
        """
        itm = self.__debuggersList.currentItem()
        if itm:
            if itm.parent() is None:
                # it is a debugger item
                return itm.text(0)
            else:
                # it is a thread item
                return itm.parent().text(0)
        else:
            return ""
    
    def getSelectedDebuggerState(self):
        """
        Public method to get the currently selected debugger's state.
        
        @return selected debugger's state (broken, exception, running)
        @rtype str
        """
        itm = self.__debuggersList.currentItem()
        if itm:
            if itm.parent() is None:
                # it is a debugger item
                return itm.data(0, self.DebuggerStateRole)
            else:
                # it is a thread item
                return itm.parent().data(0, self.DebuggerStateRole)
        else:
            return ""
    
    def __setDebuggerIconAndState(self, debuggerId, state):
        """
        Private method to set the icon for a specific debugger ID.
        
        @param debuggerId ID of the debugger backend (empty ID means the
            currently selected one)
        @type str
        @param state state of the debugger (broken, exception, running)
        @type str
        """
        debuggerItem = None
        if debuggerId:
            foundItems = self.__debuggersList.findItems(
                debuggerId, Qt.MatchFlag.MatchExactly)
            if foundItems:
                debuggerItem = foundItems[0]
        if debuggerItem is None:
            debuggerItem = self.__debuggersList.currentItem()
        if debuggerItem is not None:
            try:
                iconName = DebugViewer.StateIcon[state]
            except KeyError:
                iconName = "question"
            try:
                stateText = DebugViewer.StateMessage[state]
            except KeyError:
                stateText = self.tr("unknown state ({0})").format(state)
            debuggerItem.setIcon(0, UI.PixmapCache.getIcon(iconName))
            debuggerItem.setData(0, self.DebuggerStateRole, state)
            debuggerItem.setText(1, stateText)
            
            self.__debuggersList.header().resizeSections(
                QHeaderView.ResizeMode.ResizeToContents)
    
    def __removeDebugger(self, debuggerId):
        """
        Private method to remove a debugger given its ID.
        
        @param debuggerId ID of the debugger to be removed from the list
        @type str
        """
        foundItems = self.__debuggersList.findItems(
            debuggerId, Qt.MatchFlag.MatchExactly)
        if foundItems:
            index = self.__debuggersList.indexOfTopLevelItem(foundItems[0])
            itm = self.__debuggersList.takeTopLevelItem(index)
            # __IGNORE_WARNING__
            del itm
    
    def __addThreadList(self, currentID, threadList, debuggerId):
        """
        Private method to add the list of threads to a debugger entry.
        
        @param currentID id of the current thread
        @type int
        @param threadList list of dictionaries containing the thread data
        @type list of dict
        @param debuggerId ID of the debugger backend
        @type str
        """
        debugStatus = -1    # i.e. running
        
        debuggerItems = self.__debuggersList.findItems(
            debuggerId, Qt.MatchFlag.MatchExactly)
        if debuggerItems:
            debuggerItem = debuggerItems[0]
            
            currentItem = self.__debuggersList.currentItem()
            if currentItem.parent() is debuggerItem:
                currentChild = currentItem.text(0)
            else:
                currentChild = ""
            self.__doDebuggersListUpdate = False
            debuggerItem.takeChildren()
            for thread in threadList:
                if thread.get('except', False):
                    stateText = DebugViewer.StateMessage["exception"]
                    iconName = DebugViewer.StateIcon["exception"]
                    debugStatus = 1
                elif thread['broken']:
                    stateText = DebugViewer.StateMessage["broken"]
                    iconName = DebugViewer.StateIcon["broken"]
                    if debugStatus < 1:
                        debugStatus = 0
                else:
                    stateText = DebugViewer.StateMessage["running"]
                    iconName = DebugViewer.StateIcon["running"]
                itm = QTreeWidgetItem(debuggerItem,
                                      [thread['name'], stateText])
                itm.setData(0, self.ThreadIdRole, thread['id'])
                itm.setIcon(0, UI.PixmapCache.getIcon(iconName))
                if currentChild == thread['name']:
                    self.__debuggersList.setCurrentItem(itm)
                if thread['id'] == currentID:
                    font = debuggerItem.font(0)
                    font.setItalic(True)
                    itm.setFont(0, font)
            
            debuggerItem.setExpanded(debuggerItem.childCount() > 0)
            
            self.__debuggersList.header().resizeSections(
                QHeaderView.ResizeMode.ResizeToContents)
            self.__debuggersList.header().setStretchLastSection(True)
            self.__doDebuggersListUpdate = True
            
            if debugStatus == -1:
                debuggerState = "running"
            elif debugStatus == 0:
                debuggerState = "broken"
            else:
                debuggerState = "exception"
            self.__setDebuggerIconAndState(debuggerId, debuggerState)
    
    def __setThreadIconAndState(self, debuggerId, threadName, state):
        """
        Private method to set the icon for a specific thread name and
        debugger ID.
        
        @param debuggerId ID of the debugger backend (empty ID means the
            currently selected one)
        @type str
        @param threadName name of the thread signaling the event
        @type str
        @param state state of the debugger (broken, exception, running)
        @type str
        """
        debuggerItem = None
        if debuggerId:
            foundItems = self.__debuggersList.findItems(
                debuggerId, Qt.MatchFlag.MatchExactly)
            if foundItems:
                debuggerItem = foundItems[0]
        if debuggerItem is None:
            debuggerItem = self.__debuggersList.currentItem()
        if debuggerItem is not None:
            for index in range(debuggerItem.childCount()):
                childItem = debuggerItem.child(index)
                if childItem.text(0) == threadName:
                    break
            else:
                childItem = None
            
            if childItem is not None:
                try:
                    iconName = DebugViewer.StateIcon[state]
                except KeyError:
                    iconName = "question"
                try:
                    stateText = DebugViewer.StateMessage[state]
                except KeyError:
                    stateText = self.tr("unknown state ({0})").format(state)
                childItem.setIcon(0, UI.PixmapCache.getIcon(iconName))
                childItem.setText(1, stateText)
            
            self.__debuggersList.header().resizeSections(
                QHeaderView.ResizeMode.ResizeToContents)
