import sys
from PyQt5 import QtWidgets,QtCore

# app = QtWidgets.QApplication(sys.argv)
# widget = QtWidgets.QWidget()
# widget.resize(1024,768)
# widget.setWindowTitle("hello,pyqt5")
# widget.show()
# sys.exit(app.exec())
# print(dir(QtWidgets))

import numpy as np
import timeit
np.random.seed(0)
values = np.random.randint(1,100,size=1000000)
timeit.timeit(result = 1.0/values)
