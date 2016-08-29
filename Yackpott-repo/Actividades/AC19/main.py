import sys
from PyQt4 import QtGui
from backend import Partida


class Buscaminas(QtGui.QWidget):

    def __init__(self, n, minas):  # con "n" se genera una matriz de nxn
        super(Buscaminas, self).__init__()
        self.n = n
        self.minas = minas
        self.partida = Partida(n, minas)
        ":::COMPLETAR:::"
        self.dicc = dict()
        self.apretados = 0
        self.initUI()
        self.seguir = True

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        for i in range(self.n):
            for j in range(self.n):
                button = QtGui.QPushButton(' ')
                self.dicc[button] = (i, j)
                button.setFixedSize(50, 50)
                grid.addWidget(button, i, j)
                button.clicked.connect(self.buttonClickedLeft)

        self.label = QtGui.QLabel("Comenzo el juego")
        grid.addWidget(self.label, self.n+1, 0, 1, self.n+1)
        self.setWindowTitle('Buscaminas')
        self.show()

    def buttonClickedLeft(self):
        sender = self.sender()
        if self.seguir:
            if sender.text() == ' ':
                tupla = self.dicc[sender]
                numero = self.apretar_boton(tupla)
                sender.setText(numero)
                if numero == "X":
                    self.notificar("Moriste")
                    self.seguir = False
                else:
                    self.apretados += 1
                    if self.n**2 - self.apretados == self.minas:
                        self.notificar("Ganaste")
                        self.seguir = False
                    else:
                        self.notificar("Sigues vivo aun")

    def apretar_boton(self, posicion):  # Posición como una tupla (x, y)
        "Esta funcion devuelve la cantidad de minas alrededor de un espacio"
        "No tiene ninguna relación con lo que sucederá en la UI"
        boton = self.partida.botones[posicion]
        return self.partida.clickear(boton)

    def notificar(self, mensaje):
        ":::COMPLETAR:::"
        "Debe notificar a traves de un label cuando muera o sobreviva"
        self.label.setText(mensaje)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Buscaminas(5, 10)
    sys.exit(app.exec_())
