class Ataque:

    def __init__(self):
        self.intentos = 0
        self.exitosos = 0
        self.faltan = 0

    @property
    def disponible(self):
        return not self.faltan

    def paso(self):
        if self.faltan > 0:
            self.faltan -= 1


class UGM(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = 50
        self.turnos = 1


class BGM(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = 5
        self.turnos = 3


class Napalm(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = 5
        self.dano_fuego = 0
        self.turnos = 8


class Minuteman(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = 15
        self.turnos = 3


class Kamikaze(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = float("inf")
        self.turnos = 1


class GBU(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = 0
        self.turnos = 1


class Kit(Ataque):

    def __init__(self):
        super().__init__()
        self.dano = -1
        self.turnos = 2
