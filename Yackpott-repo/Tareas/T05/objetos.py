from PyQt4 import QtGui
from PyQt4 import QtCore
from collections import deque
import time


class Movimiento:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class RemoveEvent:

    def __init__(self, objeto):
        self.objeto = objeto


class MoveEvent:

    def __init__(self, objeto, x, y, cont=None, ataque=False):
        self.objeto = objeto
        self.x = x
        self.y = y
        self.cont = cont
        self.ataque = ataque


class Objeto(QtCore.QObject):
    trigger = QtCore.pyqtSignal(MoveEvent)
    trigger_2 = QtCore.pyqtSignal(RemoveEvent)
    dim = (20, 20)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.trigger.connect(parent.actualizarImagen)
        self.trigger_2.connect(parent.borrarImagen)
        self.__position = (0, 0)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(
            MoveEvent(
                self, self.position[0] - self.dim[0] / 2,
                self.position[1] - self.dim[1] / 2))

    def borrar(self):
        self.trigger_2.emit(RemoveEvent(self))
        self.parent.objetos.remove(self)


class Cerveza(Objeto):

    def __init__(self, parent):
        super().__init__(parent)
        self.label = QtGui.QLabel("", self.parent)
        pixmap = QtGui.QPixmap("img/cerveza.png")
        self.label.setPixmap(pixmap)
        self.label.setMouseTracking(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setVisible(True)


class Pistola(Objeto):

    def __init__(self, parent):
        super().__init__(parent)
        self.label = QtGui.QLabel("", self.parent)
        pixmap = QtGui.QPixmap("img/Pistola.png")
        self.label.setPixmap(pixmap)
        self.label.setMouseTracking(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setVisible(True)


class Bala(QtCore.QThread):
    trigger = QtCore.pyqtSignal(MoveEvent)
    trigger_2 = QtCore.pyqtSignal(RemoveEvent)
    dim = (30, 30)

    def __init__(self, parent, jugador, inicial, final):
        super().__init__()
        self.daemon = True

        self.parent = parent
        self.trigger.connect(parent.actualizarImagen)
        self.trigger_2.connect(parent.borrarImagen)

        self.jugador = jugador
        self.__position = (0, 0)
        self.cont = 0
        self.inicial = inicial
        self.final = final
        self.label = QtGui.QLabel("", self.parent)
        pixmap = QtGui.QPixmap("img/jugador/bala.png")
        self.label.setPixmap(pixmap)
        self.label.setMouseTracking(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setVisible(True)
        self.position = self.inicial

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(
            MoveEvent(
                self, self.position[0] - self.dim[0] / 2,
                self.position[1] - self.dim[1] / 2))

    def run(self):
        while self.cont < 15 and self.jugador.vivo:
            if self.parent.pausado:
                time.sleep(0.01)
            else:
                time.sleep(0.05)
                if self.mato():
                    break
                self.mover()
                self.cont += 1
        self.trigger_2.emit(RemoveEvent(self))

    def mato(self):
        zom = None
        mini = 25
        for zombie in self.parent.zombies:
            d_1 = abs(self.position[0] - zombie.position[0])
            d_2 = abs(self.position[1] - zombie.position[1])
            if d_1 < mini and d_2 < mini:
                zom = zombie
                mini = max(d_1, d_2)
        if zom:
            self.jugador.mato()
            zom.murio()
            return True
        else:
            return False

    def mover(self):
        r = 15
        y_2 = self.final[1]
        y_1 = self.position[1]
        x_2 = self.final[0]
        x_1 = self.position[0]

        mov_x, mov_y = self.parent.calcular_movimiento(r, y_2, y_1, x_2, x_1)

        self.position = self.position[0] + mov_x, self.position[1] + mov_y


class Jugador(QtCore.QThread):
    trigger = QtCore.pyqtSignal(MoveEvent)
    trigger_2 = QtCore.pyqtSignal(RemoveEvent)
    dim = (50, 50)

    def __init__(self, parent):
        super().__init__()
        self.daemon = True
        self.cont = 0

        self.parent = parent
        self.trigger.connect(parent.actualizarImagen)
        self.trigger_2.connect(parent.borrarImagen)
        self.__position = (0, 0)

        self.movimientos = deque()
        self.ammo = 30
        self.hp = 10
        self.vivo = True

        self.label_ammo = QtGui.QLabel(
            "AMMO: {}".format(str(self.ammo)), self.parent)
        self.label_ammo.setVisible(True)
        self.label_hp = QtGui.QLabel(
            "HP: {}".format(str(self.hp)), self.parent)
        self.label_hp.setVisible(True)
        self.label_ammo.move(10, 30)
        self.label_hp.move(10, 45)

        self.label_i = QtGui.QLabel("", self.parent)
        self.label_i.setVisible(True)
        pixmap_i = QtGui.QPixmap("img/jugador/i.png")
        self.label_i.setPixmap(pixmap_i)
        self.label_i.setMouseTracking(True)
        self.label_i.setAlignment(QtCore.Qt.AlignCenter)

        self.label_m = QtGui.QLabel("", self.parent)
        self.label_m.setVisible(False)
        pixmap_m = QtGui.QPixmap("img/jugador/m.png")
        self.label_m.setPixmap(pixmap_m)
        self.label_m.setMouseTracking(True)
        self.label_m.setAlignment(QtCore.Qt.AlignCenter)

        self.label_d = QtGui.QLabel("", self.parent)
        self.label_d.setVisible(False)
        pixmap_d = QtGui.QPixmap("img/jugador/d.png")
        self.label_d.setPixmap(pixmap_d)
        self.label_d.setMouseTracking(True)
        self.label_d.setAlignment(QtCore.Qt.AlignCenter)

    def agregar_movimiento(self, mov_x, mov_y):
        if len(self.movimientos) < 1:
            self.movimientos.append((mov_x, mov_y))

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(
            MoveEvent(
                self, self.position[0] - self.dim[0] / 2,
                self.position[1] - self.dim[1] / 2, self.cont))
        self.cont += 1
        if self.cont >= 4:
            self.cont -= 4

    def run(self):
        while self.vivo:
            self.label_hp.setText("HP: {}".format(self.hp))
            if self.parent.pausado:
                time.sleep(0.01)
            else:
                time.sleep(0.01)
                try:
                    mov = self.movimientos.popleft()
                    self.mover(mov)
                    obj = self.cerca()
                    if obj:
                        if obj.__class__.__name__ == "Cerveza":
                            self.hp = 10
                            self.label_hp.setText("HP: {}".format(self.hp))
                        elif obj.__class__.__name__ == "Pistola":
                            self.ammo = 30
                            self.label_ammo.setText("AMMO: {}".format(self.ammo))
                        obj.borrar()
                except:
                    pass
        self.label_hp.setText("HP: {}".format(self.hp))
        self.trigger_2.emit(RemoveEvent(self))
        self.parent.cerrar()

    def cerca(self):
        for obj in self.parent.objetos:
            d_1 = abs(self.position[0] - obj.position[0])
            d_2 = abs(self.position[1] - obj.position[1])
            if d_1 < 25 and d_2 < 25:
                return obj
        return None

    def atacado(self):
        try:
            self.hp -= 1
            if self.hp == 0:
                self.murio()
        except:
            pass

    def disparar(self):
        self.ammo -= 1
        self.label_ammo.setText("AMMO: {}".format(self.ammo))

    def mato(self):
        self.parent.puntaje += 100

    def murio(self):
        self.vivo = False

    def mover(self, mov):
        x = self.position[0]
        y = self.position[1]
        time.sleep(0.1)
        self.position = (x + mov[0], y + mov[1])


class Zombie(QtCore.QThread):
    trigger = QtCore.pyqtSignal(MoveEvent)
    trigger_2 = QtCore.pyqtSignal(RemoveEvent)
    dim = (50, 50)

    def __init__(self, parent, jugador):
        super().__init__()
        self.jugador = jugador
        self.daemon = True
        self.cont = 0

        self.parent = parent
        self.trigger.connect(parent.actualizarImagen)
        self.trigger_2.connect(parent.borrarImagen)
        self.__position = (0, 0)

        self.movimientos = deque()
        self.vivo = True
        self.atacando = False

        self.label_i = QtGui.QLabel("", self.parent)
        self.label_i.setVisible(True)
        pixmap_i = QtGui.QPixmap("img/zombie/i.png")
        self.label_i.setPixmap(pixmap_i)
        self.label_i.setMouseTracking(True)
        self.label_i.setAlignment(QtCore.Qt.AlignCenter)

        self.label_m = QtGui.QLabel("", self.parent)
        self.label_m.setVisible(False)
        pixmap_m = QtGui.QPixmap("img/zombie/m.png")
        self.label_m.setPixmap(pixmap_m)
        self.label_m.setMouseTracking(True)
        self.label_m.setAlignment(QtCore.Qt.AlignCenter)

        self.label_d = QtGui.QLabel("", self.parent)
        self.label_d.setVisible(False)
        pixmap_d = QtGui.QPixmap("img/zombie/d.png")
        self.label_d.setPixmap(pixmap_d)
        self.label_d.setMouseTracking(True)
        self.label_d.setAlignment(QtCore.Qt.AlignCenter)

        self.label_a = QtGui.QLabel("", self.parent)
        self.label_a.setVisible(False)
        pixmap_a = QtGui.QPixmap("img/zombie/ataque.png")
        self.label_a.setPixmap(pixmap_a)
        self.label_a.setMouseTracking(True)
        self.label_a.setAlignment(QtCore.Qt.AlignCenter)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(
            MoveEvent(
                self, self.position[0] - self.dim[0] / 2,
                self.position[1] - self.dim[1] / 2, self.cont))
        self.cont += 1
        if self.cont >= 4:
            self.cont -= 4

    def agregar_movimiento(self, mov_x, mov_y):
        self.movimientos.append((mov_x, mov_y))

    def run(self):
        while self.vivo and self.jugador.vivo:
            if self.parent.pausado:
                time.sleep(0.01)
            else:
                time.sleep(0.1)
                try:
                    if self.cerca():
                        self.atacar()
                    mov = self.movimientos.popleft()
                    self.mover(mov)
                except:
                    pass
        self.trigger_2.emit(RemoveEvent(self))
        self.parent.zombies.remove(self)

    def cerca(self):
        d_1 = abs(self.position[0] - self.jugador.position[0])
        d_2 = abs(self.position[1] - self.jugador.position[1])
        if d_1 < 40 and d_2 < 40:
            return True
        else:
            return False

    def atacar(self):
        self.atacando = True
        self.trigger.emit(
            MoveEvent(
                self, self.position[0] - self.dim[0] / 2,
                self.position[1] - self.dim[1] / 2, self.cont, ataque=True))
        self.jugador.atacado()
        time.sleep(0.5)
        self.atacando = False

    def murio(self):
        self.vivo = False

    def mover(self, mov):
        x = self.position[0]
        y = self.position[1]
        time.sleep(0.1)
        self.position = (x + mov[0], y + mov[1])
