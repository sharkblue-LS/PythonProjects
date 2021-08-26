# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a widget to show SSL certificate infos.
"""

from PyQt5.QtCore import pyqtSlot, QCryptographicHash, QDateTime
from PyQt5.QtWidgets import QWidget
try:
    from PyQt5.QtNetwork import QSslCertificate
except ImportError:
    QSslCertificate = None

from .Ui_E5SslCertificatesInfoWidget import Ui_E5SslCertificatesInfoWidget

import Utilities


class E5SslCertificatesInfoWidget(QWidget, Ui_E5SslCertificatesInfoWidget):
    """
    Class implementing a widget to show SSL certificate infos.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super(E5SslCertificatesInfoWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.__chain = []
    
    def showCertificateChain(self, certificateChain):
        """
        Public method to show the SSL certificates of a certificate chain.
        
        @param certificateChain list od SSL certificates
            (list of QSslCertificate)
        """
        if QSslCertificate:
            self.chainLabel.show()
            self.chainComboBox.show()
            self.chainComboBox.clear()
            
            self.__chain = certificateChain[:]
            
            for cert in self.__chain:
                name = ", ".join(cert.subjectInfo(
                    QSslCertificate.SubjectInfo.CommonName))
                if not name:
                    name = ", ".join(
                        cert.subjectInfo(
                            QSslCertificate.SubjectInfo.Organization))
                if not name:
                    name = cert.serialNumber()
                self.chainComboBox.addItem(name)
            
            self.on_chainComboBox_activated(0)
    
    def showCertificate(self, certificate):
        """
        Public method to show the SSL certificate information.
        
        @param certificate reference to the SSL certificate (QSslCertificate)
        """
        self.chainLabel.hide()
        self.chainComboBox.hide()
        self.chainComboBox.clear()
        
        self.__chain = []
        
        if QSslCertificate:
            self.__showCertificate(certificate)
    
    def __showCertificate(self, certificate):
        """
        Private method to show the  SSL certificate information.
        
        @param certificate reference to the SSL certificate (QSslCertificate)
        """
        if QSslCertificate:
            self.blacklistedLabel.setVisible(False)
            self.blacklistedLabel.setStyleSheet(
                "QLabel { color : white; background-color : red; }")
            self.expiredLabel.setVisible(False)
            self.expiredLabel.setStyleSheet(
                "QLabel { color : white; background-color : red; }")
            
            self.subjectCommonNameLabel.setText(self.__certificateString(
                ", ".join(certificate.subjectInfo(
                    QSslCertificate.SubjectInfo.CommonName))))
            self.subjectOrganizationLabel.setText(self.__certificateString(
                ", ".join(certificate.subjectInfo(
                    QSslCertificate.SubjectInfo.Organization))))
            self.subjectOrganizationalUnitLabel.setText(
                self.__certificateString(", ".join(
                    certificate.subjectInfo(
                        QSslCertificate.SubjectInfo.OrganizationalUnitName))))
            self.issuerCommonNameLabel.setText(self.__certificateString(
                ", ".join(certificate.issuerInfo(
                    QSslCertificate.SubjectInfo.CommonName))))
            self.issuerOrganizationLabel.setText(self.__certificateString(
                ", ".join(certificate.issuerInfo(
                    QSslCertificate.SubjectInfo.Organization))))
            self.issuerOrganizationalUnitLabel.setText(
                self.__certificateString(", ".join(
                    certificate.issuerInfo(
                        QSslCertificate.SubjectInfo.OrganizationalUnitName))))
            self.serialNumberLabel.setText(self.__serialNumber(certificate))
            self.effectiveLabel.setText(
                certificate.effectiveDate().toString("yyyy-MM-dd"))
            self.expiresLabel.setText(
                certificate.expiryDate().toString("yyyy-MM-dd"))
            self.sha1Label.setText(self.__formatHexString(
                str(certificate.digest(
                    QCryptographicHash.Algorithm.Sha1).toHex(),
                    encoding="ascii")))
            self.md5Label.setText(self.__formatHexString(
                str(certificate.digest(
                    QCryptographicHash.Algorithm.Md5).toHex(),
                    encoding="ascii")))
            
            if certificate.isBlacklisted():
                # something is wrong; indicate it to the user
                if self.__hasExpired(certificate.effectiveDate(),
                                     certificate.expiryDate()):
                    self.expiredLabel.setVisible(True)
                else:
                    self.blacklistedLabel.setVisible(True)
    
    def __certificateString(self, txt):
        """
        Private method to prepare some text for display.
        
        @param txt text to be displayed (string)
        @return prepared text (string)
        """
        if txt is None or txt == "":
            return self.tr("<not part of the certificate>")
        
        return Utilities.decodeString(txt)
    
    def __serialNumber(self, cert):
        """
        Private slot to format the certificate serial number.
        
        @param cert reference to the SSL certificate (QSslCertificate)
        @return formated serial number (string)
        """
        serial = cert.serialNumber()
        if serial == "":
            return self.tr("<not part of the certificate>")
        
        if b':' in serial:
            return str(serial, encoding="ascii").upper()
        else:
            hexString = hex(int(serial))[2:]
            return self.__formatHexString(hexString)
    
    def __formatHexString(self, hexString):
        """
        Private method to format a hex string for display.
        
        @param hexString hex string to be formatted (string)
        @return formatted string (string)
        """
        hexString = hexString.upper()
        
        if len(hexString) % 2 == 1:
            hexString = '0' + hexString
        
        hexList = []
        while hexString:
            hexList.append(hexString[:2])
            hexString = hexString[2:]
        
        return ':'.join(hexList)
    
    def __hasExpired(self, effectiveDate, expiryDate):
        """
        Private method to check for a certificate expiration.
        
        @param effectiveDate date the certificate becomes effective (QDateTime)
        @param expiryDate date the certificate expires (QDateTime)
        @return flag indicating the expiration status (boolean)
        """
        now = QDateTime.currentDateTime()
        
        return now < effectiveDate or now >= expiryDate
    
    @pyqtSlot(int)
    def on_chainComboBox_activated(self, index):
        """
        Private slot to show the certificate info for the selected entry.
        
        @param index number of the certificate in the certificate chain
            (integer)
        """
        self.__showCertificate(self.__chain[index])
