# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2021 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a QSerialPort with additional functionality for
MicroPython devices.
"""

from PyQt5.QtCore import QIODevice, QTime, QCoreApplication, QEventLoop
from PyQt5.QtSerialPort import QSerialPort


class MicroPythonSerialPort(QSerialPort):
    """
    Class implementing a QSerialPort with additional functionality for
    MicroPython devices.
    """
    def __init__(self, timeout=10000, parent=None):
        """
        Constructor
        
        @param timeout timout in milliseconds to be set
        @type int
        @param parent reference to the parent object
        @type QObject
        """
        super(MicroPythonSerialPort, self).__init__(parent)
        
        self.__connected = False
        self.__timeout = timeout      # 10s default timeout
        self.__timedOut = False
    
    def setTimeout(self, timeout):
        """
        Public method to set the timeout for device operations.
        
        @param timeout timout in milliseconds to be set
        @type int
        """
        self.__timeout = timeout
    
    def openSerialLink(self, port):
        """
        Public method to open a serial link to a given serial port.
        
        @param port port name to connect to
        @type str
        @return flag indicating success
        @rtype bool
        """
        self.setPortName(port)
        if self.open(QIODevice.OpenModeFlag.ReadWrite):
            self.setDataTerminalReady(True)
            # 115.200 baud, 8N1
            self.setBaudRate(115200)
            self.setDataBits(QSerialPort.DataBits.Data8)
            self.setParity(QSerialPort.Parity.NoParity)
            self.setStopBits(QSerialPort.StopBits.OneStop)
            
            self.__connected = True
            return True
        else:
            return False
    
    def closeSerialLink(self):
        """
        Public method to close the open serial connection.
        """
        if self.__connected:
            self.close()
            
            self.__connected = False
    
    def isConnected(self):
        """
        Public method to get the connection state.
        
        @return flag indicating the connection state
        @rtype bool
        """
        return self.__connected
    
    def hasTimedOut(self):
        """
        Public method to check, if the last 'readUntil' has timed out.
        
        @return flag indicating a timeout
        @@rtype bool
        """
        return self.__timedOut
    
    def readUntil(self, expected=b"\n", size=None):
        r"""
        Public method to read data until an expected sequence is found
        (default: \n) or a specific size is exceeded.
        
        @param expected expected bytes sequence
        @type bytes
        @param size maximum data to be read
        @type int
        @return bytes read from the device including the expected sequence
        @rtype bytes
        """
        data = bytearray()
        self.__timedOut = False
        
        t = QTime()
        t.start()
        while True:
            QCoreApplication.processEvents(
                QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
            c = bytes(self.read(1))
            if c:
                data += c
                if data.endswith(expected):
                    break
                if size is not None and len(data) >= size:
                    break
            if t.elapsed() > self.__timeout:
                self.__timedOut = True
                break
        
        return bytes(data)
