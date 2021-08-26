# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the preferences interface.

The preferences interface consists of a class, which defines the default
values for all configuration items and stores the actual values. These
values are read and written to the eric6 preferences file by module
functions. The data is stored in a file in a subdirectory of the users home
directory. The individual configuration data is accessed by accessor functions
defined on the module level. The module is simply imported wherever it is
needed with the statement 'import Preferences'. Do not use
'from Preferences import *' to import it.
"""

import ast
import os
import fnmatch
import shutil
import json
import sys

from PyQt5.QtCore import (
    QDir, QPoint, QLocale, QSettings, QFileInfo, QCoreApplication, QByteArray,
    QSize, QUrl, Qt, QLibraryInfo, QDateTime
)
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtWidgets import QApplication
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineSettings
except ImportError:
    QWebEngineSettings = None
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

from E5Gui import E5FileDialog

from E5Network.E5Ftp import E5FtpProxyType

import Globals

from Project.ProjectBrowserFlags import (
    SourcesBrowserFlag, FormsBrowserFlag, ResourcesBrowserFlag,
    TranslationsBrowserFlag, InterfacesBrowserFlag, OthersBrowserFlag,
    ProtocolsBrowserFlag, AllBrowsersFlag
)

from QScintilla.Shell import ShellHistoryStyle


class Prefs(object):
    """
    A class to hold all configuration items for the application.
    """
    # defaults for the variables window
    varDefaults = {
        "LocalsFilter": "[]",
        "GlobalsFilter": "[]"
    }
    
    # defaults for the debugger
    debuggerDefaults = {
        "RemoteDbgEnabled": False,
        "RemoteHost": "",
        "RemoteExecution": "",
        "PassiveDbgEnabled": False,
        "PassiveDbgPort": 42424,
        "PassiveDbgType": "Python",
        "AutomaticReset": False,
        "Autosave": True,
        "ThreeStateBreakPoints": False,
        "RecentNumber": 9,
        # max. number of file names to be remembered for the add breakpoint
        # dialog
        "BreakAlways": False,
        "ShowExceptionInShell": True,
        "Python3VirtualEnv": "",
        "RubyInterpreter": "",
        "DebugClientType3": "standard",
        # supported "standard", "custom"
        "DebugClient3": "",
        "DebugEnvironmentReplace": False,
        "DebugEnvironment": "",
        "PythonRedirect": True,
        "PythonNoEncoding": False,
        "Python3Redirect": True,
        "Python3NoEncoding": False,
        "RubyRedirect": True,
        "ConsoleDbgEnabled": False,
        "ConsoleDbgCommand": "",
        "PathTranslation": False,
        "PathTranslationRemote": "",
        "PathTranslationLocal": "",
        "NetworkInterface": "127.0.0.1",
        "AutoViewSourceCode": False,
        "MaxVariableSize": 0,     # Bytes, 0 = no limit
        "BgColorNew": QColor("#28FFEEAA"),
        "BgColorChanged": QColor("#2870FF66"),
        "AllowedHosts": ["127.0.0.1", "::1%0"],
        # space separated list of Python3 extensions
        "Python3Extensions": ".py .pyw .py3 .pyw3",
        # Global Multiprocess Debugging Support
        "MultiProcessEnabled": True,
    }
    
    # defaults for the UI settings
    uiDefaults = {
        "KeyboardInputInterval": 0,         # 0 = use system default
        "BackgroundServiceProcesses": 0,    # 0 = max. CPUs minus one
        "Language": "System",
        "Style": "System",
        "StyleSheet": "",
        "ViewManager": "tabview",
        "LayoutType": "Sidebars",           # "Toolboxes" or "Sidebars"
        "ShellPosition": "bottom",          # "left", "right" or "bottom"
        "SidebarDelay": 200,
        "BrowsersListFoldersFirst": True,
        "BrowsersHideNonPublic": False,
        "BrowsersListContentsByOccurrence": False,
        "BrowsersListHiddenFiles": False,
        "BrowsersFileFilters": "*.py[co];*.so;*.dll",
        "BrowserShowCoding": True,
        "LogViewerAutoRaise": True,
        "LogViewerStdoutFilter": [],
        "LogViewerStderrFilter": [],
        "LogViewerStdxxxFilter": [],
        "SingleApplicationMode": False,
        "CaptionShowsFilename": True,
        "CaptionFilenameLength": 100,
        "RecentNumber": 9,
        "TabViewManagerFilenameLength": 40,
        "TabViewManagerFilenameOnly": True,
        "ShowFilePreview": True,
        "ShowFilePreviewJS": True,
        "ShowFilePreviewSSI": True,
        "ShowTemplateViewer": True,             # left side
        "ShowFileBrowser": True,                # left side
        "ShowSymbolsViewer": True,              # left side
        "ShowCodeDocumentationViewer": True,    # right side
        "ShowPyPIPackageManager": True,         # right side
        "ShowCondaPackageManager": True,        # right side
        "ShowCooperation": True,                # right side
        "ShowIrc": True,                        # right side
        "ShowMicroPython": True,                # right side
        "ShowNumbersViewer": True,              # bottom side
        "ViewProfiles2": {
            "edit": [
                # saved state main window with toolbox windows (0)
                QByteArray(),
                # visibility of the toolboxes/sidebars (1)
                # left, bottom, right
                [True, True, True],
                # saved states of the splitters and sidebars of the
                # sidebars layout (2)
                # left splitter, vertical splitter, left sidebar,
                # bottom sidebar, right splitter, right sidebar
                [QByteArray(), QByteArray(), QByteArray(),
                 QByteArray(), QByteArray(), QByteArray()],
            ],
            "debug": [
                # saved state main window with toolbox windows (0)
                QByteArray(),
                # visibility of the toolboxes/sidebars (1)
                # left, bottom, right
                [False, True, True],
                # saved states of the splitters and sidebars of the
                # sidebars layout (2)
                # left splitter, vertical splitter, left sidebar,
                # bottom sidebar, right splitter, right sidebar
                [QByteArray(), QByteArray(), QByteArray(),
                 QByteArray(), QByteArray(), QByteArray()],
            ],
        },
        "ToolbarManagerState": QByteArray(),
        "PreviewSplitterState": QByteArray(),
        "ShowSplash": True,
        "SplitOrientationVertical": False,
        "UseNativeMenuBar": True,
        
        "PerformVersionCheck": 3,
        # 0 = off
        # 1 = at startup
        # 2 = daily
        # 3 = weekly
        # 4 = monthly
        "UseProxy": False,
        "UseSystemProxy": True,
        "UseHttpProxyForAll": False,
        "ProxyHost/Http": "",
        "ProxyHost/Https": "",
        "ProxyHost/Ftp": "",
        "ProxyPort/Http": 80,
        "ProxyPort/Https": 443,
        "ProxyPort/Ftp": 21,
        "ProxyUser/Http": "",
        "ProxyUser/Https": "",
        "ProxyUser/Ftp": "",
        "ProxyPassword/Http": "",
        "ProxyPassword/Https": "",
        "ProxyPassword/Ftp": "",
        "ProxyType/Ftp": E5FtpProxyType.NoProxy,
        "ProxyAccount/Ftp": "",
        "ProxyExceptions": "localhost,127.0.0.,::1",
        
        "PluginRepositoryUrl6":
        "https://eric-ide.python-projects.org/plugins6/repository.xml",
        "VersionsUrls6": [
            "https://eric-ide.python-projects.org/versions/versions6",
            "https://die-offenbachs.homelinux.org/eric/versions/"
            "versions6",
        ],
        
        "OpenOnStartup": 0,        # 0 = nothing
                                   # 1 = last file
                                   # 2 = last project
                                   # 3 = last multiproject
                                   # 4 = last global session
        "OpenCrashSessionOnStartup": True,
        "CrashSessionEnabled": True,
        
        "DownloadPath": "",
        "RequestDownloadFilename": True,
        "CheckErrorLog": True,
        "MinimumMessageTypeSeverity": 2,    # 0 = QtDebugMsg
                                            # 1 = QtWarningMsg
                                            # 2 = QtCriticalMsg, QtSystemMsg
                                            # 3 = QtFatalMsg
        
        "LogStdErrColour": QColor(Qt.GlobalColor.red),
        "NotificationTimeout": 5,       # time in seconds the notification
                                        # is shown
        "NotificationPosition": QPoint(10, 10),
        "NotificationWarningForeground": "#606000",
        "NotificationWarningBackground": "#ffffd0",
        "NotificationCriticalForeground": "#600000",
        "NotificationCriticalBackground": "#ffd0d0",
        "TextMimeTypes": [
            "application/bookmarks.xbel",
            "application/x-xbel",
            "application/opensearchdescription+xml",
            "application/x-actionscript",
            "application/x-actionscript3",
            "application/x-awk",
            "application/x-sh",
            "application/x-shellscript",
            "application/x-shell-session",
            "application/x-dos-batch",
            "application/x-befunge",
            "application/x-brainfuck",
            "application/x-javascript+cheetah",
            "application/x-javascript+spitfire",
            "application/x-cheetah",
            "application/x-spitfire",
            "application/xml+cheetah",
            "application/xml+spitfire",
            "application/x-clojure",
            "application/x-coldfusion",
            "application/x-cython",
            "application/x-django-templating",
            "application/x-jinja",
            "application/xml-dtd",
            "application/x-ecl",
            "application/x-ruby-templating",
            "application/x-evoque",
            "application/xml+evoque",
            "application/x-fantom",
            "application/x-genshi",
            "application/x-kid",
            "application/x-genshi-text",
            "application/x-gettext",
            "application/x-troff",
            "application/xhtml+xml",
            "application/x-php",
            "application/x-httpd-php",
            "application/x-httpd-php3",
            "application/x-httpd-php4",
            "application/x-httpd-php5",
            "application/x-hybris",
            "application/x-javascript+django",
            "application/x-javascript+jinja",
            "application/x-javascript+ruby",
            "application/x-javascript+genshi",
            "application/javascript",
            "application/x-javascript",
            "application/x-javascript+php",
            "application/x-javascript+smarty",
            "application/json",
            "application/x-jsp",
            "application/x-julia",
            "application/x-httpd-lasso",
            "application/x-httpd-lasso[89]",
            "application/x-httpd-lasso8",
            "application/x-httpd-lasso9",
            "application/x-javascript+lasso",
            "application/xml+lasso",
            "application/x-lua",
            "application/x-javascript+mako",
            "application/x-mako",
            "application/xml+mako",
            "application/x-gooddata-maql",
            "application/x-mason",
            "application/x-moonscript",
            "application/x-javascript+myghty",
            "application/x-myghty",
            "application/xml+myghty",
            "application/x-newlisp",
            "application/x-openedge",
            "application/x-perl",
            "application/postscript",
            "application/x-pypylog",
            "application/x-python3",
            "application/x-python",
            "application/x-qml",
            "application/x-racket",
            "application/x-pygments-tokens",
            "application/x-ruby",
            "application/x-standardml",
            "application/x-scheme",
            "application/x-sh-session",
            "application/x-smarty",
            "application/x-ssp",
            "application/x-tcl",
            "application/x-csh",
            "application/x-urbiscript",
            "application/xml+velocity",
            "application/xquery",
            "application/xml+django",
            "application/xml+jinja",
            "application/xml+ruby",
            "application/xml",
            "application/rss+xml",
            "application/atom+xml",
            "application/xml+php",
            "application/xml+smarty",
            "application/xsl+xml",
            "application/xslt+xml",
            "application/x-desktop",
            
            "image/svg+xml",
        ],
    }
    
    iconsDefaults = {
        "Path": [],
        "DefaultIconsPath": "automatic",
        # automatic, breeze-dark, breeze-light, oxygen
    }
    
    # defaults for the cooperation settings
    cooperationDefaults = {
        "ServerPort": 42000,
        "AutoStartServer": False,
        "TryOtherPorts": True,
        "MaxPortsToTry": 100,
        "AutoAcceptConnections": False,
        "BannedUsers": [],
    }
    
    # defaults for the editor settings
    editorDefaults = {
        "AutosaveInterval": 0,
        "TabWidth": 4,
        "IndentWidth": 4,
        "TabIndentOverride": "{}",      # JSON formatted dictionary
        "IndentationGuides": True,
        "LinenoMargin": True,
        "FoldingMargin": True,
        "FoldingStyle": 1,
        "TabForIndentation": False,
        "TabIndents": True,
        "ConvertTabsOnLoad": False,
        "AutomaticEOLConversion": True,
        "ShowWhitespace": False,
        "WhitespaceSize": 1,
        "ShowEOL": False,
        "UseMonospacedFont": False,
        "WrapLongLinesMode": QsciScintilla.WrapMode.WrapNone,
        "WrapVisualFlag": QsciScintilla.WrapVisualFlag.WrapFlagNone,
        "WrapIndentMode": QsciScintilla.WrapIndentMode.WrapIndentFixed,
        "WrapStartIndent": 0,
        "WarnFilesize": 512,
        "ClearBreaksOnClose": True,
        "StripTrailingWhitespace": False,
        "InsertFinalNewline": True,
        "CommentColumn0": True,
        "OverrideEditAreaColours": False,
        
        "EdgeMode": QsciScintilla.EdgeMode.EdgeNone,
        "EdgeColumn": 80,
        
        "AutoIndentation": True,
        "BraceHighlighting": True,
        "CreateBackupFile": False,
        "CaretLineVisible": False,
        "CaretLineAlwaysVisible": False,
        "CaretWidth": 1,
        "CaretLineFrameWidth": 0,
        "ColourizeSelText": False,
        "CustomSelectionColours": False,
        "ExtendSelectionToEol": False,
        "LineMarkersBackground": True,
        
        "AutoPrepareAPIs": False,
        
        "AutoCompletionEnabled": False,
        "AutoCompletionCaseSensitivity": True,
        "AutoCompletionReplaceWord": False,
        "AutoCompletionShowSingle": False,
        "AutoCompletionSource": QsciScintilla.AutoCompletionSource.AcsDocument,
        "AutoCompletionThreshold": 2,
        # timeout in ms before auto-completion is started
        "AutoCompletionTimeout": 200,
        "AutoCompletionFillups": False,
        # show QScintilla completions, if plug-in fails
        "AutoCompletionScintillaOnFail": False,
        "AutoCompletionReversedList": False,
        "AutoCompletionCacheEnabled": True,
        "AutoCompletionCacheSize": 100,
        "AutoCompletionCacheTime": 300,     # 5 minutes
        "AutoCompletionWatchdogTime": 3000,     # ms
        "AutoCompletionMaxLines": 6,
        "AutoCompletionMaxChars": 40,
        
        "CallTipsEnabled": False,
        "CallTipsVisible": 0,
        "CallTipsStyle": QsciScintilla.CallTipsStyle.CallTipsNoContext,
        # show QScintilla calltips, if plug-in fails
        "CallTipsScintillaOnFail": False,
        
        "AutoCheckSyntax": True,
        "OnlineSyntaxCheck": True,
        "OnlineSyntaxCheckInterval": 5,
        
        "OnlineChangeTrace": True,
        "OnlineChangeTraceInterval": 500,      # 1000 milliseconds
        
        "AutoReopen": False,
        
        "AnnotationsEnabled": True,
        
        "MiniContextMenu": False,
        "HideFormatButtons": True,
        
        "SearchMarkersEnabled": True,
        "QuickSearchMarkersEnabled": True,
        "MarkOccurrencesEnabled": True,
        "MarkOccurrencesTimeout": 500,     # 500 milliseconds
        "SearchRegexpMode": 0,             # 0: POSIX mode, 1: CXX11 mode
        "AdvancedEncodingDetection": True,
        
        "SpellCheckingEnabled": True,
        "AutoSpellCheckingEnabled": True,
        "AutoSpellCheckChunkSize": 30,
        "SpellCheckStringsOnly": True,
        "SpellCheckingMinWordSize": 3,
        "SpellCheckingDefaultLanguage": "en_US",
        "SpellCheckingPersonalWordList": "",
        "SpellCheckingPersonalExcludeList": "",
        "FullSpellCheckExtensions": ["md", "markdown", "rst", "txt"],
        "FullSpellCheckUnknown": False,
        
        "DefaultEncoding": "utf-8",
        "DefaultOpenFilter": QCoreApplication.translate(
            'Lexers', 'Python Files (*.py *.py3)'),
        "DefaultSaveFilter": QCoreApplication.translate(
            'Lexers', "Python3 Files (*.py)"),
        "AdditionalOpenFilters": [],
        "AdditionalSaveFilters": [],
        
        "ZoomFactor": 0,
        
        "PreviewRefreshWaitTimer": 500,     # wait time in milliseconds
        "PreviewHtmlFileNameExtensions": ["html", "htm", "svg", "asp", "kid"],
        "PreviewMarkdownFileNameExtensions": ["md", "markdown"],
        "PreviewRestFileNameExtensions": ["rst"],
        "PreviewQssFileNameExtensions": ["qss"],
        "PreviewRestUseSphinx": False,
        "PreviewMarkdownNLtoBR": False,
        "PreviewMarkdownUsePyMdownExtensions": True,
        "PreviewMarkdownMathJax": True,
        "PreviewMarkdownMermaid": True,
        "PreviewMarkdownHTMLFormat": "HTML5",  # XHTML1, HTML4, HTML5
        "PreviewRestDocutilsHTMLFormat": "HTML5",   # HTML4, HTML5
        
        "VirtualSpaceOptions": QsciScintilla.SCVS_NONE,
        
        "MouseClickHandlersEnabled": True,
        
        "ShowMarkerMapOnRight": True,
        "ShowMarkerChanges": True,
        "ShowMarkerCoverage": True,
        "ShowMarkerSearch": True,
        
        "ShowSourceOutline": True,
        "SourceOutlineWidth": 200,
        "SourceOutlineStepSize": 50,
        "SourceOutlineShowCoding": True,
        
        "DocstringType": "ericdoc",
        "DocstringAutoGenerate": True,
        
        # All (most) lexers
        "AllFoldCompact": True,
        
        # Bash specifics
        "BashFoldComment": True,
        
        # CMake specifics
        "CMakeFoldAtElse": False,
        
        # C++ specifics
        "CppCaseInsensitiveKeywords": False,
        "CppFoldComment": True,
        "CppFoldPreprocessor": False,
        "CppFoldAtElse": False,
        "CppIndentOpeningBrace": False,
        "CppIndentClosingBrace": False,
        "CppDollarsAllowed": True,
        "CppStylePreprocessor": False,
        "CppHighlightTripleQuotedStrings": False,
        "CppHighlightHashQuotedStrings": False,
        "CppHighlightBackQuotedStrings": False,
        "CppHighlightEscapeSequences": False,
        "CppVerbatimStringEscapeSequencesAllowed": False,
        
        # CoffeeScript specifics
        "CoffeScriptFoldComment": False,
        "CoffeeScriptDollarsAllowed": True,
        "CoffeeScriptStylePreprocessor": False,
        
        # CSS specifics
        "CssFoldComment": True,
        "CssHssSupport": False,
        "CssLessSupport": False,
        "CssSassySupport": False,
        
        # D specifics
        "DFoldComment": True,
        "DFoldAtElse": False,
        "DIndentOpeningBrace": False,
        "DIndentClosingBrace": False,
        
        # Gettext specifics
        "PoFoldComment": False,
        
        # HTML specifics
        "HtmlFoldPreprocessor": False,
        "HtmlFoldScriptComments": False,
        "HtmlFoldScriptHeredocs": False,
        "HtmlCaseSensitiveTags": False,
        "HtmlDjangoTemplates": False,
        "HtmlMakoTemplates": False,
        
        # JSON specifics
        "JSONHightlightComments": True,
        "JSONHighlightEscapeSequences": True,
        
        # Pascal specifics
        "PascalFoldComment": True,
        "PascalFoldPreprocessor": False,
        "PascalSmartHighlighting": True,
        
        # Perl specifics
        "PerlFoldComment": True,
        "PerlFoldPackages": True,
        "PerlFoldPODBlocks": True,
        "PerlFoldAtElse": False,
        
        # PostScript specifics
        "PostScriptTokenize": False,
        "PostScriptLevel": 3,
        "PostScriptFoldAtElse": False,
        
        # Povray specifics
        "PovFoldComment": True,
        "PovFoldDirectives": False,
        
        # Properties specifics
        "PropertiesInitialSpaces": True,
        
        # Python specifics
        "PythonBadIndentation": (
            QsciLexerPython.IndentationWarning.Inconsistent
        ),
        "PythonFoldComment": True,
        "PythonFoldString": True,
        "PythonAutoIndent": True,
        "PythonAllowV2Unicode": True,
        "PythonAllowV3Binary": True,
        "PythonAllowV3Bytes": True,
        "PythonFoldQuotes": False,
        "PythonStringsOverNewLineAllowed": False,
        "PythonHighlightSubidentifier": True,
        
        # Ruby specifics
        "RubyFoldComment": False,
        
        # SQL specifics
        "SqlFoldComment": True,
        "SqlBackslashEscapes": False,
        "SqlDottedWords": False,
        "SqlFoldAtElse": False,
        "SqlFoldOnlyBegin": False,
        "SqlHashComments": False,
        "SqlQuotedIdentifiers": False,
        
        # TCL specifics
        "TclFoldComment": False,
        
        # TeX specifics
        "TexFoldComment": False,
        "TexProcessComments": False,
        "TexProcessIf": True,
        
        # VHDL specifics
        "VHDLFoldComment": True,
        "VHDLFoldAtElse": True,
        "VHDLFoldAtBegin": True,
        "VHDLFoldAtParenthesis": True,
        
        # XML specifics
        "XMLStyleScripts": True,
        
        # YAML specifics
        "YAMLFoldComment": False,
    }
    
    if Globals.isWindowsPlatform():
        editorDefaults["EOLMode"] = QsciScintilla.EolMode.EolWindows
    else:
        editorDefaults["EOLMode"] = QsciScintilla.EolMode.EolUnix
    
    try:
        # since QScintilla 2.7.0
        editorDefaults["CallTipsPosition"] = (
            QsciScintilla.CallTipsPosition.CallTipsBelowText
        )
    except AttributeError:
        editorDefaults["CallTipsPosition"] = 0
    
    editorColourDefaults = {
        "CurrentMarker": QColor(Qt.GlobalColor.yellow),
        "ErrorMarker": QColor(Qt.GlobalColor.red),
        "MatchingBrace": QColor(Qt.GlobalColor.green),
        "MatchingBraceBack": QColor(Qt.GlobalColor.white),
        "NonmatchingBrace": QColor(Qt.GlobalColor.red),
        "NonmatchingBraceBack": QColor(Qt.GlobalColor.white),
        "CallTipsBackground": QColor(Qt.GlobalColor.white),
        "CallTipsForeground": QColor("#7f7f7f"),
        "CallTipsHighlight": QColor("#00007f"),
        "CaretForeground": QColor(Qt.GlobalColor.black),
        "CaretLineBackground": QColor(Qt.GlobalColor.white),
        "Edge": QColor(Qt.GlobalColor.lightGray),
        "SelectionBackground": QColor(Qt.GlobalColor.black),
        "SelectionForeground": QColor(Qt.GlobalColor.white),
        "SearchMarkers": QColor(Qt.GlobalColor.blue),
        "MarginsBackground": QColor(Qt.GlobalColor.lightGray),
        "MarginsForeground": QColor(Qt.GlobalColor.black),
        "FoldmarginBackground": QColor("#e6e6e6"),
        "FoldMarkersForeground": QColor(Qt.GlobalColor.white),
        "FoldMarkersBackground": QColor(Qt.GlobalColor.black),
        "SpellingMarkers": QColor(Qt.GlobalColor.red),
        "AnnotationsWarningForeground": QColor("#606000"),
        "AnnotationsWarningBackground": QColor("#ffffd0"),
        "AnnotationsErrorForeground": QColor("#600000"),
        "AnnotationsErrorBackground": QColor("#ffd0d0"),
        "AnnotationsStyleForeground": QColor("#000060"),
        "AnnotationsStyleBackground": QColor("#d0d0ff"),
        "WhitespaceForeground": QColor(Qt.GlobalColor.darkGray),
        "WhitespaceBackground": QColor(Qt.GlobalColor.white),
        "OnlineChangeTraceMarkerUnsaved": QColor("#ff8888"),
        "OnlineChangeTraceMarkerSaved": QColor("#88ff88"),
        "IndentationGuidesBackground": QColor(Qt.GlobalColor.white),
        "IndentationGuidesForeground": QColor(Qt.GlobalColor.black),
        "HighlightMarker": QColor("#200000FF"),     # ARGB format
        # colors for the marker map
        "BookmarksMap": QColor("#f8c700"),
        "ErrorsMap": QColor("#dd0000"),
        "WarningsMap": QColor("#606000"),
        "BreakpointsMap": QColor("#f55c07"),
        "TasksMap": QColor("#2278f8"),
        "CoverageMap": QColor("#ad3636"),
        "ChangesMap": QColor("#00b000"),
        "CurrentMap": QColor("#000000"),
        "SearchMarkersMap": QColor(Qt.GlobalColor.blue),
        "VcsConflictMarkersMap": QColor("#dd00dd"),
        "MarkerMapBackground": QColor("#e7e7e7"),
    }
    
    editorOtherFontsDefaults = {
        "MarginsFont": "Sans Serif,10,-1,5,50,0,0,0,0,0",
        "DefaultFont": "Sans Serif,10,-1,5,50,0,0,0,0,0",
        "MonospacedFont": "Courier,10,-1,5,50,0,0,0,0,0",
    }
    
    editorTypingDefaults = {
        "Python/EnabledTypingAids": True,
        "Python/InsertClosingBrace": True,
        "Python/IndentBrace": False,
        "Python/SkipBrace": True,
        "Python/InsertQuote": True,
        "Python/DedentElse": True,
        "Python/DedentExcept": True,
        "Python/InsertImport": True,
        "Python/ImportBraceType": False,
        "Python/InsertSelf": True,
        "Python/InsertBlank": True,
        "Python/ColonDetection": True,
        "Python/DedentDef": False,
        
        "Ruby/EnabledTypingAids": True,
        "Ruby/InsertClosingBrace": True,
        "Ruby/IndentBrace": True,
        "Ruby/SkipBrace": True,
        "Ruby/InsertQuote": True,
        "Ruby/InsertBlank": True,
        "Ruby/InsertHereDoc": True,
        "Ruby/InsertInlineDoc": True,
        
        "Yaml/EnabledTypingAids": True,
        "Yaml/InsertClosingBrace": True,
        "Yaml/SkipBrace": True,
        "Yaml/InsertQuote": True,
        "Yaml/AutoIndentation": True,
        "Yaml/ColonDetection": True,
        "Yaml/InsertBlankDash": True,
        "Yaml/InsertBlankColon": True,
        "Yaml/InsertBlankQuestion": True,
        "Yaml/InsertBlankComma": True,
    }
    
    editorExporterDefaults = {
        "HTML/WYSIWYG": True,
        "HTML/Folding": False,
        "HTML/OnlyStylesUsed": False,
        "HTML/FullPathAsTitle": False,
        "HTML/UseTabs": False,
        
        "RTF/WYSIWYG": True,
        "RTF/UseTabs": False,
        "RTF/Font": "Courier New,10,-1,5,50,0,0,0,0,0",
        
        "PDF/Magnification": 0,
        "PDF/Font": "Helvetica",  # must be Courier, Helvetica or Times
        "PDF/PageSize": "A4",         # must be A4 or Letter
        "PDF/MarginLeft": 36,
        "PDF/MarginRight": 36,
        "PDF/MarginTop": 36,
        "PDF/MarginBottom": 36,
        
        "TeX/OnlyStylesUsed": False,
        "TeX/FullPathAsTitle": False,
        
        "ODT/WYSIWYG": True,
        "ODT/OnlyStylesUsed": False,
        "ODT/UseTabs": False,
    }
    
    # defaults for the printer settings
    printerDefaults = {
        "PrinterName": "",
        "ColorMode": True,
        "FirstPageFirst": True,
        "Magnification": -3,
        "Orientation": 0,
        "PageSize": 0,
        "HeaderFont": "Serif,10,-1,5,50,0,0,0,0,0",
        "LeftMargin": 1.0,
        "RightMargin": 1.0,
        "TopMargin": 1.0,
        "BottomMargin": 1.0,
        "Resolution": 150,      # printer resolution in DPI
    }
    
    # defaults for the project settings
    projectDefaults = {
        "SearchNewFiles": False,
        "SearchNewFilesRecursively": False,
        "AutoIncludeNewFiles": False,
        "AutoLoadSession": False,
        "AutoSaveSession": False,
        "SessionAllBreakpoints": False,
        "TimestampFile": True,
        "AutoCompileForms": False,
        "AutoCompileResources": False,
        "AutoExecuteMake": False,
        "AutoLoadDbgProperties": False,
        "AutoSaveDbgProperties": False,
        "HideGeneratedForms": False,
        "FollowEditor": True,
        "FollowCursorLine": True,
        "AutoPopulateItems": True,
        "RecentNumber": 9,
        "DeterminePyFromProject": True,
        "TasksProjectAutoSave": True,
        "TasksProjectRescanOnOpen": True,
        "DebugClientsHistory": [],
        "DebuggerInterpreterHistory": [],
        "RestartShellForProject": True,
        "BrowsersListHiddenFiles": False,
    }
    
    # defaults for the multi project settings
    multiProjectDefaults = {
        "OpenMasterAutomatically": True,
        "TimestampFile": True,
        "RecentNumber": 9,
        "Workspace": "",
    }
    
    # defaults for the project browser flags settings
    projectBrowserFlagsDefaults = {
        "PyQt5": (
            SourcesBrowserFlag |
            FormsBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PyQt5C": (
            SourcesBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PyQt6": (
            SourcesBrowserFlag |
            FormsBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PyQt6C": (
            SourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "E6Plugin": (
            SourcesBrowserFlag |
            FormsBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "Console": (
            SourcesBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "Other": (
            SourcesBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PySide2": (
            SourcesBrowserFlag |
            FormsBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PySide2C": (
            SourcesBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PySide6": (
            SourcesBrowserFlag |
            FormsBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
        "PySide6C": (
            SourcesBrowserFlag |
            ResourcesBrowserFlag |
            TranslationsBrowserFlag |
            InterfacesBrowserFlag |
            OthersBrowserFlag |
            ProtocolsBrowserFlag),
    }
    
    # defaults for the project browser colour settings
    projectBrowserColourDefaults = {
        "Highlighted": QColor(Qt.GlobalColor.red),
        
        "VcsAdded": QColor(Qt.GlobalColor.blue),
        "VcsConflict": QColor(Qt.GlobalColor.red),
        "VcsModified": QColor(Qt.GlobalColor.yellow),
        "VcsReplaced": QColor(Qt.GlobalColor.cyan),
        "VcsUpdate": QColor(Qt.GlobalColor.green),
        "VcsRemoved": QColor(Qt.GlobalColor.magenta)
    }
    
    # defaults for the help settings
    helpDefaults = {
        "CustomViewer": "",
        "PythonDocDir": "",
        "Qt5DocDir": "",
        "Qt6DocDir": "",
        "PyQt5DocDir": "https://www.riverbankcomputing.com/static/Docs/PyQt5/",
        "PyQt6DocDir": "",
        "PySide2DocDir": "",
        "PySide6DocDir": "",
        "EricDocDir": "",
    }
    
    # defaults for the web browser settings
    webBrowserDefaults = {
        "SingleWebBrowserWindow": True,
        "ShowToolbars": False,
        "BookmarksToolBarVisible": True,
        "MenuBarVisible": False,
        "StatusBarVisible": True,
        "SaveGeometry": True,
        "WebBrowserState": QByteArray(),
        "StartupBehavior": 2,       # show speed dial
        # 0     open empty page
        # 1     open home page
        # 2     open speed dial
        # 3     restore last session
        # 4     ask user for session
        "NewTabBehavior": 2,        # show speed dial
        # 0     open empty page
        # 1     open home page
        # 2     open speed dial
        "HomePage": "eric:home",
        "LoadTabOnActivation": True,
        "WarnOnMultipleClose": True,
        "DefaultScheme": "https://",
        "UserStyleSheet": "",
        "ZoomValuesDB": "{}",       # empty JSON dictionary
        "HistoryLimit": 30,
        "WebSearchSuggestions": True,
        "WebSearchEngine": "DuckDuckGo",
        "WebSearchKeywords": [],    # array of two tuples (keyword,
                                    # search engine name)
        "SearchLanguage": QLocale().language(),
        "ImageSearchEngine": "Google",
        "RssFeeds": [],
        "ShowPreview": True,
        "DiskCacheEnabled": True,
        "DiskCacheSize": 50,        # 50 MB
        "SslExceptionsDB": "{}",    # empty JSON dictionary
        "AlwaysRejectFaultyCertificates": False,
        "DoNotTrack": False,
        "RefererSendReferer": 2,        # send always
        "RefererDefaultPolicy": 3,      # don't send a referer when downgrading
        "RefererTrimmingPolicy": 0,     # send full URL (no trimming)
        "SendRefererWhitelist": ["qt-apps.org", "kde-apps.org"],
        "AcceptCookies": 2,         # CookieJar.AcceptOnlyFromSitesNavigatedTo
        "KeepCookiesUntil": 0,      # CookieJar.KeepUntilExpire
        "FilterTrackingCookies": True,
        "SecureUrlColor": QColor(184, 248, 169),
        "InsecureUrlColor": QColor(248, 227, 169),
        "MaliciousUrlColor": QColor(255, 132, 140),
        "PrivateModeUrlColor": QColor(220, 220, 220),
        "UserAgent": "",
        "AcceptQuotaRequest": 2,            # yes/no/ask (0, 1, 2)
        "AcceptProtocolHandlerRequest": 2,  # yes/no/ask (0, 1, 2)
        # Auto Scroller
        "AutoScrollEnabled": True,
        "AutoScrollDivider": 8.0,
        # Tab Manager
        "TabManagerGroupByType": 0,     # TabManagerWidget.GroupByWindow
        # Grease Monkey
        "GreaseMonkeyDisabledScripts": [],
        # Downloads
        "DownloadManagerRemovePolicy": 0,      # never delete downloads
        "DownloadManagerSize": QSize(450, 600),
        "DownloadManagerPosition": QPoint(),
        "DownloadManagerDownloads": [],
        "DownloadManagerAutoOpen": False,
        "DownloadManagerAutoClose": False,
        # Spell Checking
        "SpellCheckEnabled": False,
        "SpellCheckLanguages": [],
        "SpellCheckDictionariesUrl":
        ("https://eric-ide.python-projects.org/qwebengine_dictionaries/"
         "dictionaries.xml"),
        # Sync
        "SyncEnabled": False,
        "SyncBookmarks": True,
        "SyncHistory": True,
        "SyncPasswords": False,
        "SyncUserAgents": True,
        "SyncSpeedDial": True,
        "SyncEncryptData": False,
        "SyncEncryptionKey": "",
        "SyncEncryptionKeyLength": 32,      # 16, 24 or 32
        "SyncEncryptPasswordsOnly": False,
        "SyncType": 0,
        "SyncFtpServer": "",
        "SyncFtpUser": "",
        "SyncFtpPassword": "",
        "SyncFtpPath": "",
        "SyncFtpPort": 21,
        "SyncFtpIdleTimeout": 30,
        "SyncDirectoryPath": "",
        # AdBlock
        "AdBlockEnabled": False,
        "AdBlockSubscriptions": [],
        "AdBlockUpdatePeriod": 1,
        "AdBlockExceptions": [],
        "AdBlockUseLimitedEasyList": True,
        # PIM:
        "PimFullName": "",
        "PimFirstName": "",
        "PimLastName": "",
        "PimEmail": "",
        "PimPhone": "",
        "PimMobile": "",
        "PimAddress": "",
        "PimCity": "",
        "PimZip": "",
        "PimState": "",
        "PimCountry": "",
        "PimHomePage": "",
        "PimSpecial1": "",
        "PimSpecial2": "",
        "PimSpecial3": "",
        "PimSpecial4": "",
        # VirusTotal:
        "VirusTotalEnabled": False,
        "VirusTotalServiceKey": "",
        "VirusTotalSecure": True,
        # Sessions
        "SessionAutoSave": True,
        "SessionAutoSaveInterval": 15,  # interval in seconds
        "SessionLastActivePath": "",
        # Google Safe Browsing
        "SafeBrowsingEnabled": True,
        "SafeBrowsingApiKey": "",       # API key
        "SafeBrowsingFilterPlatform": True,
        "SafeBrowsingAutoUpdate": False,
        "SafeBrowsingUpdateDateTime": QDateTime(),
        "SafeBrowsingUseLookupApi": False,
    }
    if QWebEngineSettings:
        webBrowserDefaults["HelpViewerType"] = 1      # eric browser
    else:
        webBrowserDefaults["HelpViewerType"] = 2      # Qt Assistant
    
    @classmethod
    def initWebEngineSettingsDefaults(cls):
        """
        Class method to initialize the web engine settings related defaults.
        """
        if QWebEngineSettings is None:
            return
        
        webEngineSettings = QWebEngineSettings.defaultSettings()
        cls.webBrowserDefaults.update({
            "StandardFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.StandardFont),
            "FixedFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.FixedFont),
            "SerifFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.StandardFont),
            "SansSerifFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.SansSerifFont),
            "CursiveFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.CursiveFont),
            "FantasyFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.FantasyFont),
            "DefaultFontSize": webEngineSettings.fontSize(
                QWebEngineSettings.FontSize.DefaultFontSize),
            "DefaultFixedFontSize": webEngineSettings.fontSize(
                QWebEngineSettings.FontSize.DefaultFixedFontSize),
            "MinimumFontSize": webEngineSettings.fontSize(
                QWebEngineSettings.FontSize.MinimumFontSize),
            "MinimumLogicalFontSize": webEngineSettings.fontSize(
                QWebEngineSettings.FontSize.MinimumLogicalFontSize),
            "AutoLoadImages": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.AutoLoadImages),
            "JavaScriptEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.JavascriptEnabled),
            "JavaScriptCanOpenWindows": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows),
            "JavaScriptCanAccessClipboard": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard),
            "PluginsEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.PluginsEnabled),
            "LocalStorageEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.LocalStorageEnabled),
            "DefaultTextEncoding": webEngineSettings.defaultTextEncoding(),
            "SpatialNavigationEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.SpatialNavigationEnabled),
            "LinksIncludedInFocusChain": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.LinksIncludedInFocusChain),
            "LocalContentCanAccessRemoteUrls": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute
                .LocalContentCanAccessRemoteUrls),
            "LocalContentCanAccessFileUrls": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls),
            "XSSAuditingEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.XSSAuditingEnabled),
            "ScrollAnimatorEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled),
            "ErrorPageEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.ErrorPageEnabled),
            "FullScreenSupportEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.FullScreenSupportEnabled),
            "PictographFontFamily": webEngineSettings.fontFamily(
                QWebEngineSettings.FontFamily.PictographFont),
            "ScreenCaptureEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.ScreenCaptureEnabled),
            "WebGLEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.WebGLEnabled),
            "FocusOnNavigationEnabled": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled),
            "PrintElementBackgrounds": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.PrintElementBackgrounds),
            "AllowRunningInsecureContent": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.AllowRunningInsecureContent),
            "AllowGeolocationOnInsecureOrigins":
                webEngineSettings.testAttribute(
                    QWebEngineSettings.WebAttribute
                    .AllowGeolocationOnInsecureOrigins),
            "AllowWindowActivationFromJavaScript":
                webEngineSettings.testAttribute(
                    QWebEngineSettings.WebAttribute
                    .AllowWindowActivationFromJavaScript),
            "ShowScrollBars": webEngineSettings.testAttribute(
                QWebEngineSettings.WebAttribute.ShowScrollBars),
            "PlaybackRequiresUserGesture":
                webEngineSettings.testAttribute(
                    QWebEngineSettings.WebAttribute
                    .PlaybackRequiresUserGesture),
            "JavaScriptCanPaste":
                webEngineSettings.testAttribute(
                    QWebEngineSettings.WebAttribute.JavascriptCanPaste),
            "WebRTCPublicInterfacesOnly":
                webEngineSettings.testAttribute(
                    QWebEngineSettings.WebAttribute
                    .WebRTCPublicInterfacesOnly),
            "DnsPrefetchEnabled":
                webEngineSettings.testAttribute(
                    QWebEngineSettings.WebAttribute.DnsPrefetchEnabled),
        })
        try:
            # Qt 5.13
            cls.webBrowserDefaults.update({
                "PdfViewerEnabled":
                    webEngineSettings.testAttribute(
                        QWebEngineSettings.WebAttribute.PdfViewerEnabled),
            })
        except AttributeError:
            pass
        
        cls.webEngineSettingsIntitialized = True
    
    webEngineSettingsIntitialized = False

    # defaults for system settings
    sysDefaults = {
        "StringEncoding": "utf-8",
        "IOEncoding": "utf-8",
    }
    
    # defaults for the shell settings
    shellDefaults = {
        "LinenoMargin": True,
        "AutoCompletionEnabled": True,
        "CallTipsEnabled": True,
        "WrapEnabled": True,
        "MaxHistoryEntries": 100,
        "HistoryStyle": ShellHistoryStyle.LinuxStyle,
        "HistoryWrap": False,
        "HistoryNavigateByCursor": False,
        "SyntaxHighlightingEnabled": True,
        "ShowStdOutErr": True,
        "UseMonospacedFont": False,
        "MonospacedFont": "Courier,10,-1,5,50,0,0,0,0,0",
        "MarginsFont": "Sans Serif,10,-1,5,50,0,0,0,0,0",
        "LastVirtualEnvironment": "",
        "StartWithMostRecentlyUsedEnvironment": True,
    }

    # defaults for Qt related stuff
    qtDefaults = {
        "Qt5TranslationsDir": "",
        "QtToolsDir": "",
        "QtToolsPrefix": "",
        "QtToolsPostfix": "",
        "PyuicIndent": 4,
        "PyuicFromImports": False,
        "PyuicExecute": True,
        "PyQtVenvName": "",
        "PyQtToolsDir": "",
        "Pyuic6Indent": 4,
        "Pyuic6Execute": True,
        "PyQt6VenvName": "",
        "PyQt6ToolsDir": "",
        "PySide2FromImports": False,
        "PySide2VenvName": "",
        "PySide2ToolsDir": "",
        "PySide6FromImports": False,
        "PySide6VenvName": "",
        "PySide6ToolsDir": "",
    }
    
    # defaults for corba related stuff
    corbaDefaults = {
        "omniidl": ""
    }
    
    # defaults for protobuf related stuff
    protobufDefaults = {
        "protoc": "",
        "grpcPython": "",
    }
    
    # defaults for user related stuff
    userDefaults = {
        "Email": "",
        "MailServer": "",
        "Signature": "",
        "MailServerAuthentication": False,
        "MailServerUser": "",
        "MailServerPassword": "",
        "MailServerEncryption": "No",   # valid values: No, SSL, TLS
        "MailServerPort": 25,
        "UseSystemEmailClient": False,
        "UseGoogleMailOAuth2": False,
        "MasterPassword": "",           # stores the password hash
        "UseMasterPassword": False,
        "SavePasswords": False,
    }
    
    # defaults for vcs related stuff
    vcsDefaults = {
        "AutoClose": False,
        "AutoSaveFiles": True,
        "AutoSaveProject": True,
        "AutoUpdate": False,
        "StatusMonitorInterval": 30,
        "MonitorLocalStatus": False,
        "ShowVcsToolbar": True,
    }
    
    # defaults for tasks related stuff
    tasksDefaults = {
        "TasksFixmeMarkers": "FIX" + "ME:",
        "TasksWarningMarkers": "WARN" + "ING:",
        "TasksTodoMarkers": "TO" + "DO:",
        "TasksNoteMarkers": "NO" + "TE:",
        "TasksTestMarkers": "TE" + "ST:",
        "TasksDocuMarkers": "DO" + "CU:",
        # needed to keep it from being recognized as a task
        "TasksFixmeColor": QColor("#FFA0A0"),
        "TasksWarningColor": QColor("#FFFFA0"),
        "TasksTodoColor": QColor("#A0FFA0"),
        "TasksNoteColor": QColor("#A0A0FF"),
        "TasksTestColor": QColor("#FFD000"),
        "TasksDocuColor": QColor("#FFA0FF"),
        "ClearOnFileClose": True,
    }
    
    # defaults for templates related stuff
    templatesDefaults = {
        "AutoOpenGroups": True,
        "SingleDialog": False,
        "ShowTooltip": False,
        "SeparatorChar": "$",
        "EditorFont": "Monospace,9,-1,5,50,0,0,0,0,0",
    }
    
    # defaults for plugin manager related stuff
    pluginManagerDefaults = {
        "ActivateExternal": True,
        "DownloadPath": "",
        "UpdatesCheckInterval": 3,
        # 0 = off
        # 1 = daily
        # 2 = weekly
        # 3 = monthly
        # 4 = always
        "CheckInstalledOnly": True,
        # list of plug-ins not to shown in the repo dialog
        "HiddenPlugins": [],
        # parameters for housekeeping
        "KeepGenerations": 2,
        "KeepHidden": False,
        "StartupCleanup": True,
    }
    
    # defaults for the printer settings
    graphicsDefaults = {
        "Font": "SansSerif,10,-1,5,50,0,0,0,0,0",
        "DrawingMode": "automatic",
        # automatic - determine mode depending upon desktop scheme
        # black_white - black items on white background
        # white_black - white items on black background
    }
    
    # defaults for the icon editor
    iconEditorDefaults = {
        "IconEditorState": QByteArray(),
    }
    
    # defaults for pyflakes
    pyflakesDefaults = {
        "IncludeInSyntaxCheck": True,
        "IgnoreStarImportWarnings": True,
    }
    
    # defaults for tray starter
    trayStarterDefaults = {
        "TrayStarterIcon": "erict",
        # valid values are: erict, erict-hc,
        #                   erict-bw, erict-bwi
    }
    
    # defaults for geometry
    geometryDefaults = {
        "HelpViewerGeometry": QByteArray(),
        "HelpInspectorGeometry": QByteArray(),
        "WebBrowserGeometry": QByteArray(),
        "IconEditorGeometry": QByteArray(),
        "HexEditorGeometry": QByteArray(),
        "MainGeometry": QByteArray(),
        "MainMaximized": False,
        "WebInspectorGeometry": QByteArray(),
    }

    # if true, revert layouts to factory defaults
    resetLayout = False
    
    # defaults for IRC
    ircDefaults = {
        "ShowTimestamps": True,
        "TimestampIncludeDate": False,
        "TimeFormat": "hh:mm",
        "DateFormat": "yyyy-MM-dd",
        
        "NetworkMessageColour": "#000055",
        "ServerMessageColour": "#91640A",
        "ErrorMessageColour": "#FF0000",
        "TimestampColour": "#709070",
        "HyperlinkColour": "#0000FF",
        "ChannelMessageColour": "#000000",
        "OwnNickColour": "#000000",
        "NickColour": "#18B33C",
        "JoinChannelColour": "#72D672",
        "LeaveChannelColour": "#B00000",
        "ChannelInfoColour": "#9E54B3",
        
        "EnableIrcColours": True,
        "IrcColor0": "#FFFF00",
        "IrcColor1": "#000000",
        "IrcColor2": "#000080",
        "IrcColor3": "#008000",
        "IrcColor4": "#FF0000",
        "IrcColor5": "#A52A2A",
        "IrcColor6": "#800080",
        "IrcColor7": "#FF8000",
        "IrcColor8": "#808000",
        "IrcColor9": "#00FF00",
        "IrcColor10": "#008080",
        "IrcColor11": "#00FFFF",
        "IrcColor12": "#0000FF",
        "IrcColor13": "#FFC0CB",
        "IrcColor14": "#A0A0A0",
        "IrcColor15": "#C0C0C0",
        
        "ShowNotifications": True,
        "NotifyJoinPart": True,
        "NotifyMessage": False,
        "NotifyNick": False,
        
        "AutoUserInfoLookup": True,
        "AutoUserInfoMax": 200,
        "AutoUserInfoInterval": 90,
        
        "MarkPositionWhenHidden": True,
        "MarkerLineForegroundColour": "#000000",    # Black on
        "MarkerLineBackgroundColour": "#ffff00",    # Yellow
        
        "AskOnShutdown": True,
    }
    
    # defaults for Hex Editor
    hexEditorDefaults = {
        "HexEditorState": QByteArray(),
        "AddressAreaWidth": 4,
        "ShowAddressArea": True,
        "ShowAsciiArea": True,
        "OpenInOverwriteMode": True,
        "OpenReadOnly": False,
        "HighlightChanges": True,
        "HighlightingBackGround": QColor(0xff, 0xff, 0x99, 0xff),
        "HighlightingForeGround": QColor(Qt.GlobalColor.black),
        "SelectionBackGround": QColor("#308cc6"),
        "SelectionForeGround": QColor(Qt.GlobalColor.white),
        "AddressAreaBackGround": QColor("#efedec"),
        "AddressAreaForeGround": QColor(Qt.GlobalColor.black),
        "RecentNumber": 9,
    }
    if Globals.isWindowsPlatform():
        hexEditorDefaults["Font"] = "Courier,10,-1,5,50,0,0,0,0,0"
    else:
        hexEditorDefaults["Font"] = "Monospace,10,-1,5,50,0,0,0,0,0"
    
    # defaults for Diff colors
    diffColourDefaults = {
        "TextColor": QColor(0, 0, 0),
        "AddedColor": QColor(190, 237, 190),
        "RemovedColor": QColor(237, 190, 190),
        "ReplacedColor": QColor(190, 190, 237),
        "ContextColor": QColor(255, 220, 168),
        "HeaderColor": QColor(237, 237, 190),
        "BadWhitespaceColor": QColor(255, 0, 0, 192),
    }
    
    # defaults for Code Documentation Viewer
    docuViewerDefaults = {
        "ShowInfoAsRichText": False,
        "Provider": "disabled",
        "ShowInfoOnOpenParenthesis": True,
    }
    
    # defaults for conda
    condaDefaults = {
        "CondaExecutable": "",
    }
    
    # defaults for pip
    pipDefaults = {
        "PipSearchIndex": "",               # used by the search command
        "ExcludeCondaEnvironments": True,
        # don't show conda environments in selector
    }
    
    # defaults for MicroPython
    microPythonDefaults = {
        "MpyWorkspace": "",
        "SerialTimeout": 2000,          # timeout in milliseconds
        "ReplLineWrap": True,           # wrap the REPL lines
        "SyncTimeAfterConnect": True,
        "ShowHiddenLocal": True,
        "ShowHiddenDevice": True,
        "ChartColorTheme": -1,          # -1 = automatic,
                                        # QChart.ChartTheme otherwise
        "MpyCrossCompiler": "",         # path of the mpy-cross compiler
        "DfuUtilPath": "",              # path of the dfu-util flashing tool
        "IgnoredUnknownDevices": "[]",  # empty list encoded as JSON
        "ManualDevices": "[]",          # empty list encoded as JSON
        
        # MicroPython URLs
        "MicroPythonDocuUrl":
            "https://docs.micropython.org/en/latest/",
        "MicroPythonFirmwareUrl":
            "http://micropython.org/download/",
        
        # CircuitPython URLS
        "CircuitPythonDocuUrl":
            "https://circuitpython.readthedocs.io/en/latest/",
        "CircuitPythonFirmwareUrl":
            "https://circuitpython.org/downloads/",
        "CircuitPythonLibrariesUrl":
            "https://circuitpython.org/libraries",
        
        # BBC micro:bit URLs
        "MicrobitDocuUrl":
            "https://microbit-micropython.readthedocs.io/en/latest/",
        "MicrobitFirmwareUrl":
            "https://microbit.org/guide/firmware/",
        "MicrobitMicroPythonUrl":
            "https://github.com/bbcmicrobit/micropython/releases/",
        "MicrobitV2MicroPythonUrl":
            "https://github.com/microbit-foundation/micropython-microbit-v2/"
            "releases/",
        
        # calliope mini URLS
        "CalliopeDocuUrl":
            "https://github.com/calliope-mini/calliope-mini-micropython/",
        "CalliopeDAPLinkUrl":
            "https://github.com/calliope-mini/production-test/releases/",
        "CalliopeMicroPythonUrl":
            "https://github.com/calliope-mini/calliope-mini-micropython/",
    }
    if Globals.isWindowsPlatform():
        microPythonDefaults["ColorScheme"] = "Windows 10"
    elif Globals.isMacPlatform():
        microPythonDefaults["ColorScheme"] = "xterm"
    else:
        microPythonDefaults["ColorScheme"] = "Ubuntu"
    
    # defaults for Python specific settings
    pythonDefaults = {
        "ASTViewerErrorColor": QColor(Qt.GlobalColor.darkRed),
        
        "DisViewerErrorColor": QColor(Qt.GlobalColor.darkRed),
        "DisViewerCurrentColor": QColor(Qt.GlobalColor.darkMagenta),
        "DisViewerLabeledColor": QColor(Qt.GlobalColor.darkGreen),
        "DisViewerExpandCodeInfoDetails": False,
    }


def readToolGroups(prefClass=Prefs):
    """
    Module function to read the tool groups configuration.
    
    @param prefClass preferences class used as the storage area
    @return list of tuples defing the tool groups
    """
    toolGroups = []
    groups = int(prefClass.settings.value("Toolgroups/Groups", 0))
    for groupIndex in range(groups):
        groupName = prefClass.settings.value(
            "Toolgroups/{0:02d}/Name".format(groupIndex))
        group = [groupName, []]
        items = int(prefClass.settings.value(
            "Toolgroups/{0:02d}/Items".format(groupIndex), 0))
        for ind in range(items):
            menutext = prefClass.settings.value(
                "Toolgroups/{0:02d}/{1:02d}/Menutext".format(groupIndex, ind))
            icon = prefClass.settings.value(
                "Toolgroups/{0:02d}/{1:02d}/Icon".format(groupIndex, ind))
            executable = prefClass.settings.value(
                "Toolgroups/{0:02d}/{1:02d}/Executable".format(
                    groupIndex, ind))
            arguments = prefClass.settings.value(
                "Toolgroups/{0:02d}/{1:02d}/Arguments".format(groupIndex, ind))
            redirect = prefClass.settings.value(
                "Toolgroups/{0:02d}/{1:02d}/Redirect".format(groupIndex, ind))
            
            if menutext:
                if menutext == '--':
                    tool = {
                        'menutext': '--',
                        'icon': '',
                        'executable': '',
                        'arguments': '',
                        'redirect': 'no',
                    }
                    group[1].append(tool)
                elif executable:
                    tool = {
                        'menutext': menutext,
                        'icon': icon,
                        'executable': executable,
                        'arguments': arguments,
                        'redirect': redirect,
                    }
                    group[1].append(tool)
        toolGroups.append(group)
    currentGroup = int(
        prefClass.settings.value("Toolgroups/Current Group", -1))
    return toolGroups, currentGroup
    

def saveToolGroups(toolGroups, currentGroup, prefClass=Prefs):
    """
    Module function to write the tool groups configuration.
    
    @param toolGroups reference to the list of tool groups
    @param currentGroup index of the currently selected tool group (integer)
    @param prefClass preferences class used as the storage area
    """
    # first step, remove all tool group entries
    prefClass.settings.remove("Toolgroups")
    
    # second step, write the tool group entries
    prefClass.settings.setValue("Toolgroups/Groups", len(toolGroups))
    groupIndex = 0
    for group in toolGroups:
        prefClass.settings.setValue(
            "Toolgroups/{0:02d}/Name".format(groupIndex), group[0])
        prefClass.settings.setValue(
            "Toolgroups/{0:02d}/Items".format(groupIndex), len(group[1]))
        ind = 0
        for tool in group[1]:
            prefClass.settings.setValue(
                "Toolgroups/{0:02d}/{1:02d}/Menutext".format(groupIndex, ind),
                tool['menutext'])
            prefClass.settings.setValue(
                "Toolgroups/{0:02d}/{1:02d}/Icon".format(groupIndex, ind),
                tool['icon'])
            prefClass.settings.setValue(
                "Toolgroups/{0:02d}/{1:02d}/Executable".format(
                    groupIndex, ind),
                tool['executable'])
            prefClass.settings.setValue(
                "Toolgroups/{0:02d}/{1:02d}/Arguments".format(groupIndex, ind),
                tool['arguments'])
            prefClass.settings.setValue(
                "Toolgroups/{0:02d}/{1:02d}/Redirect".format(groupIndex, ind),
                tool['redirect'])
            ind += 1
        groupIndex += 1
    prefClass.settings.setValue("Toolgroups/Current Group", currentGroup)
    

def initPreferences():
    """
    Module function to initialize the central configuration store.
    """
    from E5Gui.E5Application import e5App
    Prefs.settings = QSettings(
        QSettings.Format.IniFormat, QSettings.Scope.UserScope,
        Globals.settingsNameOrganization, Globals.settingsNameGlobal,
        e5App())
    if not Globals.isWindowsPlatform():
        hp = QDir.homePath()
        dn = QDir(hp)
        dn.mkdir(".eric6")
    QCoreApplication.setOrganizationName(Globals.settingsNameOrganization)
    QCoreApplication.setApplicationName(Globals.settingsNameGlobal)
    try:
        Prefs.settings.setAtomicSyncRequired(False)
    except AttributeError:
        # backward compatibility fot Qt < 5.10
        pass
    
    Prefs.settings.value("UI/SingleApplicationMode")
    

def syncPreferences(prefClass=Prefs):
    """
    Module function to sync the preferences to disk.
    
    In addition to syncing, the central configuration store is reinitialized
    as well.
    
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("General/Configured", True)
    prefClass.settings.sync()
    

