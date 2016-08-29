from ataques import Kamikaze, Napalm
from vehiculo import Vehiculo


class Explorador(Vehiculo):

    def __init__(self):
        super().__init__()
        self.espacio = (3, 3)


class IXXI(Vehiculo):

    def __init__(self):
        super().__init__()
        self.espacio = (1, 1)
        self.ataques = dict()
        self.ataques[Kamikaze().__class__.__name__] = Kamikaze()


class Caza(Vehiculo):

    def __init__(self):
        super().__init__()
        self.espacio = (1, 1)
        self.ataques = dict()
        self.ataques[Napalm().__class__.__name__] = Napalm()
