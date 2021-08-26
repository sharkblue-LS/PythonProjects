# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to generate code for a Qt5 dialog.
"""

import sys
import os
import json

from PyQt5.QtCore import (
    pyqtSlot, Qt, QMetaObject, QRegularExpression, QSortFilterProxyModel,
    QProcess, QProcessEnvironment
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QDialog, QDialogButtonBox


from E5Gui.E5Application import e5App
from E5Gui import E5MessageBox

from .Ui_CreateDialogCodeDialog import Ui_CreateDialogCodeDialog
from .NewDialogClassDialog import NewDialogClassDialog

from eric6config import getConfig

import Preferences


pyqtSignatureRole = Qt.ItemDataRole.UserRole + 1
pythonSignatureRole = Qt.ItemDataRole.UserRole + 2
rubySignatureRole = Qt.ItemDataRole.UserRole + 3
returnTypeRole = Qt.ItemDataRole.UserRole + 4
parameterTypesListRole = Qt.ItemDataRole.UserRole + 5
parameterNamesListRole = Qt.ItemDataRole.UserRole + 6


class CreateDialogCodeDialog(QDialog, Ui_CreateDialogCodeDialog):
    """
    Class implementing a dialog to generate code for a Qt5 dialog.
    """
    DialogClasses = {
        "QDialog", "QWidget", "QMainWindow", "QWizard", "QWizardPage",
        "QDockWidget", "QFrame", "QGroupBox", "QScrollArea", "QMdiArea",
        "QTabWidget", "QToolBox", "QStackedWidget"
    }
    Separator = 25 * "="
    
    def __init__(self, formName, project, parent=None):
        """
        Constructor
        
        @param formName name of the file containing the form (string)
        @param project reference to the project object
        @param parent parent widget if the dialog (QWidget)
        """
        super(CreateDialogCodeDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok)
        
        self.slotsView.header().hide()
        
        self.project = project
        
        self.formFile = formName
        filename, ext = os.path.splitext(self.formFile)
        self.srcFile = '{0}{1}'.format(
            filename, self.project.getDefaultSourceExtension())
        
        self.slotsModel = QStandardItemModel()
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.slotsModel)
        self.slotsView.setModel(self.proxyModel)
        
        # initialize some member variables
        self.__initError = False
        self.__module = None
        
        packagesRoot = self.project.getUicParameter("PackagesRoot")
        if packagesRoot:
            self.packagesPath = os.path.join(self.project.getProjectPath(),
                                             packagesRoot)
        else:
            self.packagesPath = self.project.getProjectPath()
        
        if os.path.exists(self.srcFile):
            vm = e5App().getObject("ViewManager")
            ed = vm.getOpenEditor(self.srcFile)
            if ed and not vm.checkDirty(ed):
                self.__initError = True
                return
            
            try:
                splitExt = os.path.splitext(self.srcFile)
                if len(splitExt) == 2:
                    exts = [splitExt[1]]
                else:
                    exts = None
                from Utilities import ModuleParser
                self.__module = ModuleParser.readModule(
                    self.srcFile, extensions=exts, caching=False)
            except ImportError:
                pass
        
        if self.__module is not None:
            self.filenameEdit.setText(self.srcFile)
            
            classesList = []
            vagueClassesList = []
            for cls in list(self.__module.classes.values()):
                if not set(cls.super).isdisjoint(
                        CreateDialogCodeDialog.DialogClasses):
                    classesList.append(cls.name)
                else:
                    vagueClassesList.append(cls.name)
            classesList.sort()
            self.classNameCombo.addItems(classesList)
            if vagueClassesList:
                if classesList:
                    self.classNameCombo.addItem(
                        CreateDialogCodeDialog.Separator)
                self.classNameCombo.addItems(sorted(vagueClassesList))
        
        if (
            os.path.exists(self.srcFile) and
            self.__module is not None and
            self.classNameCombo.count() == 0
        ):
            self.__initError = True
            E5MessageBox.critical(
                self,
                self.tr("Create Dialog Code"),
                self.tr(
                    """The file <b>{0}</b> exists but does not contain"""
                    """ any classes.""").format(self.srcFile))
        
        self.okButton.setEnabled(self.classNameCombo.count() > 0)
        
        self.__updateSlotsModel()
        
    def initError(self):
        """
        Public method to determine, if there was an initialzation error.
        
        @return flag indicating an initialzation error (boolean)
        """
        return self.__initError
    
    def __runUicLoadUi(self, command):
        """
        Private method to run the UicLoadUi.py script with the given command
        and return the output.
        
        @param command uic command to be run
        @type str
        @return tuple of process output and error flag
        @rtype tuple of (str, bool)
        """
        venvManager = e5App().getObject("VirtualEnvManager")
        projectType = self.project.getProjectType()
        
        venvName = self.project.getDebugProperty("VIRTUALENV")
        if not venvName:
            # no project specific environment, try a type specific one
            if projectType in ("PyQt5", "E6Plugin", "PySide2"):
                venvName = Preferences.getQt("PyQtVenvName")
            elif projectType in ("PyQt6", "PySide6"):
                venvName = Preferences.getQt("PyQt6VenvName")
        interpreter = venvManager.getVirtualenvInterpreter(venvName)
        execPath = venvManager.getVirtualenvExecPath(venvName)
        
        if not interpreter:
            interpreter = sys.executable
        
        env = QProcessEnvironment.systemEnvironment()
        if execPath:
            if env.contains("PATH"):
                env.insert(
                    "PATH", os.pathsep.join([execPath, env.value("PATH")])
                )
            else:
                env.insert("PATH", execPath)
        
        if projectType in ("PyQt5", "E6Plugin", "PySide2"):
            loadUi = os.path.join(os.path.dirname(__file__), "UicLoadUi5.py")
        elif projectType in ("PyQt6", "PySide6"):
            loadUi = os.path.join(os.path.dirname(__file__), "UicLoadUi6.py")
        args = [
            loadUi,
            command,
            self.formFile,
            self.packagesPath,
        ]
        
        uicText = ""
        ok = False
        
        proc = QProcess()
        proc.setWorkingDirectory(self.packagesPath)
        proc.setProcessEnvironment(env)
        proc.start(interpreter, args)
        started = proc.waitForStarted(5000)
        finished = proc.waitForFinished(30000)
        if started and finished:
            output = proc.readAllStandardOutput()
            outText = str(output, "utf-8", "replace")
            if proc.exitCode() == 0:
                ok = True
                uicText = outText.strip()
            else:
                E5MessageBox.critical(
                    self,
                    self.tr("uic error"),
                    self.tr(
                        """<p>There was an error loading the form <b>{0}</b>"""
                        """.</p><p>{1}</p>""").format(
                        self.formFile, outText)
                )
        else:
            E5MessageBox.critical(
                self,
                self.tr("uic error"),
                self.tr(
                    """<p>The project specific Python interpreter <b>{0}</b>"""
                    """ could not be started or did not finish within 30"""
                    """ seconds.</p>""").format(interpreter)
            )
        
        return uicText, ok
    
    def __objectName(self):
        """
        Private method to get the object name of a form.
        
        @return object name
        @rtype str
        """
        objectName = ""
        
        output, ok = self.__runUicLoadUi("object_name")
        if ok and output:
            objectName = output
        
        return objectName
    
    def __className(self):
        """
        Private method to get the class name of a form.
        
        @return class name
        @rtype str
        """
        className = ""
        
        output, ok = self.__runUicLoadUi("class_name")
        if ok and output:
            className = output
        
        return className
    
    def __signatures(self):
        """
        Private slot to get the signatures.
        
        @return list of signatures (list of strings)
        """
        if self.__module is None:
            return []
            
        signatures = []
        clsName = self.classNameCombo.currentText()
        if clsName:
            cls = self.__module.classes[clsName]
            for meth in list(cls.methods.values()):
                if meth.name.startswith("on_"):
                    if meth.pyqtSignature is not None:
                        sig = ", ".join(
                            [bytes(QMetaObject.normalizedType(t)).decode()
                             for t in meth.pyqtSignature.split(",")])
                        signatures.append("{0}({1})".format(meth.name, sig))
                    else:
                        signatures.append(meth.name)
        return signatures
        
    def __mapType(self, type_):
        """
        Private method to map a type as reported by Qt's meta object to the
        correct Python type.
        
        @param type_ type as reported by Qt (QByteArray)
        @return mapped Python type (string)
        """
        mapped = bytes(type_).decode()
        
        # I. always check for *
        mapped = mapped.replace("*", "")
        
        # 1. check for const
        mapped = mapped.replace("const ", "")
        
        # 2. replace QString and QStringList
        mapped = (
            mapped
            .replace("QStringList", "list")
            .replace("QString", "str")
        )
        
        # 3. replace double by float
        mapped = mapped.replace("double", "float")
        
        return mapped
    
    def __updateSlotsModel(self):
        """
        Private slot to update the slots tree display.
        """
        self.filterEdit.clear()
        
        output, ok = self.__runUicLoadUi("signatures")
        if ok and output:
            objectsList = json.loads(output.strip())
            
            signatureList = self.__signatures()
            
            self.slotsModel.clear()
            self.slotsModel.setHorizontalHeaderLabels([""])
            for objectDict in objectsList:
                itm = QStandardItem("{0} ({1})".format(
                    objectDict["name"],
                    objectDict["class_name"]))
                self.slotsModel.appendRow(itm)
                for methodDict in objectDict["methods"]:
                    itm2 = QStandardItem(methodDict["signature"])
                    itm.appendRow(itm2)
                    
                    if self.__module is not None:
                        if (
                            methodDict["methods"][0] in signatureList or
                            methodDict["methods"][1] in signatureList
                        ):
                            itm2.setFlags(
                                Qt.ItemFlags(Qt.ItemFlag.ItemIsEnabled))
                            itm2.setCheckState(Qt.CheckState.Checked)
                            if e5App().usesDarkPalette():
                                itm2.setForeground(QBrush(QColor("#75bfff")))
                            else:
                                itm2.setForeground(QBrush(Qt.GlobalColor.blue))
                            continue
            
                    itm2.setData(methodDict["pyqt_signature"],
                                 pyqtSignatureRole)
                    itm2.setData(methodDict["python_signature"],
                                 pythonSignatureRole)
                    itm2.setData(methodDict["return_type"],
                                 returnTypeRole)
                    itm2.setData(methodDict["parameter_types"],
                                 parameterTypesListRole)
                    itm2.setData(methodDict["parameter_names"],
                                 parameterNamesListRole)
                    
                    itm2.setFlags(Qt.ItemFlags(
                        Qt.ItemFlag.ItemIsUserCheckable |
                        Qt.ItemFlag.ItemIsEnabled |
                        Qt.ItemFlag.ItemIsSelectable)
                    )
                    itm2.setCheckState(Qt.CheckState.Unchecked)
            
            self.slotsView.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        
    def __generateCode(self):
        """
        Private slot to generate the code as requested by the user.
        """
        # first decide on extension
        if (
            self.filenameEdit.text().endswith(".py") or
            self.filenameEdit.text().endswith(".pyw")
        ):
            self.__generatePythonCode()
        elif self.filenameEdit.text().endswith(".rb"):
            pass
        # second decide on project language
        elif self.project.getProjectLanguage() == "Python3":
            self.__generatePythonCode()
        elif self.project.getProjectLanguage() == "Ruby":
            pass
        else:
            # assume Python (our global default)
            self.__generatePythonCode()
        
    def __generatePythonCode(self):
        """
        Private slot to generate Python code as requested by the user.
        """
        if self.project.getProjectLanguage() != "Python3":
            E5MessageBox.critical(
                self,
                self.tr("Code Generation"),
                self.tr(
                    """<p>Code generation for project language"""
                    """ "{0}" is not supported.</p>""")
                .format(self.project.getProjectLanguage()))
            return
        
        # init some variables
        sourceImpl = []
        appendAtIndex = -1
        indentStr = "    "
        slotsCode = []
        
        if self.__module is None:
            # new file
            try:
                if self.project.getProjectType() == "PySide2":
                    tmplName = os.path.join(
                        getConfig('ericCodeTemplatesDir'),
                        "impl_pyside2.py.tmpl")
                elif self.project.getProjectType() == "PySide6":
                    tmplName = os.path.join(
                        getConfig('ericCodeTemplatesDir'),
                        "impl_pyside6.py.tmpl")
                elif self.project.getProjectType() in [
                        "PyQt5", "E6Plugin"]:
                    tmplName = os.path.join(
                        getConfig('ericCodeTemplatesDir'),
                        "impl_pyqt5.py.tmpl")
                elif self.project.getProjectType() == "PyQt6":
                    tmplName = os.path.join(
                        getConfig('ericCodeTemplatesDir'),
                        "impl_pyqt6.py.tmpl")
                else:
                    E5MessageBox.critical(
                        self,
                        self.tr("Code Generation"),
                        self.tr(
                            """<p>No code template file available for"""
                            """ project type "{0}".</p>""")
                        .format(self.project.getProjectType()))
                    return
                with open(tmplName, 'r', encoding="utf-8") as tmplFile:
                    template = tmplFile.read()
            except OSError as why:
                E5MessageBox.critical(
                    self,
                    self.tr("Code Generation"),
                    self.tr(
                        """<p>Could not open the code template file"""
                        """ "{0}".</p><p>Reason: {1}</p>""")
                    .format(tmplName, str(why)))
                return
            
            objName = self.__objectName()
            if objName:
                template = (
                    template
                    .replace(
                        "$FORMFILE$",
                        os.path.splitext(os.path.basename(self.formFile))[0])
                    .replace("$FORMCLASS$", objName)
                    .replace("$CLASSNAME$", self.classNameCombo.currentText())
                    .replace("$SUPERCLASS$", self.__className())
                )
                
                sourceImpl = template.splitlines(True)
                appendAtIndex = -1
                
                # determine indent string
                for line in sourceImpl:
                    if line.lstrip().startswith("def __init__"):
                        indentStr = line.replace(line.lstrip(), "")
                        break
        else:
            # extend existing file
            try:
                with open(self.srcFile, 'r', encoding="utf-8") as srcFile:
                    sourceImpl = srcFile.readlines()
                if not sourceImpl[-1].endswith("\n"):
                    sourceImpl[-1] = "{0}{1}".format(sourceImpl[-1], "\n")
            except OSError as why:
                E5MessageBox.critical(
                    self,
                    self.tr("Code Generation"),
                    self.tr(
                        """<p>Could not open the source file "{0}".</p>"""
                        """<p>Reason: {1}</p>""")
                    .format(self.srcFile, str(why)))
                return
            
            cls = self.__module.classes[self.classNameCombo.currentText()]
            if cls.endlineno == len(sourceImpl) or cls.endlineno == -1:
                appendAtIndex = -1
                # delete empty lines at end
                while not sourceImpl[-1].strip():
                    del sourceImpl[-1]
            else:
                appendAtIndex = cls.endlineno - 1
                while not sourceImpl[appendAtIndex].strip():
                    appendAtIndex -= 1
                appendAtIndex += 1
            
            # determine indent string
            for line in sourceImpl[cls.lineno:cls.endlineno + 1]:
                if line.lstrip().startswith("def __init__"):
                    indentStr = line.replace(line.lstrip(), "")
                    break
        
        # do the coding stuff
        if self.project.getProjectType() in ("PySide2", "PySide6"):
            pyqtSignatureFormat = '@Slot({0})'
        else:
            pyqtSignatureFormat = '@pyqtSlot({0})'
        for row in range(self.slotsModel.rowCount()):
            topItem = self.slotsModel.item(row)
            for childRow in range(topItem.rowCount()):
                child = topItem.child(childRow)
                if (
                    child.checkState() and
                    child.flags() & Qt.ItemFlags(
                        Qt.ItemFlag.ItemIsUserCheckable)
                ):
                    slotsCode.append('{0}\n'.format(indentStr))
                    slotsCode.append('{0}{1}\n'.format(
                        indentStr,
                        pyqtSignatureFormat.format(
                            child.data(pyqtSignatureRole))))
                    slotsCode.append('{0}def {1}:\n'.format(
                        indentStr, child.data(pythonSignatureRole)))
                    indentStr2 = indentStr * 2
                    slotsCode.append('{0}"""\n'.format(indentStr2))
                    slotsCode.append(
                        '{0}Slot documentation goes here.\n'.format(
                            indentStr2))
                    if (
                        child.data(returnTypeRole) or
                        child.data(parameterTypesListRole)
                    ):
                        slotsCode.append('{0}\n'.format(indentStr2))
                        if child.data(parameterTypesListRole):
                            for name, type_ in zip(
                                child.data(parameterNamesListRole),
                                    child.data(parameterTypesListRole)):
                                slotsCode.append(
                                    '{0}@param {1} DESCRIPTION\n'.format(
                                        indentStr2, name))
                                slotsCode.append('{0}@type {1}\n'.format(
                                    indentStr2, type_))
                        if child.data(returnTypeRole):
                            slotsCode.append(
                                '{0}@returns DESCRIPTION\n'.format(
                                    indentStr2))
                            slotsCode.append('{0}@rtype {1}\n'.format(
                                indentStr2, child.data(returnTypeRole)))
                    slotsCode.append('{0}"""\n'.format(indentStr2))
                    slotsCode.append('{0}# {1}: not implemented yet\n'.format(
                        indentStr2, "TODO"))
                    slotsCode.append('{0}raise NotImplementedError\n'.format(
                        indentStr2))
        
        if appendAtIndex == -1:
            sourceImpl.extend(slotsCode)
        else:
            sourceImpl[appendAtIndex:appendAtIndex] = slotsCode
        
        # write the new code
        if self.project.useSystemEol():
            newline = None
        else:
            newline = self.project.getEolString()
        fn = self.filenameEdit.text()
        try:
            with open(fn, 'w', encoding="utf-8", newline=newline) as srcFile:
                srcFile.write("".join(sourceImpl))
        except OSError as why:
            E5MessageBox.critical(
                self,
                self.tr("Code Generation"),
                self.tr("""<p>Could not write the source file "{0}".</p>"""
                        """<p>Reason: {1}</p>""")
                .format(fn, str(why)))
            return
        
        self.project.appendFile(fn)
        
    @pyqtSlot(int)
    def on_classNameCombo_activated(self, index):
        """
        Private slot to handle the activated signal of the classname combo.
        
        @param index index of the activated item (integer)
        """
        if (self.classNameCombo.currentText() ==
                CreateDialogCodeDialog.Separator):
            self.okButton.setEnabled(False)
            self.filterEdit.clear()
            self.slotsModel.clear()
            self.slotsModel.setHorizontalHeaderLabels([""])
        else:
            self.okButton.setEnabled(True)
            self.__updateSlotsModel()
        
    def on_filterEdit_textChanged(self, text):
        """
        Private slot called, when thext of the filter edit has changed.
        
        @param text changed text (string)
        """
        rx = QRegularExpression(
            text,
            QRegularExpression.PatternOption.CaseInsensitiveOption)
        self.proxyModel.setFilterRegularExpression(rx)
        
    @pyqtSlot()
    def on_newButton_clicked(self):
        """
        Private slot called to enter the data for a new dialog class.
        """
        path, file = os.path.split(self.srcFile)
        objName = self.__objectName()
        if objName:
            dlg = NewDialogClassDialog(objName, file, path, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                className, fileName = dlg.getData()
                
                self.classNameCombo.clear()
                self.classNameCombo.addItem(className)
                self.srcFile = fileName
                self.filenameEdit.setText(self.srcFile)
                self.__module = None
            
            self.okButton.setEnabled(self.classNameCombo.count() > 0)
        
    def on_buttonBox_clicked(self, button):
        """
        Private slot to handle the buttonBox clicked signal.
        
        @param button reference to the button that was clicked
            (QAbstractButton)
        """
        if button == self.okButton:
            self.__generateCode()
            self.accept()