def exportPreferences(prefClass=Prefs):
    """
    Module function to export the current preferences.
    
    @param prefClass preferences class used as the storage area
    """
    filename, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
        None,
        QCoreApplication.translate("Preferences", "Export Preferences"),
        "",
        QCoreApplication.translate(
            "Preferences",
            "Properties File (*.ini);;All Files (*)"),
        None,
        E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
    if filename:
        ext = QFileInfo(filename).suffix()
        if not ext:
            ex = selectedFilter.split("(*")[1].split(")")[0]
            if ex:
                filename += ex
        settingsFile = prefClass.settings.fileName()
        prefClass.settings = None
        shutil.copy(settingsFile, filename)
        initPreferences()


def importPreferences(prefClass=Prefs):
    """
    Module function to import preferences from a file previously saved by
    the export function.
    
    @param prefClass preferences class used as the storage area
    """
    filename = E5FileDialog.getOpenFileName(
        None,
        QCoreApplication.translate("Preferences", "Import Preferences"),
        "",
        QCoreApplication.translate(
            "Preferences",
            "Properties File (*.ini);;All Files (*)"))
    if filename:
        settingsFile = prefClass.settings.fileName()
        shutil.copy(filename, settingsFile)
        initPreferences()


def isConfigured(prefClass=Prefs):
    """
    Module function to check, if the the application has been configured.
    
    @param prefClass preferences class used as the storage area
    @return flag indicating the configured status (boolean)
    """
    return toBool(prefClass.settings.value("General/Configured", False))
    

