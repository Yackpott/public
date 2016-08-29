import sys
import time
from PyQt4 import QtGui
from gui.gui import GrillaSimulacion
from transito import Calle
from arbol import Arbol
from edificios import Casa
from transito import Transito
from emergencias import Cuartel, Comisaria, Hospital
from itertools import permutations

ANTES = time.time()


class Simulacion:

    def __init__(self, app, repeticiones):
        self.app = app
        self.repeticiones = repeticiones
        self.var = {"t": 0, "t_max": 1209600, "t_incendio": 0,
                    "n_incendio": 0, "n_atrapado": 0, "n_escapo": 0,
                    "n_robos": 0, "t_ambulancia": 0, "n_enfermos": 0}
        self.grilla = None
        self.dimx = None
        self.dimy = None
        self.calles = dict()
        self.casas = dict()
        self.vacios = dict()
        self.cargar_archivos()
        self.arbol = Arbol(self.calles)
        self.cargar_gui()
        self.transito = Transito(
            self.calles, self.grilla, self.dimx, self.dimy)
        self.transito.cargar()
        self.transito.actualizar_transito()

        # refresh mas lento
        self.grilla.tiempo_intervalo = 0.5

        self.combinaciones()

    def dim(self, linea):
        x = int(linea[:linea.find(",")])
        y = int(linea[linea.find(",") + 1:])
        return x, y

    def cargar_archivos(self):
        with open("mapa.txt", "r") as f:
            linea = f.readline()
            self.dimx = int(linea[:linea.find("x")])
            self.dimy = int(linea[linea.find("x") + 1:])
            linea = f.readline()
            while linea != "":
                linea = linea.replace("\n", "")
                lineas = linea.split(" ")
                x, y = self.dim(lineas[0])
                if "calle" in linea:
                    self.calles[lineas[0]] = Calle(x, y, lineas[2])
                elif "casa" in linea:
                    tipo = lineas[3]
                    t_min = int(lineas[4][1:-1])
                    t_max = int(lineas[5][:-2])
                    self.casas[lineas[0]] = Casa(tipo, x, y, t_min, t_max)
                else:
                    self.vacios[lineas[0]] = None
                linea = f.readline()

    def cargar_gui(self):
        self.grilla = GrillaSimulacion(self.app, rows=25, cols=23)
        self.grilla.show()

        # cargar
        for casa in self.casas.values():
            self.grilla.agregar_casa(casa.y + 1, casa.x + 1)

        for calle in self.calles.values():
            self.grilla.agregar_calle(calle.y + 1, calle.x + 1)

    def combinaciones(self):
        lista = [Cuartel(), Comisaria(), Hospital(), None]
        permutaciones = list(permutations(lista))
        for combinacion in permutaciones:
            combinacion = list(combinacion)
            for k in self.vacios:
                self.vacios[k] = combinacion.pop()
            self.emergencias_gui()
            self.simular()

    def emergencias_gui(self):
        self.grilla.tiempo_intervalo = 0
        self.borrar_emergencias()
        for k, v in self.vacios.items():
            x, y = self.dim(k)
            if v is not None:
                if v.tipo == "Cuartel":
                    self.grilla.agregar_cuartel_bomberos(y + 1, x + 1)
                elif v.tipo == "Comisaria":
                    self.grilla.agregar_comisaria(y + 1, x + 1)
                elif v.tipo == "Hospital":
                    self.grilla.agregar_hospital(y + 1, x + 1)
        self.grilla.tiempo_intervalo = 0.5

    def borrar_emergencias(self):
        for k in self.vacios:
            x, y = self.dim(k)
            self.grilla.quitar_imagen(y + 1, x + 1)

    def simular(self):
        time.sleep(1)

REPETICIONES = 50

# inicio
app = QtGui.QApplication([])


print("Empezando la simulacion...")
Simulacion(app, REPETICIONES)
DESPUES = time.time()
print("Termino la simulacion")
print("Se demoro", DESPUES - ANTES)

# para terminar
sys.exit(app.exec_())
