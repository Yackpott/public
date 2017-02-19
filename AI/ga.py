# Objetive: minimize obj

import random

G_MAX = 10  # number of generations
C_MAX = 64  # number of cells
S_MAX = 128  # number of sons per gen
FUNC = None  # Some func
ARGS = None  # Some args for starting
E_FUNC = None  # Some random func


class Algorithm:
    _list = []
    _sons = []

    def __init__(self):
        self.first()
        for i in range(G_MAX):
            self.run()

    def first(self):
        for i in range(C_MAX):
            self._list.append(Cell(E_FUNC(ARGS, ARGS)))

    def run(self):
        for i in range(S_MAX):
            random.shuffle(self._list)
            father = self._list.pop()
            mother = self._list.pop()
            self._sons.append(Cell(E_FUNC(father.args, mother.args)))
        self._list = self._sons.sort(key=lambda x: x.obj)[0:64]
        self._sons = []


class Cell:

    def __init__(self, **kwargs):
        self.args = kwargs
        self.func = FUNC
        self.obj = self.func(self.args)