def initRecentSettings():
    """
    Module function to initialize the central configuration store for recently
    opened files and projects.
    
    This function is called once upon import of the module.
    """
    Prefs.rsettings = QSettings(
        QSettings.Format.IniFormat, QSettings.Scope.UserScope,
        Globals.settingsNameOrganization, Globals.settingsNameRecent)
    

def getVarFilters(prefClass=Prefs):
    """
    Module function to retrieve the variables filter settings.
    
    @param prefClass preferences class used as the storage area
    @return a tuple defining the variables filter
    """
    localsFilter = ast.literal_eval(prefClass.settings.value(
        "Variables/LocalsFilter", prefClass.varDefaults["LocalsFilter"]))
    globalsFilter = ast.literal_eval(prefClass.settings.value(
        "Variables/GlobalsFilter", prefClass.varDefaults["GlobalsFilter"]))
    return (localsFilter, globalsFilter)
    

def setVarFilters(filters, prefClass=Prefs):
    """
    Module function to store the variables filter settings.
    
    @param filters variable filters to set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Variables/LocalsFilter", str(filters[0]))
    prefClass.settings.setValue("Variables/GlobalsFilter", str(filters[1]))
    

def getDebugger(key, prefClass=Prefs):
    """
    Module function to retrieve the debugger settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested debugger setting
    """
    if key in ["RemoteDbgEnabled", "PassiveDbgEnabled",
               "AutomaticReset", "DebugEnvironmentReplace",
               "PythonRedirect", "PythonNoEncoding",
               "Python3Redirect", "Python3NoEncoding",
               "RubyRedirect",
               "ConsoleDbgEnabled", "PathTranslation",
               "Autosave", "ThreeStateBreakPoints",
               "BreakAlways", "AutoViewSourceCode",
               "ShowExceptionInShell", "MultiProcessEnabled",
               ]:
        return toBool(prefClass.settings.value(
            "Debugger/" + key, prefClass.debuggerDefaults[key]))
    elif key in ["PassiveDbgPort", "MaxVariableSize", "RecentNumber"]:
        return int(
            prefClass.settings.value(
                "Debugger/" + key, prefClass.debuggerDefaults[key]))
    elif key in ["AllowedHosts"]:
        return toList(
            prefClass.settings.value(
                "Debugger/" + key, prefClass.debuggerDefaults[key]))
    elif key in ["PythonInterpreter", "Python3Interpreter"]:
        # This code is here to ensure backward compatibility.
        # Keep "PythonInterpreter" for backward compatibility.
        newKey = "Python3VirtualEnv"
        venvName = prefClass.settings.value(
            "Debugger/" + newKey, prefClass.debuggerDefaults[newKey])
        if venvName:
            try:
                from E5Gui.E5Application import e5App
                virtualenvManager = e5App().getObject("VirtualEnvManager")
            except KeyError:
                from VirtualEnv.VirtualenvManager import VirtualenvManager
                virtualenvManager = VirtualenvManager()
            interpreter = virtualenvManager.getVirtualenvInterpreter(venvName)
        else:
            interpreter = ""
        if not interpreter:
            return sys.executable
        return interpreter
    elif key == "DebugClientType3":
        debugClientType = prefClass.settings.value(
            "Debugger/" + key, prefClass.debuggerDefaults[key])
        # Correct obsolete entry "threaded"
        if debugClientType == 'threaded':
            return "standard"
        else:
            return debugClientType
    elif key == "PythonExtensions":
        # we don't support Python2 anymore
        return ""
    elif key == "Python2VirtualEnv":
        # we don't support Python2 anymore
        return ""
    else:
        return prefClass.settings.value(
            "Debugger/" + key, prefClass.debuggerDefaults[key])
    

def setDebugger(key, value, prefClass=Prefs):
    """
    Module function to store the debugger settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Debugger/" + key, value)


