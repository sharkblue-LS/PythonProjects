# -*- coding: utf-8 -*-

# Copyright (c) 2013 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the setup.py wizard plug-in.
"""

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog

from E5Gui.E5Application import e5App
from E5Gui.E5Action import E5Action
from E5Gui import E5MessageBox

import UI.Info

# Start-of-Header
name = "setup.py Wizard Plug-in"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = UI.Info.VersionOnly
className = "SetupWizard"
packageName = "__core__"
shortDescription = "Wizard for the creation of a setup.py file."
longDescription = (
    """This plug-in implements a wizard to generate code for"""
    """ a setup.py file. It supports the 'distutils' and 'setuptools'"""
    """ variants."""
)
needsRestart = False
pyqtApi = 2
# End-of-Header

error = ""


class SetupWizard(QObject):
    """
    Class implementing the setup.py wizard plug-in.
    """
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object (UI.UserInterface)
        """
        super(SetupWizard, self).__init__(ui)
        self.__ui = ui
        self.__action = None
    
    def __initialize(self):
        """
        Private slot to (re)initialize the plug-in.
        """
        self.__act = None
    
    def activate(self):
        """
        Public method to activate this plug-in.
        
        @return tuple of None and activation status (boolean)
        """
        self.__initAction()
        self.__initMenu()
        
        return None, True
    
    def deactivate(self):
        """
        Public method to deactivate this plug-in.
        """
        menu = self.__ui.getMenu("wizards")
        if menu:
            menu.removeAction(self.__action)
        self.__ui.removeE5Actions([self.__action], 'wizards')
    
    def __initAction(self):
        """
        Private method to initialize the action.
        """
        self.__action = E5Action(
            self.tr('setup.py Wizard'),
            self.tr('&setup.py Wizard...'),
            0, 0, self,
            'wizards_setup_py')
        self.__action.setStatusTip(self.tr('setup.py Wizard'))
        self.__action.setWhatsThis(self.tr(
            """<b>setup.py Wizard</b>"""
            """<p>This wizard opens a dialog for entering all the parameters"""
            """ needed to create the basic contents of a setup.py file. The"""
            """ generated code is inserted at the current cursor position."""
            """</p>"""
        ))
        self.__action.triggered.connect(self.__handle)
        
        self.__ui.addE5Actions([self.__action], 'wizards')

    def __initMenu(self):
        """
        Private method to add the actions to the right menu.
        """
        menu = self.__ui.getMenu("wizards")
        if menu:
            menu.addAction(self.__action)
    
    def __callForm(self, editor):
        """
        Private method to display a dialog and get the code.
        
        @param editor reference to the current editor
        @return the generated code (string)
        """
        from WizardPlugins.SetupWizard.SetupWizardDialog import (
            SetupWizardDialog
        )
        dlg = SetupWizardDialog(None)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            line, index = editor.getCursorPosition()
            indLevel = editor.indentation(line) // editor.indentationWidth()
            if editor.indentationsUseTabs():
                indString = '\t'
            else:
                indString = editor.indentationWidth() * ' '
            return (dlg.getCode(indLevel, indString), True)
        else:
            return (None, False)
        
    def __handle(self):
        """
        Private method to handle the wizards action.
        """
        editor = e5App().getObject("ViewManager").activeWindow()
        
        if editor is None:
            E5MessageBox.critical(
                self.__ui,
                self.tr('No current editor'),
                self.tr('Please open or create a file first.'))
        else:
            code, ok = self.__callForm(editor)
            if ok:
                line, index = editor.getCursorPosition()
                # It should be done on this way to allow undo
                editor.beginUndoAction()
                editor.insertAt(code, line, index)
                editor.endUndoAction()

#
# eflag: noqa = M801
