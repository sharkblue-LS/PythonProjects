# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\PythonProjects\Eric6Workspace\WinUI\MainWinSignalSlot.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWinSignalSlot(object):
    def setupUi(self, MainWinSignalSlot):
        MainWinSignalSlot.setObjectName("MainWinSignalSlot")
        MainWinSignalSlot.resize(400, 300)
        self.closeWinBtn = QtWidgets.QPushButton(MainWinSignalSlot)
        self.closeWinBtn.setGeometry(QtCore.QRect(320, 0, 75, 23))
        self.closeWinBtn.setObjectName("closeWinBtn")
        self.label = QtWidgets.QLabel(MainWinSignalSlot)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(80, 140, 54, 12))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(MainWinSignalSlot)
        self.lineEdit.setGeometry(QtCore.QRect(200, 140, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(MainWinSignalSlot)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(130, 80, 71, 16))
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(MainWinSignalSlot)
        self.closeWinBtn.clicked.connect(MainWinSignalSlot.close)
        self.checkBox.clicked['bool'].connect(self.label.setVisible)
        self.checkBox.clicked['bool'].connect(self.lineEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWinSignalSlot)

    def retranslateUi(self, MainWinSignalSlot):
        _translate = QtCore.QCoreApplication.translate
        MainWinSignalSlot.setWindowTitle(_translate("MainWinSignalSlot", "Form"))
        self.closeWinBtn.setText(_translate("MainWinSignalSlot", "关闭窗口"))
        self.label.setText(_translate("MainWinSignalSlot", "显示1"))
        self.lineEdit.setText(_translate("MainWinSignalSlot", "显示2"))
        self.checkBox.setText(_translate("MainWinSignalSlot", "选择"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWinSignalSlot = QtWidgets.QWidget()
    ui = Ui_MainWinSignalSlot()
    ui.setupUi(MainWinSignalSlot)
    MainWinSignalSlot.show()
    sys.exit(app.exec_())