def getPython(key, prefClass=Prefs):
    """
    Module function to retrieve the Python settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested debugger setting
    """
    if key == "PythonExtensions":
        # we don't support Python2 anymore
        return []
    
    if key == "Python3Extensions":
        exts = []
        for ext in getDebugger(key, prefClass).split():
            if ext.startswith("."):
                exts.append(ext)
            else:
                exts.append(".{0}".format(ext))
        return exts
    elif key in (
        "ASTViewerErrorColor", "DisViewerErrorColor",
        "DisViewerCurrentColor", "DisViewerLabeledColor",
    ):
        return QColor(prefClass.settings.value(
            "Python/" + key, prefClass.pythonDefaults[key]))
    elif key in ("DisViewerExpandCodeInfoDetails"):
        return toBool(prefClass.settings.value(
            "Python/" + key, prefClass.pythonDefaults[key]))
    else:
        return prefClass.settings.value(
            "Python/" + key, prefClass.pythonDefaults[key])


def setPython(key, value, prefClass=Prefs):
    """
    Module function to store the Python settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key == "Python3Extensions":
        setDebugger(key, value, prefClass)
    elif key in (
        "ASTViewerErrorColor", "DisViewerErrorColor",
        "DisViewerCurrentColor", "DisViewerLabeledColor",
    ):
        if value.alpha() < 255:
            val = "#{0:8x}".format(value.rgba())
        else:
            val = value.name()
        prefClass.settings.setValue("Python/" + key, val)
    else:
        prefClass.settings.setValue("Python/" + key, value)


def getUILanguage(prefClass=Prefs):
    """
    Module function to retrieve the language for the user interface.
    
    @param prefClass preferences class used as the storage area
    @return the language for the UI
    """
    lang = prefClass.settings.value("UI/Language",
                                    prefClass.uiDefaults["Language"])
    if lang == "None" or lang == "" or lang is None:
        return None
    else:
        return lang
    

def setUILanguage(lang, prefClass=Prefs):
    """
    Module function to store the language for the user interface.
    
    @param lang the language
    @param prefClass preferences class used as the storage area
    """
    if lang is None:
        prefClass.settings.setValue("UI/Language", "None")
    else:
        prefClass.settings.setValue("UI/Language", lang)


def getViewManager(prefClass=Prefs):
    """
    Module function to retrieve the selected viewmanager type.
    
    @param prefClass preferences class used as the storage area
    @return the viewmanager type
    """
    return prefClass.settings.value(
        "UI/ViewManager", prefClass.uiDefaults["ViewManager"])
    

def setViewManager(vm, prefClass=Prefs):
    """
    Module function to store the selected viewmanager type.
    
    @param vm the viewmanager type
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("UI/ViewManager", vm)


