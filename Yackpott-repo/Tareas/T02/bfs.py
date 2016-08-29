from sistema import *
from lista import Lista


class BFS:

    def __init__(self, grafo):
        self.ruta_bummer = ""
        self.id_bummer = puerto_final()
        self.lista = Lista()
        self.recorridos = Lista()
        inicial = grafo.buscar_nodo(0)
        anterior = None
        self.recorridos.append(Lista(inicial, anterior))
        for arco in inicial.arcos:
            self.lista.append(Lista(arco.hijo, inicial))
        while not self.recorrer():
            pass

    def recorrer(self):
        lista = self.lista.popleft()
        nodo, padre = lista[0], lista[1]
        if nodo.id == self.id_bummer:
            self.recorridos.append(Lista(nodo, padre))
            self.ruta_bummer = self.ruta(nodo)[1:]
            return True
        if nodo not in self.recorridos[0]:
            self.recorridos.append(Lista(nodo, padre))
            for arco in nodo.arcos:
                self.lista.append(Lista(arco.hijo, nodo))
        return False

    def ruta(self, nodo):
        for otro, padre in self.recorridos:
            if nodo == otro and padre:
                texto = "CONEXION {} {}".format(padre.id, nodo.id)
                return self.ruta(padre) + "\n" + texto
        return ""

    def __str__(self):
        return self.ruta_bummer
