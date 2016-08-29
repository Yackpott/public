class Casa:
    lista = []

    def __init__(self, tipo, x, y, t_min, t_max):
        self.material = globals()[tipo.capitalize()]()
        self.x = x
        self.y = y
        self.t_min = t_min
        self.t_max = t_max

    @property
    def proba_incendio(self):
        num = self.material.peso
        dem = sum(list(map(lambda casa: casa.material.peso, Casa.lista)))
        self._proba_incendio = num / dem
        return self._proba_incendio

    @property
    def proba_robo(self):
        num = 10 + self.x + self.y
        dem = sum(list(map(lambda casa: 10 + casa.x + casa.y, Casa.lista)))
        self._proba_robo = num / dem
        return self._proba_robo

    @property
    def proba_enfermo(self):
        self._proba_enfermo = 1/len(Casa.lista)
        return self._proba_enfermo


class Madera:
    peso = 10
    a = 30
    b = 120


class Ladrillos:
    peso = 7
    a = 40
    b = 100


class Hormigon:
    peso = 4
    a = 60
    b = 80


class Metal:
    peso = 2
    a = 30
    b = 40
