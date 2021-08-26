# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the QFileDialog wizard plugin.
"""

import re

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog

from E5Gui.E5Application import e5App
from E5Gui.E5Action import E5Action
from E5Gui import E5MessageBox

import UI.Info

# Start-Of-Header
name = "QFileDialog Wizard Plugin"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = UI.Info.VersionOnly
className = "FileDialogWizard"
packageName = "__core__"
shortDescription = "Show the QFileDialog wizard."
longDescription = """This plugin shows the QFileDialog wizard."""
pyqtApi = 2
# End-Of-Header

error = ""


class FileDialogWizard(QObject):
    """
    Class implementing the QFileDialog wizard plugin.
    """
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object (UI.UserInterface)
        """
        super(FileDialogWizard, self).__init__(ui)
        self.__ui = ui
        
        # PyQt5
        self.__pyqtRe = re.compile(r"(?:import|from)\s+PyQt([56])")

    def activate(self):
        """
        Public method to activate this plugin.
        
        @return tuple of None and activation status (boolean)
        """
        self.__initActions()
        self.__initMenu()
        
        return None, True

    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        menu = self.__ui.getMenu("wizards")
        if menu:
            menu.removeAction(self.qFileDialogAction)
            menu.removeAction(self.e5FileDialogAction)
        self.__ui.removeE5Actions(
            [self.qFileDialogAction, self.e5FileDialogAction],
            'wizards')
    
    def __initActions(self):
        """
        Private method to initialize the actions.
        """
        self.qFileDialogAction = E5Action(
            self.tr('QFileDialog Wizard'),
            self.tr('Q&FileDialog Wizard...'), 0, 0, self,
            'wizards_qfiledialog')
        self.qFileDialogAction.setStatusTip(self.tr('QFileDialog Wizard'))
        self.qFileDialogAction.setWhatsThis(self.tr(
            """<b>QFileDialog Wizard</b>"""
            """<p>This wizard opens a dialog for entering all the parameters"""
            """ needed to create a QFileDialog. The generated code is"""
            """ inserted at the current cursor position.</p>"""
        ))
        self.qFileDialogAction.triggered.connect(self.__handleQFileDialog)
        
        self.e5FileDialogAction = E5Action(
            self.tr('E5FileDialog Wizard'),
            self.tr('E&5FileDialog Wizard...'), 0, 0, self,
            'wizards_e5filedialog')
        self.e5FileDialogAction.setStatusTip(self.tr('E5FileDialog Wizard'))
        self.e5FileDialogAction.setWhatsThis(self.tr(
            """<b>E5FileDialog Wizard</b>"""
            """<p>This wizard opens a dialog for entering all the parameters"""
            """ needed to create an E5FileDialog. The generated code is"""
            """ inserted at the current cursor position.</p>"""
        ))
        self.e5FileDialogAction.triggered.connect(self.__handleE5FileDialog)
        
        self.__ui.addE5Actions(
            [self.qFileDialogAction, self.e5FileDialogAction],
            'wizards')

    def __initMenu(self):
        """
        Private method to add the actions to the right menu.
        """
        menu = self.__ui.getMenu("wizards")
        if menu:
            menu.addAction(self.e5FileDialogAction)
            menu.addAction(self.qFileDialogAction)
    
    def __callForm(self, editor, variant):
        """
        Private method to display a dialog and get the code.
        
        @param editor reference to the current editor
        @type Editor
        @param variant variant of code to be generated
            (-1 = E5FileDialog, 0 = unknown, 5 = PyQt5)
        @type int
        @return the generated code (string)
        """
        from WizardPlugins.FileDialogWizard.FileDialogWizardDialog import (
            FileDialogWizardDialog
        )
        dlg = FileDialogWizardDialog(variant, None)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            line, index = editor.getCursorPosition()
            indLevel = editor.indentation(line) // editor.indentationWidth()
            if editor.indentationsUseTabs():
                indString = '\t'
            else:
                indString = editor.indentationWidth() * ' '
            return (dlg.getCode(indLevel, indString), 1)
        else:
            return (None, 0)
        
    def __handle(self, variant):
        """
        Private method to handle the wizards action.
        
        @param variant dialog variant to be generated
            (E5FileDialog or QFileDialog)
        @type str
        @exception ValueError raised to indicate an illegal file dialog variant
        """
        editor = e5App().getObject("ViewManager").activeWindow()
        
        if editor is None:
            E5MessageBox.critical(
                self.__ui,
                self.tr('No current editor'),
                self.tr('Please open or create a file first.'))
        else:
            if variant == "QFileDialog":
                match = self.__pyqtRe.search(editor.text())
                if match is None:
                    # unknown
                    dialogVariant = 0
                else:
                    # PyQt5/PyQt6
                    dialogVariant = int(match.group(1))
            elif variant == "E5FileDialog":
                # E5FileDialog
                dialogVariant = -1
            else:
                raise ValueError("Illegal dialog variant given")
            
            code, ok = self.__callForm(editor, dialogVariant)
            if ok:
                line, index = editor.getCursorPosition()
                # It should be done on this way to allow undo
                editor.beginUndoAction()
                editor.insertAt(code, line, index)
                editor.endUndoAction()
    
    def __handleQFileDialog(self):
        """
        Private slot to handle the wizard QFileDialog action.
        """
        self.__handle("QFileDialog")
    
    def __handleE5FileDialog(self):
        """
        Private slot to handle the wizard E5FileDialog action.
        """
        self.__handle("E5FileDialog")
