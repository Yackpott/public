from collections import deque


class Traidores:

    def __init__(self, buffalos, rivales):
        self.traidores = []
        self.buffalos = buffalos
        self.rivales = rivales
        archivo = open(self.buffalos, "r")
        self.lista1 = set(archivo.readlines())
        archivo.close()
        archivo = open(self.rivales, "r")
        self.lista2 = set(archivo.readlines())
        archivo.close()
        for i in self.lista1:
            for j in self.lista2:
                if i == j:
                    self.traidores.append(i)


class Pizza():
    id = 0

    def __init__(self):
        Pizza.id += 1
        self.id = Pizza.id


class Pizzeria:

    def __init__(self, ruta):
        self.pila = list()
        self.cola = deque()
        self.ruta = ruta
        archivo = open(self.ruta, "r")
        self.intrucciones = archivo.readlines()
        archivo.close()
        for intruccion in self.intrucciones:
            if intruccion == "APILAR":
                self.apilar(Pizza())
            elif intruccion == "ENCOLAR":
                self.encolar(Pizza())
            elif intruccion == "SACAR":
                self.sacar()

    def apilar(self, pizza):
        pizza = Pizza()
        self.pila.append(pizza)
        print("Pizza {} apilada. {} pizzas apiladas - {} pizzas en cola".format(pizza.id, len(self.pila)), len(self.cola))

    def encolar(self, pizza):
        pizza = Pizza()
        self.cola.append(pizza)
        self.pila.pop()
        print("Pizza {} encolada. {} pizzas apiladas - {} pizzas en cola".format(pizza.id, len(self.pila)), len(self.cola))

    def sacar(self):
        pizza = self.cola.popleft()
        print("Pizza {} sacada. {} pizzas apiladas - {} pizzas en cola".format(pizza.id, len(self.pila)), len(self.cola))
