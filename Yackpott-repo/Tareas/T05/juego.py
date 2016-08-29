from PyQt4 import QtGui
from PyQt4 import QtCore
from objetos import Jugador, Zombie, Cerveza, Pistola, Bala
import random
import math

# parte del codigo fue sacado de la ayudantia 8 ;)


class Juego(QtGui.QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.setWindowTitle("#ZombieTroll")
        self.dim = (640, 640)
        self.pausado = False
        self.boton = QtGui.QPushButton('&Pausa', self)
        self.boton.resize(self.boton.sizeHint())
        self.boton.move(0, 0)
        self.boton.clicked.connect(self.pausa)
        self.puntaje = 0
        self.label_puntaje = QtGui.QLabel(
            "Puntaje: {}".format(self.puntaje), self)
        self.label_puntaje.setVisible(True)
        self.label_puntaje.move(10, 60)
        self.lambd = 5000
        self.balas = []
        self.zombies = []
        self.objetos = []
        self.resize(self.dim[0], self.dim[1])
        self.jugador = Jugador(self)
        self.jugador.position = (320, 320)
        self.jugador.start()
        self.crear_zombie()
        self.mover_zombies()
        self.helicoptero()
        self.mostrar_puntaje()
        self.show()

    def pausa(self):
        self.pausado = True
        self.boton.setText('&Play')
        self.boton.resize(self.boton.sizeHint())
        self.boton.clicked.connect(self.play)

    def play(self):
        self.pausado = False
        self.boton.setText('&Pausa')
        self.boton.resize(self.boton.sizeHint())
        self.boton.clicked.connect(self.pausa)

    def mostrar_puntaje(self):
        if not self.pausado:
            self.puntaje += 1
            self.label_puntaje.setText("Puntaje: {}".format(self.puntaje))
            self.label_puntaje.resize(self.label_puntaje.sizeHint())
        QtCore.QTimer.singleShot(1000, self.mostrar_puntaje)

    def crear_zombie(self):
        if not self.pausado:

            rand_1 = random.randint(1, 4)

            if rand_1 == 1:
                x = Zombie.dim[0] / 2 + 65
                y = random.randint(
                    Zombie.dim[1] / 2 + 65, self.dim[1] - Zombie.dim[1] / 2)
            elif rand_1 == 2:
                x = self.dim[0] - Zombie.dim[0] / 2
                y = random.randint(
                    Zombie.dim[1] / 2 + 65, self.dim[1] - Zombie.dim[1] / 2)
            elif rand_1 == 3:
                x = random.randint(
                    Zombie.dim[0] / 2 + 65, self.dim[0] - Zombie.dim[0] / 2)
                y = Zombie.dim[1] / 2 + 65
            elif rand_1 == 4:
                x = random.randint(
                    Zombie.dim[0] / 2 + 65, self.dim[0] - Zombie.dim[0] / 2)
                y = self.dim[1] - Zombie.dim[1] / 2

            d_1 = abs(x - self.jugador.position[0])
            d_2 = abs(y - self.jugador.position[1])
            if self.choque(x, y) and (d_1 < 50 or d_2 < 50):
                self.crear_zombie()
                return
            zombie = Zombie(self, self.jugador)
            self.zombies.append(zombie)
            zombie.position = (x, y)
            self.direccionar_zombie(zombie)
            zombie.start()
            self.lambd = self.lambd * 0.75 + 500
        if self.jugador.vivo:
            QtCore.QTimer.singleShot(self.lambd, self.crear_zombie)

    def choque(self, pos_x, pos_y, obj=None):
        for otro in self.zombies:
            d_1 = abs(pos_x - otro.position[0])
            d_2 = abs(pos_y - otro.position[1])
            if otro != obj and d_1 < 25 and d_2 < 25:
                return True
        else:
            return False

    def mover_zombies(self):
        if not self.pausado:
            for zombie in self.zombies:
                if not zombie.atacando:
                    jugador_x = self.jugador.position[0]
                    jugador_y = self.jugador.position[1]
                    r = 10
                    y_2 = jugador_y
                    y_1 = zombie.position[1]
                    x_2 = jugador_x
                    x_1 = zombie.position[0]
                    mov_x, mov_y = self.calcular_movimiento(
                        r, y_2, y_1, x_2, x_1)
                    f_x = zombie.position[0] + mov_x
                    f_y = zombie.position[1] + mov_y
                    d_1 = abs(f_x - self.jugador.position[0])
                    d_2 = abs(f_y - self.jugador.position[1])
                    if not self.choque(f_x, f_y, zombie) and d_1 > 20 and d_2 > 20:
                        zombie.agregar_movimiento(mov_x, mov_y)
        if self.jugador.vivo:
            QtCore.QTimer.singleShot(500, self.mover_zombies)

    def helicoptero(self):
        if not self.pausado:
            rand = random.randint(1, 2)
            if rand == 1:
                obj = Cerveza(self)
            elif rand == 2:
                obj = Pistola(self)
            self.objetos.append(obj)
            x = random.randint(obj.dim[0] / 2, self.dim[0] - obj.dim[0] / 2)
            y = random.randint(obj.dim[1] / 2, self.dim[1] - obj.dim[1] / 2)
            obj.position = (x, y)
        if self.jugador.vivo:
            QtCore.QTimer.singleShot(30000, self.helicoptero)

    def diff(self, y_2, y_1, x_2, x_1):
        x = x_2 - x_1
        y = -1 * (y_2 - y_1)
        return x, y

    def theta(self, y_2, y_1, x_2, x_1):
        x, y = self.diff(y_2, y_1, x_2, x_1)
        rad = math.atan2(y, x)
        theta = math.degrees(rad)
        if theta < 0:
            theta += 360
        theta = -1 * theta
        theta -= 90
        return theta

    def direccion_jugador(self):

        y_2 = self.mouse_y
        y_1 = self.jugador.position[1]
        x_2 = self.mouse_x
        x_1 = self.jugador.position[0]

        theta = self.theta(y_2, y_1, x_2, x_1)

        pixmap_i = QtGui.QPixmap("img/jugador/i.png")
        pixmap_i = pixmap_i.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        self.jugador.label_i.setPixmap(pixmap_i)

        pixmap_m = QtGui.QPixmap("img/jugador/m.png")
        pixmap_m = pixmap_m.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        self.jugador.label_m.setPixmap(pixmap_m)

        pixmap_d = QtGui.QPixmap("img/jugador/d.png")
        pixmap_d = pixmap_d.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        self.jugador.label_d.setPixmap(pixmap_d)

    def direccion_bala(self, bala):

        y_2 = self.mouse_y
        y_1 = bala.position[1]
        x_2 = self.mouse_x
        x_1 = bala.position[0]

        theta = self.theta(y_2, y_1, x_2, x_1)
        theta -= 90

        pixmap = QtGui.QPixmap("img/jugador/bala.png")
        pixmap = pixmap.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        bala.label.setPixmap(pixmap)

    def direccionar_zombie(self, zombie):
        y_2 = self.jugador.position[1]
        y_1 = zombie.position[1]
        x_2 = self.jugador.position[0]
        x_1 = zombie.position[0]

        theta = self.theta(y_2, y_1, x_2, x_1)

        pixmap_i = QtGui.QPixmap("img/zombie/i.png")
        pixmap_i = pixmap_i.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        zombie.label_i.setPixmap(pixmap_i)

        pixmap_m = QtGui.QPixmap("img/zombie/m.png")
        pixmap_m = pixmap_m.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        zombie.label_m.setPixmap(pixmap_m)

        pixmap_d = QtGui.QPixmap("img/zombie/d.png")
        pixmap_d = pixmap_d.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        zombie.label_d.setPixmap(pixmap_d)

        pixmap_a = QtGui.QPixmap("img/zombie/ataque.png")
        pixmap_a = pixmap_a.transformed(
            QtGui.QTransform().rotate(theta), QtCore.Qt.SmoothTransformation)
        zombie.label_a.setPixmap(pixmap_a)

    def direccion_zombies(self):
        for zombie in self.zombies:
            self.direccionar_zombie(zombie)

    def calcular_movimiento(self, r, y_2, y_1, x_2, x_1, theta=0):
        x, y = self.diff(y_2, y_1, x_2, x_1)
        rad = math.atan2(y, x) + math.radians(theta)
        mov_x = round(r * math.cos(rad))
        mov_y = -1 * (round(r * math.sin(rad)))

        return mov_x, mov_y

    def mover_jugador(self, letra):
        r = 10
        y_2 = self.mouse_y
        y_1 = self.jugador.position[1]
        x_2 = self.mouse_x
        x_1 = self.jugador.position[0]

        dicc = {"w": 0, "a": 90, "s": 180, "d": 270}

        theta = dicc[letra]

        mov_x, mov_y = self.calcular_movimiento(r, y_2, y_1, x_2, x_1, theta)

        x = self.jugador.position[0]
        y = self.jugador.position[1]

        dim_x = self.jugador.dim[0] / 2
        dim_y = self.jugador.dim[1] / 2

        if not self.choque(x + mov_x, y + mov_y) \
                and x + mov_x >= dim_x and y + mov_y >= dim_y \
                and x + mov_x <= self.dim[0]-self.jugador.dim[0] \
                and y + mov_y <= self.dim[1]-self.jugador.dim[0]:
            self.jugador.agregar_movimiento(mov_x, mov_y)

    def keyPressEvent(self, QKeyEvent):

        if QKeyEvent.key() == QtCore.Qt.Key_W:
            self.mover_jugador("w")

        elif QKeyEvent.key() == QtCore.Qt.Key_A:
            self.mover_jugador("a")

        elif QKeyEvent.key() == QtCore.Qt.Key_S:
            self.mover_jugador("s")

        elif QKeyEvent.key() == QtCore.Qt.Key_D:
            self.mover_jugador("d")
        elif QKeyEvent.key() == QtCore.Qt.Key_Space:
            if self.pausado:
                self.play()
            else:
                self.pausa()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            if self.jugador.ammo > 0:

                r = 225
                y_2 = self.mouse_y
                y_1 = self.jugador.position[1]
                x_2 = self.mouse_x
                x_1 = self.jugador.position[0]

                inicial = self.jugador.position
                mov_x, mov_y = self.calcular_movimiento(r, y_2, y_1, x_2, x_1)
                final = inicial[0] + mov_x, inicial[1] + mov_y
                bala = Bala(self, self.jugador, inicial, final)
                self.balas.append(bala)
                self.direccion_bala(bala)
                bala.start()
                self.jugador.disparar()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_x = QMouseEvent.x()
        self.mouse_y = QMouseEvent.y()
        self.direccion_jugador()

    def actualizarImagen(self, myImageEvent):
        lista = ["Bala", "Cerveza", "Pistola"]
        if myImageEvent.objeto.__class__.__name__ in lista:
            myImageEvent.objeto.label.move(myImageEvent.x, myImageEvent.y)
        else:
            myImageEvent.objeto.label_i.move(myImageEvent.x, myImageEvent.y)
            myImageEvent.objeto.label_m.move(myImageEvent.x, myImageEvent.y)
            myImageEvent.objeto.label_d.move(myImageEvent.x, myImageEvent.y)

            if myImageEvent.ataque:

                myImageEvent.objeto.label_a.setVisible(True)
                myImageEvent.objeto.label_i.setVisible(False)
                myImageEvent.objeto.label_m.setVisible(False)
                myImageEvent.objeto.label_d.setVisible(False)

            else:

                if myImageEvent.cont == 0:
                    myImageEvent.objeto.label_i.setVisible(False)
                    myImageEvent.objeto.label_m.setVisible(True)

                elif myImageEvent.cont == 1:
                    myImageEvent.objeto.label_m.setVisible(False)
                    myImageEvent.objeto.label_d.setVisible(True)

                elif myImageEvent.cont == 2:
                    myImageEvent.objeto.label_d.setVisible(False)
                    myImageEvent.objeto.label_m.setVisible(True)

                elif myImageEvent.cont == 3:
                    myImageEvent.objeto.label_m.setVisible(False)
                    myImageEvent.objeto.label_i.setVisible(True)

            if myImageEvent.objeto.__class__.__name__ == "Jugador":
                self.direccion_zombies()
            elif myImageEvent.objeto.__class__.__name__ == "Zombie":
                myImageEvent.objeto.label_a.move(
                    myImageEvent.x, myImageEvent.y)
                if not myImageEvent.ataque:
                    myImageEvent.objeto.label_a.setVisible(False)
            else:
                self.direccionar_zombie(myImageEvent.objeto)

    def borrarImagen(self, myImageEvent):
        lista = ["Bala", "Cerveza", "Pistola"]
        if myImageEvent.objeto.__class__.__name__ in lista:
            myImageEvent.objeto.label.close()
        else:
            if myImageEvent.objeto.__class__.__name__ == "Zombie":
                myImageEvent.objeto.label_a.close()
            myImageEvent.objeto.label_i.close()
            myImageEvent.objeto.label_m.close()
            myImageEvent.objeto.label_d.close()

    def cerrar(self):
        self.parent.volver(self.puntaje)
        self.close()

    def closeEvent(self, QCloseEvent):
        QCloseEvent.accept()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    juego = Juego()
    juego.show()
    app.exec_()
