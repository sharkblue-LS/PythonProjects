# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the properties for 'make'.
"""

from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from E5Gui.E5PathPicker import E5PathPickerModes

from .Ui_MakePropertiesDialog import Ui_MakePropertiesDialog


class MakePropertiesDialog(QDialog, Ui_MakePropertiesDialog):
    """
    Class implementing a dialog to enter the properties for 'make'.
    """
    def __init__(self, project, new, parent=None):
        """
        Constructor
        
        @param project reference to the project object
        @type Project
        @param new flag indicating the generation of a new project
        @type bool
        @param parent reference to the parent widget of this dialog
        @type QWidget
        """
        super(MakePropertiesDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.__project = project
        
        self.makePicker.setMode(E5PathPickerModes.OpenFileMode)
        self.makePicker.setFilters(self.tr("All Files (*)"))
        
        self.makefilePicker.setMode(E5PathPickerModes.OpenFileMode)
        self.makefilePicker.setDefaultDirectory(self.__project.ppath)
        self.makefilePicker.setFilters(self.tr(
            "Makefiles (*makefile Makefile *.mak);;All Files (*)"))
        
        self.makeTargetEdit.textChanged.connect(self.__updateOkButton)
        
        self.initDialog()
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def initDialog(self):
        """
        Public method to initialize the dialog's data.
        """
        makeData = self.__project.pdata["MAKEPARAMS"]
        
        if makeData["MakeExecutable"]:
            self.makePicker.setText(makeData["MakeExecutable"])
        else:
            self.makePicker.setText(self.__project.DefaultMake)
        if makeData["MakeFile"]:
            self.makefilePicker.setText(makeData["MakeFile"])
        else:
            self.makefilePicker.setText(self.__project.DefaultMakefile)
        self.makeTargetEdit.setText(makeData["MakeTarget"])
        self.makeParametersEdit.setText(makeData["MakeParameters"])
        self.testOnlyCheckBox.setChecked(makeData["MakeTestOnly"])
        
        self.__updateOkButton()
    
    def __updateOkButton(self):
        """
        Private slot to update the enabled state of the OK button.
        """
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(bool(
                self.makeTargetEdit.text()))
    
    def storeData(self):
        """
        Public method to store the entered/modified data.
        """
        makeData = self.__project.pdata["MAKEPARAMS"]
        
        makeExe = self.makePicker.text()
        if makeExe == self.__project.DefaultMake:
            makeExe = ""
        makeData["MakeExecutable"] = makeExe
        
        makefile = self.__project.getRelativePath(self.makefilePicker.text())
        if makefile == self.__project.DefaultMakefile:
            makefile = ""
        makeData["MakeFile"] = makefile
        
        makeData["MakeTarget"] = self.makeTargetEdit.text()
        makeData["MakeParameters"] = self.makeParametersEdit.text()
        makeData["MakeTestOnly"] = self.testOnlyCheckBox.isChecked()
