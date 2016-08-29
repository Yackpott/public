from PyQt4 import QtGui
from juego import Juego

# parte del codigo fue sacado de la ayudantia 8


class Inicial(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.resize(640, 640)
        self.setWindowTitle("#ZombieTroll")
        self.ventana()
        self.show()

    def ventana(self):
        self.boton_inicial = QtGui.QPushButton('&Iniciar', self)
        self.boton_inicial.resize(self.boton_inicial.sizeHint())
        self.boton_inicial.move(280, 400)
        self.boton_inicial.clicked.connect(self.iniciar)
        self.label_inicial = QtGui.QLabel("", self)
        self.label_inicial.move(170, 140)
        self.pixmap_inicial = QtGui.QPixmap("img/inicial_zombie.jpeg")
        self.label_inicial.setPixmap(self.pixmap_inicial)
        self.label_puntaje = QtGui.QLabel("", self)
        self.label_puntaje.resize(self.label_puntaje.sizeHint())
        self.label_puntaje.move(275, 150)

    def iniciar(self):
        juego = Juego(self)
        juego.show()
        self.setVisible(False)

    def volver(self, puntaje):
        self.label_puntaje.setText("Puntaje: {}".format(puntaje))
        self.label_puntaje.resize(self.label_puntaje.sizeHint())
        self.setVisible(True)

    def cerrar(self):
        self.close()

    def closeEvent(self, QCloseEvent):
        QCloseEvent.accept()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    inicial = Inicial()
    inicial.show()
    app.exec_()
