# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the closehead extension project helper.
"""

from PyQt5.QtWidgets import QMenu

from E5Gui.E5Action import E5Action

from ..HgExtensionProjectHelper import HgExtensionProjectHelper

import UI.PixmapCache


class CloseheadProjectHelper(HgExtensionProjectHelper):
    """
    Class implementing the closehead extension project helper.
    """
    def __init__(self):
        """
        Constructor
        """
        super(CloseheadProjectHelper, self).__init__()
    
    def initActions(self):
        """
        Public method to generate the action objects.
        """
        self.hgCloseheadAct = E5Action(
            self.tr('Close Heads'),
            UI.PixmapCache.getIcon("closehead"),
            self.tr('Close Heads'),
            0, 0, self, 'mercurial_closehead')
        self.hgCloseheadAct.setStatusTip(self.tr(
            'Close arbitrary heads without checking them out first'
        ))
        self.hgCloseheadAct.setWhatsThis(self.tr(
            """<b>Close Heads</b>"""
            """<p>This closes arbitrary heads without the need to check them"""
            """ out first.</p>"""
        ))
        self.hgCloseheadAct.triggered.connect(self.__hgClosehead)
        self.actions.append(self.hgCloseheadAct)
    
    def initMenu(self, mainMenu):
        """
        Public method to generate the extension menu.
        
        @param mainMenu reference to the main menu
        @type QMenu
        @return populated menu (QMenu)
        """
        menu = QMenu(self.menuTitle(), mainMenu)
        menu.setIcon(UI.PixmapCache.getIcon("closehead"))
        menu.setTearOffEnabled(True)
        
        menu.addAction(self.hgCloseheadAct)
        
        return menu
    
    def menuTitle(self):
        """
        Public method to get the menu title.
        
        @return title of the menu
        @rtype str
        """
        return self.tr("Close Heads")
    
    def __hgClosehead(self):
        """
        Private slot used to close arbitrary heads.
        """
        self.vcs.getExtensionObject("closehead").hgCloseheads()
