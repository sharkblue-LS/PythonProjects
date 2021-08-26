# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select a SSL certificate.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTreeWidgetItem
try:
    from PyQt5.QtNetwork import QSslCertificate
except ImportError:
    pass

from .Ui_E5SslCertificateSelectionDialog import (
    Ui_E5SslCertificateSelectionDialog
)

import Utilities
import UI.PixmapCache


class E5SslCertificateSelectionDialog(QDialog,
                                      Ui_E5SslCertificateSelectionDialog):
    """
    Class implementing a dialog to select a SSL certificate.
    """
    CertRole = Qt.ItemDataRole.UserRole + 1
    
    def __init__(self, certificates, parent=None):
        """
        Constructor
        
        @param certificates list of SSL certificates to select from
        @type list of QSslCertificate
        @param parent reference to the parent widget
        @type QWidget
        """
        super(E5SslCertificateSelectionDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.viewButton.setIcon(
            UI.PixmapCache.getIcon("certificates"))
        
        self.buttonBox.button(QDialogButtonBox.OK).setEnabled(False)
        self.viewButton.setEnabled(False)
        
        self.__populateCertificatesTree(certificates)
    
    def __populateCertificatesTree(self, certificates):
        """
        Private slot to populate the certificates tree.
        
        @param certificates list of SSL certificates to select from
        @type list of QSslCertificate
        """
        for cert in certificates():
            self.__createCertificateEntry(cert)
        
        self.certificatesTree.expandAll()
        for i in range(self.certificatesTree.columnCount()):
            self.certificatesTree.resizeColumnToContents(i)
        self.certificatesTree.sortItems(0, Qt.SortOrder.AscendingOrder)
    
    def __createCaCertificateEntry(self, cert):
        """
        Private method to create a certificate entry.
        
        @param cert certificate to insert
        @type QSslCertificate
        """
        # step 1: extract the info to be shown
        organisation = Utilities.decodeString(
            ", ".join(cert.subjectInfo(
                QSslCertificate.SubjectInfo.Organization)))
        commonName = Utilities.decodeString(
            ", ".join(cert.subjectInfo(
                QSslCertificate.SubjectInfo.CommonName)))
        if organisation is None or organisation == "":
            organisation = self.tr("(Unknown)")
        if commonName is None or commonName == "":
            commonName = self.tr("(Unknown common name)")
        expiryDate = cert.expiryDate().toString("yyyy-MM-dd")
        
        # step 2: create the entry
        items = self.certificatesTree.findItems(
            organisation,
            Qt.MatchFlag.MatchFixedString | Qt.MatchFlag.MatchCaseSensitive)
        if len(items) == 0:
            parent = QTreeWidgetItem(self.certificatesTree, [organisation])
            parent.setFirstColumnSpanned(True)
        else:
            parent = items[0]
        
        itm = QTreeWidgetItem(parent, [commonName, expiryDate])
        itm.setData(0, self.CertRole, cert.toPem())
    
    @pyqtSlot()
    def on_certificatesTree_itemSelectionChanged(self):
        """
        Private slot to handle the selection of an item.
        """
        enable = (
            len(self.certificatesTree.selectedItems()) > 0 and
            self.certificatesTree.selectedItems()[0].parent() is not None
        )
        self.buttonBox.button(QDialogButtonBox.OK).setEnabled(enable)
        self.viewButton.setEnabled(enable)
    
    @pyqtSlot()
    def on_viewButton_clicked(self):
        """
        Private slot to show data of the selected certificate.
        """
        try:
            from E5Network.E5SslCertificatesInfoDialog import (
                E5SslCertificatesInfoDialog
            )
            cert = QSslCertificate.fromData(
                self.certificatesTree.selectedItems()[0].data(
                    0, self.CertRole))
            dlg = E5SslCertificatesInfoDialog(cert, self)
            dlg.exec()
        except ImportError:
            pass
    
    def getSelectedCertificate(self):
        """
        Public method to get the selected certificate.
        
        @return selected certificate
        @rtype QSslCertificate
        """
        valid = (
            len(self.certificatesTree.selectedItems()) > 0 and
            self.certificatesTree.selectedItems()[0].parent() is not None
        )
        
        if valid:
            certificate = QSslCertificate.fromData(
                self.certificatesTree.selectedItems()[0].data(
                    0, self.CertRole))
        else:
            certificate = None
        
        return certificate
