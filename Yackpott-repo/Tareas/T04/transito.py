import random


class Semaforo:
    semaforos = []

    def __init__(self):
        Semaforo.semaforos.append(self)
        self.verde = True
        self.espera = 20

    @property
    def roja(self):
        return not(self.verde)


class Calle:

    def __init__(self, x, y, dirr):
        self.x = x
        self.y = y
        self.dirr = dirr
        self.auto = None
        self.semaforo = None
        self.entrada = False
        self.salida = False


class Auto:

    def __init__(self):
        self.tipo = self.__class__.__name__
        self.posicion = None
        self.t_cambio = 0.5
        self.sirena = False
        self.dicc_teta = {
            "arriba": 270, "abajo": 90, "derecha": 0, "izquierda": 0}

    @property
    def x(self):
        try:
            self._x = self.posicion.x
        except Exception:
            self._x = None
        return self._x

    @property
    def y(self):
        try:
            self._y = self.posicion.y
        except Exception:
            self._y = None
        return self._y

    @property
    def teta(self):
        try:
            self._teta = self.dicc_teta[self.posicion.dirr]
            if self.posicion.dirr == "izquierda":
                self.refleccion = True
            else:
                self.refleccion = False
        except Exception:
            self._teta = None
        return self._teta

    @property
    def velocidad(self):
        if self.tipo != "Normal" and self.tipo != "Taxi":
            if self.sirena:
                self._velocidad = 1
            else:
                self._velocidad = 0.5
        else:
            self._velocidad = random.uniform(0.5, 1)
        return self._velocidad


class Taxi(Auto):

    def __init__(self):
        self.tipo = self.__class__.__name__
        super().__init__()
        self.t_recoger = random.uniform(5, 15)
        self.t_dejar = random.uniform(10, 20)


class Bombero(Auto):

    def __init__(self):
        super().__init__()
        self.tipo = self.__class__.__name__


class Policia(Auto):

    def __init__(self):
        super().__init__()
        self.tipo = self.__class__.__name__


class Ambulancia(Auto):

    def __init__(self):
        super().__init__()
        self.tipo = self.__class__.__name__


class Transito:

    def __init__(self, calles, grilla, dimx, dimy):
        self.calles = calles
        self.grilla = grilla
        self.dimx = dimx
        self.dimy = dimy
        self.autos = []
        self.taxis = []

    def cargar(self):
        self.agregar_semaforos()
        self.ver_extremos()
        self.crear_vehiculos()
        self.poner_vehiculos()

    def agregar_semaforos(self):
        pass

    def ver_extremos(self):
        for calle in self.calles.values():
            if calle.x == 0:
                if calle.dirr == "arriba":
                    calle.salida = True
                elif calle.dirr == "abajo":
                    calle.entrada = True
            if calle.x == self.dimx - 1:
                if calle.dirr == "arriba":
                    calle.entrada = True
                elif calle.dirr == "abajo":
                    calle.salida = True
            if calle.y == 0:
                if calle.dirr == "derecha":
                    calle.entrada = True
                elif calle.dirr == "izquierda":
                    calle.salida = True
            if calle.y == self.dimy - 1:
                if calle.dirr == "derecha":
                    calle.salida = True
                elif calle.dirr == "izquierda":
                    calle.entrada = True

    def crear_vehiculos(self):
        # 4 porque hay calle por pista
        for _ in range(int(len(self.calles) / 4)):
            if 0.2 > random.random():
                self.taxis.append(Taxi())
            else:
                self.autos.append(Auto())

    def poner_vehiculos(self):
        calles = list(self.calles.values())
        for auto in self.autos:
            auto.posicion = calles.pop(random.randint(0, len(calles) - 1))
        for taxi in self.taxis:
            taxi.posicion = calles.pop(random.randint(0, len(calles) - 1))

    def actualizar_autos(self, t):
        """
        funcion
        si sale auto:
            self.salio_auto()
            self.agregar_auto()
        self.borrar_transito()
        self.actualizar_transito()
        """
        pass

    def salio_auto(self):
        pass

    def agregar_auto(self):
        pass

    def actualizar_transito(self):
        for auto in self.autos:
            self.grilla.agregar_auto(
                auto.y + 1, auto.x + 1, auto.teta, auto.refleccion)

        for taxi in self.taxis:
            self.grilla.agregar_taxi(
                auto.y + 1, auto.x + 1, taxi.teta, auto.refleccion)

    def borrar_transito(self):
        for calle in self.calles.values():
            self.grilla.quitar_imagen(calle.y + 1, calle.x + 1)
