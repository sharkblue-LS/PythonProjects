# -*- coding: utf-8 -*-

# Copyright (c) 2011 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the guards of a selected patch.
"""

from PyQt5.QtCore import pyqtSlot, Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog, QListWidgetItem

from .Ui_HgQueuesListGuardsDialog import Ui_HgQueuesListGuardsDialog

import UI.PixmapCache


class HgQueuesListGuardsDialog(QDialog, Ui_HgQueuesListGuardsDialog):
    """
    Class implementing a dialog to show the guards of a selected patch.
    """
    def __init__(self, vcs, patchesList, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param patchesList list of patches (list of strings)
        @param parent reference to the parent widget (QWidget)
        """
        super(HgQueuesListGuardsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.vcs = vcs
        self.__hgClient = vcs.getClient()
        
        self.patchSelector.addItems([""] + patchesList)
        
        self.show()
        QCoreApplication.processEvents()
    
    def closeEvent(self, e):
        """
        Protected slot implementing a close event handler.
        
        @param e close event (QCloseEvent)
        """
        if self.__hgClient.isExecuting():
            self.__hgClient.cancel()
        
        e.accept()
    
    def start(self):
        """
        Public slot to start the list command.
        """
        self.on_patchSelector_activated(0)
    
    @pyqtSlot(int)
    def on_patchSelector_activated(self, index):
        """
        Private slot to get the list of guards for the given patch name.
        
        @param index index of the selected entry
        @type int
        """
        patch = self.patchSelector.itemText(index)
        self.guardsList.clear()
        self.patchNameLabel.setText("")
        
        args = self.vcs.initCommand("qguard")
        if patch:
            args.append(patch)
        
        output = self.__hgClient.runcommand(args)[0].strip()
        
        if output:
            patchName, guards = output.split(":", 1)
            self.patchNameLabel.setText(patchName)
            guardsList = guards.strip().split()
            for guard in guardsList:
                if guard.startswith("+"):
                    icon = UI.PixmapCache.getIcon("plus")
                    guard = guard[1:]
                elif guard.startswith("-"):
                    icon = UI.PixmapCache.getIcon("minus")
                    guard = guard[1:]
                else:
                    icon = None
                    guard = self.tr("Unguarded")
                itm = QListWidgetItem(guard, self.guardsList)
                if icon:
                    itm.setIcon(icon)
