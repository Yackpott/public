from lista import Lista


class NoCiclos:

    def __init__(self, grafo):
        self.grafo = grafo
        self.min = float("inf")
        self.minimo()

    def buscar(self):
        nodo = self.grafo.buscar_nodo(0)
        return self.recorrrer(nodo)

    def recorrrer(self, nodo, lista=None, ciclo=None):
        if not lista:
            lista = Lista()
        if not ciclo:
            ciclo = Lista()

        aux = None
        for i in range(len(lista)):
            for arco in lista[i]:
                for j in range(i + 1, len(lista)):
                    if arco in lista[j]:
                        if not aux:
                            aux = Lista()
                        aux.append(arco)
        if aux:
            return aux

        if nodo in map(lambda x: x.padre, ciclo):
            for i in range(len(ciclo)):
                if ciclo[i].padre.id == nodo.id:
                    lista.append(ciclo[i:])
            ciclo = Lista()
        for arco in nodo.arcos:
                ciclo.append(arco)
                return self.recorrrer(arco.hijo, lista, ciclo)
        return None

    def minimo(self, cont=0):
        if cont < self.min:
            lista = self.buscar()
            if lista is None:
                self.imprimir()
                self.min = cont
            else:
                for i in range(len(lista)):
                    arco = lista.popleft()
                    self.eliminar(arco)
                    self.minimo(cont + 1)
                    self.agregar(arco)
                    lista.append(arco)

    def imprimir(self):
        f = open("noCycle.txt", "w")
        f.write(str(self.grafo))
        f.close()

    def procedencia(self, arco):
        return self.grafo.buscar_nodo(arco.padre.id)

    def agregar(self, arco):
        padre = self.procedencia(arco)
        padre.arcos.append(arco)

    def eliminar(self, arco):
        padre = self.procedencia(arco)
        for i in range(len(padre.arcos)):
            if padre.arcos[i] == arco:
                padre.arcos.pop(i)
                break
