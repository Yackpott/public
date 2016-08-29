class Lista:

    def __init__(self, *args):
        self.cabeza = None
        self.cola = None
        self.len = 0
        for arg in args:
            self.append(arg)

    def __len__(self):
        return self.len

    def get_nodo(self, i):
        if i < 0:
            i = len(self) + i
        if i >= self.len:
            raise KeyError('Invalid key')
        nodo_actual = self.cabeza
        for cont in range(i):
            nodo_actual = nodo_actual.siguiente
        return nodo_actual

    def __getitem__(self, item):
        if isinstance(item, slice):
            indices = item.indices(len(self))
            aux = Lista()
            for item in range(*indices):
                aux.append(self.get_nodo(item).valor)
            return aux
        return self.get_nodo(item).valor

    def __iter__(self):
        nodo_actual = self.cabeza
        for i in range(self.len):
            yield nodo_actual.valor
            nodo_actual = nodo_actual.siguiente

    def append(self, valor):
        self.len += 1
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def pop(self, i=None):
        if i is None:
            i = self.len - 1
        if i == 0:
            nodo_actual = self.get_nodo(0)
            aux = self.cabeza
            self.cabeza = nodo_actual.siguiente
        elif i == self.len - 1:
            nodo_actual = self.get_nodo(i - 1)
            aux = nodo_actual.siguiente
            nodo_actual.siguiente = None
            self.cola = nodo_actual
        else:
            nodo_actual = self.get_nodo(i - 1)
            aux = nodo_actual.siguiente
            nodo_actual.siguiente = nodo_actual.siguiente.siguiente
        self.len -= 1
        return aux.valor

    def popleft(self):
        return self.pop(0)

    def __reversed__(self):
        aux = Lista()
        for i in range(len(self)):
            aux.append(self[len(self)-1-i])
        return aux

    def __repr__(self):
        rep = '['
        nodo_actual = self.cabeza

        while nodo_actual:
            rep += '{}, '.format(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        return rep[:-2] + "]" if len(rep) > 1 else "None"


class Nodo:

    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None
