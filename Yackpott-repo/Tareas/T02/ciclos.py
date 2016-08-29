class Ciclos:

    def __init__(self, grafo):
        self.texto = ""
        for nodo in grafo.lista:
            self.texto += self.ruta(nodo)

    def ruta(self, nodo):
        for arco in nodo.arcos:
            for arco_2 in arco.hijo.arcos:
                for arco_3 in arco_2.hijo.arcos:
                    if nodo == arco_3.hijo:
                        for arco_4 in arco_3.hijo.arcos:
                            if nodo == arco_4.hijo:
                                return str(nodo.id) + " " + str(arco.hijo.id) + " " + str(arco_2.hijo.id) + " " + str(arco_3.hijo.id) + "\n"
                        return str(nodo.id) + " " + str(arco.hijo.id) + " " + str(arco_2.hijo.id) + "\n"
        return ""

    def __str__(self):
        return self.texto