def getUI(key, prefClass=Prefs):
    """
    Module function to retrieve the various UI settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested UI setting
    """
    if key in ["BrowsersListFoldersFirst", "BrowsersHideNonPublic",
               "BrowsersListContentsByOccurrence", "BrowsersListHiddenFiles",
               "BrowserShowCoding", "LogViewerAutoRaise",
               "SingleApplicationMode", "TabViewManagerFilenameOnly",
               "ShowFilePreview", "ShowFilePreviewJS", "ShowFilePreviewSSI",
               "CaptionShowsFilename", "ShowSplash",
               "SplitOrientationVertical",
               "UseProxy", "UseSystemProxy", "UseHttpProxyForAll",
               "RequestDownloadFilename", "CheckErrorLog",
               "OpenCrashSessionOnStartup", "CrashSessionEnabled",
               "ShowCodeDocumentationViewer", "ShowPyPIPackageManager",
               "ShowCondaPackageManager", "ShowCooperation", "ShowIrc",
               "ShowTemplateViewer", "ShowFileBrowser", "ShowSymbolsViewer",
               "ShowNumbersViewer", "ShowMicroPython", "UseNativeMenuBar"]:
        return toBool(prefClass.settings.value(
            "UI/" + key, prefClass.uiDefaults[key]))
    elif key in ["TabViewManagerFilenameLength", "CaptionFilenameLength",
                 "ProxyPort/Http", "ProxyPort/Https", "ProxyPort/Ftp",
                 "ProxyType/Ftp", "OpenOnStartup",
                 "PerformVersionCheck", "RecentNumber", "NotificationTimeout",
                 "SidebarDelay", "KeyboardInputInterval",
                 "BackgroundServiceProcesses", "MinimumMessageTypeSeverity"]:
        return int(prefClass.settings.value(
            "UI/" + key, prefClass.uiDefaults[key]))
    elif key in ["ProxyPassword/Http", "ProxyPassword/Https",
                 "ProxyPassword/Ftp", ]:
        from Utilities.crypto import pwConvert
        return pwConvert(
            prefClass.settings.value("UI/" + key, prefClass.uiDefaults[key]),
            encode=False)
    elif key in ("LogStdErrColour",):
        col = prefClass.settings.value("UI/" + key)
        if col is not None:
            return QColor(col)
        else:
            return prefClass.uiDefaults[key]
    elif key in "ViewProfiles2":
        profilesStr = prefClass.settings.value("UI/ViewProfiles2")
        if profilesStr is None:
            # use the defaults
            viewProfiles = prefClass.uiDefaults["ViewProfiles2"]
        else:
            viewProfiles = {}
            profiles = json.loads(profilesStr)
            for name in ["edit", "debug"]:
                viewProfiles[name] = [
                    QByteArray.fromBase64(profiles[name][0].encode("utf-8")),
                    profiles[name][1][:],
                    []
                ]
                for bs in profiles[name][2]:
                    viewProfiles[name][2].append(
                        QByteArray.fromBase64(bs.encode("utf-8")))
        return viewProfiles
    elif key in ["ToolbarManagerState", "PreviewSplitterState"]:
        state = prefClass.settings.value("UI/" + key)
        if state is not None:
            return state
        else:
            return prefClass.uiDefaults[key]
    elif key in ["VersionsUrls6"]:
        urls = toList(
            prefClass.settings.value("UI/" + key, prefClass.uiDefaults[key]))
        if len(urls) == 0:
            return prefClass.uiDefaults[key]
        else:
            return urls
    elif key in ["LogViewerStdoutFilter", "LogViewerStderrFilter",
                 "LogViewerStdxxxFilter", "TextMimeTypes"]:
        return toList(
            prefClass.settings.value("UI/" + key, prefClass.uiDefaults[key]))
    else:
        return prefClass.settings.value("UI/" + key, prefClass.uiDefaults[key])
    

def setUI(key, value, prefClass=Prefs):
    """
    Module function to store the various UI settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key == "ViewProfiles2":
        profiles = {}
        for name in ["edit", "debug"]:
            profiles[name] = [
                bytes(value[name][0].toBase64()).decode(),
                value[name][1][:],
                []
            ]
            for ba in value[name][2]:
                profiles[name][2].append(bytes(ba.toBase64()).decode())
        prefClass.settings.setValue("UI/" + key, json.dumps(profiles))
    elif key in ("LogStdErrColour",):
        prefClass.settings.setValue("UI/" + key, value.name())
    elif key in ["ProxyPassword/Http", "ProxyPassword/Https",
                 "ProxyPassword/Ftp", ]:
        from Utilities.crypto import pwConvert
        prefClass.settings.setValue("UI/" + key, pwConvert(value, encode=True))
    else:
        prefClass.settings.setValue("UI/" + key, value)
    

def getIcons(key, prefClass=Prefs):
    """
    Module function to retrieve the various Icons settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested Icons setting
    """
    dirlist = prefClass.settings.value("UI/Icons/" + key)
    if dirlist is not None:
        return dirlist
    else:
        return prefClass.iconsDefaults[key]
    
    if key in ["Path"]:
        return toList(prefClass.settings.value(
            "UI/Icons/" + key, prefClass.iconsDefaults[key]))
    else:
        return prefClass.settings.value(
            "UI/Icons/" + key, prefClass.iconsDefaults[key])


def setIcons(key, value, prefClass=Prefs):
    """
    Module function to store the various Icons settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("UI/Icons/" + key, value)
    

def getCooperation(key, prefClass=Prefs):
    """
    Module function to retrieve the various Cooperation settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested UI setting
    """
    if key in ["AutoStartServer", "TryOtherPorts", "AutoAcceptConnections"]:
        return toBool(prefClass.settings.value(
            "Cooperation/" + key, prefClass.cooperationDefaults[key]))
    elif key in ["ServerPort", "MaxPortsToTry"]:
        return int(prefClass.settings.value(
            "Cooperation/" + key, prefClass.cooperationDefaults[key]))
    elif key in ["BannedUsers"]:
        return toList(prefClass.settings.value(
            "Cooperation/" + key, prefClass.cooperationDefaults[key]))
    else:
        return prefClass.settings.value(
            "Cooperation/" + key, prefClass.cooperationDefaults[key])
    

def setCooperation(key, value, prefClass=Prefs):
    """
    Module function to store the various Cooperation settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Cooperation/" + key, value)


def getEditor(key, prefClass=Prefs):
    """
    Module function to retrieve the various editor settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested editor setting
    """
    if key in ["DefaultEncoding", "DefaultOpenFilter", "DefaultSaveFilter",
               "SpellCheckingDefaultLanguage", "SpellCheckingPersonalWordList",
               "SpellCheckingPersonalExcludeList",
               "PreviewMarkdownHTMLFormat", "PreviewRestDocutilsHTMLFormat",
               "DocstringType"]:
        return prefClass.settings.value(
            "Editor/" + key, prefClass.editorDefaults[key])
    elif key in ["AutosaveInterval", "TabWidth", "IndentWidth",
                 "FoldingStyle", "WarnFilesize", "EdgeMode", "EdgeColumn",
                 "CaretWidth", "CaretLineFrameWidth", "AutoCompletionSource",
                 "AutoCompletionThreshold", "AutoCompletionTimeout",
                 "AutoCompletionCacheSize", "AutoCompletionCacheTime",
                 "AutoCompletionWatchdogTime", "AutoCompletionMaxLines",
                 "AutoCompletionMaxChars", "CallTipsVisible",
                 "CallTipsStyle", "MarkOccurrencesTimeout", "SearchRegexpMode",
                 "AutoSpellCheckChunkSize", "SpellCheckingMinWordSize",
                 "PostScriptLevel", "EOLMode", "ZoomFactor", "WhitespaceSize",
                 "OnlineSyntaxCheckInterval", "OnlineChangeTraceInterval",
                 "WrapLongLinesMode", "WrapVisualFlag", "WrapIndentMode",
                 "WrapStartIndent", "CallTipsPosition", "VirtualSpaceOptions",
                 "PreviewRefreshWaitTimer", "SourceOutlineWidth",
                 "SourceOutlineStepSize"]:
        return int(prefClass.settings.value(
            "Editor/" + key, prefClass.editorDefaults[key]))
    elif key in ["AdditionalOpenFilters", "AdditionalSaveFilters",
                 "PreviewMarkdownFileNameExtensions",
                 "PreviewRestFileNameExtensions",
                 "PreviewHtmlFileNameExtensions",
                 "PreviewQssFileNameExtensions",
                 "FullSpellCheckExtensions"]:
        return toList(prefClass.settings.value(
            "Editor/" + key, prefClass.editorDefaults[key]))
    elif key in ["PythonBadIndentation"]:
        value = prefClass.settings.value(
            "Editor/" + key, prefClass.editorDefaults[key])
        if value in ["true", "True"]:
            value = 1
        elif value in ["false", "False"]:
            value = 0
        return QsciLexerPython.IndentationWarning(int(value))
    elif key == "TabIndentOverride":
        overrideStr = prefClass.settings.value(
            "Editor/" + key, prefClass.editorDefaults[key])
        if overrideStr:
            return json.loads(overrideStr)
        else:
            return {}
    else:
        return toBool(prefClass.settings.value(
            "Editor/" + key, prefClass.editorDefaults[key]))
    

def setEditor(key, value, prefClass=Prefs):
    """
    Module function to store the various editor settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key == "TabIndentOverride":
        prefClass.settings.setValue("Editor/" + key, json.dumps(value))
    else:
        prefClass.settings.setValue("Editor/" + key, value)
    

