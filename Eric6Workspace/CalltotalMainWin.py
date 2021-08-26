import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget,QFileDialog
from PyQt5.QtCore import pyqtSlot
from WinUI.totalMainWin import *
from WinUI.ChildrenForm1 import *

class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.fileCloseAction.triggered.connect(self.close)
        self.fileOpenAction.triggered.connect(self.openMsg)
        self.child = ChildrenForm()
        self.addWinAction.triggered.connect(self.childShow)

    def openMsg(self):
        file,ok=QFileDialog.getOpenFileName(self,"打开","E://PythonProjects/Eric6Workspace","All Files (*);;Text Files(*.txt)")
        self.statusbar.showMessage(file)

    def childShow(self):
        self.MaingridLayout.addWidget(self.child)
        self.child.show()

class ChildrenForm(QWidget,Ui_ChildrenForm1):
    def __init__(self):
        super(ChildrenForm,self).__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec())
