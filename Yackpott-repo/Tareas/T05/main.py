from PyQt4 import QtGui
from inicial import Inicial

# enlazar dos widgets

if __name__ == '__main__':
    app = QtGui.QApplication([])
    inicial = Inicial()
    inicial.show()
    app.exec_()
