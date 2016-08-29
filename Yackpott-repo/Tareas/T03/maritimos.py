from ataques import UGM, Minuteman, BGM, GBU, Kit
from vehiculo import Vehiculo


class Maritimo(Vehiculo):

    def __init__(self):
        super().__init__()
        self.fuego = False
        self.dano = 0

    def recibir(self, dano, sistema):
        if self.dano + dano >= self.resistencia:
            dano = self.resistencia - self.dano
            sistema.eliminar(self)
        if dano > 0:
            self.dano_recibido += dano
        self.dano += dano


class Barco(Maritimo):

    def __init__(self):
        super().__init__()
        self.resistencia = 30
        self.espacio = (3, 1)
        self.ataques = dict()
        self.ataques[UGM().__class__.__name__] = UGM()
        self.ataques[Minuteman().__class__.__name__] = Minuteman()
        self.ataques[GBU().__class__.__name__] = GBU()


class Guerra(Maritimo):

    def __init__(self):
        super().__init__()
        self.resistencia = 60
        self.espacio = (2, 3)
        self.ataques = dict()
        self.ataques[UGM().__class__.__name__] = UGM()
        self.ataques[BGM().__class__.__name__] = BGM()
        self.ataques[GBU().__class__.__name__] = GBU()


class Lancha(Maritimo):

    def __init__(self):
        super().__init__()
        self.resistencia = 1
        self.espacio = (2, 1)

    def atacar(self):
        raise Exception(
            "Error: {} no puede atacar".format(self.__class__.__name__))


class Puerto(Maritimo):

    def __init__(self):
        super().__init__()
        self.resistencia = 80
        self.espacio = (2, 4)
        self.ataques = dict()
        self.ataques[Kit().__class__.__name__] = Kit()

    def mover(self, der, ab):
        raise Exception(
            "Error: {} no puede moverse".format(self.__class__.__name__))
