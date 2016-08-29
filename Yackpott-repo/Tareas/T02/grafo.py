from sistema import *
from lista import Lista
from random import randint


class ArbolBinario:

    def __init__(self, nodo_raiz=None):
        self.nodo_raiz = nodo_raiz

    def agregar_nodo(self, nodo):
        if self.nodo_raiz is None:
            self.nodo_raiz = nodo
        else:
            temp = self.nodo_raiz
            agregado = False

            while not agregado:
                if nodo.id <= temp.id:
                    if temp.hijo_izquierdo is None:
                        temp.hijo_izquierdo = nodo
                        agregado = True

                    else:
                        temp = temp.hijo_izquierdo

                else:
                    if temp.hijo_derecho is None:
                        temp.hijo_derecho = nodo
                        agregado = True

                    else:
                        temp = temp.hijo_derecho

    def buscar(self, objetivo):
        def recorrer(nodo, objetivo):
            if nodo is None:
                return None
            else:
                if objetivo == nodo.id:
                    return nodo
                else:
                    if objetivo < nodo.id:
                        return recorrer(nodo.hijo_izquierdo, objetivo)
                    else:
                        return recorrer(nodo.hijo_derecho, objetivo)
        return recorrer(self.nodo_raiz, objetivo)


class Grafo:
    arbol = ArbolBinario()
    lista = Lista()

    def __init__(self, id=0):
        self.id = id
        self.capacidad = get_capacidad()
        self.hijo_izquierdo = None
        self.hijo_derecho = None
        Grafo.arbol.agregar_nodo(self)
        Grafo.lista.append(self)
        self.arcos = Lista()

    def agregar_arco(self, arco):
        if arco not in self.arcos:
            self.arcos.append(arco)

    def agregar_nodo(self):
        id_arco = randint(0, posibles_conexiones() - 1)
        hacer_conexion(id_arco)
        if preguntar_puerto_actual()[1]:
            return self.buscar_nodo(0)
        id_hijo = preguntar_puerto_actual()[0]
        hijo = self.buscar_nodo(id_hijo)
        if not hijo:
            hijo = Grafo(id_hijo)
        arco = Arco(id_arco, self, hijo)
        self.agregar_arco(arco)
        return hijo

    def buscar_nodo(self, objetivo):
        return Grafo.arbol.buscar(objetivo)

    def __str__(self):
        linea = ""
        for i in range(len(Grafo.lista)):
            nodo = self.buscar_nodo(i)
            linea += "PUERTO {}".format(nodo.id) + "\n"
            for arco in nodo.arcos:
                linea += "CONEXION {} {}".format(nodo.id, arco.hijo.id)
                linea += "\n"
        return linea


class Arco:

    def __init__(self, id, padre, hijo):
        self.id = id
        self.padre = padre
        self.hijo = hijo

    def __eq__(self, other):
        if self.id == other.id and self.hijo == other.hijo:
            return True
        else:
            return False
