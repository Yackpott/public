class Radar:

    def __init__(self):
        self.movimientos = dict()

    def agregar(self, turno, posicion):
        try:
            self.movimientos[turno].append(posicion)
        except:
            self.movimientos[turno] = [posicion]

    def obtener(self, turno):
        try:
            lista = self.movimientos[turno]
            print("Los movimientos del turno {} son:".format(turno))
            for posicion in lista:
                print(posicion)
        except:
            pass
