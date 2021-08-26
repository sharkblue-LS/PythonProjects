import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from WinUI.Ui_firstMainWin import *
from PyQt5.QtCore import pyqtSlot


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        print("收益_min：",self.doubleSpinBox_returns_min.text())
        print("收益_max：",self.doubleSpinBox_returns_max.text())
        print("最大回撤_min：",self.doubleSpinBox_maxdrawdown_min.text())
        print("最大回撤_max：",self.doubleSpinBox_maxdrawdown_max.text())
        print("sharp比_min：",self.doubleSpinBox_sharp_min.text())
        print("sharp比_max：", self.doubleSpinBox_sharp_max.text())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec())
