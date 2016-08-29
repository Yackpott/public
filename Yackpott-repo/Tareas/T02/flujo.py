from sistema import *
from lista import Lista
import sys

sys.setrecursionlimit(10000)


class Flujo():

    def __init__(self, grafo):
        self.id_bummer = puerto_final()
        self.lista = Lista()
        self.recorridos = Lista()
        self.camino = ""
        inicial = grafo.buscar_nodo(0)
        self.cap = inicial.capacidad
        for arco in inicial.arcos:
            self.lista.append(Lista(arco, Lista(arco.padre)))
        self.recorrer()

    def recorrer(self):
        aux = max(self.lista, key=lambda x: x[0].hijo.capacidad)
        arc_max, ant = aux[0], aux[1]
        self.eliminar(arc_max)
        if arc_max.hijo.capacidad < self.cap:
            self.cap = arc_max.hijo.capacidad
        for arco in arc_max.hijo.arcos:
            if arco not in self.recorridos:
                if arco.hijo.id == self.id_bummer:
                    ant.append(arco.hijo)
                    self.ruta(ant)
                    return
                self.recorridos.append(arco)
                aux = Lista()
                for i in ant:
                    aux.append(i)
                aux.append(arco.padre)
                self.lista.append(Lista(arco, aux))
        self.recorrer()

    def eliminar(self, arco):
        for i in range(len(self.lista)):
            if self.lista[i][0] == arco:
                self.lista.pop(i)
                break

    def ruta(self, ant):
        self.camino += "CAP {}\n".format(self.cap)
        for i in range(len(ant) - 1):
            self.camino += "{} {}\n".format(ant[i].id, ant[i + 1].id)

    def __str__(self):
        return self.camino
