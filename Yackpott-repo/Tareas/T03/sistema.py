from copy import copy


class Sistema:
    sistemas = []

    def __init__(self, tipo, mapa, otro_mapa, lista, otra_lista, radar, estadisticas, otra_estadisticas, n):
        Sistema.sistemas.append(self)
        self.tipo = tipo
        self.mapa = mapa
        self.otro_mapa = otro_mapa
        self.lista = lista
        self.otra_lista = otra_lista
        self.radar = radar
        self.estadisticas = estadisticas
        self.otra_estadisticas = otra_estadisticas
        self.n = n
        self.cont = 0

    def leer(self, texto):
        aux = input(texto)
        exit(0) if aux == "exit" else None
        return aux

    def turno(self):
        if self.tipo == "Jugador" or "Oponente":
            self.jugador()
        else:
            self.computador()
        for vehiculo in self.lista:
            try:
                if vehiculo.fuego:
                    vehiculo.dano += vehiculo.fuego
                    vehiculo.fuego = False
                    if vehiculo.dano >= vehiculo.resistencia:
                        self.estadisticas.agregar(vehiculo)
                        self.lista.remove(vehiculo)
                        print(
                            "Se quemo por completo el {}".format(vehiculo.__class__.__name__))
                        for x in range(len(self.mapa.mar)):
                            for y in range(len(self.mapa.mar[0])):
                                if self.mapa.mar[x][y] == vehiculo:
                                    self.mapa.mar[x][y] = 0
                    else:
                        print("Se un quemo un poco, el que recibio Napalm")
            except:
                pass
        self.siguiente()

    def jugador(self):
        copia = [i for i in self.lista if i.__class__.__name__ !=
                 "Explorador" or i.disponible]
        for i in copia:
            if i.__class__.__name__ == "Caza":
                if not i.ataques["Napalm"].disponible:
                    copia.remove(i)
                break
        seguir = True
        while len(copia) > 0 and seguir:
            while True:
                try:
                    imp = "\nTurno {} {}:\nVehiculos disponibles:\n".format(
                        self.cont, self.tipo)
                    for i in range(len(copia)):
                        imp += str(i) + " --> " + \
                            copia[i].__class__.__name__ + "\n"
                    imp += "radar --> para ver ataques\n"
                    imp += "listo --> para terminar el turno\n"
                    linea = self.leer(imp)
                    if linea == "radar":
                        turno = self.leer("Ingrese turno: ")
                        self.radar.obtener(int(turno))
                        break
                    elif linea == "listo":
                        seguir = False
                        break
                    vehiculo = copia.pop(int(linea))
                    if vehiculo.__class__.__name__ == "Puerto":
                        linea = self.leer(
                            "Entre nombre del barco a recuperar... ")
                        ataque = vehiculo.ataques["Kit"]
                        if not self.recuperar(ataque, linea):
                            raise Exception
                        break
                    imp = """
Vehiculo seleccionado {}
Escoja opcion:
0 --> para atacar
1 --> para mover
""".format(vehiculo.__class__.__name__)
                    linea = self.leer(imp)
                    if linea == "0":
                        nom = vehiculo.__class__.__name__
                        if nom == "Explorador" or nom == "Lancha":
                            raise AttributeError
                        else:
                            self.atacar(vehiculo)
                    elif linea == "1":
                        if vehiculo.__class__.__name__ == "Puerto":
                            raise AttributeError
                        self.mover(vehiculo)
                    else:
                        raise ValueError(linea)
                    break
                except Exception as e:
                    print("[ERROR] {}".format(type(e).__name__))

    def recuperar(self, ataque, linea):
        if ataque.disponible:
            for i in self.lista:
                if i.__class__.__name__ == linea:
                    vehiculo = i
                    break
            print(vehiculo.dano)
            if vehiculo.dano > 0:
                vehiculo.recibir(ataque.dano, self)
                ataque.faltan = ataque.turnos
                return True
            else:
                print("No tenia dano")
                return False
        else:
            print("Kit no disponible")
            return False

    def computador(self):
        # proximamente jajaja
        pass

    def atacar(self, vehiculo):
        while True:
            try:
                imp = "Seleccione ataque:\n"
                for nombre in vehiculo.ataques:
                    imp += nombre + "\n"
                linea = self.leer(imp)
                ataque = vehiculo.ataques[linea]
                if not ataque.disponible:
                    print("Ataque no disponible...")
                    raise Exception
                linea = self.leer("Ingrese el primer punto de la forma x,y: ")
                if linea.count(",") != 1:
                    raise ValueError
                x = int(linea[:linea.find(",")])
                y = int(linea[linea.find(",") + 1:])
                if ataque.__class__.__name__ == "BGM":
                    linea = self.leer("horizontal o vertical? ")
                    if linea == "horizontal":
                        cont = 0
                        for i in range(self.n):
                            posicion = self.otro_mapa.mar[x][i]
                            if posicion != 0:
                                cont += 1
                                posicion.recibir(ataque.dano, self)
                                ataque.exitosos += 1
                        print("Se daño {} veces".format(cont))
                    elif linea == "vertical":
                        cont = 0
                        for i in range(self.n):
                            posicion = self.otro_mapa.mar[i][y]
                            if posicion != 0:
                                cont += 1
                                posicion.recibir(ataque.dano, self)
                                ataque.exitosos += 1
                        print("Se dañaron {} vehiculos".format(cont))
                    else:
                        raise ValueError
                elif ataque.__class__.__name__ == "GBU":
                    if self.otro_mapa.aire[x][y].__class__.__name__ == "Explorador" \
                            and self.otro_mapa.aire[x + 1][y].__class__.__name__ == "Explorador":
                        self.otro_mapa.aire[x][y].faltan = 5
                        ataque.exitosos += 1
                        print("Se inmovilizo el explorador por 5 turnos")
                else:
                    posicion = self.otro_mapa.mar[x][y]
                    if ataque.__class__.__name__ == "Napalm":
                        posicion.fuego = ataque.dano
                    if posicion != 0:
                        print("Se ataco a un enemigo en {},{}".format(x, y))
                        posicion.recibir(ataque.dano, self)
                        ataque.exitosos += 1
                    if vehiculo.__class__.__name__ == "IXXI":
                        self.estadisticas.agregar(vehiculo)
                        self.lista.remove(vehiculo)
                        print("Autodestrucccion de IXXI...")
                        for x in range(len(self.mapa.aire)):
                            for y in range(len(self.mapa.aire[0])):
                                if self.mapa.aire[x][y] == vehiculo:
                                    self.mapa.aire[x][y] = 0
                ataque.intentos += 1
                ataque.faltan = ataque.turnos
                self.radar.agregar(self.cont, (x, y))
                break
            except Exception as e:
                print("[ERROR] {}".format(type(e).__name__))

    def mover(self, vehiculo):
        copia = copy(self.mapa)
        while True:
            try:
                vector = self.leer("Ingrese vector de la forma x,y: ")
                h, k = int(vector[:vector.find(",")]), int(
                    vector[vector.find(",") + 1])
                if vehiculo.__class__.__name__ != "Lancha":
                    if abs(h) > 1 or abs(k) > 1:
                        print(5)
                        print("Error movimiento muy grande")
                        raise Exception
                if vehiculo.__class__.__bases__[0].__name__ == "Maritimo":
                    aux = self.mapa.mar
                else:
                    aux = self.mapa.aire
                found = False
                for x in range(len(aux)):
                    for y in range(len(aux[0])):
                        if aux[x][y] == vehiculo:
                            i = x
                            j = y
                            found = True
                            break
                    if found:
                        break

                for x in range(len(aux)):
                    for y in range(len(aux[0])):
                        if aux[x][y] == vehiculo:
                            aux[x][y] = 0
                for x in range(vehiculo.espacio[1]):
                    for y in range(vehiculo.espacio[0]):
                        aux[i + x + k][j + y + h] = vehiculo
                vehiculo.movimientos += 1
                print(self.mapa)
                break
            except Exception as e:
                print("[ERROR] {}".format(type(e).__name__))
                self.mapa = copia

    def eliminar(self, vehiculo):
        self.otra_estadisticas.agregar(vehiculo)
        self.otra_lista.remove(vehiculo)
        print("Se elimino el {}".format(vehiculo.__class__.__name__))
        for x in range(len(self.otro_mapa.mar)):
            for y in range(len(self.otro_mapa.mar[0])):
                if self.otro_mapa.mar[x][y] == vehiculo:
                    self.otro_mapa.mar[x][y] = 0
        self.gano()

    def gano(self):
        for vehiculo in self.otra_lista:
            if vehiculo.__class__.__bases__[0].__name__ == "Maritimo" and vehiculo.__class__.__name__ != "Lancha":
                return None
        print("El ganador es {}".format(self.tipo))
        for vehiculo in self.lista:
            self.estadisticas.agregar(vehiculo)
        for vehiculo in self.otra_lista:
            self.otra_estadisticas.agregar(vehiculo)
        for sis in Sistema.sistemas:
            sis.estadisticas.imprimir(sis.cont)
        exit(0)

    def siguiente(self):
        for vehiculo in self.lista:
            vehiculo.paso()
        self.cont += 1
