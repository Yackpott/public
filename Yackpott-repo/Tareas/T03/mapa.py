class Mapa:

    def __init__(self, tipo, n):
        self.tipo = tipo
        self.mar = [[0 for x in range(n)] for x in range(n)]
        self.aire = [[0 for x in range(n)] for x in range(n)]

    def agregar(self, vehiculo, linea):
        try:
            if linea.count(",") != 1:
                raise Exception("Error: formato input")
            x = int(linea[:linea.find(",")])
            y = int(linea[linea.find(",") + 1:])
            for i in range(vehiculo.espacio[0]):
                for j in range(vehiculo.espacio[1]):
                    tipo = vehiculo.__class__.__bases__[0].__name__
                    if tipo == "Maritimo":
                        aux = self.mar
                    elif tipo == "Vehiculo":
                        aux = self.aire
                    if aux[x + j][y + i] != 0:
                        raise Exception(
                            "Error: ya estaba el {} ahi".format(
                                aux[x + j][y + i].__class__.__name__))
                    aux[x + j][y + i] = vehiculo
        except Exception as e:
            for i in range(len(aux)):
                for j in range(len(aux[0])):
                    if aux[i][j] == vehiculo:
                        aux[i][j] = 0
            print(e)
            return False
        else:
            print(self)
            return True

    def eliminar(self, vehiculo):
        if vehiculo.__class__.__bases__[0].__name__ is "Maritimo":
            aux = self.mar
        elif vehiculo.__class__.__bases__[0].__name__ is "Vehiculo":
            aux = self.aire
        else:
            raise Exception("Error: no es ni maritimo ni aereo")
        for i in range(len(aux)):
            for j in range(len(aux)):
                aux[i][j] = 0 if aux[i][j] == vehiculo else None

    def __str__(self):
        ret = "\nMapa Maritimo del {}\n".format(self.tipo)
        for i in self.mar:
            ret += str(i) + "\n"
        ret += "\nMapa Aereo del {}\n".format(self.tipo)
        for i in self.aire:
            ret += str(i) + "\n"
        return ret
