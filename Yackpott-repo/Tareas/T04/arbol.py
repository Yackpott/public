class Arbol:

    def __init__(self, calles, registrados=[], pista=None, otra=None):
        self.calles = calles
        self.registrados = registrados
        self.pista = pista
        self.otra = otra
        self.hijos = []
        self.semaforo = False
        self.terminal = False

        # sigue corriendo hasta que haya registrado todos
        if len(self.calles.values()) > len(self.registrados):
            self.agregar()

    # tranforma facil para buscar en el dicc
    def buscar(self, x, y):
        if self.calles[str(x) + "," + str(y)]:
            return self.calles[str(x) + "," + str(y)]
        else:
            return None

    def siguiente(self, calle):
        if calle.dirr == "arriba":
            if self.buscar(calle.x - 1, calle.y):
                return self.buscar(calle.x - 1, calle.y)
        elif calle.dirr == "abajo":
            if self.buscar(calle.x + 1, calle.y):
                return self.buscar(calle.x + 1, calle.y)
        elif calle.dirr == "derecha":
            if self.buscar(calle.x, calle.y + 1):
                return self.buscar(calle.x, calle.y + 1)
        elif calle.dirr == "izquierda":
            if self.buscar(calle.x, calle.y - 1):
                return self.buscar(calle.x, calle.y - 1)
        else:
            return None

    # tupla true es la pista de la derecha, el otro elemento es la otra pista
    def encontrar_otra(self, pista):
        if pista.dirr == "arriba" or pista.dirr == "abajo":
            if self.buscar(pista.x + 1, pista.y):
                return True, self.buscar(pista.x + 1, pista.y)
            elif self.buscar(pista.x - 1, pista.y):
                return False, self.buscar(pista.x - 1, pista.y)
        else:
            if self.buscar(pista.x, pista.y + 1):
                return True, self.buscar(pista.x, pista.y + 1)
            elif self.buscar(pista.x, pista.y + 1):
                return False, self.buscar(pista.x, pista.y - 1)

    def es_semaforo(self, pista, otra):
        if pista.dirr == "arriba":
            pass
        elif pista.dirr == "abajo":
            pass
        elif pista.diir == "derecha":
            pass
        elif pista.dirr == "izquierda":
            pass

    def agregar(self):
        if self.otra is None and self.pista is None:
            pista_1 = list(self.calles.values())[0]
            derecha, pista_2 = self.encontrar_otra(pista_1)
            if derecha:
                self.pista = pista_1
                self.otra = pista_2
            else:
                self.pista = pista_2
                self.otra = pista_1
        else:
            pista = self.siguiente(self.pista)
            if pista:
                if pista not in self.registrados:
                    derecha, otra = self.encontrar_otra(pista)
                    if self.es_semaforo(pista, otra):
                        pass
                    else:
                        self.registrados.extend([pista, otra])
                        self.hijos.append(Arbol(self.calles, pista, otra))
            else:
                self.terminal = True

    # encuentra el arbol
    def buscar_rama(self, key):
        if self.calles[key] == self.pista or self.calles[key] == self.otra:
            return self
        else:
            for hijo in self.hijos:
                hijo.buscar_rama(key)

    # camino mas corto factible
    def camino(self, origen, destino):
        pass
