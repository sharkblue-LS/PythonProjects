# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a wizard dialog to enter the synchronization data.
"""

from PyQt5.QtWidgets import QWizard

import UI.PixmapCache
import Globals


class SyncAssistantDialog(QWizard):
    """
    Class implementing a wizard dialog to enter the synchronization data.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(SyncAssistantDialog, self).__init__(parent)
        
        from . import SyncGlobals

        from .SyncDataPage import SyncDataPage
        from .SyncEncryptionPage import SyncEncryptionPage
        from .SyncHostTypePage import SyncHostTypePage
        from .SyncFtpSettingsPage import SyncFtpSettingsPage
        from .SyncDirectorySettingsPage import SyncDirectorySettingsPage
        from .SyncCheckPage import SyncCheckPage

        self.setPage(SyncGlobals.PageData, SyncDataPage(self))
        self.setPage(SyncGlobals.PageEncryption, SyncEncryptionPage(self))
        self.setPage(SyncGlobals.PageType, SyncHostTypePage(self))
        self.setPage(SyncGlobals.PageFTPSettings, SyncFtpSettingsPage(self))
        self.setPage(SyncGlobals.PageDirectorySettings,
                     SyncDirectorySettingsPage(self))
        self.setPage(SyncGlobals.PageCheck, SyncCheckPage(self))
        
        self.setPixmap(QWizard.WizardPixmap.LogoPixmap,
                       UI.PixmapCache.getPixmap("ericWeb48"))
        self.setPixmap(QWizard.WizardPixmap.WatermarkPixmap,
                       UI.PixmapCache.getPixmap("eric256"))
        self.setPixmap(QWizard.WizardPixmap.BackgroundPixmap,
                       UI.PixmapCache.getPixmap("eric256"))
        
        self.setMinimumSize(650, 450)
        if Globals.isWindowsPlatform():
            self.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        
        self.setOption(QWizard.WizardOption.NoCancelButtonOnLastPage, True)
