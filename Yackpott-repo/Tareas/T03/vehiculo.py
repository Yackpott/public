from sistema import Sistema


class Vehiculo:

    def __init__(self):
        self.movimientos = 0
        self.dano_recibido = 0
        self.faltan = 0

    def paso(self):
        if self.faltan > 0:
            self.faltan -= 1
        try:
            for ataque in self.ataques.values():
                ataque.paso()
        except:
            pass

    def atacar(self, ataque, objetivo):
        try:
            self.ataque[ataque](objetivo)
        except KeyError as e:
            print("Error: {} no existe el ataque {}".format(e, ataque))

    def mover(self, vector):
        Sistema.mover(self, vector)

    @property
    def disponible(self):
        return not self.faltan

    def __repr__(self):
        return self.__class__.__name__[0]