def getEditorColour(key, prefClass=Prefs):
    """
    Module function to retrieve the various editor marker colours.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested editor colour
    """
    col = prefClass.settings.value("Editor/Colour/" + key)
    if col is not None:
        if len(col) == 9:
            # color string with alpha
            return QColor.fromRgba(int(col[1:], 16))
        else:
            return QColor(col)
    else:
        # palette based defaults here because of Qt5
        if key == "EditAreaForeground":
            return QApplication.palette().color(QPalette.ColorGroup.Active,
                                                QPalette.ColorRole.Base)
        elif key == "EditAreaBackground":
            return QApplication.palette().color(QPalette.ColorGroup.Active,
                                                QPalette.ColorRole.Text)
        else:
            return prefClass.editorColourDefaults[key]
    

def setEditorColour(key, value, prefClass=Prefs):
    """
    Module function to store the various editor marker colours.
    
    @param key the key of the colour to be set
    @param value the colour to be set
    @param prefClass preferences class used as the storage area
    """
    if value.alpha() < 255:
        val = "#{0:8x}".format(value.rgba())
    else:
        val = value.name()
    prefClass.settings.setValue("Editor/Colour/" + key, val)
    

def getEditorOtherFonts(key, prefClass=Prefs):
    """
    Module function to retrieve the various editor fonts except the lexer
    fonts.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested editor font (QFont)
    """
    f = QFont()
    f.fromString(prefClass.settings.value(
        "Editor/Other Fonts/" + key, prefClass.editorOtherFontsDefaults[key]))
    return f
    

def setEditorOtherFonts(key, font, prefClass=Prefs):
    """
    Module function to store the various editor fonts except the lexer fonts.
    
    @param key the key of the font to be set
    @param font the font to be set (QFont)
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Editor/Other Fonts/" + key, font.toString())
    

def getEditorAPI(language, projectType="", prefClass=Prefs):
    """
    Module function to retrieve the various lists of API files.
    
    @param language language of the API list
    @type str
    @param projectType project type of the API list
    @type str
    @param prefClass preferences class used as the storage area
    @type Prefs
    @return requested list of API files
    @rtype list of str
    """
    if projectType:
        key = "{0}_{1}".format(language, projectType)
    else:
        key = language
    apis = prefClass.settings.value("Editor/APIs/" + key)
    if apis is not None:
        if len(apis) and apis[0] == "":
            return []
        else:
            return apis
    else:
        if projectType:
            # try again without project type
            return getEditorAPI(language, prefClass=prefClass)
        
        return []
    

def setEditorAPI(language, projectType, apilist, prefClass=Prefs):
    """
    Module function to store the various lists of API files.
    
    @param language language of the API list
    @type str
    @param projectType project type of the API list
    @type str
    @param apilist list of API files
    @type list of str
    @param prefClass preferences class used as the storage area
    @type Prefs
    """
    if projectType:
        key = "{0}_{1}".format(language, projectType)
    else:
        key = language
    prefClass.settings.setValue("Editor/APIs/" + key, apilist)
    

def getEditorKeywords(key, prefClass=Prefs):
    """
    Module function to retrieve the various lists of language keywords.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested list of language keywords (list of strings)
    """
    keywords = prefClass.settings.value("Editor/Keywords/" + key)
    if keywords is not None:
        return keywords
    else:
        return []
    

def setEditorKeywords(key, keywordsLists, prefClass=Prefs):
    """
    Module function to store the various lists of language keywords.
    
    @param key the key of the api to be set
    @param keywordsLists the list of language keywords (list of strings)
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Editor/Keywords/" + key, keywordsLists)
    

def getEditorLexerAssocs(prefClass=Prefs):
    """
    Module function to retrieve all lexer associations.
    
    @param prefClass preferences class used as the storage area
    @return a reference to the list of lexer associations
        (dictionary of strings)
    """
    editorLexerAssoc = {}
    prefClass.settings.beginGroup("Editor/LexerAssociations")
    keyList = prefClass.settings.childKeys()
    prefClass.settings.endGroup()
    
    import QScintilla.Lexers
    editorLexerAssocDefaults = QScintilla.Lexers.getDefaultLexerAssociations()
    
    if len(keyList) == 0:
        # build from scratch
        for key in list(editorLexerAssocDefaults.keys()):
            editorLexerAssoc[key] = editorLexerAssocDefaults[key]
    else:
        for key in keyList:
            if key in editorLexerAssocDefaults:
                defaultValue = editorLexerAssocDefaults[key]
            else:
                defaultValue = ""
            editorLexerAssoc[key] = prefClass.settings.value(
                "Editor/LexerAssociations/" + key, defaultValue)
        
        # check for new default lexer associations
        for key in list(editorLexerAssocDefaults.keys()):
            if key not in editorLexerAssoc:
                editorLexerAssoc[key] = editorLexerAssocDefaults[key]
    return editorLexerAssoc
    

def setEditorLexerAssocs(assocs, prefClass=Prefs):
    """
    Module function to retrieve all lexer associations.
    
    @param assocs dictionary of lexer associations to be set
    @param prefClass preferences class used as the storage area
    """
    # first remove lexer associations that no longer exist, than save the rest
    prefClass.settings.beginGroup("Editor/LexerAssociations")
    keyList = prefClass.settings.childKeys()
    prefClass.settings.endGroup()
    for key in keyList:
        if key not in assocs:
            prefClass.settings.remove("Editor/LexerAssociations/" + key)
    for key in assocs:
        prefClass.settings.setValue(
            "Editor/LexerAssociations/" + key, assocs[key])
    

def getEditorLexerAssoc(filename, prefClass=Prefs):
    """
    Module function to retrieve a lexer association.
    
    @param filename filename used to determine the associated lexer language
        (string)
    @param prefClass preferences class used as the storage area
    @return the requested lexer language (string)
    """
    for pattern, language in list(getEditorLexerAssocs().items()):
        if fnmatch.fnmatch(filename, pattern):
            return language
    
    return ""
    

def getEditorTyping(key, prefClass=Prefs):
    """
    Module function to retrieve the various editor typing settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested editor setting
    """
    return toBool(prefClass.settings.value(
        "Editor/Typing/" + key, prefClass.editorTypingDefaults[key]))
    

def setEditorTyping(key, value, prefClass=Prefs):
    """
    Module function to store the various editor typing settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Editor/Typing/" + key, value)
    

def getEditorExporter(key, prefClass=Prefs):
    """
    Module function to retrieve the various editor exporters settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested editor setting
    """
    if key in ["RTF/Font"]:
        f = QFont()
        f.fromString(prefClass.settings.value(
            "Editor/Exporters/" + key, prefClass.editorExporterDefaults[key]))
        return f
    elif key in ["HTML/WYSIWYG", "HTML/Folding", "HTML/OnlyStylesUsed",
                 "HTML/FullPathAsTitle", "HTML/UseTabs", "RTF/WYSIWYG",
                 "RTF/UseTabs", "TeX/OnlyStylesUsed", "TeX/FullPathAsTitle",
                 "ODT/WYSIWYG", "ODT/OnlyStylesUsed", "ODT/UseTabs"]:
        return toBool(prefClass.settings.value(
            "Editor/Exporters/" + key, prefClass.editorExporterDefaults[key]))
    elif key in ["PDF/Magnification", "PDF/MarginLeft", "PDF/MarginRight",
                 "PDF/MarginTop", "PDF/MarginBottom"]:
        return int(prefClass.settings.value(
            "Editor/Exporters/" + key, prefClass.editorExporterDefaults[key]))
    else:
        return prefClass.settings.value(
            "Editor/Exporters/" + key, prefClass.editorExporterDefaults[key])


def setEditorExporter(key, value, prefClass=Prefs):
    """
    Module function to store the various editor exporters settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["RTF/Font"]:
        prefClass.settings.setValue(
            "Editor/Exporters/" + key, value.toString())
    else:
        prefClass.settings.setValue("Editor/Exporters/" + key, value)
    

def getPrinter(key, prefClass=Prefs):
    """
    Module function to retrieve the various printer settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested printer setting
    """
    if key in ["ColorMode", "FirstPageFirst"]:
        return toBool(prefClass.settings.value(
            "Printer/" + key, prefClass.printerDefaults[key]))
    elif key in ["Magnification", "Orientation", "PageSize", "Resolution"]:
        return int(prefClass.settings.value(
            "Printer/" + key, prefClass.printerDefaults[key]))
    elif key in ["LeftMargin", "RightMargin", "TopMargin", "BottomMargin"]:
        return float(prefClass.settings.value(
            "Printer/" + key, prefClass.printerDefaults[key]))
    elif key in ["HeaderFont"]:
        f = QFont()
        f.fromString(prefClass.settings.value(
            "Printer/" + key, prefClass.printerDefaults[key]))
        return f
    else:
        return prefClass.settings.value(
            "Printer/" + key, prefClass.printerDefaults[key])


def setPrinter(key, value, prefClass=Prefs):
    """
    Module function to store the various printer settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["HeaderFont"]:
        prefClass.settings.setValue("Printer/" + key, value.toString())
    else:
        prefClass.settings.setValue("Printer/" + key, value)


def getShell(key, prefClass=Prefs):
    """
    Module function to retrieve the various shell settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested shell setting
    """
    if key in ["MonospacedFont", "MarginsFont"]:
        f = QFont()
        f.fromString(prefClass.settings.value(
            "Shell/" + key, prefClass.shellDefaults[key]))
        return f
    elif key in ["MaxHistoryEntries"]:
        return int(prefClass.settings.value(
            "Shell/" + key, prefClass.shellDefaults[key]))
    elif key in ["HistoryStyle"]:
        return ShellHistoryStyle(int(prefClass.settings.value(
            "Shell/" + key, prefClass.shellDefaults[key].value)))
    elif key in ["LastVirtualEnvironment"]:
        return prefClass.settings.value(
            "Shell/" + key, prefClass.shellDefaults[key])
    else:
        return toBool(prefClass.settings.value(
            "Shell/" + key, prefClass.shellDefaults[key]))


def setShell(key, value, prefClass=Prefs):
    """
    Module function to store the various shell settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["MonospacedFont", "MarginsFont"]:
        prefClass.settings.setValue("Shell/" + key, value.toString())
    elif key in ["HistoryStyle"]:
        prefClass.settings.setValue("Shell/" + key, value.value)
    else:
        prefClass.settings.setValue("Shell/" + key, value)


def getProject(key, prefClass=Prefs):
    """
    Module function to retrieve the various project handling settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested project setting
    """
    if key in ["RecentNumber"]:
        return int(prefClass.settings.value(
            "Project/" + key, prefClass.projectDefaults[key]))
    elif key in ["DebugClientsHistory", "DebuggerInterpreterHistory"]:
        return toList(prefClass.settings.value(
            "Project/" + key, prefClass.projectDefaults[key]))
    else:
        return toBool(prefClass.settings.value(
            "Project/" + key, prefClass.projectDefaults[key]))
    

def setProject(key, value, prefClass=Prefs):
    """
    Module function to store the various project handling settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["DebugClientsHistory", "DebuggerInterpreterHistory"]:
        # max. list sizes is hard coded to 20 entries
        newList = [v for v in value if v]
        if len(newList) > 20:
            newList = newList[:20]
        prefClass.settings.setValue("Project/" + key, newList)
    else:
        prefClass.settings.setValue("Project/" + key, value)
    

def getProjectBrowserFlags(key, prefClass=Prefs):
    """
    Module function to retrieve the various project browser flags settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested project setting
    """
    try:
        default = prefClass.projectBrowserFlagsDefaults[key]
    except KeyError:
        default = AllBrowsersFlag
    
    return int(prefClass.settings.value(
        "Project/BrowserFlags/" + key, default))
    

def setProjectBrowserFlags(key, value, prefClass=Prefs):
    """
    Module function to store the various project browser flags settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Project/BrowserFlags/" + key, value)
    

def setProjectBrowserFlagsDefault(key, value, prefClass=Prefs):
    """
    Module function to store the various project browser flags settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.projectBrowserFlagsDefaults[key] = value
    

def removeProjectBrowserFlags(key, prefClass=Prefs):
    """
    Module function to remove a project browser flags setting.
    
    @param key the key of the setting to be removed
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.remove("Project/BrowserFlags/" + key)
    

def getProjectBrowserColour(key, prefClass=Prefs):
    """
    Module function to retrieve the various project browser colours.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested project browser colour
    """
    col = prefClass.settings.value("Project/Colour/" + key)
    if col is not None:
        return QColor(col)
    else:
        return prefClass.projectBrowserColourDefaults[key]
    

def setProjectBrowserColour(key, value, prefClass=Prefs):
    """
    Module function to store the various project browser colours.
    
    @param key the key of the colour to be set
    @param value the colour to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Project/Colour/" + key, value.name())
    

def getMultiProject(key, prefClass=Prefs):
    """
    Module function to retrieve the various project handling settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested project setting
    """
    if key in ["RecentNumber"]:
        return int(prefClass.settings.value(
            "MultiProject/" + key, prefClass.multiProjectDefaults[key]))
    elif key in ["OpenMasterAutomatically", "TimestampFile"]:
        return toBool(prefClass.settings.value(
            "MultiProject/" + key, prefClass.multiProjectDefaults[key]))
    else:
        return prefClass.settings.value(
            "MultiProject/" + key, prefClass.multiProjectDefaults[key])


def setMultiProject(key, value, prefClass=Prefs):
    """
    Module function to store the various project handling settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("MultiProject/" + key, value)


def getQtDocDir(version, prefClass=Prefs):
    """
    Module function to retrieve the Qt5DocDir setting.
    
    @param version Qt version to get documentation directory for
    @type int
    @param prefClass preferences class used as the storage area
    @return the requested Qt5DocDir setting
    @rtype str
    """
    key = "Qt{0}DocDir".format(version)
    s = prefClass.settings.value(
        "Help/{0}".format(key), prefClass.helpDefaults[key])
    if s == "":
        s = os.getenv(key.upper(), "")
    if s == "":
        s = os.path.join(
            QLibraryInfo.location(
                QLibraryInfo.LibraryLocation.DocumentationPath),
            "qtdoc")
    return s


