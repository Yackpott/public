class Estadisticas:

    def __init__(self, tipo, otro):
        self.tipo = tipo
        self.otro = otro
        self.lista = []

    def agregar(self, vehiculo):
        self.lista.append(vehiculo)

    def imprimir(self, turno):
        try:
            print("\nEstadisticas {}:".format(self.tipo))
            self.acierto()
            self.dano()
            self.ataques()
            self.barco_movimientos()
            self.turnos(turno)
        except Exception as e:
            print("[ERROR]", e)

    def acierto(self):
        total_exitosos = 0
        total_intentos = 0
        for vehiculo in self.lista:
            exitosos = 0
            intentos = 0
            nom = vehiculo.__class__.__name__
            if nom != "Lancha" and nom != "Puerto" and nom != "Explorador":
                for ataque in vehiculo.ataques.values():
                    exitosos += ataque.exitosos
                    intentos += ataque.intentos
                if intentos != 0:
                    porcentaje = 100 * (exitosos / intentos)
                else:
                    porcentaje = 0
                print("Porcentaje de acierto del {}: {}".format(
                    vehiculo.__class__.__name__, porcentaje))
                total_exitosos += exitosos
                total_intentos += intentos
        if total_intentos != 0:
            porcentaje = 100 * (total_exitosos / total_intentos)
        else:
            porcentaje = 0
        print("Porcentaje de acierto total: {}".format(porcentaje))

    def dano(self):
        total = 0
        for vehiculo in self.lista:
            total += vehiculo.dano_recibido
            print("El {} dano {}".format(
                vehiculo.__class__.__name__, vehiculo.dano_recibido))
        print("{} recibio en total {}".format(self.tipo, total))
        print("{} te ataco en total {}".format(self.otro, total))

    def ataques(self):
        aux = ["UGM", "BGM", "Napalm", "Minuteman", "Kamikaze", "GBU"]
        utilizado = {"UGM": 0, "BGM": 0, "Napalm": 0,
                     "Minuteman": 0, "Kamikaze": 0, "GBU": 0}
        eficiente = {"UGM": [0, 0], "BGM": [0, 0], "Napalm": [
            0, 0], "Minuteman": [0, 0], "Kamikaze": [0, 0], "GBU": [0, 0]}
        for i in aux:
            for vehiculo in self.lista:
                nom = vehiculo.__class__.__name__
                if nom != "Lancha" and nom != "Explorador":
                    for nombre, ataque in vehiculo.ataques.items():
                        if i == nombre:
                            utilizado[nombre] += ataque.intentos
                            eficiente[nombre][0] += ataque.exitosos
                            eficiente[nombre][1] += ataque.intentos
        mas_utilizado = [None, 0]
        mas_eficiente = [None, 0]
        for k, v in utilizado.items():
            if mas_utilizado[1] <= v:
                mas_utilizado[0] = k
                mas_utilizado[1] = v
        for k, v in eficiente.items():
            if v[1] != 0:
                if mas_eficiente[1] <= v[0] / v[1]:
                    mas_eficiente[0] = k
                    mas_eficiente[1] = v[0] / v[1]
        print("El ataque mas utilizado es {}".format(mas_utilizado[0]))
        print("El ataque mas eficiente es {}".format(mas_eficiente[0]))

    def barco_movimientos(self):
        mas = [None, 0]
        for vehiculo in self.lista:
            if vehiculo.__class__.__bases__[0].__name__ == "Maritimo":
                if mas[1] <= vehiculo.movimientos:
                    mas[0] = vehiculo
                    mas[1] = vehiculo.movimientos
        print("{} es el barco con mas movimientos".format(
            mas[0].__class__.__name__))

    def turnos(self, turno):
        print("El turno es {}".format(turno))
