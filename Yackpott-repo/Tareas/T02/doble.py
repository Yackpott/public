from lista import Lista


class Doble:

    def __init__(self, grafo):
        self.texto = ""
        for nodo in grafo.lista:
            ruta = self.ruta(nodo)
            if ruta and str(nodo.id) not in self.texto:
                aux = str(nodo.id) + " " + ruta
                if aux.count(" ") > 2:
                    self.texto += "Ruta " + aux + "\n"
                else:
                    self.texto += "Par " + aux + "\n"

    def ruta(self, nodo, lista=None):
        if not(lista):
            lista = Lista()
        for arco in nodo.arcos:
            for arco_2 in arco.hijo.arcos:
                if nodo == arco_2.hijo and arco.hijo not in lista:
                    lista.append(nodo)
                    aux = str(arco.hijo.id) + " "
                    return aux + self.ruta(arco.hijo, lista)
        return ""

    def __str__(self):
        return self.texto