def getHelp(key, prefClass=Prefs):
    """
    Module function to retrieve the various help settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested help setting
    """
    return prefClass.settings.value("Help/" + key,
                                    prefClass.helpDefaults[key])


def setHelp(key, value, prefClass=Prefs):
    """
    Module function to store the various help settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Help/" + key, value)


def getWebBrowser(key, prefClass=Prefs):
    """
    Module function to retrieve the various web browser settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested help setting
    """
    if not prefClass.webEngineSettingsIntitialized:
        prefClass.initWebEngineSettingsDefaults()
    
    if key in ["StandardFont", "FixedFont"]:
        f = QFont()
        f.fromString(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]))
        return f
    elif key in ["SecureUrlColor", "InsecureUrlColor", "MaliciousUrlColor",
                 "PrivateModeUrlColor"]:
        col = prefClass.settings.value("WebBrowser/" + key)
        if col is not None:
            return QColor(col)
        else:
            return prefClass.webBrowserDefaults[key]
    elif key in ["WebSearchKeywords"]:
        # return a list of tuples of (keyword, engine name)
        keywords = []
        size = prefClass.settings.beginReadArray("WebBrowser/" + key)
        for index in range(size):
            prefClass.settings.setArrayIndex(index)
            keyword = prefClass.settings.value("Keyword")
            engineName = prefClass.settings.value("Engine")
            keywords.append((keyword, engineName))
        prefClass.settings.endArray()
        return keywords
    elif key == "DownloadManagerDownloads":
        # return a list of dicts containing the URL, save location, done flag,
        # page URL, date/time downloaded
        downloads = []
        length = prefClass.settings.beginReadArray("WebBrowser/" + key)
        for index in range(length):
            download = {}
            prefClass.settings.setArrayIndex(index)
            download["URL"] = prefClass.settings.value("URL")
            if download["URL"] is None:
                download["URL"] = QUrl()
            download["Location"] = prefClass.settings.value("Location")
            download["Done"] = toBool(prefClass.settings.value("Done"))
            download["PageURL"] = prefClass.settings.value("PageURL")
            if download["PageURL"] is None:
                download["PageURL"] = QUrl()
            download["Downloaded"] = prefClass.settings.value("Downloaded")
            if download["Downloaded"] is None:
                download["Downloaded"] = QDateTime()
            elif isinstance(download["Downloaded"], str):
                download["Downloaded"] = QDateTime.fromString(
                    download["Downloaded"], "yyyy-MM-dd hh:mm:ss")
            downloads.append(download)
        prefClass.settings.endArray()
        return downloads
    elif key == "RssFeeds":
        # return a list of tuples of (URL, title, icon)
        feeds = []
        length = prefClass.settings.beginReadArray("WebBrowser/" + key)
        for index in range(length):
            prefClass.settings.setArrayIndex(index)
            url = prefClass.settings.value("URL")
            title = prefClass.settings.value("Title")
            icon = prefClass.settings.value("Icon")
            feeds.append((url, title, icon))
        prefClass.settings.endArray()
        return feeds
    elif key in ["SyncFtpPassword", "SyncEncryptionKey"]:
        from Utilities.crypto import pwConvert
        return pwConvert(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]),
            encode=False)
    elif key == "HelpViewerType":
        # special treatment to adjust for missing QtWebEngine
        value = int(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]))
        if QWebEngineSettings is None:
            value = prefClass.webBrowserDefaults[key]
        return value
    elif key in ["StartupBehavior", "HistoryLimit",
                 "DownloadManagerRemovePolicy", "SyncType", "SyncFtpPort",
                 "SyncFtpIdleTimeout", "SyncEncryptionKeyLength",
                 "SearchLanguage", "DefaultFontSize", "DefaultFixedFontSize",
                 "MinimumFontSize", "MinimumLogicalFontSize",
                 "DiskCacheSize", "AcceptCookies", "KeepCookiesUntil",
                 "AdBlockUpdatePeriod", "TabManagerGroupByType",
                 "SessionAutoSaveInterval", "NewTabBehavior",
                 "RefererSendReferer", "RefererDefaultPolicy",
                 "RefererTrimmingPolicy", "AcceptQuotaRequest",
                 "AcceptProtocolHandlerRequest",
                 ]:
        return int(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]))
    elif key in ["SingleWebBrowserWindow", "SaveGeometry",
                 "JavaScriptEnabled", "JavaScriptCanOpenWindows",
                 "JavaScriptCanAccessClipboard",
                 "AutoLoadImages", "LocalStorageEnabled",
                 "SpatialNavigationEnabled", "LinksIncludedInFocusChain",
                 "LocalContentCanAccessRemoteUrls",
                 "LocalContentCanAccessFileUrls", "XSSAuditingEnabled",
                 "ScrollAnimatorEnabled", "ErrorPageEnabled",
                 "WarnOnMultipleClose", "WebSearchSuggestions",
                 "SyncEnabled", "SyncBookmarks", "SyncHistory",
                 "SyncPasswords", "SyncUserAgents", "SyncSpeedDial",
                 "SyncEncryptData", "SyncEncryptPasswordsOnly",
                 "ShowPreview", "DiskCacheEnabled",
                 "DoNotTrack", "FilterTrackingCookies",
                 "AdBlockEnabled", "AdBlockUseLimitedEasyList",
                 "PluginsEnabled", "FullScreenSupportEnabled",
                 "AutoScrollEnabled", "ScreenCaptureEnabled",
                 "WebGLEnabled", "FocusOnNavigationEnabled",
                 "PrintElementBackgrounds", "AllowRunningInsecureContent",
                 "SpellCheckEnabled", "ShowToolbars", "MenuBarVisible",
                 "BookmarksToolBarVisible", "StatusBarVisible",
                 "SessionAutoSave", "LoadTabOnActivation",
                 "SafeBrowsingEnabled", "SafeBrowsingFilterPlatform",
                 "SafeBrowsingAutoUpdate", "SafeBrowsingUseLookupApi",
                 "AllowGeolocationOnInsecureOrigins",
                 "AllowWindowActivationFromJavaScript", "ShowScrollBars",
                 "DownloadManagerAutoOpen", "DownloadManagerAutoClose",
                 "PlaybackRequiresUserGesture", "JavaScriptCanPaste",
                 "WebRTCPublicInterfacesOnly", "DnsPrefetchEnabled",
                 "VirusTotalEnabled", "VirusTotalSecure",
                 "PdfViewerEnabled", "AlwaysRejectFaultyCertificates",
                 ]:
        return toBool(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]))
    elif key in ["GreaseMonkeyDisabledScripts", "SendRefererWhitelist",
                 "AdBlockSubscriptions", "AdBlockExceptions",
                 "SpellCheckLanguages",
                 ]:
        return toList(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]))
    elif key in ["AutoScrollDivider"]:
        return float(prefClass.settings.value(
            "WebBrowser/" + key, prefClass.webBrowserDefaults[key]))
    elif key in ["SafeBrowsingUpdateDateTime"]:
        dateTimeStr = prefClass.settings.value("WebBrowser/" + key)
        if dateTimeStr is not None:
            return QDateTime.fromString(dateTimeStr, Qt.DateFormat.ISODate)
        else:
            return prefClass.webBrowserDefaults[key]
    else:
        return prefClass.settings.value("WebBrowser/" + key,
                                        prefClass.webBrowserDefaults[key])
    

def setWebBrowser(key, value, prefClass=Prefs):
    """
    Module function to store the various web browser settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["StandardFont", "FixedFont"]:
        prefClass.settings.setValue("WebBrowser/" + key, value.toString())
    elif key in ["SecureUrlColor", "InsecureUrlColor", "MaliciousUrlColor",
                 "PrivateModeUrlColor"]:
        prefClass.settings.setValue("WebBrowser/" + key, value.name())
    elif key == "WebSearchKeywords":
        # value is list of tuples of (keyword, engine name)
        prefClass.settings.remove("WebBrowser/" + key)
        prefClass.settings.beginWriteArray("WebBrowser/" + key, len(value))
        index = 0
        for v in value:
            prefClass.settings.setArrayIndex(index)
            prefClass.settings.setValue("Keyword", v[0])
            prefClass.settings.setValue("Engine", v[1])
            index += 1
        prefClass.settings.endArray()
    elif key == "DownloadManagerDownloads":
        # value is list of dicts containing the URL, save location, done flag,
        # page URL, date/time downloaded
        prefClass.settings.remove("Help/" + key)
        prefClass.settings.beginWriteArray("WebBrowser/" + key, len(value))
        index = 0
        for v in value:
            prefClass.settings.setArrayIndex(index)
            prefClass.settings.setValue("URL", v["URL"])
            prefClass.settings.setValue("Location", v["Location"])
            prefClass.settings.setValue("Done", v["Done"])
            prefClass.settings.setValue("PageURL", v["PageURL"])
            prefClass.settings.setValue(
                "Downloaded", v["Downloaded"].toString("yyyy-MM-dd hh:mm:ss"))
            index += 1
        prefClass.settings.endArray()
    elif key == "RssFeeds":
        # value is list of tuples of (URL, title, icon)
        prefClass.settings.remove("WebBrowser/" + key)
        prefClass.settings.beginWriteArray("WebBrowser/" + key, len(value))
        index = 0
        for v in value:
            prefClass.settings.setArrayIndex(index)
            prefClass.settings.setValue("URL", v[0])
            prefClass.settings.setValue("Title", v[1])
            prefClass.settings.setValue("Icon", v[2])
            index += 1
        prefClass.settings.endArray()
    elif key in ["SyncFtpPassword", "SyncEncryptionKey"]:
        from Utilities.crypto import pwConvert
        prefClass.settings.setValue(
            "WebBrowser/" + key, pwConvert(value, encode=True))
    elif key in ["SafeBrowsingUpdateDateTime"]:
        # value is a QDateTime
        prefClass.settings.setValue("WebBrowser/" + key,
                                    value.toString(Qt.DateFormat.ISODate))
    else:
        prefClass.settings.setValue("WebBrowser/" + key, value)
    

def getSystem(key, prefClass=Prefs):
    """
    Module function to retrieve the various system settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested system setting
    """
    from Utilities import supportedCodecs
    if key in ["StringEncoding", "IOEncoding"]:
        encoding = prefClass.settings.value(
            "System/" + key, prefClass.sysDefaults[key])
        if encoding not in supportedCodecs:
            encoding = prefClass.sysDefaults[key]
        return encoding
    
    return None
    

def setSystem(key, value, prefClass=Prefs):
    """
    Module function to store the various system settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("System/" + key, value)
    

def getQtTranslationsDir(prefClass=Prefs):
    """
    Module function to retrieve the Qt5TranslationsDir
    setting depending on the current Qt version.
    
    @param prefClass preferences class used as the storage area
    @return the requested setting (string)
    """
    s = prefClass.settings.value(
        "Qt/Qt5TranslationsDir",
        prefClass.qtDefaults["Qt5TranslationsDir"])
    if s == "":
        s = QLibraryInfo.location(
            QLibraryInfo.LibraryLocation.TranslationsPath)
    if s == "" and Globals.isWindowsPlatform():
        transPath = os.path.join(Globals.getPyQt5ModulesDirectory(),
                                 "translations")
        if os.path.exists(transPath):
            s = transPath
    return s
    

def getQt(key, prefClass=Prefs):
    """
    Module function to retrieve the various Qt settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested Qt setting
    """
    if key in ["Qt5TranslationsDir"]:
        return getQtTranslationsDir(prefClass)
    elif key in ["PyuicIndent", "Pyuic6Indent"]:
        return int(prefClass.settings.value(
            "Qt/" + key, prefClass.qtDefaults[key]))
    elif key in ["PyuicFromImports", "PyuicExecute", "Pyuic6Execute",
                 "PySide2FromImports", "PySide6FromImports"]:
        return toBool(prefClass.settings.value(
            "Qt/" + key, prefClass.qtDefaults[key]))
    else:
        return prefClass.settings.value("Qt/" + key, prefClass.qtDefaults[key])
    

def setQt(key, value, prefClass=Prefs):
    """
    Module function to store the various Qt settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Qt/" + key, value)
    

def getCorba(key, prefClass=Prefs):
    """
    Module function to retrieve the various Corba settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested corba setting
    """
    return prefClass.settings.value(
        "Corba/" + key, prefClass.corbaDefaults[key])
    

def setCorba(key, value, prefClass=Prefs):
    """
    Module function to store the various Corba settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Corba/" + key, value)
    

def getProtobuf(key, prefClass=Prefs):
    """
    Module function to retrieve the various protobuf settings.
    
    @param key the key of the value to get
    @type str
    @param prefClass preferences class used as the storage area
    @type Prefs
    @return the requested protobuf setting
    @rtype any
    """
    return prefClass.settings.value(
        "Protobuf/" + key, prefClass.protobufDefaults[key])
    

def setProtobuf(key, value, prefClass=Prefs):
    """
    Module function to store the various protobuf settings.
    
    @param key the key of the setting to be set
    @type str
    @param value the value to be set
    @type any
    @param prefClass preferences class used as the storage area
    @type Prefs
    """
    prefClass.settings.setValue("Protobuf/" + key, value)
    

def getUser(key, prefClass=Prefs):
    """
    Module function to retrieve the various user settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key == "MailServerPassword":
        from Utilities.crypto import pwConvert
        return pwConvert(prefClass.settings.value(
            "User/" + key, prefClass.userDefaults[key]), encode=False)
    elif key in ["MailServerPort"]:
        try:
            return int(prefClass.settings.value(
                "User/" + key, prefClass.userDefaults[key]))
        except ValueError:
            return prefClass.userDefaults[key]
    elif key in ["MailServerAuthentication", "UseSystemEmailClient",
                 "UseMasterPassword", "SavePasswords", "UseGoogleMailOAuth2"]:
        return toBool(prefClass.settings.value(
            "User/" + key, prefClass.userDefaults[key]))
    elif key == "MailServerEncryption":
        # convert from old key 'MailServerUseTLS'
        val = prefClass.settings.value("User/" + key)
        if val is None:
            if toBool(prefClass.settings.value("User/MailServerUseTLS")):
                val = "TLS"
            else:
                val = prefClass.userDefaults[key]
        return val
    else:
        return prefClass.settings.value(
            "User/" + key, prefClass.userDefaults[key])
    

