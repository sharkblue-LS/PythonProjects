# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the results of the code style check.
"""

import os
import fnmatch
import copy

from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDialog, QTreeWidgetItem, QAbstractButton, QDialogButtonBox, QApplication,
    QHeaderView, QListWidgetItem, QInputDialog, QLineEdit
)

from E5Gui.E5Application import e5App

from .Ui_CodeStyleCheckerDialog import Ui_CodeStyleCheckerDialog

import UI.PixmapCache
import Preferences
import Utilities

from . import pycodestyle

from .Miscellaneous.MiscellaneousDefaults import (
    MiscellaneousCheckerDefaultArgs
)

try:
    basestring          # __IGNORE_WARNING__
except Exception:
    basestring = str    # define for Python3


class CodeStyleCheckerDialog(QDialog, Ui_CodeStyleCheckerDialog):
    """
    Class implementing a dialog to show the results of the code style check.
    """
    filenameRole = Qt.ItemDataRole.UserRole + 1
    lineRole = Qt.ItemDataRole.UserRole + 2
    positionRole = Qt.ItemDataRole.UserRole + 3
    messageRole = Qt.ItemDataRole.UserRole + 4
    fixableRole = Qt.ItemDataRole.UserRole + 5
    codeRole = Qt.ItemDataRole.UserRole + 6
    ignoredRole = Qt.ItemDataRole.UserRole + 7
    argsRole = Qt.ItemDataRole.UserRole + 8
    
    availableFutures = [
        'division', 'absolute_import', 'with_statement',
        'print_function', 'unicode_literals', 'generator_stop',
        'annotations']
    
    cryptoBitSelectionsDsaRsa = [
        "512", "1024", "2048", "4096", "8192", "16384", "32786",
    ]
    cryptoBitSelectionsEc = [
        "160", "224", "256", "384", "512",
    ]
    
    checkCategories = {
        "A": QCoreApplication.translate(
            "CheckerCategories",
            "Annotations"),
        "C": QCoreApplication.translate(
            "CheckerCategories",
            "Code Complexity"),
        "D": QCoreApplication.translate(
            "CheckerCategories",
            "Documentation"),
        "E": QCoreApplication.translate(
            "CheckerCategories",
            "Errors"),
        "M": QCoreApplication.translate(
            "CheckerCategories",
            "Miscellaneous"),
        "N": QCoreApplication.translate(
            "CheckerCategories",
            "Naming"),
        "P": QCoreApplication.translate(
            "CheckerCategories",
            "'pathlib' Usage"),
        "S": QCoreApplication.translate(
            "CheckerCategories",
            "Security"),
        "W": QCoreApplication.translate(
            "CheckerCategories",
            "Warnings"),
    }
    
    noResults = 0
    noFiles = 1
    hasResults = 2
    
    def __init__(self, styleCheckService, project=None, parent=None):
        """
        Constructor
        
        @param styleCheckService reference to the service
        @type CodeStyleCheckService
        @param project reference to the project if called on project or project
            browser level
        @type Project
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CodeStyleCheckerDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.__project = project
        
        self.optionsTabWidget.setCurrentIndex(0)
        
        self.excludeMessagesSelectButton.setIcon(
            UI.PixmapCache.getIcon("select"))
        self.includeMessagesSelectButton.setIcon(
            UI.PixmapCache.getIcon("select"))
        self.fixIssuesSelectButton.setIcon(
            UI.PixmapCache.getIcon("select"))
        self.noFixIssuesSelectButton.setIcon(
            UI.PixmapCache.getIcon("select"))
        
        self.docTypeComboBox.addItem(self.tr("PEP-257"), "pep257")
        self.docTypeComboBox.addItem(self.tr("Eric"), "eric")
        
        for category, text in CodeStyleCheckerDialog.checkCategories.items():
            itm = QListWidgetItem(text, self.categoriesList)
            itm.setData(Qt.ItemDataRole.UserRole, category)
            itm.setFlags(itm.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            itm.setCheckState(Qt.CheckState.Unchecked)
        
        for future in CodeStyleCheckerDialog.availableFutures:
            itm = QListWidgetItem(future, self.futuresList)
            itm.setFlags(itm.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            itm.setCheckState(Qt.CheckState.Unchecked)
        
        self.dsaHighRiskCombo.addItems(
            CodeStyleCheckerDialog.cryptoBitSelectionsDsaRsa)
        self.dsaMediumRiskCombo.addItems(
            CodeStyleCheckerDialog.cryptoBitSelectionsDsaRsa)
        self.rsaHighRiskCombo.addItems(
            CodeStyleCheckerDialog.cryptoBitSelectionsDsaRsa)
        self.rsaMediumRiskCombo.addItems(
            CodeStyleCheckerDialog.cryptoBitSelectionsDsaRsa)
        self.ecHighRiskCombo.addItems(
            CodeStyleCheckerDialog.cryptoBitSelectionsEc)
        self.ecMediumRiskCombo.addItems(
            CodeStyleCheckerDialog.cryptoBitSelectionsEc)
        
        self.statisticsButton.setEnabled(False)
        self.showButton.setEnabled(False)
        self.cancelButton.setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        
        self.resultList.headerItem().setText(self.resultList.columnCount(), "")
        self.resultList.header().setSortIndicator(
            0, Qt.SortOrder.AscendingOrder)
        
        self.addBuiltinButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.deleteBuiltinButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.addWhitelistButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.deleteWhitelistButton.setIcon(UI.PixmapCache.getIcon("minus"))
        
        self.restartButton.setEnabled(False)
        self.fixButton.setEnabled(False)
        
        self.checkProgress.setVisible(False)
        self.checkProgressLabel.setVisible(False)
        self.checkProgressLabel.setMaximumWidth(600)
        
        self.styleCheckService = styleCheckService
        self.styleCheckService.styleChecked.connect(self.__processResult)
        self.styleCheckService.batchFinished.connect(self.__batchFinished)
        self.styleCheckService.error.connect(self.__processError)
        self.filename = None
        
        self.results = CodeStyleCheckerDialog.noResults
        self.cancelled = False
        self.__lastFileItem = None
        self.__batch = False
        self.__finished = True
        self.__errorItem = None
        
        self.__fileOrFileList = ""
        self.__project = None
        self.__forProject = False
        self.__data = {}
        self.__statistics = {}
        self.__onlyFixes = {}
        self.__noFixCodesList = []
        
        self.on_loadDefaultButton_clicked()
        
        self.mainWidget.setCurrentWidget(self.configureTab)
        self.optionsTabWidget.setCurrentWidget(self.globalOptionsTab)
    
    def __resort(self):
        """
        Private method to resort the tree.
        """
        self.resultList.sortItems(self.resultList.sortColumn(),
                                  self.resultList.header().sortIndicatorOrder()
                                  )
    
    def __createErrorItem(self, filename, message):
        """
        Private slot to create a new error item in the result list.
        
        @param filename name of the file
        @type str
        @param message error message
        @type str
        """
        if self.__errorItem is None:
            self.__errorItem = QTreeWidgetItem(self.resultList, [
                self.tr("Errors")])
            self.__errorItem.setExpanded(True)
            self.__errorItem.setForeground(0, Qt.GlobalColor.red)
        
        msg = "{0} ({1})".format(self.__project.getRelativePath(filename),
                                 message)
        if not self.resultList.findItems(msg, Qt.MatchFlag.MatchExactly):
            itm = QTreeWidgetItem(self.__errorItem, [msg])
            itm.setForeground(0, Qt.GlobalColor.red)
            itm.setFirstColumnSpanned(True)
    
    def __createFileErrorItem(self, filename, message):
        """
        Private method to create an error entry for a given file.
        
        @param filename file name of the file
        @type str
        @param message error message text
        @type str
        """
        result = {
            "file": filename,
            "line": 1,
            "offset": 1,
            "code": "",
            "args": [],
            "display": self.tr("Error: {0}").format(message).rstrip(),
            "fixed": False,
            "autofixing": False,
            "ignored": False,
        }
        self.__createResultItem(filename, result)
    
    def __createResultItem(self, filename, result):
        """
        Private method to create an entry in the result list.
        
        @param filename file name of the file
        @type str
        @param result dictionary containing check result data
        @type dict
        @return reference to the created item
        @rtype QTreeWidgetItem
        """
        from .CodeStyleFixer import FixableCodeStyleIssues
        
        if self.__lastFileItem is None:
            # It's a new file
            self.__lastFileItem = QTreeWidgetItem(self.resultList, [
                self.__project.getRelativePath(filename)])
            self.__lastFileItem.setFirstColumnSpanned(True)
            self.__lastFileItem.setExpanded(True)
            self.__lastFileItem.setData(0, self.filenameRole, filename)
        
        msgCode = result["code"].split(".", 1)[0]
        
        fixable = False
        itm = QTreeWidgetItem(
            self.__lastFileItem, [
                "{0:6}".format(result["line"]),
                msgCode,
                result["display"]
            ]
        )
        if msgCode.startswith(("W", "-", "C", "M")):
            itm.setIcon(1, UI.PixmapCache.getIcon("warning"))
        elif msgCode.startswith(("A", "N")):
            itm.setIcon(1, UI.PixmapCache.getIcon("namingError"))
        elif msgCode.startswith("D"):
            itm.setIcon(1, UI.PixmapCache.getIcon("docstringError"))
        elif msgCode.startswith("P"):
            itm.setIcon(1, UI.PixmapCache.getIcon("dirClosed"))
        elif msgCode.startswith("S"):
            if "severity" in result:
                if result["severity"] == "H":
                    itm.setIcon(1, UI.PixmapCache.getIcon("securityLow"))
                elif result["severity"] == "M":
                    itm.setIcon(1, UI.PixmapCache.getIcon("securityMedium"))
                elif result["severity"] == "L":
                    itm.setIcon(1, UI.PixmapCache.getIcon("securityHigh"))
                else:
                    itm.setIcon(1, UI.PixmapCache.getIcon("securityLow"))
            else:
                itm.setIcon(1, UI.PixmapCache.getIcon("securityLow"))
        else:
            itm.setIcon(1, UI.PixmapCache.getIcon("syntaxError"))
        if result["fixed"]:
            itm.setIcon(0, UI.PixmapCache.getIcon("issueFixed"))
        elif (
            msgCode in FixableCodeStyleIssues and
            not result["autofixing"] and
            msgCode not in self.__noFixCodesList
        ):
            itm.setIcon(0, UI.PixmapCache.getIcon("issueFixable"))
            fixable = True
        
        itm.setTextAlignment(0, Qt.AlignmentFlag.AlignRight)
        itm.setTextAlignment(1, Qt.AlignmentFlag.AlignHCenter)
        
        itm.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter)
        itm.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter)
        itm.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter)
        
        itm.setData(0, self.filenameRole, filename)
        itm.setData(0, self.lineRole, int(result["line"]))
        itm.setData(0, self.positionRole, int(result["offset"]))
        itm.setData(0, self.messageRole, result["display"])
        itm.setData(0, self.fixableRole, fixable)
        itm.setData(0, self.codeRole, msgCode)
        itm.setData(0, self.ignoredRole, result["ignored"])
        itm.setData(0, self.argsRole, result["args"])
        
        if result["ignored"]:
            font = itm.font(0)
            font.setItalic(True)
            for col in range(itm.columnCount()):
                itm.setFont(col, font)
        
        return itm
    
    def __modifyFixedResultItem(self, itm, result):
        """
        Private method to modify a result list entry to show its
        positive fixed state.
        
        @param itm reference to the item to modify
        @type QTreeWidgetItem
        @param result dictionary containing check result data
        @type dict
        """
        if result["fixed"]:
            itm.setText(2, result["display"])
            itm.setIcon(0, UI.PixmapCache.getIcon("issueFixed"))
            
            itm.setData(0, self.messageRole, result["display"])
        else:
            itm.setIcon(0, QIcon())
        itm.setData(0, self.fixableRole, False)
    
    def __updateStatistics(self, statistics, fixer, ignoredErrors, securityOk):
        """
        Private method to update the collected statistics.
        
        @param statistics dictionary of statistical data with
            message code as key and message count as value
        @type dict
        @param fixer reference to the code style fixer
        @type CodeStyleFixer
        @param ignoredErrors number of ignored errors
        @type int
        @param securityOk number of acknowledged security reports
        @type int
        """
        self.__statistics["_FilesCount"] += 1
        stats = [k for k in statistics.keys() if k[0].isupper()]
        if stats:
            self.__statistics["_FilesIssues"] += 1
            for key in statistics:
                if key in self.__statistics:
                    self.__statistics[key] += statistics[key]
                else:
                    self.__statistics[key] = statistics[key]
        self.__statistics["_IssuesFixed"] += fixer
        self.__statistics["_IgnoredErrors"] += ignoredErrors
        self.__statistics["_SecurityOK"] += securityOk
    
    def __updateFixerStatistics(self, fixer):
        """
        Private method to update the collected fixer related statistics.
        
        @param fixer reference to the code style fixer
        @type CodeStyleFixer
        """
        self.__statistics["_IssuesFixed"] += fixer
    
    def __resetStatistics(self):
        """
        Private slot to reset the statistics data.
        """
        self.__statistics = {}
        self.__statistics["_FilesCount"] = 0
        self.__statistics["_FilesIssues"] = 0
        self.__statistics["_IssuesFixed"] = 0
        self.__statistics["_IgnoredErrors"] = 0
        self.__statistics["_SecurityOK"] = 0
    
    def prepare(self, fileList, project):
        """
        Public method to prepare the dialog with a list of filenames.
        
        @param fileList list of filenames
        @type list of str
        @param project reference to the project object
        @type Project
        """
        self.__fileOrFileList = fileList[:]
        self.__project = project
        self.__forProject = True
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        self.cancelButton.setEnabled(False)
        
        self.__data = self.__project.getData("CHECKERSPARMS", "Pep8Checker")
        if (
            self.__data is None or
            len(self.__data) < 6
        ):
            # initialize the data structure
            self.__data = {
                "ExcludeFiles": "",
                "ExcludeMessages": pycodestyle.DEFAULT_IGNORE,
                "IncludeMessages": "",
                "RepeatMessages": False,
                "FixCodes": "",
                "FixIssues": False,
            }
        if "EnabledCheckerCategories" not in self.__data:
            self.__data["EnabledCheckerCategories"] = ",".join(
                CodeStyleCheckerDialog.checkCategories.keys())
        if "MaxLineLength" not in self.__data:
            self.__data["MaxLineLength"] = pycodestyle.MAX_LINE_LENGTH
        if "MaxDocLineLength" not in self.__data:
            # Use MAX_LINE_LENGTH to avoid messages on existing code
            self.__data["MaxDocLineLength"] = pycodestyle.MAX_LINE_LENGTH
        if "BlankLines" not in self.__data:
            self.__data["BlankLines"] = (2, 1)
            # top level, method
        if "HangClosing" not in self.__data:
            self.__data["HangClosing"] = False
        if "NoFixCodes" not in self.__data:
            self.__data["NoFixCodes"] = "E501"
        if "DocstringType" not in self.__data:
            self.__data["DocstringType"] = "pep257"
        if "ShowIgnored" not in self.__data:
            self.__data["ShowIgnored"] = False
        if "MaxCodeComplexity" not in self.__data:
            self.__data["MaxCodeComplexity"] = 10
        if "LineComplexity" not in self.__data:
            self.__data["LineComplexity"] = 15
        if "LineComplexityScore" not in self.__data:
            self.__data["LineComplexityScore"] = 10
        if "ValidEncodings" not in self.__data:
            self.__data["ValidEncodings"] = (
                MiscellaneousCheckerDefaultArgs["CodingChecker"]
            )
        if (
            "CopyrightMinFileSize" not in self.__data or
            "CopyrightAuthor" not in self.__data
        ):
            self.__data["CopyrightMinFileSize"] = (
                MiscellaneousCheckerDefaultArgs[
                    "CopyrightChecker"]["MinFilesize"]
            )
            self.__data["CopyrightAuthor"] = (
                MiscellaneousCheckerDefaultArgs["CopyrightChecker"]["Author"]
            )
        if "FutureChecker" not in self.__data:
            self.__data["FutureChecker"] = ""
        if "BuiltinsChecker" not in self.__data:
            self.__data["BuiltinsChecker"] = copy.deepcopy(
                MiscellaneousCheckerDefaultArgs["BuiltinsChecker"]
            )
        
        if "CommentedCodeChecker" not in self.__data:
            self.__data["CommentedCodeChecker"] = copy.deepcopy(
                MiscellaneousCheckerDefaultArgs["CommentedCodeChecker"]
            )
        if "WhiteList" not in self.__data["CommentedCodeChecker"]:
            self.__data["CommentedCodeChecker"]["WhiteList"] = (
                MiscellaneousCheckerDefaultArgs[
                    "CommentedCodeChecker"]["WhiteList"][:]
            )
        
        if "AnnotationsChecker" not in self.__data:
            self.__data["AnnotationsChecker"] = {
                "MinimumCoverage": 75,
                "MaximumComplexity": 3,
            }
        
        if "SecurityChecker" not in self.__data:
            from .Security.SecurityDefaults import SecurityDefaults
            self.__data["SecurityChecker"] = {
                "HardcodedTmpDirectories":
                    SecurityDefaults["hardcoded_tmp_directories"],
                "InsecureHashes":
                    SecurityDefaults["insecure_hashes"],
                "InsecureSslProtocolVersions":
                    SecurityDefaults["insecure_ssl_protocol_versions"],
                "WeakKeySizeDsaHigh":
                    str(SecurityDefaults["weak_key_size_dsa_high"]),
                "WeakKeySizeDsaMedium":
                    str(SecurityDefaults["weak_key_size_dsa_medium"]),
                "WeakKeySizeRsaHigh":
                    str(SecurityDefaults["weak_key_size_rsa_high"]),
                "WeakKeySizeRsaMedium":
                    str(SecurityDefaults["weak_key_size_rsa_medium"]),
                "WeakKeySizeEcHigh":
                    str(SecurityDefaults["weak_key_size_ec_high"]),
                "WeakKeySizeEcMedium":
                    str(SecurityDefaults["weak_key_size_ec_medium"]),
                "CheckTypedException":
                    SecurityDefaults["check_typed_exception"],
            }
        
        self.__initCategoriesList(self.__data["EnabledCheckerCategories"])
        self.excludeFilesEdit.setText(self.__data["ExcludeFiles"])
        self.excludeMessagesEdit.setText(self.__data["ExcludeMessages"])
        self.includeMessagesEdit.setText(self.__data["IncludeMessages"])
        self.repeatCheckBox.setChecked(self.__data["RepeatMessages"])
        self.fixIssuesEdit.setText(self.__data["FixCodes"])
        self.noFixIssuesEdit.setText(self.__data["NoFixCodes"])
        self.fixIssuesCheckBox.setChecked(self.__data["FixIssues"])
        self.ignoredCheckBox.setChecked(self.__data["ShowIgnored"])
        self.lineLengthSpinBox.setValue(self.__data["MaxLineLength"])
        self.docLineLengthSpinBox.setValue(self.__data["MaxDocLineLength"])
        self.blankBeforeTopLevelSpinBox.setValue(self.__data["BlankLines"][0])
        self.blankBeforeMethodSpinBox.setValue(self.__data["BlankLines"][1])
        self.hangClosingCheckBox.setChecked(self.__data["HangClosing"])
        self.docTypeComboBox.setCurrentIndex(
            self.docTypeComboBox.findData(self.__data["DocstringType"]))
        self.complexitySpinBox.setValue(self.__data["MaxCodeComplexity"])
        self.lineComplexitySpinBox.setValue(self.__data["LineComplexity"])
        self.lineComplexityScoreSpinBox.setValue(
            self.__data["LineComplexityScore"])
        self.encodingsEdit.setText(self.__data["ValidEncodings"])
        self.copyrightFileSizeSpinBox.setValue(
            self.__data["CopyrightMinFileSize"])
        self.copyrightAuthorEdit.setText(self.__data["CopyrightAuthor"])
        self.__initFuturesList(self.__data["FutureChecker"])
        self.__initBuiltinsIgnoreList(self.__data["BuiltinsChecker"])
        self.aggressiveCheckBox.setChecked(
            self.__data["CommentedCodeChecker"]["Aggressive"])
        self.__initCommentedCodeCheckerWhiteList(
            self.__data["CommentedCodeChecker"]["WhiteList"])
        self.minAnnotationsCoverageSpinBox.setValue(
            self.__data["AnnotationsChecker"]["MinimumCoverage"])
        self.maxAnnotationsComplexitySpinBox.setValue(
            self.__data["AnnotationsChecker"]["MaximumComplexity"])
        
        # security
        self.tmpDirectoriesEdit.setPlainText("\n".join(
            self.__data["SecurityChecker"]["HardcodedTmpDirectories"]))
        self.hashesEdit.setText(", ".join(
            self.__data["SecurityChecker"]["InsecureHashes"]))
        self.insecureSslProtocolsEdit.setPlainText("\n".join(
            self.__data["SecurityChecker"]["InsecureSslProtocolVersions"]))
        self.dsaHighRiskCombo.setCurrentText(
            self.__data["SecurityChecker"]["WeakKeySizeDsaHigh"])
        self.dsaMediumRiskCombo.setCurrentText(
            self.__data["SecurityChecker"]["WeakKeySizeDsaMedium"])
        self.rsaHighRiskCombo.setCurrentText(
            self.__data["SecurityChecker"]["WeakKeySizeRsaHigh"])
        self.rsaMediumRiskCombo.setCurrentText(
            self.__data["SecurityChecker"]["WeakKeySizeRsaMedium"])
        self.ecHighRiskCombo.setCurrentText(
            self.__data["SecurityChecker"]["WeakKeySizeEcHigh"])
        self.ecMediumRiskCombo.setCurrentText(
            self.__data["SecurityChecker"]["WeakKeySizeEcMedium"])
        self.typedExceptionsCheckBox.setChecked(
            self.__data["SecurityChecker"]["CheckTypedException"])
        
        self.__cleanupData()
    
    def __prepareProgress(self):
        """
        Private method to prepare the progress tab for the next run.
        """
        self.progressList.clear()
        if len(self.files) > 0:
            self.checkProgress.setMaximum(len(self.files))
            self.checkProgressLabel.setVisible(len(self.files) > 1)
            self.checkProgress.setVisible(len(self.files) > 1)
            if len(self.files) > 1:
                if self.__project:
                    self.progressList.addItems([
                        os.path.join("...", self.__project.getRelativePath(f))
                        for f in self.files
                    ])
                else:
                    self.progressList.addItems(self.files)
        
        QApplication.processEvents()
    
    def start(self, fn, save=False, repeat=None):
        """
        Public slot to start the code style check.
        
        @param fn file or list of files or directory to be checked
        @type str or list of str
        @param save flag indicating to save the given file/file list/directory
        @type bool
        @param repeat state of the repeat check box if it is not None
        @type None or bool
        """
        if self.__project is None:
            self.__project = e5App().getObject("Project")
        
        self.mainWidget.setCurrentWidget(self.progressTab)
        
        self.cancelled = False
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.cancelButton.setEnabled(True)
        self.cancelButton.setDefault(True)
        self.statisticsButton.setEnabled(False)
        self.showButton.setEnabled(False)
        self.fixButton.setEnabled(False)
        self.startButton.setEnabled(False)
        self.restartButton.setEnabled(False)
        if repeat is not None:
            self.repeatCheckBox.setChecked(repeat)
        self.checkProgress.setVisible(True)
        QApplication.processEvents()
        
        if save:
            self.__fileOrFileList = fn
        
        if isinstance(fn, list):
            self.files = fn[:]
        elif os.path.isdir(fn):
            self.files = []
            extensions = set(Preferences.getPython("Python3Extensions"))
            for ext in extensions:
                self.files.extend(Utilities.direntries(
                    fn, True, '*{0}'.format(ext), 0))
        else:
            self.files = [fn]
        
        # filter the list depending on the filter string
        if self.files:
            filterString = self.excludeFilesEdit.text()
            filterList = [f.strip() for f in filterString.split(",")
                          if f.strip()]
            for fileFilter in filterList:
                self.files = [
                    f for f in self.files
                    if not fnmatch.fnmatch(f, fileFilter.strip())
                ]
        
        self.__errorItem = None
        self.__resetStatistics()
        self.__clearErrors(self.files)
        self.__cleanupData()
        self.__prepareProgress()
        
        if len(self.files) > 0:
            self.securityNoteLabel.setVisible(
                "S" in self.__getCategories(True, asList=True))
            
            # extract the configuration values
            excludeMessages = self.__assembleExcludeMessages()
            includeMessages = self.includeMessagesEdit.text()
            repeatMessages = self.repeatCheckBox.isChecked()
            fixCodes = self.fixIssuesEdit.text()
            noFixCodes = self.noFixIssuesEdit.text()
            self.__noFixCodesList = [
                c.strip() for c in noFixCodes.split(",") if c.strip()
            ]
            fixIssues = self.fixIssuesCheckBox.isChecked() and repeatMessages
            self.showIgnored = (
                self.ignoredCheckBox.isChecked() and repeatMessages
            )
            maxLineLength = self.lineLengthSpinBox.value()
            maxDocLineLength = self.docLineLengthSpinBox.value()
            blankLines = (
                self.blankBeforeTopLevelSpinBox.value(),
                self.blankBeforeMethodSpinBox.value()
            )
            hangClosing = self.hangClosingCheckBox.isChecked()
            docType = self.docTypeComboBox.itemData(
                self.docTypeComboBox.currentIndex())
            codeComplexityArgs = {
                "McCabeComplexity": self.complexitySpinBox.value(),
                "LineComplexity": self.lineComplexitySpinBox.value(),
                "LineComplexityScore": self.lineComplexityScoreSpinBox.value(),
            }
            miscellaneousArgs = {
                "CodingChecker": self.encodingsEdit.text(),
                "CopyrightChecker": {
                    "MinFilesize": self.copyrightFileSizeSpinBox.value(),
                    "Author": self.copyrightAuthorEdit.text(),
                },
                "FutureChecker": self.__getSelectedFutureImports(),
                "BuiltinsChecker": self.__getBuiltinsIgnoreList(),
                "CommentedCodeChecker": {
                    "Aggressive": self.aggressiveCheckBox.isChecked(),
                    "WhiteList": self.__getCommentedCodeCheckerWhiteList(),
                }
            }
            annotationArgs = {
                "MinimumCoverage":
                    self.minAnnotationsCoverageSpinBox.value(),
                "MaximumComplexity":
                    self.maxAnnotationsComplexitySpinBox.value(),
            }
            
            securityArgs = {
                "hardcoded_tmp_directories": [
                    t.strip()
                    for t in self.tmpDirectoriesEdit.toPlainText().splitlines()
                ],
                "insecure_hashes": [
                    h.strip()
                    for h in self.hashesEdit.text().split(",")
                ],
                "insecure_ssl_protocol_versions": [
                    p.strip()
                    for p in self.insecureSslProtocolsEdit.toPlainText()
                    .splitlines()
                ],
                "weak_key_size_dsa_high":
                    int(self.dsaHighRiskCombo.currentText()),
                "weak_key_size_dsa_medium":
                    int(self.dsaMediumRiskCombo.currentText()),
                "weak_key_size_rsa_high":
                    int(self.rsaHighRiskCombo.currentText()),
                "weak_key_size_rsa_medium":
                    int(self.rsaMediumRiskCombo.currentText()),
                "weak_key_size_ec_high":
                    int(self.ecHighRiskCombo.currentText()),
                "weak_key_size_ec_medium":
                    int(self.ecMediumRiskCombo.currentText()),
                "check_typed_exception":
                    self.typedExceptionsCheckBox.isChecked(),
            }
            
            self.__options = [excludeMessages, includeMessages, repeatMessages,
                              fixCodes, noFixCodes, fixIssues, maxLineLength,
                              maxDocLineLength, blankLines, hangClosing,
                              docType, codeComplexityArgs, miscellaneousArgs,
                              annotationArgs, securityArgs]
            
            # now go through all the files
            self.progress = 0
            self.files.sort()
            if len(self.files) == 1:
                self.__batch = False
                self.mainWidget.setCurrentWidget(self.resultsTab)
                self.check()
            else:
                self.__batch = True
                self.checkBatch()
        else:
            self.results = CodeStyleCheckerDialog.noFiles
            self.__finished = False
            self.__finish()
    
    def __modifyOptions(self, source):
        """
        Private method to modify the options based on eflag: entries.
        
        This method looks for comment lines like '# eflag: noqa = M601'
        at the end of the source in order to extend the list of excluded
        messages for one file only.
        
        @param source source text
        @type list of str or str
        @return list of checker options
        @rtype list
        """
        options = self.__options[:]
        flags = Utilities.extractFlags(source)
        if "noqa" in flags and isinstance(flags["noqa"], basestring):
            excludeMessages = options[0].strip().rstrip(",")
            if excludeMessages:
                excludeMessages += ","
            excludeMessages += flags["noqa"]
            options[0] = excludeMessages
        return options
    
    def check(self, codestring=''):
        """
        Public method to start a style check for one file.
        
        The results are reported to the __processResult slot.
        
        @param codestring optional sourcestring
        @type str
        """
        if not self.files:
            self.checkProgressLabel.setPath("")
            self.checkProgress.setMaximum(1)
            self.checkProgress.setValue(1)
            self.__finish()
            return
        
        self.filename = self.files.pop(0)
        self.checkProgress.setValue(self.progress)
        self.checkProgressLabel.setPath(self.filename)
        QApplication.processEvents()

        if self.cancelled:
            self.__resort()
            return
        
        self.__lastFileItem = None
        
        if codestring:
            source = codestring.splitlines(True)
            encoding = Utilities.get_coding(source)
        else:
            try:
                source, encoding = Utilities.readEncodedFile(
                    self.filename)
                source = source.splitlines(True)
            except (UnicodeError, OSError) as msg:
                self.results = CodeStyleCheckerDialog.hasResults
                self.__createFileErrorItem(self.filename, str(msg))
                self.progress += 1
                # Continue with next file
                self.check()
                return
        if encoding.endswith(
                ('-selected', '-default', '-guessed', '-ignore')):
            encoding = encoding.rsplit('-', 1)[0]
        
        options = self.__modifyOptions(source)
        
        errors = []
        self.__itms = []
        for error, itm in self.__onlyFixes.pop(self.filename, []):
            errors.append(error)
            self.__itms.append(itm)
        
        eol = self.__getEol(self.filename)
        args = options + [
            errors, eol, encoding, Preferences.getEditor("CreateBackupFile")
        ]
        self.__finished = False
        self.styleCheckService.styleCheck(
            None, self.filename, source, args)
    
    def checkBatch(self):
        """
        Public method to start a style check batch job.
        
        The results are reported to the __processResult slot.
        """
        self.__lastFileItem = None
        
        self.checkProgressLabel.setPath(self.tr("Preparing files..."))
        progress = 0
        
        argumentsList = []
        for filename in self.files:
            progress += 1
            self.checkProgress.setValue(progress)
            QApplication.processEvents()
            
            try:
                source, encoding = Utilities.readEncodedFile(
                    filename)
                source = source.splitlines(True)
            except (UnicodeError, OSError) as msg:
                self.results = CodeStyleCheckerDialog.hasResults
                self.__createFileErrorItem(filename, str(msg))
                continue
            
            if encoding.endswith(
                    ('-selected', '-default', '-guessed', '-ignore')):
                encoding = encoding.rsplit('-', 1)[0]
            
            options = self.__modifyOptions(source)
            
            errors = []
            self.__itms = []
            for error, itm in self.__onlyFixes.pop(filename, []):
                errors.append(error)
                self.__itms.append(itm)
            
            eol = self.__getEol(filename)
            args = options + [
                errors, eol, encoding,
                Preferences.getEditor("CreateBackupFile")
            ]
            argumentsList.append((filename, source, args))
        
        # reset the progress bar to the checked files
        self.checkProgress.setValue(self.progress)
        self.checkProgressLabel.setPath(self.tr("Transferring data..."))
        QApplication.processEvents()
        
        self.__finished = False
        self.styleCheckService.styleBatchCheck(argumentsList)
    
    def __batchFinished(self):
        """
        Private slot handling the completion of a batch job.
        """
        self.checkProgressLabel.setPath("")
        self.checkProgress.setMaximum(1)
        self.checkProgress.setValue(1)
        self.__finish()
    
    def __processError(self, fn, msg):
        """
        Private slot to process an error indication from the service.
        
        @param fn filename of the file
        @type str
        @param msg error message
        @type str
        """
        self.__createErrorItem(fn, msg)
        
        if not self.__batch:
            self.check()
    
    def __processResult(self, fn, codeStyleCheckerStats, fixes, results):
        """
        Private slot called after perfoming a style check on one file.
        
        @param fn filename of the just checked file
        @type str
        @param codeStyleCheckerStats stats of style and name check
        @type dict
        @param fixes number of applied fixes
        @type int
        @param results dictionary containing check result data
        @type dict
        """
        if self.__finished:
            return
        
        # Check if it's the requested file, otherwise ignore signal if not
        # in batch mode
        if not self.__batch and fn != self.filename:
            return
        
        # disable updates of the list for speed
        self.resultList.setUpdatesEnabled(False)
        self.resultList.setSortingEnabled(False)
        
        fixed = None
        ignoredErrors = 0
        securityOk = 0
        if self.__itms:
            for itm, result in zip(self.__itms, results):
                self.__modifyFixedResultItem(itm, result)
            self.__updateFixerStatistics(fixes)
        else:
            self.__lastFileItem = None
            
            for result in results:
                if result["ignored"]:
                    ignoredErrors += 1
                    if self.showIgnored:
                        result["display"] = self.tr(
                            "{0} (ignored)"
                        ).format(result["display"])
                    else:
                        continue
                
                elif result["securityOk"]:
                    securityOk += 1
                    continue
                
                self.results = CodeStyleCheckerDialog.hasResults
                self.__createResultItem(fn, result)

            self.__updateStatistics(
                codeStyleCheckerStats, fixes, ignoredErrors, securityOk)
        
        if fixed:
            vm = e5App().getObject("ViewManager")
            editor = vm.getOpenEditor(fn)
            if editor:
                editor.refresh()
        
        self.progress += 1
        
        self.__resort()
        # reenable updates of the list
        self.resultList.setSortingEnabled(True)
        self.resultList.setUpdatesEnabled(True)
        
        self.__updateProgress(fn)
        
        if not self.__batch:
            self.check()
    
    def __updateProgress(self, fn):
        """
        Private method to update the progress tab.
        
        @param fn filename of the just checked file
        @type str
        """
        if self.__project:
            fn = os.path.join("...", self.__project.getRelativePath(fn))
        
        self.checkProgress.setValue(self.progress)
        self.checkProgressLabel.setPath(fn)
        
        # remove file from the list of jobs to do
        fileItems = self.progressList.findItems(fn, Qt.MatchFlag.MatchExactly)
        if fileItems:
            row = self.progressList.row(fileItems[0])
            self.progressList.takeItem(row)
        
        QApplication.processEvents()
    
    def __finish(self):
        """
        Private slot called when the code style check finished or the user
        pressed the cancel button.
        """
        if not self.__finished:
            self.__finished = True
            
            self.cancelled = True
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Close).setEnabled(True)
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Close).setDefault(True)
            self.cancelButton.setEnabled(False)
            self.statisticsButton.setEnabled(True)
            self.showButton.setEnabled(True)
            self.startButton.setEnabled(True)
            self.restartButton.setEnabled(True)
            
            if self.results != CodeStyleCheckerDialog.hasResults:
                if self.results == CodeStyleCheckerDialog.noResults:
                    QTreeWidgetItem(
                        self.resultList, [self.tr('No issues found.')])
                else:
                    QTreeWidgetItem(
                        self.resultList,
                        [self.tr('No files found (check your ignore list).')])
                QApplication.processEvents()
                self.showButton.setEnabled(False)
            else:
                self.showButton.setEnabled(True)
            self.resultList.header().resizeSections(
                QHeaderView.ResizeMode.ResizeToContents)
            self.resultList.header().setStretchLastSection(True)
            
            self.checkProgress.setVisible(False)
            self.checkProgressLabel.setVisible(False)
            
            self.mainWidget.setCurrentWidget(self.resultsTab)
    
    def __getEol(self, fn):
        """
        Private method to get the applicable eol string.
        
        @param fn filename where to determine the line ending
        @type str
        @return eol string
        @rtype str
        """
        if self.__project.isOpen() and self.__project.isProjectFile(fn):
            eol = self.__project.getEolString()
        else:
            eol = Utilities.linesep()
        return eol
    
    @pyqtSlot()
    def on_startButton_clicked(self):
        """
        Private slot to start a code style check run.
        """
        self.__cleanupData()
        
        if self.__forProject:
            data = {
                "EnabledCheckerCategories": self.__getCategories(True),
                "ExcludeFiles": self.excludeFilesEdit.text(),
                "ExcludeMessages": self.excludeMessagesEdit.text(),
                "IncludeMessages": self.includeMessagesEdit.text(),
                "RepeatMessages": self.repeatCheckBox.isChecked(),
                "FixCodes": self.fixIssuesEdit.text(),
                "NoFixCodes": self.noFixIssuesEdit.text(),
                "FixIssues": self.fixIssuesCheckBox.isChecked(),
                "ShowIgnored": self.ignoredCheckBox.isChecked(),
                "MaxLineLength": self.lineLengthSpinBox.value(),
                "MaxDocLineLength": self.docLineLengthSpinBox.value(),
                "BlankLines": (
                    self.blankBeforeTopLevelSpinBox.value(),
                    self.blankBeforeMethodSpinBox.value()
                ),
                "HangClosing": self.hangClosingCheckBox.isChecked(),
                "DocstringType": self.docTypeComboBox.itemData(
                    self.docTypeComboBox.currentIndex()),
                "MaxCodeComplexity": self.complexitySpinBox.value(),
                "LineComplexity": self.lineComplexitySpinBox.value(),
                "LineComplexityScore": self.lineComplexityScoreSpinBox.value(),
                "ValidEncodings": self.encodingsEdit.text(),
                "CopyrightMinFileSize": self.copyrightFileSizeSpinBox.value(),
                "CopyrightAuthor": self.copyrightAuthorEdit.text(),
                "FutureChecker": self.__getSelectedFutureImports(),
                "BuiltinsChecker": self.__getBuiltinsIgnoreList(),
                "CommentedCodeChecker": {
                    "Aggressive": self.aggressiveCheckBox.isChecked(),
                    "WhiteList": self.__getCommentedCodeCheckerWhiteList(),
                },
                "AnnotationsChecker": {
                    "MinimumCoverage":
                        self.minAnnotationsCoverageSpinBox.value(),
                    "MaximumComplexity":
                        self.maxAnnotationsComplexitySpinBox.value(),
                },
                "SecurityChecker": {
                    "HardcodedTmpDirectories": [
                        t.strip()
                        for t in self.tmpDirectoriesEdit.toPlainText()
                        .splitlines()
                    ],
                    "InsecureHashes": [
                        h.strip()
                        for h in self.hashesEdit.text().split(",")
                    ],
                    "InsecureSslProtocolVersions": [
                        p.strip()
                        for p in self.insecureSslProtocolsEdit.toPlainText()
                        .splitlines()
                    ],
                    "WeakKeySizeDsaHigh":
                        self.dsaHighRiskCombo.currentText(),
                    "WeakKeySizeDsaMedium":
                        self.dsaMediumRiskCombo.currentText(),
                    "WeakKeySizeRsaHigh":
                        self.rsaHighRiskCombo.currentText(),
                    "WeakKeySizeRsaMedium":
                        self.rsaMediumRiskCombo.currentText(),
                    "WeakKeySizeEcHigh":
                        self.ecHighRiskCombo.currentText(),
                    "WeakKeySizeEcMedium":
                        self.ecMediumRiskCombo.currentText(),
                    "CheckTypedException":
                        self.typedExceptionsCheckBox.isChecked(),
                },
            }
            if data != self.__data:
                self.__data = data
                self.__project.setData("CHECKERSPARMS", "Pep8Checker",
                                       self.__data)
        
        self.resultList.clear()
        self.results = CodeStyleCheckerDialog.noResults
        self.cancelled = False
        
        self.start(self.__fileOrFileList)
    
    @pyqtSlot()
    def on_restartButton_clicked(self):
        """
        Private slot to restart a code style check run.
        """
        self.on_startButton_clicked()
    
    def __selectCodes(self, edit, categories, showFixCodes):
        """
        Private method to select message codes via a selection dialog.
        
        @param edit reference of the line edit to be populated
        @type QLineEdit
        @param categories list of message categories to omit
        @type list of str
        @param showFixCodes flag indicating to show a list of fixable
            issues
        @type bool
        """
        from .CodeStyleCodeSelectionDialog import CodeStyleCodeSelectionDialog
        dlg = CodeStyleCodeSelectionDialog(edit.text(), categories,
                                           showFixCodes, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            edit.setText(dlg.getSelectedCodes())
    
    @pyqtSlot()
    def on_excludeMessagesSelectButton_clicked(self):
        """
        Private slot to select the message codes to be excluded via a
        selection dialog.
        """
        self.__selectCodes(self.excludeMessagesEdit,
                           self.__getCategories(False, asList=True),
                           False)
    
    @pyqtSlot()
    def on_includeMessagesSelectButton_clicked(self):
        """
        Private slot to select the message codes to be included via a
        selection dialog.
        """
        self.__selectCodes(self.includeMessagesEdit,
                           self.__getCategories(True, asList=True),
                           False)
    
    @pyqtSlot()
    def on_fixIssuesSelectButton_clicked(self):
        """
        Private slot to select the issue codes to be fixed via a
        selection dialog.
        """
        self.__selectCodes(self.fixIssuesEdit, [], True)
    
    @pyqtSlot()
    def on_noFixIssuesSelectButton_clicked(self):
        """
        Private slot to select the issue codes not to be fixed via a
        selection dialog.
        """
        self.__selectCodes(self.noFixIssuesEdit, [], True)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_resultList_itemActivated(self, item, column):
        """
        Private slot to handle the activation of an item.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column column the item was activated in
        @type int
        """
        if self.results != CodeStyleCheckerDialog.hasResults:
            return
        
        if item.parent():
            fn = os.path.abspath(item.data(0, self.filenameRole))
            lineno = item.data(0, self.lineRole)
            position = item.data(0, self.positionRole)
            message = item.data(0, self.messageRole)
            code = item.data(0, self.codeRole)
            
            vm = e5App().getObject("ViewManager")
            vm.openSourceFile(fn, lineno=lineno, pos=position + 1)
            editor = vm.getOpenEditor(fn)
            
            if code in ["E901", "E902"]:
                editor.toggleSyntaxError(lineno, 0, True, message, True)
            else:
                editor.toggleWarning(
                    lineno, 0, True, message, warningType=editor.WarningStyle)
            
            editor.updateVerticalScrollBar()
    
    @pyqtSlot()
    def on_resultList_itemSelectionChanged(self):
        """
        Private slot to change the dialog state depending on the selection.
        """
        self.fixButton.setEnabled(len(self.__getSelectedFixableItems()) > 0)
    
    @pyqtSlot()
    def on_showButton_clicked(self):
        """
        Private slot to handle the "Show" button press.
        """
        vm = e5App().getObject("ViewManager")
        
        selectedIndexes = []
        for index in range(self.resultList.topLevelItemCount()):
            if self.resultList.topLevelItem(index).isSelected():
                selectedIndexes.append(index)
        if len(selectedIndexes) == 0:
            selectedIndexes = list(range(self.resultList.topLevelItemCount()))
        for index in selectedIndexes:
            itm = self.resultList.topLevelItem(index)
            fn = os.path.abspath(itm.data(0, self.filenameRole))
            vm.openSourceFile(fn, 1)
            editor = vm.getOpenEditor(fn)
            editor.clearStyleWarnings()
            for cindex in range(itm.childCount()):
                citm = itm.child(cindex)
                lineno = citm.data(0, self.lineRole)
                message = citm.data(0, self.messageRole)
                editor.toggleWarning(
                    lineno, 0, True, message, warningType=editor.WarningStyle)
        
        # go through the list again to clear warning markers for files,
        # that are ok
        openFiles = vm.getOpenFilenames()
        errorFiles = []
        for index in range(self.resultList.topLevelItemCount()):
            itm = self.resultList.topLevelItem(index)
            errorFiles.append(
                os.path.abspath(itm.data(0, self.filenameRole)))
        for file in openFiles:
            if file not in errorFiles:
                editor = vm.getOpenEditor(file)
                editor.clearStyleWarnings()
        
        editor = vm.activeWindow()
        editor.updateVerticalScrollBar()
    
    @pyqtSlot()
    def on_statisticsButton_clicked(self):
        """
        Private slot to show the statistics dialog.
        """
        from .CodeStyleStatisticsDialog import CodeStyleStatisticsDialog
        dlg = CodeStyleStatisticsDialog(self.__statistics, self)
        dlg.exec()
    
    @pyqtSlot()
    def on_loadDefaultButton_clicked(self):
        """
        Private slot to load the default configuration values.
        """
        self.__initCategoriesList(Preferences.Prefs.settings.value(
            "PEP8/EnabledCheckerCategories",
            ",".join(CodeStyleCheckerDialog.checkCategories.keys())))
        self.excludeFilesEdit.setText(Preferences.Prefs.settings.value(
            "PEP8/ExcludeFilePatterns", ""))
        self.excludeMessagesEdit.setText(Preferences.Prefs.settings.value(
            "PEP8/ExcludeMessages", pycodestyle.DEFAULT_IGNORE))
        self.includeMessagesEdit.setText(Preferences.Prefs.settings.value(
            "PEP8/IncludeMessages", ""))
        self.repeatCheckBox.setChecked(Preferences.toBool(
            Preferences.Prefs.settings.value("PEP8/RepeatMessages", False)))
        self.fixIssuesEdit.setText(Preferences.Prefs.settings.value(
            "PEP8/FixCodes", ""))
        self.noFixIssuesEdit.setText(Preferences.Prefs.settings.value(
            "PEP8/NoFixCodes", "E501"))
        self.fixIssuesCheckBox.setChecked(Preferences.toBool(
            Preferences.Prefs.settings.value("PEP8/FixIssues", False)))
        self.ignoredCheckBox.setChecked(Preferences.toBool(
            Preferences.Prefs.settings.value("PEP8/ShowIgnored", False)))
        self.lineLengthSpinBox.setValue(int(Preferences.Prefs.settings.value(
            "PEP8/MaxLineLength", pycodestyle.MAX_LINE_LENGTH)))
        # Use MAX_LINE_LENGTH to avoid messages on existing code
        self.docLineLengthSpinBox.setValue(int(
            Preferences.Prefs.settings.value(
                "PEP8/MaxDocLineLength", pycodestyle.MAX_LINE_LENGTH)))
        self.blankBeforeTopLevelSpinBox.setValue(
            int(Preferences.Prefs.settings.value(
                "PEP8/BlankLinesBeforeTopLevel", 2)))
        self.blankBeforeMethodSpinBox.setValue(
            int(Preferences.Prefs.settings.value(
                "PEP8/BlankLinesBeforeMethod", 1)))
        self.hangClosingCheckBox.setChecked(Preferences.toBool(
            Preferences.Prefs.settings.value("PEP8/HangClosing", False)))
        self.docTypeComboBox.setCurrentIndex(self.docTypeComboBox.findData(
            Preferences.Prefs.settings.value("PEP8/DocstringType", "pep257")))
        self.complexitySpinBox.setValue(int(Preferences.Prefs.settings.value(
            "PEP8/MaxCodeComplexity", 10)))
        self.lineComplexitySpinBox.setValue(
            int(Preferences.Prefs.settings.value(
                "PEP8/LineComplexity", 15)))
        self.lineComplexityScoreSpinBox.setValue(
            int(Preferences.Prefs.settings.value(
                "PEP8/LineComplexityScore", 10)))
        self.encodingsEdit.setText(Preferences.Prefs.settings.value(
            "PEP8/ValidEncodings",
            MiscellaneousCheckerDefaultArgs["CodingChecker"]
        ))
        self.copyrightFileSizeSpinBox.setValue(int(
            Preferences.Prefs.settings.value(
                "PEP8/CopyrightMinFileSize",
                MiscellaneousCheckerDefaultArgs[
                    "CopyrightChecker"]["MinFilesize"]
            )
        ))
        self.copyrightAuthorEdit.setText(
            Preferences.Prefs.settings.value(
                "PEP8/CopyrightAuthor",
                MiscellaneousCheckerDefaultArgs["CopyrightChecker"]["Author"]
            )
        )
        self.__initFuturesList(
            Preferences.Prefs.settings.value("PEP8/FutureChecker", ""))
        self.__initBuiltinsIgnoreList(Preferences.toDict(
            Preferences.Prefs.settings.value(
                "PEP8/BuiltinsChecker",
                MiscellaneousCheckerDefaultArgs["BuiltinsChecker"]
            ))
        )
        self.aggressiveCheckBox.setChecked(Preferences.toBool(
            Preferences.Prefs.settings.value(
                "PEP8/AggressiveSearch",
                MiscellaneousCheckerDefaultArgs[
                    "CommentedCodeChecker"]["Aggressive"]
            )))
        self.__initCommentedCodeCheckerWhiteList(Preferences.toList(
            Preferences.Prefs.settings.value(
                "PEP8/CommentedCodeWhitelist",
                MiscellaneousCheckerDefaultArgs[
                    "CommentedCodeChecker"]["WhiteList"]
            )
        ))
        self.minAnnotationsCoverageSpinBox.setValue(int(
            Preferences.Prefs.settings.value(
                "PEP8/MinimumAnnotationsCoverage", 75)))
        self.maxAnnotationsComplexitySpinBox.setValue(int(
            Preferences.Prefs.settings.value(
                "PEP8/MaximumAnnotationComplexity", 3)))
        
        # security
        from .Security.SecurityDefaults import SecurityDefaults
        self.tmpDirectoriesEdit.setPlainText("\n".join(
            Preferences.toList(Preferences.Prefs.settings.value(
                "PEP8/HardcodedTmpDirectories",
                SecurityDefaults["hardcoded_tmp_directories"]))))
        self.hashesEdit.setText(", ".join(
            Preferences.toList(Preferences.Prefs.settings.value(
                "PEP8/InsecureHashes",
                SecurityDefaults["insecure_hashes"])))),
        self.insecureSslProtocolsEdit.setPlainText("\n".join(
            Preferences.toList(Preferences.Prefs.settings.value(
                "PEP8/InsecureSslProtocolVersions",
                SecurityDefaults["insecure_ssl_protocol_versions"])))),
        self.dsaHighRiskCombo.setCurrentText(
            Preferences.Prefs.settings.value(
                "PEP8/WeakKeySizeDsaHigh",
                str(SecurityDefaults["weak_key_size_dsa_high"])))
        self.dsaMediumRiskCombo.setCurrentText(
            Preferences.Prefs.settings.value(
                "PEP8/WeakKeySizeDsaMedium",
                str(SecurityDefaults["weak_key_size_dsa_medium"]))),
        self.rsaHighRiskCombo.setCurrentText(
            Preferences.Prefs.settings.value(
                "PEP8/WeakKeySizeRsaHigh",
                str(SecurityDefaults["weak_key_size_rsa_high"]))),
        self.rsaMediumRiskCombo.setCurrentText(
            Preferences.Prefs.settings.value(
                "PEP8/WeakKeySizeRsaMedium",
                str(SecurityDefaults["weak_key_size_rsa_medium"]))),
        self.ecHighRiskCombo.setCurrentText(
            Preferences.Prefs.settings.value(
                "PEP8/WeakKeySizeEcHigh",
                str(SecurityDefaults["weak_key_size_ec_high"]))),
        self.ecMediumRiskCombo.setCurrentText(
            Preferences.Prefs.settings.value(
                "PEP8/WeakKeySizeEcMedium",
                str(SecurityDefaults["weak_key_size_ec_medium"]))),
        self.typedExceptionsCheckBox.setChecked(Preferences.toBool(
            Preferences.Prefs.settings.value(
                "PEP8/CheckTypedException",
                SecurityDefaults["check_typed_exception"]))),
        
        self.__cleanupData()
    
    @pyqtSlot()
    def on_storeDefaultButton_clicked(self):
        """
        Private slot to store the current configuration values as
        default values.
        """
        Preferences.Prefs.settings.setValue(
            "PEP8/EnabledCheckerCategories", self.__getCategories(True))
        Preferences.Prefs.settings.setValue(
            "PEP8/ExcludeFilePatterns", self.excludeFilesEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/ExcludeMessages", self.excludeMessagesEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/IncludeMessages", self.includeMessagesEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/RepeatMessages", self.repeatCheckBox.isChecked())
        Preferences.Prefs.settings.setValue(
            "PEP8/FixCodes", self.fixIssuesEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/NoFixCodes", self.noFixIssuesEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/FixIssues", self.fixIssuesCheckBox.isChecked())
        Preferences.Prefs.settings.setValue(
            "PEP8/ShowIgnored", self.ignoredCheckBox.isChecked())
        Preferences.Prefs.settings.setValue(
            "PEP8/MaxLineLength", self.lineLengthSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/MaxDocLineLength", self.docLineLengthSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/BlankLinesBeforeTopLevel",
            self.blankBeforeTopLevelSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/BlankLinesBeforeMethod",
            self.blankBeforeMethodSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/HangClosing", self.hangClosingCheckBox.isChecked())
        Preferences.Prefs.settings.setValue(
            "PEP8/DocstringType", self.docTypeComboBox.itemData(
                self.docTypeComboBox.currentIndex()))
        Preferences.Prefs.settings.setValue(
            "PEP8/MaxCodeComplexity", self.complexitySpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/LineComplexity", self.lineComplexitySpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/LineComplexityScore",
            self.lineComplexityScoreSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/ValidEncodings", self.encodingsEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/CopyrightMinFileSize", self.copyrightFileSizeSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/CopyrightAuthor", self.copyrightAuthorEdit.text())
        Preferences.Prefs.settings.setValue(
            "PEP8/FutureChecker", self.__getSelectedFutureImports())
        Preferences.Prefs.settings.setValue(
            "PEP8/BuiltinsChecker", self.__getBuiltinsIgnoreList())
        Preferences.Prefs.settings.setValue(
            "PEP8/AggressiveSearch", self.aggressiveCheckBox.isChecked())
        Preferences.Prefs.settings.setValue(
            "PEP8/CommentedCodeWhitelist",
            self.__getCommentedCodeCheckerWhiteList())
        Preferences.Prefs.settings.setValue(
            "PEP8/MinimumAnnotationsCoverage",
            self.minAnnotationsCoverageSpinBox.value())
        Preferences.Prefs.settings.setValue(
            "PEP8/MaximumAnnotationComplexity",
            self.maxAnnotationsComplexitySpinBox.value())
        
        # security
        Preferences.Prefs.settings.setValue(
            "PEP8/HardcodedTmpDirectories",
            [t.strip()
             for t in self.tmpDirectoriesEdit.toPlainText().splitlines()
             ]),
        Preferences.Prefs.settings.setValue(
            "PEP8/InsecureHashes",
            [h.strip()
             for h in self.hashesEdit.text().split(",")
             ]),
        Preferences.Prefs.settings.setValue(
            "PEP8/InsecureSslProtocolVersions",
            [p.strip()
             for p in self.insecureSslProtocolsEdit.toPlainText().splitlines()
             ]),
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeDsaHigh",
            self.dsaHighRiskCombo.currentText()),
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeDsaMedium",
            self.dsaMediumRiskCombo.currentText()),
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeRsaHigh",
            self.rsaHighRiskCombo.currentText()),
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeRsaMedium",
            self.rsaMediumRiskCombo.currentText()),
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeEcHigh",
            self.ecHighRiskCombo.currentText()),
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeEcMedium",
            self.ecMediumRiskCombo.currentText()),
        Preferences.Prefs.settings.setValue(
            "PEP8/CheckTypedException",
            self.typedExceptionsCheckBox.isChecked()),
    
    @pyqtSlot()
    def on_resetDefaultButton_clicked(self):
        """
        Private slot to reset the configuration values to their default values.
        """
        Preferences.Prefs.settings.setValue(
            "PEP8/EnabledCheckerCategories",
            ",".join(CodeStyleCheckerDialog.checkCategories.keys()))
        Preferences.Prefs.settings.setValue("PEP8/ExcludeFilePatterns", "")
        Preferences.Prefs.settings.setValue(
            "PEP8/ExcludeMessages", pycodestyle.DEFAULT_IGNORE)
        Preferences.Prefs.settings.setValue("PEP8/IncludeMessages", "")
        Preferences.Prefs.settings.setValue("PEP8/RepeatMessages", False)
        Preferences.Prefs.settings.setValue("PEP8/FixCodes", "")
        Preferences.Prefs.settings.setValue("PEP8/NoFixCodes", "E501")
        Preferences.Prefs.settings.setValue("PEP8/FixIssues", False)
        Preferences.Prefs.settings.setValue("PEP8/ShowIgnored", False)
        Preferences.Prefs.settings.setValue(
            "PEP8/MaxLineLength", pycodestyle.MAX_LINE_LENGTH)
        # Hard reset to pycodestyle preferences
        Preferences.Prefs.settings.setValue(
            "PEP8/MaxDocLineLength", pycodestyle.MAX_DOC_LENGTH)
        Preferences.Prefs.settings.setValue(
            "PEP8/BlankLinesBeforeTopLevel", 2)
        Preferences.Prefs.settings.setValue(
            "PEP8/BlankLinesBeforeMethod", 1)
        Preferences.Prefs.settings.setValue("PEP8/HangClosing", False)
        Preferences.Prefs.settings.setValue("PEP8/DocstringType", "pep257")
        Preferences.Prefs.settings.setValue("PEP8/MaxCodeComplexity", 10)
        Preferences.Prefs.settings.setValue("PEP8/LineComplexity", 15)
        Preferences.Prefs.settings.setValue("PEP8/LineComplexityScore", 10)
        Preferences.Prefs.settings.setValue(
            "PEP8/ValidEncodings",
            MiscellaneousCheckerDefaultArgs["CodingChecker"]
        )
        Preferences.Prefs.settings.setValue(
            "PEP8/CopyrightMinFileSize",
            MiscellaneousCheckerDefaultArgs["CopyrightChecker"]["MinFilesize"]
        )
        Preferences.Prefs.settings.setValue(
            "PEP8/CopyrightAuthor",
            MiscellaneousCheckerDefaultArgs["CopyrightChecker"]["Author"]
        )
        Preferences.Prefs.settings.setValue("PEP8/FutureChecker", "")
        Preferences.Prefs.settings.setValue(
            "PEP8/BuiltinsChecker",
            MiscellaneousCheckerDefaultArgs["BuiltinsChecker"]
        )
        Preferences.Prefs.settings.setValue(
            "PEP8/AggressiveSearch",
            MiscellaneousCheckerDefaultArgs[
                "CommentedCodeChecker"]["Aggressive"]
        )
        Preferences.Prefs.settings.setValue(
            "PEP8/CommentedCodeWhitelist",
            MiscellaneousCheckerDefaultArgs[
                "CommentedCodeChecker"]["WhiteList"]
        )
        Preferences.Prefs.settings.setValue(
            "PEP8/MinimumAnnotationsCoverage", 75)
        Preferences.Prefs.settings.setValue(
            "PEP8/MaximumAnnotationComplexity", 3)
        
        # security
        from .Security.SecurityDefaults import SecurityDefaults
        Preferences.Prefs.settings.setValue(
            "PEP8/HardcodedTmpDirectories",
            SecurityDefaults["hardcoded_tmp_directories"])
        Preferences.Prefs.settings.setValue(
            "PEP8/InsecureHashes",
            SecurityDefaults["insecure_hashes"])
        Preferences.Prefs.settings.setValue(
            "PEP8/InsecureSslProtocolVersions",
            SecurityDefaults["insecure_ssl_protocol_versions"])
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeDsaHigh",
            str(SecurityDefaults["weak_key_size_dsa_high"]))
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeDsaMedium",
            str(SecurityDefaults["weak_key_size_dsa_medium"]))
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeRsaHigh",
            str(SecurityDefaults["weak_key_size_rsa_high"]))
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeRsaMedium",
            str(SecurityDefaults["weak_key_size_rsa_medium"]))
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeEcHigh",
            str(SecurityDefaults["weak_key_size_ec_high"]))
        Preferences.Prefs.settings.setValue(
            "PEP8/WeakKeySizeEcMedium",
            str(SecurityDefaults["weak_key_size_ec_medium"]))
        Preferences.Prefs.settings.setValue(
            "PEP8/CheckTypedException",
            SecurityDefaults["check_typed_exception"])
        
        # Update UI with default values
        self.on_loadDefaultButton_clicked()
    
    @pyqtSlot()
    def on_cancelButton_clicked(self):
        """
        Private slot to handle the "Cancel" button press.
        """
        if self.__batch:
            self.styleCheckService.cancelStyleBatchCheck()
            QTimer.singleShot(1000, self.__finish)
        else:
            self.__finish()
    
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked
        @type QAbstractButton
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
    
    def __clearErrors(self, files):
        """
        Private method to clear all warning markers of open editors to be
        checked.
        
        @param files list of files to be checked
        @type list of str
        """
        vm = e5App().getObject("ViewManager")
        openFiles = vm.getOpenFilenames()
        for file in [f for f in openFiles if f in files]:
            editor = vm.getOpenEditor(file)
            editor.clearStyleWarnings()
    
    @pyqtSlot()
    def on_fixButton_clicked(self):
        """
        Private slot to fix selected issues.
        
        Build a dictionary of issues to fix. Update the initialized __options.
        Then call check with the dict as keyparam to fix selected issues.
        """
        fixableItems = self.__getSelectedFixableItems()
        # dictionary of lists of tuples containing the issue and the item
        fixesDict = {}
        for itm in fixableItems:
            filename = itm.data(0, self.filenameRole)
            if filename not in fixesDict:
                fixesDict[filename] = []
            fixesDict[filename].append((
                {
                    "file": filename,
                    "line": itm.data(0, self.lineRole),
                    "offset": itm.data(0, self.positionRole),
                    "code": itm.data(0, self.codeRole),
                    "display": itm.data(0, self.messageRole),
                    "args": itm.data(0, self.argsRole),
                },
                itm
            ))
    
        # update the configuration values (3: fixCodes, 4: noFixCodes,
        # 5: fixIssues, 6: maxLineLength)
        self.__options[3] = self.fixIssuesEdit.text()
        self.__options[4] = self.noFixIssuesEdit.text()
        self.__options[5] = True
        self.__options[6] = self.lineLengthSpinBox.value()
        
        self.files = list(fixesDict.keys())
        # now go through all the files
        self.progress = 0
        self.files.sort()
        self.cancelled = False
        self.__onlyFixes = fixesDict
        self.check()
    
    def __getSelectedFixableItems(self):
        """
        Private method to extract all selected items for fixable issues.
        
        @return selected items for fixable issues
        @rtype list of QTreeWidgetItem
        """
        fixableItems = []
        for itm in self.resultList.selectedItems():
            if itm.childCount() > 0:
                for index in range(itm.childCount()):
                    citm = itm.child(index)
                    if self.__itemFixable(citm) and citm not in fixableItems:
                        fixableItems.append(citm)
            elif self.__itemFixable(itm) and itm not in fixableItems:
                fixableItems.append(itm)
        
        return fixableItems
    
    def __itemFixable(self, itm):
        """
        Private method to check, if an item has a fixable issue.
        
        @param itm item to be checked
        @type QTreeWidgetItem
        @return flag indicating a fixable issue
        @rtype bool
        """
        return (itm.data(0, self.fixableRole) and
                not itm.data(0, self.ignoredRole))
    
    def __initFuturesList(self, selectedFutures):
        """
        Private method to set the selected status of the future imports.
        
        @param selectedFutures comma separated list of expected future imports
        @type str
        """
        if selectedFutures:
            expectedImports = [
                i.strip() for i in selectedFutures.split(",")
                if bool(i.strip())]
        else:
            expectedImports = []
        for row in range(self.futuresList.count()):
            itm = self.futuresList.item(row)
            if itm.text() in expectedImports:
                itm.setCheckState(Qt.CheckState.Checked)
            else:
                itm.setCheckState(Qt.CheckState.Unchecked)
    
    def __getSelectedFutureImports(self):
        """
        Private method to get the expected future imports.
        
        @return expected future imports as a comma separated string
        @rtype str
        """
        selectedFutures = []
        for row in range(self.futuresList.count()):
            itm = self.futuresList.item(row)
            if itm.checkState() == Qt.CheckState.Checked:
                selectedFutures.append(itm.text())
        return ", ".join(selectedFutures)
    
    def __initBuiltinsIgnoreList(self, builtinsIgnoreDict):
        """
        Private method to populate the list of shadowed builtins to be ignored.
        
        @param builtinsIgnoreDict dictionary containing the builtins
            assignments to be ignored
        @type dict of list of str
        """
        self.builtinsAssignmentList.clear()
        for left, rightList in builtinsIgnoreDict.items():
            for right in rightList:
                QTreeWidgetItem(self.builtinsAssignmentList, [left, right])
        
        self.on_builtinsAssignmentList_itemSelectionChanged()
    
    def __getBuiltinsIgnoreList(self):
        """
        Private method to get a dictionary containing the builtins assignments
        to be ignored.
        
        @return dictionary containing the builtins assignments to be ignored
        @rtype dict of list of str
        """
        builtinsIgnoreDict = {}
        for row in range(self.builtinsAssignmentList.topLevelItemCount()):
            itm = self.builtinsAssignmentList.topLevelItem(row)
            left, right = itm.text(0), itm.text(1)
            if left not in builtinsIgnoreDict:
                builtinsIgnoreDict[left] = []
            builtinsIgnoreDict[left].append(right)
        
        return builtinsIgnoreDict
    
    @pyqtSlot()
    def on_builtinsAssignmentList_itemSelectionChanged(self):
        """
        Private slot to react upon changes of the selected builtin assignments.
        """
        self.deleteBuiltinButton.setEnabled(
            len(self.builtinsAssignmentList.selectedItems()) > 0)
    
    @pyqtSlot()
    def on_addBuiltinButton_clicked(self):
        """
        Private slot to add a built-in assignment to be ignored.
        """
        from .CodeStyleAddBuiltinIgnoreDialog import (
            CodeStyleAddBuiltinIgnoreDialog
        )
        dlg = CodeStyleAddBuiltinIgnoreDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            left, right = dlg.getData()
            QTreeWidgetItem(self.builtinsAssignmentList, [left, right])
    
    @pyqtSlot()
    def on_deleteBuiltinButton_clicked(self):
        """
        Private slot to delete the selected items from the list.
        """
        for itm in self.builtinsAssignmentList.selectedItems():
            index = self.builtinsAssignmentList.indexOfTopLevelItem(itm)
            self.builtinsAssignmentList.takeTopLevelItem(index)
            del itm
    
    def __initCategoriesList(self, enabledCategories):
        """
        Private method to set the enabled status of the checker categories.
        
        @param enabledCategories comma separated list of enabled checker
            categories
        @type str
        """
        if enabledCategories:
            enabledCategoriesList = [
                c.strip() for c in enabledCategories.split(",")
                if bool(c.strip())]
        else:
            enabledCategoriesList = list(
                CodeStyleCheckerDialog.checkCategories.keys())
        for row in range(self.categoriesList.count()):
            itm = self.categoriesList.item(row)
            if itm.data(Qt.ItemDataRole.UserRole) in enabledCategoriesList:
                itm.setCheckState(Qt.CheckState.Checked)
            else:
                itm.setCheckState(Qt.CheckState.Unchecked)
    
    def __getCategories(self, enabled, asList=False):
        """
        Private method to get the enabled or disabled checker categories.
        
        @param enabled flag indicating to return enabled categories
        @type bool
        @param asList flag indicating to return the checker categories as a
            Python list
        @type bool
        @return checker categories as a list or comma separated string
        @rtype str or list of str
        """
        state = Qt.CheckState.Checked if enabled else Qt.CheckState.Unchecked
        
        checkerList = []
        for row in range(self.categoriesList.count()):
            itm = self.categoriesList.item(row)
            if itm.checkState() == state:
                checkerList.append(itm.data(Qt.ItemDataRole.UserRole))
        if asList:
            return checkerList
        else:
            return ", ".join(checkerList)
    
    def __assembleExcludeMessages(self):
        """
        Private method to assemble the list of excluded checks.
        
        @return list of excluded checks as a comma separated string.
        @rtype str
        """
        excludeMessages = self.excludeMessagesEdit.text()
        disabledCategories = self.__getCategories(False)
        
        if excludeMessages and disabledCategories:
            return disabledCategories + "," + excludeMessages
        elif disabledCategories:
            return disabledCategories
        elif excludeMessages:
            return excludeMessages
        else:
            return ""
    
    def __cleanupData(self):
        """
        Private method to clean the loaded/entered data of redundant entries.
        """
        # Migrate single letter exclude messages to disabled checker categories
        # and delete them from exlude messages
        excludedMessages = [
            m.strip()
            for m in self.excludeMessagesEdit.text().split(",")
            if bool(m)
        ]
        excludedMessageCategories = [
            c for c in excludedMessages if len(c) == 1
        ]
        enabledCheckers = self.__getCategories(True, asList=True)
        for category in excludedMessageCategories:
            if category in enabledCheckers:
                enabledCheckers.remove(category)
            excludedMessages.remove(category)
        
        # Remove excluded messages of an already excluded category
        disabledCheckers = self.__getCategories(False, asList=True)
        for message in excludedMessages[:]:
            if message[0] in disabledCheckers:
                excludedMessages.remove(message)
        
        self.excludeMessagesEdit.setText(",".join(excludedMessages))
        self.__initCategoriesList(",".join(enabledCheckers))
    
    def __initCommentedCodeCheckerWhiteList(self, whitelist):
        """
        Private method to populate the list of commented code whitelist
        patterns.
        
        @param whitelist list of commented code whitelist patterns
        @type list of str
        """
        self.whitelistWidget.clear()
        
        for pattern in whitelist:
            QListWidgetItem(pattern, self.whitelistWidget)
        
        self.on_whitelistWidget_itemSelectionChanged()
    
    def __getCommentedCodeCheckerWhiteList(self):
        """
        Private method to get the list of commented code whitelist patterns.
        
        @return list of commented code whitelist patterns
        @rtype list of str
        """
        whitelist = []
        
        for row in range(self.whitelistWidget.count()):
            whitelist.append(self.whitelistWidget.item(row).text())
        
        return whitelist
    
    @pyqtSlot()
    def on_whitelistWidget_itemSelectionChanged(self):
        """
        Private slot to react upon changes of the selected whitelist patterns.
        """
        self.deleteWhitelistButton.setEnabled(
            len(self.whitelistWidget.selectedItems()) > 0)
    
    @pyqtSlot()
    def on_addWhitelistButton_clicked(self):
        """
        Private slot to add a commented code whitelist pattern.
        """
        pattern, ok = QInputDialog.getText(
            self,
            self.tr("Commented Code Whitelist Pattern"),
            self.tr("Enter a Commented Code Whitelist Pattern"),
            QLineEdit.EchoMode.Normal)
        if ok and pattern:
            QListWidgetItem(pattern, self.whitelistWidget)
    
    @pyqtSlot()
    def on_deleteWhitelistButton_clicked(self):
        """
        Private slot to delete the selected items from the list.
        """
        for itm in self.whitelistWidget.selectedItems():
            row = self.whitelistWidget.row(itm)
            self.whitelistWidget.takeItem(row)
            del itm