def setUser(key, value, prefClass=Prefs):
    """
    Module function to store the various user settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key == "MailServerPassword":
        from Utilities.crypto import pwConvert
        prefClass.settings.setValue(
            "User/" + key, pwConvert(value, encode=True))
    elif key == "MasterPassword":
        from Utilities.crypto.py3PBKDF2 import hashPassword
        prefClass.settings.setValue(
            "User/" + key, hashPassword(value))
    else:
        prefClass.settings.setValue("User/" + key, value)
    

def getVCS(key, prefClass=Prefs):
    """
    Module function to retrieve the VCS related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["StatusMonitorInterval"]:
        return int(prefClass.settings.value(
            "VCS/" + key, prefClass.vcsDefaults[key]))
    else:
        return toBool(prefClass.settings.value(
            "VCS/" + key, prefClass.vcsDefaults[key]))
    

def setVCS(key, value, prefClass=Prefs):
    """
    Module function to store the VCS related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("VCS/" + key, value)
    

def getTasks(key, prefClass=Prefs):
    """
    Module function to retrieve the Tasks related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["TasksFixmeColor", "TasksWarningColor",
               "TasksTodoColor", "TasksNoteColor",
               "TasksTestColor", "TasksDocuColor"]:
        col = prefClass.settings.value("Tasks/" + key)
        if col is not None:
            return QColor(col)
        else:
            return prefClass.tasksDefaults[key]
    elif key in ["ClearOnFileClose", ]:
        return toBool(prefClass.settings.value(
            "Tasks/" + key, prefClass.tasksDefaults[key]))
    else:
        return prefClass.settings.value(
            "Tasks/" + key, prefClass.tasksDefaults[key])
    

def setTasks(key, value, prefClass=Prefs):
    """
    Module function to store the Tasks related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["TasksFixmeColor", "TasksWarningColor",
               "TasksTodoColor", "TasksNoteColor"]:
        prefClass.settings.setValue("Tasks/" + key, value.name())
    else:
        prefClass.settings.setValue("Tasks/" + key, value)
    

def getTemplates(key, prefClass=Prefs):
    """
    Module function to retrieve the Templates related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["SeparatorChar"]:
        return prefClass.settings.value(
            "Templates/" + key, prefClass.templatesDefaults[key])
    elif key in ["EditorFont"]:
        f = QFont()
        f.fromString(prefClass.settings.value(
            "Templates/" + key, prefClass.templatesDefaults[key]))
        return f
    else:
        return toBool(prefClass.settings.value(
            "Templates/" + key, prefClass.templatesDefaults[key]))
    

def setTemplates(key, value, prefClass=Prefs):
    """
    Module function to store the Templates related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["EditorFont"]:
        prefClass.settings.setValue("Templates/" + key, value.toString())
    else:
        prefClass.settings.setValue("Templates/" + key, value)
    

def getPluginManager(key, prefClass=Prefs):
    """
    Module function to retrieve the plugin manager related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["DownloadPath"]:
        return prefClass.settings.value(
            "PluginManager/" + key, prefClass.pluginManagerDefaults[key])
    elif key in ["UpdatesCheckInterval", "KeepGenerations"]:
        return int(prefClass.settings.value(
            "PluginManager/" + key, prefClass.pluginManagerDefaults[key]))
    elif key in ["HiddenPlugins"]:
        return toList(prefClass.settings.value(
            "PluginManager/" + key, prefClass.pluginManagerDefaults[key]))
    else:
        return toBool(prefClass.settings.value(
            "PluginManager/" + key, prefClass.pluginManagerDefaults[key]))
    

def setPluginManager(key, value, prefClass=Prefs):
    """
    Module function to store the plugin manager related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("PluginManager/" + key, value)
    

def getGraphics(key, prefClass=Prefs):
    """
    Module function to retrieve the Graphics related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["Font"]:
        font = prefClass.settings.value(
            "Graphics/" + key, prefClass.graphicsDefaults[key])
        if isinstance(font, QFont):
            # workaround for an old bug in eric < 4.4
            return font
        else:
            f = QFont()
            f.fromString(font)
            return f
    else:
        return prefClass.settings.value(
            "Graphics/" + key, prefClass.graphicsDefaults[key])
    

def setGraphics(key, value, prefClass=Prefs):
    """
    Module function to store the Graphics related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["Font"]:
        prefClass.settings.setValue("Graphics/" + key, value.toString())
    else:
        prefClass.settings.setValue("Graphics/" + key, value)
    

def getIconEditor(key, prefClass=Prefs):
    """
    Module function to retrieve the Icon Editor related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    return prefClass.settings.value(
        "IconEditor/" + key, prefClass.iconEditorDefaults[key])
    

def setIconEditor(key, value, prefClass=Prefs):
    """
    Module function to store the Icon Editor related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("IconEditor/" + key, value)


def getFlakes(key, prefClass=Prefs):
    """
    Module function to retrieve the pyflakes related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["IncludeInSyntaxCheck", "IgnoreStarImportWarnings"]:
        return toBool(prefClass.settings.value("Py3Flakes/" + key,
                      prefClass.pyflakesDefaults[key]))
    else:
        return prefClass.settings.value(
            "Py3Flakes/" + key, prefClass.pyflakesDefaults[key])
    

def setFlakes(key, value, prefClass=Prefs):
    """
    Module function to store the pyflakes related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Py3Flakes/" + key, value)


def getTrayStarter(key, prefClass=Prefs):
    """
    Module function to retrieve the tray starter related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    return prefClass.settings.value(
        "TrayStarter/" + key, prefClass.trayStarterDefaults[key])
    

def setTrayStarter(key, value, prefClass=Prefs):
    """
    Module function to store the tray starter related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("TrayStarter/" + key, value)
    

def getIrc(key, prefClass=Prefs):
    """
    Module function to retrieve the IRC related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["TimestampIncludeDate", "ShowTimestamps", "ShowNotifications",
               "NotifyJoinPart", "NotifyMessage", "NotifyNick",
               "EnableIrcColours", "AutoUserInfoLookup",
               "MarkPositionWhenHidden", "AskOnShutdown"]:
        return toBool(prefClass.settings.value(
            "IRC/" + key, prefClass.ircDefaults[key]))
    elif key in ["AutoUserInfoMax", "AutoUserInfoInterval"]:
        return int(prefClass.settings.value(
            "IRC/" + key, prefClass.ircDefaults[key]))
    else:
        return prefClass.settings.value(
            "IRC/" + key, prefClass.ircDefaults[key])


def setIrc(key, value, prefClass=Prefs):
    """
    Module function to store the IRC related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("IRC/" + key, value)


def getHexEditor(key, prefClass=Prefs):
    """
    Module function to retrieve the Hex Editor related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["AddressAreaWidth", "RecentNumber"]:
        return int(prefClass.settings.value(
            "HexEditor/" + key, prefClass.hexEditorDefaults[key]))
    elif key in ["ShowAddressArea", "ShowAsciiArea", "OpenInOverwriteMode",
                 "OpenReadOnly", "HighlightChanges"]:
        return toBool(prefClass.settings.value(
            "HexEditor/" + key, prefClass.hexEditorDefaults[key]))
    elif key in ["HighlightingBackGround", "HighlightingForeGround",
                 "SelectionBackGround", "SelectionForeGround",
                 "AddressAreaBackGround", "AddressAreaForeGround"]:
        return QColor(prefClass.settings.value(
            "HexEditor/" + key, prefClass.hexEditorDefaults[key]))
    elif key in ["Font"]:
        f = QFont()
        f.fromString(prefClass.settings.value(
            "HexEditor/" + key, prefClass.hexEditorDefaults[key]))
        return f
    else:
        return prefClass.settings.value(
            "HexEditor/" + key, prefClass.hexEditorDefaults[key])
    

def setHexEditor(key, value, prefClass=Prefs):
    """
    Module function to store the Hex Editor related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["HighlightingBackGround", "HighlightingForeGround",
               "SelectionBackGround", "SelectionForeGround",
               "AddressAreaBackGround", "AddressAreaForeGround"]:
        if value.alpha() < 255:
            val = "#{0:8x}".format(value.rgba())
        else:
            val = value.name()
        prefClass.settings.setValue("HexEditor/" + key, val)
    elif key in ["Font"]:
        prefClass.settings.setValue("HexEditor/" + key, value.toString())
    else:
        prefClass.settings.setValue("HexEditor/" + key, value)
    

def getDiffColour(key, prefClass=Prefs):
    """
    Module function to retrieve the colours for the diff highlighter.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested diff colour
    """
    col = prefClass.settings.value("Diff/" + key)
    if col is not None:
        if len(col) == 9:
            # color string with alpha
            return QColor.fromRgba(int(col[1:], 16))
        else:
            return QColor(col)
    else:
        return prefClass.diffColourDefaults[key]
    

def setDiffColour(key, value, prefClass=Prefs):
    """
    Module function to store the diff highlighter colours.
    
    @param key the key of the colour to be set
    @param value the colour to be set
    @param prefClass preferences class used as the storage area
    """
    if value.alpha() < 255:
        val = "#{0:8x}".format(value.rgba())
    else:
        val = value.name()
    prefClass.settings.setValue("Diff/" + key, val)


def getDocuViewer(key, prefClass=Prefs):
    """
    Module function to retrieve the Code Documentation Viewer related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested Code Documentation Viewer value
    """
    if key in ["ShowInfoAsRichText", "ShowInfoOnOpenParenthesis"]:
        return toBool(prefClass.settings.value(
            "CodeDocumentationViewer/" + key,
            prefClass.docuViewerDefaults[key]))
    else:
        return prefClass.settings.value(
            "CodeDocumentationViewer/" + key,
            prefClass.docuViewerDefaults[key])
    

def setDocuViewer(key, value, prefClass=Prefs):
    """
    Module function to store the Code Documentation Viewer related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("CodeDocumentationViewer/" + key, value)


def getConda(key, prefClass=Prefs):
    """
    Module function to retrieve the conda related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested conda value
    """
    return prefClass.settings.value(
        "Conda/" + key,
        prefClass.condaDefaults[key])


def setConda(key, value, prefClass=Prefs):
    """
    Module function to store the conda related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Conda/" + key, value)


def getPip(key, prefClass=Prefs):
    """
    Module function to retrieve the pip related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested pip value
    """
    if key in ("ExcludeCondaEnvironments"):
        return toBool(prefClass.settings.value(
            "Pip/" + key,
            prefClass.pipDefaults[key]))
    else:
        return prefClass.settings.value(
            "Pip/" + key,
            prefClass.pipDefaults[key])


def setPip(key, value, prefClass=Prefs):
    """
    Module function to store the pip related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Pip/" + key, value)


def getMicroPython(key, prefClass=Prefs):
    """
    Module function to retrieve the MicroPython related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested MicroPython value
    """
    if key in ("SerialTimeout", "ChartColorTheme"):
        return int(prefClass.settings.value(
            "MicroPython/" + key,
            prefClass.microPythonDefaults[key]))
    elif key in ["ReplLineWrap", "SyncTimeAfterConnect", "ShowHiddenLocal",
                 "ShowHiddenDevice"]:
        return toBool(prefClass.settings.value(
            "MicroPython/" + key,
            prefClass.microPythonDefaults[key]))
    elif key in ["IgnoredUnknownDevices", "ManualDevices"]:
        jsonStr = prefClass.settings.value(
            "MicroPython/" + key,
            prefClass.microPythonDefaults[key])
        if jsonStr:
            return json.loads(jsonStr)
        else:
            return None
    else:
        return prefClass.settings.value(
            "MicroPython/" + key,
            prefClass.microPythonDefaults[key])


def setMicroPython(key, value, prefClass=Prefs):
    """
    Module function to store the pip MicroPython settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["IgnoredUnknownDevices", "ManualDevices"]:
        prefClass.settings.setValue(
            "MicroPython/" + key,
            json.dumps(value))
    else:
        prefClass.settings.setValue(
            "MicroPython/" + key,
            value)


def getGeometry(key, prefClass=Prefs):
    """
    Module function to retrieve the display geometry.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested geometry setting
    """
    if key in ["MainMaximized"]:
        return toBool(prefClass.settings.value(
            "Geometry/" + key,
            prefClass.geometryDefaults[key]))
    else:
        v = prefClass.settings.value("Geometry/" + key)
        if v is not None:
            return v
        else:
            return prefClass.geometryDefaults[key]


def setGeometry(key, value, prefClass=Prefs):
    """
    Module function to store the display geometry.
    
    @param key the key of the setting to be set
    @param value the geometry to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["MainMaximized"]:
        prefClass.settings.setValue("Geometry/" + key, value)
    else:
        if prefClass.resetLayout:
            v = prefClass.geometryDefaults[key]
        else:
            v = value
        prefClass.settings.setValue("Geometry/" + key, v)


def resetLayout(prefClass=Prefs):
    """
    Module function to set a flag not storing the current layout.
    
    @param prefClass preferences class used as the storage area
    """
    prefClass.resetLayout = True


def shouldResetLayout(prefClass=Prefs):
    """
    Module function to indicate a reset of the layout.
    
    @param prefClass preferences class used as the storage area
    @return flag indicating a reset of the layout (boolean)
    """
    return prefClass.resetLayout
    

def saveResetLayout(prefClass=Prefs):
    """
    Module function to save the reset layout.
    
    @param prefClass preferences class used as the storage area
    """
    if prefClass.resetLayout:
        for key in list(prefClass.geometryDefaults.keys()):
            prefClass.settings.setValue(
                "Geometry/" + key,
                prefClass.geometryDefaults[key])


def toBool(value):
    """
    Module function to convert a value to bool.
    
    @param value value to be converted
    @return converted data
    """
    if value in ["true", "1", "True"]:
        return True
    elif value in ["false", "0", "False"]:
        return False
    else:
        return bool(value)


def toList(value):
    """
    Module function to convert a value to a list.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


def toByteArray(value):
    """
    Module function to convert a value to a byte array.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Module function to convert a value to a dictionary.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return {}
    else:
        return value


def convertPasswords(oldPassword, newPassword, prefClass=Prefs):
    """
    Module function to convert all passwords.
    
    @param oldPassword current master password (string)
    @param newPassword new master password (string)
    @param prefClass preferences class used as the storage area
    """
    from Utilities.crypto import pwRecode
    for key in ["ProxyPassword/Http", "ProxyPassword/Https",
                "ProxyPassword/Ftp", ]:
        prefClass.settings.setValue(
            "UI/" + key,
            pwRecode(
                prefClass.settings.value("UI/" + key,
                                         prefClass.uiDefaults[key]),
                oldPassword,
                newPassword
            )
        )
    for key in ["MailServerPassword"]:
        prefClass.settings.setValue(
            "User/" + key,
            pwRecode(
                prefClass.settings.value("User/" + key,
                                         prefClass.userDefaults[key]),
                oldPassword,
                newPassword
            )
        )
    for key in ["SyncFtpPassword", "SyncEncryptionKey"]:
        prefClass.settings.setValue(
            "WebBrowser/" + key,
            pwRecode(
                prefClass.settings.value("WebBrowser/" + key,
                                         prefClass.webBrowserDefaults[key]),
                oldPassword,
                newPassword
            )
        )


initPreferences()
initRecentSettings()

#
# eflag: noqa = M201, M613
